---
name: linuxdo-application
description: >
  Craft high-pass-rate, de-AI'd Chinese applications (小作文) for Linux.do registration.
  Conducts an adaptive survey to learn the applicant's real background, then generates
  natural, rule-compliant plain text ready to paste. All user interactions in Chinese.
metadata:
  openclaw:
    emoji: "📝"
    homepage: "https://github.com/Fei2-Labs/skill-genie"
  version: "1.0.0"
  category: "content-generation"
  author: "Skill Genie"
  license: "MIT"
  language:
    backend: English
    user-facing: Chinese
---

# Linux.do Application Writer

Generate a natural, high-pass-rate registration application for Linux.do through
an adaptive interview followed by rule-aware, de-AI'd text generation.

## Triggers

- "write linux.do application"
- "linux.do 小作文"
- "linux.do 注册申请"
- "help me apply to linux.do"

## Quick Reference

| Input | Output | Duration |
|-------|--------|----------|
| Answers to 5-8 survey questions | Plain text Chinese application (~80-150 chars) | 5-10 min |

## Process

### Phase 1: Applicant Survey

Conduct an adaptive interview in Chinese to collect the 4 required info blocks.
Ask **one question at a time**. Adapt follow-ups based on answers.

**Core questions (ask in Chinese, adapt order based on flow):**

1. 你平时主要做什么？（工作、学习、兴趣方向）
2. 你是怎么知道 Linux.do 的？（搜索、朋友推荐、看到某个帖子？）
3. 你在上面浏览过哪些内容？有没有印象深的帖子或话题？
4. 为什么现在想注册？有什么具体的需求或场景吗？
5. 注册之后你打算怎么用？（潜水、回帖、关注某类话题、分享经验？）

**Adaptive rules:**
- If an answer is vague (e.g., "想学习交流"), probe deeper: "具体想学什么？在哪看到过相关讨论？"
- If an answer already covers multiple blocks, skip redundant questions
- If the applicant mentions a specific post/topic, ask them to elaborate — this is gold
- Stop when all 4 info blocks are covered (see references/linuxdo-rules.md)

**Verification:** Before moving to Phase 2, confirm internally:
- [ ] Background covered (what they do/follow)
- [ ] Discovery path covered (how they found the site)
- [ ] Join reason covered (why register now, specific scenario)
- [ ] Usage plan covered (what they'll do with the account)

If any block is missing, ask one more targeted question.

### Phase 2: Draft Generation + Risk Check

Generate the application draft using collected info.

**Generation rules:**
1. Write in first person, casual Chinese — like telling a friend why you signed up
2. Target 80-150 characters. Not too short (looks lazy), not too long (looks try-hard)
3. Weave all 4 info blocks naturally — do NOT use a 4-paragraph structure
4. Use the applicant's own words and phrasing where possible
5. No greetings, no sign-offs, no "你好" or "谢谢" — just the substance
6. Allow sentence fragments, colloquialisms, and imperfect grammar
7. Vary sentence length: mix short punchy lines with longer ones

**Risk check — scan the draft against these (see references/linuxdo-rules.md):**

| Risk Level | Check |
|------------|-------|
| HIGH | Does it mention background? Discovery path? Join reason? |
| HIGH | Is there any concrete fact, or is it all fluff? |
| HIGH | Does it look like a template that could apply to anyone? |
| MEDIUM | Is it only admiration/flattery without substance? |
| MEDIUM | Is it only "I can contribute X" without explaining why here? |
| MEDIUM | Is info density too low for the character count? |

If any HIGH risk is triggered, rewrite before proceeding.

### Phase 3: De-AI Polish + Final Output

Run the draft through the full de-AI checklist (see references/de-ai-checklist.md).

**Audit steps:**
1. Check all 12 AI markers — flag and rewrite any matches
2. Read the text as if you're a human reviewer — does it smell like AI?
3. Apply the 3-question smell test:
   - Could you swap details and reuse this for someone else? → too generic
   - Does every sentence add new information? → cut filler
   - Would you text this to a friend? → loosen if too formal

**Output:** Present the final application as plain text in a code block.
Tell the user in Chinese: "这是你的申请文，可以直接复制粘贴到注册页面。"

If the user wants changes, revise and re-run Phase 3 checks.

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Parallel structures (我喜欢X，我热爱Y) | AI marker #1 | Vary grammar patterns |
| 三段式 (首先/其次/最后) | AI marker #2 | Drop scaffolding |
| AI vocab (赋能/深耕/沉淀/赛道) | AI marker #5 | Use plain spoken Chinese |
| Flattery (久仰大名/慕名而来) | High-risk per rules | Replace with real discovery story |
| Generic motivation (想学习交流) | Medium-risk per rules | State specific use case |
| Press-release tone | AI marker #9 | Add 吧/嘛/其实/反正 |

## Verification

After final output, confirm:

- [ ] All 4 info blocks present
- [ ] 80-150 characters
- [ ] Zero high-risk patterns
- [ ] Passes all 12 de-AI markers
- [ ] Reads like a real person wrote it
- [ ] Plain text, no formatting

## Extension Points

1. **Rule updates:** When Linux.do changes registration rules, update `references/linuxdo-rules.md`
2. **New AI markers:** As AI detection evolves, add markers to `references/de-ai-checklist.md`
3. **Multi-community:** Adapt the survey + rule framework for other invite-only communities

## References

- [Linux.do Rules & Signals](references/linuxdo-rules.md) — official rules + community patterns
- [De-AI Checklist](references/de-ai-checklist.md) — 12 AI markers to detect and fix

## Related Skills

| Skill | Use When |
|-------|----------|
| wechat-compliance-check | Need to check Chinese content for platform compliance |
| psychology-master | Need deeper user profiling during survey |
| humanizer-zh | Additional de-AI processing for Chinese text |
