# Research note

`bonsai_edsl_report.pdf` is the 16-page report prepared September 19, 2026,
from the original 84-response local inference experiment.

From this directory, with TeX and latexmk installed:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error bonsai_edsl_report.tex
```

The figure and appendix are already included. To regenerate them from the saved
data, run from the repository root:

```sh
uv sync --locked --group paper
uv run --group paper python paper/build_assets.py
```

This checks and reads the published responses without making model calls.
The PDF preserves the original experiment's paths and date; its
`examples/prismml_local/` prefix maps to this repository's root.
Original scripts are under `original_scripts/`; the current quick start is in
the repository README. All original EDSL packages are in `behavioral_bias_run/`.
