# web-to-obsidian

[English](./README.md) | [简体中文](./README.zh-CN.md)

将公开网页文章，尤其是微信公众号文章，导入为适合 Obsidian 使用的 Markdown 笔记。

## 仓库定位

这个仓库提供的是一个 `web-to-obsidian` skill，用于把下面这条链路做完整：

`URL -> 网页正文 -> Markdown -> frontmatter -> 本地 Obsidian 笔记`

它不是单纯的网页读取工具，也不是单纯的 Markdown 转换器，而是一个完整的“抓取并落库”工作流。

## 底层依赖

本仓库**不再使用** `to_markdown`。

底层获取策略改为参考并依赖 [`eze-is/web-access`](https://github.com/eze-is/web-access)：

- 先尝试最低成本的可行路径
- 只有在失败或内容不完整时，才升级到浏览器/CDP
- 把反爬、动态渲染、环境异常视为“切换路径的信号”

## 核心工作流

尤其针对微信公众号文章：

1. 优先用移动端 User-Agent 直接请求页面
2. 从 HTML 中提取：
   - 标题
   - 作者
   - 正文
3. 将正文规范化为 Markdown
4. 加上 Obsidian 所需的 frontmatter
5. 写入用户指定目录

如果直连请求失败：
- 再切换到 `web-access` 的浏览器/CDP 路线

## 仓库内容

```text
web-to-obsidian/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── requirements.txt
└── scripts/
    └── save_obsidian_note.py
```

## 相比通用网页 skill 增加了什么

这个仓库在通用联网能力之上，额外补了：

- 面向文章的抽取规则
- 微信公众号专用选择器
- Markdown 清洗规则
- Obsidian frontmatter 规范
- 本地笔记落库行为

## 说明

- `web-access` 负责“怎么读到网页”
- 本仓库负责“怎么把文章变成 Obsidian 笔记”
- 对于私有页面、强登录态页面，仍可能需要浏览器/CDP 路径

