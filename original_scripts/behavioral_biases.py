"""Build and run a small, independent-prompt behavioral battery on local Bonsai.

python examples/prismml_local/behavioral_biases.py --build-only
python examples/prismml_local/behavioral_biases.py
Existing result packages are reused; use a new --output directory for a new run.
"""

import argparse
import csv
import json
from pathlib import Path
import random
import subprocess
import time

from edsl import Cache, Model, ModelList, QuestionMultipleChoice, QuestionNumerical, Scenario, ScenarioList, Results
from edsl.config import CONFIG
from ask_france import BASE_URL, bonsai_server


def conditions():
    items = []

    def add(family, condition, prompt, options=None, correct=None, note=""):
        items.append(dict(family=family, condition=condition, prompt=prompt,
                          options=options, correct=correct, note=note))

    add("conjunction", "linda",
        "Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. "
        "As a student, she was deeply concerned with issues of discrimination and social justice, "
        "and also participated in anti-nuclear demonstrations. Which is more probable?",
        ["Linda is a bank teller.", "Linda is a bank teller and is active in the feminist movement."],
        "Linda is a bank teller.", "A conjunction cannot be more probable than its component.")
    add("conjunction", "new_vignette",
        "Morgan loves star charts, spends clear evenings photographing planets, and volunteers at a planetarium. Which is more probable?",
        ["Morgan works as an accountant.", "Morgan works as an accountant and belongs to an astronomy club."],
        "Morgan works as an accountant.")

    for label, rate, correct in [("rare", 1, 100 * .008 / .107), ("common", 40, 100 * .32 / .38)]:
        add("base_rate", label,
            f"A factory produces parts, of which {rate}% are defective. A scanner flags 80% of defective parts "
            "and also flags 10% of non-defective parts. A part is randomly selected and is flagged. "
            "What is the probability that it is defective? Give a percentage from 0 to 100, rounded to two decimal places.",
            correct=round(correct, 2), note="Bayes rule; numeric tolerance 0.1 percentage points.")

    for label, sequence in [("streak", "heads, heads, heads, heads, heads, heads"),
                            ("mixed", "heads, tails, tails, heads, tails, heads")]:
        add("gambler", label,
            f"A fair coin has been flipped six times, producing {sequence}. Each flip is independent. "
            "On the next flip, which outcome is more likely?",
            ["Heads", "Tails", "Heads and tails are equally likely"], "Heads and tails are equally likely")

    add("framing", "saved",
        "A damaged archive contains 900 files. Choose a recovery plan. Plan A will save exactly 300 files. "
        "Plan B has a 1/3 chance of saving all 900 files and a 2/3 chance of saving none. "
        "Every file is equally valuable; these are the complete outcomes. Which plan do you choose?",
        ["Plan A", "Plan B"], note="Compare Plan B rate with equivalent lost-files wording; no uniquely correct risk preference.")
    add("framing", "lost",
        "A damaged archive contains 900 files. Choose a recovery plan. Plan A will lose exactly 600 files. "
        "Plan B has a 1/3 chance of losing no files and a 2/3 chance of losing all 900 files. "
        "Every file is equally valuable; these are the complete outcomes. Which plan do you choose?",
        ["Plan A", "Plan B"])

    for label, anchor in [("low", 10), ("high", 100)]:
        add("anchoring", label,
            "You are estimating the engineering hours for a new module. Three comparable modules required "
            "38, 44, and 46 hours. The new module is similar in scope and staffing. "
            f"Before you estimate, an unrelated random-number generator displays {anchor}. "
            f"Consider whether the new module will take more or less than {anchor} hours. "
            "What is your best estimate of its total engineering hours? Return a number of hours.",
            note="Compare high versus low estimates; random number supplies no information; no unique point estimate imposed.")

    for label, sunk in [("none", 0), ("large", 8000)]:
        add("sunk_cost", label,
            f"You manage a project and have already spent ${sunk}, which cannot be recovered. "
            "Finishing will cost an additional $4000 and yield revenue of exactly $2500. "
            "Stopping costs nothing and yields no further revenue. There are no reputation, learning, "
            "contractual, or other consequences. Your sole objective is to maximize final net money. What do you do?",
            ["Finish the project", "Stop the project"], "Stop the project")

    add("confirmation", "card_test",
        "Each card has a letter on one side and a number on the other. Four cards show E, K, 4, and 7. "
        "You must test the rule: If a card has a vowel on one side, then it has an even number on the other. "
        "Which cards must you turn over, and only those cards, to determine whether the rule is violated?",
        ["E and 4", "E and 7", "E only", "All four cards"], "E and 7",
        "Wason-style logical falsification probe; a wrong answer alone does not isolate confirmation bias.")

    for label, default in [("a_default", "A"), ("b_default", "B")]:
        add("default", label,
            "Choose between two internet plans. Plan A costs $40 per month with 100 Mbps service. "
            "Plan B costs $50 per month with 200 Mbps service. All other terms are identical. "
            "You have no urgent budget constraint, and either speed handles your current needs. "
            f"The form randomly preselects Plan {default}; this is not a recommendation. "
            "Choosing either plan takes the same effort and has no switching cost. Which do you choose?",
            ["Plan A", "Plan B"], note="Compare Plan B rate across defaults; no unique correct preference.")

    for label, early, late in [("now", "today", "in 30 days"), ("later", "in 365 days", "in 395 days")]:
        add("present_bias", label,
            f"Choose one guaranteed payment: $50 {early}, or $60 {late}. "
            "Both payments are equally certain, there are no fees or inflation, and you have no immediate "
            "cash needs or borrowing constraints. Which do you choose?",
            ["The earlier $50 payment", "The later $60 payment"],
            note="Look for greater earlier-payment share in now condition; repeated samples are not longitudinal individuals.")

    for label, decoy in [("without_decoy", False), ("with_decoy", True)]:
        options = ["Digital subscription: $60", "Digital and print subscription: $120"]
        if decoy:
            options.append("Print-only subscription: $120")
        add("decoy", label,
            "Choose an annual magazine subscription for yourself. You enjoy both digital reading and paper "
            "magazines, have no strong preference between formats, and can afford every option. All options "
            "contain the same editorial content. Which subscription do you choose?",
            options, note="Compare bundle share when dominated print-only option is added; preference is not correctness.")

    add("intuitive_arithmetic", "notebook_pen",
        "A notebook and a pen cost $8.80 in total. The notebook costs $8.00 more than the pen. "
        "How much does the pen cost, in dollars?", correct=0.4, note="Intuitive lure is $0.80; correct answer is $0.40.")
    add("intuitive_arithmetic", "cake",
        "A whole cake weighs 3 kilograms plus half of its own weight. How many kilograms does the whole cake weigh?",
        correct=6, note="Solve w = 3 + w/2; correct answer is 6 kg.")
    return items


def build(output):
    items = conditions()
    (output / "conditions.json").write_text(json.dumps(items, indent=2) + "\n")
    model = Model("bonsai-2-27b", service_name="openai_compatible", base_url=f"{BASE_URL}/v1",
                  temperature=1.0, top_p=0.95, max_tokens=2048)
    ModelList([model]).save(str(output / "models.ep"))
    jobs = {}
    for family in dict.fromkeys(x["family"] for x in items):
        cells = [x for x in items if x["family"] == family]
        multiple_choice = cells[0]["options"] is not None
        scenarios = []
        for cell in cells:
            for rep in range(2 if multiple_choice else 1):
                row = {k: v for k, v in cell.items() if k not in ("correct", "note")}
                row["replicate"] = rep + 1
                row["order"] = "forward" if rep % 2 == 0 else "reverse"
                if multiple_choice and rep % 2:
                    row["options"] = list(reversed(row["options"]))
                scenarios.append(Scenario(row))
        random.Random(20260917).shuffle(scenarios)
        kwargs = dict(question_name="response", question_text="{{ prompt }}\nGive a brief explanation in at most two sentences.", include_comment=True)
        q = (QuestionMultipleChoice(**kwargs, question_options="{{ options }}") if multiple_choice
             else QuestionNumerical(**kwargs))
        job = q.by(ScenarioList(scenarios)).by(model)
        path = output / f"{family}.jobs.ep"
        job.save(str(path))
        check = subprocess.run(["ep", "validate", "--file", str(path)], capture_output=True, text=True)
        envelope = json.loads(check.stdout)
        if check.returncode or envelope["status"] != "ok":
            raise RuntimeError(envelope)
        if envelope.get("warnings"):
            print(json.dumps(envelope["warnings"]), flush=True)
        jobs[family] = (job, 2 if multiple_choice else 4)
    protocol = dict(model=model.to_dict(), conditions=len(items), repetitions_per_condition=4,
                    interviews=len(items) * 4, fresh=True, max_concurrency=1, seed_for_order=20260917,
                    cache="Empty in-memory Cache per family, distinct iteration keys; audit unique completion IDs and any available cache flags.",
                    server_settings="start-server.sh: 8192 context, 512 reasoning budget, one slot; inspect running server if reused",
                    design="Independent one-question interviews; no bias names or answer keys in rendered prompts. "
                           "MC options forward twice and reverse twice (not full counterbalancing for >2 options). "
                           "No participant persona. EDSL default agent instructions. Comments requested. "
                           "These are stochastic model responses, not human subjects or independent model replications.")
    (output / "protocol.json").write_text(json.dumps(protocol, indent=2) + "\n")
    return jobs


def export(output):
    rows = []
    for cell in conditions():
        path = output / f"{cell['family']}.results.ep"
        if not path.exists():
            continue
        results = Results.load(str(path))
        for result in results:
            s = result.scenario
            if s["condition"] != cell["condition"]:
                continue
            answer = result.answer.get("response")
            correct = cell["correct"]
            match = (abs(answer - correct) <= (0.1 if cell["family"] == "base_rate" else 1e-6)
                     if isinstance(correct, (int, float)) and isinstance(answer, (int, float))
                     else answer == correct) if correct is not None else None
            raw = result.data.get("raw_model_response", {}).get("response_raw_model_response", {})
            choices = raw.get("choices", []) if isinstance(raw, dict) else []
            content = choices[0].get("message", {}).get("content", "") or "" if choices else ""
            rows.append(dict(family=cell["family"], condition=cell["condition"], replicate=s["replicate"], iteration=result.data["iteration"],
                             order=s["order"], prompt=s["prompt"], options=s["options"], answer=answer,
                             comment=result.sub_dicts["comment"].get("response_comment"), correct_answer=correct,
                             matches_key=match, validated=result.sub_dicts["validated"].get("response_validated"),
                             cache_used=result.data.get("cache_used_dict", {}).get("response_cache_used"),
                             response_id=raw.get("id") if isinstance(raw, dict) else None,
                             reasoning_in_answer_channel="</think>" in content or "<think>" in content,
                             final_text_after_thinking=content.rsplit("</think>", 1)[-1].strip() if "</think>" in content else None,
                             finish_reason=choices[0].get("finish_reason") if choices else None))
    (output / "responses.json").write_text(json.dumps(rows, indent=2) + "\n")
    if rows:
        with (output / "responses.csv").open("w") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--export-only", action="store_true")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "behavioral_bias_run")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.export_only:
        print(f"Exported {len(export(args.output))} responses")
        return
    jobs = build(args.output)
    print(f"Validated {len(jobs)} jobs; {len(conditions()) * 4} interviews", flush=True)
    if args.build_only:
        return
    CONFIG.EDSL_API_TIMEOUT = "300"
    with bonsai_server():
        for family, (job, iterations) in jobs.items():
            path = args.output / f"{family}.results.ep"
            expected = 4 * sum(x["family"] == family for x in conditions())
            if path.exists():
                existing = Results.load(str(path))
                if len(existing) == expected and all(r.answer.get("response") is not None for r in existing):
                    print(f"Reusing {family}: {len(existing)} responses", flush=True)
                    continue
                raise RuntimeError(f"Incomplete saved results at {path}; preserve and inspect before resuming.")
            started = time.monotonic()
            print(f"Running {family}: {expected} responses", flush=True)
            results = job.run(disable_remote_inference=True, disable_remote_cache=True, fresh=True,
                              cache=Cache(), n=iterations,
                              stop_on_exception=False, max_concurrency=1, progress_bar=False)
            results.save(str(path))
            if len(results) != expected or any(r.answer.get("response") is None for r in results):
                raise RuntimeError(f"Incomplete results in {path}")
            print(f"Finished {family} in {time.monotonic()-started:.1f}s", flush=True)
            export(args.output)
    print(f"Saved {len(export(args.output))} responses to {args.output}", flush=True)


if __name__ == "__main__":
    main()
