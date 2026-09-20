# Bonsai behavioral tests with EDSL

Run PrismML's **Ternary Bonsai 2 27B** locally through [EDSL](https://github.com/expectedparrot/edsl), ask a question, and reproduce an exploratory behavioral battery.

The original run used an **Apple M4 Max MacBook Pro with 48 GB unified memory**, PQ2_0 weights, and PrismML's Metal-enabled llama.cpp fork. The model weights occupy **7.21 GB**; this is not a measurement of total runtime memory. Other Macs have not been tested here. The included launcher targets Apple Silicon macOS; Linux/CUDA requires a different runtime.

**Read without running:** [academic report (PDF)](paper/bonsai_edsl_report.pdf) · [observed results](behavioral_bias_run/report.md) · [all prompts and answers](behavioral_bias_run/all_responses.md) · [methodology](BEHAVIORAL_TESTS.md)

## Quick start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
git clone https://github.com/expectedparrot/edsl-bonsai-behavioral-tests.git
cd edsl-bonsai-behavioral-tests
uv sync --locked
uv run python download_model.py
uv run python ask_linda.py
```

The downloader fetches the pinned runtime and approximately 7.21 GB of weights, verifies SHA-256 checksums, and extracts the runtime. Allow disk space for both the weights and Python dependencies. Downloads require internet access; inference runs locally and needs no API key.

`ask_linda.py` starts the server as a subprocess, waits for model readiness, asks the question, saves `runs/linda.results.ep`, and shuts down its server even if inference fails. If a healthy server already runs on port 8087, the script reuses it and leaves it running. A reused server must use the same model alias and intended settings. Startup messages are in `managed-server.log`.

The correct Linda answer is “Linda is a bank teller.” Generated answers can vary.

## The EDSL connection

EDSL's existing OpenAI-compatible provider talks to the local server:

```python
from edsl import Cache, Model, QuestionFreeText
from bonsai_server import bonsai_server

model = Model(
    "bonsai-2-27b",
    service_name="openai_compatible",
    base_url="http://127.0.0.1:8087/v1",
    temperature=1.0,
    max_tokens=2048,
)
question = QuestionFreeText(
    question_name="capital",
    question_text="What is the capital of France?",
)
with bonsai_server():
    results = question.by(model).run(
        disable_remote_inference=True,
        disable_remote_cache=True,
        cache=Cache(),
        stop_on_exception=True,
    )
print(results.select("answer.capital").first())
```

The full Linda example adds a longer request timeout and saves the result. `start-server.sh` uses one inference slot, an 8192-token context, Metal GPU offloading, and a 512-token reasoning budget. The Python examples allow 2048 output tokens. These are bounded test settings.

## Run the behavioral battery

Build and validate inputs without loading the model:

```sh
uv run python behavioral_biases.py --build-only
```

Run 84 interviews across 21 conditions and 11 families:

```sh
uv run python behavioral_biases.py
uv run python summarize_biases.py
```

New results go in **`runs/local/`**, separate from the published observations in **`behavioral_bias_run/`**. Complete family results are reused on restart. For an independent rerun:

```sh
uv run python behavioral_biases.py --output runs/replication-01
uv run python summarize_biases.py --output runs/replication-01
```

Model sampling is stochastic and not seeded. The fixed shuffle seed controls scenario order only. The original completion timestamps spanned about 26 minutes, including a checkpoint/resume interval; that is not a controlled throughput benchmark.

To inspect the published results without model weights or inference:

```sh
uv run ep results select \
  --file behavioral_bias_run/conjunction.results.ep \
  --column scenario.condition --column answer.response
```

To regenerate exported tables from the original Results packages:

```sh
uv run python summarize_biases.py --output behavioral_bias_run
```

## What happened in the original run?

| Observation | Result |
| --- | --- |
| Questions with explicit answer keys | 41/44 correct |
| Canonical Linda conjunction item | 4/4 correct |
| New astronomy conjunction vignette | 1/4 correct; three conjunction errors |
| Bayes, independent coins, sunk costs, logical cards, arithmetic | All scored answers correct |
| Matched preference/estimate conditions | No consistent classic bias pattern in this small sample |
| Completion audit | 84 validated answers; 84 distinct completion IDs |

The preference conditions are not included in the accuracy denominator. Four draws per condition from one model do not establish general rationality, a population bias rate, or similarity to human respondents. Familiarity with canonical questions is one possible explanation for the conjunction contrast, not a demonstrated mechanism. One completion leaked reasoning into the answer channel; the report documents it and its effect on interpretation.

## Reproducibility and repository layout

- `ask_linda.py`, `bonsai_server.py`, `start-server.sh`: single-question example and managed local inference.
- `download_model.py`, `downloads.json`: pinned assets and checksum verification.
- `behavioral_biases.py`, `summarize_biases.py`: battery construction, execution, and reporting.
- `behavioral_bias_run/`: original 84 observations, all Jobs/Results packages, exports, conditions, and protocol.
- `original_scripts/`: preserved scripts associated with the original run and recorded source hashes.
- `paper/`: PDF, LaTeX, references, figure, and prompt appendix.
- `tests/`: offline checks; no weights or model calls required.

`uv.lock` pins the dependency environment. EDSL is pinned to commit `852a050d0b4e84facdaea0628e7c1e062daa4a46`, verified for this packaging exercise. The original run recorded EDSL `1.0.8.dev1` but did not record its Git revision; this dependency pin is not a claim about the original run's exact checkout. The standalone scripts split out the server helper, rename the single-question example, and use a separate output directory. The battery prompts and inference settings are preserved.

The PDF describes the original EDSL repository paths (`examples/prismml_local/...`). In this standalone repository that directory is the repository root; the old `ask_france.py` helper is split between `ask_linda.py` and `bonsai_server.py`. The paper's Macaw/Modal section is a deployment assessment, not an implemented or tested Modal deployment.

## Checks and paper build

```sh
uv run pytest -q
uv run python download_model.py --check-only
uv sync --locked --group paper
uv run --group paper python paper/build_assets.py
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error bonsai_edsl_report.tex
```

The checksum check needs downloaded assets; the other offline checks do not. Building the paper needs a TeX installation with `latexmk` and `pdflatex`. The generated appendix and figure are committed, so compiling the existing LaTeX does not need Python or new inference. See [paper instructions](paper/README.md).

## License and upstream assets

The example code and documentation are distributed under the [MIT license](LICENSE). Model-generated outputs are included as research artifacts. PrismML's weights, runtime binaries, and their licenses remain upstream and are not included in this repository:

- [Pinned model card and weights](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/tree/6ed5e12bf84b7a63069882c91dd9e9218647d17b)
- [Pinned runtime release](https://github.com/PrismML-Eng/llama.cpp/releases/tag/prism-b10683-d8f26ee)
- [PrismML runtime documentation](https://github.com/PrismML-Eng/Bonsai-demo)

The research note and repository packaging were prepared with AI assistance.
