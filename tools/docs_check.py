"""Детерминированная проверка документации и evidence её review перед archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

REQUIRED_PAGES = tuple(f"docs/{name}.md" for name in (
    "README", "architecture", "domains", "services", "api", "database", "operations", "development"
))
MERMAID_PAGES = {"docs/architecture.md", "docs/services.md", "docs/database.md"}
GENERATED_FILES = {
    "docs-review.json", "docs-snapshot.json", "run-results.json", "run-manifest.json", "run-summary.md",
    "regression-registry.yaml", "regression-evidence.json", "archive-gate-check.json", "archive-completion.json",
}
SOURCE_REPOS = {
    "container-adm-api", "entity-subject-adm-api", "entity-object-adm-api", "policy-adm-api",
    "policy-decision-api", "access-assignment-api", "db-control", "TamarixTests", "TamarixCD",
}
MERMAID_TYPES = {
    "flowchart", "graph", "sequenceDiagram", "erDiagram", "classDiagram", "stateDiagram-v2",
    "stateDiagram", "journey", "gantt", "pie", "timeline", "mindmap", "gitGraph",
    "quadrantChart", "requirementDiagram", "C4Context", "C4Container", "block-beta", "architecture-beta",
}


class DocsError(ValueError):
    """Документация или её подтверждение не готовы к archive."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DocsError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(store: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(store), *args], capture_output=True, text=True)
    require(result.returncode == 0, f"Git документации: не удалось выполнить {args[0]}")
    return result.stdout.strip()


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        raise DocsError(f"Evidence документации недоступен: {path.name}") from exc
    require(isinstance(value, dict), "Evidence документации должен быть JSON object")
    return value


def docs_hashes(store: Path) -> dict[str, str]:
    hashes = {}
    for path in sorted((store / "docs").rglob("*.md")):
        require(not path.is_symlink(), "Страница docs не должна быть symlink")
        hashes[path.relative_to(store).as_posix()] = digest(path.read_bytes())
    return hashes


def change_hashes(root: Path) -> dict[str, str]:
    """Хэши исходных артефактов с путями, устойчивыми к перемещению в archive."""
    require(root.is_dir(), "Change для документации отсутствует")
    hashes = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        relative = path.relative_to(root).as_posix()
        if relative in GENERATED_FILES:
            continue
        require(not path.is_symlink(), "Артефакт change не должен быть symlink")
        hashes[relative] = digest(path.read_bytes())
    require(bool(hashes), "Change не содержит исходных артефактов")
    return hashes


def markdown_body(text: str, label: str) -> tuple[str, list[str]]:
    """Отделить fenced code от текста и проверить структуру Mermaid без рендера."""
    prose, mermaid, content = [], [], []
    fence = language = None
    for line in text.splitlines():
        if fence:
            if re.fullmatch(r"\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                if language == "mermaid":
                    meaningful = [x.strip() for x in content if x.strip() and not x.lstrip().startswith("%%")]
                    require(len(meaningful) >= 2, f"Пустая Mermaid схема: {label}")
                    require(meaningful[0].split()[0] in MERMAID_TYPES, f"Неизвестный тип Mermaid схемы: {label}")
                    mermaid.append("\n".join(content))
                fence = language = None
                content = []
            else:
                content.append(line)
            continue
        opening = re.match(r"\s*(`{3,}|~{3,})\s*([^\s]*)[^\n]*$", line)
        if opening:
            fence, language = opening.groups()
        else:
            prose.append(line)
    require(fence is None, f"Незакрытый fenced block: {label}")
    return "\n".join(prose), mermaid


def source_roots(store: Path) -> set[Path]:
    """Явный список соседних source checkouts, которые не поставляются с store CI."""
    return {(store.parent / repo).resolve() for repo in SOURCE_REPOS} | {
        (store.parent.parent / repo).resolve() for repo in {"TamarixTests", "TamarixCD"}
    }


def check_links(store: Path, page: Path, prose: str, snapshot: dict[str, str] | None = None) -> list[str]:
    unavailable = []
    targets = re.findall(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", prose)
    definitions = re.findall(r"^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)", prose, re.M)
    for raw in targets + definitions:
        target = raw.strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        path_text = unquote(parsed.path)
        require(not path_text.startswith("/"), f"Непереносимая абсолютная ссылка: {page.name}: {target}")
        linked = (page.parent / path_text).resolve() if path_text else page.resolve()
        if snapshot is not None and linked.is_relative_to((store / "docs").resolve()):
            relative = linked.relative_to(store.resolve()).as_posix()
            if linked.suffix.lower() == ".md":
                require(relative in snapshot, f"Битая ссылка внутри docs snapshot: {page.name}: {target}")
                linked_text = snapshot[relative]
            else:
                # Snapshot фиксирует Markdown, а не произвольные двоичные assets.
                continue
        elif snapshot is not None:
            # Исторические исходные specs/код могли измениться после этого archive.
            if not linked.is_relative_to(store.resolve()):
                require(any(linked.is_relative_to(root) for root in source_roots(store)),
                        f"Ссылка вне известных исходных репозиториев: {page.name}: {target}")
            continue
        else:
            linked_text = None
        if not linked.is_relative_to(store.resolve()):
            allowed = next((root for root in source_roots(store) if linked.is_relative_to(root)), None)
            require(allowed is not None, f"Ссылка вне известных исходных репозиториев: {page.name}: {target}")
            if not allowed.is_dir():
                unavailable.append(target)
                continue
        require(linked_text is not None or linked.exists(), f"Битая локальная ссылка: {page.name}: {target}")
        if parsed.fragment and linked.suffix.lower() == ".md":
            target_prose, _ = markdown_body(linked_text if linked_text is not None else linked.read_text(), linked.name)
            anchors, duplicates = set(), {}
            for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", target_prose, re.M):
                anchor = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                count = duplicates.get(anchor, 0)
                duplicates[anchor] = count + 1
                anchors.add(anchor + (f"-{count}" if count else ""))
            anchors.update(re.findall(r'<(?:a|h[1-6])\b[^>]*(?:id|name)=["\']([^"\']+)', target_prose))
            require(unquote(parsed.fragment) in anchors, f"Битый Markdown anchor: {page.name}: {target}")
    return unavailable


def validate_document_set(store: Path, documents: dict[str, str], historical: bool = False) -> dict:
    for relative in REQUIRED_PAGES:
        require(relative in documents, f"Обязательная страница документации отсутствует: {relative}")
    diagrams, unavailable = 0, []
    for relative, text in documents.items():
        path = store / relative
        prose, blocks = markdown_body(text, relative)
        require(bool(re.search(r"[А-Яа-яЁё]", prose)), f"Русское описание отсутствует: {relative}")
        require(bool(re.search(r"^#\s+\S", prose, re.M)), f"Заголовок страницы отсутствует: {relative}")
        if relative in MERMAID_PAGES:
            require(bool(blocks), f"Mermaid схема отсутствует: {relative}")
        diagrams += len(blocks)
        unavailable += check_links(store, path, prose, documents if historical else None)
    return {"schema_version": 1, "status": "PASS", "pages_checked": len(documents), "mermaid_blocks": diagrams,
            "unavailable_source_links": sorted(set(unavailable))}


def validate_docs(store: Path) -> dict:
    documents = {path: (store / path).read_bytes().decode("utf-8") for path in docs_hashes(store)}
    return validate_document_set(store, documents)


def validate_snapshot(store: Path, root: Path, review: dict) -> None:
    path = root / "docs-snapshot.json"
    require(path.is_file(), "Content snapshot документации отсутствует")
    require(review.get("snapshot_sha256") == digest(path.read_bytes()), "Hash content snapshot документации не совпадает")
    value = read_json(path)
    files = value.get("files")
    require(value.get("schema_version") == 1 and isinstance(files, dict), "Некорректная версия/структура docs snapshot")
    require(set(files) == set(review["docs_sha256"]), "Состав content snapshot не совпадает с docs hashes")
    documents = {}
    for relative, entry in files.items():
        require(isinstance(entry, dict) and isinstance(entry.get("content"), str), "Текст страницы отсутствует в docs snapshot")
        content_sha = digest(entry["content"].encode("utf-8"))
        require(entry.get("sha256") == review["docs_sha256"][relative] == content_sha, f"Content hash страницы docs не совпадает: {relative}")
        documents[relative] = entry["content"]
    validate_document_set(store, documents, historical=True)


def base_docs_hashes(store: Path, base_commit: str) -> dict[str, str]:
    require(bool(re.fullmatch(r"[0-9a-f]{40}", base_commit or "")), "Полный base_commit документации отсутствует")
    git(store, "merge-base", "--is-ancestor", base_commit, "HEAD")
    paths = git(store, "ls-tree", "-r", "--name-only", base_commit, "--", "docs").splitlines()
    hashes = {}
    for path in paths:
        if path.endswith(".md"):
            result = subprocess.run(["git", "-C", str(store), "show", f"{base_commit}:{path}"], capture_output=True)
            require(result.returncode == 0, "Историческая страница документации недоступна")
            hashes[path] = digest(result.stdout)
    return hashes


def changed_pages(before: dict, after: dict) -> list[str]:
    return sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))


def prepare_review(store: Path, change: str, base_ref: str = "HEAD", refresh: bool = False) -> dict:
    require(bool(re.fullmatch(r"[a-z0-9][a-z0-9-]*", change)), "Некорректное имя change")
    root = store / "openspec/changes" / change
    path = root / "docs-review.json"
    require(refresh or not path.exists(), "docs-review.json уже существует; --refresh сохраняет baseline и требует нового review")
    base = read_json(path).get("base_commit") if path.exists() else git(store, "rev-parse", "--verify", f"{base_ref}^{{commit}}")
    validate_docs(store)
    hashes = docs_hashes(store)
    snapshot = {"schema_version": 1, "files": {
        relative: {"sha256": sha, "content": (store / relative).read_bytes().decode("utf-8")}
        for relative, sha in hashes.items()
    }}
    snapshot_path = root / "docs-snapshot.json"
    snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    value = {"schema_version": 1, "change": change, "base_commit": base,
             "change_sha256": change_hashes(root), "docs_sha256": hashes,
             "snapshot_sha256": digest(snapshot_path.read_bytes()),
             "changed_pages": changed_pages(base_docs_hashes(store, base), hashes),
             "sections": {page: {"status": "pending", "reason": ""} for page in REQUIRED_PAGES}}
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    return value


def validate_review(store: Path, change: str, root: Path | None = None, current_docs: bool = True) -> dict:
    root = root or store / "openspec/changes" / change
    value = read_json(root / "docs-review.json")
    require(value.get("schema_version") == 1 and value.get("change") == change, "Версия/change docs evidence не совпадают")
    require(value.get("change_sha256") == change_hashes(root), "Change изменён после review документации; обновите docs и evidence")
    hashes = value.get("docs_sha256")
    require(isinstance(hashes, dict) and set(REQUIRED_PAGES) <= hashes.keys(), "Полный snapshot docs hashes отсутствует")
    for path, sha in hashes.items():
        require(isinstance(path, str) and path.startswith("docs/") and path.endswith(".md") and ".." not in Path(path).parts,
                "Некорректный docs path в evidence")
        require(isinstance(sha, str) and bool(re.fullmatch(r"[0-9a-f]{64}", sha)), "Некорректный SHA-256 страницы docs")
    validate_snapshot(store, root, value)
    before = base_docs_hashes(store, value.get("base_commit"))
    actual_changed = changed_pages(before, hashes)
    require(bool(actual_changed), "Документация не обновлена относительно baseline")
    require(value.get("changed_pages") == actual_changed, "Список обновлённых страниц docs не совпадает с baseline")
    sections = value.get("sections")
    require(isinstance(sections, dict) and set(sections) == set(REQUIRED_PAGES), "Review должен охватывать все разделы docs")
    for page, section in sections.items():
        require(isinstance(section, dict) and section.get("status") in {"updated", "reviewed"}, f"Review раздела не завершён: {page}")
        require((section["status"] == "updated") == (page in actual_changed), f"Статус review не соответствует изменению страницы: {page}")
        reason = section.get("reason")
        require(isinstance(reason, str) and bool(re.search(r"[А-Яа-яЁё]", reason)) and len(reason.strip()) >= 12,
                f"Нужно содержательное русское обоснование review: {page}")
    if current_docs:
        validate_docs(store)
        require(hashes == docs_hashes(store), "Документация изменена после review; обновите evidence")
    return value


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "prepare", "review"])
    parser.add_argument("--store", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--change")
    parser.add_argument("--base-ref", default="HEAD")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args(argv)
    try:
        store = args.store.resolve()
        if args.action == "check":
            result = validate_docs(store)
        else:
            require(bool(args.change), "Нужен --change")
            result = prepare_review(store, args.change, args.base_ref, args.refresh) if args.action == "prepare" else validate_review(store, args.change)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (DocsError, OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
