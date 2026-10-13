# Verification Report: t-1-container-definition

Дата проверки: **2026-10-13**, Europe/Moscow. Store: `tamarix-specs`.
Схема: `spec-driven`. Проверены текущие `master` пяти сервисов и центрального store.
Область — согласованное логическое ядро, локальные Protocol и сквозные тестовые адаптеры.

**Все применимые проверки пройдены. T-1 готов к архивированию в согласованном логическом scope.**

## Summary

| Dimension | Status |
| --- | --- |
| Completeness | Task Completion: 31/31; Spec Coverage: 29/29 ADDED Requirements |
| Correctness | Requirement Implementation Mapping: 29/29; Scenario Coverage: 91/91; 336 тестов прошли |
| Coherence | Design Adherence: все 7 решений соблюдены; Code Pattern Consistency подтверждена в пяти сервисах; ADR 0001–0003 соблюдены |

CRITICAL: **0**. WARNING: **0**. SUGGESTION: **0**.
Пропущенных применимых проверок / Not verified: **0**.
MODIFIED / REMOVED / RENAMED Requirements: **0 / 0 / 0**.

## Источники и состояние

Прочитаны [proposal](proposal.md), [design](design.md), [tasks](tasks.md),
все четыре delta specs, [requirements](requirements.md),
[среда](python-environment.md), [логические контракты](logical-contracts.md),
AGENTS/config, применимый постоянный context и ADR 0001–0003.
Прослеживаемость из [исторического evidence](test-evidence.json) повторно сверена
с актуальными specs, фактическими assertions и свежими результатами тестов.
Три независимых read-only review проверили контейнеры/модели,
субъекты/объекты и вычисление доступа. Замечаний не найдено.

CLI status и instructions apply использованы для определения схемы, артефактов
и агрегированных задач. `all_done` не принимался за результат verification.
Task tracking включён; все 31 описанная задача доступны; unavailable tracking files отсутствуют.
Исторические сведения tasks об отсутствии исходников и промежуточных неуспехах
установки рассматривались на дату записи, отдельно от текущего состояния.

| Репозиторий | Проверенный HEAD master | Pytest | Сквозные случаи |
| --- | --- | --- | --- |
| container-adm-api | `34da5c9` | 94 passed | 0 |
| entity-subject-adm-api | `1f8e434` | 32 passed | 0 |
| entity-object-adm-api | `5f203b2` | 28 passed | 0 |
| policy-adm-api | `ceedc53` | 72 passed | 4 |
| policy-decision-api | `822a151` | 110 passed | 12 |
| Всего | — | **336 passed** | **16** |

Store проверен на master `f27e76c`. SHA-256 текущих файлов, полные revisions,
выход команд и pytest node IDs сохранены в
[verification-evidence-2026-10-13.json](verification-evidence-2026-10-13.json).
Исходники и тесты T-1 совпадают с исходными T-1 commits во всех пяти сервисах.
Все девять change inputs из исторического evidence также неизменны.
Из включённых в прежний snapshot файлов изменился только README сервиса контейнеров;
его текущий hash записан в новом evidence.

## Completeness

| Проверка | Результат |
| --- | --- |
| Task Completion | Verified: 31/31, remaining 0; документальные задачи 1–2 и результаты реализации согласованы с принятой областью |
| Spec Coverage | Verified: 29/29 ADDED Requirements имеют фактическую реализацию |

| Capability | ADDED Requirements | Scenarios |
| --- | --- | --- |
| containers | 14 | 42 |
| authorization/access-check | 11 | 39 |
| entities/subjects | 2 | 5 |
| entities/objects | 2 | 5 |
| Всего | **29** | **91** |

Точные тройки Capability / Requirement / Scenario совпадают с прослеживаемостью.
Каждый обязательный node ID присутствует среди прошедших тестов свежего запуска.
Повторения ADM проверены во всех трёх административных сервисах;
ADM* развёрнут согласно назначению сценария. Inventory совпадает с 336 случаями
исторического evidence; новых, исчезнувших или пропущенных случаев нет.

## Correctness

| Проверка | Результат |
| --- | --- |
| Requirement Implementation Mapping | Verified: 29/29 требований соответствуют intent актуальных delta specs |
| Scenario Coverage | Verified: 91/91 WHEN/THEN имеют содержательные assertions; все относящиеся к scope тесты прошли |

Проверка покрытия включала ожидаемые результаты и сохранение состояния при отказе,
а не только совпадение названий тестов. Ссылки Scenario → repository/test/node ID
находятся в новом evidence и таблицах tasks.md.

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

| Решение design | Подтверждение |
| --- | --- |
| 1. Предметная ответственность сервисов | CS — дерево/ключи/DN; entity-сервисы — их факты/держатели; PAM — модели/ссылки/полный набор; PDP — решение. DDL и access-assignment не входят в задачи T-1 |
| 2. Структурное дерево и составные ключи | CS core:48,72,115; реальные parent-связи, допустимый порядок типов, пропуски, полный путь. Ранги и строковый префикс не заменяют родство |
| 3. Подтверждение владельца | CS core:144–165; оба вида обращения требуют явные C/O, подтверждённый сертификатный факт и DN→O; дополнительной роли нет |
| 4. Проверки до изменения | SUB core:74, OBJ core:66, PAM core:146; авторитетный D, O ≼ C ≼ D и инварианты проверяются до save |
| 5. Полный состав до вычисления | PDP core:140–163; root→R и все модели устанавливаются до первого evaluator; unknown даёт Deny |
| 6. Два оператора объединения | PDP core:24–53; Deny имеет приоритет внутри модели и в цепочке; Neutral/Undefined нейтральны; default Deny |
| 7. Локальные логические интерфейсы | facts.py / ports.py / core.py каждого src-пакета; immutable DTO, Protocol, явные Complete/Unknown и отдельные ошибки обязательных фактов |

Design Adherence и Code Pattern Consistency: **Verified**.
Фактический AST src не содержит runtime-импортов внутренних пакетов соседних сервисов.
Межсервисные преобразования ограничены тестовыми адаптерами.
Форма claim проверяется DTO потребителя; истинность родства и полноту источника
подтверждает поставщик, как предусмотрено logical-contracts.md.
Во всех пяти проектах сохранены src-пакеты, согласованные pins и store-only pointers;
локальных specs/changes нет. Runtime dependencies пусты.

## Свежие проверки 2026-10-13

В каждом из пяти каталогов сервисов выполнен полный запуск:

```sh
.venv/bin/python -m pytest -q -p no:cacheprovider --junitxml=/private/tmp/t1-verify-20261013/<repository>.xml
uv tool run --from uv==0.12.24 uv lock --check
```

Все команды завершились с exit 0. JUnit подтверждает **336 passed,
failures 0, errors 0, skipped 0**; из них четыре holder contracts PAM
и двенадцать сквозных flow cases PDP. Полный inventory и результаты каждого
случая сохранены в новом JSON evidence; отдельный collect-only не требовался.

Фактическая среда во всех пяти .venv — **Python 3.15.0 final / pytest 9.1.1**;
проекты доступны как установленные пакеты 0.1.0.
Версия проверяющего uv — **0.12.24**. Манифесты задают uv_build 0.12.24,
requires-python >=3.15,<3.16, prerelease disallow и pytest 9.1.1;
согласованность каждого lock подтверждена свежим uv lock --check.
Новые версии зависимостей не выбирались.

`openspec validate t-1-container-definition --strict --store tamarix-specs`
прошёл с exit 0. Текущее покрытие сценариев и отсутствие чужих runtime-импортов
проверены отдельно от этого структурного валидатора.
Установка/сборка из tasks и test-evidence.json — датированное историческое
свидетельство; они не представлены как повторные команды этого запуска.

## Issues by Priority

### CRITICAL — 0

Не выявлены.

### WARNING — 0

Не выявлены.

### SUGGESTION — 0

Не выявлены.

## Область применимости и Final Assessment

Все шесть применимых проверок выполнены; Not verified — **0**.
Реальные HTTP/API, PKI/trust, wire-форматы, физическое хранение,
актуальность и конкурентная атомарность, конкретные движки и ошибки отдельных
правил, deployment исключены принятым proposal/design. Они не учитываются
как пропущенные проверки согласованного логического scope.

**Все проверки пройдены. CRITICAL — 0, WARNING — 0, SUGGESTION — 0.
t-1-container-definition готов к архивированию в согласованном логическом scope.**

Результат этой verification сохранён в новых датированных report/evidence.
Код, tasks, прежние отчёты/evidence и существовавшие staged изменения сохранены.
