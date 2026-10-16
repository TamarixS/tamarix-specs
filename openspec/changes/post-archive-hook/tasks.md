# Tasks

## 1. Scope и источники

- [x] tamarix-specs: оформить узкий companion для central CLI hook/docs; сохранить
  deployment planning и CD-ARCHIVE-01..06 в локальном TamarixCD change.
- [x] tamarix-specs/TamarixCD: сверить фактический hook и CD driver с HOOK-01..04,
  указать реальные pytest node IDs без предметной delta и переноса CD tests.

## 2. Реализация и документация

- [x] tamarix-specs: вызвать CD только после complete результата CLI archive,
  сохранить API archive(), покрытие resume и read-only actions.
- [x] tamarix-specs: описать default missing NOT_CONFIGURED, explicit missing FAIL,
  безопасную ошибку, независимые статусы/reports и повтор прежней operation.
- [x] tamarix-specs: подготовить docs snapshot/review всех восьми страниц от
  baseline `38c5af8f9c9c40db0f3ba66fbe0b00b5ab0e9dc4`; не изменять старые архивы.

## 3. Явная проверка окончательных версий

- [ ] TamarixCD: зафиксировать окончательный source commit и завершённые CD tests
  с HOOK-01..04/CD-ARCHIVE-01..06; записать команды, report paths и hashes.
- [ ] TamarixTests/TamarixCD: по запросу пользователя получить полный текущий
  regression PASS на окончательных immutable commits; сохранить новый manifest,
  русскую summary и JSON, без копирования исторического T-5 PASS.
- [ ] tamarix-specs: проверить прежние archive API tests и новый CLI hook coverage,
  записать фактический результат; выполнить strict validate и docs gate.

## 4. Archive и передача

- [ ] tamarix-specs: после окончательных tasks/verification выполнить docs review
  refresh с прежним baseline, заполнить восемь разделов и проверить hashes.
- [ ] tamarix-specs: выполнить check/archive через tools/archive_gate.py с новым
  полным report; сохранить operation ID и фактический deployment status отдельно.
- [ ] tamarix-specs/TamarixCD: сохранить исходные reports/snapshots, проверить
  archive evidence и подготовить разрешённые пользователем commit/merge.
