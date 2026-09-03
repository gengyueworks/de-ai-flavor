# 如何把 AI 变成顶尖设计师

*👋 你好，我是 Lenny。每周我都会分享深度研究的产品、增长与职业建议。*

我过去一直觉得 AI 做设计很烂。但读完 [Anshu Chimala](https://www.linkedin.com/in/achimala/) 那篇颠覆认知的文章后，我发现是我自己用错了方法。Anshu 在 Apple 领导软件工程与设计团队长达 12 年，专注未来 AI 产品的研究与原型探索。他经常在 [X](https://x.com/anshuc) 上分享设计教程和 Demo。如果你想深入探索如何用 AI 打造独特体验，可以关注他的 [Substack](https://substack.com/@anshuc) 和 [LinkedIn](https://www.linkedin.com/in/achimala/)。

我们直接进入正题。

**用 Claude Fable 5，通过 3 条 Prompt 制作的对话式卡路里追踪器：**
![](https://substackcdn.com/image/fetch/$s_!4xxl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe65824c9-c146-4dc4-b7be-b2fcfd6b2c28_1200x675.png)

**用 Claude Opus 5，通过 2 条 Prompt 制作的太空探索游戏：**
![](https://substackcdn.com/image/fetch/$s_!Gt3V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F624f2b18-b223-4df4-aa6c-5e4df2f2a74c_1200x675.png)

**用 Claude Opus 5 + GPT-5.6 Sol，通过 3 条 Prompt 制作的动态 Landing Page：**
![](https://substackcdn.com/image/fetch/$s_!o3aj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb346747b-1cb8-48b4-a218-bd7d4a6fa189_1200x675.png)

我经常在 X 上发布这类 AI 设计演示。每次发出来，总有人问我：“为什么我用 Claude 做出的是那种标准的紫蓝渐变平铺页面，而你却能做出像苹果或 Stripe 级别的设计？”

我用的其实是完全相同的模型，但我从模型里榨出了更多可能性。大多数人用 AI 设计时，只用一条 Prompt 让模型“从零凭空画出设计”，结果往往令人失望。

AI 模型本身蕴含着惊人的创造力，但这种创造力被它们的训练方式压制了。为了安全和泛化，LLM 被训练去预测最合理、最符合大众平均审美的输出。

这让日常 LLM 非常适合写代码、做分析，但却是不合格的设计师。要完成一项设计，LLM 会去抓取训练集里出现最频繁的常见组合——比如紫蓝渐变、居中大字、左文右图。这种结果很安全，但也极其无趣。

优秀的设计刚好相反。设计始于某种情绪，目的是激发情感共鸣。它从不选择最平庸安全的方案，而是寻找最贴切、最能打动人的视觉语言。

只要我们能引导模型跳出最容易预测的惯性选择，就能激活它背后庞大的设计可能性空间。

![](https://substackcdn.com/image/fetch/$s_!ATUP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9eeeb6a-dcce-4cb0-a548-c9c049d560c5_1600x900.png)

这是我在苹果带人类设计团队时学到的教训。在苹果的十多年里，我的绝大多数工作不是自己去设计界面，而是搭建一个系统，让团队能持续产出顶尖成果。

离开苹果后，我一直在把这套工作流应用到 AI 设计中。过去一年里，我总结出一套适合 AI 的三阶段设计体系。

这套体系灵感来自 [Double Diamond 设计模型](https://en.wikipedia.org/wiki/Double_Diamond_(design_process))：

- **探索（Discover）**：通过多方向探索和大胆的视觉尝试，打破 AI 输出“平均平庸废稿”的宿命。
- **定义（Define）**：通过逼迫 AI 跨越熟悉套路、链式调用专业子模型，打造独特的视觉风格与组件语言。
- **交付（Deliver）**：抛弃多余修饰，精细打磨细节，把初稿雕琢成令人惊艳的最终成品。

按照这三个阶段逐步推进，你就能建立起一套可复用的工作流，让 AI 持续输出大师级的设计。

---

# 探索阶段：展开无限可能的空间

设计流程中最难的一步，莫过于面对一张充满无限可能却空无一物的空白画布。

我们都知道，模型极度依赖熟悉套路，习惯做保守的选择。如果你给它的 Prompt 太宽泛（比如“帮我设计一个优雅的待办事项 App”），它只会给你一个随处可见的标准模板。

## 技巧 1：用随机 Seed 注入多样性

这个技巧的核心，是让模型寻找全新的灵感来源，而不是去翻它脑子里最容易调取的那套常用模板。

举个简单的例子，我给 4 个 Claude Code 窗口发送了完全相同的 Prompt：

**Prompt：**
> *帮我给我的效率 App 制作一个落地页（Landing Page）。*

**Claude Opus 5 的输出：**
![](https://substackcdn.com/image/fetch/$s_!lTyI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54f67c3b-bd98-498a-9311-53fdcbf6fe9f_1200x675.png)

几乎每一次，模型给出的都是相同的紫蓝渐变、左侧标题右侧示意图、卡片式布局。

我们没有要求模型做任何独特或有差异化的尝试，它自然就会选择最安全的概率通路。

如果我们要求它“更有创意”会怎样？

**Prompt：**
> *帮我给我的效率 App 制作一个落地页。给我一些完全独特的东西，让每一个设计元素都出人意料。*

**Claude Opus 5 的输出：**
![](https://substackcdn.com/image/fetch/$s_!cBfL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe65ee003-8d06-4bfb-b6fe-2b9eb02b11dd_1200x675.png)

结果和之前有所不同，但依然谈不上丰富。模型依然在使用它习惯的那几套排版规则。

**根本问题在于：模型无法真正做到随机。** 它只能预测概率最高的内容。

为了迫使模型跨越惯性，我们可以引入一个真正的外部随机源，强制模型围绕该随机提示进行构思：

**Prompt：**
> *我想让你帮我给我的效率 App 制作一个落地页。*
> *按照以下步骤执行：*
> 1. *运行 Shell 脚本生成一串长随机字符串。*
> 2. *基于这串随机字符定义视觉方向（配色方案、布局排版、字体风格等）。*
> 3. *发挥你的设计审美把这个视觉方向落地，让它看起来非常高级。*
> 4. *不要在页面上直接展示这个随机字符串，它仅作为你的灵感 Seed。*

**Claude Opus 5 的输出：**
![](https://substackcdn.com/image/fetch/$s_!nrWZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ef0e5a8-2df8-4ec8-b6ff-ea1ef78f0ec9_1200x675.png)

效果立竿见影。生成的页面展现出了截然不同的配色、字体和视觉结构。

## 技巧 2：在 Prompt 中下更狠的视觉指令

另一种强力推模型一把的方法，是在 Prompt 中给出极度具体、甚至看似野蛮的视觉设定。

> *“帮我给我的效率 App 制作一个落地页，采用极具张力的复古像素画风格，带有拟真网格阴影。”*
![](https://substackcdn.com/image/fetch/$s_!KhUV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcfe75e1-5bc4-4dc4-b78f-ef812bf08518_1200x675.png)

> *“帮我给我的效率 App 制作一个落地页，设计成一个等轴测（Isometric）的活体 3D 城市，用户做完任务后城市建筑物会发生变化。”*
![](https://substackcdn.com/image/fetch/$s_!OSVS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6eeb536-a19f-4318-ab93-1b919d713c7c_1200x675.png)

> *“帮我给我的效率 App 制作一个落地页，采用打破常规的极度非对称布局，展示杂乱中的秩序感。”*
![](https://substackcdn.com/image/fetch/$s_!ycYL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67aa79aa-cebe-4700-880a-9d665f80f1cb_1200x675.png)

当然，最难的部分往往是想出那些原创的视觉点子。这一点 AI 同样可以帮你：

#### 1. 让 AI 列出大量简略的想法，故意不加细节，目的仅在于激活你的想象力。

> *我想为我的产品建立一套大胆、独特的设计语言。你能列出尽可能多的视觉构想吗？要求涵盖不同的时代背景、工业领域和艺术流派。*
![](https://substackcdn.com/image/fetch/$s_!fvto!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62bbabfe-2ed8-47ac-a169-be5ecbdc5bd6_1200x675.png)

#### 2. 将你最喜欢的方向可视化，记录你对不同视觉尝试的真实反应，然后让 AI 精修。

> *工业控制面板方向：*
> - *我想要一种实体触感，就像有机械按压感的按钮、清脆的回馈和音效。*
> - *我一开始脑子里想的是卡通拟物化（Skeuomorphic），但又觉得容易显得俗气。要避开拟物化的老套做法。*
> - *相反，我想要统一的组件感和精致的小细节，既能体现这种工业质感，又不会显得用力过猛。*
> - *纯灰色渐变会很枯燥，需要更多材质纹理。也许可以融入一些点缀色彩。*
> *你能根据我的个人偏好，进一步打磨这个方向吗？*
![](https://substackcdn.com/image/fetch/$s_!Pppd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F205f15d8-e766-4ed0-9494-0cfd80aeed87_1200x675.png)

#### 3. 持续迭代直到满意，然后让 AI 撰写最终用以构建原型的 Prompt。

> *你能写一条精炼的 Prompt，让 AI Agent 能直接用来构建初始原型页面吗？*
![](https://substackcdn.com/image/fetch/$s_!AVWS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe65824c9-c146-4dc4-b7be-b2fcfd6b2c28_1200x675.png)

如果你只是把 AI 生成的点子直接原封不动贴回给 AI，很难做出真正独特的东西。加入了你的直觉、审美与判断之后，AI 才能真正为你所用。

不要害怕尝试那些听起来疯狂甚至怪异的想法。当你觉得“这不可能做出来吧”的时候，往往正是突破平庸的开始。

---

# 定义阶段：深化你的视觉方向

到目前为止，我们讨论了如何在大范围的想法中探索，并锁定一个有潜力的方向。

看看我们之前用随机 Seed 跑出来的那些设计：
![](https://substackcdn.com/image/fetch/$s_!nrWZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ef0e5a8-2df8-4ec8-b6ff-ea1ef78f0ec9_1200x675.png)

这些设计很有潜力，但它们依旧夹杂着旧套路的影子：文字左对齐、右侧放卡片、标准导航栏。

下一步的目标，是赋予每个设计独特的视觉灵魂，通过清晰的视觉决策打破陈规。

## 技巧 3：用 Subagent 打造正向反馈闭环

我们需要对设计进行持续迭代。但是，如果只是简单地让代码 Agent“看看截图然后修改”，Agent 往往很难发现自身代码的问题，或者稍微改动两下就草草收工。

解决办法是：不要让写代码的 Agent 自己判断设计的好坏，而是引入一个独立的评审子模型（Critic Subagent），形成“代码生成 - 独立评审 - 重新迭代”的正向闭环。

这种做法还有一个额外的好处：我们可以把昂贵的高阶模型专门用来做评审，而让更快速的写代码 Agent 执行具体修改。

我们在之前的设计上尝试这套流程，使用 Claude Fable 5 作为评审员：

**Prompt：**
> *我想让你改进这个设计。为了确定修改重点，每次修改时调用 Fable 5 子模型作为评审员。*
> *在每次迭代中遵循以下流程：*
> 1. *截取当前设计的网页截图。*
> 2. *在一个全新的上下文窗口中调用评审员，只给它看截图，不提供代码或实现细节。*
> 3. *要求评审员评估当前视觉风格，想象顶级设计工作室会如何呈现，并列出差距。*
> 4. *最后，让评审员给出一个 1-10 的评分，表明当前设计距离目标有多近。*
> *在评审员 Prompt 中加入以下要求：*
> - *从整体结构布局到细微组件，进行全面宏观与微观审查。*
> - *警惕那些看起来泛滥、多余或明显带有 AI 废稿味道的套路。*
> - *给出精准、具体的修改建议，拒绝含糊其词的套话。*
> - *保持大胆有主见的审美品味，不要给安全保守的方案。*
> *只有当评审员独立打出 9/10 分以上时，你的工作才算完成。未达标前请持续迭代代码。*

**Claude Opus 5 的输出：**
![](https://substackcdn.com/image/fetch/$s_!nik4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5bc2f19-9aa0-4fd2-a7d1-cf37a6b8ef99_1200x675.png)

不再是那些干瘪重复的模版，每一个设计都展现出了极其鲜明的视觉个性。

值得注意的是，在整个过程中，Fable 5 的 Token 消耗不到总数的 10%。把高阶模型作为精准的评价中枢，是极其高效且省钱的策略。

设置闭环反馈时，有几个关键细节：

- **确保评审标准尽可能清晰客观。**
  - 差的示范：“评价我们的设计是否好看、是否有 AI 味。”（太主观，模型无法给出精准建议）
  - 好的示范：“审查我们要达到的视觉风格，想象顶级设计工作室会如何呈现，给出差距与 1-10 分评分。”
  - 卓越示范：“这里有 5 张设计图：4 张是顶级同行案例，1 张是我们产品的截图。将我们的截图混入其中，排序并给出打分理由。”
- **提供参考图片作为质量标杆。** 你可以使用相似产品的优秀截图，或者网上找的视觉参考图。
- **谨慎设置终止条件。** 否则评审员可能会陷入无限死循环，要求永远无法满足。
- **因地制宜选择模型。** 评审员适合用推理和视觉能力更强的模型，而代码生成可以使用速度更快、成本更低的模型。

## 技巧 4：结合生图模型丰富视觉细节

写代码的 AI 喜欢纯代码构件，往往很少主动使用图片。它们倾向于用简单的 CSS 渐变或通用图标来糊弄。

有些 Agent 内置了生图工具但很少调用，有些则完全没有生图能力。我们可以显式要求 Agent 结合生图 API 来丰富设计。

我们在上一阶段的设计上试试：

**Prompt：**
> *目前的设计显得过于平淡。请调用生图能力为其注入更多视觉个性。可以考虑 Shader 材质、3D 视觉元素或局部纹理。*
> *生图请使用这个 OpenAI API Key（仅在本地调用，不要写入代码库）。*
> *在浏览器中逐帧验证输出的视觉质量。*

**Claude Opus 5 效果对比（修改前与修改后）：**
![](https://substackcdn.com/image/fetch/$s_!kEu8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F624f2b18-b223-4df4-aa6c-5e4df2f2a74c_1200x675.png)

注入图像和材质效果后，页面迅速脱离了干瘪的代码感，视觉层次大幅提升。

根据你的工具链，有几种方式可以让 Agent 具备生图能力：

- **如果你使用 Codex、Antigravity 或 Grok Build：** 直接让 Agent 调用其内置的生图能力即可。
- **如果你使用 Claude Code 等 Agent 且拥有 ChatGPT 订阅：** 告诉 Agent：“使用 Codex CLI 来生成图片，如果未安装请帮我配置。”
- **如果你只用纯 Claude 或其他终端工具：** 最直接的方式是提供一个 OpenAI 或 Gemini 的 API Key，让 Agent 在后台运行 Python 脚本生成图片。

## 技巧 5：引入生视频模型实现高级动效

现在的生视频模型能力非常惊人，但大多数人只把它们当作艺术创作工具，忽视了它们在界面交互中的潜力。

市面上有不少出色的视频模型。我习惯通过统一 API 平台（如 fal.ai）调用这些模型。

我最常在设计中使用视频模型的两种方式：

#### 1. 打造惊艳的动态视觉元素

技巧在于生成带有纯色背景的循环视频片段，然后通过抠图或 CSS 混合模式（Mix-blend-mode）透明化处理，嵌入到网页中。

例如，我在之前的设计上运行了这个 Prompt：

**Prompt：**
> *你能把页面上的静态图片替换为循环视频片段吗？要求体现玻璃折射与光影流动感。*
> *为了获得逼真的玻璃折射效果，让玻璃视频叠加在网页背景上方渲染。*
> *使用这个 fal.ai Key：sk-a1b2c3d4…*
> *自动寻找合适的视频生成与背景抠图模型。*

**GPT-5.6 Sol 效果对比：**
![](https://substackcdn.com/image/fetch/$s_!SAf-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54f67c3b-bd98-498a-9311-53fdcbf6fe9f_1200x675.png)

这种物理级别的光影流转与折射效果，是纯代码很难达到的质感。

#### 2. 打造流畅的状态过渡动效

这是视频模型被严重低估的应用场景。除了文本生视频外，我们还可以指定“首帧”和“尾帧”，让视频模型生成两者之间极其自然的物理过渡动画。

这是一个展示行李箱视效的 Demo 页，我只用一条 Prompt 让 GPT-5.6 Sol 生成：

**Prompt：**
> *制作一个行李箱的 Demo 展示页，使用视频模型制作交互式滚动过渡动画：*
> - *初始状态：行李箱悬浮在空中。*
> - *随滚动降落：行李箱平稳落到地面并自动弹开。*
> - *收尾状态：收纳物品整齐地从上方落入行李箱中。*
> *使用你的生图能力生成初始帧，然后使用视频模型生成状态过渡片段。*
> *使用 Key：sk-a1b2c3d4…*
> *挑选具备强物理引擎和一致性的视频模型（如 Seedance 2.5）。*

**GPT-5.6 Sol 的输出：**
![](https://substackcdn.com/image/fetch/$s_!E1CZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ef0e5a8-2df8-4ec8-b6ff-ea1ef78f0ec9_1200x675.png)

随着用户的滚动，不同状态之间的过渡动画极其平滑自然，交互体验非常出色。

---

# 交付阶段：精雕细琢，将设计打磨成精品

当我们探索出了独特方向并深化了视觉风格后，最后一步就是精简修饰、去除毛刺，让设计达到商业发行的标准。

## 技巧 6：果断做减法，裁掉无价值元素

AI 极度喜欢在页面上不断堆砌元素，但几乎从不主动做减法。设计充斥着 AI 味的最显著特征，就是各种毫无意义的修饰、装饰性阴影和多余的包裹框。

在精修 AI 设计时，我的大部分精力都花在删除东西上。例如，在我开发卡路里追踪 App 的初始版本时：

我向 AI 描述了功能，并明确要求“干净、极简的设计”：

AI 却塞进来一堆多余的修饰：
- 背景和进度条上发光的粉色荧光效果
- 标题文字上莫名其妙的渐变配色
- 在展示每日食物时加了一堆花哨的标签和留白，而原本的图片其实已经足够直观
- 臃肿的自定义按钮，比 iOS 原生控件难看得多

我让 Claude 重新做减法：
- 将布局简化为以图片为核心的网格
- 砍掉所有发光渐变、荧光效果和多余的容器框
- 追求极致的极简主义，让它看起来像是苹果原生的应用

**最终效果：**
![](https://substackcdn.com/image/fetch/$s_!iD6y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb346747b-1cb8-48b4-a218-bd7d4a6fa189_1200x675.png)

在我看来，这个版本比之前高级得多。它足够克制，把视觉焦点完整地留给了内容本身。

今天的 AI 模型永远不会主动做出这种决定。记住，AI 并不懂得少即是多——这需要你作为人类设计师去行使最终的审美裁决权。

## 技巧 7：全面清除 AI 味指纹

在最后交付前，使用自动化检测规则对全篇设计和代码文本进行扫描，彻底清除所有的“AI 味”套路（包含冗余形容词、呆板的排版、无意义的渐变）。只有剔除这些机械痕迹，设计才能真正展现出大师级的活人感与高级质感。
