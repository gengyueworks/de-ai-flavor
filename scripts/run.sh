#!/usr/bin/env bash
# run.sh — de-ai-flavor 通用版
#   bash run.sh scan [文件]   # 扫描（默认 doc 层）
#   bash run.sh test          # 跑回归测试
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="python3"
case "${1:-}" in
  scan)
    shift || true
    if [ $# -ge 1 ]; then
      exec "$PY" "$ROOT/scripts/scan.py" --layer doc -f "$1"
    else
      exec "$PY" "$ROOT/scripts/scan.py" --layer doc
    fi
    ;;
  test)
    exec "$PY" "$ROOT/tests/regression/run_regression.py"
    ;;
  *)
    echo "用法: bash run.sh scan [文件] | bash run.sh test"
    exit 1
    ;;
esac
