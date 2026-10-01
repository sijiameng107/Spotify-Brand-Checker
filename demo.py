"""Inspect one archived case or explicitly request a new paid inference.

Reads the frozen experiment and selected case, prints input/reference/result, and
uses checker.api_attempt only when --live is supplied. Keys use a hidden prompt
or environment variable. New attempts go to ignored local_runs, never the archive.
"""
import argparse
import getpass
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import checker

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', default='T01', help='Formal case ID, e.g. T01, T21, T45 or T36')
    parser.add_argument('--mode', choices=['all_rules','retrieved_rules'], default='retrieved_rules')
    parser.add_argument('--live', action='store_true', help='Make a new paid API call (at most one validation retry)')
    args = parser.parse_args()
    folder = ROOT / 'results/formal/13c744bb98422507'
    experiment = json.loads((folder/'experiment.json').read_text())
    case = next((c for c in experiment['cases'] if c['Case_ID']==args.case),None)
    if case is None:
        parser.error('Unknown case ID; choose T01 through T50.')
    if args.live:
        key = os.environ.get('OPENROUTER_API_KEY') or getpass.getpass('OpenRouter API key (hidden): ')
        if not key.strip():
            parser.error('No API key entered.')
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        log = ROOT / 'local_runs' / stamp / 'attempts.jsonl'
        row = checker.api_attempt(case,experiment['rules'],experiment['model'],key,args.mode,log,1)
        if row.get('retryable') and not row.get('fatal'):
            row = checker.api_attempt(case,experiment['rules'],experiment['model'],key,args.mode,log,2,row.get('error'))
        label = 'NEW LIVE INFERENCE — separate from reported formal results'
    else:
        rows = [json.loads(s) for s in (folder/'attempts.jsonl').read_text().splitlines() if s.strip()]
        row = next(r for r in reversed(rows) if r['case_id']==args.case and r['mode']==args.mode)
        label = 'SAVED FORMAL RESULT — replay, no new model call'
    print(label)
    print(json.dumps({'case_id':case['Case_ID'],'content':case['Content'],'context':case['Context'],
                      'reference_decision':case['Expected_Decision'],'result':row},indent=2))


if __name__ == '__main__':
    main()
