#!/usr/bin/env python3
# TODO: split _wechat_delivery_render.py into smaller modules/components
from __future__ import annotations

import html
import re
from pathlib import Path

from _wechat_design_catalog import build_design_catalog, select_design_profile
from _wechat_delivery_shared import compact_html, load_article, pick_meta


def render_article(markdown_path: str, output_path: str, image_map: dict[str, str], design: str, color_mode: str, design_path: str) -> dict[str, str]:
    packet = load_article(markdown_path)
    profile = load_profile(packet.meta, design, color_mode, design_path)
    author_cfg = load_author_config(markdown_path)
    blocks = render_blocks(packet.body.splitlines(), profile, image_map, bool(pick_meta(packet.meta, "title")))
    cta_block = render_cta(author_cfg, profile, image_map)
    document = wrap_document(packet.meta, blocks + cta_block, profile, image_map)
    Path(output_path).write_text(document, encoding="utf-8")
    return {"html": output_path, "title": pick_meta(packet.meta, "title"), "colorMode": str(profile["mode"]), "designId": str(profile["id"]), "designName": str(profile["name"]), "ctaId": str(profile["cta"]["id"])}


def load_profile(meta: dict[str, str], design: str, color_mode: str, design_path: str) -> dict[str, object]:
    try:
        return select_design_profile(build_design_catalog(design_path), meta, design, color_mode)
    except Exception:
        mode = "dark" if color_mode == "dark" else "light"
        base = "#0F172A" if mode == "dark" else "#FFFDF8"
        text = "#F8FAFC" if mode == "dark" else "#1F2937"
        return {"id": "fallback", "name": f"Fallback {mode.title()}", "mode": mode, "background": base, "surface": "#111827" if mode == "dark" else "#FFFFFF", "text": text, "muted": "#CBD5E1" if mode == "dark" else "#6B7280", "accent": "#7DD3FC" if mode == "dark" else "#C08457", "line": "#334155" if mode == "dark" else "#E5DCCF", "radius": 18, "heading": {"size": 20}, "body": {"size": 16}, "title": {"size": 34}, "intro": {"size": 15}, "meta": {"size": 14}, "quote": {"size": 14}, "hero": {"kind": "none", "fill": "transparent", "height": 0}, "flags": {"headerBar": False, "heroOverlay": False, "sectionNumbers": False, "quoteMarker": False}, "cta": {"id": "fallback-cta"}}


def render_blocks(lines: list[str], profile: dict[str, object], image_map: dict[str, str], has_title: bool) -> str:
    blocks, index, state = [], 0, {"sections": 0}
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        block, index = consume_block(lines, index, profile, image_map, has_title, state)
        blocks.append(block)
    return "".join(blocks)


def consume_block(lines: list[str], index: int, profile: dict[str, object], image_map: dict[str, str], has_title: bool, state: dict[str, int]) -> tuple[str, int]:
    line = lines[index].strip()
    if line.startswith("```"):
        return consume_code(lines, index, profile)
    if re.match(r"^#{1,4}\s", line):
        return consume_heading(line, index, profile, has_title, state)
    if image_line(line):
        return render_image(line, index, profile, image_map)
    if is_table_start(lines, index):
        return consume_table(lines, index, profile)
    if list_line(line):
        return consume_list(lines, index, profile)
    if line.startswith(">"):
        return consume_quote(lines, index, profile)
    return consume_paragraph(lines, index, profile)


def consume_code(lines: list[str], index: int, profile: dict[str, object]) -> tuple[str, int]:
    chunk, marker = [], lines[index].strip()
    index += 1
    while index < len(lines) and not lines[index].strip().startswith("```"):
        chunk.append(lines[index])
        index += 1
    label = marker[3:].strip()
    lead = f'<p style="margin:0 0 8px;color:{profile["accent"]};font-size:12px;font-family:Menlo,Monaco,Consolas,monospace;">{html.escape(label)}</p>' if label else ""
    code_bg = _code_bg(profile)
    code_fg = _code_fg(profile)
    block = f'<section style="margin:16px 0;padding:16px 18px;background:{code_bg};border:1px solid {profile["line"]};border-radius:{min(int(profile["radius"]), 10)}px;overflow-x:auto;">{lead}<pre style="margin:0;white-space:pre-wrap;overflow-wrap:anywhere;font-family:Menlo,Monaco,Consolas,monospace;font-size:13px;line-height:1.6;color:{code_fg};"><code>{html.escape(chr(10).join(chunk))}</code></pre></section>'
    return block, min(index + 1, len(lines))


def _code_bg(profile: dict[str, object]) -> str:
    if profile["mode"] == "dark":
        return "#020617"
    return "#F8FAFC"


def _code_fg(profile: dict[str, object]) -> str:
    if profile["mode"] == "dark":
        return "#4ADE80"
    return "#1E293B"


def consume_heading(line: str, index: int, profile: dict[str, object], has_title: bool, state: dict[str, int]) -> tuple[str, int]:
    raw = len(line) - len(line.lstrip("#"))
    level = min(raw + (1 if has_title else 0), 4)
    size = max(int(profile["heading"]["size"]) - max(level - 2, 0) * 2, 18) if level > 1 else int(profile["title"]["size"])
    kicker = ""
    if raw >= 2 and profile["flags"]["sectionNumbers"]:
        state["sections"] += 1
        kicker = f'<p style="margin:0 0 6px;color:{profile["accent"]};font-size:12px;font-weight:700;">{state["sections"]:02d}</p>'
    text = inline_markup(line[raw:].strip())
    border = f"padding-bottom:10px;border-bottom:1px solid {profile['line']};" if level <= 3 else ""
    margin_top = "36px" if level <= 3 else "26px"
    block = f'<section style="margin:{margin_top} 0 14px;">{kicker}<h{level} style="margin:0;color:{profile["text"]};font-size:{size}px;font-weight:700;line-height:1.35;{border}">{text}</h{level}></section>'
    return block, index + 1


def render_image(line: str, index: int, profile: dict[str, object], image_map: dict[str, str]) -> tuple[str, int]:
    alt, src = image_line(line)
    target = image_map.get(src, src)
    caption = f'<p style="margin:8px 0 0;color:{profile["muted"]};font-size:12px;text-align:center;">{html.escape(alt)}</p>' if alt else ""
    block = f'<section style="margin:20px 0;"><img src="{html.escape(target)}" alt="{html.escape(alt)}" style="display:block;width:100%;border-radius:{min(int(profile["radius"]), 12)}px;" loading="lazy" />{caption}</section>'
    return block, index + 1


def consume_table(lines: list[str], index: int, profile: dict[str, object]) -> tuple[str, int]:
    rows = []
    while index < len(lines) and "|" in lines[index]:
        rows.append(split_row(lines[index]))
        index += 1
    head, body = rows[0], rows[2:] if len(rows) > 1 and separator_row(rows[1]) else rows[1:]
    thead = "".join(f'<th style="padding:10px;border:1px solid {profile["line"]};text-align:left;color:{profile["text"]};">{inline_markup(cell)}</th>' for cell in head)
    tbody = "".join(f'<tr>{"".join(f"""<td style="padding:10px;border:1px solid {profile["line"]};vertical-align:top;color:{profile["text"]};">{inline_markup(cell)}</td>""" for cell in row)}</tr>' for row in body)
    return f'<section style="margin:18px 0;"><table style="width:100%;border-collapse:collapse;background:{profile["surface"]};"><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></section>', index


def consume_list(lines: list[str], index: int, profile: dict[str, object]) -> tuple[str, int]:
    items, ordered = [], bool(re.match(r"^\d+\.\s", lines[index].strip()))
    while index < len(lines) and list_line(lines[index].strip()):
        items.append(f"<li>{inline_markup(re.sub(r'^([-*]|\\d+\\.)\\s+', '', lines[index].strip()))}</li>")
        index += 1
    tag = "ol" if ordered else "ul"
    return f'<section style="margin:14px 0;color:{profile["text"]};"><{tag} style="padding-left:24px;margin:0;">{"".join(items)}</{tag}></section>', index


def consume_quote(lines: list[str], index: int, profile: dict[str, object]) -> tuple[str, int]:
    chunk = []
    while index < len(lines) and lines[index].strip().startswith(">"):
        chunk.append(lines[index].strip().lstrip(">").strip())
        index += 1
    marker = f'<p style="margin:0 0 8px;color:{profile["accent"]};font-size:20px;font-weight:800;">//</p>' if profile["flags"]["quoteMarker"] else ""
    text = "<br />".join(inline_markup(item) for item in chunk)
    block = f'<section style="margin:18px 0;padding:16px 18px;border-left:4px solid {profile["accent"]};background:{profile["surface"]};color:{profile["muted"]};border-radius:{max(int(profile["radius"]) - 6, 8)}px;">{marker}{text}</section>'
    return block, index


def consume_paragraph(lines: list[str], index: int, profile: dict[str, object]) -> tuple[str, int]:
    chunk = []
    while index < len(lines) and lines[index].strip() and not block_break(lines, index):
        chunk.append(lines[index].strip())
        index += 1
    text = inline_markup(" ".join(chunk))
    return f'<section style="margin:0 0 16px;"><p style="margin:0;color:{profile["muted"] if text.startswith("注：") else profile["text"]};font-size:{profile["body"]["size"]}px;line-height:1.9;">{text}</p></section>', index


def wrap_document(meta: dict[str, str], blocks: str, profile: dict[str, object], image_map: dict[str, str]) -> str:
    title, author, digest = inline_markup(pick_meta(meta, "title", "Untitled Article")), inline_markup(pick_meta(meta, "author")), inline_markup(pick_meta(meta, "digest"))
    cover = image_map.get(pick_meta(meta, "coverImage"), pick_meta(meta, "coverImage"))
    bar = f'<section style="height:8px;background:{profile["accent"]};margin:0 0 18px;border-radius:{profile["radius"]}px;"></section>' if profile["flags"]["headerBar"] else ""
    hero = render_hero(meta, profile, cover, title, author, digest)
    meta_line = f'<p style="margin:0 0 12px;color:{profile["muted"]};font-size:{profile["meta"]["size"]}px;">{author}</p>' if author else ""
    digest_block = f'<section style="margin:0 0 22px;padding:16px 18px;background:{profile["surface"]};border:1px solid {profile["line"]};border-radius:{profile["radius"]}px;"><p style="margin:0;color:{profile["text"]};font-size:{profile["intro"]["size"]}px;line-height:1.8;">{digest}</p></section>' if digest and not hero else ""
    intro = "" if hero else f'<section style="margin:0 0 24px;"><h1 style="margin:0 0 10px;color:{profile["text"]};font-size:{profile["title"]["size"]}px;line-height:1.25;">{title}</h1>{meta_line}</section>'
    body = f'<section style="background:{profile["background"]};padding:28px 18px;margin:0;"><section style="max-width:760px;margin:0 auto;background:{profile["background"]};">{bar}{hero}{intro}{digest_block}{blocks}</section></section>'
    head = f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="color-scheme" content="{profile["mode"]}" /><title>{html.escape(pick_meta(meta, "title", "Article"))}</title></head><body style="margin:0;background:{profile["background"]};">{body}</body></html>'
    return compact_html(head) + "\n"


def render_hero(meta: dict[str, str], profile: dict[str, object], cover: str, title: str, author: str, digest: str) -> str:
    if cover and not profile["flags"]["heroOverlay"]:
        return f'<section style="margin:0 0 18px;"><img src="{html.escape(cover)}" alt="{html.escape(pick_meta(meta, "title"))}" style="display:block;width:100%;border-radius:{profile["radius"] + 4}px;" /></section>'
    if profile["hero"]["kind"] == "none" and not cover:
        return ""
    visual = f"background:{profile['hero']['fill']};"
    meta_line = f'<p style="margin:10px 0 0;color:{profile["muted"]};font-size:{profile["meta"]["size"]}px;">{author}</p>' if author else ""
    digest_line = f'<p style="margin:14px 0 0;color:{profile["muted"]};font-size:{profile["intro"]["size"]}px;line-height:1.8;">{digest}</p>' if digest else ""
    return f'<section style="margin:0 0 24px;padding:32px 24px;min-height:{max(int(profile["hero"]["height"]), 220)}px;display:block;{visual}border-radius:{profile["radius"] + 4}px;"><h1 style="margin:0;color:{profile["text"]};font-size:{max(profile["title"]["size"], 32)}px;line-height:1.2;">{title}</h1>{meta_line}{digest_line}</section>'


def block_break(lines: list[str], index: int) -> bool:
    current = lines[index].strip()
    return bool(current.startswith(("```", ">", "#")) or image_line(current) or list_line(current) or is_table_start(lines, index))


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r'<code style="background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;font-family:Menlo,Monaco,Consolas,monospace;font-size:0.9em;">\1</code>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", escaped)


def image_line(line: str) -> tuple[str, str] | None:
    match = re.match(r"^!\[(.*?)\]\(([^)]+)\)$", line)
    return (match.group(1), match.group(2)) if match else None


def list_line(line: str) -> bool:
    return bool(re.match(r"^([-*]|\d+\.)\s", line))


def is_table_start(lines: list[str], index: int) -> bool:
    return "|" in lines[index] and index + 1 < len(lines) and separator_row(split_row(lines[index + 1]))


def separator_row(row: list[str]) -> bool:
    return all(set(cell) <= {"-", ":"} for cell in row if cell)


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def load_author_config(markdown_path: str) -> dict[str, object]:
    """Load EXTEND.md from project dir, ~/.config/research-to-wechat, or ~/.research-to-wechat."""
    project = Path(markdown_path).resolve().parent
    candidates = [
        project / "EXTEND.md",
        project.parent / "EXTEND.md",
        Path.home() / ".config" / "research-to-wechat" / "EXTEND.md",
        Path.home() / ".research-to-wechat" / "EXTEND.md",
    ]
    for path in candidates:
        if path.is_file():
            return _parse_extend(path.read_text(encoding="utf-8"))
    return {}


def _parse_extend(text: str) -> dict[str, object]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    raw = parts[1].strip()
    result: dict[str, object] = {}
    current_section = ""
    for line in raw.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if not stripped.startswith((" ", "\t")) and ":" in stripped:
            key, val = stripped.split(":", 1)
            val = val.strip()
            if not val:
                current_section = key.strip()
                result[current_section] = {}
            else:
                result[key.strip()] = _yaml_val(val)
        elif current_section and isinstance(result.get(current_section), dict) and ":" in stripped:
            key, val = stripped.strip().split(":", 1)
            result[current_section][key.strip()] = _yaml_val(val.strip())
    return result


def _yaml_val(v: str) -> object:
    v = v.strip()
    if v.lower() in ("true", "yes"):
        return True
    if v.lower() in ("false", "no"):
        return False
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    return v


def render_cta(author_cfg: dict[str, object], profile: dict[str, object], image_map: dict[str, str]) -> str:
    cta = author_cfg.get("cta")
    if not isinstance(cta, dict) or cta.get("enabled") is False:
        return ""
    heading = str(cta.get("heading", ""))
    body = str(cta.get("body", ""))
    footer = str(cta.get("footer", ""))
    blog_url = str(cta.get("blog_url", ""))
    interactions = str(cta.get("interactions", ""))
    qr_src = str(cta.get("qr_image", ""))
    qr_url = image_map.get(qr_src, image_map.get(f"imgs/{qr_src}", qr_src))
    parts = []
    if heading:
        parts.append(f'<p style="margin:0 0 16px;font-size:16px;color:{profile["text"]};font-weight:600;">{html.escape(heading)}</p>')
    if qr_url:
        parts.append(f'<section style="margin:0 0 16px;"><img src="{html.escape(qr_url)}" alt="QR" style="display:block;width:120px;margin:0 auto;border-radius:8px;" /></section>')
    if body:
        parts.append(f'<p style="margin:0 0 12px;font-size:14px;color:{profile["muted"]};line-height:1.7;">{html.escape(body)}</p>')
    if footer:
        parts.append(f'<p style="margin:0 0 16px;font-size:13px;color:{profile["muted"]};opacity:0.7;">{html.escape(footer)}</p>')
    if blog_url:
        parts.append(f'<section style="margin:0 0 12px;padding:10px 16px;background:{profile["background"]};border-radius:6px;display:inline-block;"><p style="margin:0;font-size:13px;color:{profile["muted"]};">无删减全文请移步 {html.escape(blog_url)}</p></section>')
    if interactions:
        parts.append(f'<p style="margin:12px 0 0;font-size:13px;color:{profile["muted"]};opacity:0.7;">{html.escape(interactions)}</p>')
    if not parts:
        return ""
    inner = "".join(parts)
    return f'<section style="margin:40px 0 20px;padding:28px 20px;background:{profile["surface"]};border-radius:{min(int(profile["radius"]), 12)}px;text-align:center;">{inner}</section>'
