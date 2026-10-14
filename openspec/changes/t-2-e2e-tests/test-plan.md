# Test plan: t-2-e2e-tests

Начальный набор содержит 20 самостоятельных integration случаев с постоянными
pytest node ID и стабильными test ID в `TamarixTests/registry.yaml`. Это явное
добавление регрессионных проверок выбранных действующих критериев T-1, без
изменения предметной семантики и исторических архивов. Набор не заявляет
полноту покрытия всех исторических сценариев; остальные требования продолжают
проверяться владельцами сервисных unit/component тестов.

## Scope и тестовые зависимости

Проверяемая граница — пять **установленных реальных Python-ядер**:
`container-adm-api`, `entity-subject-adm-api`, `entity-object-adm-api`,
`policy-adm-api`, `policy-decision-api` версии 0.1.0. Установка выполняется
через uv sources с `editable = false`, не через соседние `src` в sys.path.
Общий допуск, дерево/полнота пути, чтение фактов сущностей, проверка ссылок,
сохранение моделей, подтверждение полного состава и решение вызываются через
настоящие `core/facts/ports` этих пакетов.

`TamarixTests/fixtures/cross_service.py` содержит собственные тестовые
репозитории, DN/O привязки и явные DTO адаптеры. При подготовке каждая модель
проходит реальный `ModelManagementService.update_model` и reference checker;
для решения используются реальные `ModelFactsService` и `AccessCheckService`.
Контролируемый evaluator сообщает уже подходящие эффекты и объявленную ошибку
известной модели: язык политик и вычисление применимости правил не подменяются
заявлением об их production-проверке. Исходники сервисных tests не импортируются
и не распространяются; сторонний код в fixtures не включён.

Каждый параметризованный случай имеет русское пояснение условий, ожидаемого
результата и назначения рядом с параметрами. Все тестовые функции имеют русские
docstrings, те же описания сохраняются в registry и отображаются runner.

## Изоляция и manifest

Каждый случай создаёт новое дерево, новые repositories, адаптеры и снимок
entity-фактов. После выполнения проверяются исходные держатели и отсутствие
записей субъекта. Общее изменяемое состояние, сетевые адреса, файловые базы,
DDL и миграции не используются; очистка — освобождение объектов случая.
Manifest runner фиксирует commits установленных сервисных исходников, тестовой
репы, CD/store, spec hashes и уникальную изоляцию прогона. Scope указывать
`logical-integration`, endpoints/image digests/migrations — явные `null`.

## Traceability выбранных критериев

Названия Requirement/Scenario и критерии ниже взяты из действующих основных
specs целиком; ссылки разрешаются относительно центрального `tamarix-specs`.
Один node ID может проверять несколько критериев. Все исходники имеют level
`integration`, начальное состояние `candidate`, introduced_by `t-2-e2e-tests`.

| Spec | Requirement | Scenario | Наблюдаемый критерий | Test ID | Фактический node ID |
| --- | --- | --- | --- | --- | --- |
| `openspec/specs/authorization/access-check/spec.md` | Запрет по умолчанию | Пустая цепочка моделей | итог SHALL быть запретом по умолчанию | `access-empty-chain-denied` | `tests/integration/test_access_flow.py::test_access_decision[empty-chain-denied]` |
| `openspec/specs/authorization/access-check/spec.md` | Запрет по умолчанию | Все модели нейтральны | итог SHALL быть запретом по умолчанию | `access-neutral-chain-denied` | `tests/integration/test_access_flow.py::test_access_decision[neutral-chain-denied]` |
| `openspec/specs/authorization/access-check/spec.md` | Запрет по умолчанию | Все результаты неопределённы | итог SHALL быть запретом по умолчанию | `access-undefined-chain-denied` | `tests/integration/test_access_flow.py::test_access_decision[undefined-chain-denied]` |
| `openspec/specs/authorization/access-check/spec.md` | Приоритет запрета в цепочке моделей | Только разрешения и нейтральные результаты | итог SHALL быть разрешением | `access-allow-with-neutral-models` | `tests/integration/test_access_flow.py::test_access_decision[allow-with-neutral-models]` |
| `openspec/specs/authorization/access-check/spec.md` | Полная цепочка моделей до контейнера объекта | Запрет предка адресуемого контейнера | модель `root` SHALL участвовать в проверке, а итог SHALL быть запретом | `access-ancestor-deny-precedes-addressed` | `tests/integration/test_access_flow.py::test_access_decision[ancestor-deny-precedes-addressed]` |
| `openspec/specs/authorization/access-check/spec.md` | Полная цепочка моделей до контейнера объекта | Адресация непосредственно к контейнеру объекта | цепочка SHALL включать модель корня и модель `R`, а итог SHALL быть запретом | `access-direct-object-address-keeps-root-deny` | `tests/integration/test_access_flow.py::test_access_decision[direct-object-address-keeps-root-deny]` |
| `openspec/specs/authorization/access-check/spec.md` | Полная цепочка моделей до контейнера объекта | Несколько моделей одного контейнера | обе модели этого контейнера SHALL участвовать в проверке, а итог SHALL быть запретом | `access-all-models-of-container-evaluated` | `tests/integration/test_access_flow.py::test_access_decision[all-models-of-container-evaluated]` |
| `openspec/specs/authorization/access-check/spec.md` | Объединение подходящих правил модели | Разрешение и запрет внутри одной модели | результат модели SHALL быть запретом | `access-all-models-of-container-evaluated` | `tests/integration/test_access_flow.py::test_access_decision[all-models-of-container-evaluated]` |
| `openspec/specs/authorization/access-check/spec.md` | Отсутствие общей привязки субъекта к адресату | Держатель субъекта является потомком адресата | обращение SHALL быть допустимо, а итог проверки SHALL быть разрешением | `access-descendant-subject-neutralizes-ancestor-models` | `tests/integration/test_access_flow.py::test_access_decision[descendant-subject-neutralizes-ancestor-models]` |
| `openspec/specs/authorization/access-check/spec.md` | Нейтральность модели вне области субъекта | Другая модель разрешает доступ | итог проверки SHALL быть разрешением при отсутствии запретов других моделей | `access-descendant-subject-neutralizes-ancestor-models` | `tests/integration/test_access_flow.py::test_access_decision[descendant-subject-neutralizes-ancestor-models]` |
| `openspec/specs/authorization/access-check/spec.md` | Нейтральная трактовка неопределённого результата модели | Ошибка модели при известном разрешении | неопределённый результат SHALL считаться нейтральным, а итог SHALL быть разрешением | `access-known-model-error-keeps-allow` | `tests/integration/test_access_flow.py::test_access_decision[known-model-error-keeps-allow]` |
| `openspec/specs/authorization/access-check/spec.md` | Полная цепочка моделей до контейнера объекта | Пропущенные уровни дерева | цепочка SHALL включать модели обоих контейнеров без требования контейнеров `environment` и `system` | `access-skipped-levels-keep-real-path` | `tests/integration/test_access_flow.py::test_access_decision[skipped-levels-keep-real-path]` |
| `openspec/specs/authorization/access-check/spec.md` | Полная цепочка моделей до контейнера объекта | Соседняя ветка исключена | модели `X` SHALL не входить в цепочку проверки объекта `R` | `access-sibling-model-excluded` | `tests/integration/test_access_flow.py::test_access_decision[sibling-model-excluded]` |
| `openspec/specs/authorization/access-check/spec.md` | Адресация проверки относительно объекта | Представляемый контейнер вне пути объекта | положение `O` SHALL не нарушать условие адресации проверки; условие SHALL оцениваться по `C` | `access-represented-outside-object-path` | `tests/integration/test_access_flow.py::test_access_decision[represented-outside-object-path]` |
| `openspec/specs/authorization/access-check/spec.md` | Запрет при неизвестном составе цепочки | Неизвестен путь до контейнера объекта | результат проверки SHALL быть запретом | `access-unknown-path-denied-despite-allow` | `tests/integration/test_access_flow.py::test_access_decision[unknown-path-denied-despite-allow]` |
| `openspec/specs/authorization/access-check/spec.md` | Запрет при неизвестном составе цепочки | Известное разрешение при неизвестном составе цепочки | результат проверки SHALL быть запретом независимо от известного разрешения | `access-unknown-path-denied-despite-allow` | `tests/integration/test_access_flow.py::test_access_decision[unknown-path-denied-despite-allow]` |
| `openspec/specs/authorization/access-check/spec.md` | Запрет при неизвестном составе цепочки | Неизвестен полный набор моделей | результат проверки SHALL быть запретом; отсутствующий полный набор SHALL не подменяться пустым набором или нейтральными результатами | `access-unknown-model-set-denied-despite-allow` | `tests/integration/test_access_flow.py::test_access_decision[unknown-model-set-denied-despite-allow]` |
| `openspec/specs/authorization/access-check/spec.md` | Запрет при неизвестном составе цепочки | Известное разрешение при неизвестном составе цепочки | результат проверки SHALL быть запретом независимо от известного разрешения | `access-unknown-model-set-denied-despite-allow` | `tests/integration/test_access_flow.py::test_access_decision[unknown-model-set-denied-despite-allow]` |
| `openspec/specs/containers/spec.md` | Сертификатное подтверждение представляемого контейнера | Отсутствует успешная сертификатная аутентификация | оно SHALL не допускаться к выполнению запрошенной операции | `admission-unverified-certificate` | `tests/integration/test_access_flow.py::test_unconfirmed_caller_rejected[unverified-certificate]` |
| `openspec/specs/containers/spec.md` | Сертификатное подтверждение представляемого контейнера | DN приписан только к другому контейнеру | обращение SHALL быть отклонено; принадлежность DN к `Q` SHALL не подтверждать `O` | `admission-dn-bound-to-other-container` | `tests/integration/test_access_flow.py::test_unconfirmed_caller_rejected[dn-bound-to-other-container]` |
| `openspec/specs/entities/subjects/spec.md` | Сохранение держателя субъекта при использовании в модели | Модель потомка использует субъект предка | `C` SHALL оставаться единственным держателем субъекта, а `M` SHALL не становиться его держателем | `holder-subject-single-descendant-model` | `tests/integration/test_holder_preservation.py::test_model_references_keep_entity_holder[subject-single-descendant-model]` |
| `openspec/specs/entities/subjects/spec.md` | Сохранение держателя субъекта при использовании в модели | Несколько моделей других контейнеров | `C` SHALL оставаться единственным держателем субъекта независимо от количества и держателей использующих моделей | `holder-subject-multiple-descendant-models` | `tests/integration/test_holder_preservation.py::test_model_references_keep_entity_holder[subject-multiple-descendant-models]` |
| `openspec/specs/entities/objects/spec.md` | Сохранение держателя объекта при использовании в модели | Модель предка использует объект потомка | `C` SHALL оставаться единственным держателем объекта, а `M` SHALL не становиться его держателем | `holder-object-single-ancestor-model` | `tests/integration/test_holder_preservation.py::test_model_references_keep_entity_holder[object-single-ancestor-model]` |
| `openspec/specs/entities/objects/spec.md` | Сохранение держателя объекта при использовании в модели | Несколько моделей других контейнеров | `C` SHALL оставаться единственным держателем объекта независимо от количества и держателей использующих моделей | `holder-object-multiple-ancestor-models` | `tests/integration/test_holder_preservation.py::test_model_references_keep_entity_holder[object-multiple-ancestor-models]` |

## Запуск по требованию

Из `TamarixTests`, после `uv lock --check` и `uv sync --frozen`:

```bash
.venv/bin/python -m tamarix_tests run --store ../Tamarix/tamarix-specs --change t-2-e2e-tests --bootstrap-empty-regression --manifest /absolute/path/manifest.json --output-dir reports --junit
```

Команда соответствует реализованному CLI; окончательный полный прогон runner
фиксируется в verification/evidence после checkpoint commit. Runner сохраняет
отдельные `summary.md`, `results.json` и JUnit XML. Прямой pytest допускается
как диагностическая проверка реализации с сохранением результатов, но его
exit code/JUnit без полного отчёта, manifest и окончательного commit не
подтверждают допуск archive. Первый прежний регресс пустой — это явный bootstrap;
20 обязательных новых случаев должны существовать и пройти.

Promotion меняет только `candidate -> regression` для стабильных test ID;
исходники остаются на месте. После зафиксированного promotion нужен полный
успешный прогон окончательного tests commit. Этот test-plan и наличие candidate
тестов сами по себе не подтверждают promotion или готовность archive.

## Непроверенные HTTP e2e границы

Предметные бизнес HTTP endpoints, транспортные DTO, production PKI/проверка
сертификатов, хранилище PostgreSQL, миграции, конкурентное управление и язык
политик не реализуются и не подтверждаются этим набором. `/health` не заменяет
эти проверки. Полноценный бизнес e2e требует отдельных согласованных changes
API/adapters/PKI/storage и реальной среды с публичными контрактами. Каталог
`tests/e2e/` подготовлен, но предметных HTTP e2e тестов пока нет.

## Фактическая проверка начального набора

2026-10-14 на Python 3.15.0, pytest 9.1.1 и пяти установленных пакетах 0.1.0
выполнена диагностическая проверка `.venv/bin/python -m pytest tests/integration
-q --junitxml=reports/integration-seed-3ad24bf88cd447c6b78cd69c98d78808/junit.xml`
из `TamarixTests`: **20 passed in 0.04s**, без fail/error/skip/NOT_RUN.
Все 20 зарегистрированных параметризованных node ID получили PASS в JUnit.
Для этого прогона сохранены отдельные `summary.md`, `results.json`, `junit.xml`
и `pytest.log` в `TamarixTests/reports/integration-seed-3ad24bf88cd447c6b78cd69c98d78808/`.
Отчёт явно помечен диагностическим: он создан до окончательного tests commit
и manifest и не является evidence допуска archive.

Проверено, что импорты каждого ядра разрешаются из
`TamarixTests/.venv/lib/python3.15/site-packages/`, без добавления соседних src.
Реальные revisions исходников на момент установки и диагностического прогона:

| Пакет 0.1.0 | Commit исходника |
| --- | --- |
| container-adm-api | `b29e639c15892bfb3bb54330f530ef068de0b91e` |
| entity-subject-adm-api | `8706e2dde6944cdae1fd06a2784cb027540cae46` |
| entity-object-adm-api | `1707a6f470842646609ac86545a72f99f2ca741b` |
| policy-adm-api | `4230502fe1e068e08d3516ddfa85e2c6a3215d8c` |
| policy-decision-api | `e7a0409be87e2ba7a8a2a9fc1b869a858f84ab81` |

Русские docstrings, описания параметров и соответствующие registry description
проверены при реализации. Полный отчёт runner с manifest/revisions, promotion
и прогон окончательного commit отслеживаются отдельно в tasks/verification.
