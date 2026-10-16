# Проверка T-5

## Реализованный срез

- Alembic `20261016_0004` после `20261015_0003`: immutable named shapes,
  точные definition/shape pins, общие validator/equality metadata, прежние views
  и совместимые catalog wrappers. Исторические SQL migrations не менялись.
- Внутренняя сверка fingerprints до commit сохраняет payload, IDs, semantic
  tuples, применимость и пользовательские/технические revisions. Обратный
  переход разрешён только в disposable БД и теряет новый каталог shapes.
- 13 новых integration cases и отдельное component evidence для 10 критериев,
  которые нельзя доказать публичными catalog calls. Gate не ослабляет полный
  обязательный integration/regression набор.
- Все восемь страниц docs и ADR 0005 обновлены по коду. При параллельном
  завершении T-4 исходные восемь docs в новом HEAD совпали побайтно с сохранённым
  пользовательским baseline; T-5 добавлен поверх него отдельными изменениями.

## Завершённые проверки

| Проверка | Версия / отчёт | Результат |
| --- | --- | --- |
| Component PostgreSQL | db-control `90e59d2caa23ebb684f4f9dbe5c45c882270a817`; `component-results.json` | 206/206 PASS, complete; run-start clean provenance |
| Tooling docs/archive gate | `verification/tooling-20261016T131239-7fc0c344/results.json` | 105/105 PASS; включая 17 новых случаев component evidence |
| Registry collection | TamarixTests `4a3b68e846e541a75496e0c62cb2a4ddcf82895c`; validate-registry --change t-5-persistant-change-1 | 114 точных node ID |
| Traceability | union registry links + component-evidence.json | Все 45 THEN delta покрыты точными сценариями и nodes |
| Документация | docs_check.py check | 8 страниц, 15 Mermaid blocks, PASS |
| OpenSpec | validate t-5-persistant-change-1 --strict | PASS |

Component-прогон выполнен через `db-control/tools/run_tests.py --output-dir
reports -- tests/component -q` на отдельном PostgreSQL; сохранены исходные
Python/package pins. Новая изолированная integration среда подготовлена и
переведена на 0004 существующим CD executor, без изменения production-сервисов.

## Полный прогон перед promotion

- Первый полный запуск `20261016T131510-74fff58579f3` на tests `4c807d3`:
  112 PASS, 2 FAIL. В c11 исправлено необоснованное ожидание двух commit без
  допустимого SERIALIZABLE 40001: проверяется полный повтор с исходным CAS token,
  независимые revisions и неизменность shared shape. В c13 чтение subject facts
  выполняется предназначенным для него native subject LOGIN.
- Повторный полный запуск `20261016T131757-7b037542699f` на tests
  `466f1597001d2dc3a7c63419f88474ebcb5bd4fa`, store `3398d74`, db-control
  `90e59d2caa23ebb684f4f9dbe5c45c882270a817`: **114/114 PASS**, complete,
  без skips/xfails/NOT_RUN. Отчёт:
  `TamarixTests/reports/a7e21157a4624facaad1858dec50d6bb/reports/20261016T131757-7b037542699f/results.json`.
- Promotion выполнен по готовому PASS: 13 shapes cases переведены из candidate
  в regression; семантически изменились только эти 13 state полей, остальные
  данные registry сохранены. Promotion commit:
  `4a3b68e846e541a75496e0c62cb2a4ddcf82895c`.

## Финальный полный прогон

**114/114 PASS**, complete, FAIL/ERROR/SKIP/XFAIL/XPASS/NOT_RUN = 0.
Run `20261016T132240-925d0021ad54`, PostgreSQL integration; tests commit
`4a3b68e846e541a75496e0c62cb2a4ddcf82895c`, db-control
`90e59d2caa23ebb684f4f9dbe5c45c882270a817`, store source
`67967107f50fd05a616f945f2f112032f8fb7391`, CD
`022f4c3dcc9aa592410e039a8ba4268d54f8ae44`. Полные commits пяти consumers,
SQL/resource/package hashes, DB facts/head и Python 3.15.0 зафиксированы в
[manifest](run-manifest.json). Store commits после запуска добавляют только
итоги, документацию и review; основные и delta specs не менялись.

- [Готовый report](run-results.json), [русская сводка](run-summary.md),
  [окончательный registry](regression-registry.yaml).
- [Полный комплект report/manifest/JUnit/log](verification/integration-20261016T132240-925d0021ad54/).
- SHA-256 raw report:
  `56e8f2ecb6be4c9217eb1887db2528e9b302676d08d0fdd01cbd26316849339f`.
- SHA-256 manifest:
  `797350024df83a807f79f73ca5b5a6b2da7d18cefed44d5e095e1293c6e27ac4`.
- SHA-256 registry:
  `e74b8c4baf01502574c39248b4deb2811ef8584f162b3e508f9ee576bab730e1`.

Запуск выполнен через существующий `TamarixCD/ci/external_tests.py run` с
`--scope postgresql-integration --change t-5-persistant-change-1 --junit`,
явными путями workspace/tests/store/db-control, state отдельного PostgreSQL и
private env. Значения DSN/password в evidence не записаны. Runner использует
новый manifest после promotion. Подготовка среды и миграция выполнены штатным
`ci/postgresql_environment.py`; прежняя пользовательская среда не затронута.

## Итоговые проверки

Для docs review сохранён отдельный baseline T-5:
`6882ec9b9af212dda8effb3017bfac0473bbc2a1`. Все восемь страниц сверены с кодом;
Mermaid показывает общие shapes, точные definition pins и прежние owner/CAS
границы. Дополнительно независимые read-only review всех восьми docs, SQL migration
и gate не выявили существенных замечаний.

Команды завершения:

```sh
../../TamarixTests/.venv/bin/python tools/docs_check.py check
../../TamarixTests/.venv/bin/python tools/docs_check.py review --change t-5-persistant-change-1
openspec validate t-5-persistant-change-1 --strict --store tamarix-specs
../../TamarixTests/.venv/bin/python tools/archive_gate.py check --tests ../../TamarixTests --change t-5-persistant-change-1 --report openspec/changes/t-5-persistant-change-1/verification/integration-20261016T132240-925d0021ad54/results.json
```

Результаты: `docs_check.py check` **PASS** (8 страниц, 15 Mermaid blocks),
`review --change` **PASS**, strict OpenSpec **PASS**, `archive_gate.py check`
**PASS** по финальному run `20261016T132240-925d0021ad54`. Точные links registry
и component bundle подтверждают все **45 THEN**. [Docs review](docs-review.json)
и [полный snapshot](docs-snapshot.json) обновлены после закрытия всех задач;
[gate check](archive-gate-check.json) сохранён отдельно.

**25/25 задач завершены.** Изменение остаётся активным и готово к отдельному
archive через gate; архивирование в apply не выполнялось.
