"""Offline verification of the frozen formal experiment.

Checks prompt/data identity, recomputes final decisions and all-attempt costs,
reruns baseline/retrieval, and checks the request-item field boundary. Assertions
signal inconsistencies; this does not independently establish label correctness.
Inputs are repository archives; output is a console summary, with no network calls.
"""
import csv
import json
from pathlib import Path
import checker

ROOT = Path(__file__).resolve().parent


def verify():
    folder = ROOT / 'results/formal/13c744bb98422507'
    experiment = json.loads((folder / 'experiment.json').read_text())
    cases, rules = experiment['cases'], experiment['rules']
    attempts = [json.loads(line) for line in (folder / 'attempts.jsonl').read_text().splitlines() if line.strip()]
    assert checker.experiment_id(rules, cases, experiment['model']) == experiment['experiment_id']
    assert checker.SYSTEM == experiment['system_prompt']
    inputs = checker.read_csv(ROOT / 'data/test_inputs.csv')
    labels = checker.read_csv(ROOT / 'data/test_reference_labels.csv')
    assert len(inputs) == len(labels) == len(cases) == 50
    assert [dict(item, **label) for item, label in zip(inputs, labels)] == cases
    expected = json.loads((folder / 'summary.json').read_text())
    for saved in expected:
        summary, final = checker.summarize_mode(attempts, cases, saved['mode'])
        for key in ['correct', 'cases', 'confusion_counts', 'total_attempts', 'failed_attempts',
                    'violations_passed', 'violations_flagged', 'abstentions', 'attempts_missing_cost']:
            assert summary[key] == saved[key], (saved['mode'], key)
        assert abs(summary['known_cost_all_attempts_usd'] - saved['known_cost_all_attempts_usd']) < 1e-10
        assert len(final) == 50 and summary['all_outputs_valid']
        print(f"{saved['mode']}: {summary['correct']}/50; false passes {summary['violations_passed']}/22")
    baseline = [{'case_id':c['Case_ID'], 'status':'ok', 'cost_usd':0.0, **checker.baseline(c,rules)} for c in cases]
    assert checker.evaluate(baseline,cases)['correct'] == 16
    recalls = []
    for c in cases:
        found = {r['Rule_ID'] for r in checker.retrieve(c,rules,2)}
        wanted = {r.strip() for r in c['Relevant_Rule_IDs'].split(';')}
        recalls.append(len(found & wanted) / len(wanted))
    assert abs(sum(recalls)/50 - .83) < 1e-10
    # Reference annotations never appear in the request item.
    payload = checker.make_payload(cases[0], rules, experiment['model'])
    assert set(json.loads(payload['messages'][-1]['content'])['item']) == {'Content','Context'}
    print('Baseline: 16/50; mean retrieval recall@2: 83%. Saved results verified; no API calls made.')


if __name__ == '__main__':
    verify()
