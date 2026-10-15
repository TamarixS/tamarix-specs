# Отчёт прогона 20261015T142314-ee85d1c224a3

Итог: **PASS**. Завершён: да.
Начало: 2026-10-15T14:23:14.009337+00:00. Окончание: 2026-10-15T14:24:39.326612+00:00.
Длительность: 85.317 с.

Запрошенный набор: `{"change": "t-3-persistent", "ids": [], "level": null, "regression": false, "bootstrap_empty_regression": false}`.
Собрано node ID: 101; выполнено случаев: 101.
Счётчики: PASS=101, FAIL=0, ERROR=0, SKIP=0, XFAIL=0, XPASS=0, NOT_RUN=0, total=101.

| Test ID | Статус | Время, с | Описание |
| --- | --- | ---: | --- |
| access-empty-chain-denied | PASS | 0.001 | Без моделей на всём пути ожидается запрет по умолчанию; защищает от разрешения пустого набора. |
| access-neutral-chain-denied | PASS | 0.000 | Все известные модели нейтральны: ожидается запрет по умолчанию; защищает отсутствие подходящих разрешений. |
| access-undefined-chain-denied | PASS | 0.000 | Все известные модели завершаются объявленной ошибкой: ожидается запрет; контролирует отсутствие определённых разрешений. |
| access-allow-with-neutral-models | PASS | 0.000 | Модель объекта разрешает, остальные нейтральны: ожидается разрешение; проверяет прохождение разрешения через пять ядер. |
| access-ancestor-deny-precedes-addressed | PASS | 0.000 | Корень запрещает, C и R разрешают: итоговый запрет; контролирует включение предков адресуемого контейнера. |
| access-direct-object-address-keeps-root-deny | PASS | 0.000 | При обращении прямо к R корень запрещает, R разрешает: итоговый запрет; защищает полную цепочку при C=R. |
| access-all-models-of-container-evaluated | PASS | 0.000 | Две модели одного C: разрешающая и с разрешением/запретом; итоговый запрет защищает учёт всех моделей и приоритет запрета. |
| access-descendant-subject-neutralizes-ancestor-models | PASS | 0.000 | Субъект принадлежит R: модели предков вне его области, R разрешает; ожидается разрешение без общей привязки к C. |
| access-known-model-error-keeps-allow | PASS | 0.000 | Известная модель корня даёт ошибку, R разрешает: ожидается разрешение; отличает неопределённый результат от неизвестного состава. |
| access-skipped-levels-keep-real-path | PASS | 0.000 | Organization непосредственно содержит module R; обе модели участвуют и R разрешает; контролирует фактический путь без пустых уровней. |
| access-sibling-model-excluded | PASS | 0.000 | Модель соседней ветки запрещает, R разрешает: итоговое разрешение; защищает исключение посторонних моделей из цепочки. |
| access-represented-outside-object-path | PASS | 0.000 | Подтверждённый O находится в соседней ветке, C на пути объекта и R разрешает: итоговое разрешение; защищает независимость C и O. |
| access-unknown-path-denied-despite-allow | PASS | 0.000 | Полнота пути неизвестна при сохранённом разрешении: итоговый запрет до вычисления; предотвращает разрешение по частичному пути. |
| access-unknown-model-set-denied-despite-allow | PASS | 0.000 | Полный список моделей C неизвестен при разрешении корня: итоговый запрет до вычисления; не подменяет неизвестный список пустым. |
| admission-unverified-certificate | PASS | 0.000 | Без подтверждённого сертификата обращение отклоняется до чтения пути; защищает обязательный допуск. |
| admission-dn-bound-to-other-container | PASS | 0.000 | DN зарегистрирован только за outside, а заявлен root: обращение отклоняется; защищает привязку DN к конкретному O. |
| holder-subject-single-descendant-model | PASS | 0.000 | Одна модель потомка использует субъект root: root остаётся единственным держателем; защищает от передачи владения ссылкой. |
| holder-subject-multiple-descendant-models | PASS | 0.000 | Две модели разных потомков используют субъект root: исходная запись неизменна; защищает держателя при повторном использовании. |
| holder-object-single-ancestor-model | PASS | 0.000 | Модель предка C использует объект R: R остаётся единственным держателем; защищает от передачи владения ссылкой. |
| holder-object-multiple-ancestor-models | PASS | 0.000 | Две модели разных предков используют объект R: факты объекта неизменны; защищает держателя при повторном использовании. |
| persistent-containers-c01 | PASS | 1.148 | Все16 parent/child сочетаний enum проверяются настоящим create_child: допускается ровно полная матрица строгого порядка типов. |
| persistent-containers-c02 | PASS | 0.943 | Environment под system отклоняется без нового узла; проверяет запрет обратного порядка типов. |
| persistent-containers-c03 | PASS | 0.976 | System под system отклоняется без нового узла; проверяет отсутствие повторения типа по пути. |
| persistent-containers-c04 | PASS | 0.986 | Два module одного system получают разные ID/ветки; ни один ребёнок не является предком другого. |
| persistent-containers-c05 | PASS | 1.127 | Попытка назначить system второму environment отклоняется с сохранением единственного исходного parent/path. |
| persistent-containers-c06 | PASS | 1.152 | Независимые корни разных допустимых типов сохраняют собственные деревья и не становятся предками чужих узлов. |
| persistent-containers-c07 | PASS | 1.026 | Допустимый строковый собственный key сохраняет spelling и участвует в разрешении полного typed address. |
| persistent-containers-c08 | PASS | 1.122 | Число, None, bytes, list, dict и bool не принимаются вместо container key; новых узлов не возникает. |
| persistent-containers-c09 | PASS | 1.018 | Границы1/255 ASCII принимаются;0/256, кириллица и пробел отклоняются без частичной записи. |
| persistent-containers-c10 | PASS | 0.981 | Полный JSON organization/environment/module адрес разрешает leaf независимо от порядка JSON members. |
| persistent-containers-c11 | PASS | 1.001 | Typed address каждого root состоит только из его собственного type/key и разрешает тот же stable ID. |
| persistent-containers-c12 | PASS | 1.028 | Точный и case-only duplicate root/sibling typed address отклоняются; одному адресу не принадлежат два ID. |
| persistent-containers-c13 | PASS | 1.009 | Одинаковые keys у разных root типов и разных допустимых sibling типов дают разные ID и typed addresses. |
| persistent-containers-c14 | PASS | 0.952 | Пропуск существующего уровня не находит leaf, повтор type в исходном JSON отвергается до разрешения. |
| persistent-containers-c15 | PASS | 0.985 | VerifiedCertificateFact с DN DER зарегистрированного O принимается обоими типами общего допуска и реальным management service. |
| persistent-containers-c16 | PASS | 0.989 | DN другого Q не подтверждает заявленный O для management/access-check; факты остаются без изменения. |
| persistent-containers-c17 | PASS | 0.980 | Отсутствующий/непроверенный сертификатный факт не допускается для обоих RequestKind и не запускает mutation. |
| persistent-containers-c18 | PASS | 1.094 | Два DN у O и общий DN у Q дают точную M:N принадлежность только явно зарегистрированным контейнерам. |
| persistent-containers-c19 | PASS | 1.134 | После remove value, unset attribute и empty set свежий admission snapshot больше не подтверждает отозванный DN. |
| persistent-containers-c20 | PASS | 0.967 | Эквивалентные Printable/UTF8 Name с DN StringPrep подтверждают O, не добавляя второй set element и сохраняя original DER. |
| persistent-containers-c21 | PASS | 1.026 | Неизвестный OID допускает DirectoryString preparation и opaque exact DER; регистр opaque и иной ASN.1 tag не смешиваются. |
| persistent-containers-c22 | PASS | 0.964 | Rename предка сохраняет ID/parents потомков, вычисляет новые полные addresses и перестаёт разрешать старый путь. |
| persistent-containers-c23 | PASS | 0.987 | Занятый CI key и попытки менять ID/type/parent откатывают весь aggregate, включая предварительно записанные attrs. |
| persistent-containers-c24 | PASS | 1.056 | Две реальные service команды с одним CAS конкурируют за key/attr/DN: одна Changed, вторая RevisionConflict после свежего retry. |
| persistent-containers-c25 | PASS | 0.954 | Валидный первый attr и неизвестный второй откатывают attrs/key/revision контейнера одной transaction. |
| persistent-containers-c26 | PASS | 1.169 | Каждый отдельный child/active subject/object/model blocker запрещает container delete, сохраняя holder и собственные данные. |
| persistent-containers-c27 | PASS | 1.120 | Hard delete пустого holder purge tombstones/retained attrs/собственный DN/technical key guards атомарно, сохраняя общий каталог. |
| persistent-containers-c28 | PASS | 1.120 | Public restore/delete с двумя LOGIN и обеими очередностями даёт active survivor либо purge+NotFound, сохраняя исходные CAS tokens. |
| persistent-containers-c29 | PASS | 1.029 | Подтверждённый O через C управляет descendant D: rename, attrs и delete разрешаются при O<=C<=D. |
| persistent-containers-c30 | PASS | 1.172 | Каждая rename/attrs/delete отдельно отклоняется при нарушении O<=C либо C<=D, включая sibling и другое дерево, при валидном DN. |
| persistent-subjects-c01 | PASS | 1.000 | Зарегистрированный тип принимает subject create, неизвестный тип отклоняется без новой записи; проверяет обязательный общий каталог. |
| persistent-subjects-c02 | PASS | 1.012 | Ключи типов длиной1/512 принимаются; CI дубль, пустой,513, недопустимый символ и rename отклоняются без изменения каталога. |
| persistent-subjects-c03 | PASS | 0.959 | Предметный владелец контейнера без catalog role не регистрирует тип; проверяет отдельное глобальное полномочие. |
| persistent-subjects-c04 | PASS | 0.983 | Один subject key у разных типов и держателей создаёт независимые stable ID; проверяет scope holder/type/key. |
| persistent-subjects-c05 | PASS | 1.009 | Exact Unicode subject keys сохраняют регистр/NFC/NFD/пробелы; границы1/512 принимаются,0/513/control отклоняются. |
| persistent-subjects-c06 | PASS | 1.056 | Точный subject duplicate и изменение holder/type/key запрещены; tombstone резервирует identity и восстанавливает прежний ID. |
| persistent-subjects-c07 | PASS | 0.981 | Name/description читаются как два зарегистрированных атрибута с сохранением subject identity, без JSONB content. |
| persistent-subjects-c08 | PASS | 0.949 | Soft delete сохраняет ID/identity/attrs/deleted_at, но active get/find исключают tombstone; проверяет границу active/admin views. |
| persistent-subjects-c09 | PASS | 0.954 | Restore очищает deleted_at прежней записи и возвращает её ID/attrs без второй записи и без неявного fresh ID. |
| persistent-subjects-c10 | PASS | 0.925 | Прямой physical delete active subject и удаление его holder отклоняются; активные данные сохраняются. |
| persistent-subjects-c11 | PASS | 0.933 | После изменения subject attrs прежний CAS конфликтует для change/delete/restore и не перезаписывает current aggregate. |
| persistent-subjects-c12 | PASS | 1.001 | Ошибки после частичной записи attrs и после soft delete откатывают subject/status/attrs/revision целиком. |
| persistent-objects-c01 | PASS | 0.971 | Длинный Unicode TEXT key вне B-tree лимита, разный регистр и NFC/NFD сохраняются и находятся точно без application max. |
| persistent-objects-c02 | PASS | 0.956 | Пустой object key и C0/C1 control отклоняются без сохранения объекта; проверяет обязательную политику identity. |
| persistent-objects-c03 | PASS | 0.963 | Одинаковый key другого holder даёт независимый ID; изменение ID/holder/key существующего object запрещено. |
| persistent-objects-c04 | PASS | 1.002 | Два независимых SERIALIZABLE writer одновременно создают один key; после retry фиксируется один объект и unique conflict второго. |
| persistent-objects-c05 | PASS | 1.206 | Защищённая db-control collision seam помещает разные ключи в один bucket; оба сохраняются и разрешаются настоящим adapter по полному key. |
| persistent-objects-c06 | PASS | 1.004 | Object hard delete чистит собственные attrs одной операцией и сохраняет holder, subjects и model metadata. |
| persistent-objects-c07 | PASS | 1.074 | Изменение object attrs повышает aggregate revision; stale change/delete конфликтуют без перезаписи текущего состояния. |
| persistent-objects-c08 | PASS | 1.091 | Ошибка после частичных attrs либо после начала hard delete откатывает object/attrs/revision целиком. |
| persistent-attributes-c01 | PASS | 1.065 | Незарегистрированный definition отклоняется без автоматического создания definition/instance/value и без изменения aggregate. |
| persistent-attributes-c02 | PASS | 1.066 | CI конфликт DisplayName/displayname запрещает второе definition общего каталога, сохраняя первое. |
| persistent-attributes-c03 | PASS | 0.942 | Definition keys1/512 ASCII принимаются; пустой,513 и Unicode я отклоняются без регистрации. |
| persistent-attributes-c04 | PASS | 1.051 | Переименование зарегистрированного definition отклоняется DB guard, исходный key сохраняется. |
| persistent-attributes-c05 | PASS | 1.005 | Один definition явно применим к module/user/object/model; одно допустимое значение читается у всех четырёх владельцев. |
| persistent-attributes-c06 | PASS | 1.294 | Виды/типы вне applicability, включая новый subject type, не получают instance и не меняют прежние values. |
| persistent-attributes-c07 | PASS | 0.984 | Изменение атрибута одного из двух владельцев одного definition не затрагивает другого; проверяет owner-local storage. |
| persistent-attributes-c08 | PASS | 1.192 | Попытка назначить attribute несуществующему owner каждого вида отклоняется без orphan instances/values. |
| persistent-attributes-c09 | PASS | 0.949 | Существующий scalar нельзя оставить без value или с двумя values; оба отказа сохраняют прежний scalar. |
| persistent-attributes-c10 | PASS | 1.056 | Перестановка set и повтор равного элемента не меняют состав/revision и не создают значимого порядка либо дубля. |
| persistent-attributes-c11 | PASS | 1.018 | SnapshotReader различает AbsentAttribute и существующий SetAttribute без values у разных владельцев. |
| persistent-attributes-c12 | PASS | 1.034 | Явный null и у scalar, и как set element отклоняется без частичной записи; отсутствие остаётся отдельным состоянием. |
| persistent-attributes-c13 | PASS | 1.021 | Шесть native типов, включая обе BIGINT границы, читаются соответствующими Python/DB типами без общей TEXT сериализации. |
| persistent-attributes-c14 | PASS | 1.009 | Wrong type, BIGINT overflow и несколько заполненных native columns отклоняются, сохраняя прежнее значение. |
| persistent-attributes-c15 | PASS | 0.957 | Exact set хранит A/a/é/e+0301/начальный пробел как пять разных исходных строк без нормализации. |
| persistent-attributes-c16 | PASS | 0.992 | D145 поиск å возвращает исходное A+030A, но не строку с пробелом; duplicate исключается без потери spelling. |
| persistent-attributes-c17 | PASS | 1.013 | Пустой set удерживает definition type/cardinality/profile; все три изменения запрещены, исходная семантика и instance сохраняются. |
| persistent-attributes-c18 | PASS | 0.974 | Retained attribute tombstone удерживает type/cardinality/profile; все три изменения запрещены без потери original values. |
| persistent-attributes-c19 | PASS | 1.328 | Container actor без global catalog полномочия не регистрирует definition и не изменяет applicability. |
| persistent-attributes-c20 | PASS | 0.988 | Catalog operator не получает право изменять attrs произвольного контейнера; прежний aggregate сохраняется. |
| persistent-models-c01 | PASS | 1.097 | CI дубль модели в одном держателе отклоняется, а другой держатель получает собственный ID. |
| persistent-models-c02 | PASS | 0.992 | Только ASCII keys длиной 1/512 принимаются; ID/holder/key созданной модели не изменяются. |
| persistent-models-c03 | PASS | 0.956 | После изменения атрибута прежняя revision даёт конфликт без перезаписи metadata. |
| persistent-models-c04 | PASS | 0.936 | Ошибка второй части атрибутов откатывает metadata, значения и revision целиком. |
| persistent-models-c05 | PASS | 0.994 | Physical delete удаляет metadata/её attrs и сохраняет holder, субъекты и объекты. |
| persistent-models-c06 | PASS | 0.934 | Известные metadata остаются отдельным полным набором и не становятся исполнимой моделью/Undefined. |
| persistent-facts-c01 | PASS | 1.191 | Commit другой connection между чтениями не меняет старый snapshot; новый read видит изменение всех фактов. |
| persistent-facts-c02 | PASS | 1.096 | Путь root→holder содержит предков C и оба конца; субъект и O другого дерева сохраняются. |
| persistent-facts-c03 | PASS | 1.105 | Контейнер без моделей остаётся в полном пути с явным пустым metadata group. |
| persistent-facts-c04 | PASS | 1.091 | Ошибка path или metadata явно обозначена unknown и не превращается в полный пустой набор. |
| persistent-facts-c05 | PASS | 1.112 | Reader LOGIN не может писать, вызывать mutations или менять схему; факты после отказов сохраняются. |

Подробные результаты и версии: [results.json](results.json).
