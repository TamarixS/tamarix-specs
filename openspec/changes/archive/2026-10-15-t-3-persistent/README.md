# Архив T-3-persistent

Change завершён и архивирован 2026-10-15 через проектную обёртку archive.
Все 54 задачи закрыты; 81 новый case включён в постоянный regression.
Готовый итоговый прогон после promotion: **101/101 PASS**.

Основные specifications синхронизированы: `containers`, `entities/subjects`,
`entities/objects`, `attributes`, `access-model/models`,
`authorization/access-check`. Проверены 60 requirements, сохранены
незатронутые блоки и дословные Purpose новых capabilities.

- [Фактический итоговый отчёт](run-results.json)
- [Русская сводка](run-summary.md)
- [Manifest проверенных версий](run-manifest.json)
- [Regression registry snapshot](regression-registry.yaml)
- [Evidence обёртки](regression-evidence.json)
- [Завершение archive и проверки слияния](archive-completion.json)
- [Результаты реализации до archive](verification.md)

Archive использовал готовый отчёт и не запускал тесты. Исходники и стабильные
ID тестов остаются в TamarixTests. Внутреннее хранение моделей, privileges,
actions, непустые model references/cleanup и полноценный persistent PDP
сохраняются для следующего отдельного change.
