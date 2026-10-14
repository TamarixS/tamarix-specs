# Проверка добавленного процесса

Дата: 2026-10-14, timezone Europe/Moscow. Проверены документация, конфигурация
и planning artifacts; исходники сервисов/CD, предметные specs и старые архивы
не изменялись. `TamarixTests`, registry/runner, обёртка и CI gate не реализованы.
Integration/e2e и сервисные автотесты в рамках добавления правил не запускались.

По указанию пользователя change переименован в `t-2-e2e-tests`. Проверки
validate/status и read-only instructions apply/archive повторены с новым именем;
все завершились успешно. Ссылки обновлены, статусы задач сохранены.

## Команды и результаты

| Проверка | Результат |
| --- | --- |
| `openspec --version` | 1.14.1, существующий CLI |
| `openspec validate t-2-e2e-tests --strict --store tamarix-specs` | PASS; tooling-only `skip_specs: true`, предметные deltas не нужны |
| `openspec validate --all --strict --store tamarix-specs --json` | PASS: change и четыре основные specs, 5/5, без ошибок/предупреждений; INFO о skip_specs |
| `openspec status --change t-2-e2e-tests --store tamarix-specs --json` | Proposal/design/tasks созданы, specs skipped; это статус наличия planning artifacts, не выполнения implementation tasks |
| `openspec instructions apply --change t-2-e2e-tests --store tamarix-specs --json` | PASS: context содержит TamarixTests, operationGuidance требует чтения testing.md |
| `openspec instructions archive --change t-2-e2e-tests --store tamarix-specs --json` | PASS: guidance содержит traceability, новые тесты/регресс, версии/evidence и promotion; команда read-only, archive не выполнялся |
| `openspec status --change service-launch-pipeline --json` из TamarixCD | PASS: локальный root TamarixCD сохранён, config читается |
| `git diff --check` в tamarix-specs и TamarixCD | PASS |
| Read-only проверка локальных Markdown-ссылок через pathlib | PASS для policy/ADR/context/AGENTS и proposal/design/tasks; отсутствующих целей нет |
| Независимое read-only review | Конкретных проблем в ownership, ссылках, evidence/promotion и статусе реализации не обнаружено |

## Локальная регистрация store

Первичная проверка выявила registry, указывавший на отсутствующий прежний путь
`/Users/mfedotenko/Projects/Tamarix/tamarix-specs`. После разрешённого обновления
регистрации через `openspec store unregister` и `openspec store register`
store `tamarix-specs` разрешается в
`/Users/mfedotenko/Projects/TamarixS/Tamarix/tamarix-specs`.
Файлы репозитория и его store identity при перерегистрации не создавались
и не удалялись. `openspec list/context --json --store tamarix-specs` после
обновления завершились успешно и вернули текущий root.

## Оставшаяся работа

В [tasks.md](tasks.md) завершены только документальные задачи раздела 1.
Разделы 2–5 остаются открытыми: тестовая репа, registry/runner, реальные
проверки начального набора, CD integration prerequisite, wrapper/required
CI check и сквозная проверка восстановления. Предметные HTTP e2e требуют
соответствующих бизнес endpoints/adapters; `/health` не закрывает эти критерии.

## Дополнение: русские описания всех тестов

По прямому указанию пользователя добавлено обязательное описание на русском
для всех уровней и репозиториев: что проверяется, условия, ожидаемый результат
и назначение/применимость. В Python используется docstring теста; различающиеся
параметризованные случаи поясняются по-русски. Для TamarixTests предусмотрены
description в registry и его вывод в отчёте. Обновлены policy/ADR, инструкции
центрального store и TamarixCD, proposal/design/tasks; исходники тестов не менялись.

Повторный `openspec validate --all --strict --store tamarix-specs --json`
завершился PASS, 5/5. `openspec instructions tasks/apply` для `t-2-e2e-tests`
передали новое правило; instructions tasks для локального CD change также
передали проверку русских описаний. `git diff --check` обоих репозиториев — PASS.
Это подтверждает добавление правил, а не наличие описаний у прежних тестов
или реализацию валидатора/runner.

## Дополнение: запуск по требованию и отчёты

По указанию пользователя добавлены явная инициация прогона, выбор/повтор
набора независимо от archive и обязательные summary.md на русском/results.json
каждого прогона; JUnit XML — по требованиям CI. Отчёты содержат случаи с русскими
описаниями, статусы/длительность/ошибки, набор, версии и артефакты, сохраняются
также при неуспехе/отмене без перезаписи истории. Незавершённый snapshot и NOT_RUN
не считаются успехом. Archive gate проверяет готовый отчёт и не инициирует тесты.

Обновлены policy/ADR, AGENTS/config центрального store и TamarixCD,
proposal/design/tasks. Повторный strict validate — PASS, 5/5; instructions
tasks/archive store и tasks локального CD change передают новые правила;
`git diff --check` обоих репозиториев — PASS. Это документальное дополнение:
runner/reporting и соответствующие проверки остаются открытыми задачами.
Runtime, integration/e2e или сервисные тесты этим запросом не запускались.

## Реализация и фактические прогоны — 2026-10-14

Создана отдельная локальная Git-репа [TamarixTests](../../../../../TamarixTests/README.md).
Store pointer разрешает `tamarix-specs`; remote тестовой репы не назначен.
Проверены `uv lock --check`, `uv sync --frozen`: Python 3.15.0 final,
uv/uv_build 0.12.24, pytest 9.1.1, PyYAML 6.0.3. Пять ядер 0.1.0
установлены noneditable; импорты разрешаются из site-packages, без соседних src.

Runner/registry/promotion и отчёты реализованы в TamarixTests; archive wrapper
и CI-валидатор — в этом store. CD manifest/readiness и внешний вызов реализованы
отдельным локальным [external-test-runner](../../../../../TamarixCD/openspec/changes/external-test-runner/verification.md),
4/4 его задач выполнены, strict validation PASS. Контракт описан в
[EXTERNAL_TESTS.md](../../../../../TamarixCD/ci/EXTERNAL_TESTS.md).

Проверка реализации из TamarixTests:

```sh
.venv/bin/python -m pytest tests/unit tests/integration \
  ../Tamarix/tamarix-specs/tests/test_archive_gate.py \
  ../TamarixCD/tests/test_external_tests.py -q \
  --junitxml=reports/t2-implementation-checks/junit.xml
```

**143 passed in 54.33s**, без fail/error/skip; summary.md/results.json/JUnit
сохранены в `TamarixTests/reports/t2-implementation-checks/`. Все 143 отчётных
случая имеют русские описания, составленные из docstrings и пояснений параметров.
Проверены missing/duplicate/parameter/invalid link, fail/skip/xfail/xpass/NOT_RUN,
выбор набора, отмена/kill, отчёты ошибок, provenance и подмена summary.

Реальные команды из TamarixCD, на чистых зафиксированных checkout:

```sh
python3 ci/external_tests.py run --workspace ../Tamarix --tests ../TamarixTests \
  --store ../Tamarix/tamarix-specs --change t-2-e2e-tests \
  --runner-python ../TamarixTests/.venv/bin/python \
  --output-dir ../TamarixTests/reports/immutable-runs --junit \
  --bootstrap-empty-regression
```

Первый полный candidate прогон **20/20 PASS**: tests commit
`a5b1bd1074bcdaa0001c7d99e497967a4e5f1258`, run ID
`20261014T145101-7d03ab41781c`. Начальный пустой прежний регресс явно bootstrap.
Затем из TamarixTests выполнена CLI `promote` с этим results.json,
сохранён promotion commit `b51f49486db1a13be64f0f03a5034846f8114e61`,
и та же CD команда без bootstrap дала **20/20 PASS** окончательного commit:
run ID `20261014T145613-3635e2ccfb98`. Отдельный `--regression` прогон
без выбора change также дал **20/20 PASS**. Нет fail/error/skip/NOT_RUN.

Во всех трёх входах CD commit `c37933127b83c93aa726111d52db7a0fb987ec54`,
store input commit `af97e100fa1222e12279a14ced6ea63433c81fa3`; точные commits
пяти сервисов и SHA256 всех Python source/spec файлов — в manifest/evidence.
Scope `logical-integration`: endpoints/image digests/migrations явно null;
уникальная environment.id, новые объекты fixtures каждого случая.
Это подтверждение интеграции установленных ядер и адаптеров, не HTTP/PKI/storage.
HTTP readiness пяти health имён проверена CD focused tests и не выдаётся за бизнес e2e.

[implementation-evidence.json](implementation-evidence.json) сохраняет paths,
report/manifest/registry hashes и полный version manifest. Вложенный case report,
а не верхний CD orchestration report, прошёл реальную `archive_gate.py check`:
**PASS**. Обёртка не запускала тесты; реальный T-2 остаётся активным.

## Изолированный полный lifecycle, задача 5.1

В `TamarixTests/reports/lifecycle-c466c9759993469e92265d8dfeac2a7f/` сохранены
scenario.py, команды/logs, русская сводка, JSON, raw candidate/final manifests
и скопированные archive evidence. Временные репы созданы из immutable snapshots
реального кода, store без глобальной регистрации. К 20 исходным случаям
добавлен временный 21-й для MODIFIED критерия смешанных нейтральных/неопределённых
моделей. Настоящие CD/runner/CLI promotion/OpenSpec archive выполнили:

`21 candidate PASS → promotion commit → отказ старого report → 21 final PASS
→ archive fixture-flow → store commit → CI PASS → идемпотентный повтор`.

До promotion gate отказал «Promotion не зафиксирован», после promotion старому
report — «Registry изменён после прогона». Окончательный tests commit временной
репы `63fdb535838dc62a6fbc3ac87e3ae073c8ee2ce1`; финальный report SHA256
`d37c842b229cb4c6890a0dcdb1c5482c1e6a83b4a41f6ff489599fe344d92e48`.
Настоящий OpenSpec изменил только временный store; `archives_checked: 1`,
повтор операции не создал новых records/commit.

49 gate tests дополнительно подтвердили MODIFIED/RENAMED/REMOVED с реальным
OpenSpec CLI, retry после частичного spec merge и перемещения change, отказ
прямому archive без evidence, незавершённым tasks/критериям, повреждённым hashes
и удалению одного обязательного archive-артефакта. Эти tooling проверки
не являются предметным HTTP e2e. Исторические архивы T-1 не изменены.

## Реальная required CI policy, задача 4.3

GitHub для приватного `TamarixS/tamarix-specs` вернул 403 с требованием
GitHub Pro либо публичной видимости. Пользователь явно ответил «Сделай публичным».
Просмотр tracked/new файлов и всех 4 доступных commits (62 уникальных blob)
не обнаружил явных credentials, токенов или приватных ключей. GitHub PATCH
подтвердил `visibility: public`, HTTP 200; прочие репозитории не публиковались.

Для main установлен required `archive-evidence` от GitHub Actions app 15368,
`strict: true`, `enforce_admins: true`, force push/deletion запрещены.
Прежней branch protection не было (GET 404), новая настройка дала PUT 200.
Реальный [PR реализации #1](https://github.com/TamarixS/tamarix-specs/pull/1)
получил [SUCCESS check](https://github.com/TamarixS/tamarix-specs/actions/runs/38585140683/job/115924989511).

Временный [негативный PR #2](https://github.com/TamarixS/tamarix-specs/pull/2)
с намеренно неполным archive получил [FAILURE check](https://github.com/TamarixS/tamarix-specs/actions/runs/38586525692/job/115929876958).
Checkout и установка валидатора прошли; archive validation завершилась exit 1:
«Прямой archive без evidence». GitHub подтвердил для открытого, не draft,
неконфликтного PR `mergeable: true`, **`mergeable_state: blocked`**, `merged: false`.
Это фактическое подтверждение запрета принятия archive при проваленном required
check. Запрос merge заведомо ошибочного archive не выполнялся. PR закрыт
без слияния и временная remote ветка удалена; fixture не попадает в main.

Настройки и результаты API/checks сохранены в
[github-required-check-evidence.json](github-required-check-evidence.json).

Итоговая `openspec validate --all --strict --store tamarix-specs --json`: **5/5 PASS**;
повтор `archive_gate.py check` окончательного отчёта после записи задач/evidence:
**PASS**. `git diff --check` чистый. OpenSpec apply сообщает **all_done, 16/16**.
Реальный T-2 не архивирован; архивирование — следующий отдельный workflow.
