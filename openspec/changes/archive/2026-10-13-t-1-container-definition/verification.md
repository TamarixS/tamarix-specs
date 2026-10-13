# Verification Report: t-1-container-definition

Дата проверки: **2026-10-12**, Europe/Moscow. Store: `tamarix-specs`.
Схема: `spec-driven`. Область: принятое логическое ядро пяти сервисов,
локальные контракты поставщиков фактов и сквозные тестовые адаптеры.

**Все применимые проверки пройдены. Изменение готово к архивированию
в согласованном логическом scope.**

## Summary

| Dimension | Status |
| --- | --- |
| Completeness | Task Completion: 31/31; Spec Coverage: 29/29 ADDED Requirements |
| Correctness | Requirement Implementation Mapping: 29/29; Scenario Coverage: 91/91; 336 тестов прошли |
| Coherence | Design Adherence и Code Pattern Consistency подтверждены во всех пяти сервисах; ADR 0001–0003 соблюдены |

CRITICAL: **0**. WARNING: **0**. SUGGESTION: **0**.
Пропущенных применимых проверок / Not verified: **0**.
REMOVED / RENAMED Requirements: **0 / 0**.

## Проверенные источники

- CLI `openspec status --change t-1-container-definition --json --store tamarix-specs`
  и `openspec instructions apply --change t-1-container-definition --json --store tamarix-specs`.
  Артефакты доступны; task tracking включён; недоступных tracking files нет;
  агрегированный прогресс — 31/31, remaining 0.
  Статус apply `all_done` использован как свидетельство чекбоксов, отдельно от результата verification.
- [Proposal](proposal.md), [design](design.md), [tasks](tasks.md), четыре delta specs,
  [requirements](requirements.md), [среда](python-environment.md),
  [логические контракты](logical-contracts.md) и [test-evidence.json](test-evidence.json).
  Заготовки основных entity specs не принимались за нормативные требования.
- Центральные AGENTS/config, применимые context docs и принятые ADR 0001–0003.
- Фактические `src/`, `tests/`, manifests, pins, locks и README пяти сервисов.
  Три независимых read-only review сверили WHEN/THEN с кодом и assertions:
  контейнеры/сущности, управление моделями, вычисление доступа.
  Замечаний и пропущенных применимых проверок в этих областях нет.

## Completeness

| Проверка | Результат и основание |
| --- | --- |
| Task Completion | Verified: все 31 описанная задача отмечены выполненными; CLI использует единственный доступный tracking file tasks.md |
| Spec Coverage | Verified: все 29 требований находятся под ADDED; реализация каждого определена в таблицах ниже |

| Capability | ADDED Requirements | Scenarios |
| --- | --- | --- |
| containers | 14 | 42 |
| entities/subjects | 2 | 5 |
| entities/objects | 2 | 5 |
| authorization/access-check | 11 | 39 |
| Всего | **29** | **91** |

Состав Requirements/Scenarios актуальных delta specs точно совпадает с
прослеживаемостью test-evidence.json. Каждая обязательная ссылка разрешается
в существующий pytest node ID; `ADM` проверен отдельно в каждом из трёх сервисов,
`ADM*` развёрнут по назначению сценария. Сбор тестов 2026-10-12 совпадает
с сохранённым inventory: 336 случаев, из них 16 сквозных.

## Correctness

| Проверка | Результат и основание |
| --- | --- |
| Requirement Implementation Mapping | Verified: 29/29 требований сопоставлены с текущими реализациями; расхождений с intent не найдено |
| Scenario Coverage | Verified: 91/91 сценариев имеют содержательные assertions, включая варианты таблиц; все относящиеся к scope тесты прошли |

Точные Scenario → repository/test/node ID находятся в test-evidence.json
и таблицах tasks.md. Независимые review проверяли условия и ожидаемый результат,
а не только совпадение названий тестов.

### Привязка требований к коду

Обозначения в ссылках:
CS — container-adm-api; SUB — entity-subject-adm-api;
OBJ — entity-object-adm-api; PAM — policy-adm-api; PDP — policy-decision-api.
Каждая ссылка указывает на фактический файл и строку текущего рабочего каталога.

### containers

| Requirement | Текущая реализация |
| --- | --- |
| Упорядоченное дерево контейнеров | [CS/core.py:48](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:48), [CS/core.py:115](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:115) |
| Пропуск уровней и тип корня | [CS/core.py:59](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:59) |
| Строковый ключ контейнера | [CS/facts.py:65](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/facts.py:65) |
| Уникальная идентификация составным ключом | [CS/core.py:72](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:72), [CS/core.py:103](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:103), [CS/core.py:107](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:107), [CS/facts.py:38](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/facts.py:38) |
| Единственный контейнер-держатель модели | [PAM/core.py:40](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:40), [PAM/facts.py:107](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/facts.py:107) |
| Необязательное наличие моделей | [PAM/core.py:54](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:54) |
| Допустимая область субъектов модели | [PAM/core.py:89](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:89) |
| Допустимая область объектов модели | [PAM/core.py:102](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:102) |
| Два типа обращений с явной адресацией | [CS/facts.py:83](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/facts.py:83), [CS/core.py:144](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:144) |
| Сертификатное подтверждение представляемого контейнера | [CS/core.py:161](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:161) |
| Полные права владельца на управление | [CS/core.py:144](/Users/mfedotenko/Projects/Tamarix/container-adm-api/src/container_adm_api/core.py:144), [SUB/core.py:92](/Users/mfedotenko/Projects/Tamarix/entity-subject-adm-api/src/entity_subject_adm_api/core.py:92), [OBJ/core.py:73](/Users/mfedotenko/Projects/Tamarix/entity-object-adm-api/src/entity_object_adm_api/core.py:73), [PAM/core.py:146](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:146) |
| Область адресации управления | [SUB/core.py:116](/Users/mfedotenko/Projects/Tamarix/entity-subject-adm-api/src/entity_subject_adm_api/core.py:116), [OBJ/core.py:85](/Users/mfedotenko/Projects/Tamarix/entity-object-adm-api/src/entity_object_adm_api/core.py:85), [PAM/core.py:169](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:169) |
| Область управляемых моделей и сущностей | [SUB/core.py:118](/Users/mfedotenko/Projects/Tamarix/entity-subject-adm-api/src/entity_subject_adm_api/core.py:118), [OBJ/core.py:89](/Users/mfedotenko/Projects/Tamarix/entity-object-adm-api/src/entity_object_adm_api/core.py:89), [PAM/core.py:171](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:171) |
| Сохранение инвариантов при управлении | [SUB/core.py:108](/Users/mfedotenko/Projects/Tamarix/entity-subject-adm-api/src/entity_subject_adm_api/core.py:108), [OBJ/core.py:94](/Users/mfedotenko/Projects/Tamarix/entity-object-adm-api/src/entity_object_adm_api/core.py:94), [PAM/core.py:161](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:161), [PAM/core.py:174](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:174) |

### entities/subjects

| Requirement | Текущая реализация |
| --- | --- |
| Единственный контейнер-держатель субъекта | [SUB/facts.py:32](/Users/mfedotenko/Projects/Tamarix/entity-subject-adm-api/src/entity_subject_adm_api/facts.py:32), [SUB/core.py:28](/Users/mfedotenko/Projects/Tamarix/entity-subject-adm-api/src/entity_subject_adm_api/core.py:28) |
| Сохранение держателя субъекта при использовании в модели | [SUB/core.py:46](/Users/mfedotenko/Projects/Tamarix/entity-subject-adm-api/src/entity_subject_adm_api/core.py:46), [PAM/core.py:94](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:94) |

### entities/objects

| Requirement | Текущая реализация |
| --- | --- |
| Единственный контейнер-держатель объекта | [OBJ/facts.py:31](/Users/mfedotenko/Projects/Tamarix/entity-object-adm-api/src/entity_object_adm_api/facts.py:31), [OBJ/core.py:30](/Users/mfedotenko/Projects/Tamarix/entity-object-adm-api/src/entity_object_adm_api/core.py:30) |
| Сохранение держателя объекта при использовании в модели | [OBJ/core.py:40](/Users/mfedotenko/Projects/Tamarix/entity-object-adm-api/src/entity_object_adm_api/core.py:40), [PAM/core.py:102](/Users/mfedotenko/Projects/Tamarix/policy-adm-api/src/policy_adm_api/core.py:102) |

### authorization/access-check

| Requirement | Текущая реализация |
| --- | --- |
| Отдельный субъект проверки доступа | [PDP/core.py:86](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:86), [PDP/facts.py:175](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/facts.py:175) |
| Адресация проверки относительно объекта | [PDP/core.py:116](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:116) |
| Отсутствие общей привязки субъекта к адресату | [PDP/core.py:107](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:107) |
| Полная цепочка моделей до контейнера объекта | [PDP/core.py:140](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:140), [PDP/facts.py:212](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/facts.py:212), [PDP/facts.py:253](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/facts.py:253) |
| Нейтральность модели вне области субъекта | [PDP/core.py:56](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:56) |
| Объединение подходящих правил модели | [PDP/core.py:24](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:24) |
| Нейтральная трактовка неопределённого результата модели | [PDP/core.py:70](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:70), [PDP/core.py:40](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:40) |
| Приоритет запрета в цепочке моделей | [PDP/core.py:40](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:40) |
| Запрет по умолчанию | [PDP/core.py:53](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:53) |
| Запрет при неизвестном составе цепочки | [PDP/core.py:141](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:141) |
| Административные права не подменяют доступ субъекта | [PDP/core.py:134](/Users/mfedotenko/Projects/Tamarix/policy-decision-api/src/policy_decision_api/core.py:134) |

### Проверенные смысловые границы

- Родство основано на действительных parent-связях. Матрица типов 4×4,
  четыре типа корня, пропуски и соседние ветки проверены отдельно.
  Составной ключ включает все существующие узлы пути и не фиксирует wire-разделитель.
- Допуск обоих видов обращения требует явных C/O и проверенного сертификатного
  факта с зарегистрированной DN→O. Подтверждения достаточно для владельца;
  дополнительная роль или наличие модели не нужны.
- Административные ядра получают D из собственной авторитетной записи.
  Обе области O ≼ C ≼ D, держатели и ссылки проверяются до save.
  Отказные assertions подтверждают отсутствие записи и сохранение исходного состояния.
- H(S) ≼ M и M ≼ H(Q) проверяются по структурным отношениям.
  Ссылки сохраняют исходные entity records, content, holders и идентичность ссылок.
  Сквозные тесты соединяют реальные операции сервисов.
- Проверяемый S отделён от O/DN; адресация требует C ≼ R.
  Общего H(S) ≼ C и ограничения O относительно пути объекта нет.
  Административные права не дают субъекту автоматического разрешения.
- Путь root→R и все модели каждого его контейнера устанавливаются до вычисления.
  Участвуют оба конца, предки C, пустые группы и несколько моделей узла;
  соседние ветки исключены.
- Неизвестный путь/полный список даёт Deny до evaluator даже при доступном Allow.
  Неопределённый результат известной модели обрабатывается отдельно:
  Allow + Undefined без Deny даёт Allow.
- Deny имеет приоритет внутри определённых подходящих правил и в цепочке моделей.
  Первый Allow не завершает цепочку. Только Neutral/Undefined и отсутствие моделей
  дают default Deny. Вне области субъекта модель Neutral и evaluator не вызывается.
- Некорректные обязательные входы и неуспех обязательных фактов не подменяются
  Undefined модели. Регрессия вложенного нехешируемого subject key проверена до
  допуска и чтения фактов.

## Coherence

| Проверка | Результат и основание |
| --- | --- |
| Design Adherence | Verified: карта сервисов, структурные отношения, отдельный допуск, проверки до записи, полный состав до вычисления, два оператора и локальные fact ports соответствуют design/ADR |
| Code Pattern Consistency | Verified: пять src-пакетов с локальными facts/ports/core, Protocol и явными результатами; согласованные pins; runtime-импортов соседних сервисов нет |

DTO потребителя проверяет форму claim, а реальное родство и полноту источника
подтверждает поставщик. Complete/Unknown не подменяются пустым ответом.
Локальные варианты ошибок сохраняют согласованную семантику отказов.
Операции content update сохраняют держателя как границу метода;
нормативный запрет будущего переноса держателя не вводится.

Runtime-зависимости пяти пакетов пусты. В manifest, pin и фактической среде
сохранены Python 3.15.0 final, uv/uv_build 0.12.24, pytest 9.1.1;
`prerelease = "disallow"`. Согласованность manifest/lock подтверждена
свежим `uv lock --check`, без выбора новых версий.
OpenSpec остаётся store-only: в сервисах только pointer, локальных specs/changes нет.
DDL/Alembic задачи в этом scope отсутствуют; их ответственность остаётся в db-control.

## Команды и результаты на 2026-10-12

В каждом из пяти рабочих каталогов выполнены:

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest --collect-only -q
uv tool run --from uv==0.12.24 uv lock --check
```

Все команды завершились с exit 0.

| Рабочий каталог | Полный запуск pytest | Collect-only |
| --- | --- | --- |
| container-adm-api | 94 passed in 0.04s | 94 tests collected in 0.01s |
| entity-subject-adm-api | 32 passed in 0.03s | 32 tests collected in 0.01s |
| entity-object-adm-api | 28 passed in 0.03s | 28 tests collected in 0.01s |
| policy-adm-api | 72 passed in 0.06s | 72 tests collected in 0.03s |
| policy-decision-api | 110 passed in 0.09s | 110 tests collected in 0.04s |
| Всего | **336 passed**, failed/skipped 0 | **336 случаев** |

Python/pytest фактически **3.15.0 / 9.1.1** во всех пяти средах.
Четыре contract cases находятся в policy-adm-api,
двенадцать — в policy-decision-api.

Дополнительные проверки:

- `openspec validate t-1-container-definition --strict --json --store tamarix-specs`:
  exit 0, valid true, issues [].
- `git diff --check -- openspec/context openspec/changes/t-1-container-definition`:
  exit 0.
- SHA-256 всех включённых source/test/manifest/lock/pin/README/config файлов,
  change inputs и wheel/sdist совпадают с evidence от 2026-10-10.
  Добавленных или исчезнувших source/test файлов относительно снимка нет.
  Свидетельство сборки — успешные команды от 2026-10-10 и проверенные неизменные артефакты.
- Статические AST-импорты src не содержат ссылок на внутренние пакеты соседних сервисов.
- До добавления этого отчёта все **198** локальных Markdown targets context/change
  разрешались; ссылочная проверка итогового отчёта выполнена при сохранении.
- Точные идентификаторы каждого актуального теста сопоставлены с inventory и
  обязательными Scenario-ссылками; пропущенных или неизвестных идентификаторов нет.

Проверены рабочие каталоги; результат не приписывается несуществующему commit
кодовых репозиториев. Идентификация исходников — SHA-256 снимки в test-evidence.json.
Код, tasks и прежнее evidence во время verification сохранены; добавлен этот отчёт.

## Issues by Priority

### CRITICAL — 0

Не выявлены.

### WARNING — 0

Не выявлены.

### SUGGESTION — 0

Не выявлены.

## Область применимости результата

Все шесть применимых проверок этой схемы выполнены; Not verified — 0.
Реальные API/PKI/trust, wire-форматы и AuthZEN, физическое хранение,
актуальность и конкурентная атомарность, конкретные движки и ошибки отдельных
правил, deployment исключены принятым proposal/design и требуют отдельных
изменений. Они не учитываются как пропущенные проверки текущего логического scope.

## Final Assessment

**Все проверки согласованного логического scope пройдены. CRITICAL — 0,
WARNING — 0, SUGGESTION — 0. t-1-container-definition готов к архивированию.**
