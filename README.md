# Spotify Guideline Checker

PE6201 End-of-Course Project — Meng Sijia

This project addresses the difficulty of checking AI-generated advertising copy against brand requirements through a focused Spotify case study. It checks four requirements for partner-integration labels and third-party application names/descriptions, returning **Pass**, **Flag** or **Insufficient evidence** with available rule evidence. It supports informed revision before publication; it does not grant Spotify approval or assess every advertising requirement.

## Start here

- [Product overview](docs/Product_Overview.md): persona, input, output, architecture diagram, target and achieved metrics.
- [Project report](docs/Project_Report.md) and [Word report](docs/Project_Report.docx): reasoning, difficulties, evaluation critique and practical contribution.
- [Data documentation](data/README.md): sources, schemas, split and annotation policy.
- [Evaluation documentation](evals/README.md): metric definitions, evaluation code, artifacts and limitations.
- [Code map](docs/Code_Map.md): file and function-group responsibilities.

## Formal results

| Method | Correct | Violations passed | Abstentions | API cost in USD |
|---|---:|---:|---:|---:|
| Deterministic baseline | 16/50 | 0/22 | 40/50 | 0 |
| All rules | 40/50 | 7/22 | 8/50 | 0.0068721 |
| Retrieved rules | 47/50 | 1/22 | 6/50 | 0.0077445 |

The agreement target was at least 90% (45/50). Retrieval exceeded it in this run. Both model variants completed 50 valid first attempts without errors or retries using `openai/gpt-4o-mini` through OpenRouter. Mean lexical recall@2 was 83%. A false pass and incomplete explanations remain. No measured human time saving is claimed.

## Install and verify locally

Use Python 3.10 or later and Git. All Python scripts use the standard library; no pip installation is required.

```bash
git clone https://github.com/sijiameng107/Spotify-Brand-Checker.git
cd Spotify-Brand-Checker
python3 verify_results.py
```

On Windows, use `python` if `python3` is unavailable. Expected output includes all rules 40/50, retrieved rules 47/50, baseline 16/50 and retrieval recall@2 83%. This recomputes archived results without API access or overwriting files.

Inspect specific archived cases:

```bash
python3 demo.py --case T01
python3 demo.py --case T21
python3 demo.py --case T45
python3 demo.py --case T36
```

The CLI explicitly labels these as saved formal results. They illustrate Pass, Flag, Insufficient evidence and a false pass. It displays input, context, reference decision and the archived response. Inspect the explanation and evidence, not only the label.

## Request a new model inference

An OpenRouter account with available credit and a compatible model/provider is required:

```bash
python3 demo.py --case T01 --mode retrieved_rules --live
```

Enter the API key at the hidden prompt, or configure `OPENROUTER_API_KEY` in your local environment. Do not put it in tracked files. The request may incur charges and allows at most one validation retry. New logs are stored under ignored `local_runs/`. They are separate from the reported experiment; fresh responses and charges may differ. The default command makes no new model call.

## Run a fresh formal evaluation in Colab

Open `notebooks/Spotify_Formal_Test.ipynb` in Google Colab. It embeds the rules and 50 reviewed cases; additional CSV upload is unnecessary. Run its five code cells in order:

1. Load frozen checker and data; no API call.
2. Compute baseline, per-category metrics and retrieval recall locally.
3. Enter the hidden API key and initialize model settings; no paid call.
4. Run both model variants: 100 initial requests, at most 200 with validation retries. Account/configuration errors stop further unusable calls.
5. Download the results ZIP, including attempt logs and summaries.

Re-running in the same runtime resumes matching saved records; resetting it loses those records. Keep a fresh evaluation in a separate archive. Do not replace the submitted experiment with a more favorable run or tune against it while describing it as unseen.

## Repository layout

- `checker.py`: inference, retrieval, validation, experiment control and scoring.
- `demo.py`: archived case inspection and optional new inference.
- `verify_results.py`: offline archive consistency check.
- `notebooks/`: self-contained formal evaluation runner.
- `data/`: frozen rules, development cases and separate formal inputs/reference labels.
- `evals/`: evaluation explanation with links to executable implementations.
- `results/development/`: final v2 development artifacts.
- `results/formal/`: baseline, retrieval and all 100 model attempts, settings and summaries.
- `docs/`: report, product architecture, code map, course connections and completed evidence review.
- `PACKAGE_SHA256.json`: SHA-256 file manifest excluding itself.

## Interpretation and reproducibility

The formal set contains 20 clear compliant, 20 clear non-compliant and 10 borderline cases; its labels are 22 Pass, 22 Flag and six Insufficient evidence. Labels remain local to scoring. Student review is not independent validation, and repeated patterns constrain generalization. The blank evidence-review CSV in the original experiment is retained for traceability; the completed review is `docs/Evidence_Review_Completed.xlsx`.

The evaluated prompt and classifier remain frozen. File-level documentation explains the modules without changing decision logic. OpenRouter errors should be inspected by status: authentication, credit or provider configuration issues cannot be fixed by repeated requests. Missing cost is not zero cost. Runtime validation verifies structure and supplied IDs, not semantic correctness.

Rule source: [Spotify Design Guidelines](https://developer.spotify.com/documentation/design). The local records distinguish quotations from paraphrases and define the frozen project interpretation.
