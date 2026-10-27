#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python checks/validate_distribution.py
cd reference
python -m unittest discover -s tests -v
python -m lisan_gov demo
python -m lisan_gov corpus-smoke --stdio ../baseline/Lisan-LibreChat-Pack-1.0.0/runtime/tools/stdio.mjs
