#!/usr/bin/env python3
"""run_regression.py — de-ai-flavor 通用版回归测试。

通用版只含 doc 通用层，回归只验证 doc 层：
    对 doc_ai_draft.md 跑 scan --layer doc，断言 block 命中数 ≥ 1（doc 层覆盖）

通过 subprocess 调用 python3 scripts/scan.py，不 import 路径耦合。
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCAN = os.path.join(ROOT, "scripts", "scan.py")
FIXTURES = os.path.join(ROOT, "tests", "regression", "fixtures")
DOC_AI_DRAFT = os.path.join(FIXTURES, "doc_ai_draft.md")

SUMMARY_RE = re.compile(r"共 (\d+) 处建议（block (\d+) / warn (\d+)）")


def run_scan_doc(path):
    """subprocess 调用 scan.py --layer doc，返回 (exit_code, block, warn, stdout)。"""
    proc = subprocess.run(
        [sys.executable, SCAN, "--layer", "doc", "-f", path],
        capture_output=True, text=True, encoding="utf-8")
    m = SUMMARY_RE.search(proc.stdout)
    if m:
        block, warn = int(m.group(2)), int(m.group(3))
    else:
        block = warn = 0
    return proc.returncode, block, warn, proc.stdout


def main():
    results = []
    ok = True

    # doc 层：典型文档段落扫描，block 命中 ≥ 1
    rc, doc_block, doc_warn, out = run_scan_doc(DOC_AI_DRAFT)
    print(f"[regression] doc_ai_draft.md : block={doc_block} warn={doc_warn} (exit={rc})")
    if rc != 0:
        ok = False
        results.append("FAIL  scan --layer doc 在 doc_ai_draft.md 上非零退出")
    if doc_block < 1:
        ok = False
        results.append(f"FAIL  doc 层 block 命中数 {doc_block} 应 ≥ 1")
    else:
        results.append("PASS  doc 层 block 命中数 ≥ 1")

    print()
    for r in results:
        print(f"[regression] {r}")
    if ok:
        print("\n[regression] 全部 PASS")
        return 0
    print("\n[regression] 存在 FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
