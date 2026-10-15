# Verification — t-3-persistent

**Полный candidate: 101/101 PASS. Promotion выполнен. Окончательный post-promotion прогон и archive gate ещё ожидаются.**

## Граница foundation

Проверяется PostgreSQL persistence containers/subjects/objects/model metadata/attributes, реальные LOGIN и защищённые routines/views, CAS/atomic rollback, DN codec/admission, lifecycle и единый подготовленный snapshot. Модель содержит id/holder/key/revision/attrs. В следующий change перенесены privileges/actions, внутреннее хранение моделей/ссылок, cleanup непустых model refs с affected revisions и полный persistent PDP/CompleteModelSet/evaluator. Проверки этих отложенных частей не подменяются пустыми ссылками или metadata. TLS/PKI и business HTTP e2e здесь не заявлены.

## Полный source-pinned candidate

[Отчёт 101 PASS](/private/tmp/tamarix-t3-candidate-runs/ccdd327592a94abfa0bab75a9c7584df/reports/20261015T141541-f0b56743d607/results.json) · [русская сводка](/private/tmp/tamarix-t3-candidate-runs/ccdd327592a94abfa0bab75a9c7584df/reports/20261015T141541-f0b56743d607/summary.md) · [manifest](/private/tmp/tamarix-t3-candidate-runs/ccdd327592a94abfa0bab75a9c7584df/reports/20261015T141541-f0b56743d607/manifest.json).
Run ID `20261015T141541-f0b56743d607`, complete=true, FAIL/ERROR/SKIP/XFAIL/XPASS/NOT_RUN=0. Собраны и исполнены все 81 новых + 20 прежних stable IDs без диагностического фильтра. Manifest фиксирует чистые commits, Python/SQL/resources fingerprints, PostgreSQL 18.6/Unicode/comparison profiles и Alembic head `20261015_0003`; его полное содержимое и SHA256 сохранены в [evidence.json](evidence.json).

[Первый полный запуск: 100 PASS / 1 FAIL](/private/tmp/tamarix-t3-candidate-runs/e21827db1d8144199c050b2b02ce412b/reports/20261015T141230-7b0fac41087a/results.json) сохранён. Исправлено только ожидание тестом materialized containers: добавлен holder субъекта другого дерева. Runtime не менялся; полный повтор дал 101 PASS.

## Promotion и текущий реестр

[Promotion report](/private/tmp/tamarix-t3-promotion/b8056ba31b384298ab0ee85bb0945fa9/results.json) имеет PASS/complete=true: 81 candidate переведены в regression без перемещения исходников. Tests promotion commit: `85d5b492f18b30501c42ba0915251d3c22e00eff`. Сейчас [registry.yaml](/Users/mfedotenko/Projects/TamarixS/TamarixTests/registry.yaml) содержит 101 regression case; SHA256 `064e31fcf452a9a07f98fd57c02602fd22e1f4a6b32426d604874f9bfca609a3`. Все 81 новых ID/node ID и состояния перечислены в evidence; группы: containers30, subjects12, objects8, attributes20, models6, facts5.

CD change завершён 6/6; commit `1fa3c718bdbd29293eb4e7e4159ec83b653e42d7`. По handoff root центральные задачи завершены 52/54; этим обновлением tasks.md не менялся.

## Финальные локальные unit/component наборы

| Набор | PASS | Отчёт |
| --- | --- | --- |
| db-control full final local suite | 298 | [b17d2f5c6bff457490af16039b4128fc](/Users/mfedotenko/Projects/TamarixS/Tamarix/db-control/reports/b17d2f5c6bff457490af16039b4128fc/results.json) |
| Container full scope | 198 | [92c59e71154b4550924503ad47805ae5](/Users/mfedotenko/Projects/TamarixS/Tamarix/container-adm-api/reports/92c59e71154b4550924503ad47805ae5/results.json) |
| Subject full scope | 123 | [6a3f64e86aaa41829cc0a9d8ec9500dd](/Users/mfedotenko/Projects/TamarixS/Tamarix/entity-subject-adm-api/reports/6a3f64e86aaa41829cc0a9d8ec9500dd/results.json) |
| Object full scope | 116 | [6dd4064c6d5f48d2a6285fa624dcdb2a](/Users/mfedotenko/Projects/TamarixS/Tamarix/entity-object-adm-api/reports/6dd4064c6d5f48d2a6285fa624dcdb2a/results.json) |
| Policy full scope | 162 | [1f9504f20ccf4931824b118207628dd0](/Users/mfedotenko/Projects/TamarixS/Tamarix/policy-adm-api/reports/1f9504f20ccf4931824b118207628dd0/results.json) |
| PDP full local suite | 139 | [a161d6a6c6ee4b2b9fc1f3a8b1656960](/Users/mfedotenko/Projects/TamarixS/Tamarix/policy-decision-api/reports/a161d6a6c6ee4b2b9fc1f3a8b1656960/results.json) |
| TamarixTests unit/component | 83 | [10e1b3989c344ace84f9979577609f63](/Users/mfedotenko/Projects/TamarixS/TamarixTests/reports/10e1b3989c344ace84f9979577609f63/results.json) |
| CD tooling | 42 | [559ce1ed771e42f4aef864c381eb4baa](/private/tmp/tamarix-cd-test-runs/559ce1ed771e42f4aef864c381eb4baa/results.json) |

Четыре management scope suites дают 599 PASS (198+123+116+162), PDP — 139. JSON evidence хранит точные selectors, timestamps, версии и report/summary/log/JUnit hashes. Локальные wrapper reports сами не связывают source commits; immutable source binding полного candidate фиксирует отдельный manifest. Эти результаты не объявляются проверкой ещё не выполненного post-promotion commit.

## Оставшаяся проверка

Нужен новый полный run `--change t-3-persistent` с final manifest окончательного Tests promotion commit и нового store checkpoint; старый candidate report не подтверждает изменившийся registry hash. Final report и gate result пока null/NOT_RUN в evidence. Archive-ready=false.

Из TamarixTests после подготовки final manifest:

```sh
.venv/bin/python -m tamarix_tests run --store ../Tamarix/tamarix-specs --manifest "$TAMARIX_FINAL_MANIFEST" --change t-3-persistent --output-dir reports --junit
```

Затем из tamarix-specs:

```sh
../../TamarixTests/.venv/bin/python tools/archive_gate.py check --tests ../../TamarixTests --change t-3-persistent --report "$TAMARIX_FINAL_REPORT"
```

Gate не запускает тесты и не читает этот supplemental evidence.json: он проверяет финальные results/manifest/summary, hashes, весь набор, promoted registry, source revisions и criterion links. Только отдельная archive операция создаёт regression-evidence.json с schema_version/operation_id/change/run_id/report_sha256/registry_sha256/tested_store_commit. Подготовка документа не запускала tests, gate или archive.
