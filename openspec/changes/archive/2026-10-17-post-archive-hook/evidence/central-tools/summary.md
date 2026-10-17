# Проверки TamarixCD

Прогон: 9aa7e003f633449cb4e04b92db79abd2. Итог: **PASS**.
Начало: 2026-10-16T20:40:19.993917+00:00. Конец: 2026-10-16T20:41:15.728850+00:00.
Длительность: 55.736 с. Python: 3.15.0.

Запрошено: ../Tamarix/tamarix-specs/tests/test_archive_gate.py, ../Tamarix/tamarix-specs/tests/test_docs_check.py, -q, --tb=short.
Собрано: 105. Статусы: {'PASS': 105}.

- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_current_full_promoted_report_passes: PASS. Полный PASS двух случаев на чистых commits допускается; задаёт позитивный контроль проверки evidence.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[missing]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[fail]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[skip]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[xfail]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[not-run]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[incomplete]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[partial]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[partial-collection]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_report_preserves_change_without_hidden_execution[diagnostic-selection]: PASS. При непригодном отчёте ожидает GateError и неизменный активный change.

Причина каждого случая пояснена у параметров; применяется для защиты
от ложного PASS, потери change и незаказанного неявного запуска тестов.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_stale_inputs_block_gate[tests-revision]: PASS. Меняет один проверяемый вход и ожидает GateError; защищает привязку прогона к конкретным версиям и spec hashes.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_stale_inputs_block_gate[registry-hash]: PASS. Меняет один проверяемый вход и ожидает GateError; защищает привязку прогона к конкретным версиям и spec hashes.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_stale_inputs_block_gate[service-revision]: PASS. Меняет один проверяемый вход и ожидает GateError; защищает привязку прогона к конкретным версиям и spec hashes.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_stale_inputs_block_gate[source-hash]: PASS. Меняет один проверяемый вход и ожидает GateError; защищает привязку прогона к конкретным версиям и spec hashes.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_stale_inputs_block_gate[spec-hash]: PASS. Меняет один проверяемый вход и ожидает GateError; защищает привязку прогона к конкретным версиям и spec hashes.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_stale_inputs_block_gate[delta-hash]: PASS. Меняет один проверяемый вход и ожидает GateError; защищает привязку прогона к конкретным версиям и spec hashes.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_stale_inputs_block_gate[manifest-hash]: PASS. Меняет один проверяемый вход и ожидает GateError; защищает привязку прогона к конкретным версиям и spec hashes.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_russian_descriptions_and_promotion_required[registry-description]: PASS. Обновляет вход и полный report согласованно, затем ожидает отказ по отсутствующему русскому описанию или promotion.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_russian_descriptions_and_promotion_required[test-docstring]: PASS. Обновляет вход и полный report согласованно, затем ожидает отказ по отсутствующему русскому описанию или promotion.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_russian_descriptions_and_promotion_required[promotion]: PASS. Обновляет вход и полный report согласованно, затем ожидает отказ по отсутствующему русскому описанию или promotion.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_open_task_blocks_before_archive: PASS. При незавершённой задаче даже полный PASS не архивируется; защищает критерии завершения change.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_partial_operation_resumes_and_completed_is_idempotent[before-move]: PASS. Сохраняет частичную операцию, продолжает её тем же входом и повторяет завершённую без второго archive; защищает безопасный retry.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_partial_operation_resumes_and_completed_is_idempotent[after-move]: PASS. Сохраняет частичную операцию, продолжает её тем же входом и повторяет завершённую без второго archive; защищает безопасный retry.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_operation_id_rejects_changed_report: PASS. После завершения меняет run ID отчёта: прежний operation ID отвергается; защищает привязку операции к неизменяемому входу.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_direct_archive_without_evidence_is_rejected: PASS. Перемещает change напрямую без evidence и коммитит: CI gate должен отказать; контролирует обход обёртки archive.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archive_ci_rejects_corrupted_evidence[report-hash]: PASS. Создаёт полный archive и портит один артефакт: ожидает CI GateError; защищает целостность и завершённость archived evidence.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archive_ci_rejects_corrupted_evidence[registry-hash]: PASS. Создаёт полный archive и портит один артефакт: ожидает CI GateError; защищает целостность и завершённость archived evidence.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archive_ci_rejects_corrupted_evidence[tasks]: PASS. Создаёт полный archive и портит один артефакт: ожидает CI GateError; защищает целостность и завершённость archived evidence.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archive_ci_rejects_corrupted_evidence[source-spec-hash]: PASS. Создаёт полный archive и портит один артефакт: ожидает CI GateError; защищает целостность и завершённость archived evidence.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_real_openspec_lifecycle_and_archived_ci: PASS. В одноразовой репе выполняет candidate → promotion commit → final PASS → настоящий OpenSpec archive и CI проверку.

Runtime-прогон представлен реалистичным fixture report; ожидается один archive
с согласованными snapshots. Применяется для проверки настоящего CLI и lifecycle tooling.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_requirement_evolution_archives_against_target_specs[modified]: PASS. Проверяет prospective target traceability и итоговый CI для MODIFIED/RENAMED/REMOVED через настоящий OpenSpec в временном store.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_requirement_evolution_archives_against_target_specs[renamed]: PASS. Проверяет prospective target traceability и итоговый CI для MODIFIED/RENAMED/REMOVED через настоящий OpenSpec в временном store.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_requirement_evolution_archives_against_target_specs[removed]: PASS. Проверяет prospective target traceability и итоговый CI для MODIFIED/RENAMED/REMOVED через настоящий OpenSpec в временном store.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_report_summary_integrity_and_errors_required[summary-missing]: PASS. При отсутствующей/нерусской сводке, потерянных hashes или ошибках ожидает GateError; защищает полный достоверный отчёт выполнения.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_report_summary_integrity_and_errors_required[summary-english]: PASS. При отсутствующей/нерусской сводке, потерянных hashes или ошибках ожидает GateError; защищает полный достоверный отчёт выполнения.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_report_summary_integrity_and_errors_required[artifact-hashes-cleared]: PASS. При отсутствующей/нерусской сводке, потерянных hashes или ошибках ожидает GateError; защищает полный достоверный отчёт выполнения.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_report_summary_integrity_and_errors_required[report-errors]: PASS. При отсутствующей/нерусской сводке, потерянных hashes или ошибках ожидает GateError; защищает полный достоверный отчёт выполнения.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_empty_or_missing_active_tasks_rejected[empty]: PASS. При пустом/отсутствующем tasks ожидает отказ до вызова CLI и сохранение активного change; закрывает ошибку all([]).
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_empty_or_missing_active_tasks_rejected[missing]: PASS. При пустом/отсутствующем tasks ожидает отказ до вызова CLI и сохранение активного change; закрывает ошибку all([]).
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_empty_or_missing_archived_tasks_rejected[empty]: PASS. Меняет только tasks уже принятого archive и ожидает GateError; защищает CI от исчезновения критериев завершения.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_empty_or_missing_archived_tasks_rejected[missing]: PASS. Меняет только tasks уже принятого archive и ожидает GateError; защищает CI от исчезновения критериев завершения.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_deleting_only_required_archived_artifact_rejected[report-only-deleted]: PASS. После полного archive удаляет один обязательный файл и ожидает GateError; защищает проверку diff, содержащего только D записи.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_deleting_only_required_archived_artifact_rejected[evidence-only-deleted]: PASS. После полного archive удаляет один обязательный файл и ожидает GateError; защищает проверку diff, содержащего только D записи.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_deleting_only_required_archived_artifact_rejected[summary-only-deleted]: PASS. После полного archive удаляет один обязательный файл и ожидает GateError; защищает проверку diff, содержащего только D записи.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archive_ci_rejects_english_summary_with_matching_hash: PASS. Подменяет archived сводку английской и согласованно обновляет hashes: ожидает отказ CI по отсутствию русского описания отчёта.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_incomplete_changed_criterion_coverage_rejected[added-criterion-uncovered]: PASS. Добавляет новый критерий в delta, оставляя остальные links и PASS согласованными; ожидает GateError для неполной traceability затронутых критериев.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_incomplete_changed_criterion_coverage_rejected[modified-criterion-uncovered]: PASS. Добавляет новый критерий в delta, оставляя остальные links и PASS согласованными; ожидает GateError для неполной traceability затронутых критериев.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_ci_rejects_incomplete_final_delta_merge: PASS. Даёт полный PASS и links двух критериев, но CLI fixture пропускает delta merge; ожидает отказ CI по итоговым основным specs.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_partial_cli_spec_merge_resumes_before_archive_move: PASS. CLI успевает применить корректную delta, затем падает до перемещения change; retry должен закончить archive с прежним неизменным report.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_docs_review_blocks_archive_before_any_mutation[missing-docs-review]: PASS. Делает review непригодным согласно описанию параметра и ожидает отказ без вызова OpenSpec и изменения активного change; защищает docs lifecycle.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_docs_review_blocks_archive_before_any_mutation[stale-docs]: PASS. Делает review непригодным согласно описанию параметра и ожидает отказ без вызова OpenSpec и изменения активного change; защищает docs lifecycle.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_docs_review_blocks_archive_before_any_mutation[stale-change]: PASS. Делает review непригодным согласно описанию параметра и ожидает отказ без вызова OpenSpec и изменения активного change; защищает docs lifecycle.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_ci_rejects_new_archive_without_docs_review: PASS. Удаляет docs-review и его hash из нового archive при полном regression evidence; CI обязан отказать и закрыть обход прямым OpenSpec CLI.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_ci_rejects_deleting_previous_docs_evidence: PASS. В уже принятом archive удаляет docs-review и hash одновременно; CI видит прежнее evidence в base и запрещает ослабление завершённого gate.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_later_docs_updates_do_not_invalidate_historical_archive: PASS. После успешного archive меняет docs и проверяет CI с историческим base без новых archives; прежние hashes остаются историческими и не требуют переписывать архив.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_existing_legacy_archive_does_not_require_retroactive_docs_review: PASS. Моделирует archive прежней версии без docs evidence в base, затем меняет только его tasks; CI сохраняет прежний regression gate без навязывания нового review задним числом.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_ci_accepts_two_sequential_archives_with_distinct_docs_snapshots: PASS. Архивирует A, затем обновляет docs и архивирует B, проверяя общий base до обоих; CI должен принять оба immutable snapshots при текущем docs B.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_ci_rejects_stale_docs_after_single_new_archive: PASS. После единственного нового archive меняет docs без нового review; CI относительно исходного base должен отказать, даже если сохранённый snapshot структурно корректен.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_ci_rejects_self_consistent_rewrite_of_historical_docs_evidence[rewrite-review-hashes]: PASS. Подделывает прежние docs evidence согласно описанию параметра и пересчитывает связанные hashes; ожидается отказ CI по неизменяемости исторического snapshot относительно base.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_ci_rejects_self_consistent_rewrite_of_historical_docs_evidence[rewrite-content-and-all-hashes]: PASS. Подделывает прежние docs evidence согласно описанию параметра и пересчитывает связанные hashes; ожидается отказ CI по неизменяемости исторического snapshot относительно base.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_component_pass_completes_only_component_criterion_coverage: PASS. Полный db-control PASS дополняет один DB-only criterion при неизменном полном integration наборе.

Проверяет валидные source snapshots/provenance и точную связь с artifact;
component test не добавляется в integration registry или его счётчики.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[missing-report]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[tampered-report]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[failed-case]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[missing-node]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[missing-collection]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[missing-run-start-provenance]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[mismatched-commit]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[mismatched-resource]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[invalid-criterion-link]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_invalid_component_evidence_blocks_gate[stale-test-source]: PASS. Портит дополнительное evidence согласно параметру и требует отказа gate без скрытого запуска тестов.

Кроме raw tamper/missing, пересчитывает внешние hashes: это доказывает
проверку смысла PASS, provenance, конкретного node и ссылки, а не одного SHA.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_component_report_cannot_replace_missing_integration_case: PASS. Валидный component bundle не допускает неполный integration report; исходная защита полного регресса сохраняется.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archived_component_evidence_validates_without_source_checkouts: PASS. После archive удаляет db-control и tests checkout; CI принимает сохранённые sources и prospective archived delta.

Проверка доказывает независимость исторического component evidence от
локального пути manifest и доступности рабочей копии исходного runner.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archived_component_snapshot_cannot_be_deleted[component-evidence.json]: PASS. Удаление любого из component evidence/report/summary отклоняется CI; каждое имя параметра — обязательный snapshot bundle.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archived_component_snapshot_cannot_be_deleted[component-results.json]: PASS. Удаление любого из component evidence/report/summary отклоняется CI; каждое имя параметра — обязательный snapshot bundle.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archived_component_snapshot_cannot_be_deleted[component-summary.md]: PASS. Удаление любого из component evidence/report/summary отклоняется CI; каждое имя параметра — обязательный snapshot bundle.
- Tamarix/tamarix-specs/tests/test_archive_gate.py::test_archived_component_evidence_cannot_be_rewritten_self_consistently: PASS. Переписывает сохранённый component report и все внешние hashes; CI отклоняет изменение уже принятого immutable snapshot.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_complete_review_passes_in_clean_checkout: PASS. Фиксирует обновлённые docs и review, затем ожидает PASS на чистом checkout; подтверждает сохранение baseline после commit.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_invalid_documentation_is_rejected[missing-page]: PASS. Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_invalid_documentation_is_rejected[broken-local-link]: PASS. Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_invalid_documentation_is_rejected[absolute-link]: PASS. Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_invalid_documentation_is_rejected[unknown-source-root]: PASS. Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_invalid_documentation_is_rejected[missing-mermaid]: PASS. Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_invalid_documentation_is_rejected[unclosed-fence]: PASS. Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_invalid_documentation_is_rejected[empty-mermaid]: PASS. Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_invalid_documentation_is_rejected[unknown-mermaid-type]: PASS. Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_source_links_work_without_sibling_ci_checkouts: PASS. Ссылка на объявленный service checkout отсутствует в store-only CI и допускается с явным списком пропущенных source ссылок.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_present_source_checkout_requires_existing_link_target: PASS. При доступном соседнем checkout ссылка на отсутствующий файл должна давать отказ; проверка находит устаревшие ссылки исходников локально.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_stale_or_incomplete_review_is_rejected[stale-proposal]: PASS. Меняет один вход уже завершённого review и ожидает отказ; различающиеся причины перечислены у параметров и защищают свежесть evidence.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_stale_or_incomplete_review_is_rejected[stale-delta]: PASS. Меняет один вход уже завершённого review и ожидает отказ; различающиеся причины перечислены у параметров и защищают свежесть evidence.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_stale_or_incomplete_review_is_rejected[stale-page]: PASS. Меняет один вход уже завершённого review и ожидает отказ; различающиеся причины перечислены у параметров и защищают свежесть evidence.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_stale_or_incomplete_review_is_rejected[missing-section]: PASS. Меняет один вход уже завершённого review и ожидает отказ; различающиеся причины перечислены у параметров и защищают свежесть evidence.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_stale_or_incomplete_review_is_rejected[pending-review]: PASS. Меняет один вход уже завершённого review и ожидает отказ; различающиеся причины перечислены у параметров и защищают свежесть evidence.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_stale_or_incomplete_review_is_rejected[english-reason]: PASS. Меняет один вход уже завершённого review и ожидает отказ; различающиеся причины перечислены у параметров и защищают свежесть evidence.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_stale_or_incomplete_review_is_rejected[false-changed-pages]: PASS. Меняет один вход уже завершённого review и ожидает отказ; различающиеся причины перечислены у параметров и защищают свежесть evidence.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_prepare_preserves_baseline_and_requires_new_review_on_refresh: PASS. Повторный prepare без флага отказывает, refresh после commit сохраняет исходный SHA и сбрасывает решения; предотвращает тихое переподтверждение docs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_tooling_change_without_actual_docs_update_is_rejected: PASS. Новый docs-only/tooling change на неизменных docs обязан обновить хотя бы страницу; полный reviewed checklist не заменяет фактический diff.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_archived_review_keeps_historical_docs_hashes: PASS. После перемещения change и последующего редактирования docs historical review проходит без current snapshot, новый archive с тем же evidence отказывает.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_broken_local_heading_anchor_is_rejected: PASS. Ссылка на существующий Markdown с отсутствующим заголовком должна блокироваться; проверка защищает навигацию между разделами документации.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_tooling_review_can_update_one_page_and_review_remaining_sections: PASS. Для tooling change обновляет development и оставляет семь разделов reviewed с русским обоснованием; ожидается PASS без предметных delta specs.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_historical_snapshot_requires_valid_content_not_only_declared_hashes[missing-content-snapshot]: PASS. Проверяет сохранённый текст без сравнения с current docs: случай указан у параметра, ожидается отказ для отсутствующего, повреждённого или структурно неверного snapshot.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_historical_snapshot_requires_valid_content_not_only_declared_hashes[content-hash-mismatch]: PASS. Проверяет сохранённый текст без сравнения с current docs: случай указан у параметра, ожидается отказ для отсутствующего, повреждённого или структурно неверного snapshot.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_historical_snapshot_requires_valid_content_not_only_declared_hashes[snapshot-without-russian-prose]: PASS. Проверяет сохранённый текст без сравнения с current docs: случай указан у параметра, ожидается отказ для отсутствующего, повреждённого или структурно неверного snapshot.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_historical_snapshot_requires_valid_content_not_only_declared_hashes[empty-mermaid-in-snapshot]: PASS. Проверяет сохранённый текст без сравнения с current docs: случай указан у параметра, ожидается отказ для отсутствующего, повреждённого или структурно неверного snapshot.
- Tamarix/tamarix-specs/tests/test_docs_check.py::test_historical_snapshot_requires_valid_content_not_only_declared_hashes[broken-snapshot-link]: PASS. Проверяет сохранённый текст без сравнения с current docs: случай указан у параметра, ожидается отказ для отсутствующего, повреждённого или структурно неверного snapshot.


[JSON](results.json) · [pytest log](pytest.log) · [JUnit](junit.xml)
