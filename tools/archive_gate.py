"""Проверка evidence и безопасное архивирование без неявного запуска тестов."""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

import yaml


class GateError(ValueError):
    """Отчёт не подтверждает допуск архивирования."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_digest(value: Any) -> str:
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    require(result.returncode == 0, f"Git: {root.name}: не удалось выполнить {args[0]}")
    return result.stdout.strip()


def safe_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "Путь выходит за пределы репозитория")
    return path


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        raise GateError(f"Отчёт/JSON недоступен: {path.name}") from exc
    require(isinstance(value, dict), "Ожидается JSON object")
    return value


def require_sha(sha: Any, label: str) -> None:
    require(isinstance(sha, str) and bool(re.fullmatch(r"[0-9a-f]{40}", sha)), f"Неизменяемый commit отсутствует: {label}")


def hash_specs(store: Path, change: str | None = None) -> dict[str, str]:
    base = store / "openspec" / ("specs" if change is None else f"changes/{change}/specs")
    return {p.relative_to(store).as_posix(): digest(p.read_bytes()) for p in sorted(base.rglob("spec.md"))}


def registry_from_bytes(data: bytes) -> list[dict]:
    try:
        value = yaml.safe_load(data)
    except yaml.YAMLError as exc:
        raise GateError("Некорректный registry") from exc
    require(isinstance(value, dict) and value.get("schema_version") == 1, "Неверная версия registry")
    cases = value.get("cases")
    require(isinstance(cases, list), "Registry не содержит cases")
    ids = [c.get("id") for c in cases if isinstance(c, dict)]
    require(len(ids) == len(cases) and all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids), "Некорректные/повторяющиеся test ID")
    for case in cases:
        require(case.get("state") in {"candidate", "regression", "retired"}, "Некорректное состояние теста")
        description = case.get("description", "")
        require(isinstance(description, str) and bool(re.search(r"[А-Яа-яЁё]", description)), f"Русское описание отсутствует: {case['id']}")
        require(isinstance(case.get("test"), str) and "::" in case["test"], f"Node ID отсутствует: {case['id']}")
        require(isinstance(case.get("links"), list) and bool(case["links"]), f"Traceability отсутствует: {case['id']}")
        if case["state"] == "retired":
            require(bool(case.get("retired_by")) and bool(case.get("retirement_reason")), f"Retirement не обоснован: {case['id']}")
    return cases


def expected_cases(cases: list[dict], change: str) -> list[dict]:
    return [c for c in cases if c["state"] == "regression" or (c["state"] == "candidate" and c.get("introduced_by") == change)]


def requirement_blocks(text: str) -> dict[str, str]:
    return {m.group(1).strip(): m.group(0) for m in re.finditer(r"^### Requirement: (.*?)\s*\n.*?(?=^### Requirement: |^## |\Z)", text, re.M | re.S)}


def merge_requirement_text(text: str, delta_text: str) -> str:
    """Применить delta к requirement blocks для проверки, не изменяя файлы."""
    requirements = requirement_blocks(text)
    for section in re.finditer(r"^## (ADDED|MODIFIED|REMOVED|RENAMED) Requirements\s*\n(.*?)(?=^## |\Z)", delta_text, re.M | re.S):
        action, body = section.groups()
        if action == "RENAMED":
            pairs = re.findall(r"-\s*FROM:\s*`?### Requirement:\s*([^\n`]+)`?\s*\n-\s*TO:\s*`?### Requirement:\s*([^\n`]+)`?", body)
            for old, new in pairs:
                if old.strip() in requirements:
                    block = requirements.pop(old.strip())
                    requirements[new.strip()] = block.replace("### Requirement: " + old.strip(), "### Requirement: " + new.strip(), 1)
        else:
            for match in re.finditer(r"^### Requirement: (.*?)\s*\n.*?(?=^### Requirement: |\Z)", body, re.M | re.S):
                title = match.group(1).strip()
                if action == "REMOVED":
                    requirements.pop(title, None)
                else:
                    requirements[title] = match.group(0)
    return "\n\n".join(requirements.values())


def effective_spec(store: Path, relative: str, change: str | None = None) -> str:
    """Собрать prospective требования основной capability и одного active delta."""
    main = safe_path(store, relative)
    text = main.read_text() if main.is_file() else ""
    if not change:
        return text
    delta = safe_path(store, f"openspec/changes/{change}/specs/" + relative.removeprefix("openspec/specs/"))
    return merge_requirement_text(text, delta.read_text()) if delta.is_file() else text


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\*\*|`", "", text)).strip()


def criterion_text(text: str) -> str:
    return normalized(re.sub(r"^\s*-?\s*(?:\*\*)?(?:THEN|AND)(?:\*\*)?\s+", "", text))


def delta_criteria(delta: str, spec: str) -> set[tuple[str, str, str, str]]:
    required = set()
    for section in re.finditer(r"^## (ADDED|MODIFIED) Requirements\s*\n(.*?)(?=^## |\Z)", delta, re.M | re.S):
        for title, body in requirement_blocks(section.group(2)).items():
            for scenario in re.finditer(r"^#### Scenario: (.*?)\s*\n(.*?)(?=^#### Scenario: |\Z)", body, re.M | re.S):
                after_then = False
                for line in scenario.group(2).splitlines():
                    clause = re.match(r"\s*-\s*\*\*(THEN|AND)\*\*\s+(.*)", line)
                    if clause and (clause.group(1) == "THEN" or after_then):
                        after_then = True
                        required.add((spec, title, scenario.group(1).strip(), criterion_text(clause.group(2))))
    return required


def assert_delta_coverage(cases: list[dict], deltas: dict[str, str], change: str) -> None:
    covered = {(link["spec"], link["requirement"], link["scenario"], criterion_text(link["criterion"]))
               for case in expected_cases(cases, change) for link in case["links"]}
    for relative, text in deltas.items():
        spec = "openspec/specs/" + relative.split("/specs/", 1)[1]
        missing = delta_criteria(text, spec) - covered
        require(not missing, "Delta критерии не покрыты тестами: " + "; ".join(" / ".join(item[:3]) for item in sorted(missing)))


def git_text(store: Path, commit: str, relative: str, optional: bool = False) -> str:
    safe_path(store, relative)
    result = subprocess.run(["git", "-C", str(store), "show", f"{commit}:{relative}"], capture_output=True, text=True)
    if optional and result.returncode != 0:
        return ""
    require(result.returncode == 0, f"Исторический файл отсутствует: {relative}")
    return result.stdout


def assert_merged_specs(store: Path, source_commit: str, spec_hashes: dict, deltas: dict[str, str], allow_original: bool = False) -> None:
    by_spec = {"openspec/specs/" + p.split("/specs/", 1)[1]: text for p, text in deltas.items()}
    for relative in set(spec_hashes) | set(by_spec):
        original = git_text(store, source_commit, relative, optional=relative not in spec_hashes)
        expected = merge_requirement_text(original, by_spec.get(relative, ""))
        path = safe_path(store, relative)
        actual = path.read_text() if path.is_file() else ""
        normalize_blocks = lambda content: {title: normalized(body) for title, body in requirement_blocks(content).items()}
        if relative not in by_spec:
            require(path.is_file() and digest(path.read_bytes()) == spec_hashes[relative], "Незатронутая spec изменена после прогона")
        else:
            allowed = [normalize_blocks(expected)]
            if allow_original:
                allowed.append(normalize_blocks(original))
            require(normalize_blocks(actual) in allowed, f"Результат delta merge не соответствует проверенной spec: {relative}")


def assert_traceability(case: dict, store: Path, change: str | None = None) -> None:
    for link in case["links"]:
        require(isinstance(link, dict), "Некорректная связь с criterion")
        relative = link.get("spec", "")
        require(isinstance(relative, str) and relative.startswith("openspec/specs/") and relative.endswith("/spec.md"), "Связь должна указывать на основную spec")
        text = effective_spec(store, relative, change)
        require(bool(text), f"Spec отсутствует: {relative}")
        requirement, scenario, criterion = (link.get(k, "") for k in ("requirement", "scenario", "criterion"))
        require(all(isinstance(v, str) and v.strip() for v in (requirement, scenario, criterion)), "Неполная связь criterion")
        requirement_block = re.search(r"^### Requirement: " + re.escape(requirement) + r"\s*\n(.*?)(?=^### Requirement: |\Z)", text, re.M | re.S)
        require(requirement_block is not None, f"Requirement отсутствует: {requirement}")
        scenario_block = re.search(r"^#### Scenario: " + re.escape(scenario) + r"\s*\n(.*?)(?=^#### Scenario: |\Z)", requirement_block.group(1), re.M | re.S)
        require(scenario_block is not None, f"Scenario отсутствует: {scenario}")
        normalized = lambda v: re.sub(r"\s+", " ", re.sub(r"\*\*|`", "", v)).strip()
        require(normalized(criterion) in normalized(scenario_block.group(1)), f"Критерий изменён/отсутствует: {case['id']}")


def validate_report(report: dict, cases: list[dict], change: str, require_promoted: bool = True, manifest_bytes: bytes | None = None) -> None:
    require(report.get("schema_version") == 1, "Неверная версия отчёта")
    require(report.get("complete") is True and report.get("status") == "PASS", "Прогон не завершён успешно")
    require(report.get("errors", []) == [], "Отчёт содержит ошибки")
    require(bool(report.get("run_id")) and bool(report.get("started_at")) and bool(report.get("finished_at")), "Отчёт не содержит времени завершения/run ID")
    manifest = report.get("manifest")
    require(isinstance(manifest, dict) and manifest.get("schema_version") == 1, "Manifest отсутствует/неверен")
    if manifest_bytes is None:
        expected_manifest_hash = json_digest(manifest)
    else:
        require(json.loads(manifest_bytes) == manifest, "Manifest snapshot отличается от отчёта")
        expected_manifest_hash = digest(manifest_bytes)
    require(report.get("manifest_sha256") == expected_manifest_hash, "Hash manifest не совпадает")
    for name in ("tests", "store", "cd"):
        require(isinstance(manifest.get(name), dict), f"Версия {name} отсутствует")
        require_sha(manifest[name].get("commit"), name)
    services = manifest.get("services")
    require(isinstance(services, dict) and bool(services), "Версии сервисов отсутствуют")
    for name, entry in services.items():
        require(isinstance(entry, dict), "Некорректная версия сервиса")
        require_sha(entry.get("commit"), name)
    require("migrations" in manifest and isinstance(manifest.get("environment"), dict), "Состояние миграций/среды отсутствует")
    expected = expected_cases(cases, change)
    require(bool(expected), "Обязательный набор пуст")
    rows = report.get("cases")
    require(isinstance(rows, list), "Случаи отчёта отсутствуют")
    by_id = {row.get("id"): row for row in rows if isinstance(row, dict)}
    require(len(by_id) == len(rows), "Отчёт содержит повторяющиеся test ID")
    require(set(by_id) == {c["id"] for c in expected}, "Отчёт не подтверждает полный обязательный набор")
    selection = report.get("selection")
    require(isinstance(selection, dict) and not selection.get("ids") and not selection.get("level"), "Диагностический выборочный отчёт не подтверждает archive")
    require(selection.get("change") == change or (selection.get("regression") is True and not selection.get("change")), "Отчёт относится к другому change/набору")
    expected_ids, expected_nodes = {c["id"] for c in expected}, {c["test"] for c in expected}
    for field, values in (("requested_ids", expected_ids), ("executed_ids", expected_ids), ("collected_node_ids", expected_nodes)):
        actual = report.get(field)
        require(isinstance(actual, list) and len(actual) == len(values) and set(actual) == values, f"Неполная коллекция/исполнение: {field}")
    counts = report.get("counts")
    require(isinstance(counts, dict) and counts.get("PASS") == len(expected) and counts.get("total") == len(expected), "Счётчики не соответствуют случаям")
    require(all(counts.get(status, 0) == 0 for status in ("FAIL", "ERROR", "SKIP", "XFAIL", "XPASS", "NOT_RUN")), "Счётчики содержат неуспех")
    require(isinstance(report.get("duration_seconds"), (int, float)) and math.isfinite(report["duration_seconds"]) and report["duration_seconds"] >= 0, "Некорректная длительность")
    for case in expected:
        row = by_id[case["id"]]
        require(row.get("status") == "PASS", f"Обязательный случай не PASS: {case['id']}")
        require(row.get("node_id") == case["test"], f"Node ID изменён: {case['id']}")
        require(row.get("description") == case["description"], f"Описание случая изменено: {case['id']}")
        if require_promoted and case.get("introduced_by") == change:
            require(case["state"] == "regression", f"Promotion не зафиксирован: {case['id']}")


def verify_repo_version(entry: dict, label: str, require_clean: bool = True) -> None:
    require(isinstance(entry.get("repo_root"), str), f"Checkout {label} не указан")
    root = Path(entry["repo_root"])
    require(root.is_dir(), f"Checkout {label} отсутствует")
    require(git(root, "rev-parse", "HEAD") == entry["commit"], f"Revision {label} изменена после прогона")
    if require_clean:
        require(not git(root, "status", "--porcelain", "--untracked-files=normal"), f"Checkout {label} содержит незакоммиченные изменения")
    if "source_hashes" in entry:
        actual = {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in sorted((root / "src").rglob("*.py"))}
        require(entry["source_hashes"] == actual, f"Исходники {label} не соответствуют manifest")


def check(store: Path, tests: Path, change: str, report_path: Path, promoted: bool = True, allow_synced: bool = False) -> dict:
    require(bool(re.fullmatch(r"[a-z0-9][a-z0-9-]*", change)), "Некорректное имя change")
    require(report_path.is_file(), "Отчёт отсутствует; инициируйте прогон по требованию")
    report = read_json(report_path)
    registry_path = tests / "registry.yaml"
    require(registry_path.is_file(), "Registry отсутствует")
    registry_data = registry_path.read_bytes()
    cases = registry_from_bytes(registry_data)
    require(report.get("registry_sha256") == digest(registry_data), "Registry изменён после прогона")
    manifest_path = report_path.parent / "manifest.json"
    require(manifest_path.is_file(), "Manifest snapshot отсутствует")
    validate_report(report, cases, change, promoted, manifest_path.read_bytes())
    summary_path = report_path.parent / "summary.md"
    require(summary_path.is_file(), "Русская сводка отсутствует")
    require(bool(re.search(r"[А-Яа-яЁё]", summary_path.read_text())), "Сводка должна быть на русском языке")
    require(report.get("artifact_sha256", {}).get("summary") == digest(summary_path.read_bytes()), "Hash русской сводки отсутствует/не совпадает")
    for name, expected_hash in report.get("artifact_sha256", {}).items():
        relative = report.get("artifacts", {}).get(name)
        require(isinstance(relative, str), "Отсутствует путь артефакта")
        artifact = safe_path(report_path.parent, relative)
        require(artifact.is_file() and digest(artifact.read_bytes()) == expected_hash, f"Hash артефакта не совпадает: {name}")
    manifest = report["manifest"]
    require(Path(manifest["tests"].get("repo_root", "")).resolve() == tests.resolve(), "Отчёт относится к другой тестовой репе")
    verify_repo_version(manifest["tests"], "tests")
    verify_repo_version(manifest["cd"], "CD")
    for name, entry in manifest["services"].items():
        verify_repo_version(entry, name)
    require(Path(manifest["store"].get("repo_root", "")).resolve() == store.resolve(), "Отчёт относится к другому store")
    source_commit = manifest["store"]["commit"]
    ancestry = subprocess.run(["git", "-C", str(store), "merge-base", "--is-ancestor", source_commit, "HEAD"], capture_output=True)
    require(ancestry.returncode == 0, "Store revision прогона не относится к текущей истории")
    require(manifest["store"].get("delta_hashes") == hash_specs(store, change), "Delta specs изменены после прогона")
    deltas = {path: safe_path(store, path).read_text() for path in manifest["store"]["delta_hashes"]}
    if manifest["store"].get("spec_hashes") != hash_specs(store):
        require(allow_synced, "Основные specs изменены после прогона")
        assert_merged_specs(store, source_commit, manifest["store"]["spec_hashes"], deltas, allow_original=True)
    assert_delta_coverage(cases, deltas, change)
    for case in expected_cases(cases, change):
        assert_traceability(case, store, change)
        source = safe_path(tests, case["test"].split("::", 1)[0])
        function_name = case["test"].split("::")[-1].split("[", 1)[0]
        require(source.is_file(), f"Исходник теста отсутствует: {case['id']}")
        try:
            tree = ast.parse(source.read_text())
        except (SyntaxError, OSError) as exc:
            raise GateError("Исходник теста не читается") from exc
        docs = [ast.get_docstring(n) or "" for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == function_name]
        require(any(re.search(r"[А-Яа-яЁё]", d) for d in docs), f"Русский docstring отсутствует: {case['id']}")
    return report


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def archive(store: Path, tests: Path, change: str, report_path: Path, operation_id: str, execute=None) -> dict:
    require(bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", operation_id)), "Некорректный operation ID")
    record = store / ".archive-operations" / (operation_id + ".json")
    report_sha = digest(report_path.read_bytes()) if report_path.is_file() else ""
    previous = read_json(record) if record.exists() else None
    active = store / "openspec/changes" / change
    if previous:
        require(previous.get("change") == change and previous.get("report_sha256") == report_sha, "Operation ID уже связан с другим входом; нужен новый прогон/ID")
        destination = Path(previous.get("archive_path", ""))
        if previous.get("state") == "complete":
            require(destination.is_dir() and not active.exists(), "Завершённая операция не соответствует состоянию файлов")
            return previous
        if not active.exists() and destination.is_dir():
            require((destination / "regression-evidence.json").is_file(), "Archive без evidence")
            previous["state"] = "complete"
            atomic_json(record, previous)
            return previous
    require(active.is_dir(), "Активный change отсутствует")
    report = check(store, tests, change, report_path, allow_synced=previous is not None)
    tasks = active / "tasks.md"
    require(tasks.is_file(), "Tasks отсутствуют")
    boxes = re.findall(r"^\s*-\s*\[([^]]*)\]", tasks.read_text(), re.M)
    require(bool(boxes) and all(box.strip().lower() == "x" for box in boxes), "Tasks не завершены/отсутствуют")
    date = datetime.now(timezone.utc).date().isoformat()
    archive_path = store / "openspec/changes/archive" / f"{date}-{change}"
    require(not archive_path.exists(), "Целевой archive уже существует")
    value = {"schema_version": 1, "operation_id": operation_id, "change": change, "report_sha256": report_sha, "archive_path": str(archive_path), "state": "validated"}
    atomic_json(record, value)
    (active / "run-results.json").write_bytes(report_path.read_bytes())
    (active / "run-manifest.json").write_bytes((report_path.parent / "manifest.json").read_bytes())
    (active / "run-summary.md").write_bytes((report_path.parent / "summary.md").read_bytes())
    (active / "regression-registry.yaml").write_bytes((tests / "registry.yaml").read_bytes())
    evidence = {"schema_version": 1, "operation_id": operation_id, "change": change, "run_id": report["run_id"], "report_sha256": report_sha, "registry_sha256": report["registry_sha256"], "tested_store_commit": report["manifest"]["store"]["commit"]}
    atomic_json(active / "regression-evidence.json", evidence)
    command = ["openspec", "archive", change, "--yes", "--json"]
    identity = store / ".openspec-store/store.yaml"
    if identity.is_file():
        command += ["--store", yaml.safe_load(identity.read_text())["id"]]
    result = (execute or subprocess.run)(command, cwd=store, text=True, capture_output=True)
    require(result.returncode == 0, "OpenSpec archive не завершён; change и evidence сохранены для повторного запуска")
    require(archive_path.is_dir() and not active.exists(), "Archive не переместил change в ожидаемый каталог")
    value["state"] = "complete"
    atomic_json(record, value)
    return value


def validate_archived(store: Path, base: str, head: str = "HEAD") -> dict:
    names = git(store, "diff", "--name-only", "--no-renames", "--diff-filter=AMD", base, head, "--", "openspec/changes/archive").splitlines()
    roots = sorted({str(Path(name).parent) for name in names if Path(name).name == "regression-evidence.json"})
    changed_roots = sorted({"/".join(Path(name).parts[:4]) for name in names if len(Path(name).parts) >= 5})
    for relative in changed_roots:
        root = safe_path(store, relative)
        require((root / "regression-evidence.json").is_file(), f"Прямой archive без evidence: {relative}")
        require(relative in roots or (root / "regression-evidence.json").is_file(), "Archive evidence отсутствует")
        evidence = read_json(root / "regression-evidence.json")
        report_path = root / "run-results.json"
        require(report_path.is_file(), "Archive без отчёта")
        report = read_json(report_path)
        registry_path = root / "regression-registry.yaml"
        require(registry_path.is_file(), "Archive без registry snapshot")
        data = registry_path.read_bytes()
        require(evidence.get("report_sha256") == digest(report_path.read_bytes()), "Archived report hash не совпадает")
        require(evidence.get("registry_sha256") == digest(data) == report.get("registry_sha256"), "Archived registry hash не совпадает")
        require(evidence.get("run_id") == report.get("run_id"), "Archived run ID не совпадает")
        change = evidence.get("change")
        require(isinstance(change, str) and relative.endswith("-" + change), "Archive change ID не совпадает")
        cases = registry_from_bytes(data)
        manifest_path = root / "run-manifest.json"
        require(manifest_path.is_file(), "Archived manifest snapshot отсутствует")
        validate_report(report, cases, change, manifest_bytes=manifest_path.read_bytes())
        summary_path = root / "run-summary.md"
        require(summary_path.is_file() and report.get("artifact_sha256", {}).get("summary") == digest(summary_path.read_bytes()), "Archived русская сводка/hash отсутствует")
        require(bool(re.search(r"[А-Яа-яЁё]", summary_path.read_text())), "Archived сводка должна быть на русском языке")
        tasks_path = root / "tasks.md"
        require(tasks_path.is_file(), "Archived tasks отсутствуют")
        boxes = re.findall(r"^\s*-\s*\[([^]]*)\]", tasks_path.read_text(), re.M)
        require(bool(boxes) and all(box.strip().lower() == "x" for box in boxes), "Archived tasks не завершены/отсутствуют")
        source_commit = evidence.get("tested_store_commit")
        require_sha(source_commit, "tested store")
        require(source_commit == report["manifest"]["store"]["commit"], "Archived tested revision не совпадает")
        for spec, expected_hash in report["manifest"]["store"].get("spec_hashes", {}).items():
            require(isinstance(spec, str) and spec.startswith("openspec/specs/") and spec.endswith("/spec.md"), "Некорректный исторический spec path")
            result = subprocess.run(["git", "-C", str(store), "show", f"{source_commit}:{spec}"], capture_output=True)
            require(result.returncode == 0 and digest(result.stdout) == expected_hash, "Исторический spec hash не совпадает")
        deltas = {}
        for relative_delta, expected_hash in report["manifest"]["store"].get("delta_hashes", {}).items():
            require(relative_delta.startswith(f"openspec/changes/{change}/specs/"), "Некорректный delta path")
            original = subprocess.run(["git", "-C", str(store), "show", f"{source_commit}:{relative_delta}"], capture_output=True)
            require(original.returncode == 0 and digest(original.stdout) == expected_hash, "Исторический delta hash не совпадает")
            archived_delta = root / "specs" / relative_delta.split("/specs/", 1)[1]
            require(archived_delta.is_file() and digest(archived_delta.read_bytes()) == expected_hash, "Archived delta hash не совпадает")
            deltas[relative_delta] = archived_delta.read_text()
        assert_delta_coverage(cases, deltas, change)
        assert_merged_specs(store, source_commit, report["manifest"]["store"]["spec_hashes"], deltas)
        for case in expected_cases(cases, change):
            assert_traceability(case, store)
    return {"schema_version": 1, "status": "PASS", "archives_checked": len(changed_roots)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "archive", "validate-archives"])
    parser.add_argument("--store", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--tests", type=Path)
    parser.add_argument("--change")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--operation-id")
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args(argv)
    try:
        if args.action == "validate-archives":
            require(bool(args.base), "Для CI нужен --base")
            result = validate_archived(args.store.resolve(), args.base, args.head)
        else:
            require(args.tests is not None and args.report is not None and args.change is not None, "Нужны --tests, --report и --change")
            if args.action == "check":
                report = check(args.store.resolve(), args.tests.resolve(), args.change, args.report.resolve())
                result = {"status": "PASS", "run_id": report["run_id"]}
            else:
                require(bool(args.operation_id), "Для archive нужен --operation-id")
                result = archive(args.store.resolve(), args.tests.resolve(), args.change, args.report.resolve(), args.operation_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (GateError, OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
