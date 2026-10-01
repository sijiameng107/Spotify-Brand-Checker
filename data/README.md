# Data Documentation

## Scope and source

The project uses four frozen rule records derived from [Spotify Design Guidelines](https://developer.spotify.com/documentation/design). `brand_rules.csv` preserves the source URL and separates requirement text, interpretation and applicability. R01 contains a source excerpt; R02–R04 are explicitly marked paraphrases. Their operational violation and uncertainty criteria are project interpretations, not claims that Spotify supplied the evaluation labels.

Cases are project-specific test examples, not a sample of deployed advertising campaigns. The checker accepts text regardless of how it was authored; the evaluation does not establish performance across all AI-generated advertising. The rule corpus is not refreshed at runtime.

## Files and schemas

| File | Size | Purpose and fields |
|---|---|---|
| `brand_rules.csv` | 4 rules R01–R04 | `Rule_ID`, `Rule_Name`, `Official_Requirement`, `Interpretation`, `Applicable_Context`, `Source_URL`, `Violation_Criteria`, `Insufficient_Evidence_Criteria` |
| `development_cases.csv` | 12 cases D01–D12 | `Case_ID`, `Content`, `Context`, `Category`, `Expected_Decision`, `Relevant_Rule_IDs`, `Label_Rationale`. Category values are blank in the original development CSV; do not infer formal categories from them. |
| `test_inputs.csv` | 50 cases T01–T50 | `Case_ID`, `Content`, `Context`; inference inputs are Content and Context only. |
| `test_reference_labels.csv` | 50 corresponding rows | `Case_ID`, `Category`, `Expected_Decision`, `Relevant_Rule_IDs`, `Label_Rationale`, `Review_Status`, `Reviewer`; local scoring and annotation data. |

CSV encoding is UTF-8; the loader also accepts a UTF-8 BOM. Multiple reference rule IDs are separated by semicolons. Join inputs and labels by `Case_ID`; checked-in row order also matches the frozen experiment, as verified by `verify_results.py`.

## Splits and labeling

The development split contains four Pass, four Flag and four Insufficient evidence references. It was used to inspect failure handling and output format. The formal composition was fixed before labeling: 20 clear compliant, 20 clear non-compliant and 10 borderline. Final reference decisions are 22 Pass, 22 Flag and six Insufficient evidence. Borderline is a difficulty category, not synonymous with abstention.

The formal label file records verification by Meng Sijia before inference. T41 and T42 use the reviewed R04 annotations. These frozen labels were not changed to fit formal predictions. The experiment snapshot in `results/formal/13c744bb98422507/experiment.json` includes the rules and all joined reference cases; the labels remain local and do not enter model requests.

## Interpretation and limitations

A Flag requires a supported violation in the applicable context. A Pass means the supplied applicable checks pass. Unknown installation status, unclear field boundaries or unverified claimed permission can justify Insufficient evidence. Permission handling is evaluated against the frozen project interpretation.

This small corpus contains related wording patterns and covers only four requirements. Student review is not independent external validation. Do not treat 50 cases as statistically independent coverage of Spotify's full policy. Keep these inputs and labels unchanged when reproducing the reported evaluation; new design changes require a separately identified evaluation set.
