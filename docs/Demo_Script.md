# Suggested Recorded Demonstration

Suggested length: about 3–4 minutes, subject to the final course brief. This sequence uses saved formal results and identifies them as such. A live demonstration is optional and must be labelled separately.

## 1. Purpose and scope

Show the README introduction.

“My project checks four selected Spotify text requirements for partner-integration links and third-party app naming and descriptions. It returns Pass, Flag or Insufficient evidence. It supports review rather than granting final brand approval.”

## 2. Architecture

Show data/brand_rules.csv and the report design section.

“I compared a deterministic baseline, a model receiving all four rules, and the same model receiving up to two rules selected by lexical TF-IDF retrieval. I used GPT-4o-mini through OpenRouter. Reference labels are used for scoring and are excluded from the model input. This fixed workflow does not need an autonomous agent.”

## 3. Three output types

Run `python demo.py --case T01`, then T21 and T45, or open the corresponding rows in the saved result CSV if recording without a terminal.

“These are saved outputs from the frozen formal test, not new calls. T01 passes because the installed-app link label matches R01. T21 is flagged because the label is outside the permitted options. T45 lacks installation status, so the system requests more information rather than guessing.”

## 4. Evaluation and a failure

Run `python verify_results.py` and `python demo.py --case T36`.

“The formal set has 50 cases, including 10 borderline cases. Retrieved rules matched 47 references, while all rules matched 40. Both completed without runtime errors. However, T36 was incorrectly passed: the text claims joint development while the context denies that relationship. This is why a high overall score does not justify unattended approval.”

Show the completed review workbook and T42.

“I also checked explanation support. A correct decision can still have incomplete evidence: T42 checks the name but misses the endorsement issue. I therefore report decision accuracy separately from explanation quality.”

## 5. Trade-off and conclusion

Show the report economics section.

“The retrieved-rules run cost about 0.000155 US dollars per item in recorded API charges. This excludes human review and operating costs. I do not claim measured review-time savings. The next improvement would be better handling of contradictory claims and complete rule coverage, evaluated on new cases.”

Before recording, open the selected files, hide credentials and rehearse navigation. Keep the original formal results unchanged. Save the recording separately and submit its file or link according to the course instructions.
