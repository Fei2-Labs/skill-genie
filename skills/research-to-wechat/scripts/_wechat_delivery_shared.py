#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse


@dataclass
class ArticlePacket:
    meta: dict[str, str]
    body: str


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


def load_json(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    data = json.loads(read_text(path))
    return {str(key): str(value) for key, value in data.items()}


def dump_json(data: object, path: str | None) -> None:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        write_text(path, payload + "\n")
        return
    print(payload)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    _, head, body = text.split("---\n", 2)
    return parse_frontmatter(head), body.lstrip()


def parse_frontmatter(block: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for raw in block.splitlines():
        if ":" not in raw or raw.startswith((" ", "\t")):
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = strip_quotes(value.strip())
    return meta


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_article(path: str) -> ArticlePacket:
    meta, body = split_frontmatter(read_text(path))
    return ArticlePacket(meta=meta, body=body)


def normalize_markdown_links(path: str) -> bool:
    original = read_text(path)
    normalized = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", original)
    if normalized == original:
        return False
    write_text(path, normalized)
    return True


def pick_meta(meta: dict[str, str], key: str, default: str = "") -> str:
    return meta.get(key, default).strip()


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return cleaned.strip("-") or "article"


def query_value(value: str | None, key: str) -> str:
    if not value:
        return ""
    query = parse_qs(urlparse(value).query)
    return query.get(key, [""])[0]


def resolve_token(explicit: str | None, url: str | None) -> str:
    return explicit or query_value(url, "token")


def resolve_appmsgid(explicit: str | None, url: str | None) -> str:
    return explicit or query_value(url, "appmsgid") or query_value(url, "AppMsgId")


def compact_html(text: str) -> str:
    return re.sub(r">\s+<", "><", text.replace("\n", " ")).strip()
