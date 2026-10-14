# Проверяемый допуск archive

Запускать через Python среды TamarixTests (PyYAML 6.0.3 установлен по frozen lock):

```sh
../../TamarixTests/.venv/bin/python tools/archive_gate.py check \
  --tests ../../TamarixTests --change CHANGE --report /absolute/path/results.json
../../TamarixTests/.venv/bin/python tools/archive_gate.py archive \
  --tests ../../TamarixTests --change CHANGE --report /absolute/path/results.json \
  --operation-id CHANGE-RUN-ID
```

Для другого checkout передать `--store /absolute/path/store`. Wrapper не
инициирует тесты: нужен завершённый полный PASS окончательного tests commit
после promotion. Русская сводка, JSON и manifest должны относиться к одному
прогону; точные collected/executed IDs, source revisions/hashes и criterion
links сверяются до изменения specs/переноса change. Диагностический выбор
и пропущенные/не начавшиеся случаи archive не закрывают.

Wrapper сохраняет report/manifest/registry/русскую сводку и evidence в change,
которые затем переходят в archive. Логи/крупные артефакты остаются в каталоге
прогона; ссылки и hashes доступны в отчёте. `.archive-operations/<id>.json`
позволяет повторить операцию с тем же входом без второго archive и продолжить
после частичного delta merge. Сменившиеся revisions требуют нового прогона/ID.

CI проверяет любой добавленный/изменённый/удалённый archive-файл относительно
base, включая Git rename и удаление только evidence. Выполняется проверка
сохранённых результатов, покрытия delta критериев и полного результата merge:

```sh
../../TamarixTests/.venv/bin/python tools/archive_gate.py validate-archives --base BASE_SHA
```

Workflow `.github/workflows/archive-evidence.yml` не запускает предметные тесты.
Job `archive-evidence` нужно сделать обязательным для main в реальных settings
GitHub. Наличие workflow не подтверждает доступность branch protection или
установленный required check; состояние записывается отдельным evidence.

Изменение существующих архивов до введения evidence требует отдельного review;
старые архивы этим внедрением не изменяются. Сам `t-2-e2e-tests` архивируется
только после закрытия его задач, по отдельному workflow follow-up.
