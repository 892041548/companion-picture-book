# Companion Picture Book Skill · 陪伴式绘本制作

Make a custom bilingual (Chinese–English) children's picture book with an AI assistant — from one input: the child's age.

根据孩子年龄，定制中英双语亲子绘本：先给一张适龄共读建议卡，确认故事梗概与画风后逐页生成、逐页质检，最后交付双语成品页 + 5 份朗读 TXT + 家长共读提示。

- 🌐 Product site / 产品站：https://peiban.zengchuan.cn/ （小小陪伴）
- 📖 Live demo / 在线样书：「爸爸回家啦」（2 岁 demo，站内可看、可打印）
- 📦 Skill pack / 技能包：`skills/companion-picture-book/`（本仓库即技能包，下载后按下面步骤安装）

## What it does / 能做什么

1. **Age-first advice card** — give the child's age (months/years) and get a short reading-advice card: what to focus on, which format fits, how many pages.
   先给适龄建议卡，再选形式，不先发长问卷。
2. **Two branches / 两个分支** — `single` 单页互动教辅（指认、游戏）or `story` 连续故事（生活习惯、情绪陪伴、家庭关系、同伴交往、自然探索、想象冒险）。
3. **Confirm, then make** — outline + art style confirmed in one round, then page-by-page generation with forced quality checks (face, outfit, scene and prop consistency across pages; bilingual text checked against the pictures).
   梗概与画风一次确认，逐页生成、逐页检查，不把“同一个人”寄托在一句话上。
4. **Deliverables / 交付物** — bilingual finished pages, plus 5 TXT reading scripts （中英对照含音标谐音 / 中文正文 / 英文正文 / 英文音标版 / 英文谐音版） and a parent guide.
   双语成品页 + 五份 TXT 朗读稿 + 家长提示。

## Install / 安装

The skill is one folder with a `SKILL.md` — the Agent Skills format (see [anthropics/skills](https://github.com/anthropics/skills); frontmatter needs only `name` + `description`, which this skill already has).

### Claude Code

```bash
# clone, then point Claude Code at the skills folder, or copy the skill in:
cp -r skills/companion-picture-book ~/.claude/skills/
```

Then say: “用陪伴绘本 skill，给 2 岁的孩子做一本关于刷牙的双语绘本。”

### Claude.ai / API

Upload the `skills/companion-picture-book/` folder as a skill (Claude.ai paid plans support skill upload; API: see the Skills API quickstart in the anthropics/skills README).

### Doubao / 豆包（原用法）

This skill was first built for Doubao — download the same folder from https://peiban.zengchuan.cn/, send it to Doubao and install in one click. The workflow is host-agnostic; nothing in `SKILL.md` is Doubao-only except the install path.
最初为豆包制作：去小小陪伴站下载技能包发给豆包一键安装即可，流程本身不依赖豆包。

## Repo layout / 结构

```
skills/companion-picture-book/
├── SKILL.md                  # skill instructions + frontmatter (name, description)
├── references/               # age-and-materials, production, styles, quality-checks, pronunciation, sources
├── scripts/export_texts.py   # exports the 5 TXT reading scripts from manuscript.json
└── agents/openai.yaml        # agent config
LICENSE                       # MIT
```

## Notes / 说明

- The skill never diagnoses a child's development and never promises learning outcomes; it gives reading advice and makes books.
  只做共读建议与绘本制作，不做发育诊断、不承诺学习效果。
- Photo characters are optional: a clear front-facing photo can seed the hero; animal or fictional heroes need no photo.
  照片角色可选，不用照片也可以用小动物/虚构角色当主角。
- One page, one picture; text is laid out after the illustration so Chinese/English lettering stays readable.
  一页一图，文字后排版，保证中英文字可读。

## License

MIT — see `LICENSE`.
