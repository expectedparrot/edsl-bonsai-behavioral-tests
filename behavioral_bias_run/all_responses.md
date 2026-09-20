# Bonsai behavioral-bias battery: observed responses

84/84 responses saved. 84 validated; 84 unique completion IDs.

Four samples per condition from one model, temperature 1.0, with a 512-token reasoning budget. These are descriptive results, not significance tests or estimates of human behavior.

| Test | Condition | Responses | Correct |
|---|---|---|---|
| conjunction | linda | Linda is a bank teller.: 4/4 | 4/4 |
| conjunction | new_vignette | Morgan works as an accountant.: 1/4; Morgan works as an accountant and belongs to an astronomy club.: 3/4 | 1/4 |
| base_rate | rare | 7.48: 4/4 | 4/4 |
| base_rate | common | 84.21: 4/4 | 4/4 |
| gambler | streak | Heads and tails are equally likely: 4/4 | 4/4 |
| gambler | mixed | Heads and tails are equally likely: 4/4 | 4/4 |
| framing | saved | Plan A: 4/4 | Preference/estimate |
| framing | lost | Plan A: 4/4 | Preference/estimate |
| anchoring | low | 43: 3/4; 42.67: 1/4 | Preference/estimate |
| anchoring | high | 42.67: 1/4; 42.7: 2/4; 43: 1/4 | Preference/estimate |
| sunk_cost | none | Stop the project: 4/4 | 4/4 |
| sunk_cost | large | Stop the project: 4/4 | 4/4 |
| confirmation | card_test | E and 7: 4/4 | 4/4 |
| default | a_default | Plan A: 2/4; Plan B: 2/4 | Preference/estimate |
| default | b_default | Plan A: 3/4; Plan B: 1/4 | Preference/estimate |
| present_bias | now | The later $60 payment: 4/4 | Preference/estimate |
| present_bias | later | The later $60 payment: 4/4 | Preference/estimate |
| decoy | without_decoy | Digital and print subscription: $120: 4/4 | Preference/estimate |
| decoy | with_decoy | Digital and print subscription: $120: 4/4 | Preference/estimate |
| intuitive_arithmetic | notebook_pen | 0.4: 4/4 | 4/4 |
| intuitive_arithmetic | cake | 6: 4/4 | 4/4 |

## Exact prompts and responses

The following includes every answer and its final explanation. Internal reasoning is preserved in the Results packages.

### conjunction: linda

Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice, and also participated in anti-nuclear demonstrations. Which is more probable?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Linda is a bank teller. / Linda is a bank teller and is active in the feminist movement.

- **Linda is a bank teller.** — The single statement is more probable because adding “active in the feminist movement” makes a narrower, less likely conjunction. (order: forward; iteration: 0)
- **Linda is a bank teller.** — The more specific second option combines two traits, so its probability is lower than the single-trait option. (order: forward; iteration: 1)
- **Linda is a bank teller.** — The conjunction “bank teller and active in the feminist movement” cannot be more probable than “bank teller,” because it is a subset of the first category. (order: reverse; iteration: 0)
- **Linda is a bank teller.** — A less specific hypothesis is always at least as probable as a more specific conjunction. (order: reverse; iteration: 1)

### conjunction: new_vignette

Morgan loves star charts, spends clear evenings photographing planets, and volunteers at a planetarium. Which is more probable?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Morgan works as an accountant. / Morgan works as an accountant and belongs to an astronomy club.

- **Morgan works as an accountant.** — The second option is more probable because it is a less specific claim than asserting both being an accountant and belonging to an astronomy club. (order: reverse; iteration: 0)
- **Morgan works as an accountant and belongs to an astronomy club.** — His astronomy interests make the additional club membership more likely. (order: reverse; iteration: 1)
- **Morgan works as an accountant and belongs to an astronomy club.** — The astronomy-related evidence makes the additional club membership more probable. (order: forward; iteration: 0)
- **Morgan works as an accountant and belongs to an astronomy club.** — The evidence about star charts, planetary photography, and planetarium volunteering strongly supports belonging to an astronomy club. (order: forward; iteration: 1)

### base_rate: rare

A factory produces parts, of which 1% are defective. A scanner flags 80% of defective parts and also flags 10% of non-defective parts. A part is randomly selected and is flagged. What is the probability that it is defective? Give a percentage from 0 to 100, rounded to two decimal places.

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

- **7.48** — # Using Bayes’ rule: (0.01 × 0.80) / [(0.01 × 0.80) + (0.99 × 0.10)] ≈ 0.074766, or 7.48%. (order: forward; iteration: 0)
- **7.48** — P(defective and flagged)=0.008 and P(flagged)=0.107, so P(defective|flagged)=0.008/0.107≈7.48%. (order: forward; iteration: 1)
- **7.48** — # Bayesian update: (0.01·0.80)/(0.01·0.80 + 0.99·0.10) = 0.074766..., which is 7.48%. (order: forward; iteration: 2)
- **7.48** — # Using Bayes' rule: (0.01 × 0.80) / [(0.01 × 0.80) + (0.99 × 0.10)] = 7.48%. (order: forward; iteration: 3)

### base_rate: common

A factory produces parts, of which 40% are defective. A scanner flags 80% of defective parts and also flags 10% of non-defective parts. A part is randomly selected and is flagged. What is the probability that it is defective? Give a percentage from 0 to 100, rounded to two decimal places.

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

- **84.21** — P(defective | flagged) = (0.8×0.4) / (0.8×0.4 + 0.1×0.6) = 0.8421, which is 84.21%. (order: forward; iteration: 0)
- **84.21** — Bayes' rule gives 0.8 × 0.4 / (0.8 × 0.4 + 0.1 × 0.6) = 84.21%. (order: forward; iteration: 1)
- **84.21** — Bayes’ theorem: P(defective|flagged) = (0.40×0.80)/(0.40×0.80+0.60×0.10) = 0.32/0.38 ≈ 0.8421. As a percentage, this is 84.21%. (order: forward; iteration: 2)
- **84.21** — # Using Bayes’ theorem, P(defective | flagged) = (0.4 × 0.8) / (0.4 × 0.8 + 0.6 × 0.1) = 0.32 / 0.38 ≈ 84.21%. (order: forward; iteration: 3)

### gambler: streak

A fair coin has been flipped six times, producing heads, heads, heads, heads, heads, heads. Each flip is independent. On the next flip, which outcome is more likely?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Heads / Tails / Heads and tails are equally likely

- **Heads and tails are equally likely** — Each independent fair coin flip has a 50/50 chance of heads or tails. (order: forward; iteration: 0)
- **Heads and tails are equally likely** — The previous flips do not affect the independent next flip, so it remains 50/50. (order: forward; iteration: 1)
- **Heads and tails are equally likely** — Each flip is independent and fair, so the probability of heads or tails remains 1/2 regardless of previous results. (order: reverse; iteration: 0)
- **Heads and tails are equally likely** — The coin is fair and each flip is independent, so the previous six heads do not affect the next flip. (order: reverse; iteration: 1)

### gambler: mixed

A fair coin has been flipped six times, producing heads, tails, tails, heads, tails, heads. Each flip is independent. On the next flip, which outcome is more likely?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Heads / Tails / Heads and tails are equally likely

- **Heads and tails are equally likely** — Each flip of a fair coin is independent, so previous outcomes do not affect the next flip. (order: reverse; iteration: 0)
- **Heads and tails are equally likely** — Since each fair coin flip is independent, the previous six flips do not affect the next flip. (order: reverse; iteration: 1)
- **Heads and tails are equally likely** — Each flip is independent, so the prior sequence does not affect the probability of the next flip. (order: forward; iteration: 0)
- **Heads and tails are equally likely** — The coin is fair and each flip is independent, so previous results do not change the odds for the next flip. (order: forward; iteration: 1)

### framing: saved

A damaged archive contains 900 files. Choose a recovery plan. Plan A will save exactly 300 files. Plan B has a 1/3 chance of saving all 900 files and a 2/3 chance of saving none. Every file is equally valuable; these are the complete outcomes. Which plan do you choose?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Plan A / Plan B

- **Plan A** — I choose Plan A because it guarantees 300 recovered files, matching Plan B's expected value while avoiding the risk of losing all files. (order: forward; iteration: 0)
- **Plan A** — Plan A guarantees 300 files saved, while Plan B only has the same expected value with a 2/3 chance of saving none. (order: forward; iteration: 1)
- **Plan A** — Choose A because it guarantees 300 files, while B has the same expected value but a high chance of saving none. (order: reverse; iteration: 0)
- **Plan A** — Plan A guarantees 300 files, and since Plan B has the same expected value but a risk of saving none, the safer choice is A. (order: reverse; iteration: 1)

### framing: lost

A damaged archive contains 900 files. Choose a recovery plan. Plan A will lose exactly 600 files. Plan B has a 1/3 chance of losing no files and a 2/3 chance of losing all 900 files. Every file is equally valuable; these are the complete outcomes. Which plan do you choose?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Plan A / Plan B

- **Plan A** — No final explanation supplied. (order: reverse; iteration: 0)
- **Plan A** — It guarantees recovering 300 files, whereas Plan B has the same expected value but risks losing all 900. (order: reverse; iteration: 1)
- **Plan A** — Both plans have an expected loss of 600 files, but Plan A avoids the high-variance all-loss risk. (order: forward; iteration: 0)
- **Plan A** — Both plans have the same expected number of recovered files (300), but Plan A guarantees recovery while Plan B has a 2/3 chance of losing everything. (order: forward; iteration: 1)

### anchoring: low

You are estimating the engineering hours for a new module. Three comparable modules required 38, 44, and 46 hours. The new module is similar in scope and staffing. Before you estimate, an unrelated random-number generator displays 10. Consider whether the new module will take more or less than 10 hours. What is your best estimate of its total engineering hours? Return a number of hours.

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

- **43** — The unrelated 10 should not anchor the estimate; comparable similar modules average about 42.67 hours. (order: forward; iteration: 0)
- **42.67** — # The unrelated 10 is irrelevant, and the comparable modules average about 42.7 hours, so a similar module should be estimated near that value. (order: forward; iteration: 1)
- **43** — # Best estimate is the average of the three comparable modules (38, 44, and 46), which is 42.67, rounded to 43 hours; the random 10 is irrelevant. (order: forward; iteration: 2)
- **43** — # The comparable modules average to 42.7 hours, and the unrelated display of 10 does not change that best estimate. (order: forward; iteration: 3)

### anchoring: high

You are estimating the engineering hours for a new module. Three comparable modules required 38, 44, and 46 hours. The new module is similar in scope and staffing. Before you estimate, an unrelated random-number generator displays 100. Consider whether the new module will take more or less than 100 hours. What is your best estimate of its total engineering hours? Return a number of hours.

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

- **42.67** — The new module should be well under 100 hours because the comparable modules require 38–46 hours. I estimate the average of those values, 42.67 hours. (order: forward; iteration: 0)
- **42.7** — # Comparable modules average 42.67 hours, and the unrelated 100 is irrelevant. (order: forward; iteration: 1)
- **43** — # 43 is the rounded average of the three comparable modules, and the 100 is an irrelevant distractor. (order: forward; iteration: 2)
- **42.7** — # The comparable modules average about 42.7 hours, and the unrelated 100 is not a relevant basis for estimating this similar module. (order: forward; iteration: 3)

### sunk_cost: none

You manage a project and have already spent $0, which cannot be recovered. Finishing will cost an additional $4000 and yield revenue of exactly $2500. Stopping costs nothing and yields no further revenue. There are no reputation, learning, contractual, or other consequences. Your sole objective is to maximize final net money. What do you do?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Finish the project / Stop the project

- **Stop the project** — No final explanation supplied. (order: forward; iteration: 0)
- **Stop the project** — Stopping avoids an additional net loss of $1500. (order: forward; iteration: 1)
- **Stop the project** — Finishing would reduce your net money by $1500, so stopping maximizes final money. (order: reverse; iteration: 0)
- **Stop the project** — Finishing costs $4000 to produce $2500, a net loss of $1500; stopping preserves money since the $0 spent is unrecoverable either way. (order: reverse; iteration: 1)

### sunk_cost: large

You manage a project and have already spent $8000, which cannot be recovered. Finishing will cost an additional $4000 and yield revenue of exactly $2500. Stopping costs nothing and yields no further revenue. There are no reputation, learning, contractual, or other consequences. Your sole objective is to maximize final net money. What do you do?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Finish the project / Stop the project

- **Stop the project** — The sunk $8000 is unrecoverable, so stopping avoids an additional net loss of $1,500 from finishing. (order: reverse; iteration: 0)
- **Stop the project** — Sunk costs are unrecoverable, and finishing would reduce final money by $4,000. (order: reverse; iteration: 1)
- **Stop the project** — No final explanation supplied. (order: forward; iteration: 0)
- **Stop the project** — Finishing costs $4,000 for only $2,500 revenue, so stopping avoids a $1,500 net loss. (order: forward; iteration: 1)

### confirmation: card_test

Each card has a letter on one side and a number on the other. Four cards show E, K, 4, and 7. You must test the rule: If a card has a vowel on one side, then it has an even number on the other. Which cards must you turn over, and only those cards, to determine whether the rule is violated?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): E and 4 / E and 7 / E only / All four cards

- **E and 7** — No final explanation supplied. (order: reverse; iteration: 0)
- **E and 7** — Turn over E to check that its other side is even, and 7 to check that its other side is not a vowel; 4 is already even and K doesn’t need testing. (order: reverse; iteration: 1)
- **E and 7** — No final explanation supplied. (order: forward; iteration: 0)
- **E and 7** — E could violate the rule if its hidden side is odd, and 7 could violate it if its hidden side is a vowel. (order: forward; iteration: 1)

### default: a_default

Choose between two internet plans. Plan A costs $40 per month with 100 Mbps service. Plan B costs $50 per month with 200 Mbps service. All other terms are identical. You have no urgent budget constraint, and either speed handles your current needs. The form randomly preselects Plan A; this is not a recommendation. Choosing either plan takes the same effort and has no switching cost. Which do you choose?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Plan A / Plan B

- **Plan A** — Formatting anomaly: reasoning appeared in the answer channel. Final text after the closing thinking tag: Plan A. Raw response preserved in the Results package. (order: forward; iteration: 0)
- **Plan B** — Plan B provides double the speed for only a modest price increase, with no budget constraint and no switching cost. (order: forward; iteration: 1)
- **Plan B** — It provides more speed for a small cost increase, and there is no stated budget pressure. (order: reverse; iteration: 0)
- **Plan A** — It is cheaper, and both plans already meet your current needs. (order: reverse; iteration: 1)

### default: b_default

Choose between two internet plans. Plan A costs $40 per month with 100 Mbps service. Plan B costs $50 per month with 200 Mbps service. All other terms are identical. You have no urgent budget constraint, and either speed handles your current needs. The form randomly preselects Plan B; this is not a recommendation. Choosing either plan takes the same effort and has no switching cost. Which do you choose?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Plan A / Plan B

- **Plan A** — It costs less and still meets your needs. (order: reverse; iteration: 0)
- **Plan A** — It costs less and still meets your current needs. (order: reverse; iteration: 1)
- **Plan A** — Plan A is cheaper and provides the same usable service given your needs, so it minimizes cost without any downside. (order: forward; iteration: 0)
- **Plan B** — The higher speed costs only $10 more per month and provides more future flexibility, and I have no urgent budget constraint. (order: forward; iteration: 1)

### present_bias: now

Choose one guaranteed payment: $50 today, or $60 in 30 days. Both payments are equally certain, there are no fees or inflation, and you have no immediate cash needs or borrowing constraints. Which do you choose?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): The earlier $50 payment / The later $60 payment

- **The later $60 payment** — The guaranteed $60 is equivalent to a 20% return over 30 days, which I would accept given no immediate cash needs. (order: forward; iteration: 0)
- **The later $60 payment** — $60 in 30 days pays 20% more than $50 today, and with no costs or cash needs, the extra amount is worth it. (order: forward; iteration: 1)
- **The later $60 payment** — The later $60 payment offers $10 more for zero added risk, and you have no immediate cash need. (order: reverse; iteration: 0)
- **The later $60 payment** — It provides a higher guaranteed amount, and without costs, inflation, or immediate cash needs, delaying the smaller earlier payment is not penalized. (order: reverse; iteration: 1)

### present_bias: later

Choose one guaranteed payment: $50 in 365 days, or $60 in 395 days. Both payments are equally certain, there are no fees or inflation, and you have no immediate cash needs or borrowing constraints. Which do you choose?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): The earlier $50 payment / The later $60 payment

- **The later $60 payment** — The later $60 payment is worth more in nominal terms, and with certainty, no borrowing, no costs, and no cash need, the extra $10 outweighs the 30-day delay. (order: reverse; iteration: 0)
- **The later $60 payment** — No final explanation supplied. (order: reverse; iteration: 1)
- **The later $60 payment** — A 20% increase over a short extra 30 days is better than the 10-day earlier payment under standard positive interest rates. (order: forward; iteration: 0)
- **The later $60 payment** — No final explanation supplied. (order: forward; iteration: 1)

### decoy: without_decoy

Choose an annual magazine subscription for yourself. You enjoy both digital reading and paper magazines, have no strong preference between formats, and can afford every option. All options contain the same editorial content. Which subscription do you choose?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Digital subscription: $60 / Digital and print subscription: $120

- **Digital and print subscription: $120** — I choose it because it supports both my digital and paper reading preferences without any preference between formats and I can afford it. (order: forward; iteration: 0)
- **Digital and print subscription: $120** — It gives me access to both formats I enjoy, and I can comfortably afford the higher price. (order: forward; iteration: 1)
- **Digital and print subscription: $120** — It lets me read the same magazine both on paper and digitally, which fits my enjoyment of both formats. (order: reverse; iteration: 0)
- **Digital and print subscription: $120** — I enjoy both digital and print, so I would choose the option that includes both formats. (order: reverse; iteration: 1)

### decoy: with_decoy

Choose an annual magazine subscription for yourself. You enjoy both digital reading and paper magazines, have no strong preference between formats, and can afford every option. All options contain the same editorial content. Which subscription do you choose?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

Options (also presented in reverse order): Digital subscription: $60 / Digital and print subscription: $120 / Print-only subscription: $120

- **Digital and print subscription: $120** — I choose this because it includes both formats I enjoy at the same price as print-only. (order: reverse; iteration: 0)
- **Digital and print subscription: $120** — It provides both formats at the same price as print-only. Since I enjoy reading digitally and on paper, it best matches my preferences. (order: reverse; iteration: 1)
- **Digital and print subscription: $120** — This option provides both digital and paper access, matching the stated enjoyment of both formats while covering all available options. (order: forward; iteration: 0)
- **Digital and print subscription: $120** — It gives me both reading formats at the same price as print-only, so I get the most flexibility for the money. (order: forward; iteration: 1)

### intuitive_arithmetic: notebook_pen

A notebook and a pen cost $8.80 in total. The notebook costs $8.00 more than the pen. How much does the pen cost, in dollars?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

- **0.4** — # Let p be the pen cost; then p + (p + 8) = 8.80, so 2p = 0.80 and p = 0.4. (order: forward; iteration: 0)
- **0.4** — Let the pen cost x. Then x + (x + 8) = 8.80, so 2x = 0.80 and x = 0.40. (order: forward; iteration: 1)
- **0.4** — If the pen costs p, then p + (p + 8.00) = 8.80, so 2p = 0.80 and p = 0.40. (order: forward; iteration: 2)
- **0.4** — # Let the pen cost x; then the notebook costs x+8, so x+(x+8)=8.80 gives x=0.40. (order: forward; iteration: 3)

### intuitive_arithmetic: cake

A whole cake weighs 3 kilograms plus half of its own weight. How many kilograms does the whole cake weigh?

All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.

- **6** — # Let W be the cake's weight; W = 3 + W/2, so W = 6. (order: forward; iteration: 0)
- **6** — # If the cake weighs w, then w = 3 + w/2, so w = 6 kilograms. (order: forward; iteration: 1)
- **6** — The cake's weight W satisfies W = 3 + W/2, so W = 6 kilograms. (order: forward; iteration: 2)
- **6** — Let W be the weight; W = 3 + W/2, so W = 6 kg. (order: forward; iteration: 3)

## Files and methods

See [methodology](../BEHAVIORAL_TESTS.md), [conditions](conditions.json), [protocol](protocol.json), [CSV](responses.csv), and [machine-readable summary](summary.json). Full serialized results, rendered prompts, and raw server responses are in the per-family `.results.ep` packages.
