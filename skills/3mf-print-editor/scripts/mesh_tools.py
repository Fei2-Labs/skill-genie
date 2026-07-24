#!/usr/bin/env python3
"""
mesh_tools.py — reusable helpers for the 3mf-print-editor skill.

Covers the three error-prone steps of hand-editing a Bambu/Orca .3mf project:
  1. extracting/repackaging the zip safely
  2. splitting a mesh with the validation checks that catch broken cuts
  3. computing the correct multi-plate global offset (see references/plate-coordinate-system.md)

Designed to be imported (`from mesh_tools import ...`) or run standalone for a couple of CLI
utilities. Requires: trimesh, numpy, scipy, shapely, networkx, rtree (see SKILL.md "Environment setup").

Not tied to any specific model — every function takes explicit paths/arrays so it can be reused
across unrelated 3D-printing editing tasks.
"""

from __future__ import annotations

import json
import shutil
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

CORE_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
LOGICAL_PART_PLATE_GAP = 0.2  # matches BambuStudio's LOGICAL_PART_PLATE_GAP = 1/5


# ── Package extraction / repackaging ─────────────────────────────────────────

def extract_3mf(archive_path: str | Path, dest_dir: str | Path) -> Path:
    """Extract a .3mf (zip) to dest_dir/extracted and return that path."""
    dest_dir = Path(dest_dir)
    out = dest_dir / "extracted"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    with zipfile.ZipFile(archive_path) as z:
        z.extractall(out)
    return out


def repackage_3mf(extracted_dir: str | Path, output_path: str | Path) -> Path:
    """Zip an extracted (and edited) 3MF tree back into a .3mf file.

    Overwrites output_path if it exists. Does NOT touch the original source file —
    always write to a new path per SKILL.md section 7 (non-destructive output).
    """
    extracted_dir = Path(extracted_dir)
    output_path = Path(output_path)
    if output_path.exists():
        output_path.unlink()
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(extracted_dir.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(extracted_dir).as_posix())
    return output_path


# ── Mesh parsing / splitting ──────────────────────────────────────────────

def parse_object_model(model_path: str | Path):
    """Parse a 3D/Objects/object_N.model file into (vertices, faces) numpy arrays."""
    import numpy as np

    ns = {"m": CORE_NS}
    tree = ET.parse(model_path)
    obj = tree.getroot().find(".//m:object", ns)
    mesh_el = obj.find("m:mesh", ns)
    verts = np.array(
        [[float(v.get(a)) for a in ("x", "y", "z")] for v in mesh_el.find("m:vertices", ns)],
        dtype=float,
    )
    tris = np.array(
        [[int(t.get(a)) for a in ("v1", "v2", "v3")] for t in mesh_el.find("m:triangles", ns)],
        dtype=int,
    )
    return verts, tris


def write_object_model(path: str | Path, object_id: int, mesh) -> tuple[int, int]:
    """Serialize a trimesh.Trimesh back into a 3MF object .model file.

    Returns (num_vertices, num_faces) for use in model_settings.config metadata.
    """
    v, f = mesh.vertices, mesh.faces
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
        'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
        'requiredextensions="p">',
        ' <resources>',
        f'  <object id="{object_id}" type="model">',
        '   <mesh>',
        '    <vertices>',
    ]
    for x, y, z in v:
        lines.append(f'     <vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>')
    lines.append('    </vertices>')
    lines.append('    <triangles>')
    for a, b, c in f:
        lines.append(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>')
    lines.append('    </triangles>')
    lines.append('   </mesh>')
    lines.append('  </object>')
    lines.append(' </resources>')
    lines.append(' <build/>')
    lines.append('</model>')
    Path(path).write_text("\n".join(lines))
    return len(v), len(f)


def split_mesh_plane(mesh, plane_normal, plane_origin=(0, 0, 0)):
    """Cut `mesh` at the given plane into (keep_positive, keep_negative) capped halves,
    with volume-conservation and watertightness asserted.

    plane_normal points toward the "positive" half. Raises AssertionError if the cut
    produced a non-watertight piece or lost/duplicated volume — do not silently ignore
    these, they mean the source mesh had defects or the cut plane was degenerate.
    """
    import numpy as np
    import trimesh

    normal = np.asarray(plane_normal, dtype=float)
    origin = np.asarray(plane_origin, dtype=float)

    pos = trimesh.intersections.slice_mesh_plane(
        mesh, plane_normal=normal, plane_origin=origin, cap=True
    )
    neg = trimesh.intersections.slice_mesh_plane(
        mesh, plane_normal=-normal, plane_origin=origin, cap=True
    )

    assert pos.is_watertight, "positive half is not watertight after cut"
    assert neg.is_watertight, "negative half is not watertight after cut"
    volume_diff = abs((pos.volume + neg.volume) - mesh.volume)
    assert volume_diff < 1e-3, f"volume not conserved after cut (diff={volume_diff})"

    return pos, neg


# ── Plate coordinate system (see references/plate-coordinate-system.md) ─────

def bed_size(project_settings_path: str | Path) -> tuple[float, float]:
    """Read (bed_width, bed_depth) in mm from Metadata/project_settings.config."""
    with open(project_settings_path) as f:
        cfg = json.load(f)
    corners = [tuple(map(float, c.split("x"))) for c in cfg["printable_area"]]
    xs = [c[0] for c in corners]
    ys = [c[1] for c in corners]
    return max(xs) - min(xs), max(ys) - min(ys)


def plate_origin(plate_index: int, bed_width: float, bed_depth: float, cols: int = 1):
    """Global-scene offset (x, y) for the given 0-based plate_index.

    Matches BambuStudio's PartPlateList::compute_shape_position + plate_stride_x/y
    (LOGICAL_PART_PLATE_GAP = 0.2 -> 20% gap between plates). Add this to an object's
    plate-local placement to get the transform to write into 3dmodel.model / model_settings.config.

    BambuStudio-specific: verified against BambuStudio's own source. Not confirmed for
    OrcaSlicer/PrusaSlicer/other .3mf tools — re-verify before reusing this for another app.
    """
    stride_x = bed_width * (1 + LOGICAL_PART_PLATE_GAP)
    stride_y = bed_depth * (1 + LOGICAL_PART_PLATE_GAP)
    col = plate_index % cols
    row = plate_index // cols
    return (col * stride_x, -row * stride_y)


# ── Validation ────────────────────────────────────────────────────────────

def validate_package(extracted_dir: str | Path) -> list[str]:
    """Run the checks from SKILL.md section 6 over an extracted 3MF tree.

    Returns a list of problem descriptions (empty list = all checks passed).
    """
    extracted_dir = Path(extracted_dir)
    problems: list[str] = []

    # 1. XML well-formedness for every .model/.config/.rels file
    xml_globs = ["**/*.model", "**/*.rels", "**/*.config"]
    xml_files: list[Path] = []
    for pattern in xml_globs:
        xml_files.extend(extracted_dir.glob(pattern))
    for f in xml_files:
        try:
            ET.parse(f)
        except ET.ParseError as exc:
            problems.append(f"XML parse error in {f.relative_to(extracted_dir)}: {exc}")

    # 2 & 3. Mesh integrity + watertightness for every object file
    try:
        import trimesh
    except ImportError:
        trimesh = None

    for obj_file in extracted_dir.glob("3D/Objects/*.model"):
        try:
            verts, tris = parse_object_model(obj_file)
        except Exception as exc:
            problems.append(f"could not parse mesh in {obj_file.name}: {exc}")
            continue
        if len(verts) == 0 or len(tris) == 0:
            problems.append(f"{obj_file.name} has empty geometry")
            continue
        if trimesh is not None:
            mesh = trimesh.Trimesh(vertices=verts, faces=tris, process=False)
            if not mesh.is_watertight:
                problems.append(f"{obj_file.name} is not watertight")

    # relationship sanity: every Objects/object_N.model should have a rels entry
    rels_path = extracted_dir / "3D" / "_rels" / "3dmodel.model.rels"
    if rels_path.exists():
        rels_targets = {
            el.get("Target")
            for el in ET.parse(rels_path).getroot()
        }
        for obj_file in extracted_dir.glob("3D/Objects/*.model"):
            target = f"/3D/Objects/{obj_file.name}"
            if target not in rels_targets:
                problems.append(f"missing relationship for {target} in 3dmodel.model.rels")

    return problems


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_extract = sub.add_parser("extract", help="Extract a .3mf to a working directory")
    p_extract.add_argument("archive")
    p_extract.add_argument("dest")

    p_repack = sub.add_parser("repackage", help="Zip an extracted tree back into a .3mf")
    p_repack.add_argument("extracted_dir")
    p_repack.add_argument("output")

    p_validate = sub.add_parser("validate", help="Validate an extracted 3MF tree")
    p_validate.add_argument("extracted_dir")

    p_bed = sub.add_parser("bed-size", help="Print bed width/depth from project_settings.config")
    p_bed.add_argument("project_settings_path")

    p_plate = sub.add_parser("plate-origin", help="Compute a plate's global offset")
    p_plate.add_argument("plate_index", type=int)
    p_plate.add_argument("bed_width", type=float)
    p_plate.add_argument("bed_depth", type=float)
    p_plate.add_argument("--cols", type=int, default=1)

    args = parser.parse_args()

    if args.command == "extract":
        out = extract_3mf(args.archive, args.dest)
        print(out)
    elif args.command == "repackage":
        out = repackage_3mf(args.extracted_dir, args.output)
        print(out)
    elif args.command == "validate":
        problems = validate_package(args.extracted_dir)
        if problems:
            print(f"{len(problems)} problem(s) found:")
            for p in problems:
                print(f"  - {p}")
            raise SystemExit(1)
        print("all checks passed")
    elif args.command == "bed-size":
        w, d = bed_size(args.project_settings_path)
        print(f"{w} {d}")
    elif args.command == "plate-origin":
        ox, oy = plate_origin(args.plate_index, args.bed_width, args.bed_depth, cols=args.cols)
        print(f"{ox} {oy}")
