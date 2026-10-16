# Проверка t-4-docs

Дата: 2026-10-15. Изменён только центральный `tamarix-specs`.
Предметный код, DDL, миграции, GitHub settings и исторические архивы не менялись.
Реальное архивирование этого change не запрашивалось и не выполнялось.

## Результат

- Созданы восемь русскоязычных страниц docs, общий вход README и 15 Mermaid-схем.
- Справочник БД сверяет все 25 CREATE TABLE пяти прикладных схем и служебную
  Alembic table; учебный набор согласован с Acme → Prod → Orders.
- API сверяет реальные Python signatures/DTO/outcomes, HTTP `/health`, SQL/CLI.
  Шесть Python-примеров прошли `ast.parse`; это проверка синтаксиса,
  а не выполнение бизнес-команд.
- Docs checker: 8 страниц, 15 Mermaid blocks, PASS, все source links доступны.
- Mermaid grammar parser: 15/15 PASS. Использован локальный Mermaid bundle
  установленного Obsidian; для Node-only разбора HTML sanitizer заменён identity
  stub. Грамматика/parser не изменялись. SVG layout/HTML sanitization этим
  запуском не проверяются. Результат: [mermaid-parser-results.json](verification/mermaid-parser-results.json).
- OpenSpec strict validation: PASS, warnings/issues отсутствуют.
- Single/bulk archive skills: оба `quick_validate.py` PASS.
- `git diff --check`: PASS.

## Автоматизированные tooling tests

Итог: **88/88 PASS**, 34.653 секунды; FAIL/ERROR/SKIP/XFAIL/XPASS/NOT_RUN — 0.
28 случаев docs checker и 60 случаев archive gate. Все 88 имеют русские
описания; source hashes четырёх исполняемых файлов совпадают с итоговым кодом.

Команда фактического итогового прогона из корня store:

```sh
../../TamarixTests/.venv/bin/python /tmp/tamarix_docs_gate_test_runner.py \
  tests/test_docs_check.py tests/test_archive_gate.py
```

Снимок использованного одноразового runner сохранён как
[tooling_test_runner.py](verification/tooling_test_runner.py). Для повторения
можно использовать этот путь вместо `/tmp/tamarix_docs_gate_test_runner.py`;
он формирует новый отдельный каталог `/tmp/tamarix-docs-gate-<run-id>`.
Не добавлены фоновые прогоны, расписание или tests от archive/commit.

Итоговые артефакты сохранены в change:

- [Русский отчёт](verification/tamarix-docs-gate-20261015T200806-88861760/summary.md)
- [JSON со всеми node IDs, описаниями, статусами и версиями](verification/tamarix-docs-gate-20261015T200806-88861760/results.json)
- [JUnit](verification/tamarix-docs-gate-20261015T200806-88861760/junit.xml)
- [Лог](verification/tamarix-docs-gate-20261015T200806-88861760/pytest.log)

Ранние прогоны сохранены отдельно в `/tmp`: `...200010-f7fd4d54` (ошибка
одноразового отчётного plugin до коллекции), `...200019-d28048b5` (75 PASS/1 FAIL:
fixture старого tasks-теста требовал refreshed docs review), `...200206-a688ad19`
(79 PASS до усиления batch/historical snapshot). Прежние каталоги не перезаписаны.

## Независимый review

Выявлены и исправлены два дефекта первого варианта: сравнение всех новых
batch archives с последним current docs и возможность самосогласованно
переписать historical docs hashes. Введён content snapshot каждого archive,
его structural/hash validation, any-current-match для новых batch snapshots
и неизменяемость принятых review/snapshot/hash fields относительно Git base.
Повторный независимый review подтвердил устранение обоих дефектов и достаточность
новых отрицательных тестов. Тест последовательных archives использует общий
base до обоих архивов, а не base после первого.

## Пределы проверки

Тесты gate используют изолированные одноразовые Git stores и fake reports,
а также настоящий OpenSpec lifecycle в fixture. Они не заменяют предметный
регресс TamarixTests; приложение, PostgreSQL и Docker не запускались.
`validate-archives --base HEAD` на текущем checkout даёт PASS/0 archives:
исторические архивы не менялись; новые archive-сценарии проверены fixtures.
GitHub workflow обновлён локально, удалённый CI и branch policy не проверялись.

Hashes не доказывают смысловую полноту текста. Эта часть проверена чтением
исходников и отдельной сверкой разделов API/БД/доменных правил. Перенос store
без соседних repos сохраняет docs-навигацию; внешние source links требуют checkout.
