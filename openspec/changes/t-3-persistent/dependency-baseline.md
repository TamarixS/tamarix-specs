# T-3: dependency baseline и внешняя PostgreSQL test dependency

Дата повторной проверки официальных источников: 2026-10-15.
Область: задачи 1.3–1.4 [tasks.md](tasks.md), технический подход [design.md](design.md).

## Статус

Ниже зафиксированы выбранные pins T-3 с сохранением принятого Python/uv
baseline. Проверены официальные релизы, resolver, frozen install и импорты
db-control/пяти сервисов. Реальные миграции upgrade/repeated upgrade/
disposable downgrade-upgrade и ограничения runtime roles прошли на PostgreSQL
18.6; функциональные feature/race/DN acceptance продолжаются отдельно.
Это не итоговый integration evidence всего T-3.

## Фактическая проверка реализации

- `db-control` и пять сервисов: `uv lock --check`, `uv sync --frozen`, Python
  3.15.0, SQLAlchemy 2.1.4, Psycopg 3.3.6 с implementation `binary`,
  libpq 180006; Alembic 1.20.0 в db-control. `pyproject.toml`, `uv.lock`,
  `.python-version` согласованы, прежние Python/uv/pytest pins сохранены.
- Локальный CD change создан и реализуется по отдельному явному разрешению
  пользователя: [postgresql-integration](../../../../../TamarixCD/openspec/changes/postgresql-integration/proposal.md),
  [контракт executor/readiness](../../../../../TamarixCD/openspec/changes/postgresql-integration/design.md).
  Его незавершённые задачи не объявляются завершёнными центральным change.
- Реальная среда `f263aaf8dce94140aeda313a6a39437b`: отдельный Compose project
  `tamarix-pg-f263aaf8dce94140aeda313a6a39437b`, БД
  `tamarix_t3_f263aaf8dce94140aeda313a6a39437b`, PostgreSQL 18.6 Debian,
  `server_version_num=180006`, UTF8, `block_size=8192`, Unicode 16.0,
  `casefold('Straße')='strasse'`. Все шесть предметных/catalog/reader LOGIN
  проверены отдельными TCP-соединениями. DSN и passwords находятся только
  в private env JSON вне reports; публичны лишь имена env.
- Официальный образ `postgres:18.6`, фактический digest
  `sha256:74935e72241653ca55e0414067e6d8763aceb8a810eb51b452253ec3dcfc4336`,
  platform `linux/arm64`. [Публичный state среды](../../../../../TamarixCD/reports/postgresql/f263aaf8dce94140aeda313a6a39437b/results.json)
  подтверждает READY и Alembic head `20261015_0003`. Это рабочая среда проверки;
  manifest чистых окончательных commits ещё требуется перед итоговым прогоном.
- Deployment executor: `.venv/bin/python -m db_control upgrade --dsn-env
  TAMARIX_TEST_ADMIN_DSN`. Version table `public.alembic_version`.
  CLI возвращает JSON `heads`, не печатает DSN/SQL/пароли. Test logins
  provision-ит отдельная disposable-only команда того же владельца DDL.
- [Migration component report](../../../../db-control/reports/9fac3af90b25460bbc26f82cd95f154a/summary.md):
  полный `tests/component/test_migrations.py`, 11 PASS. До исправления CASE
  expression были сохранены отдельные неуспешные отчёты; они не используются
  как подтверждение успешного upgrade.
- D145 использует `pg_unicode_fast`, зафиксированный major/Unicode fingerprint
  и version `d145-pg18-unicode16.0-v1`. DN имеет отдельные исторические таблицы
  Unicode 3.2 и version `dn-rfc5280-u32-t61-v1`; корректность codec проверяется
  отдельными DN cases, без подмены современным casefold.

## 1. Проверенные версии и основание выбора

| Компонент | Pin / статус в T-3 | Подтверждение официального источника |
| --- | --- | --- |
| Python | 3.15.0 final; существующий принятый baseline | [Python 3.15.0](https://www.python.org/downloads/release/python-3150/) явно обозначен стабильным релизом от 2026-10-09. Смена версии для T-3 не предлагается. |
| uv | 0.12.24; существующий принятый baseline | [Astral release 0.12.24](https://github.com/astral-sh/uv/releases/tag/0.12.24), опубликован 2026-10-08. Это сохранение проектного pin, а не утверждение о новейшем доступном uv. |
| SQLAlchemy | SQLAlchemy==2.1.4; кандидат | [Официальная страница релизов](https://www.sqlalchemy.org/download.html) указывает 2.1.4 от 2026-10-07 как current release; ветка 2.0 находится в maintenance. |
| Psycopg 3 | psycopg[binary]==3.3.6; кандидат | [Release notes](https://www.psycopg.org/psycopg3/docs/news.html) относят 3.3.6 к current release и отмечают поддержку Python 3.15. Раздел 3.3.7 помечен unreleased и в pin не входит. |
| Alembic | alembic==1.20.0; кандидат | [Changelog](https://alembic.sqlalchemy.org/en/latest/changelog.html) датирует 1.20.0 2026-09-11; у 1.20.1 отсутствует дата релиза. Минимум SQLAlchemy для 1.20.0 — 2.0.0. |
| PostgreSQL | 18.6; кандидат сервера и тестового образа | [Официальная таблица поддерживаемых версий](https://www.postgresql.org/support/versioning/) указывает 18.6 как current minor ветки 18. Версия 19 представлена как beta и исключена. |

Psycopg binary выбран для локальной разработки/проверок, поскольку
он поставляет собственные клиентские библиотеки. [Руководство установки](https://www.psycopg.org/psycopg3/docs/basic/install.html)
различает его с pure-Python установкой, которой нужен локальный libpq, и с
локальной C-сборкой, которой дополнительно нужен pg_config. Доступность binary
wheel для CPython 3.15/macOS arm64 подтверждена frozen install;
документация не является свидетельством наличия нужного wheel в локальной среде.
Точный psycopg-binary, libpq и транзитивные версии фиксируются lock и manifest
фактической установки, без незаметной замены выбранной реализации.

Для SQLAlchemy/Alembic опубликованные версии дают основание собрать кандидатный
набор; успешный resolver сам по себе не доказывает работу транзакций/DDL на нём.
Существующие pytest/PyYAML/uv_build pins сохраняются, пока задача не требует их
отдельного согласованного изменения. PostgreSQL major upgrade не смешивается
с baseline Alembic migration.

## 2. Что требуется для подтверждения совместимости

1. В репозиториях-владельцах согласовать новые прямые зависимости с сохранением
   Python 3.15.0/uv 0.12.24 и зафиксировать pyproject.toml, uv.lock и
   .python-version. Сначала проверять uv lock --check, затем uv sync --frozen;
   обычная установка не должна обновлять lock.
2. Зафиксировать фактические версии Python/uv/пакетов и Psycopg implementation /
   libpq после установки. При недоступном binary wheel не подменять реализацию
   или Python без отдельного решения.
3. Проверить миграции db-control на PostgreSQL 18.6, UTF8, block_size не менее
   8192; проверить наличие используемых normalize/casefold/pg_unicode_fast и
   зафиксировать фактическую Unicode/profile version. Поддержка функций
   устанавливается запросом к реальному серверу, а не только номером major.
4. После готовности reporting wrapper выполнить согласованные component и
   integration задачи с отдельными summary.md/results.json каждого прогона.
   Успех импорта/SELECT 1 не подменяет migration/concurrency acceptance.

Этот список сохраняет критерии совместимости. Подтверждённые установки,
импорты и migration checks перечислены в начале; оставшиеся feature/race
проверки не считаются выполненными на основании установки.

## 3. Исходное состояние TamarixCD до отдельного разрешения

Read-only проверка выполнена для checkout
/Users/mfedotenko/Projects/TamarixS/TamarixCD, HEAD
c37933127b83c93aa726111d52db7a0fb987ec54. git status --short был пуст.

В openspec/changes найдены только service-launch-pipeline и
external-test-runner. Change для postgresql-integration **не обнаружен**;
ссылки на якобы созданный change или его готовый результат нет.

Текущий ci/external_tests.py:

- допускает только logical-integration и http;
- строит manifest для пяти сервисных пакетов;
- записывает migrations: null;
- использует HTTP health readiness для http и не имеет PostgreSQL readiness.

Это рабочие старые границы инструмента, а не готовая среда T-3. Ранее отмеченное
отсутствие Docker daemon не сохраняется как актуальный blocker: root-агент
сообщил об успешном запуске Docker Desktop и docker info 29.8.2. Настоящий
PostgreSQL 18.6 и его image digest этим сообщением не подтверждаются.

## 4. Первоначальный план локальной CD dependency

Имя отдельно разрешённого **локального** change TamarixCD:
postgresql-integration. План ниже сохранён как исходная граница; актуальный
результат и ссылки указаны выше. Генерация его planning выполняется
отдельно в TamarixCD без --store tamarix-specs по правилам его AGENTS.md.
Центральный документ сам не разрешает edits CD: основание — отдельный ответ
пользователя о создании и реализации этого локального change.

Ожидаемый результат — явная подготовка/остановка только принадлежащей прогону
одноразовой PostgreSQL среды, migration executor, DB readiness и совместимый
manifest для расширенного TamarixTests runner. Автозапуск tests при up/commit/
archive и изменение существующего service-launch-pipeline не требуются.

Планируемые файлы **в TamarixCD**, не созданные этим документом:

| Файл | Ожидаемое изменение |
| --- | --- |
| openspec/changes/postgresql-integration/.openspec.yaml, proposal.md, design.md, tasks.md | Локальные артефакты, создаваемые будущим OpenSpec workflow. Не объявлять заранее готовыми или принятыми; необходимость delta specs определяется его instructions. |
| compose.postgresql.yaml | Новый изолированный PostgreSQL-only Compose definition, без DDL/Alembic и без присоединения к данным существующей среды. |
| ci/postgresql_environment.py | Новый явный lifecycle/readiness helper с безопасным run ID, отслеживанием собственных ресурсов, migration subprocess и cleanup/cancellation reporting. |
| ci/external_tests.py | Поддержка postgresql-integration scope и вызов helper; прежние logical-integration/http команды сохраняют контракт. |
| ci/EXTERNAL_TESTS.md | Подготовка среды, secret env, manifest, границы и ручные команды; не выдумывать уже реализованные CLI flags. |
| tests/test_postgresql_environment.py | Новые CD tooling tests с русскими описаниями: isolation, readiness, migration failure, cancellation и cleanup только своих ресурсов. |
| tests/test_external_tests.py | Проверки нового manifest/scope и совместимости старых режимов, сохранения отчётов и секретов вне артефактов. |

Точный интерфейс новых helper-команд согласуется в этом будущем локальном
change; таблица описывает требуемый контракт, а не существующие executable API.

## 5. Контракт образа, executor, секретов и manifest

### Образ и изоляция

Кандидат исходного tag: docker.io/library/postgres:18.6.
[Первичный реестр Docker Official Images](https://raw.githubusercontent.com/docker-library/official-images/master/library/postgres)
содержит этот tag и архитектуру arm64v8; источник сборки указан как
docker-library/postgres commit e00e1bd34ec5c8a8e7ad89b273b3d42efaf6d5bc,
directory 18/trixie. **Этот Git commit не является digest образа.**

Перед реальным запуском CD разрешает tag в registry digest и фиксирует
immutable docker.io/library/postgres@sha256 digest вместе с фактической
platform и локальным image ID. В этом документе digest **не получен**;
подставной sha256 не приводится. Manifest без подтверждённого digest
не считается готовым acceptance evidence. Обновление tag/digest — новый
вход прогона, а не молчаливая замена в старом отчёте.

На каждый прогон — отдельный безопасный Compose project, например
tamarix-pg-<run-id>, собственные labels/DB/volume/network и loopback endpoint
со свободным портом. Конкретная схема именования принимается локальным CD
change. Ни global prune, ни удаление чужих volumes, ни использование рабочей
БД допускаются. Многосоединительные cases получают отдельную БД случая либо
прогона с гарантированным cleanup; единый rollback fixture недостаточен для
коммитящих конкурентных транзакций.

### Migration executor

CD отвечает за подготовку PostgreSQL и запуск поставленного db-control
из фиксированного commit/frozen environment. **Только db-control** содержит
DDL, Alembic config/revisions и миграционные проверки; CD/TamarixTests не
создают схему самостоятельно и не вызывают ORM create_all.

До миграции executor подтверждает одноразовую целевую БД и preflight исходной
схемы. Применяется Alembic upgrade head и затем сравнивается фактический head
с ожидаемым. Команду и DSN env executor нужно связать с реально поставленным
entry point/config db-control; существование такого entry point здесь
не утверждается. Нельзя до этой сверки объявить выдуманную CLI команду
или env читаемыми инструментом. Migration credentials не выдаются runtime
адаптерам. Downgrade/upgrade acceptance разрешён только в одноразовой БД.

Readiness выполняется поэтапно: Docker health и соединение, SELECT 1,
фактическая server version 18.6, UTF8/block_size/Unicode capabilities,
завершённая миграция и разрешённые views/routines/roles. Только после этого
запускается запрошенный набор TamarixTests. /health пяти HTTP контейнеров
не является readiness этой DB границы.

### Предлагаемые secret env имена

| Env | Назначение |
| --- | --- |
| TAMARIX_TEST_ADMIN_DSN | Привилегированный executor/fixture lifecycle одноразовой БД, только подготовка/cleanup. |
| TAMARIX_TEST_CONTAINER_DSN | Реальная предметная роль container adapter. |
| TAMARIX_TEST_SUBJECT_DSN | Реальная предметная роль subject adapter. |
| TAMARIX_TEST_OBJECT_DSN | Реальная предметная роль object adapter. |
| TAMARIX_TEST_MODEL_DSN | Реальная предметная роль model metadata adapter. |
| TAMARIX_TEST_CATALOG_DSN | Ограниченная роль оператора каталогов. |
| TAMARIX_TEST_READER_DSN | Read-only роль подготовленного snapshot reader. |

Имена являются предложенным контрактом. DSN для самого migration entry point
согласуется с db-control до реализации, с явным mapping от admin env. Значения
не передаются в CLI/manifest/registry/logs/evidence; ошибки соединения
редактируются так, чтобы исключить credentials. Отчёт может записать имя
env и факт его предоставления, но не значение. Для negative role tests нельзя
подменять все роли привилегированным admin connection.

### Предлагаемое расширение manifest

Существующие version/hash provenance поля сохраняются. Новые поля согласуются
одновременно CD producer и TamarixTests validator, без отключения проверки
исторических logical-integration/http manifests.

| Данные | Требование к значению |
| --- | --- |
| environment.scope | postgresql-integration; уровень случаев integration, не HTTP e2e. |
| environment.id / database isolation ID | Реальный run/DB identifier и platform без credentials. |
| PostgreSQL version/image | Фактические server version/number, exact image reference + digest и platform; не один tag. |
| db-control provenance | Полный commit SHA и источник используемого migration артефакта/lock hash. |
| migrations | Ожидаемый и фактически применённый Alembic head, отличающийся от null старого логического режима. |
| Python/dependencies | Фактические Python, SQLAlchemy, Psycopg implementation/version/libpq, Alembic, lock hashes и Unicode/profile version. |
| services/tests/store/cd | Полные immutable revisions; source/distribution/module и spec/delta hashes сохраняют текущий provenance contract. Неприменимые HTTP endpoints явно null. |
| DSN sources | Только согласованные env имена/присутствие, не DSN и не пароль. |

Форма расширения/schema version выбирается в локальном CD change совместно
с validator; имя scope и обязательность DB provenance не разрешают
подсунуть DB facts старому validator, который сейчас их не поддерживает.

## 6. Условия получения результата внешней dependency

Задача 1.3 получает реальную ссылку/commit только после создания и review
локального CD change. Для integration запуска T-3 нужны установленный
candidate baseline, неизменяемый образ, успешный executor/readiness и
совместимый manifest из фактической среды. Отсутствующие артефакты остаются
открытой зависимостью; ручной JSON с неподтверждёнными версиями её не закрывает.

Reporting wrapper должен быть готов **до** первого project test/collection.
Каждый component/integration/CD прогон формирует уникальный run каталог,
русскую summary.md и results.json при PASS/FAIL/ошибке среды/collection/отмене;
NOT_RUN отличается от SKIP, незавершённый snapshot не считается PASS.
Orchestration report CD не заменяет case report TamarixTests. Эти условия
сохраняются при новом scope и не запускают тесты автоматически.
