# Локальные контракты хранения T-3

Документ задачи 1.2 уточняет применяемый [design](design.md) для последующей
реализации пяти Python-пакетов. Основание — [proposal](proposal.md), шесть
delta specs и [requirements](requirements.md). Продолжение apply пользователем
разрешает реализацию подготовленного плана после независимого review design;
наличие этого документа не подтверждает написанный код или выполненные тесты.

Контракты ниже — локальные Python/application contracts. Имена DTO и Protocol
фиксируют смысл операций, а не HTTP routes, wire-поля или transport codes.
Каждый пакет определяет собственные классы и явно преобразует чужие значения.
Общий runtime-пакет DTO и импорты внутренних классов соседнего сервиса
не вводятся. Все DDL, routines, roles и views поставляет только `db-control`.

## 1. Наблюдаемая исходная точка

| Источник | Что требует изменения для persistence |
| --- | --- |
| `container-adm-api/src/container_adm_api/facts.py`, `core.py`, `ports.py` | `CompositeKey.segments` содержит только строки; `ContainerTree` принимает одно дерево и индексирует адрес без типов; CRUD и revision отсутствуют |
| `entity-subject-adm-api/src/entity_subject_adm_api/facts.py`, `ports.py`, `core.py` | `SubjectRecord.content` непрозрачен, lookup принимает `Hashable`, `save()` не возвращает CAS-результат; нет типа субъекта, атрибутов, статуса и restore |
| `entity-object-adm-api/src/entity_object_adm_api/facts.py`, `ports.py`, `core.py` | `ObjectFacts.content` непрозрачен; `save()` не задаёт транзакцию или revision; нет предметной identity и длинного точного lookup |
| `policy-adm-api/src/policy_adm_api/facts.py`, `ports.py`, `core.py` | `ModelRecord` содержит `content` и `ModelReferences`; `CompleteModelSet` относится к логическим моделям T-1, а не к metadata |
| `policy-decision-api/src/policy_decision_api/facts.py`, `ports.py`, `core.py` | Сбор через несколько портов не задаёт общий DB snapshot; `CompleteModelSet`, unknown и `Undefined` имеют разные значения |

Старые management-методы проверяют факты до `save()`, но контракт не связывает
их одной транзакцией. Подстановка SQL repository в прежний `save() -> None`
не обеспечивает принятые гарантии. Непрозрачный `content` не становится JSONB,
TEXT/BYTEA payload или набором атрибутов посредством автоматической конвертации.

## 2. ID, opaque Ref и revision

На границе persistence каждый пакет объявляет собственные неизменяемые
целочисленные DTO `ContainerId`, `SubjectId`, `ObjectId`, `ModelId`,
`SubjectTypeId`, `AttributeDefinitionId` по фактической потребности.
Поле `value` — Python `int` в диапазоне `1..9223372036854775807`;
`bool`, float, отрицательное, ноль и выход за диапазон не принимаются.
ID создаёт PostgreSQL; create command не принимает желаемый ID. Разные
предметные таблицы могут иметь одинаковое число ID: тип ссылки различает их.

Существующие `ContainerRef` / `SubjectRef` / `ObjectRef` / `ModelRef` остаются
непрозрачными локальными ссылками T-1. Выбран явный persistence mapping:

```text
DB BIGINT -> LocalId(value) -> LocalRef(str(value))
```

Обратный mapping выполняет persistence adapter, а не ядро. Он принимает
только каноническую десятичную строку положительного ID без знака, пробелов
и ведущих нулей, проверяет диапазон и вид local Ref. Символьные токены прежних
логических fixtures допустимы в pure T-1, но не разрешаются этим адаптером
в DB ID. Чужой Ref преобразуется созданием локального Ref с тем же токеном,
после явной проверки источника; совпадение Python-классов не требуется.
Ни этот mapping, ни BIGINT не объявляют публичный wire-формат ID.

`Revision(value: int)` также положительна и помещается в BIGINT, без coercion
из bool/строки. Новый агрегат получает revision **1**. Каждая успешная
логическая мутация существующего агрегата повышает её ровно на **1**;
переполнение не оборачивается. Технические lifecycle/instance/guard versions
не выдаются за aggregate revision. Смена вычисляемого адреса потомка после
rename предка не меняет revision самого потомка: его собственные данные
и связи остались прежними.

## 3. Type-aware адрес и отношения forest

Во всех пяти пакетах локальный `CompositeKey` переходит на структуру:

```text
AddressSegment(kind: local ContainerType, key: str)
CompositeKey(segments: tuple[AddressSegment, ...])
parse_address_json(text: str) -> CompositeKey | InvalidInput
address_from_pairs(pairs: tuple[tuple[str, str], ...]) -> CompositeKey | InvalidInput
address_to_mapping(address: CompositeKey) -> dict[str, str]
```

`AddressSegment` содержит тип и исходное написание ключа. Адрес имеет 1–4
сегмента; тип встречается не более одного раза. Порядок внутренних сегментов
всегда `organization`, `environment`, `system`, `module`, с пропусками
отсутствующих уровней. Ключ каждого сегмента — ASCII `[A-Za-z0-9_-]{1,255}`.
Равенство/индекс адресов использует пары `(kind, ascii_lower(key))`;
исходное написание доступно для чтения. Ранг не заменяет фактического родства.

JSON parser принимает только объект верхнего уровня и строковые значения.
Он получает исходные пары членов и отклоняет повтор имени типа **до**
создания dict, включая повтор с одинаковым значением. Массив, null, неизвестный
тип и недопустимый key дают `InvalidInput`. Порядок членов JSON незначим.
Входной обычный dict сам по себе не доказывает отсутствие прежних повторов:
его разрешено создавать внутри программы из проверенных данных, но нельзя
использовать вместо duplicate-aware разбора непроверенного JSON.

DB resolver проверяет весь фактический путь, а не наличие конечного key.
Для `organization/acme -> environment/prod -> module/orders` адрес без
`environment` не разрешается в этот module. Сериализация вычисляется из
текущих узлов; полный путь не сохраняется в столбце и не декодируется
из opaque ID. Старый `tuple[str, ...]` не получает автоматическую догадку типов.

Локальный читающий порт контейнеров предоставляет:

```text
resolve(address) -> ContainerRef | NotFound | FactsUnavailable
get(ref) -> ContainerSnapshot | NotFound | FactsUnavailable
address_of(ref) -> CompositeKey | NotFound | FactsUnavailable
path_to(ref) -> CompletePath | UnknownPath
is_ancestor_or_self(ancestor, descendant) -> bool | RelationUnavailable
```

`CompletePath` начинается фактическим root и заканчивается target, включает
всех родителей и оба конца, не повторяет узлы. Известные узлы разных деревьев
дают `False`; отсутствие обязательного узла/ошибка источника — неизвестность,
а не `False`. Прежний exception-based object adapter переводит неизвестность
в `ContainerFactsUnavailable`, пока его logical consumer сохраняет старый
Protocol. Single-tree `ContainerTree` можно сохранять как проверку отдельного
дерева; resolver forest не загружает все корни в этот класс и не использует
его прежний key-only индекс.

## 4. Типизированные атрибуты

Каждый из четырёх административных пакетов и reader объявляет свои
`AttributeDefinition`, `AttributeInstance` и discriminated value DTO.
Definition содержит ID, key, value type, cardinality, string profile
и comparison profile version. Applicability читается из общего каталога;
заявленный клиентом вид/тип владельца не заменяет сохранённый тип.

| Значение DTO | Python-значение | Семантика |
| --- | --- | --- |
| `TextValue` | `str` | Оригинал; equality `exact` либо D145 по definition |
| `BigIntValue` | `int`, исключая bool | Знаковое 64-битное целое |
| `NumericValue` | `Decimal` | Нативное десятичное равенство, без промежуточного float |
| `BooleanValue` | `bool` | False — значение, а не отсутствие |
| `DateValue` | `date`, исключая datetime | Нативная дата |
| `TimestampValue` | aware `datetime` | Момент времени; сравнение по instant, а не offset |
| `DNValue` | исходный Name DER `bytes` | Специальный контейнерный DN type/profile из принятого apply design |

В каждом value заполнен ровно один вариант. `None` не является вариантом
значения. Неявные преобразования строки в число/дату, bool в BIGINT и float
в NUMERIC не выполняются. Физические границы PostgreSQL/драйвера не обходятся
округлением, усечением или молчаливой заменой типа. `TEXT` не получает
ограничения длины ключа субъекта или контейнера. Нуль, False и `""` сохраняются
как допустимые значения соответствующего типа.

Состояние одного атрибута имеет ровно один из видов:

```text
AbsentAttribute(definition_id)
ScalarAttribute(definition_id, value: TypedValue)
SetAttribute(definition_id, values: tuple[TypedValue, ...])
```

`AbsentAttribute` означает отсутствие instance; `SetAttribute(..., ())` —
существующий пустой instance. Scalar всегда содержит ровно одно значение.
Чтение всего агрегата возвращает только существующие instances, каждый
definition ID не более одного раза; lookup одного definition возвращает
явный `AbsentAttribute`. Порядок values множества не является контрактом.

Изменение задаётся `AttributeChanges(operations: tuple[...])` со следующими
локальными операциями:

```text
PutScalar(definition_id, value)
ReplaceSet(definition_id, values)
UnsetAttribute(definition_id)
```

Один definition ID может встретиться в changes только один раз; конфликтующие
операции отклоняются целиком. Пропущенное определение означает «не менять».
`UnsetAttribute` удаляет instance, а не пишет null. `ReplaceSet(..., ())`
оставляет instance пустого множества. `initial_attributes` у create содержит
только Scalar/Set instances; пропущенные определения отсутствуют.

Тип, cardinality, applicability и comparison profile проверяются по БД
в той же транзакции. Повторы в set сворачиваются по полному equality definition,
а не по Python hash, строковому виду числа или digest. Для уже сохранённого
эквивалентного элемента сохраняется прежний оригинал. Среди новых равных
входных элементов сохраняется первый оригинал; этот выбор не задаёт порядок
множества. Перестановка/повтор равного элемента не меняет состояние.
Новая команда переоформления оригинала эквивалентного set-элемента не вводится.

`exact` не нормализует Unicode, `unicode_ci` использует D145
`NFD(toCasefold(NFD(x)))`; пробелы значимы. NUMERIC использует нативное равенство
(`1 = 1.0`), TIMESTAMPTZ — равенство момента. Авторитетные comparator и версия
принадлежат DB write path; DTO не присылает готовый matching key. Семантика
definition и версия сравнения заморожены при любом instance, включая пустой
set и attrs tombstone. Новая семантика требует нового definition.

DN definition задаётся доверенным ID, имеет cardinality set и применимость
только к контейнерам. DN сохраняется в общей контейнерной паре attrs, без
registry/bindings как второго источника. Равенство RFC 5280/RFC 4518 и Unicode
3.2 отличается от D145; неизвестный OID не отвергается сам по себе,
поддерживаемый DirectoryString подготавливается, прочие значения сравниваются
точно в DER. DB codec получает исходный DER, сам вычисляет matching key
и отвергает неуспешную подготовку без смены equality.

## 5. Снимки агрегатов

Локальные immutable snapshots содержат только следующие предметные данные:

```text
ContainerSnapshot(id, kind, key, parent_id | None, revision, attributes)
SubjectSnapshot(id, holder_id, type_id, key, revision, deleted_at | None, attributes)
ObjectSnapshot(id, holder_id, key, revision, attributes)
ModelMetadata(id, holder_id, key, revision, attributes)
```

`attributes` — снимок существующих typed instances. Container address выдаётся
отдельно как вычисляемое значение того же снимка чтения. В SubjectSnapshot
`deleted_at` — статус lifecycle; None здесь означает активную запись и
не является null-значением атрибута. Ключи субъектов/объектов сохраняются точно,
без trim/Unicode normalization; запрет управляющих соответствует выбранному
design валидатору Cc, длина subject — 1–512 code points, object — непустой TEXT
без прикладного максимума. ASCII keys сохраняют исходное написание и имеют
явную ASCII CI equality. Holder и natural identity не изменяются командами.

Нет поля `content`, тела модели, privileges/actions, model references,
формата сериализации произвольного Python object или автоматического
«переноса content в attrs». Существующие `SubjectFacts` и `ObjectFacts`
могут быть проекцией исходной ссылки и holder для соответствующего
логического consumer. Model metadata остаётся отдельным DTO и не проецируется
в `ModelFacts`/полный набор исполнимых моделей PDP.

## 6. Общие входы и безопасные результаты

Каждая административная команда получает локальный
`ManagementContext(addressed_key, represented_key, certificate)`.
Адреса C и O — type-aware CompositeKey. `certificate` — установленный доверенной
границей `VerifiedCertificateFact`, не клиентское утверждение об успешной
проверке. В persistence adapter его `DNRef` несёт исходный Name DER из
аутентифицированного сертификата. Регистрация произвольного DNValue как
атрибута не создаёт факта аутентификации вызывающего.

Admission, поиск DN у явно указанного O, resolve и проверка области
`O <= C <= D` выполняются заново внутри transaction attempt. Клиент не передаёт
готовый `AdmittedCaller` или holder вместо авторитетного текущего holder.
Для существующего контейнера D — сам контейнер; для entity/model — holder;
при create child D — существующий parent, при create entity — holder.
Разные деревья/соседние ветки не устанавливают management scope.

Каждый пакет определяет собственные результаты, различимые по классу:

| Результат | Значение |
| --- | --- |
| `Created(snapshot)` | Новый агрегат зафиксирован, revision = 1 |
| `Changed(snapshot)` | Мутация зафиксирована, revision повышена один раз |
| `Unchanged(snapshot)` | При верной expected revision наблюдаемое состояние прежнее |
| `Removed(target_id, previous_revision)` | Physical delete зафиксирован; новой revision/строки нет |
| `NotFound` | Авторитетный lookup успешно подтвердил отсутствие требуемой записи |
| `RevisionConflict` | Агрегат существует, но expected revision устарела |
| `IdentityConflict` | Занят natural key; create не заменяет прежнюю запись |
| `RestoreRequired` | Subject identity занята tombstone; требуется явный restore с её revision |
| `InvalidInput(code, field)` | Неверная форма/тип/границы команды |
| `ManagementRejected(code)` | Нет допуска либо не выполнена область O <= C <= D |
| `InvariantRejected(code)` | Например, unknown definition/type, applicability, cardinality, непустой контейнер или запрещённая identity mutation |
| `FactsUnavailable(part, code)` | Не удалось установить обязательные факты; отсутствие не доказано |
| `StorageUnavailable(code)` | Операция не завершена; подтверждён откат либо транзакция не начиналась |
| `RetryExhausted` | Три безопасно откатившиеся попытки исчерпаны |
| `CommitOutcomeUnknown` | Подтверждение commit потеряно, нельзя достоверно заявить success или rollback |

Коды — закрытые локальные enum/классы, например `INVALID_ADDRESS`,
`ADMISSION_FAILED`, `OUT_OF_SCOPE`, `UNKNOWN_DEFINITION`, `NOT_APPLICABLE`,
`INVALID_CARDINALITY`, `CONTAINER_NOT_EMPTY`. Это не HTTP/error wire model.
Результат не содержит SQL, constraint names, DSN, traceback, исходный DN,
чужие ключи или произвольный текст исключения драйвера. Диагностика хранится
отдельно с соблюдением технической границы; свежий revision/token при конфликте
автоматически не возвращается вместо исходного expected token.

Объекты этих классов возвращаются только после завершения/отката attempt;
`Created`/`Changed`/`Unchanged`/`Removed` — только после подтверждённого commit.
На уровне внутреннего repository `NotFound` отличается от ошибки чтения.
Application сначала проверяет admission, прежде чем выдавать управленческие
результаты по найденной записи; наличие ID не обходит management scope.

## 7. Команды каждого владельца

В таблицах `ctx` означает ManagementContext, `expected` — Revision,
`changes` — AttributeChanges. Существующие строки выбираются по типизированному
stable ID; естественная identity служит точному поиску. У create нет
expected revision ещё несуществующего агрегата и нет клиентского ID.
Все перечисленные мутации используют общий transaction contract раздела 9.

### container-adm-api

| Команда/чтение | Вход | Успешный результат |
| --- | --- | --- |
| `CreateChild` | ctx, parent_id, kind, key, initial_attributes | Created(ContainerSnapshot) |
| `ChangeContainer` | ctx, container_id, expected, optional new_key, changes | Changed либо Unchanged |
| `DeleteContainer` | ctx, container_id, expected | Removed |
| `ResolveContainer` / `ReadContainer` / `ReadContainerPath` | Проверенный address либо ContainerId/Ref по порту раздела 3 | Ref / snapshot / CompletePath |

`ChangeContainer` объединяет rename и attrs, включая DN, одной командой;
ни parent, ни kind не являются изменяемыми входами. Отсутствие new_key
означает «оставить key». Create child проверяет parent/type и lifecycle gate;
он не требует клиентского token каждого предка и не меняет revision parent
из-за одной технической блокировки. Delete не каскадирует детей: child,
active subject, object или model metadata блокирует операцию. При успехе
в той же транзакции удаляются subject tombstones данного holder с их attrs,
attrs/DN контейнера и служебные object key guards. Tokens tombstones от клиента
не требуются. Concurrent restore/create согласуется DB lifecycle gate.

Runtime `CreateRoot` не вводится. Отдельная deployment-only команда
`ProvisionRoot(kind, key, initial_attributes)` принадлежит привилегированному
эксплуатационному executor, использует проверенные routines и одну транзакцию.
Initial DN передаётся через доверенное DN definition после его регистрации;
root без DN допустим. `catalog_operator` и обычные runtime роли не получают
это право вследствие владения каталогами или DDL.

### entity-subject-adm-api

```text
SubjectIdentity(holder_id: ContainerId, type_id: SubjectTypeId, key: str)
```

| Команда/чтение | Вход | Успешный результат |
| --- | --- | --- |
| `CreateSubject` | ctx, identity, initial_attributes | Created(SubjectSnapshot) |
| `ChangeSubjectAttributes` | ctx, subject_id, expected, changes | Changed либо Unchanged |
| `SoftDeleteSubject` | ctx, subject_id, expected | Changed либо Unchanged |
| `RestoreSubject` | ctx, subject_id, expected | Changed либо Unchanged |
| `ReadActiveSubject` / `FindActiveSubject` | SubjectId / точная SubjectIdentity | Активный SubjectSnapshot либо NotFound |
| `ReadAdminSubject` / `FindAdminSubject` | SubjectId / точная SubjectIdentity | SubjectSnapshot, включая tombstone, либо NotFound |

Admin repository/read нужен для получения прежнего ID/status/revision;
это внутренний контракт владельца, не новый публичный browse API.
Create по занятой активной identity возвращает IdentityConflict, по tombstone
— RestoreRequired, без создания строки или автоматической перезаписи attrs.
Вызывающий получает административный снимок и явно подаёт RestoreSubject
с прежним ID и expected revision. Команда заново загружает запись внутри
своей транзакции; прежний снимок не заменяет эту проверку.

Soft delete устанавливает DB timestamp только при переходе active -> deleted,
сохраняет ID/holder/type/key/attrs. Restore очищает deleted_at у прежнего ID,
сохраняя attrs; не принимает initial attrs вместо сохранённых и не создаёт
отсутствующую после purge запись. Повтор soft delete уже удалённого субъекта
или restore уже активного — Unchanged только при совпавшей expected revision.
ChangeSubjectAttributes не создаёт и не восстанавливает субъекта и не меняет
его deleted_at. Активный facts adapter никогда не возвращает tombstone.
Physical delete отдельного subject не предоставляется; purge — часть
DeleteContainer. Model-reference cleanup/повторное назначение относятся
к следующему change, а не имитируются здесь пустым списком.

### entity-object-adm-api

```text
ObjectIdentity(holder_id: ContainerId, key: str)
```

| Команда/чтение | Вход | Успешный результат |
| --- | --- | --- |
| `CreateObject` | ctx, identity, initial_attributes | Created(ObjectSnapshot) |
| `ChangeObjectAttributes` | ctx, object_id, expected, changes | Changed либо Unchanged |
| `DeleteObject` | ctx, object_id, expected | Removed |
| `ReadObject` / `FindObject` | ObjectId / точная ObjectIdentity | ObjectSnapshot либо NotFound |

Create/find передают полный key, а не авторитетный client digest. Сериализацию
конкурирующих записей и полное сравнение в bucket выполняет DB write path.
Hash collision разных строк не даёт IdentityConflict. Key/holder не входят
в изменяемые поля. Delete очищает собственные attrs и сохраняет holder,
subjects и model metadata. Будущий cleanup incoming model references
не входит в контракт реализованного T-3 adapter.

### policy-adm-api

```text
ModelIdentity(holder_id: ContainerId, key: str)
```

| Команда/чтение | Вход | Успешный результат |
| --- | --- | --- |
| `CreateModelMetadata` | ctx, identity, initial_attributes | Created(ModelMetadata) |
| `ChangeModelAttributes` | ctx, model_id, expected, changes | Changed либо Unchanged |
| `DeleteModelMetadata` | ctx, model_id, expected | Removed |
| `ReadModelMetadata` / `FindModelMetadata` | ModelId / ModelIdentity с ASCII CI key | ModelMetadata либо NotFound |
| `metadata_for` | tuple уникальных ContainerRef | ModelMetadataSet либо UnknownModelMetadataSet |

Новый `ModelMetadataRepositoryPort` читает/пишет только metadata и attrs.
Он не реализует старый `ModelRepositoryPort.save(ModelRecord)` и не принимает
`content`, references, privileges/actions. Delete удаляет metadata/свои attrs;
subjects/objects/holder сохраняются. Metadata не передаётся в
`ModelReferenceChecker` как будто проверенные refs уже записаны.

### Каталоговые операции

Управление каталогами — отдельный SQL-интерфейс глобального `catalog_operator`,
поставленный `db-control`, без назначения нового runtime сервиса:

```text
RegisterSubjectType(key) -> SubjectType(id, key)
RegisterAttributeDefinition(key, value_type, cardinality, string_profile,
                            comparison_profile_version, applicability)
    -> AttributeDefinition
SetApplicability(definition_id, explicit_applicability) -> current applicability
ChangeUnusedDefinitionSemantics(definition_id, value_type, cardinality,
                               string_profile, comparison_profile_version)
    -> AttributeDefinition
```

Applicability — четыре явных набора: container types, subject type IDs,
признак objects и признак models. Новые subject types не добавляются в набор
автоматически. DN definition допустим только для containers и set.
Зарегистрированный key не меняется; изменение семантики при любом instance
отклоняется. Снятие используемой applicability ограничено DB RESTRICT.
Удаление каталоговых записей/публичные delete API этим контрактом не вводятся.
Для каталогов не выдумывается entity expected_revision; конфликт и freeze
проверяются сериализованной операцией БД. Каталоговые права не дают полномочия
изменять attrs чужих контейнеров и не заменяют certificate admission.

## 8. ModelMetadataSet и policy-decision-api

Локальные типы `policy-adm-api` и `policy-decision-api` объявляются независимо:

```text
ContainerModelMetadata(container: ContainerRef, models: tuple[ModelMetadata, ...])
ModelMetadataSet(containers: tuple[ContainerRef, ...],
                 groups: tuple[ContainerModelMetadata, ...])
UnknownModelMetadataSet(code)
```

Для каждого запрошенного контейнера необходим ровно один group в порядке
`containers`, в том числе `models=()`. Duplicate container, отсутствующий group,
другой holder модели, повтор ModelId или ошибочное/частичное чтение дают unknown,
а не полный набор с пропуском. Неизвестный container не превращается в
group с нулём моделей. В path-сборке запрос всегда непустой и содержит весь
путь root -> holder объекта. Общий метод metadata_for может принять явно
пустой запрос и вернуть `ModelMetadataSet((), ())`; ошибка пути не формирует
такой запрос автоматически.

`ModelMetadataSet` не наследует и не реализует Protocol `CompleteModelSet`.
Нет adapter metadata -> CompleteModelSet, model evaluator или `Undefined`.
Полнота metadata означает только установленный состав IDs/holders/revisions
и их attrs, а не готовность моделей к исполнению.

Новый собственный reader `PreparedFactsReaderPort` имеет контракт:

```text
PreparedFactsRequest(addressed_key, represented_key, certificate,
                     subject: SubjectId | SubjectIdentity,
                     object: ObjectId | ObjectIdentity,
                     action: local ActionRef)

read(request) -> PreparedFactsSnapshot | RequestRejected
                | RequiredFactsUnavailable | UnknownPreparedFacts
```

Варианты selector явно различимы по local class; произвольный `Hashable`
не является persistence selector. Action остаётся opaque passthrough,
не требует новой таблицы/регистрации action. Адреса/selector проверяются
до чтения, admission и обязательные факты — внутри snapshot. Субъект ищется
только активный; отсутствие активного субъекта/объекта или ошибка обязательных
entity facts не превращается в Undefined модели.

`PreparedFactsSnapshot` содержит admitted caller, SubjectSnapshot,
ObjectSnapshot, исходный action, полный `CompletePath` до holder объекта,
ContainerSnapshots нужных C/O/узлов пути/holder субъекта и ModelMetadataSet
точно для этого пути. Их attrs входят в те же snapshots. Совпавший ContainerId
не дублируется. Reader подтверждает `C <= holder(object)`, включает предков C
до root и не отбрасывает субъекта из-за другой ветки/дерева его holder.
Он не накладывает management-отношение `O <= C` на access-check.

Отсутствие/ошибка полного пути или metadata даёт `UnknownPreparedFacts`
с явной частью `PATH`/`MODEL_METADATA`; обязательные entity facts отдельно
возвращают `RequiredFactsUnavailable`. Неправильная адресация/неуспешный допуск
дают `RequestRejected`. Эти результаты не являются EvaluatedDecision.
Старый `AccessCheckService.check`, его полный model provider и evaluator
не подключаются к этому reader в T-3; их T-1 Deny/Undefined semantics сохранены.

Reader открывает одну синхронную READ ONLY REPEATABLE READ session/transaction
**до первого SELECT**; все views/attributes/DN и проверка полноты используют
её. Результат материализуется неизменяемыми DTO до закрытия transaction:
lazy SQLAlchemy objects/сессионные query handles наружу не выходят.
Новое read() получает новый snapshot. Сборка не смешивает факты после
частичного повторного подключения/отдельного вызова source API; при ошибке
возвращается неполнота, а не достраивается «полный» snapshot из разных чтений.

## 9. Одна команда, session, CAS и три попытки

В каждом административном пакете application command владеет собственным
синхронным SQLAlchemy/Psycopg transaction boundary. Repository и adapters
получают текущую session/UoW; ни `get`, ни routines wrapper, ни запись attrs
не выполняют самостоятельный commit. Они не вызывают source API с отдельной
транзакцией вместо разрешённых DB views.

Один attempt использует одну SERIALIZABLE transaction:

1. Открыть session и установить isolation до первого SQL.
2. Разрешить C/O, проверить доверенный certificate Name/DN values и admission;
   загрузить current target/holder и фактические отношения.
3. Проверить `O <= C <= D`, инварианты, expected revision существующего target
   и прочитать definitions/applicability. Stale всегда даёт RevisionConflict,
   даже если предложенное изменение выглядит no-op.
4. Через обязательный DB write path выполнить CAS и mutation целевого агрегата,
   typed attrs и lifecycle/guard операции. Сохранить aggregate revision
   один раз; промежуточный scalar instance без значения допустим лишь внутри
   transaction и не может пройти commit.
5. Commit; только после подтверждения выдать успешный материализованный result.
   При отказе любой части, в том числе commit-time constraints, откатить всё.

Локальные transaction-bound repository методы: `get_by_id`, `find_by_identity`,
`insert`, `apply_changes(expected, ...)`, `delete(expected, ...)` и для subject
`soft_delete(expected)`/`restore(expected)`. Они возвращают типизированный
внутренний outcome; application публикует его лишь после commit. Это замена
для persistence пути, а не обещание совместимости старого save() по сигнатуре.

No-op — верный expected token и прежнее наблюдаемое логическое состояние:
тот же key с тем же написанием, прежние attrs с сохранёнными originals,
тот же lifecycle status. `ReplaceSet` с перестановкой/повторами равных элементов,
повтор Unset отсутствующего атрибута и пустые changes дают Unchanged.
Case-only rename контейнера меняет сохранённое написание и повышает revision.
No-op проходит admission/CAS-проверку и необходимую сериализацию, но не повышает
aggregate revision; две такие команды не обещают эксклюзивно «занять» token.

SQLSTATE `40001` и `40P01` после подтверждённого rollback допускают **не более
трёх attempts всего**: начальный и два повтора. Каждый начинается новой
session/transaction и заново читает/проверяет все факты с теми же immutable
входами и первоначальным expected_revision. Свежий token от имени клиента
не подставляется. Если после повтора revision уже другая, возвращается
RevisionConflict; после третьего retryable отказа — RetryExhausted.

Validation, admission, invariant/identity conflict, stale revision и NotFound
не повторяются автоматически. Потеря подтверждения commit не считается
доказанным rollback, даёт CommitOutcomeUnknown и не запускает слепой retry.
Идемпотентность повторного клиентского create/delete после неизвестного commit,
idempotency keys и transport retry policy не изобретаются этим change.

## 10. Переход Protocol и согласованный rollout

| Прежний контракт | Переход T-3 |
| --- | --- |
| Пять `CompositeKey(tuple[str, ...])` | Локальные typed segments; explicit conversion kind/key; JSON parsing только duplicate-aware |
| `ContainerFactsPort` с одним `ContainerTree` | Forest-capable SQL adapter; complete/unknown сохранены; exception/result boundary явно преобразуется |
| `CertificateBindingPort.is_bound_to(DNRef, O)` | Совместимый логический запрос к DN attribute конкретного O в текущей session, без второго bindings store |
| `SubjectRepositoryPort.get(Hashable)` и `SubjectService.get` | Отдельные active/admin selector contracts; T-1 facts projection сохраняет исходные ref/holder |
| `SubjectWritePort.save(...)->None`, `ObjectRepositoryPort.save(...)->None` | Новые application commands + transaction-bound repositories с revision/outcomes; старые update_content не служат DB write boundary |
| `ModelRepositoryPort` / `ModelRecord` | Отдельный ModelMetadataRepositoryPort/commands, без сохранения content/references |
| `ModelFactsPort.models_for()->CompleteModelSet` | Прежний T-1 порт сохраняется для logical provider; новый metadata_for возвращает только ModelMetadataSet |
| Независимые PDP calls к path/entity/model ports | Отдельный PreparedFactsReaderPort одной RR transaction; full persistent PDP не подключён |

Порядок внедрения пяти пакетов и адаптеров:

1. `container-adm-api`: определить typed address/ID mappings и forest/DN
   читающие контракты. Зафиксировать форму kind/key conversion, сохранив
   отдельно pure logical API и новый command/UoW boundary.
2. `entity-subject-adm-api` и `entity-object-adm-api`: объявить собственные
   typed addresses/IDs/attrs/snapshots и команды; явно map container refs,
   разделить subject active/admin read и restore. Эти два пакета после шага 1
   можно обновлять независимо.
3. `policy-adm-api`: обновить локальные адреса/ref adapters, добавить только
   metadata commands/repository/set; не направлять новый repository в старый
   ModelManagementService с content/references.
4. `policy-decision-api`: обновить свои address/ref DTO и добавить отдельные
   prepared snapshot/metadata types/reader. Старые T-1 operators и полные
   model contracts остаются до следующего change.
5. Обновить contract adapters и `TamarixTests/fixtures/cross_service.py`
   согласованным набором revisions. Адрес переносится по каждому `(kind,key)`,
   ID — через явный mapping; `.segments[-1]` не трактуется как bare key/ref.
   Проверить `.segments` copies в policy contract fixtures, key/tree tests
   и T-2 links; opaque test content остаётся только логическим fixture.

Новые command/snapshot contracts добавляются отдельно от старых content APIs.
Изменение адреса — явно breaking Python contract: одновременная работа старого
tuple-only consumer и нового provider не объявляется совместимой. Пока все
пять пакетов и contract fixtures не обновлены, persistent wiring не включается;
runtime health routes не расширяются. Старый адрес не распознаётся эвристически
по длине, отсутствующие типы не дополняются из похожего key.

DDL/views/routines предварительно поставляются `db-control`; runtime роли
получают только требуемые EXECUTE/SELECT grants. Сервисы не вызывают
`create_all`, не создают схемы и не делегируют предметное управление runtime
сервису db-control. Каталоговый SQL интерфейс не назначает новый каталоговый
сервис. При rollout будущих model references одновременно потребуются их
cleanup, affected model revisions и общий PDP snapshot; T-3 metadata release
не разрешает раннее добавление непроверенных reference writes.

В существующем коде подтверждены только logical/in-memory fixtures;
производственные данные и прежняя DB схема не исследованы. Неизвестный store
или legacy content не стирается/не сериализуется автоматически. Его импорт
требует отдельного явного mapping и проверки исходных данных. Откат code-only
изменений до persistent wiring возможен согласованным набором пакетов;
после полезных DB writes действуют forward-fix/backup границы design.

## 11. Проверяемый результат задачи 1.2

Последующая реализация проверяет без добавления HTTP контракта: duplicate-aware
address; явные BIGINT/ref conversions; сохранение source refs/holders;
initial revision 1 и no-op; stale token даже для no-op; typed scalar/set/absent;
restore прежнего ID с attrs; safe distinct results; три whole-transaction
attempts с исходным token; metadata completeness отдельно от CompleteModelSet;
один RR snapshot и отсутствие записи reader role. Автоматизированные случаи,
стабильные ID и scope прогона уже запланированы в [tasks.md](tasks.md).
Этот документ не отмечает задачи выполненными и не является test evidence.
