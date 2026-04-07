# web-to-obsidian

[English](./README.md) | [简体中文](./README.zh-CN.md)

Ingest public web articles, especially WeChat official account articles, into Obsidian-friendly Markdown notes.

## Overview

This repository contains a `web-to-obsidian` skill that combines:

- web retrieval strategy inspired by [`eze-is/web-access`](https://github.com/eze-is/web-access)
- article extraction logic
- Markdown normalization
- Obsidian note writing

The goal is not just to read a page, but to finish the whole workflow:

`URL -> article body -> Markdown -> frontmatter -> local Obsidian note`

## Underlying Retrieval Layer

This repository does **not** use `to_markdown`.

Its underlying web acquisition model is based on [`eze-is/web-access`](https://github.com/eze-is/web-access):

- choose the cheapest path that can succeed
- escalate to browser access only when needed
- treat anti-bot and dynamic rendering as routing signals, not as reasons to stop

## Supported Workflow

Especially for WeChat official account articles:

1. try direct fetch with a mobile user agent
2. extract:
   - title
   - author
   - body
3. normalize the body into Markdown
4. write the result into an Obsidian directory

If direct fetch fails:
- fall back to the browser-oriented strategy described by `web-access`

## Repository Contents

```text
web-to-obsidian/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── requirements.txt
└── scripts/
    └── save_obsidian_note.py
```

## What This Skill Adds

Compared with a general-purpose web skill, this repository adds:

- article-focused extraction rules
- WeChat-specific selectors
- Markdown cleanup rules
- Obsidian frontmatter conventions
- local note save behavior

## Notes

- `web-access` is the acquisition philosophy and tool pattern
- this repository is the ingestion-and-save layer
- for private pages or sites requiring login, browser/CDP access may still be required

