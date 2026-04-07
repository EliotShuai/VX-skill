import argparse
import json
import os
import sys
from typing import Any, Dict, Optional, Tuple

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch article Markdown from a to_markdown-compatible service."
    )
    parser.add_argument("url", help="Article URL to convert into Markdown.")
    parser.add_argument(
        "--base-url",
        default=os.getenv("TO_MARKDOWN_BASE_URL", "http://127.0.0.1:9999"),
        help="Base URL for the parser service.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.getenv("TO_MARKDOWN_TIMEOUT", "30")),
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--json-out",
        help="Optional path to write normalized JSON output.",
    )
    parser.add_argument(
        "--markdown-out",
        help="Optional path to write only the Markdown output.",
    )
    return parser.parse_args()


def call_parser(base_url: str, url: str, timeout: int) -> Tuple[Any, str]:
    endpoint = base_url.rstrip("/") + "/resolve/mark"
    response = requests.post(endpoint, json={"blogUrl": url}, timeout=timeout)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return response.json(), endpoint

    try:
        return response.json(), endpoint
    except ValueError:
        return response.text, endpoint


def extract_markdown(payload: Any) -> str:
    if isinstance(payload, str):
        return payload

    if isinstance(payload, dict):
        for key in ("markdown", "md", "content", "data"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value

    raise ValueError("Unable to extract Markdown from parser response.")


def extract_title(payload: Any, url: str) -> Optional[str]:
    if isinstance(payload, dict):
        for key in ("title", "name"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def normalize_output(payload: Any, source_url: str, endpoint: str) -> Dict[str, Any]:
    markdown = extract_markdown(payload)
    title = extract_title(payload, source_url)
    source_type = "wechat" if "mp.weixin.qq.com" in source_url else "web"

    return {
        "title": title,
        "source_url": source_url,
        "source_type": source_type,
        "parser_endpoint": endpoint,
        "markdown": markdown,
        "raw": payload,
    }


def write_text(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def write_json(path: str, payload: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> int:
    args = parse_args()

    try:
        payload, endpoint = call_parser(args.base_url, args.url, args.timeout)
        normalized = normalize_output(payload, args.url, endpoint)
    except requests.RequestException as exc:
        print(f"Parser request failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Failed to normalize parser output: {exc}", file=sys.stderr)
        return 1

    if args.json_out:
        write_json(args.json_out, normalized)

    if args.markdown_out:
        write_text(args.markdown_out, normalized["markdown"])

    if not args.json_out and not args.markdown_out:
        print(normalized["markdown"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

