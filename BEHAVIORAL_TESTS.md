# Behavioral-bias battery

Run the local battery with:

```bash
uv run python behavioral_biases.py
uv run python summarize_biases.py
```

It starts and manages the Bonsai server using `bonsai_server.bonsai_server`, or reuses
a ready server. The single-question example is `ask_linda.py`. New runs default to `runs/local/`.
The completed family packages are reused on restart. For an independent rerun,
choose a new directory with `--output PATH`. `--build-only` constructs and validates
the inputs without inference; `--export-only` exports saved results.

## Design

- 11 families, 21 conditions, four answers per condition: 84 interviews.
- Each interview is one independent question; no earlier answers are included.
- Multiple-choice conditions use both forward and reversed option order, with
  two EDSL iterations of each. Numerical conditions use four iterations.
- Forward/reverse ordering is not full positional counterbalancing for questions
  with more than two alternatives.
- Every family gets an empty in-memory EDSL cache. Iteration is part of the cache
  key. Completion IDs are audited to detect reused responses; `fresh=True` alone
  is not relied upon to control local caching.
- Temperature 1.0, top-p 0.95, 2048 output tokens. The launcher uses one slot,
  an 8192-token context, top-k 20, and a 512-token reasoning budget. Actual output
  lengths and finish reasons are inspected rather than assuming the budget works.
- Responses include a brief explanation. There is no bias label or answer key
  in the rendered question. EDSL's default agent instructions apply.
- Conditions and keys are saved before execution in `conditions.json`; complete
  Jobs specifications are stored in `.jobs.ep` packages.

## Interpretation

Conjunction, Bayes-rule, independent-coin, sunk-cost, logical-card, and arithmetic
items have specified correct answers. The cost problem explicitly excludes
nonfinancial benefits and consequences. The card item probes falsification;
an incorrect answer does not by itself establish a general confirmation bias.

Framing, default, anchoring, intertemporal, and decoy tests compare matched
conditions. A preference alone is not an error. For present bias, a larger share
choosing the earlier payment in the immediate condition is the relevant pattern;
these independent model samples do not establish within-person reversals.
Anchoring uses an explicitly random number with the same factual information in
both conditions, so it is a relatively transparent probe.

Four draws per condition are exploratory, not a precise prevalence estimate or a
significance test. They are repeated samples of one model under one configuration,
not different people or independent models. Canonical tasks may be familiar from
training. The Linda item and a novel conjunction vignette are both included;
most other scenarios are adaptations, not validated replications of the original
experiments. These results do not measure how closely the model resembles humans.

## Research background

The battery is inspired by these research traditions; not every prompt reproduces
an original instrument:

- Tversky and Kahneman (1974), [Judgment under Uncertainty: Heuristics and Biases](https://pubmed.ncbi.nlm.nih.gov/17835457/).
- Tversky and Kahneman (1981), [The Framing of Decisions and the Psychology of Choice](https://stanford.edu/class/psych205/papers/Tversky-Kahneman-1981.pdf).
- Huber, Payne, and Puto (1982), [Adding Asymmetrically Dominated Alternatives](https://doi.org/10.1086/208899).
- Frederick, Loewenstein, and O'Donoghue (2002), [Time Discounting and Time Preference](https://www.aeaweb.org/articles?id=10.1257%2F002205102320161311).

## Files

`behavioral_bias_run/` contains the original inputs, per-family Results packages,
protocol, and exported `responses.json` and `responses.csv`. The initial interrupted setup pilot is excluded from the analysis and is not distributed here. Original scripts matching the recorded hashes are in `original_scripts/`.

The completed run is described in [the report](behavioral_bias_run/report.md),
with [every prompt and response](behavioral_bias_run/all_responses.md).
