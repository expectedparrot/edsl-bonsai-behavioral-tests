# Bonsai 2 27B: behavioral-bias tests

Completed 84 local responses across 11 test families and 21 conditions, four
responses per condition. All 84 have distinct completion IDs, validated answers,
and normal completion markers. One answer-channel formatting anomaly is described
below. The automatically started server was shut down after the run.

The most interesting result was a contrast within the conjunction tests: the
model answered the familiar Linda question correctly 4/4 times, but committed
the conjunction fallacy 3/4 times in a new astronomy vignette. This is consistent
with limited transfer from a familiar example, but does not establish that the
model memorized Linda or identify the cause of the difference.

## Observed responses

| Test | What Bonsai returned | Interpretation for these prompts |
|---|---|---|
| Conjunction: Linda | “Linda is a bank teller.” — 4/4 | No conjunction error on the canonical item. |
| Conjunction: new vignette | “Morgan works as an accountant and belongs to an astronomy club.” — 3/4; accountant alone — 1/4 | Conjunction error in 3/4 responses, spanning both option orders. |
| Base rates | 7.48% at 1% prevalence; 84.21% at 40% prevalence — each 4/4 | All eight Bayes-rule calculations correct. |
| Gambler’s fallacy | Heads and tails equally likely — 4/4 after a streak, 4/4 after a mixed sequence | No fallacy observed in the explicitly independent-coin task. |
| Framing | Guaranteed recovery of 300 files — 4/4 in both saved/lost frames | No preference shift; consistently preferred the certain outcome. |
| Anchoring | Mean estimate 42.92 hours with anchor 10; 42.77 with anchor 100 | No meaningful shift toward the anchor; differences are rounding-sized. |
| Sunk cost | Stop the unprofitable project — 4/4 after $0 spent, 4/4 after $8,000 spent | Ignored irrecoverable past expenditure when future payoffs were identical. |
| Logical falsification | Turn over E and 7 — 4/4 | Correct on the Wason-style card task; not a comprehensive confirmation-bias assessment. |
| Default choice | Plan B: 2/4 with A preselected; 1/4 with B preselected | Mixed choices; observed difference runs opposite to default-following. Too few draws for a stable estimate. |
| Present bias | Later $60 rather than earlier $50 — 4/4 in both immediate and year-delayed versions | No shift toward the immediate payment. |
| Decoy | Digital-and-print bundle — 4/4 with the decoy, 4/4 without | No shift, but baseline bundle preference is already at the ceiling. |
| Intuitive arithmetic | Pen: $0.40 — 4/4; cake: 6 kg — 4/4 | All eight arithmetic answers correct; neither intuitive lure was selected. |

The novel conjunction response included this explanation:

> His astronomy interests make the additional club membership more likely.

That does not justify assigning a conjunction a higher probability than its
component. The “accountant and astronomy-club member” event is contained in the
“accountant” event, regardless of the biographical evidence.

Across the 44 responses with explicit correct-answer keys, 41 matched the key;
all three errors were in the new conjunction vignette. This is a descriptive
count for this deliberately chosen battery, not an overall model bias rate.

## Method and limits

One local model, temperature 1.0 and top-p 0.95, with an 8192-token context,
2048-token response limit, and a 512-token server-side reasoning budget. The
short reasoning budget may affect errors, so these results do not characterize
unrestricted model reasoning. Each prompt was an independent one-question EDSL
interview, with an empty system prompt and no persona traits. The question
requested an explanation in at most two sentences; EDSL added output-format
instructions. Bias names and answer keys were not shown to the model.

There are four draws per condition. Multiple-choice options were presented in
forward and reverse order, twice each; this is not full position balancing for
three- or four-option tasks. Numerical questions used four separate iterations.
An empty cache and distinct iteration keys were used for every test family.
The prompts are exploratory adaptations rather than a validated human study.
Canonical examples can be familiar from training, and several controls explicitly
state the relevant assumptions. No significance claims or human prevalence
estimates are made. Preference questions do not have a single correct answer.

One default-condition response leaked reasoning into the answer channel. EDSL
parsed Plan A, and the final text after the closing thinking tag was also Plan A;
the answer was retained and flagged, while the contaminated explanation was not
treated as a normal final explanation. One payment-timing explanation incorrectly
referred to a “10-day” interval when the prompt specified 30 days. Thus valid
answer formatting does not establish explanation quality.

## Reproduce or inspect

- [Every prompt, answer, and final explanation](all_responses.md)
- [Responses as CSV](responses.csv) and [JSON](responses.json)
- [Machine-readable counts and audit](summary.json)
- [Conditions and scoring keys](conditions.json)
- [EDSL Python runner](../behavioral_biases.py)
- [Methodology and research references](../BEHAVIORAL_TESTS.md)

The per-family `.jobs.ep` and `.results.ep` packages preserve the execution
specifications, rendered prompts, raw completions, and EDSL validation data.
