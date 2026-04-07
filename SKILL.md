---
name: wechat-to-markdown
description: Convert article URLs, especially WeChat official account links, into Markdown for Obsidian or local notes by calling a configured to_markdown service. Use when the user wants to ingest a public article URL, save it as Markdown, add frontmatter, or normalize it into an Obsidian-friendly note. This skill wraps an existing parser service rather than reimplementing page extraction.
---

# WeChat To Markdown

This skill converts article URLs into Markdown by calling a configured `to_markdown` service, then optionally normalizes the result into an Obsidian-friendly note.

The underlying parser is [`liangtengyu/to_markdown`](https://github.com/liangtengyu/to_markdown). This skill is the workflow wrapper, not the parser itself.

## When to Use

Use this skill when the user wants to:
- convert a WeChat official account article URL into Markdown
- ingest a public article URL into Obsidian
- add frontmatter and save the article as a note
- normalize parser output into a stable local file

Do not use this skill when:
- the user only wants a summary of already-provided text
- the URL is private, paywalled, or requires interactive login not available to the parser
- the user needs publishing to WeChat rather than importing from WeChat

## Required Inputs

- an article URL

Optional inputs:
- output directory
- note title override
- tags
- whether to save raw parser output or normalized Markdown

## Execution Flow

1. Call `scripts/fetch_to_markdown.py` with the article URL.
2. The script sends `POST {base_url}/resolve/mark` with JSON body:
   - `{"blogUrl": "<article-url>"}`
3. The script extracts Markdown from the response.
4. If the user wants a saved note, call `scripts/save_obsidian_note.py`.

## Configuration

The fetch script reads these environment variables:

- `TO_MARKDOWN_BASE_URL`
  - default: `http://127.0.0.1:9999`
- `TO_MARKDOWN_TIMEOUT`
  - default: `30`

The save script accepts explicit CLI arguments and does not require env vars.

## Output Contract

The parser response may be:
- a JSON object containing `markdown`
- a JSON object containing text-like fields
- plain text

Always normalize the result before presenting it as final output.

## Save Rules

When saving to Obsidian:
- prefer a filename derived from title, sanitized for Windows
- include frontmatter with:
  - `title`
  - `source_url`
  - `source_type: wechat` when the URL is a WeChat article
  - `created_at`
  - `tags`
- preserve the original source URL in the note body or frontmatter

## Failure Handling

If the parser call fails:
- report whether the base service was unreachable, timed out, or returned non-JSON output
- do not invent article contents
- suggest checking whether the `to_markdown` service is running

## Scripts

- `scripts/fetch_to_markdown.py`
  - fetches Markdown from the parser service
- `scripts/save_obsidian_note.py`
  - writes normalized Markdown to a target directory

