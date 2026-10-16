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
| Registry collection | TamarixTests `466f1597001d2dc3a7c63419f88474ebcb5bd4fa`; validate-registry --change t-5-persistant-change-1 | 114 точных node ID |
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
- Promotion и финальный повтор на окончательном registry commit выполняются
  после этого PASS. Их evidence будет записано по фактическому завершению.
  Archive не выполняется в apply.
