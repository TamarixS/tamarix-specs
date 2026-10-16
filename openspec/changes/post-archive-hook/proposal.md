# Proposal

После подтверждённого archive центральный CLI должен передавать сохранённую
operation локальному CD executor. Пользователь 2026-10-16 запросил автоматическую
раскатку после archive, а затем архивирование, commit и merge завершённой работы.
Этот companion change оформляет только центральный вызов и его документацию.
План доставки, миграций и демонстрационных данных остаётся в локальном
[CD change](../../../../../TamarixCD/openspec/changes/post-archive-deployment/proposal.md).

## Scope

- `tools/archive_gate.py`: вызов CD только в CLI `archive` после `state=complete`,
  выбор локальной конфигурации, проверка результата и безопасная ошибка.
- `tools/ARCHIVE_GATE.md`, `docs/operations.md`, `docs/development.md`: поведение
  конфигурации, разделение archive/rollout, retry и неизменность evidence.
- Documentation review всех восьми страниц и готовый полный regression report
  для окончательных immutable commits перед центральным archive.

Этот tooling change не изменяет domain capabilities, DDL, DTO, авторизацию,
сервисный runtime или test registry; предметных delta specs нет. Реализация
backup/migration/build/restart, CD tests и demo2 относится к TamarixCD.

## Acceptance criteria

| Критерий | Наблюдаемый результат | Прослеживаемость |
| --- | --- | --- |
| HOOK-01 | После нового complete archive и обеих resume веток CLI передаёт тот же `.archive-operations/<id>.json` CD executor; Python API `archive()` сохраняет прежнее поведение | CD-ARCHIVE-01; `tests/test_archive_hook.py::test_each_archive_completion_calls_same_cd_hook` |
| HOOK-02 | Без default config возвращается NOT_CONFIGURED без запуска CD; явный существующий путь передаётся одним argv, явный отсутствующий путь даёт FAIL после archive | CD-ARCHIVE-01; `::test_unconfigured_archive_stays_compatible_with_store_only_checkout`, `::test_explicit_config_override_is_passed_as_literal_argv`, `::test_missing_explicit_config_cannot_silently_skip_requested_delivery` |
| HOOK-03 | Только exit0 и JSON object со status PASS подтверждают delivery; сбой/invalid response дают ненулевой CLI exit, complete archive сохраняется, stderr/secret error не пересылаются, существующий report указывается | CD-ARCHIVE-01/04; `::test_failed_or_invalid_cd_response_preserves_archive_and_safe_report`, `::test_unavailable_cd_process_returns_safe_rollout_failure` |
| HOOK-04 | Check, validate-archives и отклонённый archive не вызывают CD; hook не запускает тестовые наборы | CD-ARCHIVE-01; `::test_read_only_cli_actions_do_not_invoke_delivery`, `::test_rejected_archive_never_starts_cd` |

Указанные pytest node IDs принадлежат `TamarixCD/tests/test_archive_hook.py`.
Полные параметризованные node IDs и русские описания сохраняет CD report.
Зависимые CD-ARCHIVE-02..06 проверяют исполнение принятого сообщения в CD и не
переносятся в центральный scope; точная связь приведена в design.

## Readiness

Реализация hook и CD component/live проверки существуют. Их evidence не заменяет
обязательный для центрального archive полный TamarixTests regression на
окончательном CD commit. До готового отчёта и завершённого docs review этот
change остаётся активным; исторический T-5 report не переименовывается и не
переписывается под новые входы.
