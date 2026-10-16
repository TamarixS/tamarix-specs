# Design

## Context and sources

Companion оформляет центральную часть уже реализуемого локального
[post-archive-deployment](../../../../../TamarixCD/openspec/changes/post-archive-deployment/design.md).
Прочитаны центральные AGENTS/config, context README, architecture-principles,
technology-stack, service-architecture, data-architecture, security/testing,
реестр ADR и руководство из восьми страниц. Проверены `tools/archive_gate.py`,
`tools/docs_check.py`, CD `ci/post_archive.py`, локальные proposal/design/tasks,
verification и реальные тесты. Основание — явный запрос пользователя 2026-10-16;
новый стек, production topology или предметная capability не вводятся.

## Ownership and contract

Gate владеет проверкой готового report/docs evidence и переносом центрального
change. Логика archive(), её API и прежние проверки не меняются. Единственная
точка интеграции — CLI main после результата `state=complete`: поэтому один
вызов покрывает новый archive и оба ранних завершения resume.

`run_post_archive(store, operation_id, config)` вычисляет соседний TamarixCD,
выбирает default `artifacts/post-archive.json` либо явный файл и передаёт driver
argv `run --archive-record PATH --config PATH` через текущий Python без shell.
Отсутствие default config даёт NOT_CONFIGURED для store-only среды. Отсутствие
явно выбранного config даёт FAIL после archive, сохраняя запрос доставки явным.
Read-only CLI actions и импортируемая функция archive() этот порт не вызывают.

Driver остаётся в TamarixCD. Он проверяет immutable archive inputs, сериализует
доставку, сохраняет backup, выполняет db-control upgrade и service rollout.
Эти решения, source snapshots, lock/recovery и demo2 не дублируются здесь.

## Failure and evidence

Gate принимает только exit0 + JSON object со `status=PASS`; успешный ответ
возвращается отдельным `deployment`. Любой другой ответ даёт ненулевой CLI exit
с сообщением о завершённом archive и неподтверждённом rollout. Сырой stderr и
driver error не пересылаются; существующий локальный CD report может указываться
в сообщении. Отказ доставки не переписывает `.archive-operations` и исторические
report/manifest/review/snapshots. Повтор прежнего operation ID снова достигает
driver, который отвечает за resume и live check завершённой доставки.

Ни archive gate, ни hook не инициируют test runner. Полный предметный regression
root запускает отдельно в пределах явного запроса перед центральным archive.
Результат фиксирует окончательные commits CD/tests/services/db-control и
актуальный migration fingerprint; CD component PASS/live readiness его не
заменяют. Исходный docs baseline до правок —
`38c5af8f9c9c40db0f3ba66fbe0b00b5ab0e9dc4`.

## Alternatives

Wrapper только в CD оставил бы существующий центральный archive CLI без доставки.
Перенос deployment planning в центральный store нарушил бы принятое CD ownership.
Вызов внутри archive() изменил бы read-only API consumers и потребовал бы покрыть
каждый resume return отдельно. Выбран общий CLI hook и этот узкий companion;
локальный CD change и его specs остаются в TamarixCD.

## Traceability and validation

| Согласованный критерий | Владелец и реальные проверки |
| --- | --- |
| CD-ARCHIVE-01 / HOOK-01..04 | `TamarixCD/tests/test_archive_hook.py`: new/resumed completion, default/explicit config, read-only/rejection, exit/JSON/redaction; центральные `tests/test_archive_gate.py` сохраняют coverage прежнего archive API |
| CD-ARCHIVE-02 | CD dependency: `tests/test_post_archive.py::test_inputs_bind_completed_archive_to_frozen_manifest`, `::test_rollout_orders_exact_build_backup_migration_preservation_and_health`, `::test_export_uses_committed_blobs_and_preserves_modified_checkout` |
| CD-ARCHIVE-03 | CD dependency: `tests/test_prepare_sources.py::test_exact_commit_overrides_common_and_individual_branches_without_checkout`, `::test_commit_export_keeps_exact_object_when_refs_move_and_replacements_exist`; `tests/test_deploy_commits.py::test_commit_and_branch_flags_reach_source_preparation_literally` |
| CD-ARCHIVE-04 | CD dependency: `tests/test_post_archive.py::test_failed_migration_or_legacy_preservation_never_starts_new_services`, `::test_migration_failure_report_redacts_credentials_and_keeps_backup` |
| CD-ARCHIVE-05 | CD dependency: `tests/test_post_archive.py::test_partial_retry_reuses_build_and_backup_then_completes_same_versions`, `::test_complete_retry_checks_live_state_without_rebuilding_or_restarting`, `::test_changed_binding_rejects_same_operation_before_runtime_access`, `::test_environment_lock_rejects_parallel_owner_and_releases_after_failure` |
| CD-ARCHIVE-06 | CD dependency: `tests/test_demo_data.py::test_dataset_has_new_names_shared_shapes_and_independent_applicability`, `::test_readback_rejects_drift`, `::test_repeated_seed_skips_writes_but_still_rejects_readback_drift`, `::test_decimal_normalization_preserves_difference_beyond_context_precision`; live readback принадлежит локальному CD change |

Полные параметризованные IDs, команды, описания и outcomes CD сохраняются в
[его verification](../../../../../TamarixCD/openspec/changes/post-archive-deployment/verification.md).
Новая domain delta и promotion записей registry этим companion не требуются;
центральный gate всё равно принимает полный существующий regression, а не
выборочный CD report. До archive root дополнит tasks фактическими командами,
immutable commits и путём нового завершённого report, затем refresh/review docs.
