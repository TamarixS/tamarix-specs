# Design

## Context

Мотивация и границы — в [proposal.md](proposal.md), исходные решения — в
[requirements.md](requirements.md). Общие immutable shapes и key приняты
пользователем; полный контракт key подтверждён отдельно 2026-10-16.
Описанные ниже миграция и SQL-интерфейсы являются проектом для review,
а не утверждением о существующем коде или выполненном deployment.

Прочитанные источники и их применимость:

| Источник | Статус и применение |
| --- | --- |
| `AGENTS.md`, `openspec/config.yaml`, `openspec/context/README.md`, `architecture-principles.md` | Действующие правила store, scope, проектирования и проверки |
| `technology-stack.md`, `service-architecture.md`, `data-architecture.md` | Принятый стек, единственный владелец DDL; датированные TBD сверены с текущими SQL и docs |
| `api-guidelines.md`, `security.md`, `patterns.md` | Ограничения совместимости и доверия; рекомендации не превращаются в новые продуктовые требования |
| `testing.md`, `adr/README.md`, ADR 0001–0004 | Принятые границы T-1, локальных контрактов и integration/regression; сохраняются в применимой области |
| Основные `attributes/spec.md`, `containers/spec.md`; `docs/database.md`, `docs/api.md`, `docs/operations.md` | Текущие требования и описание runtime; поведение DN и admission не меняется |
| `db-control/src/db_control/sql/{0001_foundation,0002_storage,dn_codec}.sql` | Реальные FK/CHECK/guards, закрытые SQL-команды и views |
| `db-control/src/db_control/migrations/{env.py,versions/20261015_0003_dn_codec.py}`, `cli.py` | Transactional DDL, текущая head и существующий disposable safeguard downgrade |
| `db-control/tests/component/`, `TamarixTests/tests/integration/persistence/`, `registry.yaml` | Реальные test surfaces и формат стабильных ID; новые ссылки в tasks пока планируемые |
| `*/src/*/storage_sql.py`, container `tree_adapter.py`, PDP `persistence.py` | Consumers читают прежние fact views; DN lookup использует definition_id и comparison_version |

Сегодня definitions содержит semantic tuple, instances копируют её, values
копируют type/cardinality. Composite FKs замораживают используемую семантику;
single-index и deferred triggers контролируют мощность, equality guard реально
обновляет instance.mutation_version. Команды используют SERIALIZABLE/CAS.
Публичная предметная поверхность — Python/SQL; business HTTP/UI отсутствуют.

## Goals / Non-Goals

**Goals:** один точный immutable shape на определение, явное переиспользование
между определениями, сохранение декларативной структурной целостности и
совместимости текущих SQL/Python readers и writers. Подготовить один внутренний
validation path для будущих параметров формы.

**Non-Goals:** policy engine, новая топология данных, новые HTTP endpoints/UI,
зависимости или PostgreSQL major upgrade; regex/length/range, JSON framework,
semantic dedup, floating latest, наследование и редактирование shapes.

## Decisions

### 1. Точный immutable shape и самостоятельная идентичность definition

`attributes.shapes` получает BIGINT identity `id`, `key TEXT COLLATE "C"`,
`value_type`, `cardinality`, nullable `comparison_profile/comparison_version`.
Существующие CHECK допустимости semantic tuple переносятся из definitions:
string — exact/unicode_ci с непустой версией; DN — set/x509_rfc5280 с версией;
остальные нативные виды — без profile/version. Регистрация проверяет установленную
реализацию сравнения существующим require_comparison_version.

Key: NOT NULL, 1–512 ASCII `[A-Za-z0-9_-]`, unique index через существующий
`containers.ascii_ci(key)`. Whole-row BEFORE UPDATE guard запрещает любое
реальное изменение строки, включая id/key и будущие semantic columns.
Отдельная публичная операция удаления форм не вводится; ссылки используют
RESTRICT и runtime-роли не получают прямой DML.

`definitions` после перехода содержит id/key/shape_id. Применимость остаётся
на definition. `shape_id` обозначает точную запись, а не семейство версий;
comparison_version по-прежнему обозначает реализацию сравнения, а не форму.

Semantic UNIQUE по tuple не вводится: разные именованные формы могут иметь
одинаковые текущие параметры. Sharing выполняется явным выбором shape_id.
Это сохраняет выбранную пользователем границу без автоматического dedup.
Альтернатива — правила непосредственно в definitions — отклонена после
явного выбора переиспользуемых форм; version-family machinery пока не требуется.

### 2. Два независимых FK экземпляра

Четыре семейства owner/applicability/instance/value сохраняются. Instance
содержит неизменяемые `definition_id`, `shape_id`, `value_type`, `cardinality`,
владельца и прежнюю mutation_version. Все поля составных ссылок NOT NULL.

| Constraint | Назначение |
| --- | --- |
| shapes UNIQUE(id,value_type,cardinality) | Цель structural FK |
| definitions UNIQUE(id,shape_id), FK(shape_id) → shapes(id) RESTRICT | Существующая точная форма определения |
| instances FK(definition_id,shape_id) → definitions(id,shape_id) RESTRICT | Замораживает привязку definition при любом instance |
| instances FK(shape_id,value_type,cardinality) → shapes(id,value_type,cardinality) RESTRICT | Доказывает правильность structural copies |
| instances UNIQUE(owner_id,definition_id), UNIQUE(id,value_type,cardinality) | Прежние owner identity и цель values FK |
| values FK(instance_id,value_type,cardinality) → instances(...) ON DELETE CASCADE | Прежняя структурная целостность и удаление values |

RESTRICT означает immediate ON UPDATE/DELETE RESTRICT. Существующие owner,
subtype и applicability FK сохраняются, как и запрет DN у noncontainer pairs.
Зарегистрированный shape immutable независимо от использования; unused
definition может выбрать другую запись. При существующем instance запрещён
даже другой shape с равными параметрами. Назначение того же shape_id — no-op.

Альтернатива с проверкой отсутствия instances одним SELECT оставляет
конкурентную щель; ограничение выражается FK и его key locks.
Полное удаление type/cardinality copies перенесло бы локальные guarantees
values в собственный процедурный протокол, поэтому сохраняется гибрид.

### 3. Закрытые операции каталога и совместимость writers

Новые SQL interfaces в `db-control`:

| Операция | Контракт |
| --- | --- |
| register_shape(key,type,cardinality,profile?,comparison_version?) → BIGINT | Для string/DN требует явные profile и comparison_version; для прочих видов оба NULL. Валидирует key/tuple/реализацию и возвращает точный id; конфликт key отклоняется |
| register_definition_with_shape(key,shape_id) → BIGINT | Регистрирует definition по существующему shape, сохраняя прежние правила key |
| bind_unused_shape(definition_id,shape_id) → VOID | Блокирует definition, проверяет целевой shape и DN applicability, меняет ссылку под FK RESTRICT |

Исполнение новых mutators — только `tamarix_catalog_operator`. Функции
SECURITY DEFINER используют квалифицированные имена и `search_path=pg_catalog`;
PUBLIC EXECUTE отозван. Runtime/fact-reader не получают прямой DML или EXECUTE
внутренних validators. Статус владельца контейнера не заменяет полномочия каталога.

Старые сигнатуры `register_definition(...)` и `change_unused_semantics(...)`
сохраняются как compatibility wrappers. Если версия в прежнем вызове не задана,
wrapper разрешает её через прежний registry и передаёт конкретную версию
новой регистрации формы. Первая создаёт отдельный shape и definition атомарно.
Вторая сначала валидирует вход и сравнивает всю tuple
с текущим shape через NULL-safe equality: совпадение сохраняет прежний no-op;
различие создаёт новый shape и пытается перепривязать definition. Отказ не
оставляет лишнюю форму. Новые автоматически создаваемые keys имеют вид
`legacy_shape_<allocated_id>` с обработкой коллизий при атомарной регистрации;
совпавшая семантика чужого shape не выбирается неявно.

`set_applicability` и bind берут одну definition row lock до чтения shape
и проверки DN. Это сохраняет инвариант при гонке applicability ↔ rebind.
Невалидная запись каталога/привязка отклоняется с прежними PostgreSQL-классами
ошибок constraint/unknown/privilege; конфликт shape key — unique violation.
Новый HTTP error mapping не вводится.

### 4. Общий validation/equality path и прежний CAS

`apply_changes` заменяет record `definition attributes.definitions` на
joined metadata definition+shape. Новые instances получают оба pin-поля и
структурные копии. `guard_value_equality` сохраняет реальное UPDATE выбранного
instance, затем читает immutable shape и выполняет прежнее полное сравнение.
Общая строка shape при записи values не обновляется и не блокируется FOR UPDATE.

Внутренний `validate_shape_value(shape,value_input)` централизует вход к
существующей typed validation; в этой поставке дополнительных условий нет.
Будущая фича добавит параметры в новые shapes и проверку в этот validator,
с собственными specs/tests. Дочерние mutable rules, обходящие immutable row,
не создаются. CHECK, single-index, deferred count и instance fencing сохраняются.

String exact и Unicode D145, исходное написание и пробелы сохраняются. DN DER
и DB-derived comparison keys не пересчитываются из-за переноса metadata.
require_comparison_version продолжает закрывать несовместимую реализацию.
Все user commands сохраняют SERIALIZABLE, порядок блокировок, whole-transaction
retry 40001 и исходный expected_revision; shape ID не заменяет aggregate CAS.

### 5. Совместимые views и отдельное чтение каталога форм

Существующие definition/instance/active-subject/DN fact views заменяются
явными проекциями JOIN shapes с прежними именами, порядком, типами и collation
колонок. В частности, `containers.dn_facts` продолжает выдавать definition_id
и comparison_version. Новые поля не добавляются к старым SELECT * contracts.

Новые `attributes.shape_facts` возвращает id/key/semantic tuple,
`attributes.definition_shape_facts` — definition_id/shape_id/shape_key.
SELECT предоставляется существующим catalog и fact-consuming ролям по той же
границе глобальных metadata. Private таблицы остаются закрытыми.

CREATE OR REPLACE VIEW позволяет сохранить ownership/grants и изменить
источник вычисления при сохранённой сигнатуре колонок
([PostgreSQL CREATE VIEW](https://www.postgresql.org/docs/18/sql-createview.html)).
Альтернатива с DROP CASCADE разрушала бы зависимости; добавление shape_id
в старые views меняло бы контракт потребителей.

### 6. Владение и проверка

Все DDL/routines/views/grants и обратные SQL ресурсы принадлежат `db-control`.
Сервисы продолжают использовать прежние SQL/Python контракты; изменения их
кода не являются предпосылкой миграции. Component tests обновляют raw SQL
fixtures под новую схему. Межсервисные проверки принадлежат `TamarixTests`:
реальный PostgreSQL, native LOGIN, публичные catalog/domain routines и readers.
HTTP health и in-memory kernels не подменяют этот scope.

Новые stable IDs — `persistent-shapes-c01…`; прежние attributes c17/c18
сохраняют смысл empty/tombstone freeze и обновляются на rebind shape.
Tasks содержит точные Requirement/Scenario → planned node ID связи.
Registry начинает с candidate; promotion и готовый полный отчёт нужны перед
archive. Набор change уже включает текущий регресс, отдельный повтор без
новой причины не требуется. Все новые/изменённые tests имеют русские описания.

При применении обнаружено, что прежний gate проверял покрытие только registry
TamarixTests. Component-only проверки FK/immutability/перехода не подменяются
integration links. Дополнение после пользовательского «продолжи»:
`component-evidence.json`, `component-results.json`, `component-summary.md`
сохраняют точные criterion links и raw PASS report db-control. Runner фиксирует
до collection commit/clean/source/resource/test hashes и сверяет их после
прогона. Gate проверяет hashes, время, завершённость, каждый PASS node и русский
docstring; commit/resources/Python/packages должны совпадать с integration
manifest.db_control. Архив сохраняет immutable test source snapshots и bundle
hashes. Полный integration report остаётся обязательным; старые archives без
дополнительного bundle сохраняют прежнюю валидацию.

Зависимости и server major не обновляются. Используются текущие pins проекта;
их manifest проверяется в согласованных прогонах. Любая необходимость обновления
зависимостей требует отдельной оценки совместимости, а не молчаливого bump.

## Migration Plan

1. Новая Alembic revision следует за `20261015_0003` и включает необходимые
   SQL resources. Старые revisions не переписываются. Одна транзакция с
   transactional DDL выбрана вместо распределённого dual-write: текущие
   contracts позволяют переключить хранение атомарно в обслуживаемом окне.
2. Перед эксплуатационным запуском определить окно, проверить backup/recovery
   и остановить приём новых writers/catalog mutations, дождаться drain.
   Выставить ограниченные lock/statement timeouts по измерению целевой БД;
   lock failure прерывает весь upgrade. Брать затронутые таблицы в одном порядке.
3. Зафиксировать до/после fingerprints: IDs/key, definitions tuple,
   applicability, instances/values, DN bytes/keys, aggregate revisions,
   view column signatures/ACL. Shape backfill не вызывает команд владельцев
   и не увеличивает пользовательские revisions или instance mutation_version.
4. Создать shapes и временно nullable shape_id columns. Для каждого прежнего
   definition создать отдельный shape с key `migrated_definition_<definition_id>`;
   сохранять точную tuple, включая прежнюю comparison_version. Автоматического
   объединения совпадающих definitions нет. Сохранить проверяемый map в отчёте.
5. Заполнить references definitions/instances. Существующие deferred
   scalar-count triggers получают события от UPDATE instances: до последующих
   ALTER TABLE выполнить накопленные проверки через SET CONSTRAINTS ALL
   IMMEDIATE. Это ретроактивно выполняет отложенные проверки
   ([PostgreSQL SET CONSTRAINTS](https://www.postgresql.org/docs/18/sql-set-constraints.html)).
   Новый guard immutable shape_id установить после backfill.
6. Добавить и проверить UNIQUE/FK/NOT NULL, заменить routines и view projections,
   выставить узкие ACL. До удаления прежних колонок убрать зависимости views,
   CHECK и FK от них; перенести нужные ограничения в shapes. Не применять
   DROP CASCADE как способ обхода незамеченных зависимостей.
7. Сверить fingerprints и map, удалить physical semantic columns definitions
   и comparator columns instances. Values/payload и comparison registry
   остаются прежними. Commit публикует целую новую схему; затем возобновить writers.
8. Проверить старые consumers, новую регистрацию/назначение и повторный upgrade
   head. Полный migration parity test в `db-control` сначала ставит именно
   0003 через Alembic API, заполняет старую схему, затем делает upgrade head:
   integration fixture, всегда создающий head, эту проверку не заменяет.

**Rollback и восстановление.** Сбой до commit откатывает схему и данные в
транзакции. После commit совместимые wrappers/views позволяют продолжить со
старыми runtime consumers и исправить дефект следующей миграцией. Production
recovery требует проверенного backup/PITR и плана для данных после backup;
восстановление старого снимка не объявляется сохранением новых записей.

Обратный SQL new revision → 0003 поддерживается только в явно disposable
`tamarix_t3_*` БД с существующим safeguard. Он восстанавливает старые columns,
FK/routines/views из shapes; новая информация shape id/key/sharing теряется
и это проверяется/документируется отдельно. Текущий CLI downgrade всегда идёт
до base и не используется как production rollback. Продление CLI до выбора
произвольной revision не требуется: component migration tests используют
существующий Alembic API. Проверка отказа без safeguard предшествует мутациям.

Обратная фазировка: добавить прежние semantic columns, заполнить их JOIN
shapes без изменения пользовательских revisions, выполнить отложенные scalar
checks через SET CONSTRAINTS ALL IMMEDIATE, восстановить старые instance
guards/routines/view projections и FK. Затем снять новые composite FK и
зависимости shape_facts/definition_shape_facts/validator с composite-аргументом
shapes; только после этого удалить shape_id columns и каталог shapes.
Полный downgrade base не заменяет тест заполненного round trip
new → 0003 → head с DN, empty set и tombstone. Потеря нового каталога на
обратном шаге допускается только как явно destructive test-only поведение.

## Risks / Trade-offs

- Дополнительные JOIN чтения metadata → PK/UNIQUE indexes уже поддерживают
  выбранные связи; проверить планы характерных reads без необоснованных индексов.
- Общая форма делает mutable UPDATE опасным → whole-row guard и закрытые ACL,
  тест изменения каждого поля unused/shared shape; FK сам не замораживает payload.
- Неатомарный semantic rebind/applicability → одна definition lock и FK RESTRICT,
  обе очередности гонок проверяются реальными транзакциями.
- Удаление columns оставляет view/record dependencies → явный inventory,
  новый joined record и прежние view signatures, migration tests заполненной БД.
- Долгая migration/ожидание lock → drain, timeouts и измерение representative
  объёма до rollout; обещание online/no-downtime не даётся.
- Автоматические migration/legacy keys менее выразительны для UI → формы
  доступны по точному id/key; осмысленный новый shared shape регистрируется явно.
- Downgrade не представляет новый каталог → production fix-forward/recovery,
  обратная destructive проверка ограничена disposable средой.

## Open Questions

Продуктовых вопросов по контракту shapes/key не осталось. Численные timeout
budgets, объём целевой БД, длительность окна и конкретный backup/PITR runbook
определяются эксплуатационным review до deployment по измерениям среды. Они
не меняют выбранную атомарную миграцию, specs или состав implementation tasks;
готовность planning artifacts не является разрешением production deployment.
