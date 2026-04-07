# wechat-to-markdown-skill

[English](./README.md) | [简体中文](./README.zh-CN.md)

一个面向 Obsidian / 本地笔记场景的 Skill 包装层，用于将网页文章链接，尤其是微信公众号文章链接，转换为 Markdown，并保存为适合 Obsidian 使用的笔记文件。

## 致谢与底层依赖

本 Skill 使用 [`liangtengyu/to_markdown`](https://github.com/liangtengyu/to_markdown) 作为底层解析器，将支持的网站文章页面转换为 Markdown。

- 上游解析器仓库：[liangtengyu/to_markdown](https://github.com/liangtengyu/to_markdown)
- 上游仓库许可证：Apache-2.0

本仓库的职责是：
- 封装调用流程
- 规范输出格式
- 对接 Obsidian / 本地知识库

本仓库**不重新实现网页解析器本身**。

## 这个 Skill 能做什么

- 调用配置好的 `to_markdown` 服务
- 将公众号文章链接转换为 Markdown
- 从解析结果中提取正文
- 可选地保存为本地 Obsidian 笔记
- 自动补充基础 frontmatter

## 预期的解析服务接口

这个包装层默认假设底层解析服务兼容以下接口：

- `POST /resolve/mark`
- 请求体：

```json
{
  "blogUrl": "https://mp.weixin.qq.com/s/example"
}
```

返回结果可以是：
- JSON
- 纯文本

如果返回 JSON，本仓库优先提取这些字段中的正文：
- `markdown`
- `md`
- `content`
- `data`

## 快速开始

### 1. 启动一个兼容的 `to_markdown` 服务

例如让它在本地监听：

```text
http://127.0.0.1:9999
```

### 2. 获取 Markdown

```powershell
$env:TO_MARKDOWN_BASE_URL="http://127.0.0.1:9999"
python .\scripts\fetch_to_markdown.py "https://mp.weixin.qq.com/s/example"
```

### 3. 保存为 Obsidian 笔记

```powershell
python .\scripts\fetch_to_markdown.py "https://mp.weixin.qq.com/s/example" --json-out result.json
python .\scripts\save_obsidian_note.py --input-json result.json --output-dir "E:\Notes\Inbox"
```

## 配置说明

### 环境变量

`fetch_to_markdown.py` 支持以下环境变量：

- `TO_MARKDOWN_BASE_URL`
  - 默认值：`http://127.0.0.1:9999`
- `TO_MARKDOWN_TIMEOUT`
  - 默认值：`30`

### Python 依赖

安装依赖：

```powershell
pip install -r .\requirements.txt
```

## 目录结构

```text
wechat-to-markdown-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── requirements.txt
└── scripts/
    ├── fetch_to_markdown.py
    └── save_obsidian_note.py
```

## 脚本说明

### `scripts/fetch_to_markdown.py`

作用：
- 调用底层解析服务
- 抽取标准化 Markdown
- 可输出纯 Markdown
- 也可输出标准化 JSON 结果

输出的标准化 JSON 里通常包含：
- `title`
- `source_url`
- `source_type`
- `parser_endpoint`
- `markdown`
- `raw`

### `scripts/save_obsidian_note.py`

作用：
- 读取标准化 JSON
- 生成带 frontmatter 的 Markdown 笔记
- 按标题生成安全文件名
- 写入指定目录

默认 frontmatter 包含：
- `title`
- `source_url`
- `source_type`
- `created_at`
- `tags`

## 适用场景

适合：
- 微信公众号文章归档
- 网页转 Markdown
- 导入 Obsidian
- 给 AI 后续做摘要、标签、知识整理提供干净输入

不适合：
- 发布文章到微信公众号
- 读取必须登录后才能访问的私有内容
- 依赖浏览器会话、验证码或强交互页面的抓取

## 当前限制

- 依赖外部解析服务运行正常
- 部分公众号页面可能受反爬、网络环境或地区访问限制影响
- 该仓库只负责“调用与落库”，不保证所有网页都能被稳定解析

## 后续可扩展方向

- 自动提取作者、发布时间、封面图
- 自动写入 Obsidian 指定目录结构
- 自动生成摘要、标签和引用卡片
- 支持批量导入链接列表
- 增加更贴近 Codex Skill 的安装说明
