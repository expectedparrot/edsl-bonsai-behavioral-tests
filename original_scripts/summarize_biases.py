"""Summarize saved behavioral-battery results without making model calls."""

from collections import Counter
import json
from pathlib import Path
import statistics

from behavioral_biases import conditions, export


def summarize(output):
    rows = export(output)
    cells = []
    for cell in conditions():
        subset = [r for r in rows if (r["family"], r["condition"]) == (cell["family"], cell["condition"])]
        if not subset:
            continue
        answers = [r["answer"] for r in subset]
        summary = dict(family=cell["family"], condition=cell["condition"], n=len(subset),
                       counts=dict(Counter(str(x) for x in answers)), correct=cell["correct"],
                       correct_count=sum(r["matches_key"] is True for r in subset) if cell["correct"] is not None else None)
        if all(isinstance(x, (int, float)) for x in answers):
            summary.update(mean=statistics.mean(answers), median=statistics.median(answers), minimum=min(answers), maximum=max(answers))
        cells.append(summary)
    ids = [r["response_id"] for r in rows if r["response_id"]]
    audit = dict(expected_responses=84, saved_responses=len(rows), validated=sum(r["validated"] is True for r in rows),
                 unique_completion_ids=len(set(ids)), missing_completion_ids=len(rows)-len(ids),
                 finish_reasons=dict(Counter(r["finish_reason"] for r in rows)),
                 explicit_cache_hits=sum(r["cache_used"] is True for r in rows),
                 reasoning_in_answer_channel=sum(r["reasoning_in_answer_channel"] for r in rows),
                 note="This EDSL version may omit cache flags; distinct completion IDs are the primary duplicate check.")
    summary = dict(audit=audit, conditions=cells)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = ["# Bonsai behavioral-bias battery: observed responses", "",
             f"{len(rows)}/84 responses saved. {audit['validated']} validated; {len(set(ids))} unique completion IDs.", "",
             "Four samples per condition from one model, temperature 1.0, with a 512-token reasoning budget. "
             "These are descriptive results, not significance tests or estimates of human behavior.", "",
             "| Test | Condition | Responses | Correct |", "|---|---|---|---|"]
    for cell in cells:
        values = "; ".join(f"{answer}: {count}/{cell['n']}" for answer, count in cell["counts"].items())
        correct = f"{cell['correct_count']}/{cell['n']}" if cell["correct"] is not None else "Preference/estimate"
        lines.append(f"| {cell['family']} | {cell['condition']} | {values} | {correct} |")
    lines += ["", "## Exact prompts and responses", "",
              "The following includes every answer and its final explanation. Internal reasoning is preserved in the Results packages."]
    for cell in conditions():
        subset = [r for r in rows if (r["family"],r["condition"]) == (cell["family"],cell["condition"])]
        if not subset:
            continue
        lines += ["", f"### {cell['family']}: {cell['condition']}", "", cell["prompt"], "",
                  "All prompts append: ‘Give a brief explanation in at most two sentences.’ EDSL adds response-format instructions.", ""]
        if cell["options"]:
            lines += ["Options (also presented in reverse order): " + " / ".join(cell["options"]), ""]
        for r in subset:
            explanation = (f"Formatting anomaly: reasoning appeared in the answer channel. Final text after the closing thinking tag: {r['final_text_after_thinking']}. Raw response preserved in the Results package."
                           if r["reasoning_in_answer_channel"] else (r["comment"] or "No final explanation supplied."))
            lines += [f"- **{r['answer']}** — {explanation} (order: {r['order']}; iteration: {r['iteration']})"]
    lines += ["", "## Files and methods", "",
              "See [methodology](../BEHAVIORAL_TESTS.md), [conditions](conditions.json), "
              "[protocol](protocol.json), [CSV](responses.csv), and [machine-readable summary](summary.json). "
              "Full serialized results, rendered prompts, and raw server responses are in the per-family `.results.ep` packages."]
    (output / "all_responses.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    summarize(Path(__file__).resolve().parent / "behavioral_bias_run")
