# Минимальная среда логического ядра T-1

Дата: 2026-10-09. Статус: **accepted**. Пользователь явно ответил
«Да, принять среду» на перечисленный набор задачи 2.2.
Область: container-adm-api, entity-subject-adm-api, entity-object-adm-api,
policy-adm-api, policy-decision-api. Этот документ не устанавливает зависимости.

## Предложение и источники

| Компонент | Pin | Официальное подтверждение |
| --- | --- | --- |
| Python | 3.15.0 | [Стабильный релиз от 2026-10-09](https://www.python.org/downloads/release/python-3150/) |
| uv | 0.12.24 | [Релиз Astral от 2026-10-08](https://github.com/astral-sh/uv/releases/tag/0.12.24) |
| pytest, только dev | 9.1.1 | [Метаданные PyPI](https://pypi.org/project/pytest/9.1.1/): Python >=3.10, заявлена Python 3.15 |
| uv_build, build | 0.12.24 | [Метаданные PyPI](https://pypi.org/project/uv-build/0.12.24/): Python >=3.8 |

Приняты и реализованы стандартные устанавливаемые pure-Python пакеты с `src/` и
[uv build backend](https://docs.astral.sh/uv/concepts/build-backend/).
Он встроен в соответствующую версию uv; дополнительных build scripts для
текущего ядра не требуется. Альтернатива — Hatchling, если появятся более сложные
потребности сборки; такой потребности пока нет.

[Параметризация pytest](https://pytest.org/en/latest/how-to/parametrize.html)
позволяет связать сценарии/таблицы specs с именованными случаями. Альтернатива —
стандартный unittest без дополнительной зависимости.

## Фиксация в каждом проекте

```toml
[project]
requires-python = ">=3.15,<3.16"
dependencies = []

[build-system]
requires = ["uv_build==0.12.24"]
build-backend = "uv_build"

[dependency-groups]
dev = ["pytest==9.1.1"]

[tool.uv]
required-version = "==0.12.24"
prerelease = "disallow"
```

`.python-version`: `3.15.0`. Имена проектов и пакетов соответствуют сервисам;
фиксируются прямые и транзитивные dev-зависимости в `uv.lock`.
[required-version](https://docs.astral.sh/uv/reference/settings/#required-version)
проверяет согласованную версию uv.
FastAPI, Pydantic и библиотеки БД не добавляются в текущие pure-Python проекты
без потребности API/хранения; утверждённый общий стек сохраняется для будущих адаптеров.

## План проверок после принятия

Сначала обеспечить доступность именно final Python 3.15.0 и uv 0.12.24.
В каждом проекте:

```sh
uv lock
uv lock --check
uv sync --frozen
uv run --frozen --no-sync python --version
uv run --frozen --no-sync python -m pytest -q
uv build --no-sources
```

[Официальный workflow lock/sync](https://docs.astral.sh/uv/concepts/projects/sync/).
При нуле тестов pytest не служит свидетельством завершения; реальные тесты
добавляются в соответствующих группах задач.

Исходная read-only проверка при подготовке 2.2: Homebrew uv 0.12.23,
system Python 3.9.6, uv-managed Python 3.13.16. Offline-каталог uv тогда содержал только
3.15.0rc3 для ветки 3.15. Поэтому наличие final в managed-каталоге нужно проверить
после подготовки uv; rc не допускается и более старая версия не выбирается молча.
При недоступности final зависимые задачи остаются открытыми.

На 2026-10-10 final Python 3.15.0 установлен из официального macOS installer.
Принятый uv доступен через `uv tool run --from uv==0.12.24 uv`;
этот launcher применяется к командам uv выше без обновления Homebrew uv.
Lock/sync/build и автоматизированные тесты выполнены во всех пяти проектах.
Точные команды, результаты и снимки исходников — в [tasks.md](tasks.md)
и [test-evidence.json](test-evidence.json). Проверки относятся к логическому ядру.

