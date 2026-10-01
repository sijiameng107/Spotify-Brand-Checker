# Code and Module Guide

| Component | Responsibility | Inputs and outputs | External effects |
|---|---|---|---|
| `checker.py` | Frozen classification and evaluation core | Case dictionaries and rules to decisions, evidence and scores | `api_attempt` calls OpenRouter and appends JSONL; comparison writes experiment artifacts |
| `demo.py` | Command-line case inspection or explicit new inference | Case ID and mode to input, reference and response display | Offline by default; `--live` uses hidden key and writes `local_runs/` |
| `verify_results.py` | Recompute and validate archived metrics | Repository data and experiment logs to assertions and console summary | No network or paid calls; no artifact replacement |
| `notebooks/Spotify_Formal_Test.ipynb` | Self-contained formal evaluation | Embedded rules and cases, optional key to baseline, retrieval and model results | Paid calls only in the model comparison cell; exports ZIP |

## Core function groups

- Data and evidence: `read_csv`, `load_data`, `evidence_for`, `save_csv`. `load_data` is the legacy development-data helper, not the formal input loader.
- Deterministic and retrieval paths: `baseline` uses narrow phrase checks; `retrieve` ranks rule records by TF-IDF cosine similarity and returns up to two positive-scoring rules.
- Model request and validation: `make_payload` includes only Content and Context as item fields; `validate_output` enforces the response contract and attaches supplied evidence; `api_attempt` logs one request and its outcome.
- Experiment control: `experiment_id` fingerprints rules, cases and settings; `run_comparison` resumes matching saved attempts, applies bounded validation retries, and stops on fatal configuration errors.
- Evaluation: `evaluate` scores one final row per case; `summarize_mode` accounts for all attempts and missing cases; the notebook-local the notebook-local `category_metrics` groups outcomes by case category.

`SYSTEM` is initialized with the original instructions and extended with the v2 output contract before any public execution path runs; the effective version is `v2_schema_bounded_retry`. The initial `v1` assignment is not the effective formal configuration. Keeping this construction preserves the evaluated prompt exactly.

Validation ensures structural correctness, not truth. No rule IDs are inferred from free-text explanations to repair a response. Nonretryable errors remain visible, and runtime data does not authorize changes to the classifier. Documentation revisions do not change the evaluated prompt or decision logic.
