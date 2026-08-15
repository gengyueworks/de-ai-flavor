#!/usr/bin/env bash
# 包根入口：转发到 scripts/run.sh（支持从包根直接调用）
exec "$(cd "$(dirname "$0")" && pwd)/scripts/run.sh" "$@"
