# Tasks

План и ход реализации основы хранения T-3. Состояние задач отражено checkbox;
фактические команды и отчёты приведены в конце. Основание: [proposal.md](proposal.md),
[design.md](design.md), [requirements.md](requirements.md) и шесть delta specs.
Зависимости указаны у каждой задачи; зависимый код начинается после принятия
соответствующего решения, а не после одного наличия файла design.

Принятая пользователем граница: метаданные моделей входят в T-3; непустые
модельные ссылки, их очистка, привилегии/actions, evaluator и подключение
полноценного persistent PDP относятся к следующему change. Никакая задача ниже
не создаёт временные reference tables, payload или тестовый evaluator для
имитации завершённого PDP. Область исходных 36 требований разобрана в разделе 12.

Пути файлов тестов и pytest node IDs ниже **планируемые**, а не существующие
или прошедшие проверки. Перед закрытием задач их нужно подтвердить фактической
коллекцией. Все test ID из раздела 13 стабильны: добавление или перестановка
сценариев не разрешает перенумеровывать существующие ID.

## 1. Принятие технического решения и контрактов

- [x] 1.1 [tamarix-specs; зависимость: нет] Получить явный результат review design, отдельно принять или скорректировать специальный тип DN и DB codec с Unicode 3.2, D145/profile versioning, SERIALIZABLE и whole-transaction retries, синхронный SQLAlchemy/Psycopg режим, SQL-интерфейс catalog_operator, DB roles, предлагаемый RESTRICT используемых каталогов и privileged deployment provisioning initial root + первичного DN. Проверка: bootstrap не выводится из владения DDL или имени db-control, не предоставляется catalog_operator и не вводит runtime create-root API; результат review с источником принятия сохранён в change, непринятое решение блокирует только зависимые задачи. Создание planning-артефактов не считать принятием.
- [x] 1.2 [tamarix-specs + пять сервисных репозиториев; зависимость: 1.1] Согласовать локальные DTO и application commands для type-aware JSON-адреса, BIGINT identity, expected revision, scalar/set/absent, restore прежнего субъекта и отдельного model metadata set; явно выбрать исходную revision, no-op и безопасные локальные результаты конфликтов/отсутствия. Проверка: документированы входы, результаты, преобразования прежних Protocol и согласованный порядок обновления пяти пакетов; новых HTTP routes, transport codes или общего runtime DTO-пакета нет.
- [x] 1.3 [tamarix-specs; внешняя зависимость: отдельный локальный change TamarixCD] Зафиксировать контракт и ссылку на внешний CD change для одноразовой PostgreSQL среды, migration executor, readiness и manifest scope postgresql-integration. Проверка: названы исполнитель, PostgreSQL/image version, db-control commit/Alembic head, isolation ID и передача DSN через secret env; CD planning/code этим центральным change не создаётся и не редактируется.
- [x] 1.4 [db-control + затронутые сервисы + TamarixTests; зависимость: 1.1] Проверить официальные стабильные релизы и совместимость Python, PostgreSQL, SQLAlchemy, Psycopg 3 и Alembic, включая поддержку согласованного Unicode алгоритма; согласовать конкретные pins. Проверка: источники и совместимый набор записаны; существующие принятые baselines не обновлены автоматически, prerelease и молчаливый downgrade исключены.
- [x] 1.5 [tamarix-specs; зависимость: 1.1–1.4] Сверить принятое решение с proposal/specs/design и этим планом; архитектурные ADR/context изменения выполнять лишь в отдельно согласованном объёме. Проверка: принятые решения, оставшиеся TBD и внешняя CD dependency различаются; требования следующего change не включены в критерии завершения foundation.

## 2. Воспроизводимая основа, миграции и тестовая среда

- [x] 2.1 [db-control; зависимость: 1.4–1.5] Создать устанавливаемый проект и Alembic entry point с согласованной Python/dependency фиксацией; в остальных затронутых пакетах добавить только необходимые зависимости адаптеров. Проверка в каждом изменённом репозитории: согласованы pyproject.toml, uv.lock, .python-version; проходят uv lock --check и uv sync --frozen без обновления lock при установке.
- [x] 2.2 [db-control; зависимость: 1.1, 2.1] Подготовить baseline migration с предметными схемами, PostgreSQL-generated BIGINT ID, base owner rows и положительной revision; включить preflight UTF8/block size/исходной схемы, deployment-only migration role и исходно закрытые предметные/catalog/reader roles. Минимальные grants на routines/views выдавать миграциями соответствующей feature group до её integration прогона; 10.1 завершает общий аудит прав. Проверка: миграции не стирают неизвестную существующую схему; все DDL, functions, triggers, roles и views находятся только в db-control, runtime create_all отсутствует.
- [x] 2.3 [db-control; зависимость: 2.2, 2.5 и доступная среда 1.3] Добавить tests/component/test_migrations.py для upgrade пустой БД, повторного upgrade head, downgrade/upgrade и повторного восстановления прав на одноразовой БД; документировать executor и forward-fix/backup границу после появления данных. Проверка: компонентные случаи выполняются по согласованной задаче, сохраняются команды, Alembic revision и отдельный отчёт; PostgreSQL major upgrade не подменяется Alembic baseline.
- [x] 2.4 [TamarixTests; зависимость: 1.3–1.5, 2.1, 2.5] Расширить validator manifest для postgresql-integration и добавить fixtures реального PostgreSQL: версии/commit/head, per-run либо per-case disposable DB, создание схемы только миграциями db-control, cleanup при отказе и отдельные соединения конкурентных случаев. Проверка: tests/unit/test_runner.py и component проверки отвергают отсутствующие/несовпадающие DB facts; DSN/пароли не попадают в manifest/report; logical-integration/http совместимость сохранена.
- [x] 2.5 [db-control + сервисы + TamarixTests; зависимость: 1.3–1.5, 2.1] Установить воспроизводимый протокол component/integration прогонов по требованию: содержательные русские docstrings и описания параметров, отдельный run ID/каталог, summary.md + results.json для любого исхода, JUnit по необходимости. Проверка: компонентные прогоны, включая ошибку коллекции/среды и отмену, сохраняют набор, версии, результаты/ошибки и NOT_RUN; integration использует существующий TamarixTests runner, а не запускается от commit/start/archive.

## 3. Контейнеры, forest и типизированные адреса

- [x] 3.1 [db-control; зависимость: 1.2, 2.2] Добавить ограничения parent/type, частичные root/sibling CI unique indexes, ASCII key checks, запрет изменения ID/type/parent и parent RESTRICT; full path не хранить. Проверка: tests/component/test_containers.py проверяет матрицу типов, независимые корни, длины 1/255/0/256, одинаковый key разных типов, регистровый дубль и обход прямым SQL.
- [x] 3.2 [container-adm-api; зависимость: 1.2, 3.1] Реализовать локальный type-aware адрес и PostgreSQL tree adapter: повторённые JSON member names выявляются до mapping, порядок членов несущественен, существующий уровень нельзя пропустить; rename сохраняет ID и меняет вычисляемые адреса потомков. Проверка: tests/test_t1_keys.py и новые tests/component/test_persistence_containers.py покрывают новый контракт и структурное отношение предка без key-only индекса.
- [ ] 3.3 [пять сервисов + TamarixTests; зависимость: 3.2] Согласованно обновить локальные consumer DTO/test adapters старого tuple-only адреса, сохраняя source ownership, complete/unknown и отсутствие общего пакета внутренних типов. Проверка: контрактные тесты пяти пакетов и прежние T-2 tests используют новый адрес без склейки типов/деревьев; migration notes описывают breaking переход.
- [ ] 3.4 [TamarixTests; зависимость: 2.4–2.5, 3.1–3.3] Реализовать tests/integration/persistence/test_containers.py::test_contract[c01]…[c14], [c22], [c23], зарегистрировать persistent-containers-c01…c14/c22/c23 как candidate и выполнить этот набор по согласованной apply-задаче. Проверка: реальные DB constraints и adapter сохраняют все критерии раздела 13.1; регистрация содержит точные links и русские описания; отчёт не заявляет HTTP/PKI.

## 4. Каталог типов и идентичность субъектов

- [x] 4.1 [db-control; зависимость: 1.1, 2.2, 3.1] Добавить глобальный каталог subject types и ограниченные registration routines; обеспечить key 1–512 ASCII CI/immutable и FK subject type. Проверка: tests/component/test_subjects.py проверяет границы, неизвестный тип, дубль/rename и отказ предметной роли без глобального полномочия.
- [x] 4.2 [db-control; зависимость: 4.1] Обеспечить subject identity по всей тройке holder/type/key, включая tombstones; запретить изменение ID/holder/type/key, точное Unicode равенство и согласованный control-character validator. Проверка: component tests проверяют различие типов/держателей, регистра/Unicode/пробелов, длины 1/512/0/513 и невозможность обхода identity прямым SQL.
- [x] 4.3 [entity-subject-adm-api; зависимость: 1.2, 4.2] Добавить PostgreSQL adapter и локальные команды субъектов, разделить активный и административный lookup, подготовить restore прежней записи без нового ID; не переносить name/description в JSONB content. Проверка: unit/component тесты repository и документация команд подтверждают identity/status mapping и один владеющий transaction boundary.
- [ ] 4.4 [TamarixTests; зависимость: 2.4–2.5, 4.1–4.3] Реализовать test_subjects.py::test_contract[c01]…[c05] в постоянном persistence каталоге, зарегистрировать соответствующие persistent-subjects-* candidate и выполнить набор. Проверка: зарегистрированный/неизвестный тип, полномочия каталога и точная тройка проверены через реальные роли/адаптеры, links соответствуют разделу 13.2; c06 с восстановлением tombstone выполняется в 9.5 после реализации lifecycle.

## 5. Длинные точные ключи объектов

- [x] 5.1 [db-control; зависимость: 1.1, 2.2, 3.1] Добавить objects key TEXT, nonunique digest candidate index и служебный key_guards с реальным MVCC UPDATE до полного сравнения; защитить write path и immutable identity, cleanup guards привязать к holder lifecycle. Проверка: tests/component/test_objects.py не использует unique hash или unique B-tree всего произвольного TEXT; исходный hash вычисляется доверенным DB path.
- [x] 5.2 [entity-object-adm-api; зависимость: 1.2, 5.1] Реализовать точные create/get команды и PostgreSQL adapter без прикладного максимума key, trim/normalization или замены сравнения на digest. Проверка: unit/component cases сохраняют длинные Unicode keys, точное различие регистра/представлений и holder identity; README описывает физические ограничения PostgreSQL.
- [x] 5.3 [db-control; зависимость: 5.1] Добавить компонентные race tests независимых транзакций для одного key и тест изолированного collision seam с полным comparator; проверить full-transaction retry со старым snapshot. Проверка: один duplicate commit и наблюдаемый конфликт; разные полные keys в bucket сосуществуют; production hash/права не ослаблены и тестовый seam недоступен runtime.
- [ ] 5.4 [TamarixTests; зависимость: 2.4–2.5, 5.2–5.3] Реализовать test_objects.py::test_contract[c01]…[c05], зарегистрировать persistent-objects-c01…c05 и выполнить набор. Проверка: настоящие commit/rollback и синхронизационные барьеры подтверждают все критерии раздела 13.3 без поиска реальной SHA-256 коллизии.

## 6. Отдельный контракт метаданных моделей

- [x] 6.1 [db-control; зависимость: 1.1–1.2, 2.2, 3.1] Добавить только model metadata identity: BIGINT, holder, key 1–512 ASCII CI, revision, immutable ID/holder/key. Проверка: tests/component/test_model_metadata.py покрывает unique/границы/FK; migration не создаёт privileges/actions/references/content columns.
- [x] 6.2 [policy-adm-api; зависимость: 1.2, 6.1] Добавить metadata DTO/repository и отдельный metadata set; не сериализовать ModelRecord.content и не выдавать metadata за CompleteModelSet. Проверка: unit/component тесты и README различают metadata, исполнимую модель и Unknown; прежнее ядро T-1 не получает фиктивный evaluator.
- [ ] 6.3 [TamarixTests; зависимость: 2.4–2.5, 6.1–6.2] Реализовать test_models.py::test_contract[c01], [c02], [c06], candidate persistent-models-c01/c02/c06 и выполнить набор. Проверка: реальные model metadata сохраняют identity и границу исполнения согласно разделу 13.5.
- [x] 6.4 [tamarix-specs + policy-adm-api; зависимость: 6.2] Документировать extension boundary следующего change: будущие ссылки обязаны добавить cleanup и affected model revision в той же транзакции до совместного rollout. Проверка: список сохранённых требований T3-28/29/30/32/33/35/36 и контракт metadata явно присутствуют; реализация ссылок в T-3 не заявлена.

## 7. Общие определения и типизированные атрибуты

- [x] 7.1 [db-control; зависимость: 1.1, 4.1, 5.1, 6.1] Добавить definitions и четыре applicability relation, общие CI immutable keys, четыре owner-specific instance/value pairs с прямыми owner FK и UNIQUE(owner, definition). Проверка: tests/component/test_attributes_schema.py проверяет настоящую применимость owner type, отсутствие polymorphic FK-обхода и независимость владельцев.
- [x] 7.2 [db-control; зависимость: 7.1] Реализовать ровно один нативный value column по определению, scalar ≤1 и deferred scalar =1 на commit, различие absent/empty set/null и корректность owner/instance cascade. Проверка: component tests проверяют все шесть типов, BIGINT boundaries, wrong type/multiple columns, scalar 0/2 и допустимое удаление scalar вместе с владельцем; допустимые 0, false и пустая строка не считаются SQL NULL или отсутствием заполненного value column.
- [x] 7.3 [db-control; зависимость: 1.1, 7.2] Реализовать exact set equality, D145 unicode_ci с фиксированной версией профиля и исходным написанием, реальные instance updates для конкурентного исключения повторов; структурные definition FK блокируют смену семантики/версии при instances. Проверка: tests/component/test_attribute_equality.py проверяет full casefold/canonical equivalence/пробелы, длинный TEXT, NUMERIC 1=1.0, одинаковый TIMESTAMPTZ instant, race duplicate и freeze при пустом set/tombstone.
- [x] 7.4 [container-adm-api + entity-subject-adm-api + entity-object-adm-api + policy-adm-api; зависимость: 1.2, 7.1–7.3] Добавить собственные attribute adapters/commands каждого владельца с общей DB семантикой и aggregate transaction path; name/description субъекта хранить только по definitions. Проверка: unit/component tests каждого сервиса проверяют local DTO/read semantics и отсутствие JSONB подмены; READMEs документируют новые команды и типы.
- [ ] 7.5 [TamarixTests; зависимость: 2.4–2.5, 7.1–7.4] Реализовать test_attributes.py::test_contract[c01]…[c17], [c19], [c20], зарегистрировать соответствующие persistent-attributes-* и выполнить набор; c13 внутри проверяет каждый из шести типов, c14 все ошибочные типизированные варианты. Проверка: критерии раздела 13.4 проверяются через реальные роли/adapters/DB; каждый параметр имеет своё русское описание и registry links, мощность scalar проверяется после commit; c18 с атрибутом tombstone выполняется в 9.5 после реализации lifecycle.
- [ ] 7.6 [TamarixTests; зависимость: 4.3, 7.4–7.5] Реализовать test_subjects.py::test_contract[c07] для name/description по общим definitions, зарегистрировать persistent-subjects-c07 и выполнить случай. Проверка: свойства читаются как собственные атрибуты, holder/type/key/ID сохранены.

## 8. DN как значение контейнерного множества

- [x] 8.1 [db-control; зависимость: явное принятие DN решения 1.1, 7.1–7.3] Реализовать согласованный DN value type и версионированный DER Name codec, доверенное DN definition и container-only applicability без самостоятельных DN registry/bindings. Проверка: tests/component/test_dn_codec.py подтверждает DER roundtrip, RDN order, AVA unordered equality и невозможность принять клиентский matching key как авторитетный.
- [x] 8.2 [db-control; зависимость: 8.1] Добавить RFC 5280/RFC 4518 подготовку поддерживаемых DirectoryString с закреплёнными таблицами и fallback точного DER только для прочих неизвестных значений; включить положительные, отрицательные и межкодировочные test vectors. Проверка: component tests отличают X.509 профиль от общего unicode_ci, сохраняют неизвестные OID, отвергают неуспех подготовки без смены равенства; непроверенный codec не объявлен завершённым.
- [x] 8.3 [container-adm-api; зависимость: 7.4, 8.1–8.2] Подключить DN attribute adapter к допуску T-1: Name берётся из установленного факта аутентификации сертификата и ищется у конкретного O. Проверка: unit/component tests допуска отличают доверенный Name от клиентской строки и сохраняют M:N семантику через атрибуты; документация не заявляет готовую PKI.
- [ ] 8.4 [TamarixTests; зависимость: 2.4–2.5, 8.1–8.3] Реализовать test_containers.py::test_contract[c15]…[c21], зарегистрировать persistent-containers-c15…c21 и выполнить набор. Проверка: реальные attribute storage/admission adapters проверяют несколько DN/контейнеров, эквивалентность, неизвестные OID, удаление/absence/empty в новом snapshot и отказ без аутентификации согласно разделу 13.1.
- [ ] 8.5 [container-adm-api + db-control; зависимость: 8.3–8.4] Документировать регистрацию/отзыв DN как aggregate mutation контейнера, профиль и обновление codec; проверить документы против actual routines и vectors. Проверка: нет второго источника DN binding, профиль/версия зафиксированы, subject identity не заменяется DN администратора.
- [x] 8.6 [db-control; зависимость: явное принятие bootstrap 1.1, 8.1–8.2] Поставить deployment-only команду атомарного initial root + DN provisioning через проверенные routines после регистрации DN-definition, с доверенным эксплуатационным Name и отдельной привилегией executor. Проверка: tests/component/test_bootstrap.py подтверждает полный rollback при ошибке DN, допустимость root без DN, отказ catalog_operator/runtime роли и отсутствие нового create-root HTTP API; README называет реального исполнителя и не назначает право по имени репозитория.

## 9. Aggregate revision, атомарность и жизненный цикл

- [ ] 9.1 [db-control + четыре административных сервиса; зависимость: 1.1–1.2, 3.2, 4.3, 5.2, 6.2, 7.4, 8.3] Завершить один UoW/application command: admission/views/facts, проверки O<=C<=D для rename/attributes/delete существующего контейнера и прочих management commands, CAS исходной expected revision, own attributes/DN и commit; включить ограниченные повторы 40001/40P01 всей транзакции с тем же token. Проверка: component tests каждого сервиса исключают обход области соседней веткой/другим деревом, отдельный repository commit, silent fresh revision и частичный rollback; technical versions не подменяют aggregate revision.
- [ ] 9.2 [db-control + entity-subject-adm-api; зависимость: 9.1] Реализовать soft delete/restore с сохранением identity/attributes, уникальностью tombstone и active lookup; физический DELETE active subject запрещён DB guard. Проверка: tests/component/test_subjects.py и сервисные component tests подтверждают прежний ID, отсутствие второй записи и атомарный откат deleted_at/attrs/revision; modelref cleanup не имитируется.
- [ ] 9.3 [db-control + entity-object-adm-api + policy-adm-api; зависимость: 9.1] Реализовать физическое удаление объекта и model metadata с каскадом собственных attributes и сохранением держателя/прочих сущностей. Проверка: component tests проверяют FK/cascade и отказ промежуточного шага; непустые модельные ссылки остаются вне schema/API этого этапа.
- [ ] 9.4 [db-control + container-adm-api; зависимость: 9.2–9.3] Реализовать lifecycle gate и child-first container delete: блокировка при child/active subject/object/model, atomic purge tombstones/attrs/DN/guards, согласование с create/restore. Проверка: tests/component/test_containers.py использует независимые соединения и барьеры; победивший restore блокирует purge либо получает NotFound/conflict после purge, active subject не удаляется.
- [ ] 9.5 [TamarixTests; зависимость: 2.4–2.5, 9.1–9.4] Реализовать test_containers.py::test_contract[c24]…[c30], test_subjects.py::test_contract[c06], [c08]…[c12], test_objects.py::test_contract[c06]…[c08], test_models.py::test_contract[c03]…[c05] и test_attributes.py::test_contract[c18], зарегистрировать соответствующие persistent-* candidate и выполнить набор. Проверка: все race/CAS/failure-injection/lifecycle/management-scope критерии разделов 13.1–13.5 подтверждены реальным PostgreSQL; holder delete c26 проверяет каждого блокирующего владельца/ребёнка, c29/c30 — rename, attribute и delete в допустимой области и при нарушении каждой части O<=C<=D.
- [ ] 9.6 [четыре административных сервиса + db-control; зависимость: 9.5] Обновить документацию mutation/restore/delete и retry/error boundary по реально реализованным командам. Проверка: lifecycle, revision и атомарность описаны без HTTP обещаний; сохранённые будущие cleanup требования и несовместимость их раннего включения отмечены.

## 10. Read-only views и подготовленный снимок

- [ ] 10.1 [db-control; зависимость: 1.1, 7.1–7.3, 8.1, 9.1–9.4] Завершить разрешённые fact views и grants: path/holders/active subjects/objects/attributes/DN/model metadata, только SELECT для reader и ограниченные routines предметных/catalog ролей. Проверка: tests/component/test_database_roles.py проверяет отсутствие runtime DDL/TRUNCATE/широкого DML, закрытый PUBLIC EXECUTE и фиксированный search_path SECURITY DEFINER; view не скрывает существующую model metadata из-за tombstone субъекта.
- [ ] 10.2 [policy-decision-api; зависимость: 1.2, 10.1] Добавить отдельный reader подготовленных фактов с одной READ ONLY REPEATABLE READ транзакцией до первого чтения, полным root-to-holder path и явными metadata empty/unknown. Проверка: tests/component/test_persistence_snapshot.py использует локальные DTO, не отбрасывает субъект из другой ветки и не подключает reader как CompleteModelSet/evaluator полного PDP.
- [ ] 10.3 [TamarixTests; зависимость: 2.4–2.5, 10.1–10.2] Реализовать test_fact_views.py::test_contract[c01]…[c05], зарегистрировать persistent-facts-c01…c05 и выполнить набор. Проверка: другой DB connection коммитит между чтениями, старая сборка остаётся согласованной, новая видит commit; path/metadata failures не превращаются в empty; SELECT role не может писать/делать DDL согласно разделу 13.6.
- [ ] 10.4 [policy-decision-api + db-control; зависимость: 10.3] Документировать public Python contract reader и views, snapshot lifetime, отсутствие persistent evaluator и extension следующего change. Проверка: consumer docs различают metadata completeness и исполнимую модель/Undefined; ограничения T-1 не переопределены.

## 11. Общая проверка, отчёты и подготовка promotion

- [ ] 11.1 [tamarix-specs + TamarixTests; зависимость: 3.4, 4.4, 5.4, 6.3, 7.5–7.6, 8.4, 9.5, 10.3] Сверить фактическую коллекцию всех 81 planned scenario cases раздела 13 с реестром и заменить planned node references подтверждёнными; проверить каждый точный THEN/AND, русские docstrings/descriptions и актуальные T-2 links после breaking изменений. Проверка: validate-registry --change t-3-persistent проходит, IDs не перенумерованы, нет исчезнувших cases или непокрытых delta-критериев.
- [ ] 11.2 [db-control + пять сервисов + TamarixTests; зависимость: все feature groups и 11.1] По согласованной apply-задаче выполнить требуемые unit/component/contract и migration проверки фиксированных версий, включая повторное upgrade/downgrade на одноразовой БД. Проверка: фактические команды, версии и отдельные summary/JSON/JUnit каждого прогона сохранены; ноль тестов, SKIP/XFAIL/NOT_RUN или collection/environment error не закрывают задачу.
- [ ] 11.3 [TamarixTests; зависимость: 11.2 и готовый результат внешнего CD change 1.3] Получить manifest фактических чистых commits и выполнить полный run --change t-3-persistent, включающий новые cases и существующий регресс T-2. Проверка: полный requested/collected/executed набор имеет PASS, manifest фиксирует PostgreSQL/image/Alembic/db-control/source revisions и spec/delta hashes; новый каталог отчёта не перезаписывает прежний.
- [ ] 11.4 [TamarixTests; зависимость: 11.3] Выполнить promote для полного успешного отчёта и зафиксировать candidate -> regression в registry.yaml без перемещения исходников. Проверка: stable IDs/links сохранены, promotion commit явно записан; предыдущее evidence не выдаётся за проверку нового commit.
- [ ] 11.5 [TamarixTests + tamarix-specs; зависимость: 11.4] Получить новый manifest окончательного promotion commit и явно повторить полный набор change + текущий регресс. Проверка: новый завершённый PASS соответствует окончательным immutable revisions; диагностика с --id/--level и старый отчёт не используются для archive.
- [ ] 11.6 [tamarix-specs; зависимость: 11.5] Записать фактические команды/результаты в этот tasks.md и подготовить verification/evidence со ссылками и hashes артефактов, scope foundation и сохранёнными ограничениями; проверить существующий archive gate на готовых данных. Проверка: полнота criterion coverage, promotion, commits, reports и граница следующего change подтверждены; при недоступной/неуспешной проверке соответствующие задачи остаются открытыми. Новые verification/evidence файлы создаются только в будущей согласованной реализации, не данным планированием.

## 12. Прослеживаемость исходных требований и отложенный объём

Указания T3-* — источник из requirements.md, а не дополнительные test ID.
Наблюдаемые критерии foundation ниже раскрыты точно в разделе 13. Технические
проверки DDL/миграций/изоляции дополняют их и принадлежат названным component
tests; общие требования не превращаются автоматически в отдельные capabilities.

| Источник | Реализация и проверка foundation | Сохранённая граница |
| --- | --- | --- |
| T3-01 | 2–10; все шесть групп integration | Только metadata моделей и подготовленные факты |
| T3-02 | 2.2–2.4, 10.1; migration/role component tests | Одна PostgreSQL БД, DDL только db-control |
| T3-03 | 3.4 c22, subjects c04/c06/c09, objects c03, models c01/c02 | Не обещается непрерывность ID |
| T3-04 | containers c01–c06; facts c02 | Родство по parent, forest без подразумеваемого tenant |
| T3-05 | containers c07–c09/c12/c13 | ASCII CI с учётом типа |
| T3-06 | containers c10/c11/c14/c22 | Полный фактический JSON-адрес, без stored path |
| T3-07 | containers c22/c23 | Только переименование key |
| T3-08 | subjects c04/c06, objects c03, models c01/c02 | Неизменяемый единственный holder |
| T3-09 | subjects c06/c09, objects c03, models c02 | Restore прежней subject identity |
| T3-10 | subjects c01/c04/c06 | Глобальный зарегистрированный type |
| T3-11 | subjects c05 | Exact Unicode до 512 |
| T3-12 | objects c01/c02 | TEXT без прикладного максимума |
| T3-13 | objects c04/c05 + component race/collision cases | Full comparison, не unique digest |
| T3-14 | models c01/c02 | Holder-local ASCII CI |
| T3-15 | models c06; задачи 6.4/10.4 | Privileges/actions/payload/evaluator/ref storage следующим change |
| T3-16 | subjects c02; attributes c02–c04 | Каталоги раздельны, keys immutable |
| T3-17 | subjects c03; attributes c19/c20; roles component | SQL catalog interface требует принятия 1.1, HTTP owner не назначен |
| T3-18 | subjects c07; attributes c01/c05/c07/c08 | Четыре пары, без JSONB subject content |
| T3-19 | attributes c05/c06 | Применимость явная |
| T3-20 | attributes c09/c10 | Scalar/set |
| T3-21 | attributes c11/c12 | Absence != empty, null запрещён |
| T3-22 | attributes c07/c08 + schema component | Прямые FK четырёх owner pairs |
| T3-23 | attributes c13/c14 | Шесть начальных native types |
| T3-24 | attributes c15/c16 + equality component | D145 отдельно от DN StringPrep |
| T3-25 | attributes c17/c18 + concurrent freeze component | Пустой set/tombstone тоже удерживают семантику |
| T3-26 | containers c18/c19/c20 | DN только multivalue attribute |
| T3-27 | containers c15–c17/c20/c21 | Trusted certificate fact, PKI deployment вне T-3 |
| T3-28 | subjects c06/c08/c09/c10/c12 | Cleanup непустых modelrefs и отсутствие их восстановления проверит следующий change |
| T3-29 | objects c06/c08 | Cleanup непустых modelrefs при physical delete — следующий change |
| T3-30 | models c05 | Очистка будущих внутренних связей — следующий change |
| T3-31 | containers c26–c28 + lifecycle component | Child-first, tombstone purge |
| T3-32 | containers c25, subjects c12, objects c08, models c04 | Транзакционность modelref cleanup проверит следующий change |
| T3-33 | containers c24, subjects c11, objects c07, models c03 | CAS own aggregate; affected modelrefs revisions — следующий change |
| T3-34 | facts c01 | В T-3 согласованный подготовленный snapshot; общий snapshot полноценного PDP — следующий change |
| T3-35 | containers c06/c15–c17/c29/c30, существующий регресс T-1/T-2 и component management tests | O<=C<=D сохраняется; persistence допустимости/очистки будущих refs — следующий change |
| T3-36 | facts c02–c04, models c06, действующий T-2 регресс | Full persistent model set/evaluator/Deny/Undefined integration — следующий change |

Отложенные части не объявляются реализованными по пустым ссылкам, metadata
или in-memory evaluator и не расширяют критерии завершения foundation T-3.
Они должны войти в proposal/specs/acceptance следующего отдельного change
до включения model references или полноценного persistent PDP.

## 13. Полная планируемая связь delta-критериев с integration tests

Для каждой таблицы путь в заголовке — **полный delta spec path каждой строки**.
Колонки Requirement/Scenario и критерий воспроизводят точные названия и THEN/AND
из соответствующего файла. Каждая строка вместе с этим путём задаёт:
spec path + Requirement + Scenario + criterion -> stable test ID ->
репозиторий TamarixTests + точный planned pytest node ID.

Все случаи имеют level integration, introduced_by t-3-persistent, начальный
state candidate. В registry links хранится постоянный основной путь
openspec/specs/<capability>/spec.md; validator --change разрешает его против
delta T-3. Это не переносит основные specs в ходе planning. Исходники остаются
в постоянном tests/integration/persistence после promotion.

Каждый test_contract[cNN] имеет собственные русские условия/ожидаемый результат/
назначение в case data и registry. Когда сценарий перечисляет несколько
вариантов, данный collected case проверяет все перечисленные варианты; при
дальнейшем разделении на отдельные collected parameters нужно сохранить ID
и явно расширить связи, не потеряв ни один THEN/AND. Единственный THEN таблицы
типов containers c01 проверяет всю приведённую в spec матрицу.

### 13.1. containers

`openspec/changes/t-3-persistent/specs/containers/spec.md`

| Requirement | Scenario | Точный критерий THEN/AND | Стабильный test ID | TamarixTests: planned pytest node ID |
| --- | --- | --- | --- | --- |
| Упорядоченное дерево контейнеров | Допустимые непосредственные дети | допустимость по типам SHALL соответствовать таблице: | `persistent-containers-c01` | `tests/integration/persistence/test_containers.py::test_contract[c01]` |
| Упорядоченное дерево контейнеров | Обратный порядок типов | связь SHALL быть отклонена как нарушающая порядок типов | `persistent-containers-c02` | `tests/integration/persistence/test_containers.py::test_contract[c02]` |
| Упорядоченное дерево контейнеров | Повторение типа вдоль пути | связь SHALL быть отклонена как повторение типа вдоль пути | `persistent-containers-c03` | `tests/integration/persistence/test_containers.py::test_contract[c03]` |
| Упорядоченное дерево контейнеров | Соседние контейнеры одного типа | обе связи SHALL быть допустимы по типам; дети SHALL оставаться в разных ветках | `persistent-containers-c04` | `tests/integration/persistence/test_containers.py::test_contract[c04]` |
| Упорядоченное дерево контейнеров | Два непосредственных родителя | состояние SHALL быть отклонено как нарушающее дерево с единственным непосредственным родителем некорневого контейнера | `persistent-containers-c05` | `tests/integration/persistence/test_containers.py::test_contract[c05]` |
| Упорядоченное дерево контейнеров | Независимые корни | все деревья SHALL сохраняться независимо, а корень одного дерева не SHALL считаться предком узла другого дерева | `persistent-containers-c06` | `tests/integration/persistence/test_containers.py::test_contract[c06]` |
| Строковый ключ контейнера | Ключ задан строкой | ключ SHALL сохраняться и использоваться как собственный текстовый ключ контейнера | `persistent-containers-c07` | `tests/integration/persistence/test_containers.py::test_contract[c07]` |
| Строковый ключ контейнера | Нестроковый ключ | значение SHALL не быть признано допустимым ключом контейнера | `persistent-containers-c08` | `tests/integration/persistence/test_containers.py::test_contract[c08]` |
| Строковый ключ контейнера | Границы собственного ключа | ключи длиной 1 и 255 допустимого алфавита SHALL приниматься, остальные перечисленные ключи SHALL отклоняться | `persistent-containers-c09` | `tests/integration/persistence/test_containers.py::test_contract[c09]` |
| Уникальная идентификация составным ключом | Путь до вложенного контейнера | адрес SHALL включать пары типов и ключей root, C и D и однозначно указывать на D независимо от порядка членов JSON | `persistent-containers-c10` | `tests/integration/persistence/test_containers.py::test_contract[c10]` |
| Уникальная идентификация составным ключом | Составной ключ корня | его адрес SHALL содержать только пару собственного типа и ключа корня | `persistent-containers-c11` | `tests/integration/persistence/test_containers.py::test_contract[c11]` |
| Уникальная идентификация составным ключом | Дублирование составного ключа | система SHALL не допустить принадлежность этого адреса обоим контейнерам | `persistent-containers-c12` | `tests/integration/persistence/test_containers.py::test_contract[c12]` |
| Уникальная идентификация составным ключом | Одинаковый ключ разных типов | оба корня или оба ребёнка SHALL сохраняться с различными адресами и ID | `persistent-containers-c13` | `tests/integration/persistence/test_containers.py::test_contract[c13]` |
| Уникальная идентификация составным ключом | Пропуск существующего уровня или повтор типа | адрес SHALL отклоняться и не SHALL разрешаться как адрес другого контейнера | `persistent-containers-c14` | `tests/integration/persistence/test_containers.py::test_contract[c14]` |
| Сертификатное подтверждение представляемого контейнера | DN приписан к представляемому контейнеру | представляемый контейнер SHALL считаться подтверждённым для этого обращения | `persistent-containers-c15` | `tests/integration/persistence/test_containers.py::test_contract[c15]` |
| Сертификатное подтверждение представляемого контейнера | DN приписан только к другому контейнеру | обращение SHALL быть отклонено; принадлежность DN к `Q` SHALL не подтверждать `O` | `persistent-containers-c16` | `tests/integration/persistence/test_containers.py::test_contract[c16]` |
| Сертификатное подтверждение представляемого контейнера | Отсутствует успешная сертификатная аутентификация | оно SHALL не допускаться к выполнению запрошенной операции | `persistent-containers-c17` | `tests/integration/persistence/test_containers.py::test_contract[c17]` |
| Сертификатное подтверждение представляемого контейнера | Несколько DN и несколько контейнеров | каждый DN SHALL подтверждать только явно указанный контейнер, в множестве DN которого присутствует эквивалентное значение | `persistent-containers-c18` | `tests/integration/persistence/test_containers.py::test_contract[c18]` |
| Сертификатное подтверждение представляемого контейнера | Удалённое значение DN | такой DN SHALL не подтверждать O | `persistent-containers-c19` | `tests/integration/persistence/test_containers.py::test_contract[c19]` |
| Сравнение значений DN | Эквивалентные имена | проверка SHALL находить регистрацию, а повторная запись эквивалентного DN не SHALL создавать второй элемент множества | `persistent-containers-c20` | `tests/integration/persistence/test_containers.py::test_contract[c20]` |
| Сравнение значений DN | Неизвестные OID | OID SHALL приниматься, а равенство SHALL определяться подготовкой строки в первом случае и точным DER значения во втором | `persistent-containers-c21` | `tests/integration/persistence/test_containers.py::test_contract[c21]` |
| Стабильная идентичность и переименование контейнера | Переименование предка | ID предка и потомков и их связи SHALL сохраняться, а вычисляемые адреса SHALL отражать новый ключ | `persistent-containers-c22` | `tests/integration/persistence/test_containers.py::test_contract[c22]` |
| Стабильная идентичность и переименование контейнера | Конфликт или изменение структуры | изменение SHALL отклоняться без частичного изменения контейнера или его атрибутов | `persistent-containers-c23` | `tests/integration/persistence/test_containers.py::test_contract[c23]` |
| Атомарное изменение контейнера и revision | Конкурентное изменение атрибута | не более одной команды SHALL фиксироваться с этой revision, а вторая SHALL получать конфликт | `persistent-containers-c24` | `tests/integration/persistence/test_containers.py::test_contract[c24]` |
| Атомарное изменение контейнера и revision | Ошибка после записи части данных | контейнер, его атрибуты и revision SHALL оставаться в состоянии до этой операции | `persistent-containers-c25` | `tests/integration/persistence/test_containers.py::test_contract[c25]` |
| Удаление контейнера после внутренних сущностей | Непустой держатель | удаление SHALL отклоняться с сохранением контейнера и всех его данных | `persistent-containers-c26` | `tests/integration/persistence/test_containers.py::test_contract[c26]` |
| Удаление контейнера после внутренних сущностей | Только удалённые субъекты | контейнер, tombstones и принадлежащие им атрибуты SHALL удаляться физически одной операцией | `persistent-containers-c27` | `tests/integration/persistence/test_containers.py::test_contract[c27]` |
| Удаление контейнера после внутренних сущностей | Восстановление одновременно с удалением держателя | субъект SHALL либо восстановиться и блокировать удаление держателя, либо получить конфликт или отсутствие после purge; активная запись не SHALL удаляться физически | `persistent-containers-c28` | `tests/integration/persistence/test_containers.py::test_contract[c28]` |
| Область операций над существующим контейнером | Управление своим поддеревом | операция SHALL быть допустима по области управления при сохранении остальных инвариантов | `persistent-containers-c29` | `tests/integration/persistence/test_containers.py::test_contract[c29]` |
| Область операций над существующим контейнером | Выход за адресованную область | операция SHALL отклоняться без изменения контейнера и его атрибутов | `persistent-containers-c30` | `tests/integration/persistence/test_containers.py::test_contract[c30]` |

### 13.2. entities/subjects

`openspec/changes/t-3-persistent/specs/entities/subjects/spec.md`

| Requirement | Scenario | Точный критерий THEN/AND | Стабильный test ID | TamarixTests: planned pytest node ID |
| --- | --- | --- | --- | --- |
| Общий каталог типов субъектов | Зарегистрированный и неизвестный тип | зарегистрированный тип SHALL приниматься, а неизвестный SHALL отклоняться без создания субъекта | `persistent-subjects-c01` | `tests/integration/persistence/test_subjects.py::test_contract[c01]` |
| Общий каталог типов субъектов | Правила ключа типа | только свободные допустимые ключи SHALL приниматься; остальные перечисленные операции SHALL отклоняться | `persistent-subjects-c02` | `tests/integration/persistence/test_subjects.py::test_contract[c02]` |
| Общий каталог типов субъектов | Владелец контейнера без глобального полномочия | операция SHALL отклоняться независимо от его прав на данные контейнера | `persistent-subjects-c03` | `tests/integration/persistence/test_subjects.py::test_contract[c03]` |
| Постоянная предметная идентичность субъекта | Разные типы и держатели | субъекты SHALL создаваться с разными ID без конфликта уникальности | `persistent-subjects-c04` | `tests/integration/persistence/test_subjects.py::test_contract[c04]` |
| Постоянная предметная идентичность субъекта | Точное сравнение и границы ключа | точные различные допустимые строки SHALL сохраняться независимо; пустой, слишком длинный и управляющий ключи SHALL отклоняться | `persistent-subjects-c05` | `tests/integration/persistence/test_subjects.py::test_contract[c05]` |
| Постоянная предметная идентичность субъекта | Дубль и изменение идентичности | дубликат или изменение SHALL отклоняться без подмены ID; для tombstone SHALL применяться восстановление прежней записи | `persistent-subjects-c06` | `tests/integration/persistence/test_subjects.py::test_contract[c06]` |
| Атрибуты субъекта по общим определениям | Именованные свойства субъекта | свойства SHALL читаться как атрибуты соответствующего субъекта и не SHALL изменять его идентичность | `persistent-subjects-c07` | `tests/integration/persistence/test_subjects.py::test_contract[c07]` |
| Логическое удаление и восстановление субъекта | Удалённый субъект и активное чтение | запись и атрибуты SHALL сохраняться с deleted_at, а поиск активного субъекта SHALL не возвращать её | `persistent-subjects-c08` | `tests/integration/persistence/test_subjects.py::test_contract[c08]` |
| Логическое удаление и восстановление субъекта | Восстановление прежней записи | deleted_at SHALL очищаться у прежнего ID с прежними атрибутами, без создания второй записи | `persistent-subjects-c09` | `tests/integration/persistence/test_subjects.py::test_contract[c09]` |
| Логическое удаление и восстановление субъекта | Попытка физического удаления активного субъекта | операция SHALL отклоняться с сохранением активной записи | `persistent-subjects-c10` | `tests/integration/persistence/test_subjects.py::test_contract[c10]` |
| Атомарность и revision субъекта | Устаревшая revision после изменения атрибута | команда SHALL получать конфликт без перезаписи сохранённого состояния | `persistent-subjects-c11` | `tests/integration/persistence/test_subjects.py::test_contract[c11]` |
| Атомарность и revision субъекта | Отказ составной записи | субъект, его атрибуты, deleted_at и revision SHALL оставаться в состоянии до операции | `persistent-subjects-c12` | `tests/integration/persistence/test_subjects.py::test_contract[c12]` |

### 13.3. entities/objects

`openspec/changes/t-3-persistent/specs/entities/objects/spec.md`

| Requirement | Scenario | Точный критерий THEN/AND | Стабильный test ID | TamarixTests: planned pytest node ID |
| --- | --- | --- | --- | --- |
| Постоянная идентичность объекта и точный ключ | Длинные и точные ключи | все допустимые точные различные ключи SHALL сохраняться и находиться без искусственного ограничения длины | `persistent-objects-c01` | `tests/integration/persistence/test_objects.py::test_contract[c01]` |
| Постоянная идентичность объекта и точный ключ | Пустой или управляющий ключ | создание SHALL отклоняться без сохранения объекта | `persistent-objects-c02` | `tests/integration/persistence/test_objects.py::test_contract[c02]` |
| Постоянная идентичность объекта и точный ключ | Другой держатель или изменение идентичности | новый объект в другом держателе SHALL получать другой ID, а изменение идентичности прежнего объекта SHALL отклоняться | `persistent-objects-c03` | `tests/integration/persistence/test_objects.py::test_contract[c03]` |
| Точная конкурентная уникальность ключа объекта | Конкурентный дубликат | SHALL фиксироваться ровно один объект, а другая операция SHALL получать конфликт уникальности | `persistent-objects-c04` | `tests/integration/persistence/test_objects.py::test_contract[c04]` |
| Точная конкурентная уникальность ключа объекта | Коллизия поискового хеша | оба объекта SHALL сохраняться и разрешаться по полному ключу независимо друг от друга | `persistent-objects-c05` | `tests/integration/persistence/test_objects.py::test_contract[c05]` |
| Физическое удаление объекта и его атрибутов | Удаление собственных данных объекта | объект и его атрибуты SHALL отсутствовать после commit, а держатель, субъекты и метаданные моделей SHALL сохраняться | `persistent-objects-c06` | `tests/integration/persistence/test_objects.py::test_contract[c06]` |
| Атомарность и revision объекта | Конфликт после изменения атрибута | команда SHALL отклоняться как конфликт без перезаписи текущего агрегата | `persistent-objects-c07` | `tests/integration/persistence/test_objects.py::test_contract[c07]` |
| Атомарность и revision объекта | Ошибка составной операции | объект, его атрибуты и revision SHALL оставаться в состоянии до операции | `persistent-objects-c08` | `tests/integration/persistence/test_objects.py::test_contract[c08]` |

### 13.4. attributes

`openspec/changes/t-3-persistent/specs/attributes/spec.md`

| Requirement | Scenario | Точный критерий THEN/AND | Стабильный test ID | TamarixTests: planned pytest node ID |
| --- | --- | --- | --- | --- |
| Предварительная регистрация общих определений | Запись без зарегистрированного определения | операция SHALL быть отклонена без создания определения, экземпляра или значения | `persistent-attributes-c01` | `tests/integration/persistence/test_attributes.py::test_contract[c01]` |
| Неизменяемые ключи определений атрибутов | Регистронезависимый конфликт ключей | регистрация второго определения SHALL быть отклонена как конфликт ключа | `persistent-attributes-c02` | `tests/integration/persistence/test_attributes.py::test_contract[c02]` |
| Неизменяемые ключи определений атрибутов | Границы и алфавит ключа определения | первые два ключа SHALL быть допустимы, а остальные SHALL быть отклонены без регистрации определения | `persistent-attributes-c03` | `tests/integration/persistence/test_attributes.py::test_contract[c03]` |
| Неизменяемые ключи определений атрибутов | Переименование зарегистрированного определения | операция SHALL быть отклонена, а прежний ключ SHALL сохраниться | `persistent-attributes-c04` | `tests/integration/persistence/test_attributes.py::test_contract[c04]` |
| Явная применимость определения | Одно определение у нескольких разрешённых видов | значение SHALL сохраняться у каждого соответствующего владельца по одному общему определению | `persistent-attributes-c05` | `tests/integration/persistence/test_attributes.py::test_contract[c05]` |
| Явная применимость определения | Владелец вне явной применимости | запись SHALL быть отклонена без создания экземпляра или изменения прежних значений | `persistent-attributes-c06` | `tests/integration/persistence/test_attributes.py::test_contract[c06]` |
| Принадлежность экземпляра конкретному владельцу | Независимые значения разных владельцев | значение SHALL измениться только у выбранного владельца, а данные другого SHALL сохраниться | `persistent-attributes-c07` | `tests/integration/persistence/test_attributes.py::test_contract[c07]` |
| Принадлежность экземпляра конкретному владельцу | Несуществующий владелец экземпляра | операция SHALL быть отклонена без сохранения экземпляра или его значений | `persistent-attributes-c08` | `tests/integration/persistence/test_attributes.py::test_contract[c08]` |
| Одиночное значение и неупорядоченное множество | Недопустимая мощность одиночного атрибута | операция SHALL быть отклонена без изменения прежнего состояния атрибута | `persistent-attributes-c09` | `tests/integration/persistence/test_attributes.py::test_contract[c09]` |
| Одиночное значение и неупорядоченное множество | Порядок и повтор элемента множества | состав множества SHALL оставаться прежним без второго равного элемента и без значимого порядка значений | `persistent-attributes-c10` | `tests/integration/persistence/test_attributes.py::test_contract[c10]` |
| Различение отсутствия, пустого множества и null | Отсутствующий атрибут и существующее пустое множество | чтение SHALL различать отсутствие атрибута у первого и существующее пустое множество у второго | `persistent-attributes-c11` | `tests/integration/persistence/test_attributes.py::test_contract[c11]` |
| Различение отсутствия, пустого множества и null | Явное null-значение | операция SHALL быть отклонена без сохранения null-значения или частичного изменения атрибута | `persistent-attributes-c12` | `tests/integration/persistence/test_attributes.py::test_contract[c12]` |
| Соответствие нативного значения типу определения | Сохранение каждого начального типа | после чтения SHALL сохраняться соответствующие типы и значения без подмены всех значений строками | `persistent-attributes-c13` | `tests/integration/persistence/test_attributes.py::test_contract[c13]` |
| Соответствие нативного значения типу определения | Несоответствующий тип или несколько типизированных значений | операция SHALL быть отклонена без изменения существующего атрибута | `persistent-attributes-c14` | `tests/integration/persistence/test_attributes.py::test_contract[c14]` |
| Профили сравнения строковых атрибутов | Точное сравнение и исходное написание | чтение SHALL возвращать пять разных значений с прежним регистром, пробелом и Unicode-представлением | `persistent-attributes-c15` | `tests/integration/persistence/test_attributes.py::test_contract[c15]` |
| Профили сравнения строковых атрибутов | Каноническое равенство без удаления пробелов | поиск SHALL находить первое значение с его исходным написанием, а значение с начальным пробелом SHALL оставаться отдельным элементом множества | `persistent-attributes-c16` | `tests/integration/persistence/test_attributes.py::test_contract[c16]` |
| Стабильность семантики используемого определения | Определение с пустым множеством | изменение SHALL быть отклонено, а семантика определения и пустой экземпляр SHALL сохраниться | `persistent-attributes-c17` | `tests/integration/persistence/test_attributes.py::test_contract[c17]` |
| Стабильность семантики используемого определения | Определение атрибута удалённого субъекта | изменение SHALL быть отклонено, а определение и сохранённый атрибут субъекта SHALL остаться прежними | `persistent-attributes-c18` | `tests/integration/persistence/test_attributes.py::test_contract[c18]` |
| Отдельное глобальное полномочие каталогов | Владелец контейнера без полномочия каталогов | операция SHALL быть отклонена без изменения каталога или применимости | `persistent-attributes-c19` | `tests/integration/persistence/test_attributes.py::test_contract[c19]` |
| Отдельное глобальное полномочие каталогов | Оператор каталогов без прав на данные контейнера | изменение SHALL быть отклонено, а данные контейнера SHALL сохраниться | `persistent-attributes-c20` | `tests/integration/persistence/test_attributes.py::test_contract[c20]` |

### 13.5. access-model/models

`openspec/changes/t-3-persistent/specs/access-model/models/spec.md`

| Requirement | Scenario | Точный критерий THEN/AND | Стабильный test ID | TamarixTests: planned pytest node ID |
| --- | --- | --- | --- | --- |
| Постоянная идентичность метаданных модели | Уникальность в держателе | регистровый дубликат первого держателя SHALL отклоняться, а модель второго держателя SHALL получать независимый ID | `persistent-models-c01` | `tests/integration/persistence/test_models.py::test_contract[c01]` |
| Постоянная идентичность метаданных модели | Границы и неизменяемость идентичности | только новые допустимые ключи длиной 1 и 512 SHALL приниматься, а остальные перечисленные операции SHALL отклоняться | `persistent-models-c02` | `tests/integration/persistence/test_models.py::test_contract[c02]` |
| Атрибуты и revision метаданных модели | Конфликт после изменения атрибутов | команда SHALL получать конфликт с сохранением текущих метаданных и атрибутов | `persistent-models-c03` | `tests/integration/persistence/test_models.py::test_contract[c03]` |
| Атрибуты и revision метаданных модели | Отказ составной записи метаданных | метаданные, атрибуты и revision SHALL оставаться в состоянии до операции | `persistent-models-c04` | `tests/integration/persistence/test_models.py::test_contract[c04]` |
| Физическое удаление метаданных модели | Удаление модели с атрибутами | метаданные и атрибуты модели SHALL отсутствовать после commit, а держатель, субъекты и объекты SHALL сохраняться | `persistent-models-c05` | `tests/integration/persistence/test_models.py::test_contract[c05]` |
| Различение метаданных и исполнимой модели | Известны только метаданные | результат SHALL явно оставаться набором метаданных и не SHALL подменять CompleteModelSet либо результаты вычисления моделей | `persistent-models-c06` | `tests/integration/persistence/test_models.py::test_contract[c06]` |

### 13.6. authorization/access-check

`openspec/changes/t-3-persistent/specs/authorization/access-check/spec.md`

| Requirement | Scenario | Точный критерий THEN/AND | Стабильный test ID | TamarixTests: planned pytest node ID |
| --- | --- | --- | --- | --- |
| Единый снимок подготовленных фактов | Конкурентный commit между чтениями | текущая сборка SHALL видеть прежнее согласованное состояние всех фактов, а новая транзакция чтения SHALL видеть зафиксированное изменение | `persistent-facts-c01` | `tests/integration/persistence/test_fact_views.py::test_contract[c01]` |
| Единый снимок подготовленных фактов | Путь и независимый субъект | сборка SHALL возвращать весь фактический путь от корня с обоими концами и предками контекста, не исключая субъект только по положению его держателя | `persistent-facts-c02` | `tests/integration/persistence/test_fact_views.py::test_contract[c02]` |
| Различение пустых и неизвестных подготовленных данных | Установленный пустой набор | результат SHALL содержать явный пустой набор метаданных этого контейнера без прерывания пути | `persistent-facts-c03` | `tests/integration/persistence/test_fact_views.py::test_contract[c03]` |
| Различение пустых и неизвестных подготовленных данных | Неизвестные путь или метаданные | результат SHALL явно обозначать неизвестную часть и не SHALL представлять сборку полной или заменять ошибку пустым набором | `persistent-facts-c04` | `tests/integration/persistence/test_fact_views.py::test_contract[c04]` |
| Доступ читателя только для чтения | Попытка записи читателем | БД SHALL отклонять запись с сохранением данных и схемы | `persistent-facts-c05` | `tests/integration/persistence/test_fact_views.py::test_contract[c05]` |

## 14. Планируемые команды и правила отчётности

Команды ниже **не выполнялись при подготовке change**. Они применяются в
будущих согласованных apply-задачах после появления исходников, pins и среды.
Каждый инициированный прогон, включая fail/error/cancel, получает новый
каталог; компоненты также сохраняют русскую summary.md и results.json с
фактическими командами, case/node IDs, версиями, временем, статусами и ошибками.
JUnit XML дополняет эти отчёты. Не начавшиеся случаи — NOT_RUN; incomplete,
нулевой набор или SKIP/XFAIL обязательного случая не считаются PASS.

Из каждого изменённого Python-репозитория:

```sh
uv lock --check
uv sync --frozen
uv run --frozen --no-sync python -m pytest tests/component -q --junitxml /absolute/path/new-component-run/junit.xml
```

Путь tests/component относится к планируемым component suites; дополнительно
выполняются фактические unit/contract paths затронутого сервиса, описанные
в группе его задач. Название успешного pytest command без обязательной
summary/JSON фиксации результата не закрывает задачу 2.5/11.2.

Из TamarixTests существующие CLI-флаги после расширения manifest validator:

```sh
.venv/bin/python -m tamarix_tests validate-registry --store ../Tamarix/tamarix-specs --change t-3-persistent
.venv/bin/python -m tamarix_tests run --store ../Tamarix/tamarix-specs --manifest /absolute/path/manifest.json --change t-3-persistent --output-dir reports --junit
.venv/bin/python -m tamarix_tests run --store ../Tamarix/tamarix-specs --manifest /absolute/path/manifest.json --id persistent-objects-c04 --level integration --output-dir reports
.venv/bin/python -m tamarix_tests promote --store ../Tamarix/tamarix-specs --change t-3-persistent --report /absolute/path/reports/run-id/results.json
```

--change включает собственные случаи и актуальный регресс; T-2 уже содержит
regression cases, поэтому bootstrap-empty-regression здесь неприменим.
--id/--level — только диагностика, не полный archive evidence. После promotion
нужны отдельный commit тестовой репы, новый manifest и повтор полного run
--change t-3-persistent для окончательного commit. Runner не поднимает БД
и не выполняет миграции: это результат внешней подготовки по задаче 1.3.

Статус OpenSpec/strict validation подтверждает planning, а не реализацию
или успешный тестовый прогон.

## Workflow follow-up

- После завершения всех tracked задач и проверки принятого foundation scope использовать существующую проектную обёртку archive с готовым полным отчётом; archive не запускает тесты неявно.
- При отсутствии/устаревании/неполноте evidence оставить change активным и необходимые задачи открытыми.
- Проверить результат синхронизации основных specs и архива отдельно; не перемещать исходники тестов и не переписывать исторические архивы T-1/T-2.
- В следующем отдельном change спроектировать внутреннее хранение моделей/привилегий/actions, атомарную очистку непустых ссылок с affected model revisions и подключение полноценного PDP ко всему согласованному snapshot.


## Результаты выполнения

- 2026-10-15, 1.1: [design-review.md](design-review.md) фиксирует независимый технический review и baseline исполнения; источник разрешения — вызов apply и последующее указание продолжить. Код и тесты этим review не подтверждаются.
- Устранён цикл 2.3/2.4 -> 2.5: reporting protocol выполняется до первого прогона, без изменения критериев. Основание — раздел Review порядка reporting tasks в design-review.md.
- 1.2: [storage-contracts.md](storage-contracts.md) фиксирует локальные ID/адреса/команды, исходную revision, no-op, safe outcomes и rollout пяти пакетов.
- 1.3–1.5: [dependency-baseline.md](dependency-baseline.md) содержит официальный stable baseline, frozen install, фактический PostgreSQL/image/Unicode и внешний локальный CD change; [design-review.md](design-review.md) сохраняет сверку foundation/будущего change. ADR/context не изменены.
- 2.1: в db-control, пяти сервисах и TamarixTests прошли `uv lock --check` и `uv sync --frozen` с uv 0.12.24; Python 3.15.0, SQLAlchemy 2.1.4, Psycopg 3.3.6 binary, Alembic 1.20.0 только у владельца миграций. Установка не обновляла locks.
- 2.5: локальные `tools/run_tests.py` в семи репозиториях и существующий integration runner сохраняют отдельные summary/JSON/log/JUnit до collection. Самопроверки исходов PASS/FAIL/collection error/CANCELLED прошли: [4 PASS](../../../../db-control/reports/b2fa306d25a3415b9a85e83885efa53a/summary.md). Отмена сохраняет NOT_RUN/complete=false. Никаких новых commit/start/archive triggers.
- 2.2–2.3: db-control поставляет baseline и Alembic CLI с UTF8/block-size/unknown-schema preflight и закрытым runtime DML/PUBLIC EXECUTE. Команда wrapper `tests/component/test_migrations.py -q --tb=short` на отдельных PostgreSQL БД: [11 PASS](../../../../db-control/reports/9fac3af90b25460bbc26f82cd95f154a/summary.md), включая повторный upgrade и downgrade/upgrade, сохранение неизвестной схемы и 6 настоящих LOGIN ролей. Production forward-fix/backup граница — README db-control.
- Промежуточные проверки (не итоговый integration evidence): db-control primitives [93 PASS](../../../../db-control/reports/25e087ccba9345d5a7aaaeb38f8e7c15/summary.md); пять существующих сервисных наборов после typed-address перехода — 466 PASS. DN component [88 PASS](../../../../db-control/reports/component/c3ce7f52b1c14421b6173afd64dfe6e8/summary.md). Функциональные/race/registry/promotion задачи остаются открытыми до своих проверок.
