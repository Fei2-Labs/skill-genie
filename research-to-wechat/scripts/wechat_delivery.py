#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _wechat_design_catalog import build_design_catalog
from _wechat_delivery_api import environment_report, save_draft, upload_images
from _wechat_delivery_render import render_article
from _wechat_delivery_shared import dump_json, load_json, normalize_markdown_links


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wechat_delivery.py")
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_check(subparsers)
    add_catalog(subparsers)
    add_render(subparsers)
    add_upload(subparsers)
    add_save(subparsers)
    return parser


def add_check(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparsers.add_parser("check")


def add_catalog(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("design-catalog")
    parser.add_argument("--design-pen", default=str(SCRIPT_DIR.parent / "design.pen"))
    parser.add_argument("--output")


def add_render(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("render")
    parser.add_argument("markdown")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--design", default="")
    parser.add_argument("--design-pen", default=str(SCRIPT_DIR.parent / "design.pen"))
    parser.add_argument("--color-mode", default="auto", choices=["auto", "light", "dark"])
    parser.add_argument("--upload-map")


def add_upload(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("upload-images")
    parser.add_argument("images", nargs="+")
    parser.add_argument("--appid")
    parser.add_argument("--secret")
    parser.add_argument("--access-token")
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")


def add_save(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("save-draft")
    parser.add_argument("--html", required=True)
    parser.add_argument("--markdown", required=True)
    parser.add_argument("--appid")
    parser.add_argument("--secret")
    parser.add_argument("--access-token")
    parser.add_argument("--media-id")
    parser.add_argument("--cover-image", default="")
    parser.add_argument("--cover-type", default="image", choices=["image", "thumb"])
    parser.add_argument("--content-source-url", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--author", default="")
    parser.add_argument("--digest", default="")
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")


def run_check(_: argparse.Namespace) -> None:
    dump_json(environment_report(), None)


def run_catalog(args: argparse.Namespace) -> None:
    dump_json(build_design_catalog(args.design_pen), args.output)


def run_render(args: argparse.Namespace) -> None:
    normalize_markdown_links(args.markdown)
    image_map = load_json(args.upload_map)
    result = render_article(args.markdown, args.output, image_map, args.design, args.color_mode, args.design_pen)
    dump_json(result, None)


def run_upload(args: argparse.Namespace) -> None:
    result = upload_images(args.images, args.appid or os.getenv("WECHAT_APPID", ""), args.secret or os.getenv("WECHAT_SECRET", ""), args.access_token or os.getenv("WECHAT_ACCESS_TOKEN", ""), args.dry_run)
    dump_json(result, args.output)


def run_save(args: argparse.Namespace) -> None:
    result = save_draft(
        args.html,
        args.markdown,
        args.appid or os.getenv("WECHAT_APPID", ""),
        args.secret or os.getenv("WECHAT_SECRET", ""),
        args.access_token or os.getenv("WECHAT_ACCESS_TOKEN", ""),
        args.media_id or os.getenv("WECHAT_DRAFT_MEDIA_ID", ""),
        args.cover_image,
        args.cover_type,
        args.title,
        args.author,
        args.digest,
        args.content_source_url,
        args.dry_run,
    )
    dump_json(result, args.output)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    commands = {"check": run_check, "design-catalog": run_catalog, "render": run_render, "upload-images": run_upload, "save-draft": run_save}
    commands[args.command](args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
