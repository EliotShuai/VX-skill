---
name: web-to-obsidian
description: Ingest a public web page, especially a WeChat official account article, into an Obsidian-friendly Markdown note by combining web-access retrieval strategies with AI cleanup and local note writing. Use when the user wants to read a URL, extract the article body, normalize it into Markdown, add frontmatter, and save it into an Obsidian vault.
---

# web-to-obsidian

This skill turns a public article URL into an Obsidian note.

It does not depend on `to_markdown`. Its retrieval layer is based on the workflow and strategy of [`eze-is/web-access`](https://github.com/eze-is/web-access): choose the lowest-cost successful access path first, then escalate only when needed.

## Purpose

Use this skill when the user wants to:
- read a public web article from a URL
- ingest a WeChat official account article into Obsidian
- convert page content into Markdown
- add frontmatter, source metadata, and tags
- save the result into a local notes directory

Do not use this skill when:
- the user only needs a summary of already-provided text
- the page is private or requires credentials you do not have
- the user wants to publish content outward rather than ingest it

## Dependency

This skill relies on the retrieval philosophy and tooling pattern of [`eze-is/web-access`](https://github.com/eze-is/web-access) as the underlying web acquisition layer.

Use `web-access` for:
- search
- static fetch
- curl / raw HTML retrieval
- Jina fallback when appropriate
- CDP browser access for anti-bot or login-gated pages

This skill adds:
- extraction strategy for article pages
- Markdown normalization
- Obsidian frontmatter rules
- local file writing

## Success Criteria

A task is complete only when all of the following are true:
- title is extracted or safely inferred
- source URL is preserved
- main article body is extracted
- content is normalized into readable Markdown
- note is written into the requested local directory

## Retrieval Strategy

### General Rule

Do not begin by assuming one tool will always work.

Pick the cheapest path that can plausibly succeed, and escalate only when the result is incomplete or blocked.

### For WeChat Official Account Articles

Use this order:

1. **Direct static fetch with mobile UA**
   - preferred first attempt for public WeChat articles
   - reason: some WeChat article pages expose full HTML when requested with a mobile-like user agent
2. **Raw HTML extraction**
   - extract title, author, and article body from the returned DOM
3. **Escalate to `web-access` browser strategy**
   - if the direct fetch returns incomplete HTML, a validation page, or an anti-bot block
   - use CDP-backed browser access through the `web-access` workflow
4. **Only use Jina as an optional lightweight path**
   - acceptable for normal article pages
   - not preferred for WeChat if direct fetch or browser mode is available
   - if Jina triggers "environment anomaly", treat that as a signal to switch methods rather than retry blindly

## WeChat Extraction Rules

When the page is a WeChat public article:

- title selector:
  - `#activity-name .js_title_inner`
- author selector:
  - `#js_author_name`
- body selector:
  - `#js_content`

Before converting body text:
- remove `script` and `style` nodes
- strip empty lines
- preserve paragraph breaks
- keep inline text readable rather than preserving noisy layout wrappers

If body extraction fails:
- report exactly which selector was missing
- do not invent content

## Markdown Normalization Rules

After extraction, normalize the content into Markdown with these rules:

- title becomes top-level heading if not already captured in frontmatter only
- preserve paragraphs as paragraphs
- convert obvious headings into `##` / `###` where structure is clear
- convert quoted or highlighted statements into blockquotes when appropriate
- do not over-format weak structure into fake headings
- preserve the original wording; do not summarize unless the user explicitly asks

## Obsidian Frontmatter Rules

Every saved note should include:

- `title`
- `source_url`
- `source_type`
- `author`
- `created_at`
- `tags`

For WeChat articles use:
- `source_type: wechat`

Example:

```yaml
---
title: "大多数公司，一开始就找错了AI人才"
source_url: "https://mp.weixin.qq.com/s/NBo8avU_geo0iEhK-YzL7A"
source_type: "wechat"
author: "张美吉"
created_at: "2026-04-07T21:00:00"
tags:
  - clipping
  - wechat
---
```

## Local Save Rules

Write the note only after the user gives or confirms an output directory, unless a repository convention already exists.

Preferred output directories:
- Obsidian inbox
- clipping folder
- source article archive folder

Use a Windows-safe filename derived from title.

## Execution Workflow

1. Identify the source type from the URL.
2. If it is a WeChat article:
   - try direct fetch with mobile UA first
   - extract `title`, `author`, `body` from HTML
3. If direct fetch fails or is incomplete:
   - switch to the `web-access` browser workflow
   - use browser DOM extraction for the same fields
4. Normalize the extracted body into Markdown.
5. Build frontmatter.
6. Write the note into the requested Obsidian directory.
7. Report:
   - where the note was saved
   - what retrieval path succeeded

## Failure Handling

If the page cannot be fully extracted:
- report the path that failed:
  - direct fetch
  - Jina
  - CDP browser path
- report whether the failure was:
  - anti-bot block
  - missing content selector
  - network error
  - login requirement
- do not fabricate article contents

## Tooling Guidance

This skill may use bundled scripts for local note writing, but retrieval should follow the `web-access` pattern instead of depending on a dedicated parser service.

If both static fetch and browser mode are available:
- prefer static fetch when it yields complete content
- prefer browser mode when anti-bot, login, or dynamic rendering blocks the static path

## References

- [`eze-is/web-access`](https://github.com/eze-is/web-access)

