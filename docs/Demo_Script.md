# Demonstration Voiceover

Target duration: approximately 2 minutes 30 seconds. Sequence: Colab execution, saved formal results, comparison, failure analysis, and economics. Only the free cells are run during the demonstration.

Hello, I’m Meng Sijia. My project addresses the difficulty of checking whether AI-generated advertising copy follows brand guidelines, using Spotify as a focused case study. The prototype checks four rules for integration link wording and application names and descriptions, returning Pass, Flag, or Insufficient evidence.

Here in Colab, I load the checker and fifty reviewed test cases. To address the uncertainty of small samples, I separated twelve development cases from fifty formal cases: twenty clear compliant, twenty clear non-compliant, and ten borderline examples.

Next, I run the free baseline and retrieval evaluation. Reference labels are used only for scoring. The model outputs shown afterward are saved formal results.

The all-rules model achieved 40 out of 50 correct decisions, while retrieved rules achieved 47 out of 50. Incorrectly approved violations decreased from seven to one.

All rules performed better during development. This reversal showed me that a small development set cannot reliably establish which approach will generalize better.

Correct decisions also need reliable explanations. In T36, the model approved a joint-development claim despite contradictory context. The relevant rule was retrieved but interpreted incorrectly. I therefore assessed evidence support separately from decision accuracy.

Recorded API cost per item was approximately 0.014 US cents for all rules and 0.015 US cents for retrieval, excluding development and human review. Timing myself on familiar cases would be biased, so I make no review-time-saving claim. A fixed workflow was sufficient; an autonomous agent was unnecessary.

Overall, this project helps reviewers check AI-generated copy by identifying potential violations, presenting relevant rules, and highlighting missing information. Within its tested scope, it provides a practical first-pass review that supports informed revisions before publication.
