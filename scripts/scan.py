#!/usr/bin/env python3
"""scan.py — de-ai-flavor 核心检测器。

扫描文本 → 输出逐条改写建议（不修改原文）→ 用户决定采纳。

用法：
    python3 scan.py [--rules rules/generic_zh.yaml]
                    [-f 文件名 | 从 stdin 读入]

行为：
    1. 加载 generic_zh.yaml：banned_words（按 severity 分级）、banned_punctuation、patterns
    2. 附加统计：平均句长、长短句交替（连续相近句）、短段落占比
    3. LLM 增强预留接口：llm_enhance() 目前返回空列表，不调用外部服务

依赖：仅标准库。yaml 可用则用，否则用内置极简 YAML 解析器（支持嵌套 map/list）。
"""
import os
import re
import sys

try:
    import yaml  # pyyaml 可用则用
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RULES_DOC = os.path.join(ROOT, "rules", "rules_doc.yaml")
DEFAULT_RULES_CREATE = os.path.join(ROOT, "rules", "rules_generic.yaml")

SENT_SPLIT_RE = re.compile(r"[。！？…!?；]|\n+")
PARA_SPLIT = re.compile(r"\n\s*\n")


# ---------- 极简 YAML 解析（pyyaml 不可用时的 fallback） ----------
def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _to_scalar(s):
    s = s.strip().strip("\"'")
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s):
        return float(s)
    if s == "true":
        return True
    if s == "false":
        return False
    return s


def _split_flow_parts(s):
    """按 ASCII 逗号拆分，尊重引号内的逗号。"""
    parts, buf, in_q, q = [], [], False, None
    for ch in s:
        if ch in ('"', "'"):
            if in_q and ch == q:
                in_q = False
            elif not in_q:
                in_q, q = True, ch
            buf.append(ch)
        elif ch == "," and not in_q:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf).strip())
    return parts


def _parse_flow(s):
    """解析 {k: v, k2: v2} 流式 map。"""
    s = s.strip()
    if s.startswith("{") and s.endswith("}"):
        s = s[1:-1].strip()
    result = {}
    for part in _split_flow_parts(s):
        if ":" not in part:
            continue
        k, _, v = part.partition(":")
        result[k.strip().strip("\"'")] = _to_scalar(v.strip())
    return result


def _parse_block(lines, pos, min_indent):
    """解析一个 map 块，返回 (dict, new_pos)。"""
    result = {}
    while pos < len(lines):
        line = lines[pos]
        ind = _indent(line)
        if ind <= min_indent:
            break
        s = line.strip()
        if s.startswith("- ") or ":" not in s:
            break
        key, _, rest = s.partition(":")
        key = key.strip().strip("\"'")
        rest = rest.strip()
        if rest.startswith("{"):
            result[key] = _parse_flow(rest)
            pos += 1
        elif not rest:
            value, pos = _parse_value(lines, pos + 1, ind)
            result[key] = value
        else:
            result[key] = _to_scalar(rest)
            pos += 1
    return result, pos


def _parse_value(lines, pos, parent_indent):
    """解析键后的值块（嵌套 map 或 list）。
    注意 pyyaml 风格：列表项与父键同缩进（key:\n- item），
    嵌套 map 则深于父键。"""
    if pos >= len(lines):
        return None, pos
    ind = _indent(lines[pos])
    if ind < parent_indent:
        return None, pos
    s = lines[pos].strip()
    if s.startswith("- "):
        return _parse_list(lines, pos, parent_indent)
    if ind == parent_indent:
        # 与键同缩进且非列表项：无值块（或已是同级键）
        return None, pos
    return _parse_block(lines, pos, parent_indent)


def _parse_list(lines, pos, parent_indent):
    items = []
    while pos < len(lines):
        line = lines[pos]
        ind = _indent(line)
        if ind < parent_indent:
            break
        s = line.strip()
        if not s.startswith("- "):
            break
        rest = s[2:].strip()
        if rest.startswith("{"):
            items.append(_parse_flow(rest))
            pos += 1
            continue
        if ":" in rest:
            key, _, v = rest.partition(":")
            key = key.strip().strip("\"'")
            v = v.strip()
            item = {}
            if v:
                item[key] = _to_scalar(v)
                pos += 1
            else:
                value, pos = _parse_value(lines, pos + 1, ind)
                item[key] = value
            # 该 item 的续键（缩进比 "- " 行深 2 的普通键）
            while pos < len(lines):
                line2 = lines[pos]
                ind2 = _indent(line2)
                s2 = line2.strip()
                if ind2 <= ind or s2.startswith("- ") or ":" not in s2:
                    break
                k2, _, v2 = s2.partition(":")
                k2 = k2.strip().strip("\"'")
                v2 = v2.strip()
                if v2:
                    item[k2] = _to_scalar(v2)
                    pos += 1
                else:
                    value2, pos = _parse_value(lines, pos + 1, ind2)
                    item[k2] = value2
            items.append(item)
        else:
            items.append(_to_scalar(rest))
            pos += 1
    return items, pos


def load_yaml(path):
    """加载 yaml：优先 pyyaml，失败用内置极简解析器。"""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if HAS_YAML:
        return yaml.safe_load(content)
    lines = []
    for raw in content.splitlines():
        if "#" in raw:
            raw = raw.split("#", 1)[0]
        if not raw.strip():
            continue
        lines.append(raw.rstrip())
    value, _ = _parse_block(lines, 0, -1)
    return value


# ---------- 扫描逻辑 ----------
def _line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def scan_words(text, banned_words):
    """banned_words 扫描，返回 (block_hits, warn_hits)。
    每条：{line, word, replace}，按行去重。"""
    block_hits, warn_hits = [], []
    seen = set()
    for i, line in enumerate(text.splitlines(), 1):
        for item in banned_words:
            word = item["word"]
            if word in line:
                key = (i, word)
                if key in seen:
                    continue
                seen.add(key)
                hit = {"line": i, "word": word, "replace": item.get("replace", "")}
                if item.get("severity", "warn") == "block":
                    block_hits.append(hit)
                else:
                    warn_hits.append(hit)
    return block_hits, warn_hits


def scan_punctuation(text, banned_punct):
    """禁用标点扫描，按行去重。"""
    hits = []
    seen = set()
    for item in banned_punct:
        ch = item["char"]
        for m in re.finditer(re.escape(ch), text):
            ln = _line_of(text, m.start())
            key = (ln, ch)
            if key in seen:
                continue
            seen.add(key)
            hits.append({"line": ln, "char": ch,
                         "replace": item.get("replace", ""),
                         "note": item.get("note", "")})
    return hits


def scan_patterns(text, patterns):
    """结构套话正则扫描，返回 (block_hits, warn_hits)。"""
    block_hits, warn_hits = [], []
    for item in patterns:
        try:
            rx = re.compile(item["pattern"])
        except re.error:
            continue
        for m in rx.finditer(text):
            ln = _line_of(text, m.start())
            hit = {"line": ln, "pattern": item["pattern"],
                   "note": item.get("note", ""), "match": m.group(0)}
            if item.get("severity", "warn") == "block":
                block_hits.append(hit)
            else:
                warn_hits.append(hit)
    return block_hits, warn_hits


def sentence_lengths(text):
    return [len(s.strip()) for s in SENT_SPLIT_RE.split(text) if s.strip()]


def short_paragraph_ratio(text):
    paras = [p.strip() for p in PARA_SPLIT.split(text) if p.strip()]
    if not paras:
        return 0.0
    return sum(1 for p in paras if len(p) <= 15) / len(paras)


def longest_similar_run(lengths, tol_ratio=0.3, tol_abs=6):
    """连续长度相近句的最长段。相近：相对差≤30% 且 绝对差≤6 字。"""
    best = 0
    run = 1 if lengths else 0
    for i in range(1, len(lengths)):
        a, b = lengths[i - 1], lengths[i]
        diff = abs(a - b)
        if diff <= tol_abs or diff <= tol_ratio * max(a, b):
            run += 1
        else:
            run = 1
        best = max(best, run)
    return max(best, 1 if lengths else 0)


def sentence_dist(lengths):
    if not lengths:
        return {"short_ratio": 0.0, "mid_ratio": 0.0, "long_ratio": 0.0,
                "avg_len": 0.0}
    total = len(lengths)
    return {
        "short_ratio": round(sum(1 for x in lengths if x <= 10) / total, 3),
        "mid_ratio": round(sum(1 for x in lengths if 11 <= x <= 30) / total, 3),
        "long_ratio": round(sum(1 for x in lengths if x > 30) / total, 3),
        "avg_len": round(sum(lengths) / total, 1),
    }


def llm_enhance(text, hits):
    """LLM 增强预留接口。

    未来可接入模型：把 text + 当前 hits 发给本地/云端模型，
    返回额外的改写建议（list of dict：{line, suggestion}）。
    目前返回空列表，不调用任何外部服务。
    """
    return []


# ---------- 报告输出 ----------
def _fmt_original(text, ln, width=60):
    lines = text.splitlines()
    src = lines[ln - 1].strip() if 0 < ln <= len(lines) else ""
    return src[:width] + ("…" if len(src) > width else "")


def render_report(text, rules):
    out = []
    banned_words = rules.get("banned_words", []) or []
    banned_punct = rules.get("banned_punctuation", []) or []
    patterns = rules.get("patterns", []) or []
    humanity = rules.get("humanity") or {}

    block_w, warn_w = scan_words(text, banned_words)
    punct_hits = scan_punctuation(text, banned_punct)
    block_p, warn_p = scan_patterns(text, patterns)

    block_total = len(block_w) + len(block_p) + len(punct_hits)
    warn_total = len(warn_w) + len(warn_p)
    all_hits = block_total + warn_total

    if all_hits == 0:
        out.append("[de-ai-flavor] 未发现 AI 味问题，通过。")
        stats = _stats_lines(text, humanity)
        if stats:
            out.append("═══ 统计 ═══")
            out.extend(stats)
        print("\n".join(out))
        return

    out.append("[de-ai-flavor] 扫描完成")
    if block_total:
        out.append("═══ 硬性违规 (block) ═══")
        for h in block_w:
            out.append(f"第{h['line']}行 | {h['word']} | → {h['replace']}")
            out.append(f"  原文：{_fmt_original(text, h['line'])}")
        for h in block_p:
            out.append(f"第{h['line']}行 | 套话模式「{h['match']}」 | {h.get('note', '')}")
            out.append(f"  原文：{_fmt_original(text, h['line'])}")
        for h in punct_hits:
            out.append(f"第{h['line']}行 | 禁用标点「{h['char']}」 | → {h['replace']}")
            out.append(f"  原文：{_fmt_original(text, h['line'])}")
    if warn_total:
        out.append("═══ 建议 (warn) ═══")
        for h in warn_w:
            out.append(f"第{h['line']}行 | {h['word']} | → {h['replace']}")
        for h in warn_p:
            out.append(f"第{h['line']}行 | 套话模式「{h['match']}」 | {h.get('note', '')}")

    stats = _stats_lines(text, humanity)
    if stats:
        out.append("═══ 统计 ═══")
        out.extend(stats)
    out.append(f"[de-ai-flavor] 共 {all_hits} 处建议（block {block_total} / warn {warn_total}）")
    print("\n".join(out))


def _stats_lines(text, humanity=None):
    lengths = sentence_lengths(text)
    if not lengths:
        return []
    dist = sentence_dist(lengths)
    run = longest_similar_run(lengths)
    spr = short_paragraph_ratio(text)
    exclaim = text.count("！") + text.count("!")
    lines = [f"平均句长: {dist['avg_len']} 字 | 连续相近句最长: {run} 句"]
    if exclaim > 1:
        lines.append(f"⚠ 感叹号 {exclaim} 个，超过上限 1 个（编辑腔规范），建议用句号结尾")
    if run >= 5:
        lines.append(f"⚠ 连续 {run} 句长度相近，节奏可能呆板，建议长短句交替")
    if spr:
        lines.append(f"短段落占比: {spr:.2f}")

    # ---- 活人感规则（Notion「去 AI 味道 & 增强活人感」指令块） ----
    humanity = humanity or {}
    max_excl = humanity.get("max_exclamation", 1)
    exclaim = text.count("！") + text.count("!")
    if exclaim > max_excl:
        lines.append(f"⚠ 感叹号 {exclaim} 个，超过上限 {max_excl} 个，尽量用句号结尾")

    # AI 创作特征：句号高频（正常写作逗号频率远高于句号，AI 相反）
    periods = text.count("。")
    commas = text.count("，")
    if periods >= 3 and periods > commas:
        lines.append(f"⚠ 句号 {periods} 个 > 逗号 {commas} 个：句号高频是 AI 典型特征，"
                     f"正常写作逗号使用频率远高于句号，建议拆开长句、多用逗号衔接")

    max_tag = humanity.get("max_hashtag", 2)
    tags = re.findall(r"#[\w\u4e00-\u9fff]+", text)
    if len(tags) > max_tag:
        lines.append(f"⚠ 标签 {len(tags)} 个，超过上限 {max_tag} 个，文末标签不超过 1-2 个")

    reaction_pats = humanity.get("reaction_patterns") or []
    min_react = humanity.get("reaction_min_count", 1)
    if reaction_pats:
        react_found = [p for p in reaction_pats if p in text]
        if len(react_found) < min_react:
            lines.append("⚠ 全文没有「主观反应」句式（反应 > 事实），活人感不足。"
                         "在陈述事实后加一句真实的个人反应，如：我翻到了 / 我没想到 / "
                         "我不喜欢 / 这让我想起 / 我发现")
    return lines


# ---------- CLI ----------
def main():
    args = sys.argv[1:]
    layer = "create"
    rules_path = None
    file_input = None

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--layer" and i + 1 < len(args):
            layer = args[i + 1]
            if layer not in ("doc", "create"):
                print(f"[de-ai-flavor] 错误：--layer 仅支持 doc|create，收到 {layer}",
                      file=sys.stderr)
                return 2
            i += 2
        elif a == "--rules" and i + 1 < len(args):
            rules_path = args[i + 1]
            i += 2
        elif a == "-f" and i + 1 < len(args):
            file_input = args[i + 1]
            i += 2
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        elif not a.startswith("-"):
            file_input = a
            i += 1
        else:
            print(f"未知参数: {a}", file=sys.stderr)
            return 2

    # 默认路径按层解析（--rules 显式覆盖）
    if rules_path is None:
        rules_path = DEFAULT_RULES_DOC if layer == "doc" else DEFAULT_RULES_CREATE

    if not os.path.exists(rules_path):
        print(f"[de-ai-flavor] 错误：规则文件不存在 {rules_path}", file=sys.stderr)
        return 1
    rules = load_yaml(rules_path)

    if file_input:
        if not os.path.exists(file_input):
            print(f"[de-ai-flavor] 错误：文件不存在 {file_input}", file=sys.stderr)
            return 1
        with open(file_input, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    render_report(text, rules)
    return 0


if __name__ == "__main__":
    sys.exit(main())
