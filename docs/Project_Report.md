# Evaluating a Spotify Brand Guideline Checker

Meng Sijia | PE6201 End of Course Project

## Purpose and practical contribution

AI-generated advertising copy can sound convincing while conflicting with brand requirements. A reviewer needs to identify problematic wording and explain the requirement behind a revision. I investigated this need through a scoped Spotify checker for integration link labels and third-party application names and descriptions. It returns Pass, Flag or Insufficient evidence, with an explanation and available rule evidence.

The intended user is a marketing or partner-integration reviewer checking copy before publication. Compared with an unstructured manual check, the prototype organizes draft text, contextual facts and rule evidence into an inspectable decision. It does not cover general advertising compliance, visual identity or brand tone. Passing its four checks is not Spotify approval. Its contribution is a practical first-pass review, rather than a measured replacement for human judgment.

## Architecture and design choices

I built the application logic in Python and rented GPT-4o-mini inference through OpenRouter. This avoided training and hosting a model while retaining control over prompts, evidence selection and evaluation. The trade-off is dependence on an external provider, including its availability, charges and processing of submitted text.

Four frozen rules address installed-app link wording, installation-link wording, distinct application names and implied endorsement. Each rule is a retrieval unit with applicability, violation criteria, uncertainty criteria and a source URL. The records distinguish quoted wording from project paraphrases of Spotify's design guidance. This matters because operational interpretation can influence what the evaluation treats as correct.

I compared a deterministic baseline, a model receiving all four rules, and the same model receiving up to two rules selected by lexical TF-IDF similarity. Retrieval tests whether focused evidence helps; with only four rules, it is not justified by a large-document requirement. Content and context enter inference; labels remain local to scoring. An autonomous agent was unnecessary because the task follows a fixed retrieval, classification and validation sequence.

## Difficulties and implementation decisions

An early development problem was structurally invalid output. For D10, the model returned Pass and mentioned R03 and R04 in its explanation, but left the rule ID list empty. The original run stopped, making an apparently sensible answer unusable downstream. D12 also encountered validation failures. These were distinct from incorrect substantive judgments.

I addressed this with an explicit output contract, a structured JSON schema, local validation and at most one corrective retry for validation errors. Pass and Flag require supplied rule IDs; abstention requires a missing-information explanation. Attempts and costs are retained, and case-specific failures no longer halt the remaining evaluation. Account and configuration errors still stop repeated unusable requests. The lesson was to make failure handling predictable rather than repeatedly patch individual examples.

The frozen v2 development run completed without errors: all rules achieved 12/12 and retrieval 11/12. This supports the usability of the revised execution path, but does not isolate which change caused improvement. I froze the prompt, temperature, output limit and retry policy before formal testing. I did not modify the classifier to repair formal-test mistakes.

## Evaluation design and its limits

A twenty-case evaluation would move by five percentage points after one error. I used twelve development cases and fifty separate formal cases, fixing the formal composition before labeling: twenty clear compliant, twenty clear non-compliant and ten borderline examples. Reference decisions were 22 Pass, 22 Flag and six Insufficient evidence. Borderline describes difficulty, not a requirement to abstain.

I reviewed the reference labels before testing and assessed agreement, false passes, abstentions, retrieval recall, output validity and cost. I treated false passes as costlier because prohibited wording could proceed unchecked. I dropped the proposed 30% review-time-saving claim: timing myself on familiar labeled cases would be biased, and model latency cannot establish human time saved.

Fifty cases improve resolution but do not establish broad coverage. Repeated wording patterns, four rules and one student's judgments limit independence and generalizability. This is a controlled evaluation of a narrow task, not evidence of effectiveness across real advertising campaigns. The completed evidence review is student-confirmed rather than independent external validation.

## Results and interpretation

| Measure | Baseline | All rules | Retrieved rules |
|---|---:|---:|---:|
| Correct decisions | 16/50 | 40/50 | 47/50 |
| Violations incorrectly passed | 0/22 | 7/22 | 1/22 |
| Violations flagged | 7/22 | 15/22 | 20/22 |
| Abstentions | 40/50 | 8/50 | 6/50 |
| API cost in USD | 0 | 0.0068721 | 0.0077445 |

Retrieval reached 47/50, or 94%, exceeding the 90% accuracy target in this run; all rules reached 80%. Both variants completed fifty first attempts without run errors or retries. The baseline's zero false passes came with forty abstentions and only sixteen correct decisions, below the 22/50 majority-class baseline. Avoiding false approval alone therefore does not establish usefulness.

Development had favored all rules, but formal testing reversed that ranking. This changed my confidence in choosing an architecture from a small development set. Preferring retrieval is a post-evaluation recommendation, requiring another unseen evaluation. Both variants achieved 9/10 on borderline cases. Retrieval's six abstentions included one unnecessary abstention and missed one intended abstention, demonstrating why matching the overall abstention count is insufficient.

## Failure analysis and evidence quality

Retrieved T27 ignored explicit installation status and abstained. T36 approved a joint-development claim despite context denying that relationship. T48 treated unverified special permission as a violation rather than requesting evidence. All three had the relevant rules retrieved: these were interpretation failures, not retrieval omissions.

Mean retrieval recall at two was 83%. Correct decisions could still have incomplete explanations: T42 passed while its response assessed the name but omitted the endorsement question. Evidence review rated all-rules explanations as 33 supported, seven partially supported and ten unsupported; retrieval received 28, nineteen and three. Retrieval improved decision agreement without producing more fully supported explanations. I therefore separate label accuracy, retrieval coverage and evidence support rather than reporting one success rate.

## Economics and future direction

Recorded API cost per item was USD 0.000137442 for all rules and USD 0.000154890 for retrieval. Total formal cost was USD 0.0146166. These exclude development, hosting, maintenance and human review. Retrieval cost slightly more despite supplying fewer rules; the experiment does not establish why. Low inference cost alone is insufficient to justify deployment.

The remaining false pass requires final human approval. A next iteration should separate submitted claims more clearly from contextual facts, require assessment of every applicable issue, and test changes on a new evaluation set. These improvements remain proposals. A blinded reviewer study would be needed before claiming time savings.

Within its tested scope, the project makes brand review more inspectable by connecting potential violations to explicit requirements and identifying missing information. This helps reviewers make informed revisions before publication while retaining responsibility for the final decision.

Source: Spotify Design Guidelines, https://developer.spotify.com/documentation/design. Evidence: frozen experiment 13c744bb98422507, development summaries and completed evidence-review workbook in this repository.
