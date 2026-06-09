# 1. 执行摘要

我把这次调研拆成三条线：检测理论、中文写作问题、Skill 产品化。结论很明确：一个好的中文“去 AI 味”Skill，不应该是“绕过检测器”的工具，也不应该是“把文字改口语”的滤镜。它应该是一个**中文编辑诊断器 + 体裁化改写器 + 作者声音校准器 + 事实风险守门员**。

AI 文本检测本身并不稳。OpenAI 早期 AI 文本分类器已因准确率低下线，官方评估里只识别出 26% 的 AI 文本，同时有 9% 的人类文本被误判；OpenAI 也明确说分类器不应作为主要决策工具，短文本、非英语、可预测文本、被编辑文本都容易出问题。([OpenAI][1]) Turnitin 和 GPTZero 这类商业工具也把结果定位为“辅助判断”，不是定罪证据；Turnitin 截至 2026 年 6 月的 FAQ 还明确说其 AI 写作检测支持长篇英文、西班牙文、日文，不支持中文。([guides.turnitin.com][2])

中文去 AI 味的核心不在“替换词”。中文 AI 味最明显的地方通常是：空泛升维、宏大判断无证据、公文腔、营销腔、翻译腔、连接词堆叠、假平衡、强行递进、抽象商业词、伪权威归因、没有具体场景、没有作者视角、段落结构过于完整、结尾总是上价值。

Humanizer-zh 有参考价值，但它更像一个英文 humanizer 的中文翻译版。它的 README 明确说明核心文件翻译自 `blader/humanizer`，规则和评分参考 `stop-slop`，原始来源是 Wikipedia 的 “Signs of AI writing”。([GitHub][3]) 它的优点是把 24 类 AI 写作痕迹做成可执行清单；短板是中文本土问题覆盖不足，且部分规则仍是英文语境直译，比如 `-ing` 结尾、Title Case、破折号、弯引号等。([GitHub][3])

我要做的 Skill 应该超过 Humanizer-zh 的地方有五个：**中文 AI 味分类体系、体裁策略、作者声音校准、事实安全、自检评分**。它不只删“此外、至关重要、深入探讨”，而要判断这段话为什么空、空在哪里、缺什么证据、该按哪个体裁重写、哪些内容不能擅自补。

---

# 2. 关键结论

| 结论                                                            | 证据类型        | 依据                                                                                                       |
| ------------------------------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------- |
| AI 文本检测是概率判断，不适合作为唯一依据                                        | 研究 + 官方说明   | OpenAI 分类器下线；Turnitin/GPTZero 都强调非最终裁决。([OpenAI][1])                                                     |
| Perplexity、burstiness、token distribution 能解释部分 AI 味，但不能等同“人味” | 研究支持        | DetectGPT、Fast-DetectGPT、Turnitin 的词概率序列说明都基于模型生成分布差异。([arXiv][4])                                       |
| 改写、释义、对抗性 paraphrasing 会显著削弱检测器                               | 研究支持        | DIPPER、Sadasivan 等研究显示 paraphrasing 能让检测器和水印失效或大幅降效。([arXiv][5])                                         |
| “降低检测分”不等于“写得好”                                               | 研究推断 + 项目实践 | 对抗 paraphrasing 研究目标是逃避检测，不是提升中文编辑质量。([arXiv][6])                                                        |
| 中文检测已有 HC3、LLM-Detector、C-ReD、NLPCC 相关工作，但中文体裁、地域、混合写作仍不足     | 研究支持        | HC3-Chinese 覆盖问答、百科、医疗、金融、心理、法律等；LLM-Detector 关注中文文档级和句子级检测；C-ReD 2026 针对真实提示和中文 benchmark。([GitHub][7]) |
| 中文 AI 味不能照搬英文 tells                                           | 我的推断 + 项目对比 | Humanizer-zh 的中文适配主要是示例和表达调整，仍保留英文语境特征；中文更需要处理公文腔、商业黑话、宣传式套话和语体错配。([GitHub][3])                          |
| 最好的中文 humanizer 应该先诊断，再改写，再自检                                 | 产品设计推断      | 上游 blader/humanizer 已加入 voice calibration、二次审稿；stop-slop 用短规则和 reference 文件支持渐进加载。([GitHub][8])          |

---

# 3. 现有理论综述

## 3.1 AI 文本检测的理论基础

**Perplexity。**
Perplexity 可以理解成“某个语言模型读到这段文本时有多意外”。LLM 生成文本往往更贴近高概率词序列，句子更平滑、可预测；人类文本可能更跳、更局部、更不稳定。但这不是铁律。法律条文、说明书、模板邮件、学生作文、二语写作、新闻通稿，也可能非常可预测。Turnitin 对外解释其检测模型时，也强调 LLM 倾向于持续选择高概率词序列，而人类写作更不一致、更有个人习惯。([guides.turnitin.com][2])

**Burstiness。**
Burstiness 指句子之间的变化幅度：长短、复杂度、信息密度、转折方式是否有波动。AI 草稿常见问题是“每段都很完整，每句都差不多长，每个段落都用同样逻辑推进”。但 burstiness 也不能直接当人类指标，因为优秀学术摘要、产品文档、法规说明本来就会压低节奏波动。

**Stylometry。**
Stylometry 研究作者风格的可量化特征，比如词汇偏好、标点、句法、功能词、段落长度、搭配习惯。新的检测研究仍在利用风格差异解释 LLM 文本与人类文本的差别，例如 StyleDecipher 用离散风格指标和连续风格表示来做更可解释的检测，并关注跨域和混合人机写作。([arXiv][9]) 但 stylometry 的问题是：体裁、主题、平台、编辑流程会强烈影响风格。公众号、招股书、政府通报、知乎回答、学术摘要不应使用同一套“人味”指标。

**Token distribution / GLTR 类方法。**
这类方法看 token 是否集中在高概率区间。早期检测常用“AI 写得太顺”这个信号。但随着模型变强、采样策略变化、用户多轮修改、LLM 之间风格趋同，这个信号越来越脆弱。MGTBench 这类 benchmark 也显示，随机空格、释义、对抗扰动会显著削弱检测有效性。([arXiv][10])

**Sentence-level detection。**
句子级检测适合找“哪几句像 AI”，但它更难，因为单句短、上下文少，尤其在人机混写、人工润色、段落内来回切换作者时，风格信号很弱。CoAuthor 相关研究指出，人机混合文本中的句子级检测困难来自人类编辑、频繁作者切换和短片段风格线索不足。([arXiv][11])

**Document-level detection。**
文档级检测利用整篇文本的统计模式，通常比单句稳，但会掩盖局部问题。Turnitin 的做法是把文章切成几百词片段，重叠处理，再给句子 0 到 1 的分数，最后聚合为整体预测。([guides.turnitin.com][2]) 对中文 Skill 来说，文档级诊断应该用来判断“整体语体是否像 AI”，句子级诊断用来标出具体可改处。

**Watermarking。**
水印不是风格检测，而是在生成阶段改变 token 概率，让输出带有可检测模式。Kirchenbauer 等人的 LLM watermark 是典型代表；Google DeepMind 的 SynthID for text 也说明，它通过在生成时调制 token 概率来嵌入不可感知水印。([arXiv][12]) 但 SynthID 官方也说，它在长而多样的文本上更有效，能承受少量修改和轻度释义；如果文本被彻底重写或翻译，置信度会显著下降；事实性短回答也不适合水印，因为可选 token 空间小。([Google DeepMind][13])

## 3.2 中文 AI 文本检测相关研究

**HC3 / HC3-Chinese。**
HC3 是较早的人类-ChatGPT 对比语料，包含英文和中文。项目仓库说明 HC3-Chinese 覆盖 open QA、百科、NLPCC-DBQA、医疗、金融、心理、法律等来源，并提供中英文检测器，包括问答版、单文本版、语言学特征版；中文模型基于 `hfl/chinese-roberta-wwm-ext`。([GitHub][7])

**LLM-Detector。**
LLM-Detector 收集中文人类专家文本和 9 类 LLM 生成文本，并构造了“人类写作句子 + LLM 润色句子”的混合数据，目标同时覆盖文档级和句子级检测。论文指出，传统 BERT/RoBERTa 类检测器容易在域内过拟合，句子级和域外检测表现差；指令微调的开源 LLM 检测器泛化更好。([arXiv][14])

**C-ReD。**
C-ReD 是 2026 年提交的中文真实提示 AI 生成文本检测 benchmark，目标是缓解中文语料里模型多样性不足、数据同质化、真实提示不足等问题。arXiv 摘要声称它支持域内检测、未见 LLM 泛化和外部中文数据泛化；但对应 GitHub 仓库截至我查看时仍显示 “Coming soon”，说明数据和代码可用性还要继续跟进。([arXiv][15])

**NLPCC 2025 相关中文检测。**
2025、2026 年已经有多篇围绕 NLPCC 2025 Chinese AI-Generated Text Detection Task 的研究。比如 Qwen2.5-7B LoRA 检测研究指出，encoder 模型可能接近记住训练数据但遇到分布迁移性能下降，而 LoRA 适配的 Qwen2.5-7B 在测试集上达到较高准确率。([arXiv][16]) EnsemJudge 则用多模型集成和投票机制提升中文检测可靠性，并报告在 NLPCC2025 Shared Task 1 中取得第一。([arXiv][17])

**中文诗歌检测。**
现代中文诗歌 benchmark 很有启发。研究构造了 800 首专业诗人作品和 41,600 首 LLM 生成诗，发现现有检测器不能可靠识别现代中文诗，最难检测的是“内在质量”，尤其是风格。([arXiv][18]) 这说明：越是体裁强、作者性强、审美判断强的中文文本，越不能靠简单检测分数判断。

## 3.3 语言差异：中文、英文、日文

英文检测中的很多表层特征不能直接搬到中文：

中文没有英文那种显式空格分词，tokenization 更依赖模型；英文里的 Title Case、hyphenated word pairs、curly quotes、`-ing` 结尾，在中文里不是核心问题。Humanizer-zh 也承认中文适配时只处理了“某些英文模式在中文中表现不同，如标题大小写问题”、添加中文示例、调整表达。([GitHub][3])

日文和中文都存在无空格书写、汉字混用、敬体/常体、体裁语气强约束等问题，但日文有更明显的敬语系统和文末形态；中文则更容易被“抽象名词 + 四字格 + 公文动词 + 宏大判断”污染。Turnitin 当前支持英文、西班牙文、日文检测，不支持中文，这也说明商业检测体系对不同语言的覆盖并不均衡。([guides.turnitin.com][2])

## 3.4 AI humanization / paraphrasing / adversarial rewriting

研究层面已经证明，paraphrasing 是检测器的弱点。DIPPER 论文显示，释义模型能规避水印、GPTZero、DetectGPT、OpenAI classifier 等检测器，DetectGPT 在固定 1% FPR 条件下的检测准确率从 70.3% 掉到 4.6%。([arXiv][5]) Sadasivan 等人的理论和实验也指出，递归释义会降低检测效果，水印可能被 spoof，且当机器文本分布接近人类文本分布时，检测上限会受到总变差距离限制。([arXiv][19])

近年的 AuthorMist、Adversarial Paraphrasing、StealthRL 等工作更进一步，把外部检测器当奖励信号，专门训练或引导改写器绕过检测器。([arXiv][20]) 这些研究对产品设计的启发不是“照着做”，而是提醒我们：**检测分数可以被优化，但优化检测分数不等于优化写作质量。**

---

# 4. 中文 AI 味的核心机制

中文 AI 味通常来自六个机制。

**第一，安全平均化。**
模型倾向于给出最稳、最不冒犯、适合最多场景的话，于是出现“具有重要意义”“提供有力支撑”“未来值得期待”这类安全句。它们不一定错，但往往不承担信息。

**第二，证据不足时自动升维。**
当输入缺少事实，模型会用“趋势、生态、价值、意义、赋能、闭环”填空。中文里这会非常像公文、品牌稿或咨询报告的低密度版本。

**第三，结构过度完整。**
真实作者常常从一个具体问题切入，段落会有轻重缓急。AI 草稿喜欢“背景—问题—方案—意义—展望”，每段都像小论文，结尾还要上价值。

**第四，连接词替代逻辑。**
“此外、同时、值得注意的是、从这个角度看、进一步而言”会让文本看起来有逻辑，但这些词经常只是把空句黏在一起。

**第五，缺少作者位置。**
人类作者通常知道自己为什么写、写给谁、站在哪个位置写。AI 草稿常常像“没有责任主体的旁白”：不说明谁观察、谁判断、谁受影响、判断来自哪里。

**第六，语体错配。**
官网文案写成公文，技术文档写成品牌稿，申请文书写成公众号，知乎回答写成咨询报告，小红书写成新闻通稿。中文读者对语体错配很敏感，哪怕句子都通顺，也会觉得“不是人写的”。

---

# 5. Humanizer-zh 项目分析

## 5.1 核心思路

Humanizer-zh 是一个 Claude Code Skill，目标是“去除文本中的 AI 生成痕迹”。它的 `SKILL.md` 任务流程是：识别 AI 模式、重写问题片段、保留含义、维持语调、注入灵魂。核心规则包括删除填充短语、打破公式结构、变化节奏、信任读者、删除金句。([GitHub][21])

它列出 24 种模式：过度强调意义、知名度、宣传语言、模糊归因、挑战与未来展望、AI 高频词、系动词回避、否定式排比、三段式、同义词循环、虚假范围、破折号、粗体、标题大写、表情符号、知识截止免责声明、谄媚语气、过度限定、通用积极结论等。([GitHub][3])

## 5.2 它继承了哪些英文项目思想

Humanizer-zh 明确说明核心文件翻译自 `blader/humanizer`，实用工具参考 `hardikpandya/stop-slop`。([GitHub][3])

`blader/humanizer` 的新版已经发展到 33 个模式，并加入 voice calibration：用户可以提供 2–3 段自己的写作样本，Skill 分析句子节奏、词汇选择、个人习惯，再应用到改写中。([GitHub][8]) 它还在版本史里记录了新增二次审稿、voice calibration、被动/无主语片段、说服性框架、signposting、制造金句等模式。([GitHub][8])

`stop-slop` 的贡献是更产品化：它把规则拆成 `SKILL.md`、`references/phrases.md`、`references/structures.md`、`references/examples.md`，用短规则控制输出，再按需加载 reference。它关注 predictable phrases、structures、rhythms，并用 Directness、Rhythm、Trust、Authenticity、Density 五个维度评分。([GitHub][22])

## 5.3 它对中文做了哪些适配

它做了三类适配：翻译规则名、加入中文示例、调整部分表达。README 也明确说中文语境特殊性主要体现在：某些英文模式在中文中表现不同、添加中文示例、调整表达。([GitHub][3])

问题是，这些适配还不够。它没有建立中文本土分类体系，也没有把“公文腔、营销腔、翻译腔、伪权威、中文商业黑话、套话式结尾、四字格滥用、语体错配”作为一级问题。

## 5.4 优点

**一，它把 AI 味变成了可执行 checklist。**
很多人说“这段有 AI 味”，但说不出哪里有。Humanizer-zh 至少能把问题拆成模式。

**二，它强调保留含义和维持语调。**
这比“随便改得口语一点”好。它的流程要求核心信息完整，并按正式、随意、技术等语气匹配。([GitHub][21])

**三，它有质量评分。**
直接性、节奏、信任度、真实性、精炼度这五个维度有实用价值。([GitHub][21])

**四，它知道“模糊归因”和“通用积极结论”很危险。**
例如把“行业专家认为”改成具体来源，或直接删除空泛结尾，这是中文里也有效的编辑策略。([GitHub][21])

## 5.5 缺点

**一，英文规则残留明显。**
`-ing` 结尾、Title Case、curly quotes、em dash 是英文文本痕迹，在中文里不是主战场。中文更常见的是“不断推进、持续赋能、深度融合、有效提升、具有重要意义”。

**二，“注入灵魂”容易误导。**
Humanizer-zh 鼓励观点、第一人称、一些混乱、复杂感受。这个策略适合博客、评论、个人写作，但不适合技术文档、法律文本、学术摘要、产品帮助文档。上游新版 blader/humanizer 其实已经加了限制：百科、技术、法律、参考文本里，中立朴素就是正确的人类声音，不要强行加观点或第一人称。([GitHub][23])

**三，示例有“擅自补事实”的风险。**
Humanizer-zh 完整示例里，原文只说“软件更新提供无缝、直观、强大的体验”，改写后变成“添加了批处理、键盘快捷键和离线模式”“测试用户反馈积极”。这些信息原文没有提供。([GitHub][21]) 对一个产品化 Skill 来说，这是严重问题：去 AI 味不能靠编事实。

**四，缺少作者声音校准。**
它没有继承上游新版 voice calibration 的完整机制。对中文来说，作者声音尤其重要：有人写得克制，有人写得锋利，有人偏书面，有人偏口语，有人喜欢短句，有人喜欢长句。如果 Skill 不建模作者声音，就容易输出“统一的自然感”。

**五，缺少体裁策略。**
同一句“不要空泛”在投融资材料、官网文案、知乎回答、技术博客、申请文书里做法完全不同。Humanizer-zh 目前没有细分体裁。

## 5.6 哪些规则对中文真的有效

有效的规则：

* 删除“意义、格局、关键作用、重要一步”这类无证据升维。
* 把“专家认为、数据显示、业内人士指出”改为具体来源，或标注“需补来源”。
* 把“无缝、直观、强大”改为具体功能或具体体验。
* 删除多余连接词。
* 减少机械三段式。
* 避免“这不仅仅是……更是……”。
* 结尾停止“展望未来”，改成交代下一步事实。

## 5.7 哪些规则像英文直译，不适合直接用于中文

不适合直接照搬的规则：

* `-ing` 结尾：中文没有对应形态，应该替换成“空泛补充状语 / 以彰显、体现、确保、推动结尾”。
* Title Case：中文标题大小写不存在，应改为“标题党式并列名词 / 咨询报告式标题”。
* Curly quotes：中文里不构成常见 AI 味。
* Em dash：中文破折号可疑度低于英文，真正问题是“破折号后面塞金句”。
* “不要被动语态”：中文常省略主语，无主句不一定糟。真正要查的是“责任主体缺失”，如“问题得到解决”“能力持续提升”，但不知道谁做了什么。
* “删所有副词”：中文里的“其实、可能、比较、基本、稍微、已经”有时是语气精度，不应一刀切。

## 5.8 如果做更好的 Skill，应超越它的方向

1. 建中文本土 AI 味 taxonomy。
2. 加体裁判断和体裁 playbook。
3. 加作者声音校准。
4. 默认不新增事实；缺事实时用 `[需补充：具体数据/案例/来源]`。
5. 先诊断，再改写，再自检。
6. 输出不要过长，默认给一个可发布版本。
7. 用 quality rubric 而不是检测器分数。
8. 对“请帮我绕过检测器”明确拒绝或转为“提升真实写作质量”。

---

# 6. 成功方法

## 方法 1：把宏大判断改成可验证事实

**为什么有效：**
AI 味常来自“判断大于证据”。把“具有重要意义”改成“谁在什么场景下解决了什么问题”，会立刻降低空泛感。

**适用体裁：** 产品介绍、行业分析、技术博客、投融资材料、新闻评论。

**例子：**

AI 味原文：

> 这款协作平台通过深度融合 AI 能力，持续赋能企业数字化转型，为组织效率提升和业务创新注入新动能。

失败改写：

> 说实话，这个平台真的挺好用，可以帮企业少走弯路，也能让大家工作更轻松。

成功改写：

> 这款协作平台主要解决三件事：任务分散在聊天软件里、审批进度没人跟、会议纪要没人整理。AI 功能目前只放在两个环节：自动生成会议纪要，提醒负责人补齐下一步动作。它不是“数字化转型引擎”，更像一个减少漏事的工作台。

成功点：删除“深度融合、赋能、新动能”，补成任务、审批、纪要这些具体场景。失败版只是换成口语，没有增加信息。

## 方法 2：把伪权威改成明确来源，没来源就标风险

AI 味原文：

> 多位行业专家认为，生成式 AI 将成为未来企业竞争的关键变量。

失败改写：

> 很多人都觉得 AI 以后会非常重要。

成功改写：

> 这句话需要来源。可以改成两种：
> 有来源版：`麦肯锡在 2023 年报告中估算，生成式 AI 每年可能带来 2.6 万亿至 4.4 万亿美元的经济价值。`
> 无来源版：`至少在客服、代码生成和内容生产这几个环节，生成式 AI 已经开始改变企业的成本结构。`

成功点：不冒充“专家认为”。没有来源就缩小判断范围。

## 方法 3：保留体裁，不乱加人味

AI 味原文，技术文档：

> 本功能旨在为用户提供更加便捷、高效和智能化的配置体验，帮助用户在复杂业务场景下快速完成相关操作。

失败改写：

> 这个功能说白了就是让你别被配置折磨，点几下就能搞定。

成功改写：

> 这个功能用于批量创建配置项。用户上传 CSV 后，系统会校验字段、显示错误行，并在确认后一次性写入配置中心。

成功点：技术文档的人味不是“口语”，而是清楚、准确、可操作。

## 方法 4：用作者位置替代安全中立腔

AI 味原文，知乎回答：

> 对于是否转行产品经理这一问题，需要从个人兴趣、能力结构、行业趋势和职业发展空间等多个维度综合判断。

失败改写：

> 我觉得转不转产品经理这事吧，还是看你自己。

成功改写：

> 我不建议只因为“产品经理门槛低”就转。这个岗位最消耗人的地方不是画原型，而是每天处理不完整的信息：老板一句方向、研发一句排期、销售一个临时客户需求。你如果讨厌反复沟通，转过去大概率更痛苦。

成功点：有判断、有场景、有取舍，不靠“多个维度综合判断”。

## 方法 5：改结构，而不是只改句子

AI 味原文：

> 随着人工智能技术的快速发展，越来越多企业开始关注 AI 在客户服务领域的应用。一方面，AI 可以提升服务效率；另一方面，AI 也可以降低运营成本。因此，AI 客服具有广阔的发展前景。

成功改写：

> 客服团队最先愿意用 AI，不是因为它“先进”，而是因为夜间、节假日和高峰期的问题太重复。订单状态、退款进度、发票抬头，这些问题不该一直占人工坐席。真正难的是边界：什么时候转人工、怎么记录上下文、出了错谁负责。AI 客服能不能省钱，最后取决于这些细节。

成功点：结构从模板三段式变成真实问题链：为什么用、能解决什么、难点在哪、判断条件是什么。

---

# 7. 失败方法

## 7.1 简单同义词替换

“重要意义”换成“重大价值”，“助力”换成“帮助”，“赋能”换成“加持”，没有用。AI 味不是单个词的问题，而是“词承担了本该由事实承担的工作”。

## 7.2 强行口语化

正式文本不能都改成“说白了、其实吧、挺、蛮、真的”。官网文案、学术摘要、产品文档、商务邮件需要的是清楚，不是聊天。

## 7.3 故意加入错别字

错别字只能降低专业性，不能增加真实感。真实作者可能犯错，但产品化 Skill 不应故意制造错误。

## 7.4 加入虚假个人感

“我觉得、说实话、老实讲、让我震惊的是”如果没有真实立场和经验，只会变成另一种 AI 腔。尤其中文社媒已经被这类假亲密污染。

## 7.5 过度缩短句子

短句不是人味。连续短句会变成“制造金句”：

> 很难。也很真实。这就是问题。

这种写法在 stop-slop 里也被视为 dramatic fragmentation。([GitHub][24])

## 7.6 为了绕过检测器牺牲事实准确性

这是最危险的失败。OpenAI、Turnitin、GPTZero 都提醒检测结果有局限，不能把检测分当最终判断。([OpenAI][1]) Skill 的目标应该是可发布质量，不是检测器分数。

## 7.7 把正式文本改成社媒口吻

例如把投融资材料改成“小红书口吻”，会损害可信度。不同体裁的人味不同：投融资材料的人味是数字、假设、风险边界；小红书的人味是体验、细节、具体对象；技术文档的人味是准确和可操作。

## 7.8 用检测器分数替代编辑质量

检测器可以作为风险提示，但不能决定文本好坏。GPTZero 自己也说 AI detection 最适合长英文 prose，且不应作为 final verdict。([GPTZero][25]) 中文 Skill 更不应该围绕检测器优化。

---

# 8. 中文 AI 味分类体系

下面这套分类不是英文 tells 的直译，而是面向中文写作的产品化诊断表。

| 类型       | 定义 / 典型句式                 | 为什么像 AI        | 体裁例外           | 推荐编辑策略             | 错误编辑策略        | 示例                               |
| -------- | ------------------------- | -------------- | -------------- | ------------------ | ------------- | -------------------------------- |
| 空泛升维     | “这不仅是工具，更是……”“标志着……新阶段”   | 用价值判断替代事实      | 品牌宣言、演讲稿可少量使用  | 降到具体对象、具体动作        | 换成更华丽的抽象词     | “不仅是工具”→“主要解决审批追踪和纪要整理”          |
| 宏大但无证据判断 | “将深刻改变行业格局”               | 判断范围过大，无来源     | 行业报告摘要可保留但需数据  | 缩小范围或补来源           | 加“可能、或许”糊弄    | “改变行业”→“先影响客服和内容生产”              |
| 机械三段式    | “首先/其次/最后”“一方面/另一方面/因此”   | 像模板自动展开        | 教材、考试答案        | 改成问题链或场景链          | 把连接词换一批       | “一方面提效，另一方面降本”→“高峰期重复问题先被自动化”    |
| 公文腔      | “扎实推进、持续深化、取得积极成效”        | 主体模糊，动作抽象      | 政府公文、正式通报      | 明确谁做了什么、结果如何       | 强行口语化         | “扎实推进流程优化”→“财务部把报销审批从 5 步减到 3 步” |
| 营销腔      | “极致体验、无缝连接、全新升级”          | 形容词多，证据少       | 广告 slogan      | 改成功能、场景、限制         | 加更多情绪词        | “无缝体验”→“切换设备后保留编辑进度”             |
| 翻译腔      | “进行一个……”“在……方面起到作用”       | 结构像英文直译        | 翻译稿初稿          | 改成中文自然动词           | 全部改口语         | “进行优化”→“优化”                      |
| 连接词堆叠    | “此外、同时、值得注意的是、进一步而言”      | 用连接词制造逻辑感      | 学术综述可少量使用      | 删除，靠内容自然推进         | 换成“另外、并且”     | “此外，该功能还……”→“该功能还……”             |
| 安全中立腔    | “需要综合判断”“各有优劣”            | 回避判断，像客服回答     | 风险提示、法律建议      | 给条件化判断             | 强行激烈表态        | “需要综合判断”→“预算低于 X 时不建议上”          |
| 假平衡      | “一方面……另一方面……”             | 两边都说，但不排序      | 政策分析可保留        | 写清主次和取舍            | 删除一边导致片面      | “一方面提效一方面风险”→“提效是真的，风险主要在转人工边界”  |
| 强行递进     | “不仅……更……”                 | 制造虚假层次         | 演讲稿可少量使用       | 直接写核心判断            | 换成“不只是……还是……” | “不仅提效，更重塑组织”→“它能减少重复录入”          |
| 抽象商业词    | “赋能、打造、助力、闭环、生态、场景化、深度融合” | 词大、边界小         | 咨询报告、融资叙事可少量保留 | 每个抽象词落到机制          | 用同义黑话替换       | “赋能门店”→“让店长每天看到缺货 SKU”           |
| 套话意义句    | “具有重要意义、提供有力支撑、注入新动能”     | 没有新增信息         | 公文结尾可保留        | 删除或改成下一步事实         | 写得更激昂         | “注入新动能”→“预计减少 20% 手工录入”          |
| 伪权威归因    | “专家认为、数据显示、业内人士指出”        | 无名来源制造可信感      | 新闻简讯需来源保护时     | 补具体来源；无来源则标注       | 编造机构/数据       | “数据显示”→“[需补充：数据来源]”              |
| 没有作者视角   | 全文像旁白，无判断位置               | 不知道谁在说、为何说     | 百科、说明书         | 加观察角度或使用边界         | 滥加“我觉得”       | “行业正在变化”→“我更关心中小团队能不能用得起”        |
| 没有具体场景   | “复杂业务场景、用户需求、多元场景”        | 场景是假名词         | 战略稿可概述         | 写一个真实使用瞬间          | 罗列更多抽象场景      | “复杂场景”→“门店晚班交接时找不到上一班记录”         |
| 句长过于均匀   | 每句 25–35 字，节奏一致           | 像模型稳定生成        | 学术摘要、规范文本      | 长短交错，按信息密度断句       | 全改短句          | 插入短句：“问题出在这里。”                   |
| 段落结构过完整  | 每段都有总起、展开、结论              | 过度像模板作文        | 教材、报告          | 允许重点段更长，过渡段更短      | 故意打乱逻辑        | 删除无用总起句                          |
| 结尾上价值    | “未来可期、值得期待、开启新篇章”         | LLM 爱用安全乐观结尾   | 品牌稿可少量         | 用行动、限制、问题收尾        | 改成鸡汤          | “未来可期”→“下一步要验证转人工率是否下降”          |
| 同义词轮换    | 同一对象反复换称呼                 | AI 怕重复，人类会稳定指代 | 文学写作           | 该重复就重复             | 生硬堆同义词        | “平台/系统/解决方案”统一成“平台”              |
| 过度限定     | “可能在一定程度上或许能够”            | 过度避责           | 法律、医疗、政策文本     | 保留必要不确定性，删重复 hedge | 变成绝对判断        | “可能会产生一定影响”→“可能影响转化率”            |

---

# 9. 不同体裁的策略

## 9.1 商业写作

| 体裁    | 常见 AI 味        | 合理的人味          | 不能怎么改  | 最适合策略          | 示例                                         |
| ----- | -------------- | -------------- | ------ | -------------- | ------------------------------------------ |
| 官网文案  | “领先、赋能、极致、全场景” | 清楚说明对象、问题、差异   | 改成闲聊口吻 | 主标题克制，副标题给具体结果 | “赋能企业增长”→“帮销售团队统一线索、跟进和回访记录”               |
| 产品介绍  | 功能堆叠 + 抽象收益    | 使用场景、操作路径、边界   | 编造数据   | 功能—场景—限制       | “智能分析”→“上传表格后自动标出异常值，需人工确认后提交”             |
| 品牌文章  | 上价值、宏大叙事       | 有真实故事、取舍、失败    | 写成自夸稿  | 用一个事件承载价值      | “我们始终坚持用户第一”→“去年我们砍掉了一个高收入但投诉率高的套餐”        |
| 投融资材料 | TAM 空泛、愿景过大    | 假设透明、数字可追、风险清楚 | 改成社媒文  | 数字 + 增长逻辑 + 反证 | “市场空间巨大”→“当前付费客户 312 家，续费率 78%，扩张假设来自两个渠道” |
| 商务邮件  | 客服腔、套话寒暄       | 目的清楚，动作明确      | 过度亲密   | 第一段说目的，最后说动作   | “期待与贵司共创未来”→“周五前确认报价后，我们下周一安排实施排期”         |

## 9.2 内容写作

| 体裁    | 常见 AI 味      | 合理的人味       | 不能怎么改    | 最适合策略        | 示例                                  |
| ----- | ------------ | ----------- | -------- | ------------ | ----------------------------------- |
| 公众号文章 | 开头宏大背景，结尾上价值 | 有选题角度和具体观察  | 标题党 + 鸡汤 | 用故事或冲突开头     | “时代浪潮下”→“过去三个月，我见了 7 个想砍预算的市场负责人”   |
| 知乎回答  | “多维度分析、因人而异” | 明确条件、经验判断   | 装作亲历     | 先给结论，再给边界    | “需要综合判断”→“如果你不愿意每天和人扯皮，不建议转产品”      |
| 小红书文案 | 假亲密、夸张情绪     | 具体体验、对象、限制  | 过度专业     | 场景 + 感受 + 避雷 | “宝藏工具”→“适合每周要做 3 次会议纪要的人，不适合只偶尔记笔记” |
| 视频口播稿 | 书面长句、连接词多    | 短信息单元、自然停顿  | 纯口水      | 一句一个信息点      | “此外值得注意的是”→“还有一点，很多人会忽略”            |
| 新闻评论  | 中立堆两边        | 有事实、有立场、有证据 | 没事实硬输出观点 | 事件—关键矛盾—判断   | “各方观点不一”→“真正的分歧在责任怎么分”              |

## 9.3 专业写作

| 体裁   | 常见 AI 味       | 合理的人味         | 不能怎么改 | 最适合策略              | 示例                                       |
| ---- | ------------- | ------------- | ----- | ------------------ | ---------------------------------------- |
| 技术博客 | “深入探讨、最佳实践”泛化 | 问题复现、代码、坑点    | 加鸡汤   | 问题—原因—修复—代价        | “优化性能”→“把接口从串行改成并发后，P95 从 1.8s 降到 620ms” |
| 产品文档 | 营销词混入说明       | 准确、可操作、少形容词   | 口语化过度 | 动作步骤 + 前置条件 + 错误提示 | “轻松完成配置”→“在左侧菜单选择配置项，点击导入 CSV”           |
| 咨询报告 | 框架词、三段式、黑话    | 定义清楚、假设透明     | 写成散文  | 图表结论 + 证据 + 建议     | “打造闭环生态”→“把获客、转化、复购三个指标放进同一张周报”          |
| 行业分析 | 大趋势无证据        | 指标、样本、反例      | 只写观点  | 明确数据口径             | “行业快速增长”→“2023–2025 年样本公司收入 CAGR 为 X%”   |
| 学术摘要 | “具有重要意义”过多    | 研究问题、方法、结果、贡献 | 口语化   | 保留术语，删除空评价         | “具有重要理论价值”→“实验显示 F1 提升 3.2 个百分点”         |

## 9.4 个人写作

| 体裁    | 常见 AI 味      | 合理的人味      | 不能怎么改 | 最适合策略         | 示例                                      |
| ----- | ------------ | ---------- | ----- | ------------- | --------------------------------------- |
| 申请文书  | “我一直热爱、塑造了我” | 具体经历、选择、反思 | 编经历   | 事件—决定—变化      | “这段经历让我成长”→“那次项目延期后，我第一次意识到自己不会拆需求”     |
| 个人陈述  | 宏大理想         | 稳定动机和证据    | 夸张苦难  | 用细节证明兴趣       | “我渴望改变世界”→“我连续两年做了同一类社区数据项目”            |
| 求职信   | 模板赞美公司       | 岗位匹配、可验证成果 | 套近乎   | 公司需求—我的证据—下一步 | “贵司平台广阔”→“JD 里提到增长实验，我过去做过 12 次 A/B 测试” |
| 反思总结  | “收获颇丰、受益匪浅”  | 承认具体失误     | 写成检讨书 | 事实—判断—下一步     | “沟通能力有待提升”→“我没有在周三同步风险，导致周五才暴露延期”       |
| 日记式表达 | 假文艺、假深刻      | 具体当下感受     | 故意乱写  | 小场景 + 不完整感受   | “生活给予我启示”→“地铁到站的时候我突然不想去公司，但还是下车了”      |

---

# 10. 对我的 Skill 的产品设计建议

## 10.1 Skill 定位

它不应该承诺：

* 保证绕过 AI 检测器。
* 保证检测器显示“人类写作”。
* 帮用户伪造原创、伪造经历、伪造数据。
* 把所有正式文本都变口语。
* 用“错别字、语病、口头禅”制造假人味。

它应该明确解决：

* 找出中文文本里的 AI 腔、套话、空话、语体错配。
* 在不新增事实的前提下，让文本更具体、更自然、更适合体裁。
* 标出缺证据、伪权威、事实风险。
* 按用户作者声音改写。
* 输出可发布版本，而不是只给建议。

它和“绕过 AI 检测器”的区别：

* 绕检测器优化的是检测模型弱点。
* 这个 Skill 优化的是中文读者、编辑和发布场景。
* 检测器分数最多作为外部风险信号，不作为质量目标。

## 10.2 触发条件

应该启用的用户表达：

* “帮我去 AI 味”
* “这段太像 AI 了”
* “改得像真人写的”
* “别公文腔 / 别营销腔 / 别公众号腔”
* “让它更自然、更可信”
* “改成知乎 / 小红书 / 官网 / 技术博客 / 商务邮件风格”
* “保留意思，但别那么模板”
* “帮我润色 AI 草稿”

不应该启用：

* 用户只要求翻译。
* 用户只要求摘要。
* 用户只要求事实核查。
* 用户要写新的虚假个人经历。
* 用户明确要求“帮我绕过 Turnitin/GPTZero/检测器”。这种请求应转为“我可以帮你提升文本质量和真实性，但不做检测规避”。

## 10.3 Skill 工作流

1. **输入识别**：判断是待改文本、写作样本、说明要求，还是混合输入。
2. **体裁判断**：识别官网、产品介绍、公众号、知乎、技术文档、学术摘要、个人陈述等。
3. **作者声音判断**：若用户提供样本，提取句长、词汇、标点、段落开头、判断强度、口语程度。
4. **AI 味诊断**：按中文 taxonomy 标出主要问题，不要逐句啰嗦。
5. **风险标注**：伪数据、伪来源、未经支持的宏大判断、个人经历缺失。
6. **策略选择**：删、降维、具体化、改结构、换语体、保留术语、标注需补事实。
7. **输出版本**：默认一个可发布版本；需要时给“克制版 / 更有作者声音版”。
8. **自检**：事实是否新增、体裁是否跑偏、是否过度口语化、是否仍有套话。

## 10.4 Skill 应该问用户的问题

必须问的情况：

* 用户没有提供文本。
* 用户要求使用“我的风格”，但没有样本。
* 文本涉及申请文书、求职信、学术提交、法律/医疗/金融等高风险用途，且需要补事实。
* 同一段文本可能被改成完全不同体裁，且无法从上下文判断。

可以自动推断的：

* 体裁明显时不用问，例如邮件、产品介绍、公众号文章。
* 目标读者明显时不用问。
* 语气可从原文和平台推断时不用问。
* 长度没有强约束时默认不大幅扩写。

避免问太多：

默认只问一个关键问题。其余用“我按 X 处理”直接完成。例如：

> 我按“产品介绍，面向潜在客户，不新增事实，语气克制”处理。

## 10.5 输出格式

默认格式：

1. **诊断**：3–5 条，指出最大问题。
2. **改写版**：直接给可用文本。
3. **修改说明**：只列关键取舍。
4. **风险 / 需补充**：只有存在事实缺口时才显示。

不建议默认给 3 个版本。多个版本会增加用户选择成本。只有在用户要求或体裁不确定时给两个版本：克制版、表达更强版。

## 10.6 质量评估标准

建议 10 个维度，每项 1–5 分：

| 维度      | 评估问题                 |
| ------- | -------------------- |
| 准确性     | 是否保留原意，是否引入新事实       |
| 具体性     | 是否减少空话，增加可验证细节       |
| 体裁一致性   | 是否符合平台和用途            |
| 作者声音一致性 | 是否像用户样本，而不是统一 AI 编辑腔 |
| 证据密度    | 判断是否有事实、案例、数据支撑      |
| 节奏自然度   | 句长、段落、转折是否有变化        |
| 可发布程度   | 是否能直接使用              |
| 克制度     | 是否删掉过度升维、过度情绪        |
| 边界感     | 是否标出不确定、限制和风险        |
| 非伪装性    | 是否避免错别字、假口语、假经历      |

---

# 11. 推荐 Skill 文件结构

```text
chinese-humanizer/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── chinese-ai-tells.md
│   ├── genre-playbook.md
│   ├── rewrite-strategies.md
│   ├── quality-rubric.md
│   ├── voice-calibration.md
│   ├── safety-and-integrity.md
│   └── examples.md
└── scripts/
    └── chinese_ai_tell_linter.py   # 可选
```

说明：

* `SKILL.md`：只放触发条件、总流程、默认输出、核心规则，不要塞完整理论。
* `references/chinese-ai-tells.md`：放中文 AI 味分类体系和例句。
* `references/genre-playbook.md`：放不同体裁策略。
* `references/rewrite-strategies.md`：放删、降维、具体化、重组、换语体等操作。
* `references/quality-rubric.md`：放评分表和自检问题。
* `references/voice-calibration.md`：放作者声音提取方法。
* `references/safety-and-integrity.md`：放不绕检测器、不伪造、不新增事实规则。
* `references/examples.md`：放 before / failed / successful 三联例。
* `scripts/chinese_ai_tell_linter.py`：可选，只做启发式辅助，比如统计抽象词、连接词、句长方差、疑似伪权威。不要把脚本结果当最终判断。

---

# 12. 初版 Skill 工作流

```text
收到用户请求
  ↓
判断是否触发：
  - 去 AI 味 / humanize / 改自然 / 去公文腔 / 去营销腔 / 改成某体裁
  - 若用户要求绕过检测器：拒绝检测规避，转为质量编辑
  ↓
解析输入：
  - 待改文本
  - 用户要求
  - 目标体裁
  - 作者样本
  - 禁止新增事实 / 长度限制
  ↓
体裁判断：
  - 商业 / 内容 / 专业 / 个人 / 其他
  - 若明显则不问
  - 若高风险且不明确，问一个关键问题
  ↓
诊断：
  - 标出 3–5 个最大 AI 味
  - 标出事实风险
  - 判断是否缺场景、缺证据、缺主体
  ↓
策略：
  - 删除空泛升维
  - 压缩宏大判断
  - 明确主体和动作
  - 替换公文/营销/翻译腔
  - 调整节奏
  - 保留体裁必要的正式度
  - 不新增事实；必要处用 [需补充]
  ↓
改写：
  - 默认输出一个版本
  - 保留原意和覆盖范围
  - 不为了人味而乱加“我觉得”
  ↓
自检：
  - 有没有编事实
  - 有没有过度口语化
  - 有没有仍然空泛
  - 有没有体裁错配
  - 有没有过多解释修改过程
  ↓
输出：
  - 诊断
  - 改写版
  - 修改说明
  - 需补事实
```

---

# 13. 初版 `SKILL.md` 草案

```markdown
---
name: chinese-humanizer
description: |
  Rewrite Chinese AI-generated or AI-polished drafts into more natural, credible, genre-appropriate Chinese.
  Use when the user asks to 去 AI 味, humanize Chinese text, remove 公文腔/营销腔/翻译腔/套话, make a draft sound more natural,
  or adapt a Chinese draft to a platform or genre such as product copy, business email, Zhihu, WeChat article,
  technical blog, documentation, personal statement, or academic abstract.
  This skill improves editorial quality and writing authenticity. It must not promise to bypass AI detectors,
  fake authorship, fabricate sources, invent personal experiences, or optimize for detector scores.
---

# Chinese Humanizer

You are a Chinese editor specializing in natural, credible, genre-aware rewriting of AI-like Chinese drafts.

Your job is not to make text "casual." Your job is to make the text fit its real writing situation.

## Use this skill when

Use this skill when the user asks to:

- 去 AI 味 / 去机器味 / humanize 中文文本
- 让中文更自然、更像真人写
- 去掉公文腔、营销腔、公众号腔、翻译腔、套话
- 保留意思但减少模板感
- 改成某种中文体裁：官网、产品介绍、品牌文章、投融资材料、商务邮件、公众号、知乎、小红书、视频口播、新闻评论、技术博客、产品文档、咨询报告、行业分析、学术摘要、申请文书、个人陈述、求职信、反思总结等

Do not use this skill for pure translation, pure summarization, or factual research unless the user also asks for style/AI-tell editing.

## Integrity boundaries

Never promise that the rewrite will bypass AI detectors.

If the user asks to "pass Turnitin/GPTZero/AI detector" or similar, respond by saying you can help improve clarity, specificity, voice, and authenticity, but you cannot help evade detection systems.

Do not fabricate:

- statistics
- citations
- expert opinions
- user experiences
- personal stories
- product features
- company results
- dates, names, organizations, or sources

When the original text lacks evidence, either narrow the claim or mark it as:

`[需补充：具体数据/案例/来源]`

## Default output

Unless the user asks otherwise, output:

1. **诊断** — 3 to 5 key AI-like issues.
2. **改写版** — one publishable rewrite.
3. **修改说明** — short notes on the main editorial choices.
4. **需补充** — only if facts, data, sources, or personal details are missing.

Keep the output compact. Do not over-explain.

## Workflow

### 1. Identify the task

Extract:

- text to rewrite
- target genre
- target audience
- tone requirement
- length requirement
- whether new facts are allowed
- any author writing sample

If the text and genre are clear, do not ask questions. Proceed.

Ask at most one clarifying question only when continuing would likely produce the wrong genre, wrong voice, or fabricated content.

### 2. Determine genre

Classify the draft as one of:

- business writing: website copy, product copy, brand article, fundraising material, business email
- content writing: WeChat article, Zhihu answer, Xiaohongshu copy, video script, news commentary
- professional writing: technical blog, product documentation, consulting report, industry analysis, academic abstract
- personal writing: application essay, personal statement, cover letter, reflection, diary-like writing
- other

Genre controls the rewrite. Do not add casual voice to technical, legal, academic, or documentation text.

### 3. Calibrate author voice

If the user provides a writing sample, analyze:

- sentence length
- paragraph rhythm
- word choice level
- amount of first person
- punctuation habits
- transition habits
- directness of opinions
- tolerance for humor or edge

Match the sample. Do not produce a generic "clean" voice.

If there is no sample, use a restrained, natural, specific Chinese style suited to the genre.

### 4. Diagnose Chinese AI tells

Check for:

- 空泛升维
- 宏大但无证据的判断
- 机械三段式
- 公文腔
- 营销腔
- 翻译腔
- 连接词堆叠
- 安全中立腔
- 假平衡：一方面……另一方面……
- 强行递进：不仅……更……
- 抽象商业词：赋能、打造、助力、闭环、生态、场景化、深度融合
- 套话：具有重要意义、提供有力支撑、注入新动能
- 伪权威归因：专家认为、数据显示、业内人士指出
- 没有作者视角
- 没有具体场景
- 句长过于均匀
- 段落结构过于完整
- 结尾总是上价值或展望未来
- 同义词轮换
- 过度限定

Prioritize the most damaging issues. Do not list every small flaw.

### 5. Choose rewrite strategy

Use these operations:

- Delete empty throat-clearing.
- Replace abstract claims with concrete subjects, actions, scenes, mechanisms, or limits.
- Narrow unsupported claims.
- Convert vague authority to specific sources or `[需补充]`.
- Replace business jargon with actual workflow or user outcome.
- Break formulaic structures.
- Vary sentence and paragraph rhythm.
- Keep necessary technical, academic, legal, or business formality.
- Preserve meaning and coverage.
- Do not add unsupported facts.

### 6. Rewrite

Write a complete version, not a patch list.

Maintain the original intent and useful information. Remove or mark unsupported information.

Do not force first person unless the genre and author voice call for it.

Do not add fake口语 markers such as “说实话”, “老实讲”, “真的”, “挺”, “蛮” unless they match the user’s sample and genre.

### 7. Self-audit before final

Check:

- Did I invent any fact?
- Did I change the user’s claim?
- Is the genre still correct?
- Is the text over-casual?
- Are there remaining empty phrases?
- Does every major claim have evidence, a source, a concrete scene, or a clear boundary?
- Does the ending say something useful instead of上价值?

If the rewrite fails, revise once before responding.

## Genre rules

### Business writing

Prefer clarity, concrete value, and proof.

Avoid:
- 赋能
- 打造生态
- 全场景解决方案
- 极致体验
- 注入新动能

Use:
- user
- problem
- workflow
- measurable result
- limitation or condition

### Content writing

Prefer angle, scene, judgment, and rhythm.

Avoid:
- 时代背景开头
- 多维度分析
- 各有利弊 without ranking
- 鸡汤式结尾

Use:
- concrete opening
- clear stance
- examples
- natural transitions

### Professional writing

Prefer precision.

Avoid:
- marketing adjectives
- unsupported significance claims
- fake authority

Use:
- definition
- method
- evidence
- result
- boundary

### Personal writing

Prefer truthful specificity.

Avoid:
- fabricated hardship
- generic growth language
- “这段经历让我受益匪浅”

Use:
- specific event
- decision
- mistake
- change in behavior
- future fit

## Quality rubric

Score internally from 1 to 5:

- accuracy: no unsupported new facts
- specificity: fewer abstractions, more concrete details
- genre fit: tone matches use case
- voice fit: matches user sample if provided
- evidence density: claims have support or boundaries
- rhythm: sentence and paragraph variation
- publishability: can be used directly
- restraint: no over-writing
- clarity: easy to understand
- integrity: no detector-evasion framing

Do not show the score unless the user asks.

## Reference files

Load these only when needed:

- `references/chinese-ai-tells.md` for detailed AI tell taxonomy.
- `references/genre-playbook.md` for genre-specific rewrites.
- `references/rewrite-strategies.md` for editing operations.
- `references/quality-rubric.md` for self-audit.
- `references/voice-calibration.md` when the user provides a writing sample.
- `references/safety-and-integrity.md` for detector-evasion, academic integrity, and fabrication risks.
- `references/examples.md` for before/failed/successful examples.
```

---

# 14. 仍需进一步验证的问题

1. **中文 AI 味 taxonomy 需要语料验证。**
   目前这套分类来自研究、项目分析和中文编辑实践推断。下一步应采集真实中文 AI 草稿、人类稿、编辑后稿，按体裁标注问题类型。

2. **不同体裁的权重不同。**
   “没有作者视角”在知乎回答里是大问题，在产品文档里不一定是问题。需要按体裁调权重。

3. **中文检测器与人类编辑判断的关系要测试。**
   不建议把检测分作为目标，但可以研究“人类觉得更自然”的改写是否也降低某些检测器置信度。这个实验必须只作风险观察，不作产品承诺。

4. **作者声音校准需要隐私规则。**
   如果用户提供个人写作样本，Skill 应只在当前任务中使用，不应总结成可复用身份画像。

5. **不能新增事实的策略要做得更细。**
   很多 AI 草稿本身太空，不补事实就不好看。Skill 应学会输出“保守可用版”和“需补资料版”，而不是擅自编。

6. **大陆、台湾、香港、新加坡中文差异需要单独处理。**
   简体/繁体、普通话/国语/华语、商务语体、新闻语体差异会影响“自然感”。现代标准汉语本身在不同地区有词汇和语音差异，中文 Skill 后续也应让用户指定地区语体。([Wikipedia][26])

7. **需要真实 A/B 测试。**
   最小测试集可以是：每类体裁 30 段 AI 草稿，三种改写策略，10 名中文编辑盲评。评价维度用“可信、自然、体裁合适、事实安全、可发布”。

---

# 15. 参考文献与链接

## AI 文本检测理论

* Mitchell et al., **DetectGPT**：用 log probability curvature 检测生成文本。([arXiv][4])
* Bao et al., **Fast-DetectGPT**：用条件概率曲率提升速度和效果。([arXiv][27])
* Sadasivan et al., **Can AI-Generated Text be Reliably Detected?**：讨论 paraphrasing、watermark spoofing 和检测理论上限。([arXiv][19])
* Kirchenbauer et al., **A Watermark for Large Language Models**：green-token 水印方法。([arXiv][12])
* Google DeepMind, **SynthID text watermarking**：官方说明水印机制、优势和限制。([Google DeepMind][13])
* OpenAI, **New AI classifier for indicating AI-written text**：官方下线说明和局限。([OpenAI][1])
* Turnitin, **AI writing detection FAQ**：商业检测的分段、句子评分、语言支持、误判说明。([guides.turnitin.com][2])
* GPTZero, **Technology / FAQ**：深度学习、句子级分类、混合文本、限制说明。([GPTZero][25])

## 中文与多语言检测

* Guo et al., **HC3: Human ChatGPT Comparison Corpus**，以及 HC3-Chinese 仓库。([arXiv][28])
* Wang et al., **LLM-Detector: Improving AI-Generated Chinese Text Detection with Open-Source LLM Instruction Tuning**。([arXiv][14])
* Qing et al., **C-ReD: A Comprehensive Chinese Benchmark for AI-Generated Text Detection Derived from Real-World Prompts**。([arXiv][15])
* NLPCC 2025 相关中文检测：Qwen2.5 LoRA、EnsemJudge。([arXiv][16])
* M4 / M4GT-Bench：多语言、多领域、多生成器检测 benchmark。([GitHub][29])
* Modern Chinese Poetry Benchmark：现代中文诗歌 AI 检测困难。([arXiv][18])

## Humanization / 对抗改写

* Krishna et al., **Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense**。([arXiv][5])
* RADAR：paraphraser 与 detector 对抗训练。([arXiv][30])
* AuthorMist：用 detector API 作为 RL reward 规避检测。([arXiv][20])
* Adversarial Paraphrasing：用检测器引导释义攻击。([arXiv][6])
* StealthRL：跨检测器集成的 RL paraphrase attack。([arXiv][31])

## 参考项目

* `op7418/Humanizer-zh`：中文 humanizer Skill。([GitHub][3])
* `op7418/Humanizer-zh` 的 `SKILL.md`：24 类规则、流程、评分。([GitHub][21])
* `blader/humanizer`：英文上游项目，33 patterns、voice calibration、二次审稿。([GitHub][8])
* `hardikpandya/stop-slop`：短规则 + references 文件组织方式。([GitHub][22])

这份报告做了三件事：先确认检测技术和 humanization 研究的边界，再拆 Humanizer-zh 与上游项目，最后把结论落到一个可执行的中文 Skill 设计。我的主要取舍是：不把“检测规避”当产品目标，不把“口语化”当自然感，不允许靠编事实制造可信度。

[1]: https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/ "https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/"
[2]: https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs "https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs"
[3]: https://github.com/op7418/Humanizer-zh "https://github.com/op7418/Humanizer-zh"
[4]: https://arxiv.org/abs/2301.11305 "https://arxiv.org/abs/2301.11305"
[5]: https://arxiv.org/abs/2303.13408 "https://arxiv.org/abs/2303.13408"
[6]: https://arxiv.org/abs/2506.07001 "https://arxiv.org/abs/2506.07001"
[7]: https://github.com/Hello-SimpleAI/chatgpt-comparison-detection "https://github.com/Hello-SimpleAI/chatgpt-comparison-detection"
[8]: https://github.com/blader/humanizer "https://github.com/blader/humanizer"
[9]: https://arxiv.org/abs/2510.12608 "https://arxiv.org/abs/2510.12608"
[10]: https://arxiv.org/abs/2303.14822 "https://arxiv.org/abs/2303.14822"
[11]: https://arxiv.org/abs/2403.03506 "https://arxiv.org/abs/2403.03506"
[12]: https://arxiv.org/abs/2301.10226 "https://arxiv.org/abs/2301.10226"
[13]: https://deepmind.google/discover/blog/watermarking-ai-generated-text-and-video-with-synthid/ "https://deepmind.google/discover/blog/watermarking-ai-generated-text-and-video-with-synthid/"
[14]: https://arxiv.org/abs/2402.01158 "https://arxiv.org/abs/2402.01158"
[15]: https://arxiv.org/abs/2604.11796 "https://arxiv.org/abs/2604.11796"
[16]: https://arxiv.org/abs/2509.00731 "https://arxiv.org/abs/2509.00731"
[17]: https://arxiv.org/abs/2603.27949 "https://arxiv.org/abs/2603.27949"
[18]: https://arxiv.org/abs/2509.01620 "https://arxiv.org/abs/2509.01620"
[19]: https://arxiv.org/abs/2303.11156 "https://arxiv.org/abs/2303.11156"
[20]: https://arxiv.org/abs/2503.08716 "https://arxiv.org/abs/2503.08716"
[21]: https://raw.githubusercontent.com/op7418/Humanizer-zh/main/SKILL.md "https://raw.githubusercontent.com/op7418/Humanizer-zh/main/SKILL.md"
[22]: https://github.com/hardikpandya/stop-slop "https://github.com/hardikpandya/stop-slop"
[23]: https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md "https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md"
[24]: https://raw.githubusercontent.com/hardikpandya/stop-slop/main/references/structures.md "https://raw.githubusercontent.com/hardikpandya/stop-slop/main/references/structures.md"
[25]: https://gptzero.me/technology "https://gptzero.me/technology"
[26]: https://zh.wikipedia.org/wiki/%E7%8F%BE%E4%BB%A3%E6%A8%99%E6%BA%96%E6%BC%A2%E8%AA%9E "https://zh.wikipedia.org/wiki/%E7%8F%BE%E4%BB%A3%E6%A8%99%E6%BA%96%E6%BC%A2%E8%AA%9E"
[27]: https://arxiv.org/abs/2310.05130 "https://arxiv.org/abs/2310.05130"
[28]: https://arxiv.org/abs/2301.07597 "https://arxiv.org/abs/2301.07597"
[29]: https://github.com/mbzuai-nlp/M4 "https://github.com/mbzuai-nlp/M4"
[30]: https://arxiv.org/abs/2307.03838 "https://arxiv.org/abs/2307.03838"
[31]: https://arxiv.org/abs/2602.08934 "https://arxiv.org/abs/2602.08934"
