# API и локальные контракты

Документ описывает фактический код на 2026-10-15. Сейчас доступны три разные
границы: HTTP health endpoint в CD runtime, локальные Python интерфейсы
предметных пакетов и deployment/SQL интерфейсы `db-control`.
Бизнес REST API пока не подключён. Имена команд ниже не являются URL.
Обязанности компонентов и потоки показаны в [services.md](services.md),
данные и SQL гарантии — в [database.md](database.md).

Быстрый переход: [HTTP](#http-единственный-реализованный-route) ·
[ID и context](#адреса-id-и-контекст-допуска) ·
[Application methods](#административные-application-methods-t-3) ·
[Prepared reader](#prepared-facts-reader-t-3) ·
[Логические контракты](#логические-операции-и-порты-t-1) ·
[Каталоги SQL](#sql-интерфейсы-каталогов-и-bootstrap) ·
[db-control CLI](#deployment-cli-db-control).

## HTTP: единственный реализованный route

Источник: [TamarixCD runtime/app.py](../../../TamarixCD/runtime/src/tamarix_runtime/app.py)
и [runtime README](../../../TamarixCD/runtime/README.md).

| Метод и путь | Вход | Ответ | Назначение |
| --- | --- | --- | --- |
| `GET /health` | Без тела и обязательных параметров | `200`, JSON со строковыми `status`, `service`, `launch_id`, `scope` | Подтверждает живой процесс, выбранный сервис и импорт `core/facts/ports` |

```sh
curl --fail http://127.0.0.1:8101/health
```

Для процесса `container-adm-api` с `--launch-id manual-1` ответ имеет вид:

```json
{
  "status": "ok",
  "service": "container-adm-api",
  "launch_id": "manual-1",
  "scope": "development"
}
```

При создании приложения импорт ядра проверяется до объявления route;
невозможность импортировать модуль завершает startup. Runtime поддерживает
пять пакетов: container, subject, object, policy administration и decision.
`db-control` и `access-assignment-api` в список runtime не входят.
Автоматические `/docs`, `/redoc`, `/openapi.json` явно отключены.

Это readiness только в узкой области процесса/импорта. Endpoint не открывает
БД, не проверяет schema head, DB role, сертификаты или бизнес-команды.
`POST /subjects`, `/objects`, `/policies`, `/access/evaluations` и другие
business routes в текущем коде отсутствуют. HTTP схемы ошибок, status codes
предметных отказов, pagination, versioning, idempotency keys и AuthZEN profile
ещё не определены; Python outcomes нельзя автоматически выдавать за эти схемы.

## Правила локальных Python контрактов

Каждый пакет определяет собственные типы. Используйте `facts`, `address`,
`storage_types`, `persistence` выбранного пакета; одинаковое имя класса в
соседнем пакете не означает совместимый Python объект. Адаптеры явно
преобразуют типы, сегменты `(kind,key)` и refs. Ни один DTO не задаёт
публичный wire format.

Есть два сосуществующих набора интерфейсов:

| Набор | Вход и назначение | Граница |
| --- | --- | --- |
| T-1: `core/facts/ports` | Логические refs, facts и непрозрачное `content`; проверки управления, ссылок и вычисление решения | Порты не задают storage transaction, PKI или transport |
| T-3: `persistence/storage_types/storage_sql` | Typed DB IDs, revision, attributes и materialized snapshots; transactional commands / prepared reader | Не хранит старое content или исполнимые модели; не подключён к business HTTP |

Особенно важно различать `core.SubjectService(repository)` и
`persistence.SubjectService(engine, dn_definition_id)`: у первого
`get(key)` без context, у второго `get(context, chosen)` с административным
допуском и scope. Это разные интерфейсы в одном пакете.

## Адреса, ID и контекст допуска

Локальный `address.py` каждого пакета содержит:

```text
ContainerType  # organization, environment, system, module
AddressSegment(kind: ContainerType, key: str)
CompositeKey(segments: tuple[AddressSegment, ...])
parse_address_json(text: str) -> CompositeKey
address_from_pairs(pairs) -> CompositeKey
address_to_mapping(address: CompositeKey) -> dict[str, str]
validate_container_key(value) -> str
```

Адрес включает 1–4 различных типа и полный фактический путь от root.
Типы сортируются в фиксированном порядке; пропущенные типы допустимы, если
соответствующих узлов действительно нет. Key контейнера — ASCII
`[A-Za-z0-9_-]{1,255}`, equality без ASCII регистра, оригинал сохраняется.
Парсер выявляет duplicate JSON members до создания dict. Функции возвращают
DTO либо выбрасывают `InvalidAddress(code: AddressErrorCode, field: str)`;
плановое обозначение `InvalidInput` в T-3 design не является фактическим
результатом этих parser-функций.

```python
from container_adm_api.address import parse_address_json, address_to_mapping

address = parse_address_json('{"module":"orders","organization":"Acme"}')
assert address_to_mapping(address) == {"organization": "Acme", "module": "orders"}
# Валидный адрес по форме; существование прямого Acme -> orders проверит resolver.
# '{"organization":"Acme","organization":"Other"}' вызовет InvalidAddress.
```

`AddressErrorCode` содержит `INVALID_TYPE`, `OUT_OF_RANGE`, `EMPTY_KEY`,
`KEY_TOO_LONG`, `INVALID_KEY_ALPHABET`, `CONTROL_CHARACTER`,
`INVALID_UNICODE`, `INVALID_JSON`, `INVALID_ADDRESS`,
`UNKNOWN_CONTAINER_TYPE`, `DUPLICATE_CONTAINER_TYPE`. Конкретный parser
использует применимые к форме адреса коды; объявленный enum не обещает,
что каждая функция возвращает каждый код.

Persistent `ContainerId`, `SubjectId`, `ObjectId`, `ModelId`,
`SubjectTypeId`, `AttributeDefinitionId`, `Revision` хранят поле `value`:
строго Python int `1..9223372036854775807`; bool, строка, ноль и float не
принимаются. ID генерирует PostgreSQL, create не принимает желаемый ID.
Ошибка конструирования — `InvalidStorageInput`.

Логические `ContainerRef`, `SubjectRef`, `ObjectRef`, `ModelRef`, `ActionRef`,
`DNRef` хранят opaque hashable `token`. DB mapping явный:
`DB BIGINT → LocalId(n) → LocalRef(str(n))`. Helpers
`ref_from_id(value, id_type, ref_type)` и
`id_from_ref(ref, ref_type, id_type)` проверяют вид локального типа;
обратное преобразование принимает только каноническую положительную
десятичную строку без знака, пробелов и ведущих нулей, в диапазоне BIGINT.
Символический `ContainerRef("root")` годится для логического fixture,
но не является DB selector.

Административный context:

```text
ManagementContext(
    addressed_key: CompositeKey,      # C: куда адресована операция
    represented_key: CompositeKey,    # O: кого представляет вызывающий
    certificate: VerifiedCertificateFact,
)
VerifiedCertificateFact(dn=DNRef(trusted_name_der_bytes))
```

`trusted_name_der_bytes` — ASN.1 Name DER из уже проверенного сертификата.
PKI, подпись, сроки и chain validation внешняя доверенная граница ещё должна
реализовать. Конструирование DTO само по себе не доказывает аутентификацию;
строка клиентского DN и клиентский comparison key не заменяют такой факт.
`dn_definition_id` берётся из доверенной конфигурации. Admission проверяет
DN только у явного O по этому definition, затем конкретная management
операция требует `O ≼ C ≼ D`. Родство вычисляется по фактическим parent links.

## Типизированные атрибуты и snapshots T-3

Источник типов: например,
[container storage_types.py](../../container-adm-api/src/container_adm_api/storage_types.py);
остальные пакеты объявляют свои варианты.

| `TypedValue(kind, value)` | Python значение | Основная проверка |
| --- | --- | --- |
| `ValueType.STRING` | `str` | UTF-8 без NUL; пустая строка допустима |
| `INTEGER` | `int` | Знаковый BIGINT, bool исключён |
| `DECIMAL` | `Decimal` | Не float; итоговую допустимость NUMERIC проверяет БД |
| `BOOLEAN` | `bool` | False является значением |
| `DATE` | `date` | datetime исключён |
| `INSTANT` | `datetime` | Обязателен timezone/offset |
| `DN` | `bytes` Name DER | Definition только `set` для containers; codec проверяет DER в БД |

Native DB semantics, cardinality, applicability и comparator version
проверяются в транзакции. Строки сравниваются по definition: `exact` или
`unicode_ci` с D145 `NFD(toCasefold(NFD(x)))`; пробелы значимы. DN использует
отдельный `x509_rfc5280` профиль версии `dn-rfc5280-u32-t61-v1`, исходный DER
сохраняется. Matching keys вычисляет БД, клиент их не присылает.

```python
AttributeChanges(operations=(
    PutScalar(definition_id, TypedValue(ValueType.STRING, "Название")),
    # Для другого definition_id:
    # ReplaceSet(other_definition_id, (TypedValue(...), ...)),
    # UnsetAttribute(third_definition_id),
))
```

В одном changes каждый definition ID встречается один раз. `PutScalar`
задаёт единственное значение, `ReplaceSet` — полное новое множество,
`UnsetAttribute` — удаляет instance. `initial_attributes` допускает только
put/replace. Пропущенный definition не меняется. `None` не является typed
значением. Пустой `SetAttribute(id, ())` и отсутствующий атрибут различаются;
объявлен `AbsentAttribute(definition_id)`, но aggregate snapshots перечисляют
только существующие instances. Отдельный публичный attribute-lookup метод
в service API сейчас не предоставлен.

Множество не имеет контрактного порядка. Равные значения сворачиваются
по полному DB equality, прежний оригинал существующего равного элемента
сохраняется; среди новых равных входов сохраняется первый. Перестановка
и повторы равных элементов не повышают revision. Semantics definition
заморожены при любом instance, включая empty set и attrs tombstone.

```text
ContainerSnapshot(id, kind, key, parent_id | None, revision, attributes)
SubjectSnapshot(id, holder_id, type_id, key, revision, deleted_at | None, attributes)
ObjectSnapshot(id, holder_id, key, revision, attributes)
ModelMetadata(id, holder_id, key, revision, attributes)
```

`attributes` — tuple `ScalarAttribute(definition_id, TypedValue)` либо
`SetAttribute(definition_id, tuple[TypedValue,...])`. Это materialized
immutable DTO; чтение не требует удерживать открытую SQLAlchemy session.

## Административные application methods T-3

Ниже приведены фактические имена аргументов реализации: `chosen` — typed
ID цели, `expected` — `Revision` клиента. В prose/design встречаются более
описательные `container_id`/`expected_revision`, но их нельзя передавать
как keyword вместо фактических имён. В примерах ниже ID и token передаются
позиционно. Все методы синхронные.

Четыре service constructors имеют вид
`Service(engine, dn_definition_id, *, repository_factory=None, admission=None,
reader_factory=SnapshotReader)`. Production engine должен иметь собственные
ограниченные DB полномочия. Factory/admission параметры — точки подстановки
локальных адаптеров и проверок; они не отменяют согласованный transaction
boundary и доверие. Constructor с неправильным DN definition ID выбрасывает
`InvalidStorageInput`.

### Контейнеры

Класс [persistence.ContainerService](../../container-adm-api/src/container_adm_api/persistence.py).

| Метод | Успех | Семантика |
| --- | --- | --- |
| `create_child(context, parent, kind, key, initial_attributes=AttributeChanges())` | `Created(ContainerSnapshot)` | `parent: ContainerId`, `kind: ContainerType`; D=parent; root этим методом не создаётся |
| `change(context, chosen, expected, changes=AttributeChanges(), *, new_key=None)` | `Changed(snapshot)` / `Unchanged(snapshot)` | Меняет attrs и optional key атомарно; `new_key=None` сохраняет key; parent/type неизменяемы |
| `delete(context, chosen, expected)` | `Removed(target_id, previous_revision)` | Физическое удаление; не рекурсивное, дети и held active данные сначала должны быть удалены |
| `get(context, chosen)` | `ContainerSnapshot` | ID lookup с administrative scope |
| `resolve(context, address)` | `ContainerSnapshot` | Полный локальный `CompositeKey`; не поиск по конечному key |
| `path(context, chosen)` | `tuple[ContainerSnapshot,...]` | Полный фактический root→target путь в одном snapshot |

Rename сохраняет ID и меняет вычисляемые адреса descendants; revision самого
потомка от изменения адреса предка не растёт. Case-only rename меняет
сохранённое написание и повышает revision переименованного узла. Delete
удаляет собственные attrs/DN и tombstones держателя в той же транзакции;
блокирующие ссылки/сущности не удаляются каскадом произвольно.

### Субъекты

Класс [persistence.SubjectService](../../entity-subject-adm-api/src/entity_subject_adm_api/persistence.py).

| Метод | Успех | Семантика |
| --- | --- | --- |
| `create(context, holder, type_id, key, initial_attributes=AttributeChanges())` | `Created(SubjectSnapshot)` | Holder/type — локальные IDs; key Unicode 1–512 codepoints, exact, без Cc/невалидного UTF-8 |
| `change_attributes(context, chosen, expected, changes)` | `Changed` / `Unchanged` | Меняет attrs всего агрегата, без изменения holder/type/key |
| `soft_delete(context, chosen, expected)` | `Changed` / `Unchanged` | Устанавливает `deleted_at`, сохраняет ID, natural key и attrs |
| `restore(context, chosen, expected)` | `Changed` / `Unchanged` | Очищает `deleted_at` прежнего ID; прежние attrs сохраняются |
| `get(context, chosen)` / `find(context, holder, type_id, key)` | `SubjectSnapshot` | Только active; tombstone даёт `NotFound` |
| `get_admin(context, chosen)` / `find_admin(context, holder, type_id, key)` | `SubjectSnapshot` | Включает tombstones и `deleted_at` |

Natural identity `(holder,type,key)` уникальна и для tombstones. Create
занятой active identity даёт `IdentityConflict`, занятой tombstone identity —
`RestoreRequired`; восстановление выполняется отдельной командой с expected
revision, create не превращается в restore автоматически. Повтор текущего
lifecycle состояния с актуальным token — no-op. Изменение attrs tombstone
не запрещается публичным методом: он читает текущую запись administrative
reader и выполняет CAS. Физический purge доступен только при удалении держателя.

### Объекты

Класс [persistence.ObjectService](../../entity-object-adm-api/src/entity_object_adm_api/persistence.py).

| Метод | Успех | Семантика |
| --- | --- | --- |
| `create(context, holder, key, initial_attributes=AttributeChanges())` | `Created(ObjectSnapshot)` | Непустой точный Unicode key без Cc/невалидного UTF-8 и application max |
| `change_attributes(context, chosen, expected, changes)` | `Changed` / `Unchanged` | Holder/key неизменяемы |
| `delete(context, chosen, expected)` | `Removed` | Физически удаляет объект и его attrs, сохраняет holder/subjects/model metadata |
| `get(context, chosen)` / `find(context, holder, key)` | `ObjectSnapshot` | ID либо полное точное `(holder,key)` |

`User42`, `user42`, `é` и `e`+U+0301 — разные keys; trim/normalization нет.
Физический предел PostgreSQL TEXT сохраняется. Поисковый hash не является
идентичностью: bucket candidates сравниваются по полному key, коллизия разных
строк допустима. Конкурентный одинаковый key защищает DB MVCC guard.

### Метаданные моделей

Класс [persistence.ModelMetadataService](../../policy-adm-api/src/policy_adm_api/persistence.py).

| Метод | Успех | Семантика |
| --- | --- | --- |
| `create(context, holder, key, initial_attributes=AttributeChanges())` | `Created(ModelMetadata)` | ASCII `[A-Za-z0-9_-]`, длина 1–512, CI equality внутри holder, оригинал сохраняется |
| `change_attributes(context, chosen, expected, changes)` | `Changed` / `Unchanged` | Меняет attrs; ID/holder/key неизменяемы |
| `delete(context, chosen, expected)` | `Removed` | Удаляет metadata и собственные attrs |
| `get(context, chosen)` / `find(context, holder, key)` | `ModelMetadata` | ID либо CI `(holder,key)` |
| `metadata_for(context, containers)` | `ModelMetadataSet` | Iterable уникальных локальных ContainerId; scope проверяется для каждого |

`ModelMetadataSet(containers, groups)` содержит ровно один
`ContainerModelMetadata(container, models)` на каждый контейнер в порядке
запроса, включая `models=()`. Повторы входных container ID дают `InvalidInput`;
ошибка/неполнота чтения — `UnknownModelMetadataSet` либо `FactsUnavailable`.
Явный пустой запрос допустим и даёт `ModelMetadataSet((), ())` после admission.
Это административное чтение, не порт исполнимых моделей для PDP.

### Успехи, ошибки и конкуренция

Все write methods возвращают результат после commit. Они используют одну
SERIALIZABLE connection/transaction на attempt для admission, текущих фактов,
scope, CAS, aggregate/attrs и commit. Read methods — один READ ONLY
REPEATABLE READ snapshot. Repository не фиксирует транзакции самостоятельно.

| Outcome | Поля и смысл | Действие вызывающего |
| --- | --- | --- |
| `Created`, `Changed`, `Unchanged` | `snapshot` | Использовать ID/revision из подтверждённого результата |
| `Removed` | `target_id`, `previous_revision` | Удаление подтверждено; revision удалённой записи не является token нового объекта |
| `NotFound()` | Установленное отсутствие target после admission | Проверить selector/lifecycle; read failure этим outcome не маскируется |
| `RevisionConflict()` | Исходный expected устарел, включая no-op | Прочитать актуальное состояние и осознанно сформировать новую команду |
| `IdentityConflict()` | Занята natural identity | Проверить уже существующую запись; DB digest collision разных object keys не является таким конфликтом |
| `RestoreRequired()` | Subject identity занята tombstone | Administrative read и явный restore прежнего ID |
| `InvalidInput(code)` | Некорректная форма входов команды | Исправить локальный ввод; constructors/parser могут выбрасывать ValueError subtype раньше вызова |
| `ManagementRejected(code)` | Не подтверждён admission / выход за scope | Проверить доверенный certificate context и фактическую область |
| `InvariantRejected(code)` | DB ограничение, identity mutation, тип/cardinality/applicability и т.п. | Исправить недопустимое состояние; автоматического retry нет |
| `FactsUnavailable(part, code)` | Обязательные facts/comparison/snapshot недоступны | Не считать отсутствие доказанным; восстановить источник |
| `StorageUnavailable(code="STORAGE_UNAVAILABLE")` | Storage/boundary failure; подтверждённого успеха нет | Зафиксировать неуспех; код также используется при ошибке rollback, не раскрывает SQL/DSN/DN |
| `RetryExhausted()` | Три retryable attempts завершились rollback | Команда не подтвердила запись; дальнейшая retry policy вызывающего не задана |
| `CommitOutcomeUnknown()` | Не удалось подтвердить исход commit | Не повторять вслепую; получить подтверждённое состояние/разобрать исход операции |
| `UnknownModelMetadataSet(code)` | Не подтверждён состав metadata | Не заменять пустыми группами и не превращать в `CompleteModelSet` |

`40001` (serialization failure) и `40P01` (deadlock) повторяют весь attempt
после подтверждённого rollback: всего максимум три попытки, включая первую.
Все факты перечитываются, но исходный `expected` не подменяется свежим token.
Validation/admission/stale/invariant/identity/NotFound автоматически не повторяются.

Новый агрегат получает revision=1. Успешное логическое изменение повышает её
ровно на 1, пустой changes/эквивалентный set/unset отсутствующего attrs — нет.
No-op всё равно проверяет admission/scope/CAS; stale token даёт конфликт.
Два no-op не обещают эксклюзивно «занять» token. Client create/delete после
потерянного commit не получает выдуманной идемпотентности.

Реализация переводит `P0002` в NotFound, `P0001/REVISION_CONFLICT` в
RevisionConflict, `23505` в IdentityConflict/RestoreRequired либо отдельный
attribute invariant, `428C9` в immutable-identity rejection, constraint SQLSTATE
`23001/23503/23514` в InvariantRejected, class `22` в invalid value, `0A000`
в comparison unavailable. Наружу выдаётся закрытый код; raw SQL/DSN/traceback
и исходные значения в DTO не включаются. HTTP mapping не определён.

### Пример: создание и изменение субъекта

Фрагмент выполняется в Python процессе с установленным subject-пакетом.
`engine`, `trusted_name_der`, ID DN definition и заранее зарегистрированных
типа/attribute definition предоставляет подготовленная среда; это не
готовый сетевой запрос и не способ обхода сертификатной границы.

```python
from entity_subject_adm_api.address import parse_address_json
from entity_subject_adm_api.facts import DNRef, VerifiedCertificateFact
from entity_subject_adm_api.persistence import SubjectService
from entity_subject_adm_api.storage_types import (
    AttributeChanges, AttributeDefinitionId, Changed, ContainerId, Created,
    ManagementContext, PutScalar, SubjectTypeId, TypedValue, ValueType,
)

context = ManagementContext(
    addressed_key=parse_address_json('{"organization":"Acme","module":"orders"}'),
    represented_key=parse_address_json('{"organization":"Acme"}'),
    certificate=VerifiedCertificateFact(DNRef(trusted_name_der)),
)
service = SubjectService(engine, AttributeDefinitionId(configured_dn_definition_id))
created = service.create(context, ContainerId(orders_holder_id),
                         SubjectTypeId(person_type_id), "User42")
if isinstance(created, Created):
    changed = service.change_attributes(
        context, created.snapshot.id, created.snapshot.revision,
        AttributeChanges((PutScalar(
            AttributeDefinitionId(display_name_definition_id),
            TypedValue(ValueType.STRING, "Анна"),
        ),)),
    )
    if isinstance(changed, Changed):
        current_revision = changed.snapshot.revision
# Остальные outcomes обрабатываются по таблице; свежий token за клиента не подставляется.
```

## Transaction-bound adapters T-3

Следующие методы нужны при подключении application слоя и разборе исходников.
Они получают уже открытую SQLAlchemy connection, не выполняют admission
самостоятельно и не являются отдельным разрешённым входом для конечного
вызывающего. Прямой вызов repository в обход service пропускает application
проверку сертификата и `O ≼ C ≼ D`.

| Adapter | Методы без самостоятельного commit |
| --- | --- |
| `ContainerRepository(connection, *, reader_factory=SnapshotReader)` | `get(chosen)`, `resolve(address)`, `path(chosen)`, `create_child(parent,kind,key,initial_attributes)`, `change(chosen,expected,changes,*,new_key=None)`, `delete(chosen,expected)` |
| `SubjectRepository(connection, *, reader_factory=SnapshotReader)` | `get(chosen,*,administrative=False)`, `find(holder,type_id,key,*,administrative=False)`, `create(holder,type_id,key,initial_attributes)`, `change_attributes(chosen,expected,changes)`, `soft_delete(chosen,expected)`, `restore(chosen,expected)` |
| `ObjectRepository(connection, *, reader_factory=SnapshotReader)` | `get(chosen)`, `find(holder,key)`, `create(holder,key,initial_attributes)`, `change_attributes(chosen,expected,changes)`, `delete(chosen,expected)` |
| `ModelMetadataRepository(connection, *, reader_factory=SnapshotReader)` | `get(chosen)`, `find(holder,key)`, `metadata_for(containers)`, `create(holder,key,initial_attributes)`, `change_attributes(chosen,expected,changes)`, `delete(chosen,expected)` |

Repository get/find/resolve возвращает snapshot либо `None`; mutation
возвращает `(snapshot, changed: bool)`, create — snapshot, physical delete —
прежнюю `Revision`. Эти значения ещё не означают commit. Невалидный ввод,
неполный snapshot и SQL errors поднимаются к transaction runner, который
откатывает и преобразует их в outcomes application слоя.

`SnapshotReader(connection, *, administrative_subjects=False)` предоставляет
`resolve(address)`, `path(target)`, `address_of(target)`,
`is_ancestor(ancestor,descendant)`, `attributes(kind,chosen)`,
`attribute(kind,chosen,definition)`, `get(kind,chosen)`,
`find(kind,holder,key,type_id=None)`, `metadata_for(containers)` и технический
`rows(sql,parameters=None)`. `kind` выбирается из `container/subject/object/model`;
single-attribute lookup возвращает `AbsentAttribute`, когда instance
отсутствует. Административный subject reader видит tombstones, обычный —
только active facts. Error boundary — `SnapshotReadError`,
`InvalidStorageInput` или SQLAlchemy error. Эти методы не смешивают чтения
из разных connection.

`storage_sql.changes_sql(changes, parameters)` формирует SQL fragment native
composites с bind parameters; исходные значения добавляются в parameters,
а не конкатенируются в текст SQL. `ManagementAdmission.admit(connection,context)`
возвращает `AdmittedManagement(addressed,represented)` либо безопасный отказ;
`.scope(connection,caller,holder)` возвращает `None` при установленном
`O≼C≼D` либо отказ. `TransactionRunner.run(operation)`/`.read(operation)`
владеют connection, isolation, commit/rollback и материализацией результатов.

## Prepared facts reader T-3

Источник: [decision persistence.py](../../policy-decision-api/src/policy_decision_api/persistence.py).

```text
SubjectIdentity(holder_id: ContainerId, type_id: SubjectTypeId, key: str)
ObjectIdentity(holder_id: ContainerId, key: str)
PreparedFactsRequest(addressed_key, represented_key, certificate,
                     subject: SubjectId | SubjectIdentity,
                     object: ObjectId | ObjectIdentity,
                     action: ActionRef)
PreparedFactsReader(engine, dn_definition_id: AttributeDefinitionId,
                    *, reader_factory=SnapshotReader).read(request)
```

Selectors строго различаются локальными классами. Произвольный Hashable или
сырой int не persistent selector. Subject key имеет exact Unicode 1–512,
object key — exact Unicode TEXT без application max. Action opaque и
не требует регистрации в таблице действий.

| Result | Содержимое / причина |
| --- | --- |
| `PreparedFactsSnapshot(caller, subject, object, action, path, containers, metadata)` | AdmittedCaller, active SubjectSnapshot, ObjectSnapshot, исходный ActionRef, полный CompletePath, уникальные ContainerSnapshots и metadata всего пути |
| `RequestRejected(reason)` | `INVALID_PREPARED_FACTS_REQUEST`, `CONTAINER_ADDRESS_UNRESOLVED`, `CERTIFICATE_DN_NOT_BOUND`, `OBJECT_OUT_OF_ADDRESSED_SCOPE` |
| `RequiredFactsUnavailable(reason)` | Отсутствует active subject/object либо обязательные entity/container/admission facts; например `ACTIVE_SUBJECT_OR_OBJECT_NOT_FOUND`, `SOURCE_UNAVAILABLE` |
| `UnknownPreparedFacts(part, code)` | `part="PATH"` / `"MODEL_METADATA"`; неполнота пути/metadata, например `SNAPSHOT_INCOMPLETE` |

До первого SELECT reader устанавливает REPEATABLE READ и READ ONLY. Admission,
active entity lookup, полный root→holder(object) путь, attrs/DN и metadata
читаются одной connection/transaction. Проверяется `C ≼ holder(object)`;
`O ≼ C` и общее `H(S) ≼ C` не навязываются. В `containers` добавляются
представляемый O и holder субъекта, если их нет на пути, без дубликатов ID.
Reader materializes DTO до завершения snapshot и не достраивает результат
после отдельного переподключения.

Пример вызова после подготовки trusted certificate context:

```python
from policy_decision_api.address import parse_address_json
from policy_decision_api.facts import ActionRef, DNRef, VerifiedCertificateFact
from policy_decision_api.persistence import (
    PreparedFactsReader, PreparedFactsRequest, PreparedFactsSnapshot,
)
from policy_decision_api.storage_types import AttributeDefinitionId, SubjectId, ObjectId

reader = PreparedFactsReader(reader_engine, AttributeDefinitionId(configured_dn_definition_id))
result = reader.read(PreparedFactsRequest(
    parse_address_json('{"organization":"Acme"}'),
    parse_address_json('{"organization":"Acme"}'),
    VerifiedCertificateFact(DNRef(trusted_name_der)),
    SubjectId(subject_id), ObjectId(object_id), ActionRef("read"),
))
if isinstance(result, PreparedFactsSnapshot):
    metadata_groups = result.metadata.groups
    # Снимок получен; итоговый доступ этим вызовом не вычисляется.
```

Reader использует SELECT LOGIN и published views; он не вызывает mutations,
не повышает роль и не исполняет модели. `ModelMetadataSet` не является
`CompleteModelSet` T-1; adapter metadata→исполняемая модель отсутствует.

## Логические операции и порты T-1

Эти контракты остаются в коде и полезны для понимания алгоритма и локальной
интеграции. Они не заменяют transactional commands T-3. Их `reason` —
локальные пояснения, не стабильный HTTP error schema.

### Контейнеры и допуск

Источник: [container core](../../container-adm-api/src/container_adm_api/core.py),
[facts](../../container-adm-api/src/container_adm_api/facts.py),
[ports](../../container-adm-api/src/container_adm_api/ports.py),
[Postgres adapter](../../container-adm-api/src/container_adm_api/tree_adapter.py).

| Публичный контракт | Результат / поведение |
| --- | --- |
| `ContainerForest(facts: Iterable[ContainerFacts])` | Immutable forest; проверяет parent, строгий порядок типов, отсутствие противоречий и duplicate full addresses |
| `ContainerTree(facts)` | Те же проверки, дополнительно ровно один root; некорректные facts дают `InvalidContainerTree` |
| `.roots` (forest), `.root` (tree), `.nodes` | Установленные refs/факты |
| `.key_of(ref)` | `CompositeKey`; неизвестный ref → `UnknownContainer` |
| `.resolve(key)` | `ContainerRef | ResolutionFailed(reason)` |
| `.is_ancestor_or_self(ancestor, descendant)` | Фактический bool; неизвестный ref → `UnknownContainer` |
| `.path_to(target)` | `CompletePath | UnknownPath(reason)`; complete включает root и target и каждого фактического parent |
| `ContainerAdmission(containers, bindings).admit(kind, addressed_key, represented_key, certificate)` | `AdmittedCaller(addressed, represented, kind) | RequestRejected(reason)` |

`ContainerFacts(ref, kind, key, parent)` хранит исходные факты.
Container `CompletePath(target, nodes)` строится из `ContainerFacts`, проверяет
parent links и предоставляет `root/target/containers`; одноимённый PDP DTO
конструируется иначе: `CompletePath(root,target,containers)` и проверяет refs.
`CertificateBindingPort.is_bound_to(dn, container)->bool` подтверждает пару
DN/O, `ContainerFactsPort` — resolve/отношение/path. Admission общий для
`RequestKind.MANAGEMENT` и `ACCESS_CHECK`, сам по себе scope не проверяет.

`PostgresContainerFacts(connection, dn_definition_id)` предоставляет
`resolve`, `key_of`, `is_ancestor_or_self`, `path_to`, `is_bound_to` на
текущей переданной transaction. Он не управляет commit; DB ошибки превращаются
в ResolutionFailed/UnknownPath/UnknownContainer, DN source failure —
`BindingFactsUnavailable`. Invalid DN token даёт False. Потребитель обязан
сохранить отличие unknown от установленного отсутствия/False.

### Субъекты, объекты и модели

| Контракт | Вход / успех / отказ |
| --- | --- |
| `subject_facts(subject_ref, holders)` | Ровно один различный ContainerRef → SubjectFacts; ноль/разные holders → InvalidSubject |
| `core.SubjectService(repository).get(key)` | Hashable key → SubjectFacts либо SubjectFactsUnavailable(reason) |
| `SubjectManagementService(repository, admission, containers).update_content(subject_key, content, *, addressed_key, represented_key, certificate, candidate_holders=None)` | O≼C≼D и единственный прежний holder; SubjectUpdated(record) либо ManagementRejected(reason) до save |
| `ObjectFacts.from_holders(object_ref, holders, content=None)` | Проверяет единственного holder; InvalidObjectFacts при нарушении |
| `ObjectFactsService(facts).get(object_ref)` / `.reference(object_ref)` | ObjectFacts / исходный ObjectRef либо ObjectLookupFailed(reason); duplicate authoritative rows отклоняются constructor |
| `ObjectManagementService(admission, containers, repository).update_content(addressed_key, represented_key, certificate, update)` | `update=ObjectContentUpdate(object_ref, content, holders=None)`; ManagementApplied(facts) либо ManagementRejected(reason) до save |
| `model_facts(model_ref, holders)` | ModelFacts с одним различным holder либо InvalidModel |
| `ModelFactsService(source).models_for(containers)` | CompleteModelSet либо UnknownModelSet(reason); source.list_for(container) обязан вернуть CompleteContainerModels или UnknownContainerModels |
| `ModelReferenceChecker(subjects, objects, containers).validate(model, references)` | `ModelReferences(subjects=(),objects=())`; проверяет H(S)≼M и M≼H(Q); ReferencesValidated(references) либо ReferencesRejected(reason) |
| `ModelManagementService(repository, admission, containers, references).update_model(model_key, content, *, addressed_key, represented_key, certificate, references=None, candidate_holders=None)` | Проверяет O≼C≼D, прежний holder и все текущие/новые references; ModelUpdated(record) либо ManagementRejected(reason) |

`SubjectRecord(facts,content)` и `ModelRecord(facts,content,references)`
не интерпретируют opaque content. Logical updates сохраняют текущего holder;
перенос не определён методом. В persistent T-3 identity уже явно неизменяема.
Модельная ссылка не меняет и не дополняет держателя entity. T-1 repositories
имеют `get`/`save(...)->None`, sources/facts ports — только чтение;
их замена прямым SQL save не создаёт необходимую T-3 атомарность.

Источники: [subject core/ports](../../entity-subject-adm-api/src/entity_subject_adm_api/),
[object core/ports](../../entity-object-adm-api/src/entity_object_adm_api/),
[policy core/ports](../../policy-adm-api/src/policy_adm_api/).

### Проверка доступа и модельные исходы

Источник: [decision core](../../policy-decision-api/src/policy_decision_api/core.py),
[facts](../../policy-decision-api/src/policy_decision_api/facts.py),
[ports](../../policy-decision-api/src/policy_decision_api/ports.py).

```python
AccessRequest(addressed_key, represented_key, certificate,
              subject_key, object_ref, action)
AccessInputService(admission, subjects, objects, containers).prepare(request)
AccessCheckService(inputs, containers, models, evaluator).check(request)
evaluate_model(model, subject, object_facts, action, containers, evaluator)
aggregate_rules(applicable_effects)
aggregate_models(results)
```

`subject_key` — отдельный фактически hashable ключ; `object_ref` — локальный
ObjectRef, action — ActionRef. `prepare` выполняет ACCESS_CHECK admission,
читает subject/object и проверяет `C ≼ holder(object)`. Результат:
`PreparedAccessCheck(caller, subject, object_facts, action)` либо
`AccessCheckRejected(reason)`/`RequiredFactsUnavailable(reason)`.
Права O не подменяют subject. Общих `O≼C` и `H(S)≼C` ограничений нет.

`check` сначала получает `ContainerPathPort.path_to(target)` и
`ModelFactsPort.models_for(path.containers)` с точным покрытием всего
root→target пути. Результат — `EvaluatedDecision(effect,reason)` либо
те же request/required-facts outcomes. `UnknownPath`/`UnknownModelSet` и
declared `ChainFactsUnavailable`/`InvalidChainFacts` дают EvaluatedDecision
Deny до вычислителя. Предки C не исключаются из пути. Подтверждённое отсутствие
моделей задаётся explicit empty groups, не неизвестным источником.

`evaluate_model` вне `H(S)≼holder(model)` возвращает Neutral без evaluator.
Неустановленное отношение — RequiredFactsUnavailable. В области вызывается
`ModelEvaluatorPort.evaluate(model,subject,object_facts,action)->ModelOutcome`;
только объявленные `ModelEvaluationFailed`/`ModelDataUnavailable` превращаются
в Undefined. Недоступные обязательные entity/отношения не маскируются под
Undefined. Неожиданные исключения вычислителя не получают общего catch-all.

| Полный вход | Результат |
| --- | --- |
| `aggregate_rules`: хотя бы один RuleEffect.DENY | ModelOutcome.DENY |
| Нет DENY, есть ALLOW | ModelOutcome.ALLOW |
| Подходящих правил нет | ModelOutcome.NEUTRAL |
| `aggregate_models`: хотя бы один ModelOutcome.DENY | EvaluatedDecision(DENY, reason) |
| Нет DENY, есть ALLOW, остальные Neutral/Undefined | EvaluatedDecision(ALLOW, reason) |
| Только Neutral/Undefined либо ни одной модели | EvaluatedDecision(DENY, default reason) |

Операторы принимают только установленные enum-значения полного набора;
невалидный элемент даёт TypeError. Пример чистой семантики без БД/HTTP:

```python
from policy_decision_api.core import aggregate_models
from policy_decision_api.facts import DecisionEffect, ModelOutcome

assert aggregate_models([ModelOutcome.ALLOW, ModelOutcome.UNDEFINED]).effect is DecisionEffect.ALLOW
assert aggregate_models([ModelOutcome.ALLOW, ModelOutcome.DENY]).effect is DecisionEffect.DENY
assert aggregate_models([]).effect is DecisionEffect.DENY
```

Этот пример не проверяет полноту реального источника: её обязан установить
оркестратор до вызова aggregate. Правила applicability/язык политики,
ошибка отдельного правила и production evaluator остаются отдельным change.

## SQL интерфейсы каталогов и bootstrap

Это прямой privileged SQL interface, поставляемый `db-control`, без нового
каталогового runtime-сервиса. Точные сигнатуры:

```sql
subjects.register_type(new_key TEXT) RETURNS BIGINT
attributes.register_definition(
  new_key TEXT, kind attributes.value_type, mode attributes.cardinality,
  selected attributes.comparison_profile DEFAULT NULL,
  selected_version TEXT DEFAULT NULL
) RETURNS BIGINT
attributes.set_applicability(
  chosen BIGINT, container_types containers.container_type[],
  subject_types BIGINT[], allow_objects BOOLEAN, allow_models BOOLEAN
) RETURNS VOID
attributes.change_unused_semantics(
  chosen BIGINT, kind attributes.value_type, mode attributes.cardinality,
  selected attributes.comparison_profile DEFAULT NULL,
  selected_version TEXT DEFAULT NULL
) RETURNS VOID
containers.provision_root(
  kind containers.container_type, new_key TEXT,
  changes attributes.change_input[] DEFAULT ARRAY[]::attributes.change_input[]
) RETURNS BIGINT
```

Первым четырём нужен `tamarix_catalog_operator`, root provisioning — отдельное
привилегированное эксплуатационное соединение; ни одна из шести runtime/catalog/
reader groups права provision-root не имеет. Catalog key ASCII CI 1–512,
неизменяем. Applicability задаёт четыре явных набора; новые subject types
не получают применимость автоматически. Нельзя снять используемую применимость
или поменять semantics definition с любым instance, включая empty set.

Native write input — `attributes.change_input(definition_id, operation,
values attributes.value_input[])`, операции SQL `put`, `replace`, `unset`.
`value_input` имеет TEXT/BIGINT/NUMERIC/BOOLEAN/DATE/TIMESTAMPTZ/BYTEA поля,
ровно одно заполнено. Runtime roles вызывают только собственные узкие routines;
catalog role не получает права менять чужие attrs и не заменяет admission.
Точные routines/grants — [0002_storage.sql](../../db-control/src/db_control/sql/0002_storage.sql),
bootstrap и безопасный параметризованный пример — [db-control README](../../db-control/README.md).

## Deployment CLI db-control

Источник: [cli.py](../../db-control/src/db_control/cli.py).
Запуск из установленного окружения db-control: `python -m db_control`.
DSN и credentials передаются по имени env-переменной, значения не включаются
в argv. CLI возвращает JSON, exit=0 при успехе; при ошибке JSON в stderr
с `status="ERROR"`, `code`, `exception_type`, `sqlstate`, exit=1.

| Команда | Аргументы | Поведение |
| --- | --- | --- |
| `artifact-info` | Нет | Без DB connection: версии пакета/Python/dependencies, heads, hashes Python/SQL/data ресурсов |
| `current` | `--dsn-env NAME` | Preflight и текущие Alembic heads, без upgrade |
| `upgrade` | `--dsn-env NAME` | Preflight и upgrade до head; schema/DDL выполняет только deployment executor |
| `downgrade` | `--dsn-env NAME --disposable` | До base, только одноразовая БД `tamarix_t3_*`; не production rollback |
| `provision-test-logins` | `--dsn-env NAME --credentials-env NAME --disposable` | Создаёт шесть новых ограниченных LOGIN для точного набора group roles, без DDL прав |
| `create-test-database` | `--dsn-env NAME --database-name tamarix_t3_case_<uuid32> --disposable` | Отдельная case DB UTF8 с ownership marker |
| `drop-test-database` | Те же аргументы | Удаляет только помеченную case DB; отсутствующая DB даёт already_absent |
| `install-test-collision-seam` | `--dsn-env NAME --disposable` | Только marked case DB; подменяет object key digest для проверки коллизий |

Preflight требует PostgreSQL 18+, UTF8 и block size≥8192. LOGIN credentials
JSON должен содержать ровно `tamarix_container_service`,
`tamarix_subject_service`, `tamarix_object_service`, `tamarix_policy_service`,
`tamarix_catalog_operator`, `tamarix_fact_reader`; каждая запись
`{"login":"t3_...","password":"..."}`. Login должен быть новым, иметь
`t3_` и 1–59 строчных ASCII букв/цифр/`_`, password — от 24 символов без NUL.
Эти команды вызываются тестовым deployment executor, не сервисными ролями.

```sh
# TAMARIX_ADMIN_DSN предварительно безопасно задан в окружении.
.venv/bin/python -m db_control artifact-info
.venv/bin/python -m db_control current --dsn-env TAMARIX_ADMIN_DSN
.venv/bin/python -m db_control upgrade --dsn-env TAMARIX_ADMIN_DSN
```

Локальный `db_control.contracts` содержит независимые primitives для
deployment/DDL: `ContainerAddress`, AddressSegment/ContainerType,
parse/address_from_pairs/address_to_mapping, validators positive BIGINT,
expected revision, container/catalog/model/subject/object key и helpers
`ascii_ci_key`, `ascii_ci_equal`, `exact_key_equal`. Ошибка —
`InvalidContract(code: ContractErrorCode, field)`. Сервисы не импортируют
их как общий DTO пакет: собственные адреса называются `CompositeKey`.

Основания договорённостей: [ADR 0001–0003](../openspec/context/adr/README.md),
[T-3 storage contracts](../openspec/changes/archive/2026-10-15-t-3-persistent/storage-contracts.md),
основные [containers spec](../openspec/specs/containers/spec.md),
[subjects spec](../openspec/specs/entities/subjects/spec.md),
[objects spec](../openspec/specs/entities/objects/spec.md),
[model metadata spec](../openspec/specs/access-model/models/spec.md),
[attributes spec](../openspec/specs/attributes/spec.md) и
[access-check spec](../openspec/specs/authorization/access-check/spec.md).
