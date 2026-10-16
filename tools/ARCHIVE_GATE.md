# Проверяемый допуск archive

Новые changes архивируются через эту обёртку. До переноса change необходимо
обновить полную проектную документацию в [`docs/`](../docs/README.md), завершить
review всех её разделов и предоставить готовый полный PASS регресса. Эти условия
распространяются и на tooling/docs-only changes без предметных delta specs.
Обёртка и CI проверяют предоставленные файлы; тесты и генерацию текста они не запускают.

Для component-only критериев допускается дополнительный комплект в change:
`component-evidence.json`, `component-results.json`, `component-summary.md`.
Raw component PASS должен содержать снятые до collection commit/clean/source,
resource и test hashes и подтверждение неизменности после выполнения. Commit,
runtime source/resources и Python/package versions совпадают с integration
manifest.db_control; evidence связывает точные THEN с реальными PASS node IDs,
русскими описаниями и immutable test source snapshots. Это дополняет покрытие
критериев, сохраняя обязательность полного integration/regression отчёта.
Неполный, подменённый или устаревший bundle отклоняется; archive фиксирует
его hashes и проверяет snapshots без обращения к изменившемуся checkout.

## Документация и review

В `docs/` обязательны восемь страниц: `README.md`, `architecture.md`, `domains.md`,
`services.md`, `api.md`, `database.md`, `operations.md`, `development.md`. В них
отражаются общая схема продукта, домены/слои/ответственность, сервисы и их связи,
API, модель БД с примерами, связи/ограничения/индексы, конкуренция и эксплуатация.
Факты реализации, принятые решения и TBD необходимо различать. Все Markdown
страницы `docs/`, включая дополнительные, входят в SHA-256 snapshot.

Перед изменением документации запомнить исходный commit (`git rev-parse HEAD`).
После завершения changes/specs/tasks и обновления docs подготовить evidence:

```sh
python3 tools/docs_check.py check
python3 tools/docs_check.py prepare --change CHANGE --base-ref BASE_SHA
```

`--base-ref` по умолчанию `HEAD`: это подходит, если docs ещё не закоммичены.
При уже закоммиченных docs передать сохранённый commit **до** их обновления.
В `openspec/changes/CHANGE/docs-review.json` заполнить каждый элемент `sections`:

```json
{
  "docs/api.md": {
    "status": "updated",
    "reason": "Добавлены запрос, ответ и ошибки нового endpoint; примеры сверены с контрактом."
  },
  "docs/database.md": {
    "status": "reviewed",
    "reason": "Схема, ограничения и индексы не затронуты; описание сверено с миграциями."
  }
}
```

Это фрагмент `sections`, а не полный файл. `updated` обязателен для фактически
изменённой обязательной страницы; `reviewed` — для неизменённой. Для каждой
нужна содержательная причина на русском. `pending` блокирует archive.
Даже если change меняет только tooling, необходимо обновить минимум одну
страницу (например, процесс разработки), а все остальные просмотреть.

Полный формат evidence v1:

| Поле | Проверяемое значение |
| --- | --- |
| `schema_version`, `change` | Версия `1` и точный ID change |
| `base_commit` | Полный Git SHA исходного состояния docs; должен быть предком HEAD |
| `change_sha256` | Словарь относительных путей и SHA-256 всех исходных файлов change, включая proposal/design/tasks/deltas |
| `docs_sha256` | SHA-256 всех текущих `docs/**/*.md` |
| `snapshot_sha256` | SHA-256 файла `docs-snapshot.json` с сохранённым содержимым всех страниц |
| `changed_pages` | Полный отсортированный список добавленных/изменённых/удалённых Markdown страниц относительно baseline; непустой |
| `sections` | Ровно восемь обязательных страниц со `status` и русским `reason` |

`prepare` также сохраняет `docs-snapshot.json`: JSON с `schema_version: 1` и
`files`, где каждому пути страницы соответствуют её `content` и `sha256`.
Текст сохраняется полностью, чтобы несколько последовательных archives могли
подтверждать разные версии docs в одном PR. Snapshot не редактируется вручную.

Из хэшей change исключены только генерируемые gate-файлы: `docs-review.json`, `docs-snapshot.json`,
`run-results.json`, `run-manifest.json`, `run-summary.md`,
`regression-registry.yaml`, `regression-evidence.json`, `archive-gate-check.json`,
`archive-completion.json`; `.DS_Store` игнорируется. Пути отсчитываются от change,
поэтому перенос в archive не меняет snapshot.

Изменение любого исходного артефакта change или docs после review делает evidence
устаревшим. Для обновления выполнить:

```sh
python3 tools/docs_check.py prepare --change CHANGE --refresh
python3 tools/docs_check.py review --change CHANGE
```

`--refresh` сохраняет исходный `base_commit`, обновляет snapshot/hashes и сбрасывает **все**
разделы в `pending`: их необходимо повторно заполнить до `review`. Обычный
`prepare` существующий файл не перезаписывает. Новый commit сам по себе не
делает неизменённые content hashes устаревшими.

`check` проверяет обязательные страницы, заголовки/русский текст и существование
локальных Markdown ссылок. Ссылки на известные соседние исходные репозитории
проверяются при наличии их checkout; в store-only CI отсутствующие source roots
явно перечисляются в `unavailable_source_links` и не считаются сломанными.
Ссылки внутри store обязательны и в CI; неизвестные внешние локальные корни и
абсолютные пути запрещены. В `architecture`, `services`, `database` обязательны
Mermaid схемы. Validator проверяет закрытые fenced blocks, известный тип и
непустое содержимое схемы; корректность отображения и предметный смысл схем
проверяются при review. Это структурная проверка, а не Mermaid renderer.

## Регресс и перенос change

Запускать через Python среды TamarixTests (PyYAML 6.0.3 установлен по frozen lock):

```sh
../../TamarixTests/.venv/bin/python tools/archive_gate.py check \
  --tests ../../TamarixTests --change CHANGE --report /absolute/path/results.json
../../TamarixTests/.venv/bin/python tools/archive_gate.py archive \
  --tests ../../TamarixTests --change CHANGE --report /absolute/path/results.json \
  --operation-id CHANGE-RUN-ID
```

Для другого checkout передать `--store /absolute/path/store`. Нужен завершённый
полный PASS окончательного tests commit после promotion. Русская сводка, JSON
и manifest должны относиться к одному прогону; collected/executed IDs, source
revisions/hashes и criterion links сверяются до изменения specs/переноса change.
Диагностический выбор и пропущенные/не начавшиеся случаи archive не закрывают.
Новый docs gate сохраняет эти проверки регресса.

Wrapper сохраняет report/manifest/registry/русскую сводку и regression evidence
в change; `docs-review.json` и `docs-snapshot.json` переносятся вместе с ним, а
их SHA-256 записываются в `regression-evidence.json` и запись операции. Крупные артефакты
остаются в каталоге прогона со ссылками/hashes в отчёте.
`.archive-operations/<id>.json` позволяет продолжить частичный delta merge или
перенос без второго archive. Изменившиеся report/review требуют нового operation ID;
изменившиеся test/service revisions требуют нового прогона.

## CI и исторические архивы

```sh
python3 tools/docs_check.py check
../../TamarixTests/.venv/bin/python tools/archive_gate.py validate-archives --base BASE_SHA
```

Workflow [archive-evidence.yml](../.github/workflows/archive-evidence.yml) проверяет
текущие docs и любой добавленный/изменённый/удалённый archive-файл относительно
base, включая Git rename и удаление только evidence. Для **каждого нового** archive
обязательны полный review, совпадающие change/snapshot hashes и фактическое
обновление docs относительно сохранённого baseline. Сохранённый текст каждого
snapshot независимо проходит структурную проверку обязательных страниц,
русского prose, fenced blocks, Mermaid и внутренних Markdown ссылок/anchors.
Ссылки исторического snapshot на specs, код и двоичные assets не проверяются
по текущему дереву: эти файлы могли измениться после archive; wrapper проверяет
их существование в актуальных docs до переноса change.

Для batch `archive A → обновление docs → archive B` текущие docs должны
совпасть **хотя бы с одним** snapshot новых archives. Snapshot A сохраняет
прежнюю версию; сравнивать его с финальными docs B не требуется. Если новый
archive один, любое последующее изменение docs без нового snapshot блокирует CI.
Git не задаёт порядок нескольких archives внутри одного commit: CI не объявляет
совпавший snapshot хронологически последним. Обёртка перед каждым archive отдельно
сверяет snapshot с текущей документацией. Прямой вызов `openspec archive` без
этих evidence блокируется CI; CLI OpenSpec сам проектный wrapper не вызывает.

Архивы, существовавшие в base до введения docs evidence, не требуют его задним
числом. Позднейшие docs changes не сравниваются с историческими docs hashes.
При правке архива, уже содержащего docs evidence, `docs-review.json`,
`docs-snapshot.json` и их hash-поля в regression evidence должны побайтно
соответствовать base; даже самосогласованная замена текста и всех hashes
запрещена. Дополнительно проверяются snapshot change и целостность review. Проверки
существующего regression evidence сохраняются. Исторические архивы не переписываются.

Для публичного `TamarixS/tamarix-specs` job `archive-evidence` установлен как
required check main от GitHub Actions app 15368, strict/enforce_admins включены
по [evidence T-2](../openspec/changes/archive/2026-10-15-t-2-e2e-tests/github-required-check-evidence.json).
При переносе в другой remote policy настраивается и подтверждается отдельно;
наличие workflow само по себе не устанавливает branch protection.
