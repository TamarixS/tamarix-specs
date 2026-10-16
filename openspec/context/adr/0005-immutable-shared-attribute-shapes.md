# ADR 0005: неизменяемые переиспользуемые формы атрибутов

- Дата: 2026-10-16.
- Статус: **accepted** для модели и реализации согласованного change.
- Источник принятия: пользователь выбрал общие переиспользуемые shapes вместо
  правил непосредственно в definitions, добавил shape.key для выбора формы,
  подтвердил его контракт и явно вызвал `openspec-apply` для подготовленного
  `t-5-persistant-change-1`. Это разрешает реализацию согласованного design;
  production deployment и неподтверждённые будущие правила этим не разрешаются.
- Change: [t-5-persistant-change-1](../../changes/t-5-persistant-change-1/requirements.md),
  [design](../../changes/t-5-persistant-change-1/design.md).
- Область: `attributes`, DDL/routines/views/migrations в `db-control`,
  PostgreSQL integration в `TamarixTests`; прежние границы сервисов сохраняются.

## Проблема

T-3 хранит правила атрибута в definitions и копирует профиль/версию сравнения
в четыре семейства instances. Такая схема защищает используемую семантику FK,
но новые параметры валидации пришлось бы размножать. Нужен общий именованный
контракт формы и сохранение локальных CHECK/FK/индексов типизированных values.

## Решение

`attributes.shapes` хранит id, key, value_type, cardinality, comparison_profile
и comparison_version. Key обязателен, неизменяем, имеет длину 1–512 символов
`[A-Za-z0-9_-]` и глобальную уникальность без учёта ASCII регистра. Зарегистрированная
строка immutable целиком даже до использования; БД запрещает изменение любых
полей. Новая семантика требует отдельного shape с новыми id и key.

Definition сохраняет собственные id/key, явную применимость и точный shape_id.
Один shape явно выбирается несколькими definitions. Две именованные формы могут
иметь одинаковые текущие параметры: semantic dedup и UNIQUE по tuple не вводятся.
Families/latest/current/наследование отсутствуют; key не является плавающей ссылкой.

Instances сохраняют definition_id/shape_id/type/cardinality с NOT NULL и двумя FK:
`(definition_id,shape_id) → definitions(id,shape_id)` и
`(shape_id,value_type,cardinality) → shapes(id,value_type,cardinality)`.
Обе ссылки имеют UPDATE/DELETE RESTRICT. Первая замораживает точную привязку
при любом instance, в том числе empty set и retained tombstone. Вторая доказывает
правильность structural copies. Values сохраняют прежние typed columns,
FK, CHECK, partial scalar unique и deferred проверку ровно одного значения.

Comparison fields физически принадлежат только shape. Общий закрытый validator
и equality trigger получают immutable shape; fencing обновляет конкретный instance,
а не shared shape. Native equality, exact/Unicode/DN, DER и derived DN keys,
SERIALIZABLE/CAS/retry и исходный expected_revision сохраняются.

Новые SQL routines register_shape/register_definition_with_shape/bind_unused_shape
принадлежат глобальному catalog operator. Старые register_definition и
change_unused_semantics остаются совместимыми wrappers. Новая регистрация
string/DN требует явную поддерживаемую comparison_version; legacy wrappers
сохраняют разрешение optional version через registry. Семантический no-op
legacy change не заменяет shape и не создаёт лишнюю запись.

## Альтернативы

- Хранить правила только в definitions: проще каталог, но пользователь выбрал
  независимые переиспользуемые формы.
- Убрать все type/cardinality copies: локальные typed CHECK/partial unique
  пришлось бы заменить дополнительным процедурным протоколом.
- Копировать каждый будущий validator в instances: сохраняет прежний паттерн,
  но не решает расширяемость. Выбран гибрид с минимальными structural copies.
- Автодедупликация по семантике: не соответствует выбранному явному reuse и
  преждевременно объединяет независимо именованные формы; отклонена в этом scope.

## Переход и восстановление

Новая revision `20261016_0004` следует за `20261015_0003`; исторические SQL
не переписываются. Атомарный upgrade в обслуживаемом окне создаёт отдельный
`migrated_definition_<id>` shape для каждого прежнего definition и сохраняет
точные comparator versions, IDs, payload/DN keys, applicability и revisions.
Перед ALTER TABLE выполняются pending deferred scalar checks. Views сохраняют
прежние column signatures через явные JOIN projections; новые shape views отдельны.

Сбой до commit откатывает transaction. После commit действуют fix-forward
и отдельно подготовленное backup/PITR recovery. Reverse до 0003 разрешён только
в disposable `tamarix_t3_*` и теряет новую информацию shape id/key/sharing.
Нынешний CLI downgrade до base не является production recovery.

## Проверка и ограничения

Приёмка требует component migration/constraints/ACL/concurrency и реальных
PostgreSQL integration cases с постоянными IDs, русскими descriptions, manifest
и отдельными отчётами. Accepted ADR не доказывает PASS или состояние deployment;
фактические команды и результаты фиксируются в tasks/evidence change.

Regex/length/range и их параметры, JSON/framework правил, UI, business HTTP,
новые зависимости и PostgreSQL major upgrade остаются за scope. Численные lock
budgets, объём и длительность окна, backup/PITR runbook уточняются перед deployment.
Процедуры docs/archive из ADR 0004 и AGENTS продолжают действовать.
