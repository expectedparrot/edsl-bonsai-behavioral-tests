#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"

# PrismML's fork is required for the Bonsai 2 weight format.
# One slot keeps memory use and EDSL concurrency predictable.
exec ./runtime/llama-prism-b10683-d8f26ee/llama-server \
  --model ./models/Ternary-Bonsai-2-27B-PQ2_0.gguf \
  --alias bonsai-2-27b \
  --host 127.0.0.1 --port 8087 \
  --n-gpu-layers 999 --flash-attn on \
  --ctx-size 8192 --parallel 1 \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0 --repeat-penalty 1.0 \
  --jinja --reasoning-format deepseek --reasoning-budget 512 \
  "$@"
