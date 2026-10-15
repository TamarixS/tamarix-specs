# Design

Статус исполнения: технический baseline принят к реализации через вызов apply
и продолжение работы; результат независимого review и источник разрешения —
[design-review.md](design-review.md). Конкретные DTO/команды —
[storage-contracts.md](storage-contracts.md), проверенные pins и отдельно
разрешённая CD dependency — [dependency-baseline.md](dependency-baseline.md).
Ниже сохранено описание выбора и альтернатив; кандидатные формулировки
не означают новый запрос подтверждения уже разрешённой реализации.

## Context

Мотивация и принятая граница — [proposal.md](proposal.md). Исходные решения —
[requirements.md](requirements.md). Пользователь отдельно подтвердил:
основа хранения завершается в T-3, очистка модельных ссылок и полноценный PDP
переносятся в следующий change. Этот design предлагает конкретные технические
механизмы для review; их статус не подменяет явное принятие до реализации.

Наблюдаемый код:

- `container-adm-api/src/container_adm_api/core.py`: `ContainerTree` проверяет
  один корень и индексирует `CompositeKey` как кортеж одних ключей. Это несовместимо
  с forest и типизированной идентичностью без согласованного изменения контрактов.
- `entity-subject-adm-api/src/entity_subject_adm_api/core.py` и
  `policy-adm-api/src/policy_adm_api/core.py`: чтение/проверка/`save` разделены;
  текущая подмена repository на SQL не создаёт транзакцию и CAS автоматически.
- `policy-adm-api/src/policy_adm_api/facts.py`: `ModelRecord` содержит произвольный
  Python `content` и ссылки. Он не является готовым persistence-форматом.
- `policy-decision-api/src/policy_decision_api/ports.py` и `core.py`: известные
  модели, неизвестный набор и Undefined вычисления имеют разные значения.
- В `db-control` обнаружен только `openspec/config.yaml`; DDL/Alembic отсутствуют.
- В пяти ядрах есть pure-Python пакеты и тесты; runtime/CD предоставляет health,
  а существующая межсервисная интеграция соединяет ядра в памяти.
- Runner `TamarixTests` и manifest helper `TamarixCD` пока допускают
  `logical-integration`/`http`, но не отдельную PostgreSQL integration среду.

Прочитанные источники: `AGENTS.md`, `openspec/config.yaml`, context
`README.md`, `architecture-principles.md`, `technology-stack.md`,
`service-architecture.md`, `data-architecture.md`, `api-guidelines.md`,
`security.md`, `patterns.md`, `testing.md`, реестр ADR и принятые ADR 0001–0004;
все четыре основные specs T-1, архив T-1 и доступный код указанных репозиториев.
Context сохраняет исторические TBD; решения текущего обсуждения не переписывают
его автоматически. Фактические внешние production-данные не исследованы.

## Goals / Non-Goals

**Goals:** целостная PostgreSQL основа, локальные адаптеры записи/чтения,
однозначное равенство ключей и значений, атомарность, CAS, lifecycle и реальные
проверки БД. Подготовленные факты пригодны для последующего PDP без потери
различия между полным и неизвестным составом.

**Non-Goals:** внутренности моделей/привилегий/actions и их очистка, persistent
evaluator/PDP целиком, новые HTTP routes, TLS/PKI deployment, назначения,
tenant/RLS-модель, брокер, outbox и кэш. Metadata не сериализует произвольный
Python `content`. Полный PDP и cleanup получают отдельный будущий change.

## Decisions

### 1. Рабочая физическая структура и владельцы

Приняты одна БД и отдельные схемы; предлагаются следующие конкретные имена:

| Схема | Основные таблицы | Владелец предметной записи |
| --- | --- | --- |
| `containers` | `nodes` | `container-adm-api` |
| `subjects` | `types`, `subjects` | Субъекты: `entity-subject-adm-api`; каталог: отдельная глобальная роль |
| `objects` | `objects`, `key_guards` | `entity-object-adm-api` |
| `policies` | `models` только metadata | `policy-adm-api` |
| `attributes` | `definitions`, четыре applicability relation, четыре пары instances/values | Значения: сервис владельца; definitions/applicability: глобальная роль |

Все DDL, функции, триггеры, роли, views и Alembic revisions находятся только
в `db-control`. `db-control` поставляет deployment-артефакты, не становится
runtime-посредником. Общий пакет внутренних Python DTO не создаётся.

Альтернатива общей polymorphic таблицы значений отклонена согласованным выбором
четырёх пар: прямые FK и права каждой предметной роли проще проверить.
Независимые БД не соответствуют выбранной топологии и усложнили бы атомарность.

### 2. Идентичность и ключи

Основные строки содержат PostgreSQL-generated `BIGINT` ID и положительную
`revision`. Начальная revision предлагается равной 1. Последовательности не
обещают непрерывности и не являются счётчиками успешных операций.

Предлагается сохранять исходное написание ASCII-ключа; индексировать явное
ASCII-преобразование `A–Z -> a–z`, не locale-зависимое Unicode lower.
Root unique index действует по `(type, key_ci)` при `parent_id IS NULL`,
child unique index — `(parent_id, type, key_ci)` для остальных строк.
Две частичные уникальности явно реализуют принятую семантику корней.

Subjects: `UNIQUE(holder_id, type_id, key COLLATE "C")` без фильтра `deleted_at`.
Models: `UNIQUE(holder_id, key_ci)`. Catalog keys имеют собственные CI unique
indexes. CHECK проверяет допустимый алфавит/длину. Для Unicode keys предлагается
считать символы как Unicode code points и запрещать категорию Cc; эти детали
валидатора входят в review. Пробелы не обрезаются, нормализация не выполняется.

Базовая конфигурация: UTF8, стандартные страницы PostgreSQL не менее 8 KiB;
это проверяется до миграции, чтобы bounded subject key 512 символов помещался
в выбранный индекс. Для другого block size нужен пересмотр индекса, а не
незаметное сокращение допустимой длины ключа.

### 3. Деревья и JSON-адрес

`nodes` содержит `id`, `parent_id`, `type`, `key`, `revision` и отдельный
технический `lifecycle_version`. FK parent — RESTRICT; триггер проверяет
строгое увеличение ранга типа. Структурные поля защищены от UPDATE в БД.
Неизменяемые parent/type и максимум четыре уровня исключают новые циклы.

Адрес разбирается с обнаружением повторённых JSON member names до свёртки
в обычный mapping. Типы упорядочиваются по фиксированному рангу; разрешение
использует root/sibling indexes и не более четырёх фактических уровней в одном
SQL snapshot. Путь для выдачи строится рекурсивным чтением parent; полный JSON
не сохраняется. Рекурсивное чтение дополнительно контролирует полноту пути.

В `container-adm-api` вводится type-aware адрес, а потребители получают локальные
DTO. Нельзя загрузить forest в старый `ContainerTree` или сохранить key-only
индекс: это снова склеит разные типы. Структурные проверки T-1 работают по ID
и фактическим родителям. Изменение старого контракта проводится согласованно
в пяти пакетах и соответствующих тестовых адаптерах без общего runtime-пакета.

### 4. Длинные ключи объектов

`objects.objects` хранит полный `key TEXT COLLATE "C"` и digest-кандидат;
индекс `(holder_id, digest)` неуникальный. `key_guards` имеет уникальный
`(holder_id, digest)` и техническую версию.

Внутри обязательного DB write path вычисляется SHA-256 полного UTF8 ключа,
создаётся/находится guard, выполняется его реальный MVCC UPDATE, затем полное
сравнение строк в bucket и вставка. Разные ключи при одном digest разрешены.
Неизменяемый key исключает обход через UPDATE; прямые обходные INSERT роли
запрещены, enforcement также проверяется в БД. Guard живёт до удаления держателя,
что избегает отдельной гонки удаления/повторного создания bucket.

Простой unique digest отвергнут: он отверг бы разные строки при коллизии.
Обычный unique B-tree по произвольному TEXT отвергнут из-за размера записи.
Одна advisory/row lock без обновления не решает старый RR snapshot. Выбран
реальный UPDATE и полный повтор транзакции при конфликте снимка; invisible
конкурентная вставка guard не считается доказательством отсутствия ключа.
FK guard к держателю использует ON DELETE CASCADE: служебный bucket не должен
блокировать удаление контейнера, у которого уже удалены объекты.
[Основание: PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

### 5. Definitions, applicability и четыре пары атрибутов

`definitions` содержит ID, неизменяемый каталоговый key, value type,
cardinality, string profile и версию реализации сравнения. В каждой owner pair:

- Instance: ID, прямой owner FK, definition ID, structural metadata и отдельная
  техническая версия. `UNIQUE(owner_id, definition_id)`.
- Value: ID, instance FK, ровно один из нативных value columns и технические
  данные, необходимые профилю. Полиморфного owner key без FK нет.

Instances ссылаются составным FK на ненулевую тройку definition/type/cardinality;
это блокирует изменение структурной семантики даже у пустого instance.
String profile проверяется отдельно с обязательностью у строк: nullable member
в одном FK с MATCH SIMPLE не должен отключить всю защиту. Для DN действует
собственный профиль из решения 7. Structural FK не использует UPDATE CASCADE.
Защита охватывает также версию реализации сравнения: изменение номера версии
при том же имени profile не должно обходить freeze существующих instances.

Четыре applicability relation задают container type, subject type, object kind
и model kind. Для typed owners копия subtype в instance связана FK с реальным
owner и applicability; её нельзя произвольно заявить при записи значения.
Предлагается RESTRICT для используемых definitions/types/applicability.
Каталоговые удаления и смена применимости публичными командами T-3 не вводятся;
DB restriction остаётся конкретным предложением защиты целостности на review.

### 6. Значения, cardinality и равенство

Нативные columns: TEXT, BIGINT, NUMERIC, BOOLEAN, DATE, TIMESTAMPTZ. CHECK
требует ровно один заполненный column нужного типа. Existing instance без
values — пустое множество только для set; отсутствие instance — отсутствие.
Scalar ≤1 обеспечивается уникальностью, scalar =1 на commit — deferred
constraint trigger. При удалении instance/owner проверка больше не требует
существования удалённого scalar.
Проверки заполненности различают SQL NULL и допустимые нулевые значения:
`0`, `false` и пустая строка не считаются отсутствием value column.

Перед изменением values выполняется реальный UPDATE технической версии instance.
Затем значения сравниваются целиком внутри instance по declared type/profile.
Это исходный механизм exact set uniqueness без ограничения длины TEXT или
размера NUMERIC индексом. Дополнительные candidate indexes допустимы позднее
после измерений, но не меняют равенство и не заменяют полное сравнение.

`exact` — точное UTF8 сравнение. `unicode_ci` — D145
`NFD(toCasefold(NFD(x)))`, результат сравнивается точно; оригинал сохраняется.
Предлагается DB implementation на `normalize`/`casefold` с явно выбранной
builtin collation `pg_unicode_fast`, если проверенный стабильный PostgreSQL
поддерживает этот набор. `unicode_version()`/major и реализация фиксируются
в manifest и версии профиля. Молчаливое изменение равенства при major upgrade
запрещено; неподдерживаемая версия блокирует запуск записи.

NUMERIC сравнивается нативным равенством, не строкой (`1` равно `1.0`),
TIMESTAMPTZ — как момент времени, не исходный offset. Пробелы строк значимы.
[SQL string functions](https://www.postgresql.org/docs/current/functions-string.html),
[collations](https://www.postgresql.org/docs/current/collation.html),
[Unicode D145](https://www.unicode.org/versions/latest/core-spec/chapter-3/).

### 7. DN — значение контейнерного атрибута

Предлагается седьмой специальный value type `DN`: исходный ASN.1 Name DER
в `container_values`, производный matching key и версия X.509 профиля.
Применимость — только контейнеры; definition DN регистрируется явно и узнаётся
по доверенному ID определения, а не по произвольному имени клиентского атрибута.
Самостоятельные DN registry/bindings не создаются. Одинаковый DN в разных
контейнерах разрешён; внутри instance используется общее set enforcement.

Авторитетный codec реализуется в функциях БД из `db-control`: DER parsing,
проверка структуры Name/RDN/AVA, сохранение порядка RDN и независимость от
порядка AVA внутри RDN, OID и значение входят в однозначное matching encoding.
Подготовка поддерживаемых строк следует RFC 5280/RFC 4518 с закреплёнными
таблицами Unicode 3.2; это другой алгоритм, чем D145 обычных атрибутов.
Для неизвестного OID поддерживаемый DirectoryString подготавливается,
прочее значение кодируется для точного DER сравнения. Неуспех подготовки
поддерживаемого значения не маскируется fallback на другое равенство.

Codec и его тестовые векторы поставляются и версионируются `db-control`;
SQL/PLpgSQL и неизменяемые таблицы подготовки не требуют PL/Python runtime.
Клиент не передаёт авторитетный matching key. Тесты проверяют обе стороны:
регистрацию и преобразование установленного сертификатного Name.
Если полный набор поддерживаемых кодировок/подготовки не подтверждён,
DN-задача остаётся открытой; обычный `Name.__eq__`, lowercase или DER всего
имени не считаются реализацией выбранного профиля.

PKI проверка цепочки сертификата остаётся внешней границей: адаптер получает
установленный факт аутентификации T-1 и извлекает Name. JSON клиента не может
заменить этот факт. Проверка допуска ищет DN у конкретного `O` через values;
metadata snapshot не назначает единственный контейнер по глобальному DN.
[RFC 5280](https://www.rfc-editor.org/rfc/rfc5280.html#section-7.1),
[RFC 4518](https://www.rfc-editor.org/rfc/rfc4518.html).

Альтернатива дополнительному типу — специальный string profile с обратимой
сериализацией Name; она сложнее сохраняет неизвестные ASN.1 значения.
Поэтому предлагается DN type, но он требует явного принятия на review T-3.

### 8. Транзакции и aggregate revision

Предлагаются синхронные SQLAlchemy/Psycopg 3 адаптеры и одна session/transaction
на application command. Administrative writes — SERIALIZABLE: admission,
views/facts, проверки ядра, CAS целевого агрегата, его attributes и commit.
Нельзя открыть отдельный repository transaction между проверкой и save.

CAS принимает исходную expected revision; успешная логическая мутация меняет
revision агрегата один раз. Начальная запись получает 1. Attribute/DN команды
проходят через тот же aggregate path; technical instance/lifecycle versions
не выдаются за публичную revision. No-op предлагается оставлять без изменения.

`40001`/`40P01` означают полный повтор транзакции с теми же входами и исходной
expected revision, с ограничением числа попыток. Обнаруженный stale revision
возвращает конфликт; свежий token вместо клиента не подставляется. Порядок
захвата lifecycle/owner/instance locks фиксируется, а race tests проверяют его.
Источник SERIALIZABLE — design candidate, не ранее принятое условие пользователя.

### 9. Lifecycle и защита удаления контейнера

Subject identity unique охватывает tombstones. Soft delete меняет deleted_at
и revision, сохраняя attributes; restore очищает deleted_at в прежней записи
с прежним ID. Lookup активных субъектов исключает tombstones, административное
чтение и восстановление могут их находить.

Object/model metadata удаляются физически с собственными attributes. Holder
FK для objects/models и parent FK — RESTRICT. Subject holder FK позволяет
purge при удалении контейнера; BEFORE DELETE subject guard дополнительно
запрещает физическое удаление активной записи. Проверка только parent precheck
была бы недостаточна при конкурирующем restore.

Создание/удаление held entities, создание детей, soft delete/restore и удаление
держателя используют общий lifecycle gate — реальный UPDATE его технической
версии. Delete держателя проверяет отсутствие детей, активных subjects,
objects/models, затем атомарно удаляет tombstones и собственные attributes.
Restore выигрывает гонку и препятствует purge либо после purge получает
NotFound/conflict; активный субъект физически не удаляется.

T-3 не создаёт model-reference tables или временные привилегии. Поэтому lifecycle
integration подтверждает собственные данные и attrs, а не cleanup непустых
модельных ссылок. До будущего change записи внутренних ссылок в эту БД
не поддерживаются. Будущее хранилище обязано добавить атомарный cleanup и bump
affected model revisions без клиентских tokens всех затронутых моделей.
Совместный rollout будущих ссылок без этого enforcement недопустим.

### 10. Каталоги и DB roles

Предлагается отдельная DB роль `catalog_operator`, с EXECUTE ограниченных
catalog routines регистрации types/definitions/applicability. Runtime HTTP
владелец каталоговых операций этим не назначается; SQL contract обеспечивает
доступный интерфейс оператора без нового сервиса. Bootstrap выполняется
эксплуатационным migration executor, после него обычные services не получают
глобальных каталоговых полномочий.

Отдельный bootstrap candidate для review: initial root и его первичный DN
может атомарно provision привилегированный эксплуатационный executor через
проверенные routines, после регистрации DN-definition. Это не выводится из
владения DDL, не является новым runtime create-root API и не предоставляется
`catalog_operator`. Root без DN остаётся допустимым, если доступ от его имени
не требуется. Идентичность/Name bootstrap поступает из доверенного
эксплуатационного ввода. Создание ребёнка в runtime проверяет существующего
родителя в области управления; переименование/attrs/delete существующего D
проверяют `O <= C <= D` по фактическому дереву.

Предметные write roles получают свои routines и read-only foreign facts views,
PDP role — только SELECT на разрешённые views. Нет DDL/TRUNCATE/широкого DML
для runtime ролей. Narrow SECURITY DEFINER functions имеют фиксированный
search_path, квалифицированные имена, закрытый PUBLIC EXECUTE и отдельного
non-login owner. Это предложение разграничения БД, не замена проверки `O<=C<=D`
или доверия сертификату в application boundary.

### 11. Views, metadata snapshot и граница PDP

Views публикуют узлы/родителей, DN values, активных субъектов, объекты,
model metadata и attributes. Snapshot reader `policy-decision-api` открывает
одну READ ONLY REPEATABLE READ транзакцию до первого чтения и собирает весь
запрошенный набор в ней. Неизвестный root/path/контейнер не становится пустым.

Model metadata set — отдельный тип от готового `CompleteModelSet` T-1.
Views могут подтвердить IDs/holders/revisions и явный пустой metadata set;
они не подтверждают наличие тела/privileges/evaluator. T-3 reader не подключается
как полный persistent provider к production PDP и не выдаёт metadata как
известную модель с Undefined. Семантика T-1 остаётся без изменений.
Будущий change подключит model provider и общий RR snapshot всех фактов.

### 12. Проверки и прослеживаемость

Все delta THEN/AND criteria связываются в tasks с планируемыми стабильными
test ID и конкретными parameter node IDs TamarixTests; текущий archive gate
проверяет именно registry links. Component tests `db-control` и сервисов
дополнительно проверяют механизмы, но не заменяют эту связь.

Граница integration — реальные адаптеры, DB roles и PostgreSQL после миграций
`db-control`, без `create_all` или тестового DDL. Конкурентные тесты используют
независимые соединения, барьеры и реальные commit/rollback. Hash collision
проверяется изолированным test seam candidate bucket, сохраняя production hash
и полный comparator; поиск настоящей SHA-256 коллизии не требуется.

Предлагаемый manifest scope — `postgresql-integration`, с PostgreSQL
version/image digest, `db-control` commit/Alembic head, commits пакетов и ID
одноразовой БД. DSN идёт через secret env, не в manifest/evidence. Для наборов
с несколькими commit используется отдельная БД прогона/случая и гарантированная
очистка, а не один общий rollback fixture.

Runner validation расширяется в TamarixTests; readiness/manifest producer
и запуск среды требуют отдельного локального change TamarixCD. Его результат
фиксируется внешней зависимостью, без edits CD в рамках центрального planning.
HTTP e2e и настоящая PKI не заявляются. Новые tests содержат русские docstrings,
case descriptions, registry description; каждый запуск сохраняет отдельные
русский/JSON отчёты, включая ошибки/отмены, и актуальный регресс T-2.

## Risks / Trade-offs

- [Сложность DN codec] -> Разобранный профиль, неизменяемые таблицы подготовки,
  положительные/негативные и межкодировочные векторы; отдельное принятие решения.
- [Сериализация больших множеств] -> Простой полный comparator обеспечивает
  корректность; измерения определяют последующие candidate indexes.
- [Повторы и deadlocks] -> Ограниченные whole-transaction retries с прежним
  expected token, единый порядок locks и независимые race tests.
- [Обход агрегата прямым DML] -> Runtime EXECUTE roles, DB guards и негативные
  проверки прав; migration role используется только при поставке.
- [Смешение metadata и исполнимой модели] -> Разные DTO/providers; полный PDP
  и cleanup остаются за принятой границей следующего change.
- [Новая среда отсутствует в CD] -> Явная внешняя зависимость PostgreSQL manifest;
  незапущенный integration набор не считается PASS или основанием archive.
- [Изменение Unicode при upgrade] -> Версия профиля/движка фиксируется; major
  upgrade и переход семантики требуют отдельной миграции/review.

## Migration Plan

1. До реализации принять этот design, в частности DN type/codec, SQL каталоговый
   интерфейс, SERIALIZABLE и DB role contract. Зафиксировать результат review
   в T-3; архитектурную запись оформить в принятом проектом порядке отдельной
   согласованной задачей. Planning не меняет context/ADR автоматически.
2. Проверить официальные stable releases и совместимость Python/SQLAlchemy/
   Psycopg/Alembic/PostgreSQL, зафиксировать pins без обновления T-1 по привычке.
   Runtime baseline должен поддерживать выбранные Unicode functions.
3. Migration executor `db-control` проверяет UTF8, block size и исходную схему;
   устанавливает baseline, constraints/functions, roles и views. Неизвестная
   существующая схема требует отдельного плана преобразования; данные не стираются.
4. Поставить согласованные local DTO и storage adapters всех затронутых пакетов.
   Старый tuple-only natural address нельзя молча трактовать как JSON address;
   callers и тестовые adapters обновляются совместно. Публичных routes сейчас нет.
5. Подготовить PostgreSQL integration среду через результат локального CD change,
   выполнить migration/component проверки, registry collection, новые cases и
   текущий regression по требованию; сохранить manifest/отчёты/traceability.
6. Подтвердить promotion и итоговые commits, повторить полный набор для них,
   сохранить verification/evidence и пройти существующий archive gate.

На одноразовой тестовой БД проверяются upgrade на пустой базе, повторный
`upgrade head`, downgrade/upgrade и права после повторного развёртывания.
До записи полезных данных baseline можно откатить проверенным downgrade.
После появления данных предпочтителен forward fix; destructive downgrade
требует отдельного согласованного восстановления из проверенной backup.
Обновление PostgreSQL major не совмещается с baseline migration автоматически.

## Open Questions

За пределами T-3 остаются конкретные wire endpoints/HTTP errors, PKI deployment,
объёмы/SLO и внутренности моделей. Они не меняют выбранную основу хранения;
создание model references и подключение полного PDP потребуют следующего change
с собственными specs, cleanup, snapshot и тестами.
