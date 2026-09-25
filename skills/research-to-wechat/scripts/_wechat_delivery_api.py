#!/usr/bin/env python3

from __future__ import annotations

import json
import mimetypes
import os
import re
import uuid
from html import unescape
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from _wechat_delivery_shared import load_article, pick_meta


def environment_report() -> dict[str, object]:
    env = {key: bool(os.getenv(key)) for key in ("WECHAT_APPID", "WECHAT_SECRET", "WECHAT_ACCESS_TOKEN", "WECHAT_DRAFT_MEDIA_ID")}
    return {"python": os.sys.executable, "env": env, "officialReady": env["WECHAT_APPID"] and env["WECHAT_SECRET"]}


def upload_images(image_paths: list[str], appid: str, secret: str, access_token: str, dry_run: bool) -> dict[str, str]:
    if dry_run:
        return {path: f"dry-run://{Path(path).name}" for path in image_paths}
    token = access_token or fetch_access_token(appid, secret)
    return {path: upload_content_image(path, token) for path in image_paths}


def save_draft(html_path: str, markdown_path: str, appid: str, secret: str, access_token: str, media_id: str, cover_image: str, cover_type: str, title: str, author: str, digest: str, source_url: str, dry_run: bool) -> dict[str, object]:
    packet = load_article(markdown_path)
    article = draft_article(packet.meta, html_path, cover_image, cover_type, title, author, digest, source_url)
    if dry_run:
        return {"draftStatus": "dry-run", "request": draft_payload(article, media_id)}
    token = access_token or fetch_access_token(appid, secret)
    article["thumb_media_id"] = upload_cover_image(article["cover_image"], token, cover_type)
    payload = draft_payload(article, media_id)
    data = post_json(draft_url(token, media_id), payload)
    result = decode_json(data)
    result["draftStatus"] = "updated" if media_id else "created"
    saved_id = media_id or str(result.get("media_id", ""))
    result["verification"] = verify_draft(saved_id, article, token)
    return result


def update_cover(appid: str, secret: str, access_token: str, media_id: str, cover_image: str, cover_type: str, dry_run: bool) -> dict[str, object]:
    """Swap ONLY the cover of an existing draft, preserving the body verbatim.

    Added 2026-09-25. save-draft rewrites the whole article from local html/markdown,
    which risks body drift and needs a re-render just to change a picture. This reads
    the live draft back with draft/get, uploads the new cover, and draft/update's the
    same media_id changing ONLY thumb_media_id -- title / author / digest / content /
    comment flags are echoed straight back from the live draft, so the body cannot move.

    Like every other write here it still resets 原创 / 赞赏 / 合集 (editor-only fields
    the API cannot touch), so only run it BEFORE those are set in the browser.
    """
    require_value("media_id", media_id)
    require_value("cover_image", cover_image)
    if dry_run:
        return {"draftStatus": "dry-run", "coverType": cover_type, "mediaId": media_id, "cover": Path(cover_image).name}
    token = access_token or fetch_access_token(appid, secret)
    live = decode_json(post_json(f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}", {"media_id": media_id}))
    items = live.get("news_item") or []
    if not items:
        raise SystemExit(f"Draft {media_id} has no news_item to update; nothing to re-cover.")
    saved = items[0]
    old_thumb = str(saved.get("thumb_media_id", ""))
    new_thumb = upload_cover_image(cover_image, token, cover_type)
    article = {
        "title": str(saved.get("title", "")),
        "author": str(saved.get("author", "")),
        "digest": str(saved.get("digest", "")),
        "content": str(saved.get("content", "")),
        "content_source_url": str(saved.get("content_source_url", "")),
        "thumb_media_id": new_thumb,
        "need_open_comment": int(saved.get("need_open_comment", 0) or 0),
        "only_fans_can_comment": int(saved.get("only_fans_can_comment", 0) or 0),
    }
    decode_json(post_json(draft_url(token, media_id), {"media_id": media_id, "index": 0, "articles": article}))
    result: dict[str, object] = {
        "draftStatus": "cover-updated",
        "mediaId": media_id,
        "coverType": cover_type,
        "oldThumbMediaId": old_thumb,
        "newThumbMediaId": new_thumb,
    }
    result["verification"] = verify_draft(media_id, article, token)
    return result


def verify_draft(media_id: str, article: dict[str, str], token: str) -> dict[str, object]:
    """Read the draft back. A write returning errcode:0 does not mean it landed.

    Observed 2026-09-25: draft/update reported ok while the live draft still held
    the previous revision's title and body. Never treat the write response as proof.
    """
    if not media_id:
        return {"checked": False, "reason": "no media_id to read back"}
    live = decode_json(post_json(f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}", {"media_id": media_id}))
    items = live.get("news_item") or []
    if not items:
        raise SystemExit(f"Draft readback failed: {media_id} has no news_item. Content did NOT land; re-push before reporting success.")
    saved = items[0]
    mismatches = [field for field in ("title", "digest") if str(saved.get(field, "")) != str(article.get(field, ""))]
    missing = missing_text(str(article.get("content", "")), str(saved.get("content", "")))
    if mismatches or missing:
        detail = ", ".join(mismatches + ([f"body text {m!r} absent" for m in missing]))
        raise SystemExit(f"Draft readback mismatch: {detail}. The write reported success but the live draft differs. Re-push and re-verify; do NOT report success.")
    return {"checked": True, "media_id": media_id, "title": saved.get("title", ""), "contentLength": len(str(saved.get("content", "")))}


def missing_text(local_html: str, live_html: str) -> list[str]:
    """Which paragraphs of the pushed body are absent from the live draft.

    WeChat rewrites the markup it is given, so the HTML never round-trips byte for
    byte. Compare the visible text instead, and check every paragraph rather than a
    sample: a stale draft typically differs in only a few paragraphs, which is
    exactly what sampling walks past.
    """
    live = visible_text(live_html)
    chunks = [c for c in visible_text(local_html).split("\n") if len(c) >= 12]
    return [c for c in dict.fromkeys(chunks) if c not in live]


def visible_text(html: str) -> str:
    """Body text as WeChat stores it, for comparing a pushed article to the live draft.

    WeChat rewrites the markup it is given and drops <head> entirely, so neither the
    HTML nor the document title survives a round trip. Only the rendered body text does.
    """
    text = re.sub(r"<head\b.*?</head>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = unescape(text)
    return "\n".join(line.strip() for line in text.split("\n") if line.strip())


def fetch_access_token(appid: str, secret: str) -> str:
    require_value("WECHAT_APPID", appid)
    require_value("WECHAT_SECRET", secret)
    body = {"grant_type": "client_credential", "appid": appid, "secret": secret}
    data = post_json("https://api.weixin.qq.com/cgi-bin/stable_token", body)
    payload = decode_json(data)
    require_value("access_token", payload.get("access_token", ""))
    return str(payload["access_token"])


def upload_content_image(path: str, token: str) -> str:
    payload, content_type = multipart_body(path, "media")
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    data = http_request(url, payload, content_type)
    return str(decode_json(data)["url"])


def upload_cover_image(path: str, token: str, media_type: str) -> str:
    require_value("cover_image", path)
    payload, content_type = multipart_body(path, "media")
    query = urlencode({"access_token": token, "type": media_type})
    data = http_request(f"https://api.weixin.qq.com/cgi-bin/material/add_material?{query}", payload, content_type)
    return str(decode_json(data)["media_id"])


def draft_article(meta: dict[str, str], html_path: str, cover_image: str, cover_type: str, title: str, author: str, digest: str, source_url: str) -> dict[str, str]:
    article = {
        "title": title or pick_meta(meta, "title"),
        "author": author or pick_meta(meta, "author"),
        "digest": digest or pick_meta(meta, "digest"),
        "content": Path(html_path).read_text(encoding="utf-8"),
        "content_source_url": source_url or pick_meta(meta, "content_source_url"),
        "thumb_media_id": "",
        "cover_image": cover_image or pick_meta(meta, "coverImage"),
        "cover_type": cover_type,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    require_value("title", article["title"])
    require_value("content", article["content"])
    return article


def draft_payload(article: dict[str, str], media_id: str) -> dict[str, object]:
    body = article.copy()
    body.pop("cover_image", None)
    body.pop("cover_type", None)
    if media_id:
        return {"media_id": media_id, "index": 0, "articles": body}
    return {"articles": [body]}


def draft_url(token: str, media_id: str) -> str:
    endpoint = "update" if media_id else "add"
    return f"https://api.weixin.qq.com/cgi-bin/draft/{endpoint}?access_token={token}"


def multipart_body(path: str, field_name: str) -> tuple[bytes, str]:
    boundary = f"----Codex{uuid.uuid4().hex}"
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    head = f"--{boundary}\r\nContent-Disposition: form-data; name=\"{field_name}\"; filename=\"{Path(path).name}\"\r\nContent-Type: {mime}\r\n\r\n".encode("utf-8")
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    return head + Path(path).read_bytes() + tail, f"multipart/form-data; boundary={boundary}"


def post_json(url: str, payload: dict[str, object]) -> bytes:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return http_request(url, body, "application/json; charset=utf-8")


def http_request(url: str, payload: bytes, content_type: str) -> bytes:
    request = Request(url, data=payload, headers={"Content-Type": content_type, "User-Agent": "Codex research-to-wechat"}, method="POST")
    with urlopen(request, timeout=30) as response:
        return response.read()


def decode_json(data: bytes) -> dict[str, object]:
    payload = json.loads(data.decode("utf-8", errors="ignore") or "{}")
    if int(payload.get("errcode", 0) or 0) != 0:
        raise SystemExit(json.dumps(payload, ensure_ascii=False))
    return payload


def require_value(name: str, value: str) -> None:
    if not value:
        raise SystemExit(f"Missing required value: {name}")
