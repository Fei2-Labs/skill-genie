#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

CTA_BY_FAMILY = {"03": "wyyNI", "04": "5hruL", "06": "wyyNI", "08": "vj1H4", "09": "U5FfV", "10": "Z7dEq"}
FRAME_HINTS = {"deep-analysis": "09", "tutorial": "04", "newsletter": "02", "case-study": "09", "commentary": "02", "narrative": "05", "trend-report": "04", "founder-letter": "01"}
TOPIC_HINTS = [
    (("ai", "agent", "code", "claude", "dev", "program", "tech", "模型", "编程", "技术", "开发", "工具"), "04"),
    (("business", "strategy", "management", "finance", "商业", "战略", "管理", "企业", "转型"), "09"),
    (("design", "brand", "creative", "视觉", "设计", "品牌", "创意"), "07"),
    (("culture", "history", "humanities", "哲学", "文化", "历史", "人文"), "06"),
    (("news", "opinion", "critique", "评论", "观点", "时评"), "02"),
    (("fun", "community", "青年", "社区"), "08"),
    (("art", "music", "film", "艺术", "音乐", "电影"), "10"),
    (("life", "emotion", "growth", "wellness", "生活", "情绪", "成长"), "05"),
]


def build_design_catalog(path: str) -> dict[str, list[dict[str, object]]]:
    frames = json.loads(Path(path).read_text(encoding="utf-8")).get("children", [])
    designs, ctas = [], []
    for frame in frames:
        profile = build_profile(frame)
        (ctas if profile["kind"] == "cta" else designs).append(profile)
    return {"designs": sorted(designs, key=lambda item: (str(item["family"]), str(item["mode"]))), "ctas": sorted(ctas, key=lambda item: str(item["name"]))}


def select_design_profile(catalog: dict[str, list[dict[str, object]]], meta: dict[str, str], hint: str, mode_hint: str) -> dict[str, object]:
    direct = match_design(catalog["designs"], hint)
    family = direct["family"] if direct else resolve_family(meta, hint)
    mode = direct["mode"] if direct else resolve_mode(meta, hint, mode_hint)
    selected = direct or next((item for item in catalog["designs"] if item["family"] == family and item["mode"] == mode), None)
    selected = selected or next((item for item in catalog["designs"] if item["family"] == family), None) or catalog["designs"][0]
    cta_id = CTA_BY_FAMILY.get(str(selected["family"]), "U5FfV" if selected["mode"] == "dark" else "YCqgA")
    cta = next((item for item in catalog["ctas"] if item["id"] == cta_id), None) or catalog["ctas"][0]
    return {**selected, "cta": cta}


def build_profile(frame: dict[str, object]) -> dict[str, object]:
    name, texts = str(frame.get("name", "")), collect_texts(frame)
    family, label, mode = parse_name(name)
    title = choose_text(texts, ("articletitle", "title"), ("cta", "hero", "sub", "footer", "badge", "scan", "qr"), 28)
    intro = choose_text(texts, ("intro", "subtitle", "desc"), ("cta", "hero", "footer"), 15)
    heading = choose_text(texts, ("h2", "sec", "featuretitle"), ("cta", "hero"), 20)
    body = choose_text(texts, ("body", "feat", "tipbody"), ("cta", "footer"), 15)
    meta = choose_text(texts, ("author", "meta", "date"), ("cta", "footer"), 13)
    quote = choose_text(texts, ("quote",), ("cta", "author"), 14)
    badge = choose_text(texts, ("badge", "label", "cmd", "trust"), ("ctabtn",), 12)
    hero, content = find_frame(frame, ("hero", "headerbar", "hdr")), find_frame(frame, ("content", "wrap"))
    base = fill_css(frame.get("fill"), "#FFFFFF" if mode == "light" else "#0F172A")
    return {
        "kind": "cta" if name.startswith("CTA") else "article",
        "id": str(frame.get("id", "")),
        "name": name,
        "family": family,
        "label": label,
        "mode": mode,
        "background": base,
        "surface": fill_css(content.get("fill"), base) if content else base,
        "text": title.get("fill") or "#111111",
        "muted": intro.get("fill") or meta.get("fill") or "#6B7280",
        "accent": first_color(quote.get("fill"), badge.get("fill"), heading.get("fill"), title.get("fill")) or "#3B82F6",
        "line": stroke_color(frame) or stroke_color(content) or "#CBD5E1",
        "radius": int((content or frame).get("cornerRadius", 20) or 20),
        "gap": int(frame.get("gap", 24) or 24),
        "padding": int(frame.get("padding", 28) or 28) if isinstance(frame.get("padding"), int) else 28,
        "hero": {"kind": fill_kind(hero.get("fill")), "fill": fill_css(hero.get("fill"), "transparent"), "height": int(hero.get("height", 260) or 260)} if hero else {"kind": "none", "fill": "transparent", "height": 0},
        "title": slim_text(title),
        "intro": slim_text(intro),
        "heading": slim_text(heading),
        "body": slim_text(body),
        "meta": slim_text(meta),
        "quote": slim_text(quote),
        "flags": {
            "headerBar": has_name(frame, ("headerbar", "hdr")),
            "heroOverlay": has_name(frame, ("herotitle",)),
            "sectionNumbers": has_name(frame, ("sec1num", "sec2num", "sec3num")),
            "quoteMarker": has_name(frame, ("quotemarker",)),
        },
    }


def parse_name(name: str) -> tuple[str, str, str]:
    match = re.match(r"^(\d+)\s+(.+?)\s+(Light|Dark)$", name)
    return (match.group(1), match.group(2), match.group(3).lower()) if match else ("cta", name.replace("CTA - ", ""), "dark" if "Dark" in name else "light")


def resolve_family(meta: dict[str, str], hint: str) -> str:
    lowered = " ".join((hint, meta.get("title", ""), meta.get("description", ""), meta.get("digest", ""), meta.get("styleMode", ""))).lower()
    for keywords, family in TOPIC_HINTS:
        if any(word in lowered for word in keywords):
            return family
    return FRAME_HINTS.get(meta.get("structureFrame", "").strip().lower(), "01")


def resolve_mode(meta: dict[str, str], hint: str, mode_hint: str) -> str:
    if mode_hint in {"light", "dark"}:
        return mode_hint
    return "dark" if "dark" in f"{hint} {meta.get('styleMode', '')}".lower() else "light"


def match_design(designs: list[dict[str, object]], hint: str) -> dict[str, object] | None:
    lowered = hint.lower().strip()
    if not lowered:
        return None
    for item in designs:
        keys = {str(item["id"]).lower(), str(item["family"]).lower(), str(item["name"]).lower(), str(item["label"]).lower()}
        if lowered in keys or lowered in str(item["name"]).lower():
            return item
    return None


def collect_texts(node: dict[str, object]) -> list[dict[str, object]]:
    items = [node] if node.get("type") == "text" else []
    for child in node.get("children", []):
        items.extend(collect_texts(child))
    return items


def collect_nodes(node: dict[str, object]) -> list[dict[str, object]]:
    items = [node]
    for child in node.get("children", []):
        items.extend(collect_nodes(child))
    return items


def choose_text(texts: list[dict[str, object]], include: tuple[str, ...], exclude: tuple[str, ...], size: int) -> dict[str, object]:
    for node in texts:
        name = str(node.get("name", "")).lower()
        if any(token in name for token in include) and not any(token in name for token in exclude):
            return node
    ranked = sorted(texts, key=lambda item: abs(int(item.get("fontSize", size) or size) - size))
    return ranked[0] if ranked else {}


def find_frame(node: dict[str, object], names: tuple[str, ...]) -> dict[str, object]:
    for child in node.get("children", []):
        if child.get("type") == "frame" and any(token in str(child.get("name", "")).lower() for token in names):
            return child
    return {}


def has_name(node: dict[str, object], names: tuple[str, ...]) -> bool:
    return any(any(token in str(child.get("name", "")).lower() for token in names) for child in collect_nodes(node))


def fill_kind(fill: object) -> str:
    return str(fill.get("type", "color")) if isinstance(fill, dict) else "color"


def fill_css(fill: object, fallback: str) -> str:
    if isinstance(fill, str) and fill:
        return fill
    if isinstance(fill, dict) and fill.get("type") == "gradient":
        stops = ", ".join(f"{item['color']} {int(float(item['position']) * 100)}%" for item in fill.get("colors", []))
        return f"linear-gradient({int(fill.get('rotation', 180))}deg, {stops})"
    if isinstance(fill, dict) and fill.get("type") == "image":
        return f"url('{fill.get('url', '')}') center/cover no-repeat"
    return fallback


def stroke_color(node: dict[str, object] | None) -> str:
    stroke = (node or {}).get("stroke")
    return str(stroke.get("fill", "")) if isinstance(stroke, dict) else ""


def slim_text(node: dict[str, object]) -> dict[str, object]:
    return {"size": int(node.get("fontSize", 16) or 16), "weight": str(node.get("fontWeight", "normal")), "fill": str(node.get("fill", ""))}


def first_color(*values: object) -> str:
    return next((value for value in values if isinstance(value, str) and value.startswith("#")), "")
