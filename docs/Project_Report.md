# Spotify Guideline Checker: Business and Technical Trade-offs

## Problem and scope

Reviewers need to check whether AI-generated advertising copy follows brand requirements and identify which wording needs revision. This project addresses that broader need through a scoped Spotify case study. This project tests a narrow decision-support tool for Spotify partner-integration link labels and registered third-party application names and descriptions. It returns Pass, Flag or Insufficient evidence, accompanied by a reason and available rule evidence. It does not assess general brand tone, visual design or every Spotify policy. Passing this checker is not approval by Spotify.

The intended user is a reviewer checking draft copy before publication. A false pass is the costlier error because non-compliant wording could proceed unchecked. The tool therefore supports review rather than replacing final human approval. No review-time saving is claimed: model latency does not measure how much time a person saves.

## Design and build-versus-buy decision

The prototype uses a Python notebook and rents model inference through OpenRouter with openai/gpt-4o-mini. Building the application logic allows explicit rule handling, logging and evaluation without training or hosting a model. Renting inference reduces implementation effort but introduces provider dependence, variable charges and external processing of submitted text.

Four frozen rules cover installed-app link wording, installation-link wording, distinct application names and implied endorsement. The rule records include source URLs, applicability and criteria for violations or insufficient evidence. Most requirements are operational paraphrases; source wording and project interpretation must remain distinguishable.

Three approaches were compared: a deterministic baseline, a model receiving all four rules, and a model receiving the top two rules selected by lexical TF-IDF retrieval. This is a small retrieval-augmented pipeline, not an embedding search system. Content and Context enter inference; reference decisions and reference rule IDs are reserved for scoring. Temperature is zero, the output limit is 800 tokens, and a structured schema constrains the response format. Validation permits one retry for an invalid response and preserves attempts and costs. Valid structure does not guarantee a correct judgment.

An autonomous agent was unnecessary. The workflow has a fixed sequence and does not require planning, browsing or taking action in external systems. Additional autonomy would introduce complexity without serving the scoped task.

## Evaluation design

The development set contained 12 cases. The frozen formal set contained 50: 20 clear compliant, 20 clear non-compliant and 10 borderline cases. Borderline denotes difficulty, not a required abstention. Reference decisions totalled 22 Pass, 22 Flag and six Insufficient evidence. The submitted workbook recorded student verification before the formal run.

Both model variants used the same frozen v2 settings. Each completed 50 cases on its first attempt, with no run errors or missing API cost records. Results were retained without tuning the checker against the formal set. Accuracy measures agreement with these references; the limited four-rule coverage and repeated case patterns restrict generalization.

## Results

| Measure | Deterministic baseline | All rules | Retrieved rules |
|---|---:|---:|---:|
| Correct decisions | 16/50 | 40/50 | 47/50 |
| Violations incorrectly passed | 0/22 | 7/22 | 1/22 |
| Violations flagged | 7/22 | 15/22 | 20/22 |
| Abstentions | 40/50 | 8/50 | 6/50 |
| Recorded API cost, USD | 0 | 0.0068721 | 0.0077445 |

Retrieved rules reached 47/50 (94%), exceeding the 90% target in this run. It performed better on clear cases, while both model variants achieved 9/10 on borderline cases. Its six abstentions included one unnecessary abstention and only five of the six intended abstentions. The baseline's zero false passes came with 40 abstentions and only 16 correct decisions, below the 22/50 majority-class baseline.

Development had favored all rules, at 12/12 versus 11/12. The reversed formal ordering demonstrates the weakness of drawing conclusions from a small development set. Favoring retrieval after this comparison is a post-evaluation recommendation, not a choice validated on a further unseen set.

## Failures and evidence quality

Retrieved T27 ignored an explicitly stated installation status and abstained. T36 approved a claim of joint development despite context denying that relationship. T48 treated missing proof of claimed special permission as grounds to flag rather than request verification. All three had their relevant rules retrieved, indicating interpretation failures rather than retrieval omissions.

Mean per-case retrieval recall at two was 83%. Correct decisions sometimes lacked complete support: T42 passed, but the retrieved response checked only the name and omitted the endorsement issue. The evidence review, checked by Meng Sijia, rated all-rules explanations as 33 supported, seven partially supported and ten unsupported; retrieval received 28, 19 and three respectively. This diagnostic review is not independent external validation. It shows why label accuracy should be reported separately from explanation completeness.

## Economics and deployment judgment

Recorded API cost per content item was USD 0.000137442 for all rules and USD 0.000154890 for retrieval. Total formal-run cost was USD 0.0146166. These figures exclude development, hosting, maintenance and human review. Retrieval was more expensive in this run despite supplying fewer rules; the available records do not establish the cause. Mean request times were approximately 1.69 and 1.38 seconds, respectively.

The prototype demonstrates inexpensive, traceable decision support within a narrow scope. It is not ready for unattended approval because a costly false pass remains and evidence coverage is incomplete. Operational use should preserve final human review, minimize sensitive input, protect API credentials, and track guideline changes. Future work should test better separation of submitted claims from contextual facts and more complete rule coverage on a new evaluation set. These improvements have not been implemented or validated in the reported run.

The project's practical contribution is to connect potentially non-compliant wording with explicit brand requirements and surface uncertainty for review. Within the four-rule scope, this provides a structured first-pass check for AI-generated copy and supports informed revision before publication.

Source basis: Spotify Design Guidelines, https://developer.spotify.com/documentation/design; frozen four-rule project corpus; formal experiment 13c744bb98422507; completed evidence-review records.
