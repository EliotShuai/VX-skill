# wechat-to-markdown-skill

[English](./README.md) | [简体中文](./README.zh-CN.md)

A small skill wrapper for converting article URLs, especially WeChat official account links, into Markdown and saving them into Obsidian-friendly notes.

## Attribution

This skill uses [`liangtengyu/to_markdown`](https://github.com/liangtengyu/to_markdown) as the underlying parser for converting supported article pages into Markdown.

- Upstream parser repository: [liangtengyu/to_markdown](https://github.com/liangtengyu/to_markdown)
- Upstream repository license: Apache-2.0

This repository focuses on workflow integration for Codex skills and Obsidian note ingestion. It does not reimplement the parser itself.

## What It Does

- Calls a configured `to_markdown` service endpoint
- Extracts Markdown from parser output
- Optionally saves the result as a local Obsidian note
- Adds frontmatter and a stable filename

## Expected Parser Endpoint

The wrapper expects a parser compatible with the `to_markdown` frontend contract:

- `POST /resolve/mark`
- JSON body:

```json
{
  "blogUrl": "https://example.com/article"
}
```

The response may be JSON or plain text. If JSON is returned, the wrapper prefers the `markdown` field.

## Quick Start

### 1. Run a compatible parser service

For example, run a local instance of `to_markdown` so that it is reachable at:

```text
http://127.0.0.1:9999
```

### 2. Fetch Markdown

```powershell
$env:TO_MARKDOWN_BASE_URL="http://127.0.0.1:9999"
python .\scripts\fetch_to_markdown.py "https://mp.weixin.qq.com/s/example"
```

### 3. Save as an Obsidian note

```powershell
python .\scripts\fetch_to_markdown.py "https://mp.weixin.qq.com/s/example" --json-out result.json
python .\scripts\save_obsidian_note.py --input-json result.json --output-dir "E:\Notes\Inbox"
```

## Repository Layout

```text
wechat-to-markdown-skill/
├── SKILL.md
├── README.md
└── scripts/
    ├── fetch_to_markdown.py
    └── save_obsidian_note.py
```

## Limitations

- Depends on an external parser service
- Some WeChat articles may fail due to anti-bot behavior or network restrictions
- This repository does not publish to WeChat; it only ingests article pages into Markdown
