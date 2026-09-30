# Spotify Guideline Checker

PE6201 End-of-Course Project — Meng Sijia

A scoped text checker for Spotify partner-integration links and registered third-party app names/descriptions. It returns **Pass**, **Flag**, or **Insufficient evidence** with available rule evidence. It supports a reviewer; it does not grant Spotify approval or assess every brand requirement.

## Recorded results

| Method | Correct | Violations passed | Abstentions | Formal API cost (USD) |
|---|---:|---:|---:|---:|
| Deterministic baseline | 16/50 | 0/22 | 40/50 | 0 |
| All rules | 40/50 | 7/22 | 8/50 | 0.0068721 |
| Retrieved rules | 47/50 | 1/22 | 6/50 | 0.0077445 |

Both model variants completed 50 cases without retries or run errors. Model: `openai/gpt-4o-mini` through OpenRouter. Mean lexical retrieval recall@2 was 83%. Retrieved rules performed better on decisions in this run, but incomplete explanations and a false pass remain. The report explains these limitations and the reversal of the development-set ranking.

## Run without an API key

Use Python 3.10 or later from this repository folder. No package installation is required.

```bash
python verify_results.py
python demo.py --case T01
python demo.py --case T21
python demo.py --case T45
python demo.py --case T36
```

The demo explicitly displays **saved formal results**, not a new inference. These examples show Pass, Flag, Insufficient evidence and a false pass, respectively. Verification recalculates metrics from saved logs without network access.

## Make a new live demonstration

```bash
python demo.py --case T01 --live
```

The key is requested through a hidden prompt, or read from `OPENROUTER_API_KEY`. A live demonstration makes one paid request, with at most one retry for an invalid structured response. New logs go to ignored `local_runs/`. Keep them separate from the reported experiment. Never paste a key into a notebook, source file or screenshot. A fresh result may differ from the recorded result.

## Re-run the formal comparison in Colab

Upload `notebooks/Spotify_Formal_Test.ipynb` to Colab and run its five code cells in order. Rules and all 50 cases are embedded; no CSV upload is required. Cells 1–2 run locally. Cell 3 takes a hidden key. Cell 4 makes 100 initial paid requests and permits at most one validation retry per case/mode. Cell 5 downloads the results ZIP. Account/configuration errors can stop a run. Re-running in the same runtime resumes saved records; a fresh runtime does not retain them.

This creates a new evaluation. Do not overwrite the archived experiment with a better-looking run. The checked-in notebook has no saved execution outputs; the complete recorded outputs are supplied under `results/formal/`.

## Repository contents

- `checker.py`: evaluated v2 inference, lexical retrieval, validation, bounded retry and scoring logic, extracted from the formal notebook.
- `notebooks/Spotify_Formal_Test.ipynb`: self-contained evaluation notebook with the same code cells as the submitted formal notebook.
- `data/`: frozen rule records, separate formal inputs/reference labels, and development cases.
- `results/formal/`: original formal-result files, including all 100 attempts, experiment settings and summaries.
- `results/development/`: development summaries, attempts and available baseline/retrieval outputs.
- `docs/Project_Report.md`: trade-off report, under 1,200 words.
- `docs/Evidence_Review_Completed.xlsx`: returned review workbook recording Meng Sijia as reviewer for all 100 outputs.
- `docs/Evidence_Review_Method.md`: criteria and support counts.
- `docs/Demo_Script.md`: suggested recording sequence and narration.
- `docs/Course_Coverage.md`: connection between the project and course topics.

The blank `results/formal/13c744bb98422507/evidence_review.csv` is the original run artifact. The completed review is the workbook in `docs/`; the original is preserved for traceability.

## Method and limitations

Each of the four rules is a retrieval chunk. The retrieval variant uses lexical TF-IDF cosine scores and supplies up to two rules. The all-rules variant supplies all four. The model receives only Content and Context from each case; reference labels, reviewer annotations and relevant-rule IDs are used locally for scoring. Temperature is zero, output limit is 800 tokens, and the structured schema requires supporting rule IDs for Pass/Flag and a missing-information explanation for abstention.

The formal set contains 20 clear compliant, 20 clear non-compliant and 10 borderline cases, with 22 Pass, 22 Flag and six Insufficient evidence references. Case count does not establish broad coverage or statistical independence. Decision agreement is separate from evidence support. The review is student-confirmed, not independent external validation. No human review-time saving is claimed.

The recorded code and prompts are frozen. This packaging step changes documentation and adds replay/verification entry points; it does not fix formal-test errors or claim a new score. Provider availability and current charges may differ when re-running.

Rule source: [Spotify Design Guidelines](https://developer.spotify.com/documentation/design). Rule records distinguish the original excerpt from project paraphrases. Operational applicability and authorization handling are evaluated against the frozen project policy.
