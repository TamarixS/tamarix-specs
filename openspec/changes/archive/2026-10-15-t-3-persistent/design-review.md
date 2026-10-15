# Design Review

Дата: 2026-10-15. Область: задача 1.1 [tasks.md](tasks.md).

## Основание и результат

Проверены актуальные [proposal.md](proposal.md), [design.md](design.md),
[requirements.md](requirements.md), все шесть delta specs и план задач,
центральный `AGENTS.md`, принятый контекст T-1 и доступные логические ядра.
Независимый технический review не выявил архитектурного blocker до реализации.
Прежние замечания о freeze версии сравнения и очистке object key guards
учтены в design.

Источник разрешения исполнять подготовленный design — пользовательский вызов
`openspec-apply-change` для `t-3-persistent` после подготовки design и последующее
указание «продолжи». В совокупности с результатом review это основание применять
описанный ниже baseline. Пользователю не приписываются отдельные ответы
«принимаю DN» либо отдельное утверждение каждого механизма. Наличие файлов
planning само по себе не считается принятием. Этот record фиксирует результат
review и источник разрешения реализации, а не завершённость кода или проверок.

## Принятый к исполнению технический baseline

- Одна PostgreSQL БД, предметные схемы и общая `attributes`; физические имена
  из design используются как рабочая конвенция реализации. Все DDL, функции,
  триггеры, роли, views и Alembic revisions принадлежат `db-control`.
- Синхронные SQLAlchemy/Psycopg 3 adapters; одна Session/transaction на application
  command. Administrative writes используют SERIALIZABLE. Проверки admission,
  фактов, исходной expected revision и мутация агрегата выполняются до одного
  commit. SQLAlchemy официально поддерживает синхронный Psycopg dialect:
  [документация](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg).
- Для `40001` и `40P01` принимаются максимум **три полные попытки**, включая
  первоначальную, с новой транзакцией на каждую попытку и исходными входами/CAS
  token. Stale revision не повторяется как свежая команда. Исчерпание попыток
  возвращает явный локальный результат конкурентного конфликта; token клиента
  не заменяется. Число попыток — конкретизация протокола реализации в этом review.
  [PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html).
- Long object key uniqueness использует SHA-256 только для bucket lookup,
  реальный MVCC UPDATE служебной guard row и полное точное сравнение ключей.
  Unique hash-only исключён. Set values сериализуются реальным UPDATE instance
  и сравниваются по type/profile; большой TEXT/NUMERIC не включается целиком
  в обязательный unique B-tree.
- Обычный `unicode_ci` реализует D145 с фиксированной версией Unicode и
  implementation profile. Candidate PostgreSQL `normalize`/`casefold` с явной
  `pg_unicode_fast` проверяется при фиксации stable baseline. Изменение версии
  реализации защищается тем же freeze, что type/cardinality/profile, включая
  пустые instances и retained attributes tombstones. Неподдерживаемая версия
  блокирует запись; upgrade не меняет равенство молча.
  [String functions](https://www.postgresql.org/docs/current/functions-string.html),
  [collations](https://www.postgresql.org/docs/current/collation.html).
- DN принимается как специальный тип значения контейнерного set attribute:
  исходный ASN.1 Name DER в BYTEA, авторитетный DB codec и версионированный
  matching key. Самостоятельного DN registry/binding source нет. Для DN
  закрепляется RFC 5280/RFC 4518 StringPrep с Unicode 3.2, отдельно от D145
  обычных строк. Client matching key не авторитетен; сертификатный Name
  поступает из установленного факта аутентификации.
- Каталоги доступны через ограниченный SQL-интерфейс `catalog_operator`.
  Предметные runtime роли получают свои routines/read-only fact views;
  SECURITY DEFINER routines имеют квалифицированные имена, фиксированный
  search_path и закрытый PUBLIC EXECUTE. Используемые types/definitions/
  applicability защищены RESTRICT. Глобальное каталоговое полномочие
  не предоставляет управление данными контейнеров.
- Initial root и первичный DN provision атомарно отдельный привилегированный
  deployment executor после регистрации доверенного DN definition. Это право
  не следует из имени `db-control`, не предоставляется `catalog_operator`
  и не вводит runtime create-root API. Root без DN допустим. Никакие реальные
  значения initial root, сертификатные идентичности или secrets этим record
  не задаются.
- Subject soft delete/restore сохраняет ID/identity/attributes; container hard
  delete выполняется child-first и purge только tombstones. Lifecycle gate
  и DB guard физического DELETE активного subject обязательны. Object key
  guards очищаются с держателем и не блокируют пустой container delete.
- Полноценный persistent PDP, model internals/references и их cleanup остаются
  следующим change. T-3 хранит metadata моделей и отдельный metadata snapshot;
  он не подменяет CompleteModelSet или модель с Undefined. Будущие ссылки
  нельзя включать без атомарного cleanup и affected model revision enforcement.

Конкретные совместимые pins проверяются в 1.4. Исходная revision/no-op и
локальные DTO/results конкретизируются в 1.2 без добавления HTTP contracts.
Внешняя PostgreSQL/CD среда остаётся отдельной зависимостью 1.3.

## DN codec: матрица и детализация перед 8.1

Для всех поддерживаемых строк после строгого decode применяется один DN
StringPrep profile; значимость пробелов отличается от обычного string D145.
Исходный DER сохраняется независимо от производного matching representation.

| ASN.1 encoding | Поддержка и decode contract |
| --- | --- |
| UTF8String | Поддерживается; строгий UTF-8 без replacement, overlong форм, surrogate или значения вне Unicode scalar range. |
| PrintableString | Поддерживается; проверяется собственный ASN.1 alphabet, затем прямое преобразование в Unicode. |
| BMPString | Поддерживается; строгие 16-битные big-endian значения BMP, без surrogate и нечётной длины. |
| UniversalString | Поддерживается; строгие 32-битные big-endian Unicode scalar values, без surrogate, выхода за диапазон и неполной последней единицы. |
| TeletexString / T61String | Требуется версионированный детерминированный mapping; конкретный candidate ниже необходимо разобрать и проверить перед 8.1. Latin-1/ISO-8859-1 fallback, guessing и replacement запрещены. |

Основание исторического DN preparation:
[RFC 4518 §2](https://www.rfc-editor.org/rfc/rfc4518.html#section-2) задаёт
Unicode 3.2 и полный pipeline, а §2.1 оставляет Teletex→Unicode mapping локальному
профилю. [RFC 5280 §7.1](https://www.rfc-editor.org/rfc/rfc5280.html#section-7.1)
требует StringPrep/caseIgnoreMatch и задаёт структурное равенство Name.
Неуспех подготовки поддерживаемого DirectoryString не переключает его на DER
equality. Для прочих неизвестных значений сохраняется согласованное точное DER
сравнение; неизвестный OID сам по себе не является ошибкой.

**Предложение детализации Teletex codec, ещё не готовая реализация:** профиль
`t61-1988-rfc2157-u32-v1` на T.61 (11/1988) и ISO 2022 state machine из
[RFC 2157 Appendix C](https://www.rfc-editor.org/rfc/rfc2157.html#appendix-C).
Начальные G0/C0/C1 — ISO-IR-102/106/107; G1 — ISO-IR-103 с указанным там
совместимым начальным вызовом верхней половины. Обрабатывать разрешённые
designation/invocation/shift sequences, включая зарегистрированный JIS
ISO-IR-87; переключение возможно внутри строки. Таблицы graphic characters,
non-spacing diacritics и допустимых сочетаний сверять с
[T.61](https://www.itu.int/rec/T-REC-T.61-198811-S/en) и регистрациями
[ISO-IR-102](https://itscj.ipsj.or.jp/ir/102.pdf)/
[ISO-IR-103](https://itscj.ipsj.or.jp/ir/103.pdf).
Для каждого поддерживаемого элемента закрепить Unicode scalar sequence,
источник таблицы и hash/version; не считать ISO 6937 идентичным T.61.

Перед 8.1 этот candidate требует конкретных mapping tables, полного описания
состояний и test vectors для diacritics, переключений и межкодировочного
равенства. Неизвестная sequence, неопределённая позиция или незавершённое
состояние получает явную codec failure, без догадки о символе. Если обнаружена
корректная стандартная последовательность без mapping, codec остаётся
незавершённым: нельзя объявить её некорректной или сузить выбранную семантику.
Этот раздел не выдаёт Teletex→Unicode candidate за единственный mapping,
установленный RFC, или за отдельный пользовательский ответ.

## Review порядка reporting tasks

Сверка 1.5: proposal, шесть delta specs и requirements сохраняют foundation
scope. Локальные команды конкретизированы в storage-contracts.md, исходная
revision 1/no-op/CAS/retry3 не меняют принятую предметную идентичность.
Проверенные pins, отдельный разрешённый CD change и фактическая READY среда
записаны в dependency-baseline.md. Runtime HTTP/PKI, внутренности моделей,
model-reference cleanup и полноценный PDP остаются вне T-3; временных ссылок
или сериализации content в реализации нет. ADR/context не переписывались.
Принятый plain-character T.61 transcode profile и закреплённые источники
описаны в db-control/docs/dn-codec.md; его acceptance подтверждают только
отдельные реальные codec cases, а не этот review.

В плане есть содержательный цикл: 2.3 требует запустить migration component
cases и сохранить отчёт, но общий reporting protocol 2.5 зависит от завершения
2.3–2.4. Первый прогон не должен происходить до готовности отчётов для fail,
collection/environment error и отмены. Это исправление порядка, не новая
возможность или изменение критериев.

Предлагаемая точная перестановка зависимостей с сохранением ID:

1. У 2.5 заменить зависимость `2.3–2.4` на `1.3–1.5, 2.1`; реализовать reporting
   protocol до первых component прогонов. Для него достаточно согласованного
   environment contract; доступность БД для реального прогона проверяется в 2.3.
2. У 2.3 добавить `2.5` к существующим зависимостям `2.2` и доступной среде `1.3`.
3. У 2.4 добавить `2.5` к существующим зависимостям `1.3–1.5, 2.1`, чтобы его
   validator/component проверки также использовали готовый reporting protocol.
4. Исполнять порядок `2.1 -> 2.5`, затем `2.3/2.4` при готовности их остальных
   зависимостей; 2.2 может готовиться параллельно с 2.5. Feature integration
   tasks по-прежнему требуют 2.4 и 2.5.

`tasks.md` этим record не изменён. Ни SQL, ни код, ни тестовые прогоны в рамках
данного review не создавались и не выполнялись.
