"""Run the certificates and compare every output with the supplied baseline."""
import argparse
import csv
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def main():
    if not __debug__:
        raise SystemExit('Run without -O: certificate assertions must be enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--with-independent', action='store_true',
                        help='also run the SymPy Sturm-and-trace verification')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    jobs = [
        ('verify_q1.py', ['verification_report.json', 'candidate_audit.csv']),
        ('verify_constructions.py', ['construction_report.json']),
    ]
    versions = {'python': platform.python_version()}
    if args.with_independent:
        try:
            import sympy
        except ImportError:
            raise SystemExit('Install the optional dependency: '
                             'python -m pip install -r requirements.txt')
        versions['sympy'] = sympy.__version__
        jobs.append(('verify_independent_sympy.py', ['independent_report.json']))
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONIOENCODING'] = 'utf-8'
    checked = []
    for program, outputs in jobs:
        result = subprocess.run([sys.executable, '-B', str(base / program)],
                                cwd=base, env=env, capture_output=True,
                                text=True, encoding='utf-8')
        if result.returncode:
            raise SystemExit('{} failed:\n{}\n{}'.format(
                program, result.stdout, result.stderr))
        for name in outputs:
            actual = base / name
            expected = base / 'expected' / name
            if name.endswith('.json'):
                matches = (json.loads(actual.read_text(encoding='utf-8')) ==
                           json.loads(expected.read_text(encoding='utf-8')))
            else:
                with actual.open(newline='', encoding='utf-8') as a:
                    with expected.open(newline='', encoding='utf-8') as e:
                        matches = list(csv.reader(a)) == list(csv.reader(e))
            if not matches:
                raise SystemExit('Output differs from expected/' + name)
            checked.append(name)
        print(program + ': PASS (all expected outputs matched)')
    report = json.loads((base / 'verification_report.json').read_text())
    summary = {
        'status': 'passed',
        'versions': versions,
        'programs': [program for program, outputs in jobs],
        'matched_expected_outputs': checked,
        'main_counts': report['main_certificate']['counts'],
        'survivors': [[r['k'], r['mu'], r['c'], r['n']]
                      for r in report['main_certificate']['survivors']],
        'focused_run_role': 'optional consistency check, not needed for the theorem',
    }
    (base / 'run_summary.json').write_text(
        json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print('Verified survivors:', summary['survivors'])


if __name__ == '__main__':
    main()
