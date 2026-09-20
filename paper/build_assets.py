"""Build paper tables, figure, and prompt appendix from saved data (no inference)."""
import json
import os
from collections import Counter
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/bonsai-paper-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "behavioral_bias_run"
rows = json.loads((DATA / "responses.json").read_text())
conditions = json.loads((DATA / "conditions.json").read_text())
assert len(rows) == 84
assert len({r["response_id"] for r in rows}) == 84
assert all(r["validated"] and r["finish_reason"] == "stop" for r in rows)
assert all(n == 4 for n in Counter((r["family"], r["condition"]) for r in rows).values())


def tex(value):
    value = str(value).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    value = value.replace("–", "--").replace("—", "---").replace("×", r"$\times$").replace("≈", r"$\approx$")
    # Protect inserted math escapes while escaping ordinary input character by character.
    value = str(value).replace(r"$\times$", "MULTSIGN").replace(r"$\approx$", "APPROXSIGN")
    escapes = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
               "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(escapes.get(c, c) for c in value).replace("MULTSIGN", r"$\times$").replace("APPROXSIGN", r"$\approx$")


labels = {"conjunction": "Conjunction", "base_rate": "Base rates", "gambler": "Independent coin flips",
          "framing": "Framing", "anchoring": "Anchoring", "sunk_cost": "Sunk cost",
          "confirmation": "Logical falsification", "default": "Defaults", "present_bias": "Payment timing",
          "decoy": "Decoy", "intuitive_arithmetic": "Intuitive arithmetic"}

appendix = []
for cell in conditions:
    group = [r for r in rows if (r["family"], r["condition"]) == (cell["family"], cell["condition"])]
    appendix += [r"\noindent\begin{minipage}{\linewidth}",
                 r"\subsection{" + tex(labels[cell["family"]] + ": " + cell["condition"].replace("_", " ")) + "}",
                 r"\noindent\textbf{Question.} " + tex(cell["prompt"]) + r"\par"]
    if cell["options"]:
        appendix += [r"\noindent\textbf{Options (forward order).}\par", r"\begin{enumerate}[nosep,leftmargin=*]"]
        appendix += [r"\item " + tex(x) for x in cell["options"]]
        appendix += [r"\end{enumerate}"]
    counts = Counter(str(r["answer"]) for r in group)
    appendix += [r"\noindent\textbf{Observed answers.} " + "; ".join(tex(k) + f" ({v}/4)" for k, v in counts.items()) + r".\par"]
    if cell["correct"] is not None:
        appendix += [r"\noindent\textbf{Scoring key.} " + tex(cell["correct"]) + r".\par"]
    comment = next((r["comment"] for r in group if r["comment"] and not r["reasoning_in_answer_channel"]), None)
    if comment:
        appendix += [r"\noindent\textbf{Example final explanation.} ``" + tex(comment.lstrip("# ")) + "''\par"]
    appendix += [r"\end{minipage}\par\medskip", ""]
(HERE / "prompt_appendix.tex").write_text("\n".join(appendix))

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "pdf.fonttype": 42})
fig, ax = plt.subplots(figsize=(6.6, 2.35))
for y, condition in [(1, "linda"), (0, "new_vignette")]:
    for x, (order, iteration) in enumerate([("forward", 0), ("forward", 1), ("reverse", 0), ("reverse", 1)]):
        row = next(r for r in rows if r["condition"] == condition and r["order"] == order and r["iteration"] == iteration)
        correct = row["matches_key"]
        ax.scatter(x, y, s=180, marker="o" if correct else "X", color="#236b77" if correct else "#aa412d", zorder=3)
ax.set_yticks([0, 1], ["New astronomy vignette", "Canonical Linda item"])
ax.set_xticks(range(4), ["Forward\ndraw 1", "Forward\ndraw 2", "Reverse\ndraw 1", "Reverse\ndraw 2"])
ax.set_xlim(-0.45, 3.45)
ax.set_ylim(-0.5, 1.55)
ax.grid(axis="x", color="#dddddd", linewidth=.7)
ax.tick_params(axis="both", length=0, pad=8)
for spine in ax.spines.values():
    spine.set_visible(False)
legend = [Line2D([0], [0], marker="o", linestyle="", color="#236b77", label="Correct", markersize=8),
          Line2D([0], [0], marker="X", linestyle="", color="#aa412d", label="Conjunction error", markersize=8)]
ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(.42, 1.25), ncol=2, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "conjunction_results.pdf", bbox_inches="tight")
fig.savefig(HERE / "conjunction_results.png", dpi=180, bbox_inches="tight")
print("Verified 84 responses; generated prompt appendix and conjunction figure.")
