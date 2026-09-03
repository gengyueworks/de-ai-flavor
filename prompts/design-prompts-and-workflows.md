# AI 设计与交互去味指南 · How to Turn Your AI into a World-Class Designer

本指南整理自 Anshu Chimala（前 Apple R&D 团队负责人）关于消除 AI 视觉与交互平庸味（AI slop）的核心方法论，适用于网页设计、前端 UI 生成及 AI 交互原型开发。

---

## 为什么 AI 生成的设计总是充斥着“AI味”（AI Slop）？

大语言模型本质上是 token 预测器：在每一步，它们都会预测最符合大众平均偏好的下一个 token。当模型做设计决策（颜色、布局、排版）时，它总是选择最不可能得罪任何人的安全选项。

其结果就是：**极其平庸、千篇一律的视觉套路**（例如：紫粉色渐变、左侧文字+右侧插图、极度可预测的顶部导航栏）。

而优秀的设计完全相反：它始于情绪与感官，通过打破规则和意想不到的选择带来惊喜。

---

## 突破 AI 平庸设计的 3 大阶段与 7 种技术

### 一、 探索阶段（Discover）：冲破可预测的框架

#### 1. 种子字符串注入多样性 (Seed Strings of Thought)
- **问题**：直接提示“给我一个独特的设计”无效，模型依然会返回预训练中的概率均值。
- **解法**：通过脚本在外部生成一个长随机字符串（Seed String），让 AI 基于该字符串提取子模式/视觉灵感来定义设计语言。
- **效果**：迫使模型从非概率均值的起点出发，每次生成完全独一无二的视觉构想。

#### 2. 大胆具体的 Prompt 激发审美性格
- 带入具体的审美来源（如：“工业控制面板”、“80年代复古像素”、“极简包豪斯”）。
- 不怕给出听起来“不可能成功”的规则破坏性要求。

---

### 二、 定型阶段（Define）：深化设计个性

#### 3. 引入“设计批评者”双 Agent 循环 (Design Critic Loop)
- **痛点**：生成代码的 Agent 无法客观评价自己的产出。
- **解法**：引入一个强模型（如 Claude Opus / Fable）作为独立 Critic。
- **规则**：
  - Critic 处于干净全新的上下文，**只看视觉截图，不看底层代码**。
  - Critic 针对预设的设计目标打分（满分10分），列出最显 AI 味的平庸套路并要求整改。
  - 只有独立打分达到 9 分以上，代码 Agent 的任务才算完成。

#### 4. 融合生成式图像与动态视效
- 拒绝纯靠 CSS 代码渐变和符号撑场面，提示 Agent 合理调用图像生成 API 或 Shader 特效。

#### 5. 使用视频生成模型打造流体交互与过渡
- 利用视频生成模型在两个 Keyframe 页面状态之间做插值，实现随着用户滚动或交互而平滑蜕变的视觉动态。

---

### 三、 交付阶段（Deliver）：精细化去味与打磨

#### 6. 果断做减法（Cut Out Non-Value Elements）
- AI 的天性是不断做加法（加发光、加渐变、加多余标签、加无意义容器）。
- **去 AI 味的核心在于删除**：去掉所有对传递核心信息没有帮助的装饰，保留纯粹的排版与空间感。

#### 7. 彻底清除 AI 视觉标志（Remove AI Tells）
- 审查并剔除：
  - 紫色/粉色渐变气泡
  - 无理由的深色暗黑卡片+发光边框
  - 呆板的左文右图双栏响应式模板
  - 虚假中立、过度解释的文字提示

---

## 实践 Prompt 模板

```markdown
I want you to improve this design using a dual-agent feedback loop.

Follow this procedure at each iteration:
1. Capture a screenshot of the current design.
2. Invoke the critic in a fresh context with ONLY the screenshot (no code/history).
3. Evaluate against top design studio standards, penalize any generic AI-generated patterns (e.g. purple gradients, repetitive cards, predictable layouts).
4. Provide a strict score out of 10. Only stop when score is >= 9/10.
```
