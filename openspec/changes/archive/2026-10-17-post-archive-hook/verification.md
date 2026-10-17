# Verification

Дата проверки: 2026-10-17. Полный текущий regression и component suites
завершились PASS. Этот verification фиксирует проверенные версии и готовность
центрального archive; фактический результат archive/rollout сохраняется отдельно.

## Scope и версии

Центральный change меняет только CLI hook и его документацию. Deployment plan,
CD tests и demo2 остаются в [локальном CD archive](../../../../../../TamarixCD/openspec/changes/archive/2026-10-17-post-archive-deployment/verification.md).
Новые предметные delta specs отсутствуют; skip_specs=true подтверждён strict
validation и не отменяет полный regression gate.

Проверяемый central source commit:
`fc394440f6c8024686f632e261c1e91b0b3fcc1a`.
CD runtime/tooling source commit до metadata-only archive:
`5375203672b86f14031cc7b03f826c303bd49fe9`.
Окончательный CD archive commit в subject manifest: `e55825793232db67c57791325fdf63d09d436b24`.
Docs baseline: `38c5af8f9c9c40db0f3ba66fbe0b00b5ab0e9dc4`.

## Component checks

Из TamarixCD выполнены отдельные wrapper runs:

```sh
runtime/.venv/bin/python ci/test_report.py --output-dir reports/post-archive-deployment/final-commit -- tests -q --tb=short
runtime/.venv/bin/python ci/test_report.py --output-dir reports/post-archive-deployment/central-gate -- ../Tamarix/tamarix-specs/tests/test_archive_gate.py ../Tamarix/tamarix-specs/tests/test_docs_check.py -q --tb=short
```

- CD: **338 PASS**, complete=true; run `67db7f26cfd044e0bbc4ff8a6ae8c5b7`.
  Включены 15 CLI hook cases и coverage CD-ARCHIVE-01..06.
- Central gate/docs: **105 PASS**, complete=true; run
  `9aa7e003f633449cb4e04b92db79abd2`, 77 archive cases и 28 docs cases.

Все cases PASS, без SKIP/NOT_RUN. Эти component отчёты не заменяют итоговый
предметный regression report и не используются вместо него в archive gate.

| Report | SHA256 results.json | SHA256 summary.md |
| --- | --- | --- |
| CD 67db7f… | `f769a6af7efde33f69332f9ea66f7c6b5b262bb370bb076d2d630946b2236a4c` | `0865766b323f375b1316f04bd85daf80195f2d04bcedf04622b588c10e7e68f2` |
| Central 9aa7e… | `c0f932e61bd789bf401fbaa7bf5e5d00c116c0326a5f1bb6695e9c4a07d09425` | `24f29127270a7ad5eb93a975fac920f4311afecd661b89577f448293fcf0ef83` |

[CD component summary](../../../../../../TamarixCD/reports/post-archive-deployment/final-commit/67db7f26cfd044e0bbc4ff8a6ae8c5b7/summary.md),
[central gate/docs summary](evidence/central-tools/summary.md).
Оригиналы reports/log/JUnit не переписываются. Raw central bundle сохранён
побайтно в evidence/central-tools; [hash inventory](evidence/central-tools/sha256.json)
проверяет каждый файл без использования reserved component-evidence contract.

## HOOK acceptance coverage

HOOK-01..04/CD-ARCHIVE-01 проверяются tests/test_archive_hook.py:
new/resumed complete, default/explicit config и explicit missing FAIL,
read-only actions/rejection, exact argv, неверный exit/status/JSON,
недоступный driver и безопасная ошибка при сохранённом complete archive.
Точные node IDs перечислены в proposal/design и фактическом CD report.
Прежний Python API archive() дополнительно покрыт 77 центральными cases.

## Полный subject regression

Итог: **114/114 PASS**, complete=true, errors=[], ноль FAIL/ERROR/SKIP/XFAIL/XPASS/NOT_RUN.
Run ID: `20261017T074524-72b901a333a2`, 2026-10-17 07:45:24–07:47:05 UTC.
Selection: полный `--regression`, без change/id/level и bootstrap.

CD producer передал реальному runner следующую команду (пути сокращены
относительно TamarixCD без изменения входных файлов):

```sh
../TamarixTests/.venv/bin/python -m tamarix_tests run \
  --manifest reports/post-archive-deployment/regression/14997da5f5a24d2bb1fd75a3b54c46c4/manifest.json \
  --store ../Tamarix/tamarix-specs \
  --output-dir reports/post-archive-deployment/regression/14997da5f5a24d2bb1fd75a3b54c46c4/reports \
  --regression --junit
```

Gate получает case results.json, а не верхний `cd-orchestration` report.

| Вход | Проверенный commit |
| --- | --- |
| tamarix-specs | `fc394440f6c8024686f632e261c1e91b0b3fcc1a` |
| TamarixCD | `e55825793232db67c57791325fdf63d09d436b24` |
| TamarixTests | `4a3b68e846e541a75496e0c62cb2a4ddcf82895c` |
| db-control | `90e59d2caa23ebb684f4f9dbe5c45c882270a817` |
| container-adm-api | `1ee2f1080bbedb37b4c2490fa748b9a70fc94038` |
| entity-subject-adm-api | `fbc5064bf93326c00bd9b16a83d24bd74a5dde7d` |
| entity-object-adm-api | `f7221186bbc36438e22e3d3c670e60a273d68bb0` |
| policy-adm-api | `0996f76a5fd63ceffd15eb0e07e12a1176a12406` |
| policy-decision-api | `23ad0f147d1eb078c072a2c0d53155b544835caa` |

Python 3.15.0, scope postgresql-integration, PostgreSQL 18.6 (180006), UTF8,
block_size8192, Unicode16.0. Actual head `20261016_0004`; migration fingerprint
`6e1c244b0c248049c2edcf156b1cfc02cd69ade951b8683072a18ca912b7d4c7`.
Store spec hashes сохранены в manifest, delta hashes пусты. Companion не
добавляет предметные cases и не меняет registry/promotion; выполнен весь
актуальный существующий regression окончательного tests commit.

| Артефакт | SHA256 |
| --- | --- |
| results.json | `ff13c64366bfb743f7a57b7fd62f273448bdbafee0a12dec481620f8a0853556` |
| manifest.json | `a8685f88cf9586d91dc1e7bb1313f429a22f5abe814e5f5e49c9daa72a6a9c61` |
| summary.md | `be61e51287979763a38be9603988b2b187ac8d9172dd43c092b37b2a9a4dcfb8` |

[Subject summary](../../../../../../TamarixCD/reports/post-archive-deployment/regression/14997da5f5a24d2bb1fd75a3b54c46c4/reports/20261017T074524-72b901a333a2/summary.md),
[case results](../../../../../../TamarixCD/reports/post-archive-deployment/regression/14997da5f5a24d2bb1fd75a3b54c46c4/reports/20261017T074524-72b901a333a2/results.json).
Gate при archive сохраняет report/manifest/summary/registry snapshots в change.

Первый диагностический вызов с `--change post-archive-hook` был отклонён
runner до выполнения: tooling companion не вводит обязательных новых предметных
cases. Отдельный report `20261017T073407-9d5f2426c139` сохранён со статусом ERROR,
114 NOT_RUN и сообщением «Полный набор change должен содержать его обязательные
новые случаи». Исправлен только выбор на `--regression`; код и ожидания не
менялись. Этот ранний отказ не объявляется PASS и не заменяет итоговый run.

## Documentation и archive readiness

После завершения фактических tasks/verification выполняются docs prepare
--refresh и review с прежним baseline, check всех 8 страниц/15 Mermaid,
strict OpenSpec validate и archive_gate check с новым case report.
Команды archive не запускают тестовые наборы. Настроенный post-archive driver
вызовется после complete archive; возможный rollout FAIL не откатывает archive.

Operation ID и неизменный путь runner report задаёт root при archive.
Фактические archive/rollout/commit/merge итоги после выполнения сохраняются
в archive-completion.json, не в изменяемом историческом source verification.
Readiness validation 2026-10-17: PASS.

- `openspec validate post-archive-hook --strict`: PASS, zero domain deltas
  осознанно разрешены skip_specs=true.
- `python3 tools/docs_check.py check`: PASS, 8 страниц, 15 Mermaid blocks,
  unavailable_source_links=[]; docs review всех восьми разделов PASS.
- `../../TamarixTests/.venv/bin/python tools/archive_gate.py check --tests ../../TamarixTests --change post-archive-hook --report /Users/mfedotenko/Projects/TamarixS/TamarixCD/reports/post-archive-deployment/regression/14997da5f5a24d2bb1fd75a3b54c46c4/reports/20261017T074524-72b901a333a2/results.json`:
  PASS, run_id=20261017T074524-72b901a333a2.

Локальная CD config существует и включена (schema1, desktop-linux/tamarix-local),
содержит существующие абсолютные paths state/workspace/db-control/Python.
Её значения credentials в evidence не копируются. Проверки готовности не
вызывали Docker, БД или test runner.

Подготовленный operation ID:
`post-archive-hook-20261017T074524-72b901a333a2`.
Для archive используется тот же case report и обычная настроенная CD конфигурация.
После завершения metadata повторный docs refresh/review/check сохраняет тот же
исходный baseline и проверяет новые hashes без запуска тестов.
