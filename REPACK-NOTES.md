# Repack notes — companion-picture-book → GitHub-ready (2026-11-10)

Source: the user's original skill pack `workspace/user/files/companion-picture-book.zip`
(built 2026-10-16, 10 files, 56,080 bytes), also downloadable at
https://peiban.zengchuan.cn/ （小小陪伴）.

## What was checked (2026-11-10, ~11:10 CST)

- `SKILL.md` frontmatter already has exactly what the Agent Skills format
  requires: `name: companion-picture-book` + a full `description`.
  Verified against the live anthropics/skills README
  (https://github.com/anthropics/skills — 191,148 stars, checked 2026-11-10
  03:10 UTC): "The frontmatter requires only two fields: name, description."
  No SKILL.md change was needed.
- Structure already matches the format: one folder + `SKILL.md` +
  `references/` + `scripts/export_texts.py` + `agents/openai.yaml`.

## What changed in this repack

- Added `README.md` (bilingual, install steps for Claude Code / Claude.ai /
  API / Doubao, repo layout, demo-book link).
- Renamed the MIT licence file `LICENSE.picture-book-generator` → `LICENSE`
  at repo root (the original file is still inside the skill folder, untouched).
- Moved the skill under `skills/companion-picture-book/` so the repo reads
  like anthropics/skills (`skills/<name>/SKILL.md`).
- Nothing inside the skill was edited: `diff -r` against the unzipped
  original is clean (COPY-OK, 2026-11-10).

## What is NOT done — needs the user

- Not published to GitHub. The user pushes under his own GitHub identity
  (892041548 / ZZY); Muse never opens repos/PRs for him.
- Suggested repo name (his choice): `companion-picture-book` or
  `picture-book-skill`. Suggested first commit message: the README + skill
  as-is, no code changes.
- Open question for him: keep the Doubao-first wording on the site, or
  present this repo as Claude-first now that Agent Skills is the hot
  category (anthropics/skills was GitHub #1 on 2026-11-10, +1K that day)?
