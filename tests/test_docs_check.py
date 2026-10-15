"""Проверки документации выполняются в изолированном store без запуска приложения."""

import importlib.util
import json
from pathlib import Path
import subprocess

import pytest

MODULE = Path(__file__).resolve().parents[1] / "tools/docs_check.py"
SPEC = importlib.util.spec_from_file_location("tamarix_docs_check_tests", MODULE)
docs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(docs)


def git(store, *args):
    result = subprocess.run(["git", "-C", str(store), *args], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def commit(store):
    git(store, "add", "-A")
    git(store, "-c", "user.name=Docs Tests", "-c", "user.email=docs@example.invalid", "commit", "-m", "Тестовый checkpoint")
    return git(store, "rev-parse", "HEAD")


def completed_review(store, base):
    path = store / "openspec/changes/demo/docs-review.json"
    value = docs.prepare_review(store, "demo", base, refresh=path.exists())
    for page, section in value["sections"].items():
        section.update(status="updated" if page in value["changed_pages"] else "reviewed",
                       reason="Раздел сверен с текущим change; объяснение и примеры соответствуют реализации.")
    path.write_text(json.dumps(value, ensure_ascii=False))
    return value


@pytest.fixture
def store(tmp_path):
    root = tmp_path / "tamarix-specs"
    root.mkdir()
    git(root, "init", "--initial-branch=main")
    (root / "baseline.md").write_text("Исходный checkpoint.\n")
    base = commit(root)
    active = root / "openspec/changes/demo"
    active.mkdir(parents=True)
    (active / "proposal.md").write_text("# Предложение\n\nОписание change.\n")
    (active / "tasks.md").write_text("- [x] Обновить документацию.\n")
    for relative in docs.REQUIRED_PAGES:
        path = root / relative
        path.parent.mkdir(exist_ok=True)
        path.write_text("# Документация\n\nОписание продукта и [навигация](README.md).\n\n```mermaid\nflowchart LR\n  A --> B\n```\n")
    completed_review(root, base)
    return root


def test_complete_review_passes_in_clean_checkout(store):
    """Фиксирует обновлённые docs и review, затем ожидает PASS на чистом checkout; подтверждает сохранение baseline после commit."""
    commit(store)
    value = docs.validate_review(store, "demo")
    assert value["changed_pages"] == sorted(docs.REQUIRED_PAGES)
    assert docs.validate_docs(store)["mermaid_blocks"] == 8


@pytest.mark.parametrize("mutation,description", [
    pytest.param("missing", "Удалённая обязательная страница блокирует неполную документацию.", id="missing-page"),
    pytest.param("link", "Несуществующая локальная ссылка блокирует сломанную навигацию.", id="broken-local-link"),
    pytest.param("absolute", "Абсолютный путь локальной машины блокируется как непереносимый.", id="absolute-link"),
    pytest.param("escape", "Выход ссылки в неизвестный соседний каталог запрещён.", id="unknown-source-root"),
    pytest.param("no-diagram", "Отсутствие обязательной Mermaid схемы блокирует architecture.", id="missing-mermaid"),
    pytest.param("unclosed", "Незакрытый fenced block блокирует повреждённый Markdown.", id="unclosed-fence"),
    pytest.param("empty-diagram", "Схема только с заголовком не подтверждает содержательную структуру.", id="empty-mermaid"),
    pytest.param("unknown-diagram", "Неизвестный тип схемы показывает опечатку в Mermaid.", id="unknown-mermaid-type"),
])
def test_invalid_documentation_is_rejected(store, mutation, description):
    """Повреждает обязательную страницу согласно русскому описанию параметра и ожидает DocsError; защищает полноту и переносимость docs."""
    assert description
    path = store / "docs/architecture.md"
    if mutation == "missing":
        path.unlink()
    elif mutation == "link":
        path.write_text(path.read_text() + "\n[Ошибка](missing.md)\n")
    elif mutation == "absolute":
        path.write_text(path.read_text() + "\n[Ошибка](/private/tmp/example.md)\n")
    elif mutation == "escape":
        path.write_text(path.read_text() + "\n[Ошибка](../../unknown/source.py)\n")
    elif mutation == "no-diagram":
        path.write_text("# Архитектура\n\nТолько текст.\n")
    elif mutation == "unclosed":
        path.write_text(path.read_text() + "\n```python\nprint(1)\n")
    elif mutation == "empty-diagram":
        path.write_text("# Архитектура\n\nОписание.\n```mermaid\nflowchart LR\n```\n")
    else:
        path.write_text(path.read_text().replace("flowchart LR", "flowchat LR"))
    with pytest.raises(docs.DocsError):
        docs.validate_docs(store)


def test_source_links_work_without_sibling_ci_checkouts(store):
    """Ссылка на объявленный service checkout отсутствует в store-only CI и допускается с явным списком пропущенных source ссылок."""
    page = store / "docs/services.md"
    page.write_text(page.read_text() + "\n[Код](../../container-adm-api/src/core.py)\n")
    result = docs.validate_docs(store)
    assert result["unavailable_source_links"] == ["../../container-adm-api/src/core.py"]


def test_present_source_checkout_requires_existing_link_target(store):
    """При доступном соседнем checkout ссылка на отсутствующий файл должна давать отказ; проверка находит устаревшие ссылки исходников локально."""
    (store.parent / "container-adm-api").mkdir()
    page = store / "docs/services.md"
    page.write_text(page.read_text() + "\n[Код](../../container-adm-api/src/missing.py)\n")
    with pytest.raises(docs.DocsError, match="Битая локальная ссылка"):
        docs.validate_docs(store)


@pytest.mark.parametrize("mutation,description", [
    pytest.param("change", "Изменившийся proposal делает прежний review устаревшим.", id="stale-proposal"),
    pytest.param("delta", "Новая delta после review требует повторно проверить все разделы.", id="stale-delta"),
    pytest.param("docs", "Изменённая страница после review не соответствует SHA-256.", id="stale-page"),
    pytest.param("missing-section", "Пропуск раздела database не подтверждает полный review.", id="missing-section"),
    pytest.param("pending", "Незавершённый pending раздел не допускает archive.", id="pending-review"),
    pytest.param("english", "Обоснование на английском не отвечает русскому review процессу.", id="english-reason"),
    pytest.param("changed-pages", "Пустой список изменённых страниц не совпадает с baseline.", id="false-changed-pages"),
])
def test_stale_or_incomplete_review_is_rejected(store, mutation, description):
    """Меняет один вход уже завершённого review и ожидает отказ; различающиеся причины перечислены у параметров и защищают свежесть evidence."""
    assert description
    path = store / "openspec/changes/demo/docs-review.json"
    value = json.loads(path.read_text())
    if mutation == "change":
        (path.parent / "proposal.md").write_text("Изменённое предложение.\n")
    elif mutation == "delta":
        delta = path.parent / "specs/example/spec.md"
        delta.parent.mkdir(parents=True)
        delta.write_text("## ADDED Requirements\n\nНовый критерий.\n")
    elif mutation == "docs":
        page = store / "docs/api.md"
        page.write_text(page.read_text() + "\nНовый API контракт.\n")
    elif mutation == "missing-section":
        del value["sections"]["docs/database.md"]
    elif mutation == "pending":
        value["sections"]["docs/database.md"]["status"] = "pending"
    elif mutation == "english":
        value["sections"]["docs/database.md"]["reason"] = "All schema details remain correct."
    else:
        value["changed_pages"] = []
    path.write_text(json.dumps(value, ensure_ascii=False))
    with pytest.raises(docs.DocsError):
        docs.validate_review(store, "demo")


def test_prepare_preserves_baseline_and_requires_new_review_on_refresh(store):
    """Повторный prepare без флага отказывает, refresh после commit сохраняет исходный SHA и сбрасывает решения; предотвращает тихое переподтверждение docs."""
    path = store / "openspec/changes/demo/docs-review.json"
    before = json.loads(path.read_text())
    commit(store)
    with pytest.raises(docs.DocsError, match="уже существует"):
        docs.prepare_review(store, "demo")
    refreshed = docs.prepare_review(store, "demo", refresh=True)
    assert refreshed["base_commit"] == before["base_commit"]
    assert all(section["status"] == "pending" for section in refreshed["sections"].values())
    with pytest.raises(docs.DocsError, match="не завершён"):
        docs.validate_review(store, "demo")


def test_tooling_change_without_actual_docs_update_is_rejected(store):
    """Новый docs-only/tooling change на неизменных docs обязан обновить хотя бы страницу; полный reviewed checklist не заменяет фактический diff."""
    commit(store)
    root = store / "openspec/changes/next"
    root.mkdir()
    (root / "proposal.md").write_text("Новое tooling изменение.\n")
    value = docs.prepare_review(store, "next")
    for section in value["sections"].values():
        section.update(status="reviewed", reason="Все существующие разделы просмотрены без изменения содержания.")
    (root / "docs-review.json").write_text(json.dumps(value, ensure_ascii=False))
    with pytest.raises(docs.DocsError, match="не обновлена"):
        docs.validate_review(store, "next")


def test_archived_review_keeps_historical_docs_hashes(store):
    """После перемещения change и последующего редактирования docs historical review проходит без current snapshot, новый archive с тем же evidence отказывает."""
    root = store / "openspec/changes/demo"
    destination = store / "openspec/changes/archive/2026-10-15-demo"
    destination.parent.mkdir()
    root.rename(destination)
    page = store / "docs/api.md"
    page.write_text(page.read_text() + "\nОписание следующего изменения.\n")
    assert docs.validate_review(store, "demo", destination, current_docs=False)
    with pytest.raises(docs.DocsError, match="изменена после review"):
        docs.validate_review(store, "demo", destination)


def test_broken_local_heading_anchor_is_rejected(store):
    """Ссылка на существующий Markdown с отсутствующим заголовком должна блокироваться; проверка защищает навигацию между разделами документации."""
    page = store / "docs/README.md"
    page.write_text(page.read_text() + "\n[Раздел](api.md#несуществующий-раздел)\n")
    with pytest.raises(docs.DocsError, match="anchor"):
        docs.validate_docs(store)


def test_tooling_review_can_update_one_page_and_review_remaining_sections(store):
    """Для tooling change обновляет development и оставляет семь разделов reviewed с русским обоснованием; ожидается PASS без предметных delta specs."""
    baseline = commit(store)
    root = store / "openspec/changes/tooling"
    root.mkdir()
    (root / "proposal.md").write_text("Изменить процесс разработки.\n")
    page = store / "docs/development.md"
    page.write_text(page.read_text() + "\nНовый шаг разработки и архивирования.\n")
    value = docs.prepare_review(store, "tooling", baseline)
    for path, section in value["sections"].items():
        section.update(status="updated" if path in value["changed_pages"] else "reviewed",
                       reason="Процесс разработки актуализирован; остальные сведения сверены с текущими источниками.")
    (root / "docs-review.json").write_text(json.dumps(value, ensure_ascii=False))
    assert docs.validate_review(store, "tooling")["changed_pages"] == ["docs/development.md"]


@pytest.mark.parametrize("invalid,description", [
    pytest.param("missing", "Отсутствующий content snapshot не подтверждает исторические hashes.", id="missing-content-snapshot"),
    pytest.param("hash", "Изменённый текст без обновления SHA страницы должен блокироваться.", id="content-hash-mismatch"),
    pytest.param("russian", "Самосогласованный snapshot без русского prose не подтверждает документацию.", id="snapshot-without-russian-prose"),
    pytest.param("mermaid", "Самосогласованный snapshot с пустой Mermaid схемой должен блокироваться.", id="empty-mermaid-in-snapshot"),
    pytest.param("link", "Ссылка в сохранённом docs snapshot на отсутствующую страницу должна блокироваться.", id="broken-snapshot-link"),
])
def test_historical_snapshot_requires_valid_content_not_only_declared_hashes(store, invalid, description):
    """Проверяет сохранённый текст без сравнения с current docs: случай указан у параметра, ожидается отказ для отсутствующего, повреждённого или структурно неверного snapshot."""
    assert description
    root = store / "openspec/changes/demo"
    path = root / "docs-snapshot.json"
    if invalid == "missing":
        path.unlink()
    else:
        snapshot = json.loads(path.read_text())
        review_path = root / "docs-review.json"
        review = json.loads(review_path.read_text())
        relative = "docs/architecture.md"
        entry = snapshot["files"][relative]
        if invalid == "hash":
            entry["content"] += "\nНеподтверждённая правка текста.\n"
        elif invalid == "russian":
            entry["content"] = "# Architecture\n\nOnly English prose.\n\n```mermaid\nflowchart LR\n A --> B\n```\n"
        elif invalid == "mermaid":
            entry["content"] = "# Архитектура\n\nОписание.\n\n```mermaid\nflowchart LR\n```\n"
        else:
            entry["content"] += "\n[Несуществующая страница](absent.md)\n"
        if invalid != "hash":
            entry["sha256"] = docs.digest(entry["content"].encode())
            review["docs_sha256"][relative] = entry["sha256"]
        path.write_text(json.dumps(snapshot, ensure_ascii=False))
        review["snapshot_sha256"] = docs.digest(path.read_bytes())
        review_path.write_text(json.dumps(review, ensure_ascii=False))
    with pytest.raises(docs.DocsError):
        docs.validate_review(store, "demo", current_docs=False)
