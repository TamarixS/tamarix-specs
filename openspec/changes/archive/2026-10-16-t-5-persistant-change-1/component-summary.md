# Component-проверки db-control

Прогон: b8125d735c354768a9cb500e397e8b7c. Итог: **PASS**.
Начало: 2026-10-16T13:11:03.291759+00:00. Конец: 2026-10-16T13:11:29.909935+00:00.
Длительность: 26.619 с. Python: 3.15.0.

Версии: {'db-control': '0.1.0', 'SQLAlchemy': '2.1.4', 'psycopg': '3.3.6', 'psycopg-binary': '3.3.6', 'alembic': '1.20.0', 'pytest': '9.1.1'}.

Запрошено: tests/component, -q.
Собрано: 206. Статусы: {'PASS': 206}.

- tests/component/test_attribute_equality.py::test_native_set_equality_is_exact_and_not_hash_unique[integer]: PASS. Нативное равенство DB определяет set uniqueness; каждый параметр описывает свой тип.

Проверка использует direct writes и настоящий instance MVCC guard. Различное
текстовое представление одного NUMERIC/instant не создаёт второй элемент.
- tests/component/test_attribute_equality.py::test_native_set_equality_is_exact_and_not_hash_unique[decimal-scale]: PASS. Нативное равенство DB определяет set uniqueness; каждый параметр описывает свой тип.

Проверка использует direct writes и настоящий instance MVCC guard. Различное
текстовое представление одного NUMERIC/instant не создаёт второй элемент.
- tests/component/test_attribute_equality.py::test_native_set_equality_is_exact_and_not_hash_unique[boolean]: PASS. Нативное равенство DB определяет set uniqueness; каждый параметр описывает свой тип.

Проверка использует direct writes и настоящий instance MVCC guard. Различное
текстовое представление одного NUMERIC/instant не создаёт второй элемент.
- tests/component/test_attribute_equality.py::test_native_set_equality_is_exact_and_not_hash_unique[date]: PASS. Нативное равенство DB определяет set uniqueness; каждый параметр описывает свой тип.

Проверка использует direct writes и настоящий instance MVCC guard. Различное
текстовое представление одного NUMERIC/instant не создаёт второй элемент.
- tests/component/test_attribute_equality.py::test_native_set_equality_is_exact_and_not_hash_unique[instant-offset]: PASS. Нативное равенство DB определяет set uniqueness; каждый параметр описывает свой тип.

Проверка использует direct writes и настоящий instance MVCC guard. Различное
текстовое представление одного NUMERIC/instant не создаёт второй элемент.
- tests/component/test_attribute_equality.py::test_native_set_equality_is_exact_and_not_hash_unique[large-decimal]: PASS. Нативное равенство DB определяет set uniqueness; каждый параметр описывает свой тип.

Проверка использует direct writes и настоящий instance MVCC guard. Различное
текстовое представление одного NUMERIC/instant не создаёт второй элемент.
- tests/component/test_attribute_equality.py::test_string_set_profiles_preserve_declared_equality[exact-canonical]: PASS. String set использует profile закреплённого shape и сохраняет оригиналы, смысл в параметре.

Длинные строки и Unicode CI проверяются через DB guard, без Python lower/hash.
Значимое различие допускает два элемента, эквивалентность возвращает duplicate.
- tests/component/test_attribute_equality.py::test_string_set_profiles_preserve_declared_equality[exact-case]: PASS. String set использует profile закреплённого shape и сохраняет оригиналы, смысл в параметре.

Длинные строки и Unicode CI проверяются через DB guard, без Python lower/hash.
Значимое различие допускает два элемента, эквивалентность возвращает duplicate.
- tests/component/test_attribute_equality.py::test_string_set_profiles_preserve_declared_equality[d145-expansion]: PASS. String set использует profile закреплённого shape и сохраняет оригиналы, смысл в параметре.

Длинные строки и Unicode CI проверяются через DB guard, без Python lower/hash.
Значимое различие допускает два элемента, эквивалентность возвращает duplicate.
- tests/component/test_attribute_equality.py::test_string_set_profiles_preserve_declared_equality[d145-canonical]: PASS. String set использует profile закреплённого shape и сохраняет оригиналы, смысл в параметре.

Длинные строки и Unicode CI проверяются через DB guard, без Python lower/hash.
Значимое различие допускает два элемента, эквивалентность возвращает duplicate.
- tests/component/test_attribute_equality.py::test_string_set_profiles_preserve_declared_equality[d145-spaces]: PASS. String set использует profile закреплённого shape и сохраняет оригиналы, смысл в параметре.

Длинные строки и Unicode CI проверяются через DB guard, без Python lower/hash.
Значимое различие допускает два элемента, эквивалентность возвращает duplicate.
- tests/component/test_attribute_equality.py::test_string_set_profiles_preserve_declared_equality[d145-not-nfkc]: PASS. String set использует profile закреплённого shape и сохраняет оригиналы, смысл в параметре.

Длинные строки и Unicode CI проверяются через DB guard, без Python lower/hash.
Значимое различие допускает два элемента, эквивалентность возвращает duplicate.
- tests/component/test_attribute_equality.py::test_string_set_profiles_preserve_declared_equality[long-text]: PASS. String set использует profile закреплённого shape и сохраняет оригиналы, смысл в параметре.

Длинные строки и Unicode CI проверяются через DB guard, без Python lower/hash.
Значимое различие допускает два элемента, эквивалентность возвращает duplicate.
- tests/component/test_attribute_equality.py::test_set_duplicate_prevention_with_old_concurrent_snapshot[read-committed]: PASS. Set guard сериализует независимых writers реальным instance UPDATE, не SELECT FOR UPDATE.

Оба snapshot открыты до первой вставки. Эквивалентные D145 значения не могут
стать двумя элементами: RC видит duplicate, RR/SERIALIZABLE отклоняют старый
snapshot. После конфликтующей transaction в БД остаётся ровно один оригинал.
- tests/component/test_attribute_equality.py::test_set_duplicate_prevention_with_old_concurrent_snapshot[repeatable-read]: PASS. Set guard сериализует независимых writers реальным instance UPDATE, не SELECT FOR UPDATE.

Оба snapshot открыты до первой вставки. Эквивалентные D145 значения не могут
стать двумя элементами: RC видит duplicate, RR/SERIALIZABLE отклоняют старый
snapshot. После конфликтующей transaction в БД остаётся ровно один оригинал.
- tests/component/test_attribute_equality.py::test_set_duplicate_prevention_with_old_concurrent_snapshot[serializable]: PASS. Set guard сериализует независимых writers реальным instance UPDATE, не SELECT FOR UPDATE.

Оба snapshot открыты до первой вставки. Эквивалентные D145 значения не могут
стать двумя элементами: RC видит duplicate, RR/SERIALIZABLE отклоняют старый
snapshot. После конфликтующей transaction в БД остаётся ровно один оригинал.
- tests/component/test_attribute_shapes.py::test_shape_registration_contracts_and_keys: PASS. Регистрация принимает все допустимые tuples и ASCII keys, отвергает неверные без следа.

Проверяются string exact/unicode_ci single/set, DN set и пять native типов
single/set; null/пустой/513/кириллический key, конфликт ASCII регистра,
неверный профиль/кратность и отсутствующая/неизвестная версия отклоняются.
Это защищает именно вход каталога, не подменяя DB immutable/FK проверки.
- tests/component/test_attribute_shapes.py::test_unused_shape_whole_row_immutability: PASS. Неиспользуемый shape защищён в БД при изменении каждого поля, включая identity/key.

Семантические UPDATE предлагают согласованные tuples, поэтому отказ нельзя
объяснить только CHECK допустимости профиля. Исходная строка сохраняется.
- tests/component/test_attribute_shapes.py::test_shared_shape_whole_row_immutability: PASS. Shape двух definitions с values нельзя изменить; все ссылки и значения сохраняются.

Отказ каждого UPDATE проверяется deployment connection, имеющей прямой DML:
закрытые runtime grants сами по себе не доказывают immutable trigger.
- tests/component/test_attribute_shapes.py::test_instance_shape_composite_fks_all_owner_families: PASS. Каждое семейство отвергает чужой shape и неверные type/cardinality именно составным FK.

Альтернативный shape имеет те же параметры: это доказывает фиксацию точного
shape_id definition независимо от равенства semantic tuple.
- tests/component/test_attribute_shapes.py::test_instance_required_shape_references_all_owner_families: PASS. Null и неизвестные definition/shape, null type/cardinality не оставляют partial instance.

Все четыре семейства получают реальные owner/applicability; тем самым отказ
относится к обязательным structural ссылкам, а не к отсутствующему владельцу.
- tests/component/test_attribute_shapes.py::test_value_fk_and_check_all_owner_families: PASS. Values всех семейств сохраняют FK/type/cardinality/one-column CHECK и прежние данные.

Неизвестный instance, чужой тип или кратность и две заполненные колонки
отвергаются; откат также сохраняет mutation_version исходного instance.
- tests/component/test_attribute_shapes.py::test_instance_identity_and_assignment_uniqueness_all_owner_families: PASS. Пара owner–definition уникальна; owner/definition/shape/type/cardinality instance неизменяемы.

Все четыре families проверяются прямым UPDATE под deployment правами;
отказы guard сохраняют исходный экземпляр и его value, не перемещая данные.
- tests/component/test_attribute_shapes.py::test_scalar_cardinality_all_owner_families: PASS. Во всех families single запрещает вторую строку сразу и пустоту при commit.

После каждого отказа исходное значение 7 сохранено; проверка выполняется
непосредственной записью values и не зависит от ранней валидации команды.
- tests/component/test_attribute_shapes.py::test_instance_delete_cascades_values_preserving_shared_shape: PASS. Удаление instance каскадно очищает только его values, сохраняя общий shape и соседей.

По две definitions с одной формой используются в каждом семействе; удаление
первой не должно удалять вторую definition, её instance, value или форму.
- tests/component/test_attribute_shapes.py::test_shape_is_only_physical_comparison_source: PASS. Comparator metadata физически находится только в shapes, старые facts возвращают его JOIN.

Во всех families создаются реальные string values; проверяются отсутствие
физических comparator columns и совпадение опубликованной tuple с shape.
- tests/component/test_attribute_shapes.py::test_legacy_catalog_wrappers: PASS. Прежние positional/named signatures сохраняют версию, no-op и атомарность без orphan shapes.

Равная tuple использованного definition не создаёт форму; другая tuple
отклоняется целиком. Дубликат key не оставляет форму, equal definitions не
deduplicate, а заранее занятый generated key обрабатывается без коллизии.
- tests/component/test_attribute_shapes.py::test_dn_applicability_and_bind_share_definition_lock: PASS. Обе очередности DN bind и расширения applicability не дают noncontainer DN definition.

Два независимых SERIALIZABLE snapshot открыты заранее; loser получает
serialization/constraint отказ, а итоговая shape/applicability пара допустима.
- tests/component/test_attribute_shapes.py::test_instance_create_and_bind_keep_exact_shape_under_both_orders: PASS. Создание empty set и bind обоих порядков не коммитят instance с прежней чужой формой.

Старые snapshot воспроизводятся Barrier/Event без sleep; проверяется точный
конечный shape_id и отсутствие partial instance после проигравшей записи.
- tests/component/test_attributes_schema.py::test_attribute_owner_fk_applicability_and_empty_set[container]: PASS. Все четыре owner families требуют applicability/FK и различают absence и empty set.

Каждый параметр задаёт настоящую предметную таблицу владельца. Ни instance
несуществующего owner, ни незарегистрированная применимость не принимаются;
разрешённый set instance без values коммитится и наблюдается как empty.
- tests/component/test_attributes_schema.py::test_attribute_owner_fk_applicability_and_empty_set[subject]: PASS. Все четыре owner families требуют applicability/FK и различают absence и empty set.

Каждый параметр задаёт настоящую предметную таблицу владельца. Ни instance
несуществующего owner, ни незарегистрированная применимость не принимаются;
разрешённый set instance без values коммитится и наблюдается как empty.
- tests/component/test_attributes_schema.py::test_attribute_owner_fk_applicability_and_empty_set[object]: PASS. Все четыре owner families требуют applicability/FK и различают absence и empty set.

Каждый параметр задаёт настоящую предметную таблицу владельца. Ни instance
несуществующего owner, ни незарегистрированная применимость не принимаются;
разрешённый set instance без values коммитится и наблюдается как empty.
- tests/component/test_attributes_schema.py::test_attribute_owner_fk_applicability_and_empty_set[model]: PASS. Все четыре owner families требуют applicability/FK и различают absence и empty set.

Каждый параметр задаёт настоящую предметную таблицу владельца. Ни instance
несуществующего owner, ни незарегистрированная применимость не принимаются;
разрешённый set instance без values коммитится и наблюдается как empty.
- tests/component/test_attributes_schema.py::test_scalar_exactly_one_is_deferred_and_instance_delete_cascades[container]: PASS. Scalar может временно быть пустым в transaction, но на commit содержит ровно одно value.

Во всех owner families пустой scalar commit отклоняется; замена delete+insert
допустима внутри одной transaction. Удаление самого instance с values допустимо
и не заставляет deferred trigger требовать value уже удалённого экземпляра.
- tests/component/test_attributes_schema.py::test_scalar_exactly_one_is_deferred_and_instance_delete_cascades[subject]: PASS. Scalar может временно быть пустым в transaction, но на commit содержит ровно одно value.

Во всех owner families пустой scalar commit отклоняется; замена delete+insert
допустима внутри одной transaction. Удаление самого instance с values допустимо
и не заставляет deferred trigger требовать value уже удалённого экземпляра.
- tests/component/test_attributes_schema.py::test_scalar_exactly_one_is_deferred_and_instance_delete_cascades[object]: PASS. Scalar может временно быть пустым в transaction, но на commit содержит ровно одно value.

Во всех owner families пустой scalar commit отклоняется; замена delete+insert
допустима внутри одной transaction. Удаление самого instance с values допустимо
и не заставляет deferred trigger требовать value уже удалённого экземпляра.
- tests/component/test_attributes_schema.py::test_scalar_exactly_one_is_deferred_and_instance_delete_cascades[model]: PASS. Scalar может временно быть пустым в transaction, но на commit содержит ровно одно value.

Во всех owner families пустой scalar commit отклоняется; замена delete+insert
допустима внутри одной transaction. Удаление самого instance с values допустимо
и не заставляет deferred trigger требовать value уже удалённого экземпляра.
- tests/component/test_attributes_schema.py::test_attribute_type_null_profile_and_used_semantics_cannot_be_changed: PASS. Explicit null/type mismatch отвергаются; empty instance удерживает shape и applicability.

NOT NULL shape_id не позволяет обойти composite FK через MATCH SIMPLE.
Используемое определение, включая пустой set, нельзя изменить или лишить
применимости; после удаления instance новая семантика доступна только явно.
- tests/component/test_attributes_schema.py::test_protected_attribute_command_roundtrip_and_aggregate_revision[container]: PASS. Все предметные wrappers применяют scalar composite input атомарно и держат общий CAS.

Первый put создаёт instance/value и revision2; повтор того же put — no-op.
Новое scalar значение заменяет прежнее без промежуточного commit и даёт
revision3. Проверяются реальные dynamic SQL/composite casts каждой owner family.
- tests/component/test_attributes_schema.py::test_protected_attribute_command_roundtrip_and_aggregate_revision[subject]: PASS. Все предметные wrappers применяют scalar composite input атомарно и держат общий CAS.

Первый put создаёт instance/value и revision2; повтор того же put — no-op.
Новое scalar значение заменяет прежнее без промежуточного commit и даёт
revision3. Проверяются реальные dynamic SQL/composite casts каждой owner family.
- tests/component/test_attributes_schema.py::test_protected_attribute_command_roundtrip_and_aggregate_revision[object]: PASS. Все предметные wrappers применяют scalar composite input атомарно и держат общий CAS.

Первый put создаёт instance/value и revision2; повтор того же put — no-op.
Новое scalar значение заменяет прежнее без промежуточного commit и даёт
revision3. Проверяются реальные dynamic SQL/composite casts каждой owner family.
- tests/component/test_attributes_schema.py::test_protected_attribute_command_roundtrip_and_aggregate_revision[model]: PASS. Все предметные wrappers применяют scalar composite input атомарно и держат общий CAS.

Первый put создаёт instance/value и revision2; повтор того же put — no-op.
Новое scalar значение заменяет прежнее без промежуточного commit и даёт
revision3. Проверяются реальные dynamic SQL/composite casts каждой owner family.
- tests/component/test_bootstrap.py::test_deployment_executor_can_provision_root_without_dn: PASS. Привилегированный executor создаёт root без DN в SERIALIZABLE transaction.

Ожидаются стабильный ID, исходная revision1 и отсутствие DN instances;
проверка сохраняет допустимость контейнера без доступа от его имени.
- tests/component/test_bootstrap.py::test_initial_root_and_trusted_dn_commit_as_one_aggregate: PASS. Зарегистрированный trusted DER Name provision вместе с initial root атомарно.

Нативные composite arrays создают container attribute с одним DN value;
comparison key вычисляет DB codec, отдельного DN registry не возникает.
- tests/component/test_bootstrap.py::test_invalid_dn_rolls_back_root_and_preceding_attribute_changes: PASS. Ошибка последнего DN откатывает root и ранее созданные integer instances/values.

Каталоговые определения из предыдущей transaction сохраняются; ни owner row,
ни часть aggregate attributes не должны остаться после codec failure.
- tests/component/test_bootstrap.py::test_catalog_and_runtime_logins_cannot_provision_initial_root[container]: PASS. Каждый настоящий LOGIN получает отказ EXECUTE deployment bootstrap без SET ROLE.

Каталоговый оператор сначала регистрирует DN definition и применимость, но
это не даёт ему provisioning; роли и ожидаемые границы описаны параметрами.
- tests/component/test_bootstrap.py::test_catalog_and_runtime_logins_cannot_provision_initial_root[subject]: PASS. Каждый настоящий LOGIN получает отказ EXECUTE deployment bootstrap без SET ROLE.

Каталоговый оператор сначала регистрирует DN definition и применимость, но
это не даёт ему provisioning; роли и ожидаемые границы описаны параметрами.
- tests/component/test_bootstrap.py::test_catalog_and_runtime_logins_cannot_provision_initial_root[object]: PASS. Каждый настоящий LOGIN получает отказ EXECUTE deployment bootstrap без SET ROLE.

Каталоговый оператор сначала регистрирует DN definition и применимость, но
это не даёт ему provisioning; роли и ожидаемые границы описаны параметрами.
- tests/component/test_bootstrap.py::test_catalog_and_runtime_logins_cannot_provision_initial_root[model]: PASS. Каждый настоящий LOGIN получает отказ EXECUTE deployment bootstrap без SET ROLE.

Каталоговый оператор сначала регистрирует DN definition и применимость, но
это не даёт ему provisioning; роли и ожидаемые границы описаны параметрами.
- tests/component/test_bootstrap.py::test_catalog_and_runtime_logins_cannot_provision_initial_root[catalog]: PASS. Каждый настоящий LOGIN получает отказ EXECUTE deployment bootstrap без SET ROLE.

Каталоговый оператор сначала регистрирует DN definition и применимость, но
это не даёт ему provisioning; роли и ожидаемые границы описаны параметрами.
- tests/component/test_bootstrap.py::test_catalog_and_runtime_logins_cannot_provision_initial_root[reader]: PASS. Каждый настоящий LOGIN получает отказ EXECUTE deployment bootstrap без SET ROLE.

Каталоговый оператор сначала регистрирует DN definition и применимость, но
это не даёт ему provisioning; роли и ожидаемые границы описаны параметрами.
- tests/component/test_bootstrap.py::test_container_runtime_cannot_convert_create_child_to_root_creation: PASS. Container LOGIN не создаёт root через NULL parent разрешённого child routine.

Ожидается явный отказ без owner rows; проверка исключает обход закрытого
provisioning через существующий runtime SQL command, без HTTP обещаний.
- tests/component/test_containers.py::test_forest_typed_case_insensitive_uniqueness_and_root_scope: PASS. Корни уникальны по type/key CI, дети по parent/type/key CI; разные деревья независимы.

Один root key допускается у другого типа, один child key — у другого holder
или типа. Пропуск уровней разрешён, но case-only duplicate в том же scope нет.
- tests/component/test_containers.py::test_parent_type_rank_is_strict[inverted-rank]: PASS. Нарушение строгого parent rank отклоняется самой БД; причина дана в параметре.

Это исключает циклы/повтор типа при создании и делает typed object path
однозначным независимо от application валидации.
- tests/component/test_containers.py::test_parent_type_rank_is_strict[equal-rank]: PASS. Нарушение строгого parent rank отклоняется самой БД; причина дана в параметре.

Это исключает циклы/повтор типа при создании и делает typed object path
однозначным независимо от application валидации.
- tests/component/test_containers.py::test_parent_type_rank_is_strict[module-parent]: PASS. Нарушение строгого parent rank отклоняется самой БД; причина дана в параметре.

Это исключает циклы/повтор типа при создании и делает typed object path
однозначным независимо от application валидации.
- tests/component/test_containers.py::test_lifecycle_active_guards_child_first_purge_and_technical_cleanup: PASS. Container hard delete требует child-first и удалённых entities; tombstones/attrs/guards очищаются.

Активный subject не может быть физически удалён даже deployment записью.
После soft delete его retained attrs purge вместе с holder; удаление модели
и объекта чистит только собственные attrs, технический key guard не блокирует
пустой holder и не сохраняет осиротевшие строки.
- tests/component/test_containers.py::test_aggregate_cas_noop_case_rename_and_full_rollback: PASS. Container CAS охватывает attrs и key: no-op сохраняет revision, ошибка откатывает весь command.

Case-only rename сохраняет ID и меняет оригинал/revision. Stale expected token
не перезаписывает новую версию. При валидной первой attribute change и ошибке
второй change не остаётся ни нового instance, ни revision/key мутации.
- tests/component/test_containers.py::test_protected_commands_require_serializable: PASS. Защищённый command отвергает READ COMMITTED до мутации; это не совет adapter.

Проверка фиксирует DB boundary для административной transaction: приложение
обязано запускать полную проверку/command в принятом SERIALIZABLE режиме.
- tests/component/test_containers.py::test_container_identity_is_immutable_in_database[container-parent]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_containers.py::test_container_identity_is_immutable_in_database[container-type]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_containers.py::test_container_identity_is_immutable_in_database[container-id]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_containers.py::test_container_key_contracts_cannot_be_bypassed[container-empty]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.
- tests/component/test_containers.py::test_container_key_contracts_cannot_be_bypassed[container-length]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.
- tests/component/test_containers.py::test_container_key_contracts_cannot_be_bypassed[container-ascii]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.
- tests/component/test_database_roles.py::test_each_native_login_cannot_execute_ddl_truncate_or_broad_dml[container]: PASS. Каждый LOGIN с единственным членством получает отказ DDL/TRUNCATE/прямой DML.

Параметры описывают шесть ролей. Обход через SET ROLE не используется;
собственный test session не должен создавать даже временную таблицу.
- tests/component/test_database_roles.py::test_each_native_login_cannot_execute_ddl_truncate_or_broad_dml[subject]: PASS. Каждый LOGIN с единственным членством получает отказ DDL/TRUNCATE/прямой DML.

Параметры описывают шесть ролей. Обход через SET ROLE не используется;
собственный test session не должен создавать даже временную таблицу.
- tests/component/test_database_roles.py::test_each_native_login_cannot_execute_ddl_truncate_or_broad_dml[object]: PASS. Каждый LOGIN с единственным членством получает отказ DDL/TRUNCATE/прямой DML.

Параметры описывают шесть ролей. Обход через SET ROLE не используется;
собственный test session не должен создавать даже временную таблицу.
- tests/component/test_database_roles.py::test_each_native_login_cannot_execute_ddl_truncate_or_broad_dml[model]: PASS. Каждый LOGIN с единственным членством получает отказ DDL/TRUNCATE/прямой DML.

Параметры описывают шесть ролей. Обход через SET ROLE не используется;
собственный test session не должен создавать даже временную таблицу.
- tests/component/test_database_roles.py::test_each_native_login_cannot_execute_ddl_truncate_or_broad_dml[catalog]: PASS. Каждый LOGIN с единственным членством получает отказ DDL/TRUNCATE/прямой DML.

Параметры описывают шесть ролей. Обход через SET ROLE не используется;
собственный test session не должен создавать даже временную таблицу.
- tests/component/test_database_roles.py::test_each_native_login_cannot_execute_ddl_truncate_or_broad_dml[reader]: PASS. Каждый LOGIN с единственным членством получает отказ DDL/TRUNCATE/прямой DML.

Параметры описывают шесть ролей. Обход через SET ROLE не используется;
собственный test session не должен создавать даже временную таблицу.
- tests/component/test_database_roles.py::test_execute_allowlist_closes_internal_mutators_and_exposes_safe_readonly_codecs[container]: PASS. Вся доступная EXECUTE поверхность совпадает с явным allowlist выбранной роли.

Неизвестные helpers/overloads и generic mutators запрещены. Четыре read-only
исключения ASCII/digest/string/DN codec проверяются действительным вызовом.
- tests/component/test_database_roles.py::test_execute_allowlist_closes_internal_mutators_and_exposes_safe_readonly_codecs[subject]: PASS. Вся доступная EXECUTE поверхность совпадает с явным allowlist выбранной роли.

Неизвестные helpers/overloads и generic mutators запрещены. Четыре read-only
исключения ASCII/digest/string/DN codec проверяются действительным вызовом.
- tests/component/test_database_roles.py::test_execute_allowlist_closes_internal_mutators_and_exposes_safe_readonly_codecs[object]: PASS. Вся доступная EXECUTE поверхность совпадает с явным allowlist выбранной роли.

Неизвестные helpers/overloads и generic mutators запрещены. Четыре read-only
исключения ASCII/digest/string/DN codec проверяются действительным вызовом.
- tests/component/test_database_roles.py::test_execute_allowlist_closes_internal_mutators_and_exposes_safe_readonly_codecs[model]: PASS. Вся доступная EXECUTE поверхность совпадает с явным allowlist выбранной роли.

Неизвестные helpers/overloads и generic mutators запрещены. Четыре read-only
исключения ASCII/digest/string/DN codec проверяются действительным вызовом.
- tests/component/test_database_roles.py::test_execute_allowlist_closes_internal_mutators_and_exposes_safe_readonly_codecs[catalog]: PASS. Вся доступная EXECUTE поверхность совпадает с явным allowlist выбранной роли.

Неизвестные helpers/overloads и generic mutators запрещены. Четыре read-only
исключения ASCII/digest/string/DN codec проверяются действительным вызовом.
- tests/component/test_database_roles.py::test_execute_allowlist_closes_internal_mutators_and_exposes_safe_readonly_codecs[reader]: PASS. Вся доступная EXECUTE поверхность совпадает с явным allowlist выбранной роли.

Неизвестные helpers/overloads и generic mutators запрещены. Четыре read-only
исключения ASCII/digest/string/DN codec проверяются действительным вызовом.
- tests/component/test_database_roles.py::test_public_execute_is_closed_and_all_definers_have_private_owner_and_fixed_path: PASS. PUBLIC не исполняет предметные функции, каждый SECURITY DEFINER защищён owner/path.

Проверяются все функции мигрированной схемы, включая DN codec после0003;
NOLOGIN owner и pg_catalog path исключают подмену через пользовательскую schema.
- tests/component/test_database_roles.py::test_catalog_operator_cannot_change_entity_attributes: PASS. Оператор регистрирует общий attribute, но не меняет данные контейнера через SQL обход.

Отказ narrow container command и generic helper оставляет integer value и
owner revision прежними; глобальные catalog rights не означают владение данными.
- tests/component/test_database_roles.py::test_reader_views_keep_model_metadata_when_only_subject_is_tombstoned: PASS. Reader видит model metadata и attrs при единственном tombstone субъекте держателя.

Active subject/attribute views пусты, retained rows скрыты и недоступны напрямую;
metadata не превращается в empty из-за lifecycle чужой сущности.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[utf8-printable]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[utf8-bmp]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[utf8-universal]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[t61-accent]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[t61-legacy-umlaut]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[historical-casefold]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[canonical-composition]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[compatibility-composition]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[combining-order]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[hangul]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[mapped-to-nothing]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[nul-before-text]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[insignificant-spaces]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[all-spaces]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[unicode32-correction]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[bidi-ignored]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[unknown-oid-string]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[domain-component]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[empty-name]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[rdn-ava-order]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_equivalent_vectors[opaque-der]: PASS. Эквивалентные Name дают одинаковый DB key; русский смысл каждого вектора в параметре.

Проверка нужна при поддержке разных ASN.1 encodings и исторических Unicode
правил: строки нельзя сравнивать как произвольный RFC4514 текст или raw DER.
- tests/component/test_dn_codec.py::test_dn_matching_preserves_significant_distinctions[rdn-order]: PASS. Значимые различия Name сохраняют разные keys; каждый параметр поясняет инвариант.

Проверка предотвращает ложное совпадение сертификатного DN и зарегистрированного
значения из-за потери порядка, OID, кратности либо иной версии Unicode.
- tests/component/test_dn_codec.py::test_dn_matching_preserves_significant_distinctions[ava-multiplicity]: PASS. Значимые различия Name сохраняют разные keys; каждый параметр поясняет инвариант.

Проверка предотвращает ложное совпадение сертификатного DN и зарегистрированного
значения из-за потери порядка, OID, кратности либо иной версии Unicode.
- tests/component/test_dn_codec.py::test_dn_matching_preserves_significant_distinctions[attribute-oid]: PASS. Значимые различия Name сохраняют разные keys; каждый параметр поясняет инвариант.

Проверка предотвращает ложное совпадение сертификатного DN и зарегистрированного
значения из-за потери порядка, OID, кратности либо иной версии Unicode.
- tests/component/test_dn_codec.py::test_dn_matching_preserves_significant_distinctions[space-before-mark]: PASS. Значимые различия Name сохраняют разные keys; каждый параметр поясняет инвариант.

Проверка предотвращает ложное совпадение сертификатного DN и зарегистрированного
значения из-за потери порядка, OID, кратности либо иной версии Unicode.
- tests/component/test_dn_codec.py::test_dn_matching_preserves_significant_distinctions[modern-correction-differs]: PASS. Значимые различия Name сохраняют разные keys; каждый параметр поясняет инвариант.

Проверка предотвращает ложное совпадение сертификатного DN и зарегистрированного
значения из-за потери порядка, OID, кратности либо иной версии Unicode.
- tests/component/test_dn_codec.py::test_dn_matching_preserves_significant_distinctions[domain-space]: PASS. Значимые различия Name сохраняют разные keys; каждый параметр поясняет инвариант.

Проверка предотвращает ложное совпадение сертификатного DN и зарегистрированного
значения из-за потери порядка, OID, кратности либо иной версии Unicode.
- tests/component/test_dn_codec.py::test_dn_matching_preserves_significant_distinctions[opaque-case]: PASS. Значимые различия Name сохраняют разные keys; каждый параметр поясняет инвариант.

Проверка предотвращает ложное совпадение сертификатного DN и зарегистрированного
значения из-за потери порядка, OID, кратности либо иной версии Unicode.
- tests/component/test_dn_codec.py::test_dn_matching_preserves_significant_distinctions[opaque-versus-string]: PASS. Значимые различия Name сохраняют разные keys; каждый параметр поясняет инвариант.

Проверка предотвращает ложное совпадение сертификатного DN и зарегистрированного
значения из-за потери порядка, OID, кратности либо иной версии Unicode.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[empty-designation]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ir87-g0]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ir87-locking]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ir87-right-half]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ss2-escape]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ss2-control]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ss3-escape]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ss3-control]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ls2]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ls3]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ls2r]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[ls3r]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[csi-sgr-eight-bit]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[csi-sgr-seven-bit]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[csi-presentation]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[underline]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[mapped-controls]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[mapped-control-spaces]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_t61_stateful_transcode_vectors[control-designations]: PASS. Объявленные T61 состояния дают ожидаемый plain текст; случай описан по-русски.

Сопоставляется публичный DN key с UTF8, поэтому ISO2022 команды, CSI параметры
и presentation markers не могут незаметно попасть в результат как символы.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[empty-input]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[indefinite-length]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[nonminimal-length]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[trailing-data]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[empty-rdn]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[unsorted-set]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[nonminimal-oid]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[truncated-oid]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[extra-ava-field]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[utf8-overlong]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[utf8-surrogate]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[utf8-out-of-range]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[utf8-truncated]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[printable-alphabet]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[bmp-truncated]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[bmp-surrogate]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[universal-truncated]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[universal-out-of-range]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[private-use-prohibited]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[unicode32-unassigned]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[replacement-prohibited]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[domain-tag]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[domain-ia5]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[opaque-integer]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[opaque-boolean]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[opaque-bitstring]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-truncated-escape]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-pending-accent]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-double-accent]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-undefined-octet]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-pending-single-shift]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-undesignated]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-truncated-jis]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-mixed-jis-half]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-truncated-csi]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-invalid-csi]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_rejects_malformed_or_unpreparable_values[t61-unsupported-set]: PASS. Повреждённый DER/encoding/preparation отвергается указанным SQLSTATE, без DER fallback.

Каждый параметр задаёт русское объяснение конкретной ошибки. Такие отказы
отличают некорректный сертификатный Name от корректного несовпадающего DN.
- tests/component/test_dn_codec.py::test_dn_version_and_private_helpers_are_enforced: PASS. Real fact reader вычисляет DN key через SECURITY DEFINER, без доступа к таблицам/helper.

Неподдерживаемая версия отвергается, owner/search_path закреплены. SELECT ранее
поставленных views сохраняется после 0003; runtime не может подменить Unicode
таблицы или обойти единственный публичный codec entry point.
- tests/component/test_dn_codec.py::test_dn_attribute_derivation_duplicate_guard_and_original_retention: PASS. Прямая DN value запись получает DB key; эквивалентный DER не создаёт второй set элемент.

Исходный DER сохраняется, поддельный client key игнорируется. Неподдерживаемый
DN rollback не оставляет value; один DN разрешено хранить в разных контейнерах.
Проверка относится к настоящим constraints/triggers, а не Python comparator.
- tests/component/test_dn_codec.py::test_dn_disposable_downgrade_removes_data_and_closes_placeholder: PASS. Разрешённый disposable rollback 0003 удаляет DN данные и возвращает закрытый placeholder.

Остальные 0002 views сохраняются; повторный upgrade вновь устанавливает codec
и позволяет сравнивать DN. Используется своя БД, чтобы не менять vectors fixture.
- tests/component/test_migrations.py::test_upgrade_empty_disposable_database: PASS. На пустой отдельной БД upgrade создаёт основу, stable BIGINT ID и закрытые ACL.

Проверка применяется к первой поставке: migration head, все предметные
схемы/owner pairs и генерация идентичности должны существовать в настоящем
PostgreSQL. Metadata модели не должна получать payload или reference columns.
- tests/component/test_migrations.py::test_repeated_upgrade_head_preserves_existing_rows: PASS. Повторный upgrade head не создаёт схемы заново и сохраняет существующий root.

При уже применённой revision повторная deployment-команда должна оставаться
безопасной: OID таблицы, ID/данные строки и единственный Alembic head прежние.
- tests/component/test_migrations.py::test_disposable_downgrade_and_upgrade_restore_closed_rights: PASS. Явный downgrade удаляет только foundation схемы; upgrade восстанавливает закрытые права.

Проверка разрешена только для собственной одноразовой БД. Повторная поставка
не должна открывать PUBLIC EXECUTE, runtime DML или менять NOLOGIN group roles.
Сохранение cluster roles позволяет не затронуть другую тестовую БД.
- tests/component/test_migrations.py::test_unknown_schema_is_rejected_without_losing_user_data: PASS. Неизвестная пользовательская таблица блокирует baseline без потери её строки.

Случай защищает от случайной инициализации занятой БД: миграция должна
откатиться до создания предметных схем и не удалять чужие данные.
- tests/component/test_migrations.py::test_real_runtime_login_cannot_execute_ddl_or_broad_dml[tamarix_catalog_operator]: PASS. Каждый отдельный runtime LOGIN получает отказ DDL/DML/EXECUTE в закрытой основе.

Параметры: container_service — контейнеры, subject_service — субъекты,
object_service — объекты, policy_service — metadata моделей,
catalog_operator — каталоги, fact_reader — подготовленные факты.
Во всех шести случаях LOGIN имеет только соответствующий group membership,
без deployment полномочий. Пока protected APIs не поставлены, даже каталоговая
и reader роли не должны обходить закрытые ACL прямой записью или функцией.
- tests/component/test_migrations.py::test_real_runtime_login_cannot_execute_ddl_or_broad_dml[tamarix_container_service]: PASS. Каждый отдельный runtime LOGIN получает отказ DDL/DML/EXECUTE в закрытой основе.

Параметры: container_service — контейнеры, subject_service — субъекты,
object_service — объекты, policy_service — metadata моделей,
catalog_operator — каталоги, fact_reader — подготовленные факты.
Во всех шести случаях LOGIN имеет только соответствующий group membership,
без deployment полномочий. Пока protected APIs не поставлены, даже каталоговая
и reader роли не должны обходить закрытые ACL прямой записью или функцией.
- tests/component/test_migrations.py::test_real_runtime_login_cannot_execute_ddl_or_broad_dml[tamarix_fact_reader]: PASS. Каждый отдельный runtime LOGIN получает отказ DDL/DML/EXECUTE в закрытой основе.

Параметры: container_service — контейнеры, subject_service — субъекты,
object_service — объекты, policy_service — metadata моделей,
catalog_operator — каталоги, fact_reader — подготовленные факты.
Во всех шести случаях LOGIN имеет только соответствующий group membership,
без deployment полномочий. Пока protected APIs не поставлены, даже каталоговая
и reader роли не должны обходить закрытые ACL прямой записью или функцией.
- tests/component/test_migrations.py::test_real_runtime_login_cannot_execute_ddl_or_broad_dml[tamarix_object_service]: PASS. Каждый отдельный runtime LOGIN получает отказ DDL/DML/EXECUTE в закрытой основе.

Параметры: container_service — контейнеры, subject_service — субъекты,
object_service — объекты, policy_service — metadata моделей,
catalog_operator — каталоги, fact_reader — подготовленные факты.
Во всех шести случаях LOGIN имеет только соответствующий group membership,
без deployment полномочий. Пока protected APIs не поставлены, даже каталоговая
и reader роли не должны обходить закрытые ACL прямой записью или функцией.
- tests/component/test_migrations.py::test_real_runtime_login_cannot_execute_ddl_or_broad_dml[tamarix_policy_service]: PASS. Каждый отдельный runtime LOGIN получает отказ DDL/DML/EXECUTE в закрытой основе.

Параметры: container_service — контейнеры, subject_service — субъекты,
object_service — объекты, policy_service — metadata моделей,
catalog_operator — каталоги, fact_reader — подготовленные факты.
Во всех шести случаях LOGIN имеет только соответствующий group membership,
без deployment полномочий. Пока protected APIs не поставлены, даже каталоговая
и reader роли не должны обходить закрытые ACL прямой записью или функцией.
- tests/component/test_migrations.py::test_real_runtime_login_cannot_execute_ddl_or_broad_dml[tamarix_subject_service]: PASS. Каждый отдельный runtime LOGIN получает отказ DDL/DML/EXECUTE в закрытой основе.

Параметры: container_service — контейнеры, subject_service — субъекты,
object_service — объекты, policy_service — metadata моделей,
catalog_operator — каталоги, fact_reader — подготовленные факты.
Во всех шести случаях LOGIN имеет только соответствующий group membership,
без deployment полномочий. Пока protected APIs не поставлены, даже каталоговая
и reader роли не должны обходить закрытые ACL прямой записью или функцией.
- tests/component/test_migrations.py::test_downgrade_requires_explicit_disposable_safeguard: PASS. CLI и прямой Alembic downgrade без disposable safeguard сохраняют основу.

Проверка предотвращает обход ограничения через Python Alembic API:
отсутствие config flag должно отклоняться самой revision, а не только CLI.
- tests/component/test_migrations.py::test_shapes_upgrade_preserves_existing_catalog_and_values: PASS. Заполненная 0003 переходит к shapes без изменения IDs/values/revisions/views/ACL и DN keys.

Содержит все families и native types, empty sets и retained tombstone.
Проверяются one-shape-per-definition map, точные структурные ссылки и
неизменность повторного head upgrade; новый fixture с одной head этого не доказывает.
- tests/component/test_migrations.py::test_shapes_upgrade_failure_rolls_back_schema_and_data: PASS. Ошибка после фактического создания shapes, но до commit возвращает целую заполненную 0003.

Test-only SQLAlchemy callback прерывает настоящий migration execution после
DDL; затем отдельный blocker воспроизводит lock_timeout. Исходные SQL/resources
не меняются. Сверка включает данные, columns, constraints, routines,
view ACL/OID и прежнюю Alembic revision после каждого отказа.
- tests/component/test_migrations.py::test_shapes_disposable_downgrade_restores_previous_contract: PASS. Filled new→0003→head сохраняет старые факты и DN, явно теряя shape key/id/sharing.

Сначала добавляются две definitions с общей именованной формой и values;
reverse разрешён только disposable flag. После нового upgrade каждая
definition получает собственный migrated shape без обещания восстановления UI metadata.
- tests/component/test_migrations.py::test_shapes_downgrade_without_disposable_safeguard_preserves_state: PASS. Прямой Alembic reverse без disposable flag отклоняется до изменения заполненной head.

Проверяется bypass CLI: semantic snapshots, raw shape rows, pin-ссылки,
schema signatures и revision после отказа должны полностью сохраниться.
- tests/component/test_model_metadata.py::test_model_metadata_view_survives_subject_tombstone_and_delete_keeps_other_entities: PASS. Модель хранит только metadata/attrs и видна независимо от tombstone другого subject.

Hard delete модели очищает собственные attrs и оставляет subjects/objects.
Проверка не вводит отложенные privileges/actions/references или fake payload.
- tests/component/test_model_metadata.py::test_model_key_case_insensitive_uniqueness_is_holder_local: PASS. Model key CI уникален у holder, сохраняет spelling и допускает512 ASCII characters.

Тот же key у другого holder разрешён; case-only duplicate в одном holder
отклоняется. Проверка относится к metadata identity, без model internals.
- tests/component/test_model_metadata.py::test_model_identity_is_immutable_in_database[model-holder]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_model_metadata.py::test_model_identity_is_immutable_in_database[model-key]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_model_metadata.py::test_model_key_contracts_cannot_be_bypassed[model-length]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.
- tests/component/test_model_metadata.py::test_model_key_contracts_cannot_be_bypassed[model-alphabet]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.
- tests/component/test_objects.py::test_object_unbounded_exact_keys_remain_collision_safe: PASS. Очень длинные object TEXT keys сохраняются, а hash collision не отвергает разные ключи.

Только в своей disposable БД trusted digest helper заменён постоянным hash:
оба разных ключа обязаны сохраниться в одном bucket, точный duplicate обязан
получить unique violation. Это проверяет реальный guard, не вероятность SHA256.
- tests/component/test_objects.py::test_object_duplicate_prevention_with_old_concurrent_snapshot[read-committed]: PASS. Два независимых writer с заранее открытыми snapshots не создают duplicate object.

Barrier открывает оба чтения до первого commit, второй INSERT идёт после него.
RC обязан вернуть unique violation, RR/SERIALIZABLE — serialization failure:
старый snapshot не даёт обойти holder/bucket MVCC fencing.
- tests/component/test_objects.py::test_object_duplicate_prevention_with_old_concurrent_snapshot[repeatable-read]: PASS. Два независимых writer с заранее открытыми snapshots не создают duplicate object.

Barrier открывает оба чтения до первого commit, второй INSERT идёт после него.
RC обязан вернуть unique violation, RR/SERIALIZABLE — serialization failure:
старый snapshot не даёт обойти holder/bucket MVCC fencing.
- tests/component/test_objects.py::test_object_duplicate_prevention_with_old_concurrent_snapshot[serializable]: PASS. Два независимых writer с заранее открытыми snapshots не создают duplicate object.

Barrier открывает оба чтения до первого commit, второй INSERT идёт после него.
RC обязан вернуть unique violation, RR/SERIALIZABLE — serialization failure:
старый snapshot не даёт обойти holder/bucket MVCC fencing.
- tests/component/test_objects.py::test_object_identity_is_immutable_in_database[object-holder]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_objects.py::test_object_identity_is_immutable_in_database[object-key]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_objects.py::test_object_key_contracts_cannot_be_bypassed[object-empty]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.
- tests/component/test_objects.py::test_object_key_contracts_cannot_be_bypassed[object-control]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.
- tests/component/test_subjects.py::test_subject_exact_keys_type_scope_and_tombstone_restore: PASS. Subject identity точна по Unicode, holder/type; tombstone резервирует ключ и восстанавливает ID.

Soft delete удерживает attrs, скрывает active view и повышает aggregate revision.
Создание fresh ID запрещено; restore с исходным актуальным CAS возвращает тот
же ID/type/key/holder, stale CAS не меняет состояние.
- tests/component/test_subjects.py::test_restore_and_container_purge_serialize_on_holder[restore-first]: PASS. Restore и hard container delete из старых snapshot имеют единственного победителя.

Два независимых SERIALIZABLE соединения читают до первого commit. Проигравший
получает40001, а повтор с новым snapshot сохраняет исходный CAS и возвращает
активный blocker либо NotFound. Нельзя восстановить уже purged tombstone.
- tests/component/test_subjects.py::test_restore_and_container_purge_serialize_on_holder[purge-first]: PASS. Restore и hard container delete из старых snapshot имеют единственного победителя.

Два независимых SERIALIZABLE соединения читают до первого commit. Проигравший
получает40001, а повтор с новым snapshot сохраняет исходный CAS и возвращает
активный blocker либо NotFound. Нельзя восстановить уже purged tombstone.
- tests/component/test_subjects.py::test_subject_identity_is_immutable_in_database[subject-holder]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_subjects.py::test_subject_identity_is_immutable_in_database[subject-type]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_subjects.py::test_subject_identity_is_immutable_in_database[subject-key]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_subjects.py::test_subject_identity_is_immutable_in_database[subject-id]: PASS. Прямая UPDATE попытка изменить identity получает отказ, даже с deployment соединением.

Каждый параметр описывает защищённое поле. Проверка подтверждает DB enforcement,
а не только отсутствие поля в публичном application DTO.
- tests/component/test_subjects.py::test_subject_key_contracts_cannot_be_bypassed[subject-length]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.
- tests/component/test_subjects.py::test_subject_key_contracts_cannot_be_bypassed[subject-control]: PASS. Недопустимый key отклоняется DB CHECK; различия политики перечислены в параметрах.

Прямая запись обходит adapters, поэтому отказ доказывает сохранение принятой
identity политики при любой будущей command implementation.


[JSON](results.json) · [pytest log](pytest.log) · [JUnit](junit.xml)
