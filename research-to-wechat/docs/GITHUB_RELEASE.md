# GitHub Release Guide

Use this checklist before pushing `research-to-wechat` as a public-facing skill update.

## Release goal

Ship the skill as a clean GitHub-ready package with:

- clear positioning
- complete usage docs
- root repo visibility
- no forbidden legacy naming inside the skill directory

## Required files

The release should include:

- `research-to-wechat/SKILL.md`
- `research-to-wechat/README.md`
- `research-to-wechat/CHANGELOG.md`
- `research-to-wechat/LICENSE`
- `research-to-wechat/references/capability-map.md`
- `research-to-wechat/references/style-engine.md`
- `research-to-wechat/references/execution-contract.md`
- `research-to-wechat/references/platform-copy.md`
- `research-to-wechat/references/design-guide.md`
- `research-to-wechat/design.pen`
- `research-to-wechat/scripts/fetch_wechat_article.py`
- `research-to-wechat/scripts/install-openclaw.sh`
- `research-to-wechat/docs/GITHUB_RELEASE.md`
- `research-to-wechat/docs/EXAMPLES.md`
- root `README.md`

## Smoke checks

Run these checks before publishing:

```bash
# Run your current forbidden-term denylist scan against research-to-wechat/
python3 '/Users/clarezoe/.agent/skills/skill-creator/scripts/package_skill.py' \
  '/Users/clarezoe/Dropbox/My Apps/my-skills/research-to-wechat' \
  /tmp/research-to-wechat-release-check
```

Expected result:

- search returns no matches in `research-to-wechat/`
- packaging succeeds without validation errors

## README review

Verify the skill README answers these questions:

- what problem does this skill solve
- who is it for
- how `Path A` and `Path B` differ
- what files does it produce
- what `manifest.json.outputs.wechat` contains
- what inputs does it accept
- how the research architecture and question lattice work
- how the writing frameworks (deep-analysis, tutorial) structure the article
- how the normalization checklist and image evaluation ensure quality
- how evidence limits and disclosure are handled
- how style resolution works
- how HTML rendering works (md2wechat ai mode)
- how the WeChat delivery ladder degrades
- how optional multi-platform distribution works (Phase 8)
- how article design selection works with Pencil MCP (10 styles, auto-selection)
- where the execution rules live

## Root repo review

Verify the root `README.md`:

- lists `research-to-wechat` in featured skills
- describes it consistently in English, Chinese, and Japanese
- presents the skill as one member of the wider skill collection

## Suggested GitHub metadata

Repository-facing short description:

`Research-first WeChat article pipeline with evidence ledger, writing frameworks, routed structure, md2wechat HTML rendering, manifest output, optional multi-platform distribution, and API/browser/manual draft fallback.`

Suggested topics:

- `skill`
- `wechat`
- `content-workflow`
- `markdown`
- `article-generation`
- `writing-system`
- `research`
- `multi-platform`

## Suggested release note shape

```md
## Added
- Writing frameworks: deep-analysis 四幕式 (8000-12000字) and tutorial 六段式 (2000-4000字)
- Writing checklists and prohibitions for each framework
- Research architecture with 32+ question lattice across 4 cognitive layers
- Strategic clarification protocol (5 dimensions) before brief creation
- Article normalization checklist (12+ rules) for source artifact cleanup
- Image placeholder strategy with placement criteria and keyword construction
- Two-tier image evaluation (Tier A elimination, Tier B quality match)
- Cover spec: 900x383px at 2x with center-cropped thumbnail
- HTML rendering via md2wechat skill (ai mode, no external API)
- Optional multi-platform distribution (小红书、即刻、小宇宙、朋友圈)
- Platform copy specs for each distribution target
- WeChat article fetch script (Python, mobile UA)

## Updated
- Evidence ledger format, manifest schema, and delivery ladder
- Capability aliases for all pipeline stages
- README, examples, and release docs match v0.4.0 contract

## Verified
- Skill packaging passes
- Release docs match the current execution contract
```

## Suggested screenshots

If you want visual proof for the GitHub page, capture:

- the skill directory tree
- the top of `research-to-wechat/README.md`
- the style engine reference
- the packaged validation output

## Publish sequence

1. Verify the smoke checks
2. Review the skill README in GitHub preview
3. Review the root README in GitHub preview
4. Commit only the intended files
5. Push the branch
6. Open the GitHub page and verify links render correctly

## Final gate

Do not publish if any of these are true:

- skill packaging fails
- any forbidden legacy term still appears in `research-to-wechat/`
- root README and skill README describe different outputs
- README omits the manifest or delivery ladder behavior
- example prompts no longer match the current style system
