## Context

Прочитаны AGENTS, config, context/README, architecture-principles,
technology-stack, service-architecture, data-architecture, api-guidelines,
security, patterns, testing и реестр ADR 0001–0004 (accepted в их scope).
Проверены основные specs, реализация archive gate/CI и локальные archive skills.
Источники описания продукта: актуальный код пяти сервисов, db-control SQL
revisions 0001–0003, TamarixCD runtime/Compose/CLI, TamarixTests runner/registry,
архив T-3 и его storage-contracts. Старый context местами описывает состояние T-1;
новое руководство явно показывает актуальные T-3 факты и оставшиеся пробелы.

## Goals / Non-Goals

Цель — понятное новичку руководство и исполняемый допуск его актуальности перед
archive. Не меняются бизнес-правила, runtime архитектура, версии зависимостей,
DDL, транспорт или GitHub policy. Основание изменения процесса — прямой запрос
пользователя 2026-10-15; дополнительного принятия архитектуры продукта не нужно.

## Decisions

1. `/docs` означает каталог от корня `tamarix-specs`, рядом с openspec и tools.
   Там восемь обзорных страниц с относительными ссылками на источники. `context`
   сохраняет правила проектирования и историю принятых решений.
2. Агент обновляет текст по завершённому change и проверяет все разделы.
   Python не генерирует предметные описания: он проверяет структуру и evidence.
   Альтернатива простого копирования delta specs не даёт связного руководства;
   одна инструкция без gate не обнаруживает обход archive.
3. `docs-review.json` фиксирует baseline Git commit, SHA-256 входов change и всех
   Markdown docs, фактически изменённые страницы и reviewed/updated с причинами.
   `docs-snapshot.json` хранит полный текст и SHA-256 страниц; review фиксирует
   hash snapshot. Каждый исторический content snapshot валидируется отдельно.
   Повторный prepare сохраняет baseline; refresh требует нового review.
   Хэши подтверждают неизменность проверенных файлов, а смысловую корректность
   документации проверяет агент/reviewer.
4. Docs validation выполняется раньше мутаций wrapper и для новых архивов CI.
   Исторические архивы не требуют нового evidence. В CI проверяется структура
   store/docs; ссылки на соседний checkout проверяются, когда он доступен.
   В batch текущие docs должны совпасть хотя бы с одним новым полным snapshot;
   порядок нескольких archives внутри Git commit не восстанавливается.
   Review/snapshot ранее принятых архивов и их hash-поля immutable относительно base.
5. Config/AGENTS задают постоянное правило; локальные single/bulk skills
   направляют через проектный gate. Прямой OpenSpec CLI сам docs не обновляет;
   обход выявляется CI новых архивов. Required check обеспечивается существующей
   branch policy, её актуальное состояние этим локальным change не меняется.

## Risks / Trade-offs

Автоматическая проверка не доказывает полноту смысла и корректность каждого
Mermaid layout. Нужны review источников и проверка Mermaid parser отдельно.
Изменение входов после review требует обновления evidence. Историческая
snapshot policy не должна сравнивать старые docs hashes с текущими страницами.
Ссылки между репозиториями требуют совместного checkout для чтения исходников.

## Migration Plan

Создать руководство, внедрить docs validator до archive mutation и CI новых
архивов, обновить правила/skills, проверить положительные и отрицательные
сценарии изолированно. Исторические архивы не переписывать. Откат — обычный
revert данного tooling change с сохранением docs, без миграций данных.
