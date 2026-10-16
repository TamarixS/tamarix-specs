"""Одноразовый runner: сохраняет русский и JSON отчёт даже при ошибке/отмене."""
import ast
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
import uuid

import pytest
import yaml

root = Path.cwd()
run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8]
output = Path('/tmp') / ('tamarix-docs-gate-' + run_id)
output.mkdir()
requested = sys.argv[1:] or ['tests/test_docs_check.py', 'tests/test_archive_gate.py']
arguments = ['-q', *requested, '--junitxml=' + str(output / 'junit.xml')]
started = time.monotonic()
run_report = dict(schema_version=1, run_id=run_id, command=[sys.executable, '-m', 'pytest', *arguments],
              requested=requested, executed_node_ids=[], collected_node_ids=[], cases=[], errors=[], complete=False,
              status='RUNNING', started_at=datetime.now(timezone.utc).isoformat(), finished_at=None,
              manifest={'python': platform.python_version(), 'pytest': pytest.__version__, 'PyYAML': yaml.__version__,
                        'store_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                        'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [
                            Path('tools/archive_gate.py'), Path('tools/docs_check.py'),
                            Path('tests/test_archive_gate.py'), Path('tests/test_docs_check.py')]}},
              artifacts={'log': str(output / 'pytest.log'), 'junit': str(output / 'junit.xml')})


def save():
    run_report['duration_seconds'] = time.monotonic() - started
    run_report['counts'] = {status: sum(c['status'] == status for c in run_report['cases']) for status in ('PASS', 'FAIL', 'ERROR', 'SKIP', 'XFAIL', 'XPASS', 'NOT_RUN')}
    run_report['counts']['total'] = len(run_report['cases'])
    (output / 'results.json').write_text(json.dumps(run_report, ensure_ascii=False, indent=2) + '\n')
    lines = ['# Отчёт проверки docs и archive gate', '', f"Прогон: `{run_id}`. Итог: **{run_report['status']}**.", '',
             'Запрошенный набор: ' + ', '.join(requested) + '.',
             f"Собрано: {len(run_report['collected_node_ids'])}; начато: {len(run_report['executed_node_ids'])}.",
             f"Длительность: {run_report['duration_seconds']:.3f} с. Счётчики: {run_report['counts']}.", '',
             'Проверяются детерминированные tooling gates в одноразовых репозиториях; приложение и предметные e2e не запускаются.', '',
             '| Случай | Русское описание | Статус |', '| --- | --- | --- |']
    lines += [f"| `{c['node_id']}` | {c['description'].replace(chr(10), ' ')} | {c['status']} |" for c in run_report['cases']]
    lines += ['', 'Ошибки: ' + ('; '.join(run_report['errors']) or 'нет') + '.', '', f"Подробности: `{output / 'results.json'}`, `{output / 'pytest.log'}`."]
    (output / 'summary.md').write_text('\n'.join(lines) + '\n')


class Plugin:
    def pytest_collection_modifyitems(self, items):
        run_report['collected_node_ids'] = [i.nodeid for i in items]
        for i in items:
            description = getattr(i.obj, '__doc__', '') or ''
            if hasattr(i, 'callspec') and 'description' in i.callspec.params:
                description += '\nСлучай: ' + i.callspec.params['description']
            run_report['cases'].append(dict(test_id=i.nodeid, node_id=i.nodeid, description=description.strip(), status='NOT_RUN', duration_seconds=0, error=None, artifacts=[]))
        save()

    def pytest_runtest_logstart(self, nodeid, location):
        run_report['executed_node_ids'].append(nodeid)
        save()

    def pytest_runtest_logreport(self, report):
        case = next(c for c in run_report['cases'] if c['node_id'] == report.nodeid)
        case['duration_seconds'] += report.duration
        if report.failed:
            case['status'] = 'FAIL' if report.when == 'call' else 'ERROR'
            case['error'] = str(report.longrepr)
        elif report.skipped:
            case['status'] = 'XFAIL' if hasattr(report, 'wasxfail') else 'SKIP'
        elif report.when == 'call' and case['status'] == 'NOT_RUN':
            case['status'] = 'XPASS' if hasattr(report, 'wasxfail') else 'PASS'
        save()

    def pytest_collectreport(self, report):
        if report.failed:
            run_report['errors'].append(str(report.longrepr))
            save()

save()
try:
    with (output / 'pytest.log').open('w') as log, redirect_stdout(log), redirect_stderr(log):
        result = int(pytest.main(arguments, plugins=[Plugin()]))
    run_report['status'] = 'PASS' if result == 0 and run_report['cases'] and all(c['status'] == 'PASS' for c in run_report['cases']) else 'FAIL'
    run_report['complete'] = result != 2
except BaseException as exc:
    result = 2
    run_report['status'] = 'CANCELLED' if isinstance(exc, KeyboardInterrupt) else 'ERROR'
    run_report['errors'].append(traceback.format_exc())
finally:
    run_report['finished_at'] = datetime.now(timezone.utc).isoformat()
    save()
print(json.dumps({'status': run_report['status'], 'counts': run_report['counts'], 'report_directory': str(output)}, ensure_ascii=False))
if result:
    print((output / 'pytest.log').read_text()[-16000:])
sys.exit(result)
