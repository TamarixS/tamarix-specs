# Tasks

Процесс принят пользователем 2026-10-14 и описан в
[design.md](design.md), [testing.md](../../context/testing.md) и
[ADR 0004](../../context/adr/0004-testing-regression-lifecycle.md).
Это tooling/docs change с `skip_specs: true`; предметных delta specs нет.
Выполненные документальные задачи не означают готовность тестовой репы/gate.

Все тесты проекта MUST иметь русские описания сценария/условий, ожидаемого
результата и назначения проверки. Для Python — docstring рядом с тестом,
с пояснениями параметризованных случаев; для TamarixTests также description
в registry/отчёте. Каждая задача создания/изменения тестов включает проверку
этих описаний. Недостающие описания прежних тестов остаются открытой работой.

Прогоны выполняются по требованию или уже согласованной задаче проверки,
с выбором и повтором набора без обязательного archive. Каждый прогон сохраняет
отдельную русскую сводку и JSON, включая неуспех/отмену; JUnit XML — для CI
по применимости. Archive gate потребляет отчёт, не запускает тесты неявно.

## 1. Правила и документальная проверка

- [x] 1.1 `tamarix-specs`: добавить testing.md, ADR 0004, ссылки в context/AGENTS и правила config для traceability, постоянных тестов и promotion; проверить наличие документов и сохранение прежних specs/архивов.
- [x] 1.2 `TamarixCD`: добавить координацию с TamarixTests в AGENTS/config с явным статусом будущего runner/gate; проверить, что CD source/tests и локальные changes не изменены.
- [x] 1.3 `tamarix-specs`: проверить change через `openspec validate t-2-e2e-tests --strict --store tamarix-specs`, передачу apply/archive guidance, Markdown-ссылки и `git diff --check`; записать фактические команды/результаты в [verification.md](verification.md), не объявлять runtime/e2e прогон выполненным.
- [x] 1.4 `tamarix-specs` + `TamarixCD`: добавить требование русских описаний всех тестов в AGENTS/config, testing.md и артефакты change; проверить передачу правила через instructions tasks/apply, strict validation и diff. Описания должны объяснять сценарий/условия, ожидаемый результат и назначение; существующие тесты этим документальным дополнением не исправлялись.
- [x] 1.5 `tamarix-specs` + `TamarixCD`: закрепить запуск по требованию и обязательную отчётность каждого прогона в инструкциях и плане; проверить instructions tasks/archive, strict validation и diff. Runner/reporting пока не реализованы; текущим дополнением тесты не запускались.

## 2. Тестовая репа и runner

- [x] 2.1 `TamarixTests`: создать локальную отдельную Git-репу с store pointer, постоянными integration/e2e каталогами, AGENTS, pyproject/uv.lock/.python-version и согласованными совместимыми pins; проверить `uv lock --check`, `uv sync --frozen` и разрешение store. Remote фиксировать по реальному размещению, не выдумывать URL.
- [x] 2.2 `TamarixTests`: реализовать registry/валидатор стабильных ID, русских description, состояний, links и точных node ID; добавить проверки отсутствующего/пустого описания, дубликата ID, пропавшего/параметризованного случая, некорректной ссылки и retirement без change; проверить их успешный прогон и понятные русские docstrings этих тестов, документировать формат.
- [x] 2.3 `TamarixTests`: реализовать запуск по требованию с выбором test ID/change/уровня/всего регресса, candidate текущего change и regression, коллекцией и результатом каждого обязательного случая; проверить выбор/повтор набора и регресс без активного change, PASS и отказ при нулевом обязательном наборе, missing/fail/skip/xfail, отдельно явный bootstrap пустого прежнего регресса; документировать реальные команды runner без незаказанных авто-триггеров.
- [x] 2.4 `TamarixTests`: реализовать отдельные summary.md на русском и results.json каждого прогона, при необходимости JUnit XML для CI, с описаниями случаев, набором, версиями, временем/длительностью, счётчиками, ошибками и артефактами; проверить отчёты успеха, fail/ошибки коллекции/среды, отмены и незавершённого снимка, различие NOT_RUN/SKIP и сохранение прежних отчётов при повторном запуске; документировать output-dir и форматы.

## 3. Начальный набор и контракт CD

- [x] 3.1 `tamarix-specs`: составить test-plan начального набора по действующим specs с точными Requirement/Scenario/критериями, test ID и планируемыми node ID; проверить, что in-memory интеграция обозначена как integration, а недоступные бизнес HTTP e2e не представлены выполненными. Исторические архивы не редактировать.
- [x] 3.2 `TamarixTests`: реализовать выбранные межсервисные integration случаи через установленные реальные пакеты и явные тестовые адаптеры с изоляцией данных; проверить русские docstrings/description и пояснения каждого параметризованного случая, собрать node ID, запустить случаи и заменить плановые ссылки фактическими в test-plan/registry с evidence версий. Не считать это подтверждением HTTP/PKI/storage.
- [x] 3.3 `tamarix-specs`: получить ссылку и evidence отдельного локального change TamarixCD, предоставляющего согласованные manifest/readiness и внешний прогон runner; проверить состав версий/адресов, изоляцию и связь результата с manifest. Разработку CD runtime/CI не планировать и не выполнять в этом центральном tasks.md.

## 4. Проверяемый допуск archive

- [x] 4.1 `tamarix-specs`: реализовать обёртку archive, сверяющую traceability, collection, предоставленный отчёт/полный набор и revisions, зафиксированный promotion и актуальность specs; добавить тесты отказов до вызова archive при отсутствующем/неполном/выборочном отчёте или другом tests commit, отсутствия неявного запуска тестов и повторного запуска после partial promotion; проверить активность change при отказе и документировать команды.
- [x] 4.2 `tamarix-specs`: реализовать CI-проверку commits с архивированием, сопоставляющую целевые specs, registry promotion и evidence; проверить отказ при прямом archive без evidence, устаревших hashes/revisions или незавершённых критериях, а также успешный согласованный archive.
- [x] 4.3 `tamarix-specs`: закрепить эту CI-проверку как обязательную в реально используемой CI/merge-политике; подтвердить блокировку принятия archive с проваленным check и записать настройки. До появления remote/CI задача остаётся открытой; YAML файл сам по себе её не закрывает.

## 5. Сквозная проверка процесса

- [x] 5.1 `tamarix-specs` + `TamarixTests`: на изолированных временных репах проверить полный цикл candidate → PASS → promotion → повторный PASS окончательного tests commit → archive, отказ после promotion и безопасное продолжение, MODIFIED/RENAMED/REMOVED; сохранить manifest, команды и evidence. Это проверка tooling-процесса, не предметный HTTP e2e Tamarix.

## Фактические проверки процесса

Пути ниже существуют; фактические collected случаи и результаты — в отчёте
143 проверок реализации, связанном из verification/evidence. Параметризованные
проверки содержат русские пояснения каждого различающегося входа.

| Проверяемое условие | Автоматизированный тест |
| --- | --- |
| Отсутствующее/пустое русское описание | `TamarixTests/tests/unit/test_registry.py::test_missing_description_rejected`, `::test_empty_description_rejected`; качество текста проверяется review |
| Ссылки и уникальные test ID | `TamarixTests/tests/unit/test_registry.py::test_duplicate_id_rejected`, `::test_missing_node_rejected` |
| Отсутствующий/проваленный обязательный случай | `TamarixTests/tests/unit/test_runner.py::test_required_case_must_pass` с именованными missing/fail/skip/xfail/empty случаями |
| Отчёт любого исхода и сохранение истории | `TamarixTests/tests/unit/test_reports.py::test_run_report` с success/fail/collection-error/environment-error/cancel/incomplete случаями; `::test_repeated_run_preserves_previous_report` |
| Archive не запускает отсутствующие тесты | `tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution` |
| Устаревшие версии/evidence | `tamarix-specs/tests/test_archive_gate.py::test_stale_inputs_block_gate` |
| Отказ до изменения specs/archive | `tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution` |
| Возобновление и прямой обход | `tamarix-specs/tests/test_archive_gate.py::test_partial_operation_resumes_and_completed_is_idempotent`, `::test_direct_archive_without_evidence_is_rejected` |

Unit-тесты самого runner находятся в тестовой репе; предметные unit/component
тесты продолжают принадлежать сервисам. Бизнес e2e и соответствующие изменения
API/adapters/PKI/storage планируются в предметных changes, не подменяются
инфраструктурными случаями этой таблицы.

## Workflow follow-up

- Архивировать этот tooling change только после выполнения открытых задач и проверки результатов; предметные specs не синхронизировать, поскольку `skip_specs: true`.
- Проверить сохранение артефактов/ссылок после archive; исходники тестов остаются в постоянных репозиториях.
