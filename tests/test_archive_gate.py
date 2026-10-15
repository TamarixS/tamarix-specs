"""Gate и archive lifecycle в одноразовых Git-репах; это проверки tooling, не HTTP e2e."""

from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
from types import SimpleNamespace

import pytest
import yaml


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools/archive_gate.py"
SPEC = importlib.util.spec_from_file_location("tamarix_archive_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

CHANGE = "demo-change"
SPEC_PATH = "openspec/specs/access/spec.md"
REQUIREMENT = "Проверка решения"
SCENARIO = "Опасный запрос"
CRITERION = "Система SHALL возвращать запрет"
BASELINE_REQUIREMENT = "Общий безопасный ответ"
BASELINE_SCENARIO = "Безопасный запрос"
BASELINE_CRITERION = "Система SHALL возвращать разрешение"


def spec_text(requirement=REQUIREMENT, criterion=CRITERION, include_current=True):
    current = f"""### Requirement: {requirement}

Система SHALL проверять доступ для опасного запроса.

#### Scenario: {SCENARIO}

- **WHEN** получен опасный запрос
- **THEN** {criterion}

""" if include_current else ""
    return f"""# access Specification

## Purpose

Минимальная спецификация одноразового тестового store.

## Requirements

{current}### Requirement: {BASELINE_REQUIREMENT}

Система SHALL разрешать безопасный запрос.

#### Scenario: {BASELINE_SCENARIO}

- **WHEN** получен безопасный запрос
- **THEN** {BASELINE_CRITERION}
"""


def git(root, *arguments):
    result = subprocess.run(["git", "-C", str(root), *arguments], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def init_repo(root):
    root.mkdir()
    git(root, "init", "--initial-branch=main")
    (root / ".gitignore").write_text(".archive-operations/\n")


def commit(root):
    git(root, "add", "-A")
    git(root, "-c", "user.name=Gate Tests", "-c", "user.email=gate-tests@example.invalid", "commit", "-m", "Тестовый checkpoint")
    return git(root, "rev-parse", "HEAD")


@dataclass
class Workspace:
    store: Path
    tests: Path
    cd: Path
    service: Path
    report_path: Path
    cases: list
    report: dict

    @property
    def active(self):
        return self.store / "openspec/changes" / CHANGE

    def save_registry(self):
        (self.tests / "registry.yaml").write_text(yaml.safe_dump(
            {"schema_version": 1, "cases": self.cases}, allow_unicode=True, sort_keys=False
        ))

    def save_report(self):
        manifest_data = json.dumps(self.report["manifest"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        self.report["manifest_sha256"] = gate.digest(manifest_data)
        (self.report_path.parent / "manifest.json").write_bytes(manifest_data)
        summary = self.report_path.parent / "summary.md"
        summary.write_text(f"# Отчёт tooling прогона\n\nПрогон `{self.report['run_id']}` завершён: PASS.\n\nПроверяются критерии одноразовой тестовой среды; предметный HTTP e2e не выполнялся.\n")
        self.report["artifact_sha256"] = {"summary": gate.digest(summary.read_bytes()), "manifest": gate.digest(manifest_data)}
        self.report_path.write_text(json.dumps(self.report, ensure_ascii=False, indent=2))

    def final_report(self):
        """Моделирует полный PASS уже зафиксированного tests checkpoint, без запуска runtime."""
        self.report["registry_sha256"] = gate.digest((self.tests / "registry.yaml").read_bytes())
        self.report["manifest"]["tests"]["commit"] = git(self.tests, "rev-parse", "HEAD")
        self.report["manifest"]["store"]["commit"] = git(self.store, "rev-parse", "HEAD")
        self.report["manifest"]["store"]["spec_hashes"] = gate.hash_specs(self.store)
        self.report["manifest"]["store"]["delta_hashes"] = gate.hash_specs(self.store, CHANGE)
        expected = gate.expected_cases(self.cases, CHANGE)
        self.report["requested_ids"] = [case["id"] for case in expected]
        self.report["executed_ids"] = [case["id"] for case in expected]
        self.report["collected_node_ids"] = [case["test"] for case in expected]
        self.report["cases"] = [dict(id=case["id"], node_id=case["test"], description=case["description"],
                                     status="PASS", duration_seconds=0.01, error=None, artifacts=[]) for case in expected]
        self.report["counts"] = {"PASS": len(expected), "total": len(expected)}
        self.save_report()
        self.review_docs()

    def review_docs(self):
        """Обновить только fixture review после осознанного изменения исходных артефактов."""
        path = self.active / "docs-review.json"
        value = gate.docs.prepare_review(self.store, CHANGE, "HEAD~1", refresh=path.exists())
        for page, section in value["sections"].items():
            section.update(status="updated", reason="Страница проверена по согласованным исходным артефактам тестовой среды.")
        gate.atomic_json(path, value)


@pytest.fixture
def workspace(tmp_path):
    store, tests, cd, service = (tmp_path / name for name in ("store", "tests-repo", "cd", "service"))
    for root in (store, tests, cd, service):
        init_repo(root)
    commit(store)
    for relative in gate.docs.REQUIRED_PAGES:
        path = store / relative
        path.parent.mkdir(exist_ok=True)
        path.write_text("# Тестовая документация\n\nОписание изолированной среды.\n\n```mermaid\nflowchart LR\n  A --> B\n```\n")
    path = store / SPEC_PATH
    path.parent.mkdir(parents=True)
    path.write_text(spec_text())
    (store / "openspec/config.yaml").write_text("schema: spec-driven\n")
    active = store / "openspec/changes" / CHANGE
    active.mkdir(parents=True)
    (active / ".openspec.yaml").write_text("schema: spec-driven\ncreated: 2026-10-14\nskip_specs: true\n")
    (active / "proposal.md").write_text("""## Why

Проверить tooling lifecycle в изолированной репе.

## What Changes

- Внедрить проверяемый lifecycle отчётов и регресса.

## Capabilities

### New Capabilities

Нет предметных изменений.

### Modified Capabilities

Нет предметных изменений.

## Impact

Только одноразовые репозитории теста.
""")
    (active / "design.md").write_text("# Design\n\nTooling test в одноразовой среде.\n")
    (active / "tasks.md").write_text("# Tasks\n\n- [x] 1.1 Проверить завершённый набор\n")
    test_source = tests / "tests/integration/test_sample.py"
    test_source.parent.mkdir(parents=True)
    test_source.write_text('''def test_deny():
    """При опасном запросе ожидает запрет; применяется для проверки tooling traceability."""
    assert True


def test_allow():
    """При безопасном запросе ожидает разрешение; представляет прежний регресс в tooling fixture."""
    assert True
''')
    cases = [
        dict(id="new-deny", description="Опасный запрос даёт запрет; защищает критерий решения в tooling fixture.",
             level="integration", state="regression", introduced_by=CHANGE,
             test="tests/integration/test_sample.py::test_deny",
             links=[dict(spec=SPEC_PATH, requirement=REQUIREMENT, scenario=SCENARIO, criterion=CRITERION)]),
        dict(id="existing-allow", description="Безопасный запрос разрешается; сохраняет прежний регресс в tooling fixture.",
             level="integration", state="regression", introduced_by="previous-change",
             test="tests/integration/test_sample.py::test_allow",
             links=[dict(spec=SPEC_PATH, requirement=BASELINE_REQUIREMENT, scenario=BASELINE_SCENARIO, criterion=BASELINE_CRITERION)]),
    ]
    (cd / "manifest-contract.md").write_text("Тестовый контракт среды.\n")
    (service / "src").mkdir()
    (service / "src/core.py").write_text("VALUE = 'test fixture'\n")
    report_path = tmp_path / "reports/results.json"
    report_path.parent.mkdir()
    report = dict(schema_version=1, complete=True, status="PASS", run_id="gate-fixture-run",
                  started_at="2026-10-14T10:00:00+00:00", finished_at="2026-10-14T10:00:01+00:00",
                  duration_seconds=1.0, selection=dict(change=CHANGE, ids=[], level=None, regression=False,
                                                       bootstrap_empty_regression=False),
                  artifacts={"manifest": "manifest.json", "summary": "summary.md"}, errors=[])
    result = Workspace(store, tests, cd, service, report_path, cases, report)
    result.save_registry()
    commits = {name: commit(root) for name, root in (("store", store), ("tests", tests), ("cd", cd), ("service", service))}
    report["manifest"] = dict(
        schema_version=1,
        tests=dict(repo_root=str(tests), commit=commits["tests"]),
        store=dict(repo_root=str(store), commit=commits["store"], spec_hashes={}, delta_hashes={}),
        cd=dict(repo_root=str(cd), commit=commits["cd"]),
        services={"test-service": dict(repo_root=str(service), commit=commits["service"], endpoint=None, image_digest=None,
                                        source_hashes={"src/core.py": gate.digest((service / "src/core.py").read_bytes())})},
        environment=dict(id="isolated-gate-fixture", scope="logical-integration", python=platform.python_version()),
        migrations=None,
    )
    result.final_report()
    return result


def active_snapshot(workspace):
    return {path.relative_to(workspace.active).as_posix(): path.read_bytes()
            for path in workspace.active.rglob("*") if path.is_file()}


def fake_archive(workspace, returncode=0):
    def execute(command, **kwargs):
        assert command[:3] == ["openspec", "archive", CHANGE]
        assert "--no-validate" not in command
        operation = next((workspace.store / ".archive-operations").glob("*.json"))
        destination = Path(json.loads(operation.read_text())["archive_path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(workspace.active, destination)
        return SimpleNamespace(returncode=returncode, stdout="fixture archive", stderr="")
    return execute


def test_current_full_promoted_report_passes(workspace):
    """Полный PASS двух случаев на чистых commits допускается; задаёт позитивный контроль проверки evidence."""
    assert gate.check(workspace.store, workspace.tests, CHANGE, workspace.report_path)["status"] == "PASS"


@pytest.mark.parametrize("mutation,description", [
    pytest.param("missing", "Отсутствующий отчёт запрещает archive без запуска тестов.", id="missing"),
    pytest.param("FAIL", "Провал обязательного случая запрещает archive.", id="fail"),
    pytest.param("SKIP", "Пропущенный обязательный случай не подтверждает успех.", id="skip"),
    pytest.param("XFAIL", "Ожидаемый провал обязательного случая не подтверждает успех.", id="xfail"),
    pytest.param("NOT_RUN", "Не начавшийся обязательный случай запрещает archive.", id="not-run"),
    pytest.param("incomplete", "Незавершённый снимок с PASS строками запрещает archive.", id="incomplete"),
    pytest.param("partial", "Отчёт только нового случая без прежнего регресса запрещает archive.", id="partial"),
    pytest.param("collection", "Полный список PASS при неполной коллекции запрещает archive.", id="partial-collection"),
    pytest.param("diagnostic", "Выборочный диагностический запуск не подтверждает полный допуск.", id="diagnostic-selection"),
])
def test_invalid_report_preserves_change_without_hidden_execution(workspace, monkeypatch, mutation, description):
    """При непригодном отчёте ожидает GateError и неизменный активный change.

    Причина каждого случая пояснена у параметров; применяется для защиты
    от ложного PASS, потери change и незаказанного неявного запуска тестов.
    """
    assert description
    before = active_snapshot(workspace)
    if mutation == "missing":
        workspace.report_path.unlink()
    elif mutation in {"FAIL", "SKIP", "XFAIL", "NOT_RUN"}:
        workspace.report["cases"][0]["status"] = mutation
    elif mutation == "incomplete":
        workspace.report["complete"] = False
    elif mutation == "partial":
        workspace.report["cases"].pop()
    elif mutation == "collection":
        workspace.report["collected_node_ids"].pop()
    else:
        workspace.report["selection"]["ids"] = [workspace.cases[0]["id"]]
    if mutation != "missing":
        workspace.save_report()
    original_run = subprocess.run
    def only_read_git(command, *args, **kwargs):
        assert command[0] == "git", "Gate не должен неявно запускать pytest/runner/archive"
        return original_run(command, *args, **kwargs)
    monkeypatch.setattr(gate.subprocess, "run", only_read_git)
    def forbidden_archive(*args, **kwargs):
        pytest.fail("Отказ должен происходить до вызова archive")
    with pytest.raises(gate.GateError):
        gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "rejected-run", execute=forbidden_archive)
    assert active_snapshot(workspace) == before
    assert not (workspace.store / ".archive-operations/rejected-run.json").exists()


@pytest.mark.parametrize("target,description", [
    pytest.param("tests", "Другой tests commit после прогона запрещает использование отчёта.", id="tests-revision"),
    pytest.param("registry", "Изменённый registry hash запрещает использование отчёта.", id="registry-hash"),
    pytest.param("service", "Другой commit сервиса запрещает использование отчёта.", id="service-revision"),
    pytest.param("source", "Ложный source hash сервиса запрещает использование отчёта при том же commit.", id="source-hash"),
    pytest.param("spec", "Изменение основных specs после прогона запрещает archive.", id="spec-hash"),
    pytest.param("delta", "Изменение delta specs после прогона запрещает archive.", id="delta-hash"),
    pytest.param("manifest", "Некорректный manifest hash запрещает использование отчёта.", id="manifest-hash"),
])
def test_stale_inputs_block_gate(workspace, target, description):
    """Меняет один проверяемый вход и ожидает GateError; защищает привязку прогона к конкретным версиям и spec hashes."""
    assert description
    if target == "tests":
        (workspace.tests / "readme.md").write_text("Другой tests checkpoint\n")
        commit(workspace.tests)
    elif target == "registry":
        workspace.cases[0]["description"] += " Изменено после прогона."
        workspace.save_registry()
        commit(workspace.tests)
    elif target == "service":
        (workspace.service / "src/core.py").write_text("VALUE = 'changed'\n")
        commit(workspace.service)
    elif target == "source":
        workspace.report["manifest"]["services"]["test-service"]["source_hashes"]["src/core.py"] = "0" * 64
        workspace.save_report()
    elif target == "spec":
        (workspace.store / SPEC_PATH).write_text(spec_text(criterion="Система SHALL возвращать другой результат"))
    elif target == "delta":
        path = workspace.active / "specs/access/spec.md"
        path.parent.mkdir(parents=True)
        path.write_text("## MODIFIED Requirements\n" + spec_text())
    else:
        workspace.report["manifest_sha256"] = "0" * 64
        workspace.report_path.write_text(json.dumps(workspace.report))
    with pytest.raises(gate.GateError):
        gate.check(workspace.store, workspace.tests, CHANGE, workspace.report_path)


@pytest.mark.parametrize("missing,description", [
    pytest.param("registry", "Английское registry description отвергается.", id="registry-description"),
    pytest.param("docstring", "Английский docstring исходника отвергается.", id="test-docstring"),
    pytest.param("promotion", "Candidate не допускается к archive без зафиксированного promotion.", id="promotion"),
])
def test_russian_descriptions_and_promotion_required(workspace, missing, description):
    """Обновляет вход и полный report согласованно, затем ожидает отказ по отсутствующему русскому описанию или promotion."""
    assert description
    if missing == "registry":
        workspace.cases[0]["description"] = "Checks denied access for tooling fixture."
    elif missing == "promotion":
        workspace.cases[0]["state"] = "candidate"
    else:
        source = workspace.tests / workspace.cases[0]["test"].split("::")[0]
        source.write_text(source.read_text().replace("При опасном запросе ожидает запрет; применяется для проверки tooling traceability.", "Denied request tooling fixture."))
    workspace.save_registry()
    commit(workspace.tests)
    workspace.final_report()
    with pytest.raises(gate.GateError):
        gate.check(workspace.store, workspace.tests, CHANGE, workspace.report_path)


def test_open_task_blocks_before_archive(workspace):
    """При незавершённой задаче даже полный PASS не архивируется; защищает критерии завершения change."""
    (workspace.active / "tasks.md").write_text("# Tasks\n\n- [ ] 1.1 Незавершённая задача\n")
    workspace.review_docs()
    called = []
    with pytest.raises(gate.GateError, match="Tasks"):
        gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "open-task", execute=lambda *a, **k: called.append(a))
    assert called == []
    assert workspace.active.is_dir()


@pytest.mark.parametrize("moved,description", [
    pytest.param(False, "OpenSpec отказал до перемещения: retry повторяет archive один раз.", id="before-move"),
    pytest.param(True, "OpenSpec переместил change, но вернул ошибку: retry распознаёт готовый archive.", id="after-move"),
])
def test_partial_operation_resumes_and_completed_is_idempotent(workspace, moved, description):
    """Сохраняет частичную операцию, продолжает её тем же входом и повторяет завершённую без второго archive; защищает безопасный retry."""
    assert description
    calls = []
    def first(command, **kwargs):
        calls.append(command)
        if moved:
            return fake_archive(workspace, returncode=1)(command, **kwargs)
        return SimpleNamespace(returncode=1, stdout="", stderr="объявленный отказ")
    with pytest.raises(gate.GateError):
        gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "retry", execute=first)
    def second(command, **kwargs):
        calls.append(command)
        return fake_archive(workspace)(command, **kwargs)
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "retry", execute=second)
    assert value["state"] == "complete"
    assert len(calls) == (1 if moved else 2)
    again = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "retry", execute=second)
    assert again == value
    assert len(calls) == (1 if moved else 2)
    assert Path(value["archive_path"]).is_dir()
    assert not workspace.active.exists()


def test_operation_id_rejects_changed_report(workspace):
    """После завершения меняет run ID отчёта: прежний operation ID отвергается; защищает привязку операции к неизменяемому входу."""
    gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "fixed-input", execute=fake_archive(workspace))
    workspace.report["run_id"] = "different-run"
    workspace.save_report()
    with pytest.raises(gate.GateError, match="другим входом"):
        gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "fixed-input")


def test_direct_archive_without_evidence_is_rejected(workspace):
    """Перемещает change напрямую без evidence и коммитит: CI gate должен отказать; контролирует обход обёртки archive."""
    base = git(workspace.store, "rev-parse", "HEAD")
    destination = workspace.store / "openspec/changes/archive/2026-10-14-demo-change"
    destination.parent.mkdir(parents=True)
    shutil.move(workspace.active, destination)
    commit(workspace.store)
    with pytest.raises(gate.GateError, match="без evidence"):
        gate.validate_archived(workspace.store, base)


@pytest.mark.parametrize("corrupt,description", [
    pytest.param("report-hash", "Изменение сохранённого отчёта нарушает evidence hash.", id="report-hash"),
    pytest.param("registry-hash", "Изменение snapshot registry нарушает evidence hash.", id="registry-hash"),
    pytest.param("tasks", "Незавершённая archived task запрещает принятие archive.", id="tasks"),
    pytest.param("source-spec-hash", "Hash исходной spec должен соответствовать tested store commit.", id="source-spec-hash"),
])
def test_archive_ci_rejects_corrupted_evidence(workspace, corrupt, description):
    """Создаёт полный archive и портит один артефакт: ожидает CI GateError; защищает целостность и завершённость archived evidence."""
    assert description
    base = git(workspace.store, "rev-parse", "HEAD")
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "ci-corrupt", execute=fake_archive(workspace))
    destination = Path(value["archive_path"])
    if corrupt == "report-hash":
        (destination / "run-results.json").write_text("{}")
    elif corrupt == "registry-hash":
        (destination / "regression-registry.yaml").write_text("schema_version: 1\ncases: []\n")
    elif corrupt == "tasks":
        (destination / "tasks.md").write_text("- [ ] Требует выполнения\n")
    else:
        report = gate.read_json(destination / "run-results.json")
        report["manifest"]["store"]["spec_hashes"][SPEC_PATH] = "0" * 64
        report["manifest_sha256"] = gate.json_digest(report["manifest"])
        report["artifact_sha256"]["manifest"] = report["manifest_sha256"]
        (destination / "run-manifest.json").write_text(json.dumps(report["manifest"], ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        gate.atomic_json(destination / "run-results.json", report)
        evidence = gate.read_json(destination / "regression-evidence.json")
        evidence["report_sha256"] = gate.digest((destination / "run-results.json").read_bytes())
        gate.atomic_json(destination / "regression-evidence.json", evidence)
    commit(workspace.store)
    with pytest.raises(gate.GateError):
        gate.validate_archived(workspace.store, base)


def test_real_openspec_lifecycle_and_archived_ci(workspace):
    """В одноразовой репе выполняет candidate → promotion commit → final PASS → настоящий OpenSpec archive и CI проверку.

    Runtime-прогон представлен реалистичным fixture report; ожидается один archive
    с согласованными snapshots. Применяется для проверки настоящего CLI и lifecycle tooling.
    """
    assert shutil.which("openspec"), "Для задачи проверки нужен установленный openspec"
    workspace.cases[0]["state"] = "candidate"
    workspace.save_registry()
    commit(workspace.tests)
    workspace.final_report()
    assert gate.check(workspace.store, workspace.tests, CHANGE, workspace.report_path, promoted=False)
    with pytest.raises(gate.GateError, match="Promotion"):
        gate.check(workspace.store, workspace.tests, CHANGE, workspace.report_path)
    previous_tests_commit = workspace.report["manifest"]["tests"]["commit"]
    workspace.cases[0]["state"] = "regression"
    workspace.save_registry()
    commit(workspace.tests)
    workspace.final_report()
    assert workspace.report["manifest"]["tests"]["commit"] != previous_tests_commit
    base = git(workspace.store, "rev-parse", "HEAD")
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "actual-openspec")
    commit(workspace.store)
    assert value["state"] == "complete"
    assert gate.validate_archived(workspace.store, base)["archives_checked"] == 1
    assert gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "actual-openspec") == value


@pytest.mark.parametrize("operation,description", [
    pytest.param("MODIFIED", "Изменённый критерий связывается с целевой spec и новым registry.", id="modified"),
    pytest.param("RENAMED", "Переименованное требование сохраняет критерий через обновлённую связь.", id="renamed"),
    pytest.param("REMOVED", "Удалённое требование выводит случай из регресса с причиной и change.", id="removed"),
])
def test_requirement_evolution_archives_against_target_specs(workspace, operation, description):
    """Проверяет prospective target traceability и итоговый CI для MODIFIED/RENAMED/REMOVED через настоящий OpenSpec в временном store."""
    assert description
    delta = workspace.active / "specs/access/spec.md"
    delta.parent.mkdir(parents=True)
    new_requirement, new_criterion = REQUIREMENT, CRITERION
    if operation == "MODIFIED":
        new_criterion = "Система SHALL возвращать явный Deny"
        delta.write_text(f"## MODIFIED Requirements\n\n### Requirement: {REQUIREMENT}\n\nСистема SHALL проверять опасный запрос.\n\n#### Scenario: {SCENARIO}\n\n- **WHEN** получен опасный запрос\n- **THEN** {new_criterion}\n")
        workspace.cases[0]["links"][0]["criterion"] = new_criterion
    elif operation == "RENAMED":
        new_requirement = "Переименованная проверка решения"
        delta.write_text(f"## RENAMED Requirements\n\n- FROM: `### Requirement: {REQUIREMENT}`\n- TO: `### Requirement: {new_requirement}`\n")
        workspace.cases[0]["links"][0]["requirement"] = new_requirement
    else:
        delta.write_text(f"## REMOVED Requirements\n\n### Requirement: {REQUIREMENT}\n\n**Reason**: Требование удалено тестовым change.\n**Migration**: Случай выведен из регресса.\n")
        workspace.cases[0].update(state="retired", retired_by=CHANGE,
                                  retirement_reason="Требование удалено согласованным demo-change.")
    (workspace.active / ".openspec.yaml").write_text("schema: spec-driven\ncreated: 2026-10-14\n")
    (workspace.active / "proposal.md").write_text("""## Why

Проверить эволюцию требования в tooling fixture.

## What Changes

- Изменить выбранное требование и его прослеживаемость.

## Capabilities

### New Capabilities

Нет.

### Modified Capabilities

- `access`: эволюция проверяемого требования.

## Impact

Только временный store и fixture registry.
""")
    workspace.save_registry()
    commit(workspace.tests)
    commit(workspace.store)
    workspace.final_report()
    base = git(workspace.store, "rev-parse", "HEAD")
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "evolution-" + operation.lower())
    commit(workspace.store)
    assert value["state"] == "complete"
    text = (workspace.store / SPEC_PATH).read_text()
    if operation == "REMOVED":
        assert f"### Requirement: {REQUIREMENT}" not in text
    else:
        assert f"### Requirement: {new_requirement}" in text
        assert new_criterion in text
    assert gate.validate_archived(workspace.store, base)["archives_checked"] == 1


@pytest.mark.parametrize("invalid,description", [
    pytest.param("summary-missing", "Отсутствующая русская сводка делает PASS отчёт неполным.", id="summary-missing"),
    pytest.param("summary-english", "Английская сводка с верным hash не удовлетворяет русской отчётности.", id="summary-english"),
    pytest.param("hashes-cleared", "Очищенный словарь artifact hashes не подтверждает целостность сводки.", id="artifact-hashes-cleared"),
    pytest.param("errors", "Непустой список ошибок запрещает PASS даже при успешных строках случаев.", id="report-errors"),
])
def test_report_summary_integrity_and_errors_required(workspace, invalid, description):
    """При отсутствующей/нерусской сводке, потерянных hashes или ошибках ожидает GateError; защищает полный достоверный отчёт выполнения."""
    assert description
    if invalid == "summary-missing":
        (workspace.report_path.parent / "summary.md").unlink()
    elif invalid == "summary-english":
        summary = workspace.report_path.parent / "summary.md"
        summary.write_text("# Run summary\n\nAll tests passed in this disposable tooling fixture.\n")
        workspace.report["artifact_sha256"]["summary"] = gate.digest(summary.read_bytes())
    elif invalid == "hashes-cleared":
        workspace.report["artifact_sha256"] = {}
    else:
        workspace.report["errors"] = ["Объявленная ошибка окружения после выполнения"]
    workspace.report_path.write_text(json.dumps(workspace.report, ensure_ascii=False, indent=2))
    with pytest.raises(gate.GateError):
        gate.check(workspace.store, workspace.tests, CHANGE, workspace.report_path)


@pytest.mark.parametrize("missing,description", [
    pytest.param(False, "Tasks без единого checkbox не подтверждают завершённый change.", id="empty"),
    pytest.param(True, "Отсутствующий tasks.md не подтверждает завершённый change.", id="missing"),
])
def test_empty_or_missing_active_tasks_rejected(workspace, missing, description):
    """При пустом/отсутствующем tasks ожидает отказ до вызова CLI и сохранение активного change; закрывает ошибку all([])."""
    assert description
    tasks = workspace.active / "tasks.md"
    if missing:
        tasks.unlink()
    else:
        tasks.write_text("# Tasks\n\nЗадачи ещё не определены.\n")
    called = []
    with pytest.raises(gate.GateError):
        gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "invalid-tasks", execute=lambda *a, **k: called.append(a))
    assert called == []
    assert workspace.active.is_dir()


@pytest.mark.parametrize("missing,description", [
    pytest.param(False, "Archived tasks без checkbox должны быть отклонены CI.", id="empty"),
    pytest.param(True, "Удаление archived tasks должно быть отклонено CI.", id="missing"),
])
def test_empty_or_missing_archived_tasks_rejected(workspace, missing, description):
    """Меняет только tasks уже принятого archive и ожидает GateError; защищает CI от исчезновения критериев завершения."""
    assert description
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "tasks-ci", execute=fake_archive(workspace))
    base = commit(workspace.store)
    tasks = Path(value["archive_path"]) / "tasks.md"
    if missing:
        tasks.unlink()
    else:
        tasks.write_text("# Tasks\n\nЗадачи отсутствуют.\n")
    commit(workspace.store)
    with pytest.raises(gate.GateError):
        gate.validate_archived(workspace.store, base)


@pytest.mark.parametrize("artifact,description", [
    pytest.param("run-results.json", "Удаление только сохранённого отчёта должно блокироваться CI.", id="report-only-deleted"),
    pytest.param("regression-evidence.json", "Удаление только evidence должно блокироваться CI.", id="evidence-only-deleted"),
    pytest.param("run-summary.md", "Удаление только русской archived сводки должно блокироваться CI.", id="summary-only-deleted"),
])
def test_deleting_only_required_archived_artifact_rejected(workspace, artifact, description):
    """После полного archive удаляет один обязательный файл и ожидает GateError; защищает проверку diff, содержащего только D записи."""
    assert description
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "deletion-ci", execute=fake_archive(workspace))
    base = commit(workspace.store)
    path = Path(value["archive_path"]) / artifact
    assert path.is_file(), "Archive обязан сохранить этот отчётный артефакт"
    path.unlink()
    commit(workspace.store)
    with pytest.raises(gate.GateError):
        gate.validate_archived(workspace.store, base)


def test_archive_ci_rejects_english_summary_with_matching_hash(workspace):
    """Подменяет archived сводку английской и согласованно обновляет hashes: ожидает отказ CI по отсутствию русского описания отчёта."""
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "english-summary-ci", execute=fake_archive(workspace))
    base = commit(workspace.store)
    destination = Path(value["archive_path"])
    summary = destination / "run-summary.md"
    summary.write_text("# Run summary\n\nAll cases passed in the disposable fixture.\n")
    report_path = destination / "run-results.json"
    report = gate.read_json(report_path)
    report["artifact_sha256"]["summary"] = gate.digest(summary.read_bytes())
    gate.atomic_json(report_path, report)
    evidence_path = destination / "regression-evidence.json"
    evidence = gate.read_json(evidence_path)
    evidence["report_sha256"] = gate.digest(report_path.read_bytes())
    gate.atomic_json(evidence_path, evidence)
    commit(workspace.store)
    with pytest.raises(gate.GateError):
        gate.validate_archived(workspace.store, base)


def prepare_delta(workspace, text):
    path = workspace.active / "specs/access/spec.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    (workspace.active / ".openspec.yaml").write_text("schema: spec-driven\ncreated: 2026-10-14\n")
    commit(workspace.store)
    workspace.save_registry()
    commit(workspace.tests) if git(workspace.tests, "status", "--porcelain") else None
    workspace.final_report()


@pytest.mark.parametrize("operation,description", [
    pytest.param("ADDED", "Новое требование без тестовой связи не должно допускаться по старому полному набору.", id="added-criterion-uncovered"),
    pytest.param("MODIFIED", "Новый сценарий изменённого требования без связи не должен допускаться по прежним случаям.", id="modified-criterion-uncovered"),
])
def test_incomplete_changed_criterion_coverage_rejected(workspace, operation, description):
    """Добавляет новый критерий в delta, оставляя остальные links и PASS согласованными; ожидает GateError для неполной traceability затронутых критериев."""
    assert description
    if operation == "ADDED":
        delta = """## ADDED Requirements

### Requirement: Новый аудит решения

Система SHALL сохранять аудит решения.

#### Scenario: Решение принято

- **WHEN** принято решение
- **THEN** Система SHALL сохранять запись аудита
"""
    else:
        delta = f"""## MODIFIED Requirements

### Requirement: {REQUIREMENT}

Система SHALL проверять опасный запрос и сохранять аудит.

#### Scenario: {SCENARIO}

- **WHEN** получен опасный запрос
- **THEN** {CRITERION}

#### Scenario: Решение принято

- **WHEN** принято решение
- **THEN** Система SHALL сохранять запись аудита
"""
    prepare_delta(workspace, delta)
    before = active_snapshot(workspace)
    with pytest.raises(gate.GateError):
        gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "uncovered-criterion", execute=fake_archive(workspace))
    assert active_snapshot(workspace) == before


def test_ci_rejects_incomplete_final_delta_merge(workspace):
    """Даёт полный PASS и links двух критериев, но CLI fixture пропускает delta merge; ожидает отказ CI по итоговым основным specs."""
    new_criterion = "Система SHALL сохранять запись аудита"
    workspace.cases[0]["links"].append(dict(spec=SPEC_PATH, requirement=REQUIREMENT, scenario=SCENARIO, criterion=new_criterion))
    delta = f"""## MODIFIED Requirements

### Requirement: {REQUIREMENT}

Система SHALL проверять опасный запрос и сохранять аудит.

#### Scenario: {SCENARIO}

- **WHEN** получен опасный запрос
- **THEN** {CRITERION}
- **AND** {new_criterion}
"""
    prepare_delta(workspace, delta)
    base = git(workspace.store, "rev-parse", "HEAD")
    try:
        value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "incomplete-merge", execute=fake_archive(workspace))
    except gate.GateError:
        # Обёртка тоже может выявить неверный merge после CLI; проверяем CI независимо.
        value = gate.read_json(workspace.store / ".archive-operations/incomplete-merge.json")
    assert Path(value["archive_path"]).is_dir()
    commit(workspace.store)
    with pytest.raises(gate.GateError):
        gate.validate_archived(workspace.store, base)


def test_partial_cli_spec_merge_resumes_before_archive_move(workspace):
    """CLI успевает применить корректную delta, затем падает до перемещения change; retry должен закончить archive с прежним неизменным report."""
    new_criterion = "Система SHALL возвращать явный Deny"
    workspace.cases[0]["links"][0]["criterion"] = new_criterion
    delta = f"""## MODIFIED Requirements

### Requirement: {REQUIREMENT}

Система SHALL проверять опасный запрос.

#### Scenario: {SCENARIO}

- **WHEN** получен опасный запрос
- **THEN** {new_criterion}
"""
    prepare_delta(workspace, delta)
    base = git(workspace.store, "rev-parse", "HEAD")
    report_before = workspace.report_path.read_bytes()
    merged_spec = "# access Specification\n\n## Purpose\n\nИзолированный tooling store.\n\n## Requirements\n\n" + gate.effective_spec(workspace.store, SPEC_PATH, CHANGE)
    calls = []
    def partial(command, **kwargs):
        calls.append(command)
        (workspace.store / SPEC_PATH).write_text(merged_spec)
        return SimpleNamespace(returncode=1, stdout="delta merged before failure", stderr="Ошибка до перемещения change")
    with pytest.raises(gate.GateError):
        gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "partial-merge", execute=partial)
    assert workspace.active.is_dir()
    def finish(command, **kwargs):
        calls.append(command)
        return fake_archive(workspace)(command, **kwargs)
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "partial-merge", execute=finish)
    assert value["state"] == "complete"
    assert len(calls) == 2
    assert workspace.report_path.read_bytes() == report_before
    assert not workspace.active.exists()
    commit(workspace.store)
    assert gate.validate_archived(workspace.store, base)["archives_checked"] == 1


@pytest.mark.parametrize("mutation,description", [
    pytest.param("missing", "Без docs-review.json новый archive не должен вызывать CLI.", id="missing-docs-review"),
    pytest.param("docs", "Правка docs после review должна остановить archive до записи evidence.", id="stale-docs"),
    pytest.param("change", "Правка design после review должна потребовать нового review всей документации.", id="stale-change"),
])
def test_docs_review_blocks_archive_before_any_mutation(workspace, mutation, description):
    """Делает review непригодным согласно описанию параметра и ожидает отказ без вызова OpenSpec и изменения активного change; защищает docs lifecycle."""
    assert description
    if mutation == "missing":
        (workspace.active / "docs-review.json").unlink()
    elif mutation == "docs":
        page = workspace.store / "docs/api.md"
        page.write_text(page.read_text() + "\nНовый API контракт.\n")
    else:
        (workspace.active / "design.md").write_text("Изменённый дизайн после review.\n")
    before = active_snapshot(workspace)
    calls = []
    with pytest.raises(gate.GateError):
        gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "docs-not-ready",
                     execute=lambda *args, **kwargs: calls.append(args))
    assert calls == []
    assert active_snapshot(workspace) == before
    assert not (workspace.store / ".archive-operations/docs-not-ready.json").exists()


def test_ci_rejects_new_archive_without_docs_review(workspace):
    """Удаляет docs-review и его hash из нового archive при полном regression evidence; CI обязан отказать и закрыть обход прямым OpenSpec CLI."""
    base = git(workspace.store, "rev-parse", "HEAD")
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "missing-docs-ci", execute=fake_archive(workspace))
    destination = Path(value["archive_path"])
    (destination / "docs-review.json").unlink()
    evidence_path = destination / "regression-evidence.json"
    evidence = gate.read_json(evidence_path)
    del evidence["docs_review_sha256"]
    gate.atomic_json(evidence_path, evidence)
    commit(workspace.store)
    with pytest.raises(gate.GateError, match="без docs-review"):
        gate.validate_archived(workspace.store, base)


def test_ci_rejects_deleting_previous_docs_evidence(workspace):
    """В уже принятом archive удаляет docs-review и hash одновременно; CI видит прежнее evidence в base и запрещает ослабление завершённого gate."""
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "deleted-docs-ci", execute=fake_archive(workspace))
    base = commit(workspace.store)
    destination = Path(value["archive_path"])
    (destination / "docs-review.json").unlink()
    evidence_path = destination / "regression-evidence.json"
    evidence = gate.read_json(evidence_path)
    del evidence["docs_review_sha256"]
    gate.atomic_json(evidence_path, evidence)
    commit(workspace.store)
    with pytest.raises(gate.GateError, match="без docs-review"):
        gate.validate_archived(workspace.store, base)


def test_later_docs_updates_do_not_invalidate_historical_archive(workspace):
    """После успешного archive меняет docs и проверяет CI с историческим base без новых archives; прежние hashes остаются историческими и не требуют переписывать архив."""
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "historical-docs", execute=fake_archive(workspace))
    base = commit(workspace.store)
    archived = Path(value["archive_path"]) / "docs-review.json"
    before = archived.read_bytes()
    page = workspace.store / "docs/api.md"
    page.write_text(page.read_text() + "\nКонтракт последующего change.\n")
    commit(workspace.store)
    assert gate.validate_archived(workspace.store, base)["archives_checked"] == 0
    assert archived.read_bytes() == before


def test_existing_legacy_archive_does_not_require_retroactive_docs_review(workspace):
    """Моделирует archive прежней версии без docs evidence в base, затем меняет только его tasks; CI сохраняет прежний regression gate без навязывания нового review задним числом."""
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "legacy-docs", execute=fake_archive(workspace))
    destination = Path(value["archive_path"])
    (destination / "docs-review.json").unlink()
    (destination / "docs-snapshot.json").unlink()
    path = destination / "regression-evidence.json"
    evidence = gate.read_json(path)
    del evidence["docs_review_sha256"]
    del evidence["docs_snapshot_sha256"]
    gate.atomic_json(path, evidence)
    base = commit(workspace.store)
    tasks = destination / "tasks.md"
    tasks.write_text(tasks.read_text() + "\nИсторическое пояснение завершённой задачи.\n")
    commit(workspace.store)
    assert gate.validate_archived(workspace.store, base)["archives_checked"] == 1


def test_ci_accepts_two_sequential_archives_with_distinct_docs_snapshots(workspace):
    """Архивирует A, затем обновляет docs и архивирует B, проверяя общий base до обоих; CI должен принять оба immutable snapshots при текущем docs B."""
    base = git(workspace.store, "rev-parse", "HEAD")
    first = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "batch-a", execute=fake_archive(workspace))
    first_root = Path(first["archive_path"])
    second_baseline = commit(workspace.store)
    second_change = "demo-change-b"
    second_root = workspace.store / "openspec/changes" / second_change
    second_root.mkdir()
    for filename in (".openspec.yaml", "proposal.md", "design.md", "tasks.md"):
        (second_root / filename).write_bytes((first_root / filename).read_bytes())
    page = workspace.store / "docs/api.md"
    page.write_text(page.read_text() + "\nНовый API для второго change в batch.\n")
    commit(workspace.store)
    review = gate.docs.prepare_review(workspace.store, second_change, second_baseline)
    for relative, section in review["sections"].items():
        section.update(status="updated" if relative in review["changed_pages"] else "reviewed",
                       reason="API обновлён по второму change; остальные разделы сверены с текущим продуктом.")
    gate.atomic_json(second_root / "docs-review.json", review)
    workspace.report = json.loads(json.dumps(workspace.report))
    workspace.report["selection"]["change"] = second_change
    workspace.report["run_id"] = "batch-b-fixture-run"
    workspace.report["manifest"]["store"]["commit"] = git(workspace.store, "rev-parse", "HEAD")
    workspace.report_path = workspace.report_path.parent.parent / "batch-b-reports/results.json"
    workspace.report_path.parent.mkdir()
    workspace.save_report()

    def archive_second(command, **kwargs):
        assert command[:3] == ["openspec", "archive", second_change]
        operation = gate.read_json(workspace.store / ".archive-operations/batch-b.json")
        shutil.move(second_root, operation["archive_path"])
        return SimpleNamespace(returncode=0, stdout="fixture second archive", stderr="")

    second = gate.archive(workspace.store, workspace.tests, second_change, workspace.report_path, "batch-b", execute=archive_second)
    commit(workspace.store)
    assert gate.validate_archived(workspace.store, base)["archives_checked"] == 2
    assert gate.read_json(first_root / "docs-review.json")["docs_sha256"] != review["docs_sha256"]
    assert Path(second["archive_path"]).is_dir()


def test_ci_rejects_stale_docs_after_single_new_archive(workspace):
    """После единственного нового archive меняет docs без нового review; CI относительно исходного base должен отказать, даже если сохранённый snapshot структурно корректен."""
    base = git(workspace.store, "rev-parse", "HEAD")
    gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "single-stale-docs", execute=fake_archive(workspace))
    page = workspace.store / "docs/api.md"
    page.write_text(page.read_text() + "\nНовая неподтверждённая версия API после archive.\n")
    commit(workspace.store)
    with pytest.raises(gate.GateError, match="не соответствует ни одному"):
        gate.validate_archived(workspace.store, base)


@pytest.mark.parametrize("mutation,description", [
    pytest.param("review", "Новые hashes в прежнем review даже с согласованным regression hash не должны переписывать историю.", id="rewrite-review-hashes"),
    pytest.param("snapshot", "Самосогласованная подмена content, page hash, review и regression evidence должна блокироваться по base.", id="rewrite-content-and-all-hashes"),
])
def test_ci_rejects_self_consistent_rewrite_of_historical_docs_evidence(workspace, mutation, description):
    """Подделывает прежние docs evidence согласно описанию параметра и пересчитывает связанные hashes; ожидается отказ CI по неизменяемости исторического snapshot относительно base."""
    assert description
    value = gate.archive(workspace.store, workspace.tests, CHANGE, workspace.report_path, "immutable-docs", execute=fake_archive(workspace))
    root = Path(value["archive_path"])
    base = commit(workspace.store)
    review_path = root / "docs-review.json"
    review = gate.read_json(review_path)
    if mutation == "review":
        review["docs_sha256"]["docs/api.md"] = "f" * 64
    else:
        snapshot_path = root / "docs-snapshot.json"
        snapshot = gate.read_json(snapshot_path)
        entry = snapshot["files"]["docs/api.md"]
        entry["content"] += "\nПодменённый исторический контракт API.\n"
        entry["sha256"] = gate.digest(entry["content"].encode())
        review["docs_sha256"]["docs/api.md"] = entry["sha256"]
        gate.atomic_json(snapshot_path, snapshot)
        review["snapshot_sha256"] = gate.digest(snapshot_path.read_bytes())
    gate.atomic_json(review_path, review)
    evidence_path = root / "regression-evidence.json"
    evidence = gate.read_json(evidence_path)
    evidence["docs_review_sha256"] = gate.digest(review_path.read_bytes())
    evidence["docs_snapshot_sha256"] = gate.digest((root / "docs-snapshot.json").read_bytes())
    gate.atomic_json(evidence_path, evidence)
    commit(workspace.store)
    with pytest.raises(gate.GateError, match="неизменяем"):
        gate.validate_archived(workspace.store, base)
