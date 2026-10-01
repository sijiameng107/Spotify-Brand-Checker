# Evaluation Documentation

## Reproduce the reported results without API calls

From the repository root, using Python 3.10 or later:

```bash
python verify_results.py
```

This recomputes scores from archived attempts, checks the experiment identity and frozen prompt, confirms input/reference alignment, reruns the deterministic baseline and lexical retrieval, and checks that request item fields contain only Content and Context. It is an offline consistency check, not an independent validation of reference labels or evidence quality.

Expected summary: all rules 40/50 with 7/22 false passes; retrieved rules 47/50 with 1/22 false passes; baseline 16/50; mean retrieval recall@2 83%. Verification does not overwrite original results.

## Evaluation implementation

`checker.py` contains `baseline`, `retrieve`, `evaluate`, `summarize_mode` and `run_comparison`. The notebook adds `category_metrics` for difficulty-group reporting. `notebooks/Spotify_Formal_Test.ipynb` embeds the frozen implementation and test data. Cell 2 evaluates the baseline and retrieval; cell 4 runs and scores both model variants; cell 5 exports artifacts. The data, code and archived outputs are included in the repository rather than only summarized in the report.

For a fresh paid comparison, follow the notebook instructions in the root README. Frozen settings: `openai/gpt-4o-mini`, temperature 0, maximum 800 output tokens, lexical top two versus all four rules, prompt version `v2_schema_bounded_retry`, at most two attempts per case and mode. Fifty cases across two modes require 100 initial requests; validation retries can raise this to at most 200. Account/configuration failures stop further requests. The archived experiment had exactly 100 first attempts and no errors or retries.

## Metric definitions

| Metric | Definition and denominator |
|---|---|
| Decision agreement | Valid final decisions equal to reference labels divided by all 50 scheduled cases; errors and unattempted cases do not count as correct. |
| False passes | Cases labeled Flag but predicted Pass, divided by 22 reference violations. A violation abstention is separate from a false pass. |
| Violations flagged | Reference Flag cases predicted Flag, divided by 22. |
| Abstention rate | Final Insufficient evidence predictions divided by 50; also inspect the confusion matrix and difficulty categories. |
| Selective accuracy | Correct non-abstaining valid decisions divided by non-abstaining valid decisions; report coverage alongside it. |
| Retrieval recall@2 | For each case, intersection of retrieved and reference rule IDs divided by reference rule count; average over 50 cases. This is evidence retrieval, not classification accuracy. |
| Run errors and completion | Track invalid/error final outputs and not-run cases separately; completing all attempts does not mean all decisions are correct. |
| API cost per item | Sum known charges across all attempts for a mode divided by 50; report missing-cost count. Costs exclude development and operations. |
| Latency | Mean elapsed seconds per API attempt, not human time saved. |
| Evidence support | Separate qualitative assessment of whether the explanation and supplied evidence justify the decision. No automated semantic guarantee is claimed. |

The 90% agreement target corresponds to at least 45/50 correct. Other diagnostic metrics have no retrospectively invented numerical targets. The majority-class comparator is 22/50 (44%).

## Where to inspect evidence

- `results/development/`: frozen v2 development attempts, summaries, baseline and retrieval records. These are the final v2 development artifacts, not a complete archive of every earlier debugging attempt.
- `results/formal/baseline_formal.csv`, `baseline_summary.json`, `baseline_by_category.csv`: deterministic results.
- `results/formal/retrieval_formal.csv`: per-case rule IDs and recall.
- `results/formal/13c744bb98422507/experiment.json`: model, prompt and data snapshot.
- `attempts.jsonl` and `all_attempts.csv` in that folder: all 100 responses with cost, tokens and validation metadata.
- `all_rules_final.csv`, `retrieved_rules_final.csv`, `summary.json`, `summary.csv` and `by_category.csv`: final decisions, metrics and difficulty breakdown.
- `docs/Evidence_Review_Completed.xlsx`: completed review for 100 model outputs; definitions and counts appear in `docs/Evidence_Review_Method.md`.
- Original `evidence_review.csv`: blank review template produced by the run, preserved separately from the completed workbook.

## Failure interpretation

T27, T36 and T48 are retrieval-mode decision errors despite retrieval of relevant rules. T42 shows incomplete reasoning despite a correct decision. All rules achieved 12/12 in development versus retrieval 11/12, but the ranking reversed in the formal set. Repeated patterns, limited rule coverage and student reference judgments constrain conclusions. Do not tune on this formal set and then describe a new run on it as unseen validation.
