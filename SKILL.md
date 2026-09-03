---
name: de-ai-flavor
description: 扫描中文文本里的 AI 味（套话、翻案腔、黑话、报告腔），逐条给出人话改写建议。以 Skill 形态融入你的写作工作流。
rules:
  - rules/rules_doc.yaml
prompts:
  - prompts/editorial-core.md
  - prompts/design-prompts-and-workflows.md
---

# de-ai-flavor · 中文与 AI 设计去味规则库

本技能用于在中文创作、AI 翻译与网页/应用 UI 设计过程中识别并去除明显的 AI 腔调（AI-slop / AI 味）。

## 核心法则与原则

1. **绝对不作平庸与可预测的选择**：
   - AI 大模型本质上是 token 预测器，倾向于在每个节点选择最稳妥、最平庸的“大众平均解”（AI slop）。
   - 高质量设计与文字必须跳出最可预测的路径，提供有性格、有情绪共鸣、令人印象深刻的选择。

2. **去 AI 设计与提示词原则（来自 Anshu Chimala 指南）**：
   - **种子字符串注入多样性 (Seed Strings)**：使用随机种子打破模型的固定模式路径，产生真正独一无二的视觉与排版构想。
   - **设计批评者双 Agent 架构 (Design Critic Loop)**：代码/内容生成 Agent 与独立 Visual/Style Critic Agent 分开。Critic 在无代码上下文的干净环境中仅看截图/最终文本，给出客观无情的打分与改写建议。
   - **做减法而非做加法**：AI 极度喜欢堆砌装饰（多余的渐变、多余的文本标签、过度的总结词）。优质成果来自果断的删除。
   - **去 AI 味标识**：坚决剔除 AI 标志性的紫色渐变、左文右图呆板双栏、毫无道理的打光、黑话套话与假装中立的修辞。

3. **中文文字去 AI 味规则**：
   - 严禁「值得注意的是」「总的来说」「综上所述」「本质上」「首先/其次」等报告腔套话。
   - 严禁「不是…而是…」类伪深刻翻案句式。
   - 严禁冒号、破折号——、双引号“”的过度滥用。

## 结合进工作流使用方式

当进行内容改写、设计建议或翻译润色时，加载本 Skill 并使用本地规则引擎或 `prompts/editorial-core.md` / `prompts/design-prompts-and-workflows.md` 指导输出，自查并清除所有 AI 痕迹。
