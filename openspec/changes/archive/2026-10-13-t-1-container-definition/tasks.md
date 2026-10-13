# Tasks

План для `t-1-container-definition`, схема `spec-driven`.
Основа: [design.md](design.md), [proposal.md](proposal.md) и четыре delta specs.
Статус на 2026-10-10: завершены и проверены все задачи согласованного логического scope (31/31).
Актуальный прогресс отражён чекбоксами; исходники и тесты находятся в пяти кодовых каталогах.

Объём кода ниже — логическое ядро и контракты поставщиков фактов из design.
Тестовые поставщики используются только в проверках и не выбирают production-хранилище
или механизм аутентификации. Реальные API/PKI, физическое хранение, конкурентная
целостность, движки правил и deployment требуют отдельных изменений до runtime-интеграции.
`db-control` и `access-assignment-api` не получают кодовых задач этого логического scope;
все будущие DDL/Alembic-изменения относятся исключительно к `db-control`.

Прочитаны корневой AGENTS.md, config, все документы `openspec/context/`,
реестр ADR, основные заготовки subjects/objects и все артефакты change.
Принятые границы сервисов, допуск владельца и семантика неизвестного состава
зафиксированы в [ADR 0001](../../../context/adr/0001-t1-service-boundaries-and-admission.md)
и Context design. Технические решения 2, 4–7 приняты пользователем в review 1.6
и зафиксированы в [ADR 0002](../../../context/adr/0002-t1-logical-core.md).

## 1. Согласование предыдущих артефактов

Зависимости: отсутствуют. Эти задачи выполняются до кода.

- [x] 1.1 `tamarix-specs`: обновить `requirements.md` по принятым ответам — достаточность сертификатной аутентификации и DN→`O`, запрет при неизвестном составе цепочки, карта сервисов. Проверка: эти решения явно записаны, соответствующие прежние TBD сняты, нейтральность неопределённой известной модели сохранена.
- [x] 1.2 `tamarix-specs`: уточнить в `specs/containers/spec.md` достаточность сертификата и привязки DN для статуса владельца; добавить Scenario «Владельцу достаточно сертификата и привязки DN». Проверка: сценарий имеет наблюдаемый WHEN/THEN, не вводит дополнительную административную роль; `openspec validate t-1-container-definition --strict --json --store tamarix-specs` проходит.
- [x] 1.3 `tamarix-specs`: добавить в `specs/authorization/access-check/spec.md` Requirement «Запрет при неизвестном составе цепочки» со Scenario «Неизвестен путь до контейнера объекта», «Неизвестен полный набор моделей», «Известное разрешение при неизвестном составе цепочки»; убрать этот вопрос из TBD. Проверка: во всех случаях ожидается запрет, известный `Undefined` по-прежнему нейтрален, строгая валидация проходит.
- [x] 1.4 `tamarix-specs`: привести scope, Capabilities и Impact `proposal.md` к принятым уточнениям; обновить в `design.md` отметку о ещё не выполненной синхронизации после 1.1–1.3. Проверка: requirements/proposal/specs/design одинаково описывают достаточный допуск владельца, неизвестную цепочку и принятую ответственность сервисов; исключения API/хранения/движков сохранены.
- [x] 1.5 `tamarix-specs`: отразить принятые границы сервисов и семантику допуска/отказов в применимых context docs и зарегистрировать ADR с источником принятия от 2026-10-09. Проверка: ссылки реестра ведут к созданной записи; принятые решения отделены от рекомендаций и неподтверждённой реализации.
- [x] 1.6 `tamarix-specs`: провести review и получить явное принятие предлагаемых технических решений 2, 4–7 design; обновить таблицу прослеживаемости после 1.2–1.3. Проверка: результат review записан, каждое новое Requirement/Scenario связано с планируемым тестом; отклонённые решения исправлены до зависимого кода.

## 2. Подготовка репозиториев и проверок

Зависимости: раздел 1. Репозиторий `container-adm-api` и абсолютный путь
`/Users/mfedotenko/Projects/Tamarix/container-adm-api` приняты пользователем 2026-10-09.

- [x] 2.1 `tamarix-specs` → `container-adm-api`: закрепить с пользователем имя и абсолютный путь нового репозитория; подготовить его с указателем `store: tamarix-specs`, затем заменить условное обозначение сервиса в design/tasks/context фактическим именем. Проверка: каталог доступен, имя согласовано, локальных specs/changes в нём нет.
- [x] 2.2 `tamarix-specs`: принять минимальную упаковку Python-ядра и testing framework, проверить официальные стабильные релизы и совместимый набор требуемых зависимостей. Проверка: решение и согласованные базовые версии записаны; для тестов заданы команды запуска; не выбраны prerelease, wire-протокол или хранилище по умолчанию.
- [x] 2.3 `tamarix-specs` совместно с `container-adm-api`, `entity-subject-adm-api`, `entity-object-adm-api`, `policy-adm-api`, `policy-decision-api`: уточнить логические контракты поставщиков фактов, подтверждённого вызывающего, полного набора моделей и вычислителя отдельной модели. Проверка: есть согласованные входы/результаты и примеры complete/unknown, Neutral/Undefined; распределение кодовых интерфейсов закреплено без выбора транспорта и общей БД.

## 3. Ядро сервиса контейнеров

Зависимости: раздел 2. Репозиторий: `container-adm-api` из 2.1.

- [x] 3.1 `container-adm-api`: подготовить Python-проект по 2.2 с `pyproject.toml`, `uv.lock` и `.python-version`. Проверка: `uv lock --check` и `uv sync --frozen` успешны; выбранная команда тестов доступна; указатель store сохранён.
- [x] 3.2 `container-adm-api`: реализовать правила типов, единственного родителя, структурное отношение «предок или сам», логический путь ключей и однозначную идентификацию. Одновременно добавить тесты `test_t1_tree.py`/`test_t1_keys.py` из таблицы и документировать входы ядра. Проверка: все перечисленные случаи проходят, включая полную матрицу типов, четыре типа корня, пропуски и дублирование составного ключа; wire-формат ключа не закреплён тестовыми данными.
- [x] 3.3 `container-adm-api`: реализовать проверку двух явно заданных контейнеров и допуска на основании проверенного сертификатного факта и зарегистрированной привязки DN→`O`. Добавить `test_t1_request_context.py`, включая новый случай из 1.2. Проверка: оба типа обращения проходят при допустимых фактах и отклоняются без подтверждения `O`; тесты не выдаются за проверку реального сертификатного адаптера.
- [x] 3.4 `container-adm-api`: предоставить логический контракт полного пути до контейнера и отношений дерева; документировать различие полного пути и невозможности его установить. Добавить контрактные проверки `tests/test_t1_container_facts.py::test_path_completeness`. Проверка: тестовый потребитель различает подтверждённый путь и unknown, а соседняя ветка в путь не попадает; команды и результаты проверок 3.2–3.4 записаны здесь.

## 4. Субъекты и область управления

Зависимости: раздел 3. Этот раздел может выполняться параллельно разделу 5.

- [x] 4.1 `entity-subject-adm-api`: подготовить Python-проект по 2.2 с согласованными manifest/lock/Python. Проверка: `uv lock --check`, `uv sync --frozen` и выбранная команда тестов успешны; store-only сохранён.
- [x] 4.2 `entity-subject-adm-api`: реализовать единственного держателя субъекта и логическое предоставление его фактов; сохранить держателя при использовании ссылок на субъект. Добавить `test_t1_subject_holders.py` и документацию контракта. Проверка: все пять entity-сценариев проходят на контролируемых фактах; использование одной/нескольких моделей не изменяет держателя; результаты записаны здесь.
- [x] 4.3 `entity-subject-adm-api`: включить подтверждение вызывающего и проверки `O ≼ C ≼ D` в логическую операцию управления субъектом; сохранить инвариант держателя. Добавить случаи ADM в `test_t1_management.py` и документировать отказные границы. Проверка: все относящиеся к субъектам случаи таблицы проходят, недопустимая операция не меняет состояние; отсутствие моделей не блокирует управление.

## 5. Объекты и область управления

Зависимости: раздел 3. Может выполняться параллельно разделу 4.

- [x] 5.1 `entity-object-adm-api`: подготовить Python-проект по 2.2 с согласованными manifest/lock/Python. Проверка: `uv lock --check`, `uv sync --frozen` и выбранная команда тестов успешны; store-only сохранён.
- [x] 5.2 `entity-object-adm-api`: реализовать единственного держателя объекта и логическое предоставление его фактов; сохранить держателя при использовании ссылок на объект. Добавить `test_t1_object_holders.py` и документацию контракта. Проверка: все пять entity-сценариев проходят на контролируемых фактах; использование одной/нескольких моделей не изменяет держателя; результаты записаны здесь.
- [x] 5.3 `entity-object-adm-api`: включить подтверждение вызывающего и проверки `O ≼ C ≼ D` в логическую операцию управления объектом; сохранить инвариант держателя. Добавить случаи ADM в `test_t1_management.py` и документировать отказные границы. Проверка: все относящиеся к объектам случаи таблицы проходят, недопустимая операция не меняет состояние; отсутствие моделей не блокирует управление.

## 6. Модели и статические ссылки

Зависимости: разделы 4 и 5.

- [x] 6.1 `policy-adm-api`: подготовить Python-проект по 2.2 с согласованными manifest/lock/Python. Проверка: `uv lock --check`, `uv sync --frozen` и выбранная команда тестов успешны; store-only сохранён.
- [x] 6.2 `policy-adm-api`: реализовать единственного держателя модели, допустимость `0..N` моделей и контракт полного списка моделей заданных контейнеров. Добавить `test_t1_models.py` и `tests/test_t1_model_facts.py::test_model_set_completeness`; документировать complete/unknown. Проверка: holder/количество/полнота проходят, отсутствие списка не подменяется пустым списком; результаты записаны здесь.
- [x] 6.3 `policy-adm-api`: реализовать проверки ссылок `H(S) ≼ M` и `M ≼ H(Q)` по фактам entity-сервисов и дерева. Добавить `test_t1_model_references.py` и описать сохранение держателей. Проверка: все случаи обеих областей проходят, включая соседние ветки и пропуски; ссылки не назначают держателем сущности контейнер модели.
- [x] 6.4 `policy-adm-api`: включить подтверждение вызывающего, `O ≼ C ≼ D` и сохранение инвариантов в логическое управление моделью. Добавить случаи ADM и ADM* в `test_t1_management.py`. Проверка: полные права не разрешают недопустимые ссылки или нескольких держателей; отказы не изменяют модель; документация и результаты обновлены в этой группе.

## 7. Проверка доступа субъекта

Зависимости: разделы 3–6; контракты 2.3. Внутри раздела сначала реализуются
операторы и вычисление известной модели, затем вход проверки и сборка цепочки.
В 7.5 проверяется входная часть; сценарии, требующие итогового решения через
полный поток, проверяются и считаются завершёнными после 7.6.

- [x] 7.1 `policy-decision-api`: подготовить Python-проект по 2.2 с согласованными manifest/lock/Python. Проверка: `uv lock --check`, `uv sync --frozen` и выбранная команда тестов успешны; store-only сохранён.
- [x] 7.2 `policy-decision-api`: реализовать чистый оператор объединения определённых подходящих правил. Добавить `test_t1_rule_aggregation.py` и описание входа. Проверка: любой подходящий запрет побеждает, неподходящий запрет не влияет, только разрешения дают Allow, отсутствие подходящих правил — Neutral; тесты проходят до следующей задачи.
- [x] 7.3 `policy-decision-api`: реализовать чистый оператор объединения результатов всех моделей установленного состава цепочки. Добавить `test_t1_chain_aggregation.py` и описание входа. Проверка: все случаи приоритета запрета и default deny проходят, Neutral/Undefined нейтральны, первое разрешение не скрывает последующий запрет; тесты проходят до следующей задачи.
- [x] 7.4 `policy-decision-api`: реализовать проверку области субъекта отдельно для каждой модели и вызов порта вычислителя с различимыми Neutral/Undefined. Добавить `test_t1_model_evaluation.py` на заданных результатах/ошибке вычисления/недоступности данных известной модели и использовать оператор 7.3 для итоговых критериев; документировать границы порта. Проверка: все случаи применимости и неопределённости проходят; семантика ошибок отдельных правил не выбрана.
- [x] 7.5 `policy-decision-api`: реализовать логический вход проверки с подтверждённым `O`, отдельным субъектом, объектом и действием; проверить `C ≼ R`. Добавить проверки валидации и разделения вызывающего/субъекта в `test_t1_access_check.py`, используя операции 7.2–7.4 и заданные факты; документировать вход. Проверка: подмена субъекта DN/владельцем отсутствует, лишнего ограничения субъекта относительно `C` нет, негативные входы отклоняются; проверки итогового доступа остаются в 7.6.
- [x] 7.6 `policy-decision-api`: реализовать сбор полного пути root→`R` и всех моделей и соединить его с входом и операциями 7.2–7.5. Добавить `test_t1_chain.py`, включая `test_unknown_chain_denies` после 1.3, и случаи итогового доступа в `test_t1_access_check.py`; документировать поток. Проверка: все критерии полной цепочки и итогового решения проходят, включая Allow для субъекта-потомка адресата и Deny независимо от прав владельца; предки `C` и все модели пути участвуют, соседние ветки исключены; unknown даёт запрет даже при доступном разрешении; команды/результаты группы записаны здесь.

## 8. Сквозная проверка логических контрактов

Зависимости: разделы 3–7. Локальные тесты и документация предыдущих групп
должны быть готовы и проверены до этого раздела.

- [x] 8.1 `policy-decision-api` совместно с `container-adm-api`, `entity-subject-adm-api`, `entity-object-adm-api`, `policy-adm-api`: добавить `tests/contracts/test_t1_flow.py::test_cross_service_facts` для сквозной сборки решения и `policy-adm-api/tests/contracts/test_t1_holder_links.py::test_holder_preservation` для состояния сущностей после ссылок моделей. Проверка: реальные логические операции всех сторон соединены тестовыми адаптерами, сценарии пропусков/веток/держателей/неполной цепочки проходят; зафиксированы команды и результаты интеграционных проверок.
- [x] 8.2 `tamarix-specs` совместно с пятью кодовыми репозиториями: сверить актуальные specs со всеми фактическими тестами, заменить планируемые ссылки и проверить evidence каждой группы. Проверка: ни один Requirement/Scenario не потерян, все относящиеся к логическому scope тесты прошли; недоступные/неуспешные проверки оставлены открытыми; подтверждённые границы готовности и последующие runtime-изменения описаны явно.

## Прослеживаемость требований и критериев приёмки

Все 29 Requirement / 91 Scenario четырёх актуальных delta specs связаны
с фактическими pytest-тестами. Таблицы ниже перечисляют существующие функции;
точные node IDs с вариантами параметризации, команды, результаты и SHA-256
проверенных исходников находятся в [test-evidence.json](test-evidence.json).
Для каждой строки проверяется полное WHEN/THEN сценария, включая строки
таблиц и варианты. Один Scenario может покрываться несколькими тестами:
локальная проверка дополняется полным потоком или сквозным контрактом.

`container-adm-api` — отдельный сервис контейнеров, подготовленный в задаче 2.1
по пути `/Users/mfedotenko/Projects/Tamarix/container-adm-api`. `ADM` означает **каждый** из трёх репозиториев:
`entity-subject-adm-api`, `entity-object-adm-api`, `policy-adm-api`.
Для `ADM*` случай «Недопустимая ссылка при полных правах» выполняется в
`policy-adm-api`; случай «Несколько держателей при управлении» — во всех трёх.
Для двух типов обращений проверки адресации/допуска повторяются для управления
и проверки доступа. Таблицы типов, вариантов корня и областей разворачиваются
во все перечисленные в specs варианты, а не в один показательный пример.

### containers

Полный путь спецификации:
`/Users/mfedotenko/Projects/Tamarix/tamarix-specs/openspec/changes/t-1-container-definition/specs/containers/spec.md`.

| Точный Requirement | Точные Scenario — отдельные случаи | Репозиторий / фактический файл::функция | Задачи |
| --- | --- | --- | --- |
| Упорядоченное дерево контейнеров | Допустимые непосредственные дети<br>Обратный порядок типов<br>Повторение типа вдоль пути<br>Соседние контейнеры одного типа<br>Два непосредственных родителя | container-adm-api / `tests/test_t1_tree.py::test_ordered_tree` | 3.2 |
| Пропуск уровней и тип корня | Пропуск промежуточных уровней<br>Каждый допустимый тип в корне<br>Корневой module | container-adm-api / `tests/test_t1_tree.py::test_skipped_levels_and_root` | 3.2 |
| Строковый ключ контейнера | Ключ задан строкой<br>Нестроковый ключ | container-adm-api / `tests/test_t1_keys.py::test_string_key` | 3.2 |
| Уникальная идентификация составным ключом | Путь до вложенного контейнера<br>Составной ключ корня<br>Дублирование составного ключа | container-adm-api / `tests/test_t1_keys.py::test_composite_key` | 3.2 |
| Единственный контейнер-держатель модели | Модель в контейнере<br>Несколько держателей модели<br>Модель без держателя | policy-adm-api / `tests/test_t1_models.py::test_single_model_holder` | 6.2 |
| Необязательное наличие моделей | Контейнер без моделей<br>Одна или несколько моделей | policy-adm-api / `tests/test_t1_models.py::test_optional_models` | 6.2 |
| Допустимая область субъектов модели | Субъект модели и её предка<br>Субъект потомка или соседней ветки<br>Предок при пропущенных типах | policy-adm-api / `tests/test_t1_model_references.py::test_subject_scope` | 6.3 |
| Допустимая область объектов модели | Объект модели и её потомка<br>Объект предка или соседней ветки<br>Потомок при пропущенных типах | policy-adm-api / `tests/test_t1_model_references.py::test_object_scope` | 6.3 |
| Два типа обращений с явной адресацией | Адресуемый и представляемый контейнеры различаются<br>Адресуемый и представляемый контейнеры совпадают<br>Не указан один из контейнеров | container-adm-api / `tests/test_t1_request_context.py::test_explicit_addressing` | 3.3 |
| Сертификатное подтверждение представляемого контейнера | DN приписан к представляемому контейнеру<br>DN приписан только к другому контейнеру<br>Отсутствует успешная сертификатная аутентификация | container-adm-api / `tests/test_t1_request_context.py::test_certificate_binding` | 3.3 |
| Полные права владельца на управление | Управление в самом представляемом контейнере<br>Управление данными потомка через владельца<br>Управление контейнером без моделей | ADM / `tests/test_t1_management.py::test_owner_management_rights` | 4.3 / 5.3 / 6.4 |
| Полные права владельца на управление | Владельцу достаточно сертификата и привязки DN | container-adm-api / `tests/test_t1_request_context.py::test_certificate_owner_sufficiency` | 3.3 |
| Область адресации управления | Прямое управление потомком<br>Потомок адресует управление к предку<br>Адресация в соседнюю ветку | ADM / `tests/test_t1_management.py::test_management_address_scope` | 4.3 / 5.3 / 6.4 |
| Область управляемых моделей и сущностей | Управление поддеревом адресуемого контейнера<br>Данные предка адресуемого контейнера<br>Данные другой ветки под представляемым контейнером | ADM / `tests/test_t1_management.py::test_managed_data_scope` | 4.3 / 5.3 / 6.4 |
| Сохранение инвариантов при управлении | Недопустимая ссылка при полных правах<br>Несколько держателей при управлении | ADM* / `tests/test_t1_management.py::test_management_invariants` | 4.3 / 5.3 / 6.4 |

### authorization/access-check

Полный путь спецификации:
`/Users/mfedotenko/Projects/Tamarix/tamarix-specs/openspec/changes/t-1-container-definition/specs/authorization/access-check/spec.md`.

| Точный Requirement | Точные Scenario — отдельные случаи | Репозиторий / фактический файл::функция | Задачи |
| --- | --- | --- | --- |
| Отдельный субъект проверки доступа | Аутентифицированный вызывающий передаёт субъект<br>Не передан ключ субъекта<br>Не задан объект или действие<br>Не подтверждён представляемый контейнер | policy-decision-api / `tests/test_t1_access_check.py::test_separate_subject`<br>policy-decision-api / `tests/test_t1_access_check.py::test_separate_subject_full_flow` | 7.5 / 7.6 |
| Адресация проверки относительно объекта | Обращение к контейнеру объекта<br>Обращение к предку контейнера объекта<br>Обращение к потомку или соседней ветке<br>Представляемый контейнер вне пути объекта | policy-decision-api / `tests/test_t1_access_check.py::test_object_address_scope`<br>policy-decision-api / `tests/contracts/test_t1_flow.py::test_cross_service_facts` | 7.5 |
| Отсутствие общей привязки субъекта к адресату | Держатель субъекта является потомком адресата<br>Субъект из другой ветки | policy-decision-api / `tests/test_t1_access_check.py::test_no_global_subject_binding`<br>policy-decision-api / `tests/test_t1_access_check.py::test_no_global_subject_binding_full_flow`<br>policy-decision-api / `tests/contracts/test_t1_flow.py::test_cross_service_facts` | 7.5 / 7.6 |
| Полная цепочка моделей до контейнера объекта | Запрет предка адресуемого контейнера<br>Адресация непосредственно к контейнеру объекта<br>Объект в корневом контейнере<br>Несколько моделей одного контейнера<br>Контейнер без моделей внутри пути<br>Пропущенные уровни дерева<br>Соседняя ветка исключена | policy-decision-api / `tests/test_t1_chain.py::test_full_model_chain`<br>policy-decision-api / `tests/contracts/test_t1_flow.py::test_cross_service_facts` | 7.6 |
| Запрет при неизвестном составе цепочки | Неизвестен путь до контейнера объекта<br>Неизвестен полный набор моделей<br>Известное разрешение при неизвестном составе цепочки | policy-decision-api / `tests/test_t1_chain.py::test_unknown_chain_denies`<br>policy-decision-api / `tests/contracts/test_t1_flow.py::test_cross_service_facts` | 7.6 |
| Нейтральность модели вне области субъекта | Держатель субъекта является потомком держателя модели<br>Субъект из соседней ветки модели<br>Другая модель разрешает доступ | policy-decision-api / `tests/test_t1_model_evaluation.py::test_model_subject_scope` | 7.4 |
| Объединение подходящих правил модели | Разрешение и запрет внутри одной модели<br>Подходят только разрешения<br>Запрет не подходит запросу<br>Подходящих правил нет | policy-decision-api / `tests/test_t1_rule_aggregation.py::test_rule_aggregation`<br>policy-decision-api / `tests/test_t1_rule_aggregation.py::test_rule_aggregation_nonmatching_deny` | 7.2 |
| Нейтральная трактовка неопределённого результата модели | Ошибка модели при известном разрешении<br>Недоступные данные при известном разрешении<br>Неопределённость при известном запрете | policy-decision-api / `tests/test_t1_model_evaluation.py::test_undefined_model`<br>policy-decision-api / `tests/test_t1_chain.py::test_known_model_failure_full_flow`<br>policy-decision-api / `tests/contracts/test_t1_flow.py::test_cross_service_facts` | 7.4 / 7.6 / 8.1 |
| Приоритет запрета в цепочке моделей | Разрешения вместе с запретом<br>Только разрешения и нейтральные результаты<br>Разрешение вместе с неопределённостью | policy-decision-api / `tests/test_t1_chain_aggregation.py::test_chain_aggregation` | 7.3 |
| Запрет по умолчанию | Все модели нейтральны<br>Нейтральность вместе с неопределённостью<br>Все результаты неопределённы<br>Пустая цепочка моделей | policy-decision-api / `tests/test_t1_chain_aggregation.py::test_default_deny` | 7.3 |
| Административные права не подменяют доступ субъекта | Владелец управляет объектом, но субъекту запрещено<br>На пути до объекта нет моделей доступа | policy-decision-api / `tests/test_t1_access_check.py::test_owner_does_not_grant_subject_access`<br>policy-decision-api / `tests/contracts/test_t1_flow.py::test_cross_service_facts` | 7.6 |

### entities/subjects

Полный путь спецификации:
`/Users/mfedotenko/Projects/Tamarix/tamarix-specs/openspec/changes/t-1-container-definition/specs/entities/subjects/spec.md`.

| Точный Requirement | Точные Scenario — отдельные случаи | Репозиторий / фактический файл::функция | Задачи |
| --- | --- | --- | --- |
| Единственный контейнер-держатель субъекта | Контейнер является держателем субъекта<br>Несколько держателей субъекта<br>Субъект без держателя | entity-subject-adm-api / `tests/test_t1_subject_holders.py::test_single_subject_holder` | 4.2 |
| Сохранение держателя субъекта при использовании в модели | Модель потомка использует субъект предка<br>Несколько моделей других контейнеров | entity-subject-adm-api / `tests/test_t1_subject_holders.py::test_subject_holder_preservation`<br>policy-adm-api / `tests/contracts/test_t1_holder_links.py::test_holder_preservation` | 4.2 / 8.1 |

### entities/objects

Полный путь спецификации:
`/Users/mfedotenko/Projects/Tamarix/tamarix-specs/openspec/changes/t-1-container-definition/specs/entities/objects/spec.md`.

| Точный Requirement | Точные Scenario — отдельные случаи | Репозиторий / фактический файл::функция | Задачи |
| --- | --- | --- | --- |
| Единственный контейнер-держатель объекта | Контейнер является держателем объекта<br>Несколько держателей объекта<br>Объект без держателя | entity-object-adm-api / `tests/test_t1_object_holders.py::test_single_object_holder` | 5.2 |
| Сохранение держателя объекта при использовании в модели | Модель предка использует объект потомка<br>Несколько моделей других контейнеров | entity-object-adm-api / `tests/test_t1_object_holders.py::test_object_holder_preservation`<br>policy-adm-api / `tests/contracts/test_t1_holder_links.py::test_holder_preservation` | 5.2 / 8.1 |

## Результаты проверок

### Документальные задачи 1.1–1.6 — 2026-10-09

- requirements/proposal/specs/design синхронизированы с принятыми ответами;
  context обновлён, ADR 0001 зарегистрирован как accepted.
- Технический review решений 2, 4–7: существенных расхождений с требованиями
  не выявлено; пользователь явно принял подход, источник записан в design/ADR 0002.
- Прослеживаемость сверена с актуальными четырьмя delta specs:
  29 Requirement / 91 Scenario, отсутствующих планируемых связей нет.
- `openspec validate t-1-container-definition --strict --json --store tamarix-specs`:
  exit 0, valid true, issues [].
- `git diff --check -- openspec/context openspec/changes/t-1-container-definition`:
  exit 0; 124 локальные ссылки обновлённого context проверены без пропусков
  перед добавлением ADR 0002.

На этапе документальных задач раздела 1 автоматизированные тесты кода
ещё не были созданы или запущены. Последующие результаты кодовых групп
записаны ниже с командами, состоянием рабочих каталогов и фактическими тестами.

Проверки на тестовых фактах не подтверждают production PKI, wire API, полноту
реальных источников, согласованность конкурентных операций или rollout.
Полную фичу нельзя объявить реализованной по этому evidence; перед подключением
runtime-адаптеров нужны соответствующие отдельные design, задачи и проверки.
Архивирование возможно после выполнения отслеживаемой работы и применимых
требований проекта, а не только после появления всех четырёх planning artifacts.

### Подготовка 2.1–2.3 и начало 3.1 — 2026-10-09

- Принято и создано: `/Users/mfedotenko/Projects/Tamarix/container-adm-api`,
  Git-ветка `feature/t-1-container-definition`, пока без коммитов/remote.
  `rg --files --hidden -g '!**/.git/**' -g '!**/.DS_Store'` при закрытии 2.1
  показал только `openspec/config.yaml`; содержимое `store: tamarix-specs`.
  `openspec list --json --store tamarix-specs` из нового каталога разрешил центральный store.
- Пользователь явно принял `python-environment.md` и `logical-contracts.md`;
  оба имеют статус accepted. Источники, metadata compatibility и границы
  зафиксированы в ADR 0003. Это не свидетельство выполненного install/build/test.
- `uv tool run --from uv==0.12.24 uv --version`: exit 0,
  `uv 0.12.24 (5411378eb 2026-10-08 aarch64-apple-darwin)`.
  Используется изолированный launcher; Homebrew uv автоматически не обновлялся.
- `uv tool run --from uv==0.12.24 uv python install 3.15.0`: exit 2,
  `No download found for request: cpython-3.15.0-macos-aarch64-none`.
- В 3.1 подготовлены manifest, pin Python, package scaffold и README.
  Lock/sync/build и тесты ожидают доступного final Python 3.15.0;
  задача 3.1 остаётся открытой.
- Официальный macOS installer загружен в
  `/private/tmp/tamarix-python-3.15.0-macos11.pkg`.
  `shasum -a 256 /private/tmp/tamarix-python-3.15.0-macos11.pkg`: exit 0,
  `7c7e7eca61cbfa5f0c6f80cd594cddbfd492f4e8b3fb87e3d9fa1efebaec43ed`,
  совпадает с release page Python.org.
  `pkgutil --check-signature /private/tmp/tamarix-python-3.15.0-macos11.pkg`
  вне sandbox: exit 0, подпись Python Software Foundation и trusted Apple notarization.
- Системная установка через `osascript` / `installer -target /`:
  exit 1, `Отменено пользователем. (-128)`.
  Установка не подтверждена; запрошен способ продолжения. Зависимые кодовые
  задачи и проверки не закрываются по наличию манифеста или принятого design.

### Завершение подготовки 3.1 — 2026-10-09

После ответа пользователя «Повторить системную установку» официальный installer
завершился с exit 0: `The install was successful`.
Интерпретатор: `/Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15`.
Ниже команды выполнены из `container-adm-api`, каждая с exit 0:

- `uv tool run --from uv==0.12.24 uv lock --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 7 пакетов разрешены, сохранён uv.lock.
- `uv tool run --from uv==0.12.24 uv lock --check --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — lock согласован.
- `uv tool run --from uv==0.12.24 uv sync --frozen --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — создана .venv, пакет и dev-зависимости установлены.
- `uv tool run --from uv==0.12.24 uv run --frozen --no-sync python --version` — Python 3.15.0.
- `uv tool run --from uv==0.12.24 uv run --frozen --no-sync python -m pytest --version` — pytest 9.1.1 доступен; это не запуск тестов требований.
- `uv tool run --from uv==0.12.24 uv build --no-sources` — wheel и sdist собраны.

Манифест, pin и lock сохранены; следующие задачи добавляют правила ядра и тесты.
Store pointer сохранён.

### Ядро контейнеров 3.2 — 2026-10-10

Revision: рабочие файлы `container-adm-api`, ветка `feature/t-1-container-definition`,
первого коммита ещё нет. Проверены сохранённые facts.py/ports.py/core.py, README
и оба тестовых файла. Реализованы 16 сочетаний parent/child, четыре типа корня,
пропуски, единственный родитель, структурные отношения и уникальные пути ключей.

Из `/Users/mfedotenko/Projects/Tamarix/container-adm-api`:
`uv tool run --from uv==0.12.24 uv run --frozen --no-sync python -m pytest -q`
— exit 0, **58 passed in 0.04s**.

Фактические тесты четырёх первых строк containers:
`tests/test_t1_tree.py::test_ordered_tree`,
`tests/test_t1_tree.py::test_skipped_levels_and_root`,
`tests/test_t1_keys.py::test_string_key`,
`tests/test_t1_keys.py::test_composite_key`.
Именованные параметры содержат точные названия Scenario; варианты матриц имеют
суффикс `::вариант`. Дополнительно проверены соседние ветки, неизвестные ссылки,
неизменяемость фактов и отсутствие строковых префиксов/разделителя wire-формата.

### Общий допуск 3.3 — 2026-10-10

Revision: рабочие файлы container-adm-api на feature/t-1-container-definition,
пока без коммита. Прочитаны сохранённые core/facts/ports и request-context tests.
ContainerAdmission разрешает отдельные C/O и признаёт владельца по проверенному
сертификатному факту и registered DN/O; дополнительная роль и O≼C в общем допуске
не проверяются. Документирована граница будущего PKI-адаптера.

Из container-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**80 passed in 0.04s**. `.venv/bin/python -m pytest --collect-only -q tests/test_t1_request_context.py`
— exit 0, **22 tests collected**, русские nodeIDs без экранирования.
Установленная .venv подготовлена в 3.1; запуск не использует защищённый uv cache.

Фактические функции planned trace: test_explicit_addressing,
test_certificate_binding и test_certificate_owner_sufficiency в
tests/test_t1_request_context.py. Каждый Scenario ID развёрнут для access-check
и management; отсутствие C/O имеет два случая, неразрешённые адреса и DN без
проверенного сертификатного факта проверены дополнительно.

### Полный путь 3.4 — 2026-10-10

Revision: рабочие файлы container-adm-api, feature/t-1-container-definition,
без коммита. CompletePath проверяет корень/конец, все parent-связи, порядок
типов и уникальность узлов; ContainerTree.path_to возвращает весь путь либо
UnknownPath. Неустановленный путь не подменяется пустым CompletePath.
Core/facts/ports, README и tests/test_t1_container_facts.py прочитаны после сохранения.

Из container-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**94 passed in 0.04s**; `.venv/bin/python -m pytest --collect-only -q tests/test_t1_container_facts.py`
— exit 0, **14 tests collected in 0.01s**.
Фактическая функция test_path_completeness содержит 12 именованных случаев:
полный путь/корень/пропуски/исключение ветки, неизвестный источник/R,
обрезанные концы, пропущенный родитель, чужая ветка, фиктивный уровень и пустой путь.
Ещё два теста проверяют неполное дерево и неизменяемость полного пути.
Команды и результаты всех задач 3.2–3.4 записаны выше.

### Подготовка 4.1 entity-subject-adm-api — 2026-10-10

Revision: рабочий каталог без собственной Git metadata; HEAD отсутствует.
Прочитаны manifest/pin/README/store pointer и smoke test; согласованные pins
совпадают с 3.1. Из /Users/mfedotenko/Projects/Tamarix/entity-subject-adm-api, exit 0:

- `uv tool run --from uv==0.12.24 uv lock --check --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 7 пакетов, lock согласован.
- `uv tool run --from uv==0.12.24 uv sync --frozen --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 6 установленных пакетов проверены.
- `.venv/bin/python --version` — Python 3.15.0.
- `.venv/bin/python -m pytest -q` — **1 passed in 0.01s**; фактический тест tests/test_package.py::test_installed_package.
- `uv tool run --from uv==0.12.24 uv build --no-sources` — wheel и sdist собраны.

Первый smoke-тест обнаружил пробел в отформатированном Requires-Python;
сравнение игнорирует этот пробел, повторный запуск успешен.
Store-only сохранён; предметные критерии ещё не проверены этими smoke-тестами.

### Держатели 4.2 entity-subject-adm-api — 2026-10-10

Revision: рабочий каталог без Git HEAD. Реализованы локальные факты, читающий
port и логическая операция get; сохранён исходный ref и единственный holder.
Сохранённые core/facts/ports и все holder tests прочитаны при review.

Из entity-subject-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**10 passed in 0.02s** (9 domain + 1 packaging).
`.venv/bin/python -m pytest --collect-only -q tests/test_t1_subject_holders.py`
— exit 0, **9 tests collected**.
Фактические функции test_single_subject_holder / test_subject_holder_preservation; пять точных Scenario IDs из entity specs.
Ссылки одного/нескольких тестовых читающих потребителей сохраняют оригинального
держателя. Реальные model-операции связываются с этим контрактом в 8.1.
Отсутствующие обязательные факты дают отдельный отказ; форматы ID/lifecycle
и production-хранилище не выбраны.

### Управление 4.3 entity-subject-adm-api — 2026-10-10

Revision: рабочий каталог без Git HEAD. Прочитаны сохранённые core/facts/ports,
тесты управления и README. SubjectManagementService.update_content получает
admission, читает текущего держателя из собственной записи, проверяет оба
отношения O ≼ C ≼ D и кандидата до единственного save. Отказы не меняют состояние.
Метод обновляет содержимое; перенос держателя не определён этим контрактом.
Модели/PDP для управления не требуются.

Из entity-subject-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**32 passed in 0.03s**. `.venv/bin/python -m pytest --collect-only -q tests/test_t1_management.py`
— exit 0, **22 tests collected**. Все применимые ADM Scenario IDs представлены;
поддерево проверено для C=D и D-потомка C. Дополнительно проверены отсутствие
допуска, неизвестные отношения, обязательные факты и подмена держателя входом.

### Подготовка 5.1 entity-object-adm-api — 2026-10-10

Revision: рабочий каталог без собственной Git metadata; HEAD отсутствует.
Прочитаны manifest/pin/README/store pointer и smoke test; согласованные pins
совпадают с 3.1. Из /Users/mfedotenko/Projects/Tamarix/entity-object-adm-api, exit 0:

- `uv tool run --from uv==0.12.24 uv lock --check --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 7 пакетов, lock согласован.
- `uv tool run --from uv==0.12.24 uv sync --frozen --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 6 установленных пакетов проверены.
- `.venv/bin/python --version` — Python 3.15.0.
- `.venv/bin/python -m pytest -q` — **1 passed in 0.01s**; фактический тест tests/test_project.py::test_installed_package.
- `uv tool run --from uv==0.12.24 uv build --no-sources` — wheel и sdist собраны.


Store-only сохранён; предметные критерии ещё не проверены этими smoke-тестами.

### Держатели 5.2 entity-object-adm-api — 2026-10-10

Revision: рабочий каталог без Git HEAD. Реализованы локальные факты, читающий
port и логическая операция get; сохранён исходный ref и единственный holder.
Сохранённые core/facts/ports и все holder tests прочитаны при review.

Из entity-object-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**9 passed in 0.02s** (8 domain + 1 packaging).
`.venv/bin/python -m pytest --collect-only -q tests/test_t1_object_holders.py`
— exit 0, **8 tests collected**.
Фактические функции test_single_object_holder / test_object_holder_preservation; пять точных Scenario IDs из entity specs.
Ссылки одного/нескольких тестовых читающих потребителей сохраняют оригинального
держателя. Реальные model-операции связываются с этим контрактом в 8.1.
Отсутствующие обязательные факты дают отдельный отказ; форматы ID/lifecycle
и production-хранилище не выбраны.

### Управление 5.3 entity-object-adm-api — 2026-10-10

Revision: рабочий каталог без Git HEAD. Прочитаны сохранённые core/ports,
тесты управления и README. ObjectManagementService.update_content получает
admission, устанавливает текущего держателя через собственный repository.get,
проверяет O ≼ C ≼ D и кандидата до единственного save. Отказы не меняют состояние.
Метод обновляет содержимое; перенос держателя не определён этим контрактом.
Модели/PDP для управления не требуются.

Из entity-object-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**28 passed in 0.03s**. `.venv/bin/python -m pytest --collect-only -q tests/test_t1_management.py`
— exit 0, **19 tests collected**. Все десять применимых ADM Scenario IDs представлены;
поддерево проверено для C=D и D-потомка C. Дополнительно проверены отсутствие
допуска, неизвестные отношения, обязательные факты и подмена держателя входом.

### Среда 6.1 policy-adm-api — 2026-10-10

Revision: рабочий каталог без Git HEAD. Manifest, Python pin, store pointer,
README и smoke test прочитаны; согласованные pins совпадают с 3.1.
Из /Users/mfedotenko/Projects/Tamarix/policy-adm-api, exit 0:

- `uv tool run --from uv==0.12.24 uv lock --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 7 пакетов.
- `uv tool run --from uv==0.12.24 uv lock --check --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — lock согласован.
- `uv tool run --from uv==0.12.24 uv sync --frozen --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 6 пакетов установлены.
- `uv tool run --from uv==0.12.24 uv build --no-sources` — wheel и sdist собраны.
- `.venv/bin/python -m pytest -q` — **1 passed in 0.01s**, tests/test_package.py::test_installed_package.

Store-only сохранён; smoke test отдельно от предметных критериев.

### Держатели и полнота моделей 6.2 — 2026-10-10

Revision: policy-adm-api, рабочий каталог без Git HEAD. Сохранённые факты,
порты, core, два test-файла и README прочитаны при review.
ModelFacts требует единственного держателя; допускаются 0/1/несколько моделей.
ModelFactsService различает подтверждённые списки каждого контейнера и unknown.
Полный набор проверяет точное покрытие, держателя и повтор модели до индексации.
Отсутствующий/частичный/неподтверждённый список не становится пустым.

Из policy-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**22 passed in 0.02s**. `.venv/bin/python -m pytest --collect-only -q tests/test_t1_models.py tests/test_t1_model_facts.py`
— exit 0, **21 tests collected**. Фактические функции test_single_model_holder,
test_optional_models, test_model_set_completeness; пять точных Scenario IDs,
варианты 0/1/3 и отдельные отрицательные проверки полноты.
Полнота/актуальность production-источника этим evidence не доказывается.

### Статические ссылки моделей 6.3 — 2026-10-10

Revision: policy-adm-api, рабочий каталог без Git HEAD. Сохранённые факты,
порты, ModelReferenceChecker, tests и README прочитаны при review.
Проверяются H(S) ≼ M и M ≼ H(Q) по читающим entity-портам и структурному
отношению; неизвестные факты/отношения отклоняют ссылку. Ссылки сохраняют
исходные refs и держателей; интерфейс записи entity-сервисов не предоставляется.

Из policy-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**39 passed in 0.03s**. `.venv/bin/python -m pytest --collect-only -q tests/test_t1_model_references.py`
— exit 0, **17 tests collected**. test_subject_scope / test_object_scope
покрывают все шесть точных Scenario IDs и варианты сам/предок/потомок/сосед/пропуски.
Дополнительно проверены missing facts, unknown relation, факты иной сущности
и сохранение держателей при нескольких моделях.

### Управление моделями 6.4 — 2026-10-10

Revision: policy-adm-api, рабочий каталог без Git HEAD. Сохранённые core,
порты, facts, management tests и README прочитаны при review.
ModelManagementService.update_model читает текущий D из собственной записи;
admission, O ≼ C ≼ D, holder и проверка всех ссылок предшествуют save.
Существующие ссылки проверяются и при обновлении только content.
Отказы не меняют модель/сущности; PDP, число моделей и дополнительная роль не нужны.
Метод сохраняет holder; создание/удаление/перенос не определены этим контрактом.

Из policy-adm-api: `.venv/bin/python -m pytest -q` — exit 0,
**68 passed in 0.05s**, повторено после уточнения ADM* WHEN до O=C=D.
`.venv/bin/python -m pytest --collect-only -q tests/test_t1_management.py`
— exit 0, **29 tests collected**. Все ADM и ADM* Scenario IDs фактические;
недопустимые субъект-сосед и объект-предок проверены отдельно при полном праве
владельца держателя модели. Поддерево — C=D и D-потомок C; остальные проверки
охватывают admission, authoritative facts, неизвестные отношения и сохранение состояния.

### Среда 7.1 policy-decision-api — 2026-10-10

Revision: рабочий каталог без Git HEAD. Manifest, Python pin, store pointer,
README, ignore-файл и smoke test прочитаны; согласованные pins совпадают с 3.1.
Из /Users/mfedotenko/Projects/Tamarix/policy-decision-api, exit 0:

- `uv tool run --from uv==0.12.24 uv lock --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 7 пакетов.
- `uv tool run --from uv==0.12.24 uv lock --check --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — lock согласован.
- `uv tool run --from uv==0.12.24 uv sync --frozen --python /Library/Frameworks/Python.framework/Versions/3.15/bin/python3.15` — 6 пакетов установлены.
- `uv tool run --from uv==0.12.24 uv build --no-sources` — wheel и sdist собраны.
- `.venv/bin/python -m pytest -q` — **1 passed in 0.01s**, tests/test_package.py::test_installed_package.

Store-only сохранён; smoke test отдельно от предметных критериев.

### Выполнение 7.2 — 2026-10-10

Ревизия: рабочие файлы без commit; каталог запуска `/Users/mfedotenko/Projects/Tamarix/policy-decision-api`.
Созданы локальные RuleEffect/ModelOutcome и aggregate_rules для полного определённого набора подходящих эффектов; файлы и README перечитаны.
`.venv/bin/python -m pytest -q` — exit 0, **10 passed in 0.01s**.
`.venv/bin/python -m pytest --collect-only -q tests/test_t1_rule_aggregation.py` — exit 0, **9 tests collected in 0.00s**.
Фактические IDs: test_rule_aggregation[Разрешение и запрет внутри одной модели::{allow-first,deny-first}], test_rule_aggregation[Подходят только разрешения::{одно,несколько}], test_rule_aggregation[Подходящих правил нет]; test_rule_aggregation_nonmatching_deny[Запрет не подходит запросу::{subject,object,action}]. Отдельная проверка отклоняет Undefined как определённый эффект правила; обработка ошибки отдельного правила не выбиралась.

### Выполнение 7.3 — 2026-10-10

Ревизия: рабочие файлы без commit; каталог `/Users/mfedotenko/Projects/Tamarix/policy-decision-api`.
Реализован aggregate_models; все изменённые файлы/README перечитаны. `.venv/bin/python -m pytest -q` — exit 0, **22 passed in 0.02s**.
`.venv/bin/python -m pytest --collect-only -q tests/test_t1_chain_aggregation.py` — exit 0, **12 tests collected in 0.00s**.
Фактические функции test_chain_aggregation (3 точных Scenario, варианты положения Deny и количества Allow), test_default_deny (4 точных Scenario), test_first_allow_does_not_skip_remaining_model_results и test_missing_result_is_not_neutral_or_undefined. Neutral/Undefined различимы; первый Allow не скрывает последующий Deny; отсутствующий результат отклоняется.

### Выполнение 7.4 — 2026-10-10

Ревизия: рабочие файлы без commit; каталог `/Users/mfedotenko/Projects/Tamarix/policy-decision-api`.
Локальные факты/Protocol/evaluate_model и README перечитаны. `.venv/bin/python -m pytest -q` — exit 0, **39 passed in 0.02s**.
`.venv/bin/python -m pytest --collect-only -q tests/test_t1_model_evaluation.py` — exit 0, **17 tests collected in 0.00s**.
Фактические test_model_subject_scope/test_undefined_model имеют все 6 точных Scenario IDs. Дополнительно проверены четыре явных исхода при H(S)=M и H(S)≺M, неприсвоение Undefined недоступному отношению дерева и отсутствие broad catch. Вне области вычислитель не вызывается; declared calculation/data failures известной модели дают Undefined. Критерии итогового объединения проверены готовым оператором 7.3; полный request/chain flow остаётся 7.6.

### Выполнение 7.5 — 2026-10-10

Ревизия: рабочие файлы без commit; каталог `/Users/mfedotenko/Projects/Tamarix/policy-decision-api`.
AccessRequest/AccessInputService, локальные факты/Protocol, support fixtures, тесты и README перечитаны. `.venv/bin/python -m pytest -q` — exit 0, **60 passed in 0.04s**.
`.venv/bin/python -m pytest --collect-only -q tests/test_t1_access_check.py` — exit 0, **21 tests collected in 0.01s**.
Фактические test_separate_subject/test_object_address_scope/test_no_global_subject_binding покрывают входную часть 10 Scenario, с отдельными вариантами отсутствующего объекта/действия и адресации к потомку/соседу. Дополнительно проверены mandatory entity result/exception, несоответствующий объект, kind допуска, C/O и certificate binding. DN/владелец не подменяют ключ S; только C≼R. Критерии итогового Allow/Deny этих случаев ещё не завершены и остаются в 7.6 вместе с owner_does_not_grant_subject_access.

### Выполнение 7.6 — 2026-10-10

Ревизия: рабочие файлы без commit; каталог `/Users/mfedotenko/Projects/Tamarix/policy-decision-api`.
AccessCheckService и локальные CompletePath/CompleteModelSet/unknown состояния реализованы, все изменённые source/tests/README полностью перечитаны.
Первый прогон: `.venv/bin/python -m pytest -q` — exit 0, **93 passed in 0.06s**. Затем добавлены 4 проверки нового полного потока для known model calculation/data failure/Undefined и отсутствующего результата.
Финальный прогон той же команды — exit 0, **97 passed in 0.05s**.
`.venv/bin/python -m pytest --collect-only -q` — exit 0, **97 tests collected in 0.01s**, literal Unicode IDs. Автоматическая read-only сверка 39 точных Scenario из authorization/access-check с collected IDs (точное имя либо имя::вариант) показала **39/39, missing=0**; это сверка идентификаторов, семантические THEN проверены соответствующими assertions.
Фактические дополнительные функции test_separate_subject_full_flow[Аутентифицированный вызывающий передаёт субъект], test_no_global_subject_binding_full_flow[Держатель субъекта является потомком адресата / Субъект из другой ветки] и test_owner_does_not_grant_subject_access[оба точных Scenario] завершают итоговые критерии 7.5. Evaluator получает исходные S/Q/action, при H(S)=R получается Allow только от in-scope модели; субъект другой ветки не отклоняется как запрос, модели вне его области нейтральны.
В test_t1_chain.py test_full_model_chain проверяет все 7 Scenario; test_unknown_chain_denies — 3 Scenario с двумя вариантами доступного Allow при неизвестном пути/моделях. Дополнительно проверены declared supplier exceptions, точное покрытие пути, duplicate/mismatched holder до схлопывания, invalid claim, immutable DTO и полный поток known Undefined с Allow/Deny.
Оба подтверждения состава получаются до evaluate. Unknown/invalid состав даёт EvaluatedDecision(Deny), обязательные entity/relations failures остаются отдельным RequiredFactsUnavailable. CS доказывает реальные parent-связи, consumer DTO проверяет форму и согласованность запроса; production-доверие/свежесть этими тестами не заявлены. Runtime API/PKI/storage и rule-error semantics не добавлялись; группа 8 остаётся открытой.

### Исправление входа после независимого review 7.5 — 2026-10-10

Hashable ABC недостаточен для кортежа с вложенным списком. AccessInputService
проверяет фактический hash ключа до admission/entity-read; TypeError этого
входа даёт AccessCheckRejected. Формат wire-ключа этим не выбирается.
Добавлен test_t1_access_check.py::test_nested_unhashable_subject_key_is_rejected_before_admission;
он проверяет отказ и отсутствие всех downstream-вызовов. Код/тест/README прочитаны.

Из policy-decision-api: `.venv/bin/python -m pytest -q tests/test_t1_access_check.py`
— exit 0, **28 passed in 0.03s**. `.venv/bin/python -m pytest -q`
— exit 0, **110 passed in 0.07s**, включая уже сохранённые 12 сквозных тестов 8.1.
7.5 временно открывалась при обнаружении дефекта и повторно закрыта после исправления.

### Сквозные логические контракты 8.1 — 2026-10-10

Сохранённые контрактные тесты/адаптеры и README обоих репозиториев прочитаны.
Реальные ContainerTree/ContainerAdmission, SubjectService, ObjectFactsService,
ModelReferenceChecker/ModelManagementService/ModelFactsService и AccessCheckService
соединены преобразованием локальных DTO исключительно в тестах. Источник моделей
общий для логической записи и models_for; evaluator вызывает реальный оператор
подходящих эффектов. Символические источники не выбирают production-хранилище/PKI.

- Из policy-adm-api: `.venv/bin/python -m pytest -q` — exit 0, **72 passed in 0.06s**.
  `.venv/bin/python -m pytest --collect-only -q tests/contracts/test_t1_holder_links.py`
  — exit 0, **4 tests collected in 0.01s**.
  test_holder_preservation покрывает оба entity WHEN с одной/несколькими моделями
  других контейнеров; исходные записи, содержимое и держатели сохраняются.
- Из policy-decision-api после исправления 7.5: `.venv/bin/python -m pytest -q`
  — exit 0, **110 passed in 0.07s**.
  `.venv/bin/python -m pytest --collect-only -q tests/contracts`
  — exit 0, **12 tests collected in 0.02s**.
  test_cross_service_facts проверяет пропуски, соседние ветки, предков C и C=R,
  все модели контейнера, Neutral по области, known Undefined + Allow, отдельный
  O вне пути, отсутствие автоматического доступа владельца и unknown пути/списка
  при доступном Allow. При unknown evaluator не вызывается.

Revision: текущие рабочие каталоги без Git HEAD. Транспорт, доверие реальных
сертификатов, свежесть источников и конкурентная атомарность не подтверждаются
этими тестами; они требуют последующих runtime-контрактов и проверок.


### Итоговая сверка 8.2 — 2026-10-10

- Четыре актуальных delta specs: **29 Requirement / 91 Scenario**.
  Все сценарии связаны с фактическими pytest node IDs; ADM развёрнут в каждый
  из трёх административных сервисов, ADM* проверен по назначению случая.
  Пропущенных обязательных связей нет. Таблицы теперь содержат реальные функции,
  включая nonmatching deny, полные потоки и сквозные контракты.
- В каждом рабочем каталоге выполнены `.venv/bin/python -m pytest -q`
  и `.venv/bin/python -m pytest --collect-only -q`: оба exit 0.
  Итоговая матрица:

| Проект | Результат полного запуска | Собрано случаев |
| --- | --- | --- |
| container-adm-api | 94 passed in 0.04s | 94 |
| entity-subject-adm-api | 32 passed in 0.03s | 32 |
| entity-object-adm-api | 28 passed in 0.03s | 28 |
| policy-adm-api | 72 passed in 0.06s | 72 |
| policy-decision-api | 110 passed in 0.08s | 110 |
| Всего | **336 passed**, без failed/skipped | **336** |

- Среди них 16 сквозных случаев: 4 сохранения держателей и 12 вычисления доступа.
  Проверка вложенного нехешируемого ключа субъекта включена в итоговый запуск.
- Во всех пяти проектах `uv tool run --from uv==0.12.24 uv lock --check`
  и `uv tool run --from uv==0.12.24 uv build --no-sources`: exit 0;
  собраны wheel и sdist текущих исходников. Python/pytest фактически 3.15.0/9.1.1;
  manifest, pin, lock и store pointer согласованы, prerelease запрещён.
- `test-evidence.json` содержит команды и результаты, полный test inventory,
  связи каждого Requirement/Scenario и SHA-256 проверенных файлов/сборок.
  Revision — снимки рабочих каталогов; результаты не приписаны commit HEAD.
  Повторная сверка файлов и артефактов: изменений относительно снимка нет;
  функции из inventory существуют, состав сценариев точно совпадает с delta specs.
- `openspec validate t-1-container-definition --strict --json --store tamarix-specs`:
  exit 0, valid true, issues [].
  `git diff --check -- openspec/context openspec/changes/t-1-container-definition`:
  exit 0. Все 198 локальных Markdown targets context/change существуют.
  AST статических импортов src показывает отсутствие runtime-импортов соседних сервисов.
- Независимый read-only review сопоставил WHEN/THEN всех 29 требований / 91 сценария
  с содержательными assertions тестов; проверил документацию и границы готовности.
  Конкретных несоответствий не выявлено; результат записан в test-evidence.json.
- Context, proposal/design, документы среды/контрактов обновлены до фактического
  состояния. Датированные первоначальные срезы, неуспешная первая установка
  и промежуточные результаты сохранены как история; итоговый набор проверок
  не содержит недоступных или неуспешных команд.
- Готовность относится к согласованному логическому scope: дерево/ключи/допуск,
  держатели и области управления, ссылки моделей, полный состав цепочки,
  оба оператора и проверка переданного субъекта. Production API/PKI,
  реальные источники и хранение, актуальность и конкурентная атомарность,
  движки и ошибки отдельных правил, deployment требуют отдельных изменений.
  Все DDL/Alembic остаются в db-control; access-assignment-api не затрагивался.
  Основные specs ещё не синхронизированы; archive и commit этим шагом не выполнялись.



