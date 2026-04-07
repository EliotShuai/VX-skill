import argparse
import datetime as dt
import json
import os
import re
from typing import Any, Dict, List, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Save normalized parser output as an Obsidian-friendly Markdown note."
    )
    parser.add_argument("--input-json", required=True, help="Path to normalized JSON input.")
    parser.add_argument("--output-dir", required=True, help="Directory to write the note into.")
    parser.add_argument("--title", help="Optional title override.")
    parser.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="Optional list of tags to include in frontmatter.",
    )
    return parser.parse_args()


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\\\|?*]', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:120] or "untitled"


def yaml_escape(value: str) -> str:
    return value.replace('"', '\\"')


def build_frontmatter(title: str, source_url: str, source_type: str, tags: List[str]) -> str:
    created_at = dt.datetime.now().isoformat(timespec="seconds")
    lines = [
        "---",
        f'title: "{yaml_escape(title)}"',
        f'source_url: "{yaml_escape(source_url)}"',
        f'source_type: "{yaml_escape(source_type)}"',
        f'created_at: "{created_at}"',
        "tags:",
    ]

    if tags:
        for tag in tags:
            lines.append(f"  - {tag}")
    else:
        lines.append("  - inbox")

    lines.append("---")
    return "\n".join(lines)


def derive_title(payload: Dict[str, Any], title_override: Optional[str]) -> str:
    if title_override:
        return title_override.strip()
    if payload.get("title"):
        return str(payload["title"]).strip()
    return "untitled"


def write_note(output_dir: str, title: str, content: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, sanitize_filename(title) + ".md")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return path


def main() -> int:
    args = parse_args()
    payload = load_json(args.input_json)

    title = derive_title(payload, args.title)
    source_url = str(payload.get("source_url", "")).strip()
    source_type = str(payload.get("source_type", "web")).strip() or "web"
    markdown = str(payload.get("markdown", "")).strip()

    frontmatter = build_frontmatter(title, source_url, source_type, args.tags)
    body = frontmatter + "\n\n" + markdown + "\n"
    path = write_note(args.output_dir, title, body)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

