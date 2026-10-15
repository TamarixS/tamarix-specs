# Verification — t-3-persistent

**Черновик; foundation change ещё не подтверждён полным integration/promotion evidence.**

Срез данных: `2026-10-15T14:06:15.595729+00:00`. Этот документ и [evidence.json](evidence.json) не являются gate-generated archive evidence. `tasks.md` этой подготовкой не изменён.

## Проверяемая граница

T-3 foundation охватывает PostgreSQL persistence контейнеров, субъектов, объектов, metadata моделей и типизированных attributes, закрытые роли/routines/views, aggregate CAS, lifecycle и подготовленный согласованный read snapshot. Модели здесь содержат id/holder/key/revision/attrs.

В следующий отдельный change перенесены privileges/actions, внутренняя модель, физические ссылки и их cleanup, revision затронутых моделей и полная транзакционность будущих ссылок, полноценные persistent CompleteModelSet/evaluator/access decisions. Пустые ссылки или metadata не подтверждают эти отложенные требования. Установленный VerifiedCertificateFact не является реализацией TLS/PKI или business HTTP e2e.

## Реестр и обязательный набор

Фактически прочитан [registry.yaml](/Users/mfedotenko/Projects/TamarixS/TamarixTests/registry.yaml); SHA256 `fe89d5d68db21b0d7dc0f72d97d5c0325a5f2aac3781585c2156be8fee1d9551`. Найдено **81** T-3 cases, все в состоянии **candidate**, и **20** прежних regression cases. Полный набор `--change t-3-persistent` сейчас содержит **101** обязательных IDs.

| Группа | Новые ID | Количество | Исходник |
| --- | --- | --- | --- |
| persistent-containers | c01–c30 | 30 | [test_containers.py](/Users/mfedotenko/Projects/TamarixS/TamarixTests/tests/integration/persistence/test_containers.py) |
| persistent-subjects | c01–c12 | 12 | [test_subjects.py](/Users/mfedotenko/Projects/TamarixS/TamarixTests/tests/integration/persistence/test_subjects.py) |
| persistent-objects | c01–c08 | 8 | [test_objects.py](/Users/mfedotenko/Projects/TamarixS/TamarixTests/tests/integration/persistence/test_objects.py) |
| persistent-attributes | c01–c20 | 20 | [test_attributes.py](/Users/mfedotenko/Projects/TamarixS/TamarixTests/tests/integration/persistence/test_attributes.py) |
| persistent-models | c01–c06 | 6 | [test_models.py](/Users/mfedotenko/Projects/TamarixS/TamarixTests/tests/integration/persistence/test_models.py) |
| persistent-facts | c01–c05 | 5 | [test_fact_views.py](/Users/mfedotenko/Projects/TamarixS/TamarixTests/tests/integration/persistence/test_fact_views.py) |

Все 81 точных ID/node ID сохранены в `registry_snapshot.cases` evidence.json; criterion links/русские descriptions — в указанном registry. Наличие записей и source AST не является успешной collection или выполнением тестов. Финальный collected/executed набор ожидает root report.

## Существующие локальные отчёты

Ниже записан фактический PASS соответствующих запусков unit/component/contract wrapper. Они не суммируются как один набор: focused suites могут пересекаться с полными. Wrapper сохраняет версии пакетов, но не связывает эти прогоны с Git commit/source hashes; они не подтверждают неизменённость последующего final checkout и не заменяют source-pinned integration report.

| Проверка | Run ID | PASS | JSON / русская сводка |
| --- | --- | --- | --- |
| db-control contracts | `25e087ccba9345d5a7aaaeb38f8e7c15` | 93/93 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/25e087ccba9345d5a7aaaeb38f8e7c15/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/25e087ccba9345d5a7aaaeb38f8e7c15/summary.md) |
| db-control deployment/reporting | `bac7a377a28d49f0af97a3f4e3433fc9` | 15/15 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/bac7a377a28d49f0af97a3f4e3433fc9/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/bac7a377a28d49f0af97a3f4e3433fc9/summary.md) |
| db-control deployment CLI | `0b91fc8f0deb4d16a32608c4bb8bf94a` | 11/11 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/0b91fc8f0deb4d16a32608c4bb8bf94a/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/0b91fc8f0deb4d16a32608c4bb8bf94a/summary.md) |
| db-control constraints/concurrency/migrations | `833dd42b57d742f4af5a16cfc36696a1` | 76/76 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/component/833dd42b57d742f4af5a16cfc36696a1/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/component/833dd42b57d742f4af5a16cfc36696a1/summary.md) |
| db-control DN codec | `c3ce7f52b1c14421b6173afd64dfe6e8` | 88/88 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/component/c3ce7f52b1c14421b6173afd64dfe6e8/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/component/c3ce7f52b1c14421b6173afd64dfe6e8/summary.md) |
| db-control bootstrap/roles | `7ccc754d4e474b11989f4a3f33b66b40` | 25/25 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/7ccc754d4e474b11989f4a3f33b66b40/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/7ccc754d4e474b11989f4a3f33b66b40/summary.md) |
| container-adm-api full local suite | `9d1c7c569872462e8750043ddcdc7c7a` | 182/182 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/container-adm-api/reports/9d1c7c569872462e8750043ddcdc7c7a/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/container-adm-api/reports/9d1c7c569872462e8750043ddcdc7c7a/summary.md) |
| entity-subject-adm-api full local suite | `9f7f612b59b5445dada40fd5c612da81` | 107/107 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/entity-subject-adm-api/reports/9f7f612b59b5445dada40fd5c612da81/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/entity-subject-adm-api/reports/9f7f612b59b5445dada40fd5c612da81/summary.md) |
| entity-object-adm-api full local suite | `52d13d42542645599b8afe085d389c47` | 104/104 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/entity-object-adm-api/reports/52d13d42542645599b8afe085d389c47/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/entity-object-adm-api/reports/52d13d42542645599b8afe085d389c47/summary.md) |
| policy-adm-api full local suite | `bb9fe3fde2824f8f8be8bcb8a706f7a6` | 150/150 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/policy-adm-api/reports/bb9fe3fde2824f8f8be8bcb8a706f7a6/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/policy-adm-api/reports/bb9fe3fde2824f8f8be8bcb8a706f7a6/summary.md) |
| policy-decision-api full local suite | `a161d6a6c6ee4b2b9fc1f3a8b1656960` | 139/139 | [JSON](/Users/mfedotenko/Projects/TamarixS/Tamarix/policy-decision-api/reports/a161d6a6c6ee4b2b9fc1f3a8b1656960/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/Tamarix/policy-decision-api/reports/a161d6a6c6ee4b2b9fc1f3a8b1656960/summary.md) |
| TamarixTests runner unit suite | `1b5b67967994482c862b2ae15ac526b8` | 79/79 | [JSON](/Users/mfedotenko/Projects/TamarixS/TamarixTests/reports/1b5b67967994482c862b2ae15ac526b8/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/TamarixTests/reports/1b5b67967994482c862b2ae15ac526b8/summary.md) |
| TamarixTests PostgreSQL environment component | `dc0d8a6c50914a7bbb0445f6a4b802e8` | 4/4 | [JSON](/Users/mfedotenko/Projects/TamarixS/TamarixTests/reports/dc0d8a6c50914a7bbb0445f6a4b802e8/results.json) · [сводка](/Users/mfedotenko/Projects/TamarixS/TamarixTests/reports/dc0d8a6c50914a7bbb0445f6a4b802e8/summary.md) |

JSON содержит пути/hash каждого report/summary/log/JUnit, точные selectors, timestamps и версии. Ранние FAIL/незавершённые локальные отчёты сохранены отдельно в `retained_nonpassing_local_reports`; наличие более позднего PASS не переписывает их историю. Два ранних constraints прогона имели узкие ожидания GeneratedAlways/RestrictViolation, исправленные в assertions; общий перечень старых failures не объявляется разбором всех их причин.

## Что пока не подтверждено

- Полный source-pinned integration PASS для текущих 81 + 20 cases: **ожидается root report**.
- Promotion candidate → regression и окончательный tests commit: **не зафиксированы этим evidence**.
- Новый полный прогон окончательного promotion commit: **ожидается**.
- Успешный `archive_gate.py check` и archive: **не выполнялись этой подготовкой**.

Наблюдаемые HEAD/dirty flags в evidence — только срез checkout, не tested revisions. Финальный manifest должен предоставить commits/hashes пяти services, db-control Python/SQL/resources и migration fingerprint, Tests/store/CD, PostgreSQL image/ownership/version/Unicode/comparison profiles и Alembic heads. Никакие DSN/password/certificate secrets сюда не включены.

## Фактический контракт gate

Прочитаны [archive_gate.py](/Users/mfedotenko/Projects/TamarixS/Tamarix/tamarix-specs/tools/archive_gate.py), [ARCHIVE_GATE.md](/Users/mfedotenko/Projects/TamarixS/Tamarix/tamarix-specs/tools/ARCHIVE_GATE.md), [runner.py](/Users/mfedotenko/Projects/TamarixS/TamarixTests/src/tamarix_tests/runner.py) и [promotion CLI](/Users/mfedotenko/Projects/TamarixS/TamarixTests/src/tamarix_tests/cli.py); hashes находятся в evidence.

`archive_gate.py check` не читает этот verification.md или evidence.json. Он требует `results.json` schema_version=1, complete=true/PASS, пустые errors и timestamps/run ID; вложенный manifest schema_version=1 с SHA256 сохранённого manifest.json; точное совпадение registry hash, descriptions, IDs/node IDs и requested/collected/executed наборов; весь ожидаемый набор без диагностического ids/level фильтра и без skip/NOT_RUN; русскую summary.md и hashes всех заявленных artifacts.

Для T-3 cases gate требует уже regression state. Он сверяет HEAD/чистоту Tests/CD/services, source hashes при наличии, store ancestry и неизменность specs/deltas, полное покрытие criterion links и русские source docstrings. PostgreSQL scope, фактический Docker/DB probe и отдельный db-control artifact/resource fingerprint проверяет `validate_manifest` runner; это отдельная проверка от базовых полей manifest в archive gate.

`archive` дополнительно требует завершения всех tasks и только после check создаёт run-results.json/run-manifest.json/run-summary.md/regression-registry.yaml и **regression-evidence.json**. Последний имеет поля schema_version, operation_id, change, run_id, report_sha256, registry_sha256, tested_store_commit. Затем запускается OpenSpec archive. `validate-archives` проверяет уже сохранённые snapshots/hashes/критерии/merge и не запускает тесты.

## Команды для последующего явного выполнения

Значения `TAMARIX_CANDIDATE_MANIFEST`, `TAMARIX_CANDIDATE_REPORT`, `TAMARIX_FINAL_MANIFEST`, `TAMARIX_FINAL_REPORT`, `TAMARIX_ARCHIVE_OPERATION` и `TAMARIX_ARCHIVE_BASE` ещё должен предоставить root. Блоки ниже документируют интерфейс; этой подготовкой команды не выполнялись.

Из TamarixTests:

```sh
.venv/bin/python -m tamarix_tests run --store ../Tamarix/tamarix-specs --manifest "$TAMARIX_CANDIDATE_MANIFEST" --change t-3-persistent --output-dir reports --junit
.venv/bin/python -m tamarix_tests promote --store ../Tamarix/tamarix-specs --change t-3-persistent --report "$TAMARIX_CANDIDATE_REPORT"
# После отдельной фиксации promotion commit и подготовки нового manifest:
.venv/bin/python -m tamarix_tests run --store ../Tamarix/tamarix-specs --manifest "$TAMARIX_FINAL_MANIFEST" --change t-3-persistent --output-dir reports --junit
```

Из tamarix-specs:

```sh
../../TamarixTests/.venv/bin/python tools/archive_gate.py check --tests ../../TamarixTests --change t-3-persistent --report "$TAMARIX_FINAL_REPORT"
# Только отдельным действием после завершения tasks и успешного check:
../../TamarixTests/.venv/bin/python tools/archive_gate.py archive --tests ../../TamarixTests --change t-3-persistent --report "$TAMARIX_FINAL_REPORT" --operation-id "$TAMARIX_ARCHIVE_OPERATION"
../../TamarixTests/.venv/bin/python tools/archive_gate.py validate-archives --base "$TAMARIX_ARCHIVE_BASE"
```

Старый candidate report после promotion не годится: registry hash меняется. Поэтому итоговый gate check должен использовать новый полный отчёт с окончательными revisions и promoted registry.
