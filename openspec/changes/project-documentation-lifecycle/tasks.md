## 1. Контракт и источники

- [x] 1.1 [tamarix-specs] Зафиксировать scope и критерии приёмки project-documentation до реализации.
- [x] 1.2 [tamarix-specs] Прочитать context/ADR, specs и текущий код сервисов, db-control, CD и Tests.

## 2. Руководство

- [x] 2.1 [tamarix-specs] Создать 8 страниц docs с навигацией, Mermaid и ссылками на источники.
- [x] 2.2 [tamarix-specs] Сверить все таблицы/constraints/indexes, API и ограничения с кодом.
- [x] 2.3 [tamarix-specs] Связать docs с context и корневой точкой входа, разделить исторические TBD и T-3 факты.

## 3. Archive lifecycle

- [x] 3.1 [tamarix-specs] Реализовать docs checker и evidence prepare/refresh/validation.
- [x] 3.2 [tamarix-specs] Добавить docs gate до archive mutation и проверку новых архивов в CI, сохранив regression gate.
- [x] 3.3 [tamarix-specs] Обновить AGENTS/config и single/bulk archive skills; описать реальные команды.

## 4. Проверка

- [x] 4.1 [tamarix-specs] Проверить структурный checker, Mermaid и локальные ссылки созданного руководства.
- [x] 4.2 [tamarix-specs] Прогнать адресные tooling tests с русскими описаниями, сохранить отдельные summary.md/results.json.
- [x] 4.3 [tamarix-specs] Проверить отрицательные archive/CI сценарии в изолированных fixtures без реального archive.
- [x] 4.4 [tamarix-specs] Записать фактическую Requirement/Scenario → test node traceability, команды и результаты.

## Traceability

Полный путь требований: `openspec/changes/project-documentation-lifecycle/specs/project-documentation/spec.md`.
Все тесты принадлежат `tamarix-specs`; параметризованные IDs ниже — фактически
collected/executed случаи итогового отчёта, все PASS.

| Requirement / Scenario | Реальный test node ID |
| --- | --- |
| Полное руководство проекта / Полный комплект документов | `tests/test_docs_check.py::test_complete_review_passes_in_clean_checkout`; содержимое API/БД дополнительно проверено по коду в verification |
| Полное руководство проекта / Неполное руководство | `tests/test_docs_check.py::test_invalid_documentation_is_rejected[missing-page]`, `[broken-local-link]`, `[absolute-link]`, `[unknown-source-root]`, `[missing-mermaid]`, `[unclosed-fence]`, `[empty-mermaid]`, `[unknown-mermaid-type]`; `test_broken_local_heading_anchor_is_rejected` |
| Обновление документации до archive / Актуальное обновление | `tests/test_docs_check.py::test_complete_review_passes_in_clean_checkout`; `test_tooling_review_can_update_one_page_and_review_remaining_sections`; `tests/test_archive_gate.py::test_current_full_promoted_report_passes` |
| Обновление документации до archive / Отсутствующий или устаревший обзор | `tests/test_docs_check.py::test_stale_or_incomplete_review_is_rejected[stale-proposal]`, `[stale-delta]`, `[stale-page]`, `[missing-section]`, `[pending-review]`, `[english-reason]`, `[false-changed-pages]`; `test_tooling_change_without_actual_docs_update_is_rejected`; `tests/test_archive_gate.py::test_docs_review_blocks_archive_before_any_mutation[missing-docs-review]`, `[stale-docs]`, `[stale-change]` |
| Проверка нового архива в CI / Новый архив без documentation evidence | `tests/test_archive_gate.py::test_ci_rejects_new_archive_without_docs_review`; `test_ci_rejects_deleting_previous_docs_evidence` |
| Проверка нового архива в CI / Исторический архив после обновления docs | `tests/test_archive_gate.py::test_later_docs_updates_do_not_invalidate_historical_archive`; `test_existing_legacy_archive_does_not_require_retroactive_docs_review`; `tests/test_docs_check.py::test_archived_review_keeps_historical_docs_hashes` |
| Проверка нового архива в CI / Последовательный batch с разными снимками | `tests/test_archive_gate.py::test_ci_accepts_two_sequential_archives_with_distinct_docs_snapshots`; `test_ci_rejects_stale_docs_after_single_new_archive` |
| Проверка нового архива в CI / Подмена принятого исторического evidence | `tests/test_archive_gate.py::test_ci_rejects_self_consistent_rewrite_of_historical_docs_evidence[rewrite-review-hashes]`, `[rewrite-content-and-all-hashes]`; `tests/test_docs_check.py::test_historical_snapshot_requires_valid_content_not_only_declared_hashes[missing-content-snapshot]`, `[content-hash-mismatch]`, `[snapshot-without-russian-prose]`, `[empty-mermaid-in-snapshot]`, `[broken-snapshot-link]` |

Фактические полные node IDs всех 88 случаев, описания, версии/source hashes
и результаты — в [JSON итогового прогона](verification/tamarix-docs-gate-20261015T200806-88861760/results.json).
Команда, промежуточные результаты и ограничения — в [verification.md](verification.md).
Предметные integration/e2e не меняются; tooling tests не требуют promotion
TamarixTests. Реальное архивирование этого change в задачу не входит.
