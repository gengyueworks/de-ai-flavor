# de-ai-flavor · 中文去 AI 味检测工具

De-AI-Flavor scans Chinese text for AI-slop patterns and suggests human-sounding rewrites. Built as a Claude Code / Codex skill.

扫描中文文本里的 AI 味（套话、翻案腔、黑话、报告腔），逐条给出人话改写建议。以 Skill 形态融入你的写作工作流。

> **绝不直接改原文，只给建议** · Never rewrites your text — it only suggests.

---

## 它治什么 AI 味 · What it catches

| 类型 Type | 例子 Example |
|---|---|
| 高频套话 Cliched fillers | 值得注意的是 / 总的来说 / 综上所述 |
| 翻案腔 Strawman-then-rebut | 「不是…而是…」类 |
| 黑话 Corporate jargon | 赋能 / 抓手 / 闭环 |
| 教科书开头 Textbook openings | 在当今…的时代 / 随着…的发展 |
| 禁用标点 Banned punctuation | 冒号：/ 破折号——/ 双引号“” |

## 快速开始 · Quick start

```bash
# 扫描文件 / Scan a file
bash run.sh scan 文章.md

# 扫描 stdin（管道或粘贴）/ Scan stdin
cat 文章.md | bash run.sh scan
echo "这本质上是一个..." | bash run.sh scan

# 跑回归测试 / Run regression tests
bash run.sh test
```

## 输出解读 · Reading the output

```
[de-ai-flavor] 扫描完成
═══ 硬性违规 (block) ═══          ← 绝对禁用，出现就建议改
第12行 | 本质上 | → 说到底 / 其实
  原文：这本质上是一个...
═══ 建议 (warn) ═══               ← 风格建议，酌情处理
第30行 | 首先 | → 直接说第一件事
═══ 统计 ═══
平均句长: 24.3 字 | 连续相近句最长: 6 句
```

- **block**：绝对禁用词/句式，出现建议必改
- **warn**：风格提示，酌情处理
- 输出还包括句长节奏统计（连续相近句过长 = 呆板）

## 安装 · Install

把本目录放给支持文件与 MCP 的 Agent（Claude Code / Codex / Cursor），或放入 `~/.claude/skills/de-ai-flavor/`。

Give this folder to a file-and-MCP-capable agent, or copy it into `~/.claude/skills/de-ai-flavor/`.

## 工作原理 · How it works

纯本地规则引擎（Python 标准库，零依赖），不调用任何外部模型：

1. 加载 `rules/rules_doc.yaml`：禁用词（block/warn 两级）、禁用标点、结构套话正则
2. 逐条命中 → 输出行号 + 原文 + 替换建议
3. 附加节奏统计（平均句长、连续相近句）

A deterministic local rule engine — Python stdlib only, no external API calls.

## 规则可编辑 · Rules are editable

所有规则在 `rules/rules_doc.yaml`，随时增删：

```yaml
banned_words:
  - {word: "综上所述", replace: "换成具体的回扣句", severity: block}
  - {word: "赋能", replace: "换成具体动作", severity: block}
```

## 边界与红线 · Boundaries

- 绝不直接改原文，只输出建议
- 反幻觉：建议只给真实可行的改写方向，改不出就标注留白
- 中文优先，标点用中文全角
- 不调外部模型（现阶段）
