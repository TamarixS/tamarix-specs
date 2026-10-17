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

- [x] TamarixCD: подтвердить CD component regression 338 PASS, включая 15 hook cases,
  и сохранить неизменённые report/summary/log/JUnit с SHA256 в verification.md.
- [x] tamarix-specs: подтвердить 105 PASS прежних archive/docs suites
  (77 archive и 28 docs), сохранив отдельные report и SHA256.
- [x] TamarixTests/TamarixCD: получить полный текущий regression PASS на окончательном
  CD archive commit и source store commit, сохранить новый manifest/summary/JSON,
  проверить отсутствие SKIP/NOT_RUN/выборочного набора и неизменность source/specs.

## 4. Готовность archive и передача результатов

- [x] tamarix-specs: завершить verification фактическими versions/report hashes,
  подготовить cross-repo links относительно будущего archive, затем refresh
  docs review с прежним baseline и проверить все восемь разделов/hashes.
- [x] tamarix-specs: подтвердить strict validate, docs gate и archive_gate check
  с новым полным report; подготовить неизменные report path/operation ID и
  проверенный post-archive config для адресной автоматической доставки.
- [x] tamarix-specs/TamarixCD: подготовить последовательность archive/CI validation,
  commit/merge, проверить сохранность исходных reports и предусмотреть запись
  фактического archive/deployment/merge результата в archive-completion.json.

## Evidence

Фактические проверки и воспроизводимые команды — [verification.md](verification.md).
Текущие checkbox описывают проверяемую готовность до мутаций archive. Сама операция
archive/rollout и её последующий commit/merge фиксируются отдельно в
archive-completion.json; они не объявляются выполненными до исполнения.
