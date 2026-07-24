---
name: "3mf-print-editor"
description: "Guideline for directly editing 3D-printing project files (.3mf), verified against BambuStudio specifically: cutting or otherwise modifying mesh geometry, wiring objects into the 3MF XML correctly, arranging multiple print plates in BambuStudio's shared multi-plate coordinate system, and setting print/project parameters. Use whenever a user asks to edit, cut, split, merge, reposition, rearrange, or reconfigure a BambuStudio .3mf project file by hand instead of through the slicer GUI. Other slicers (OrcaSlicer, PrusaSlicer, etc.) use similar-looking .3mf files but are NOT verified to follow the same plate-offset math or config schema — treat this skill's multi-plate guidance as BambuStudio-specific."
license: "MIT"
metadata: {"version":"1.0.0","category":"3d-printing","license":"MIT","tags":["3d-printing","3mf","bambustudio","orcaslicer","mesh-editing","slicer"],"hermes":{"tags":["3d-printing","3mf","bambustudio","orcaslicer","mesh-editing","slicer"]}}
---

# 3MF Print Editor

Guideline for hand-editing 3D-printing files — Bambu Lab's `.3mf` project files, as opened/sliced by **BambuStudio**
— when the user wants a model cut, split across plates, repositioned, merged, or reconfigured programmatically
rather than through the slicer GUI. Covers three things end to end: **editing the mesh correctly**,
**building/arranging plates correctly**, and **setting print parameters correctly**. Read `references/3mf-structure.md`
and `references/plate-coordinate-system.md` before editing a multi-plate project — the plate math is not obvious and
is the single most common source of silent failure (see Pitfall #1).

> **Scope disclaimer: this skill is verified against BambuStudio only.** Everything here — the `Metadata/model_settings.config`
> schema, the multi-plate shared-scene offset formula in §4, and the `project_settings.config` keys in §5 — was
> reverse-engineered from BambuStudio's own source (`bambulab/BambuStudio`) and confirmed against real BambuStudio
> behavior. OrcaSlicer, PrusaSlicer, and other tools also read/write `.3mf`, and OrcaSlicer's is close (it's a
> BambuStudio fork), but their exact plate-offset constants, config keys, or metadata schema are **not guaranteed to
> match** and have not been verified here. If the user's target application isn't BambuStudio, say so explicitly,
> and re-derive/verify the relevant constants against that application's own source or behavior before applying this
> skill's formulas — do not assume they transfer as-is.

## When to use this skill

- "把这个模型从中间切开/分成两半" — cut/split a model into pieces
- "分别放到两个盘里" / "put these on separate plates" — multi-plate arrangement
- "调整模型位置/旋转/缩放" — reposition, rotate, scale an object in a project file
- "改一下打印设置" — change bed size, plate count, filament/printer profile in a project file
- "帮我重新打包这个 3mf" — merge multiple STL/3MF sources into one project
- Any task that requires opening a `.3mf` as a zip and hand-editing its XML/config instead of using the slicer UI

Do NOT use this skill just to *view* or *slice* a file — only when the file itself needs to be programmatically
modified and re-saved.

## Environment setup

Mesh editing needs `trimesh` plus its optional dependencies for boolean ops, capping, and polygon repair. On macOS
with a Homebrew Python, the interpreter that actually has these packages may differ from the default `python3`
(check with `python3 -c "import sys; print(sys.executable)"` vs `which -a python3.*`). Install once per environment:

```bash
python3 -m pip install trimesh numpy scipy shapely networkx rtree manifold3d
```

Verify:

```bash
python3 -c "import trimesh, numpy, scipy, shapely, networkx, rtree; print('ok', trimesh.__version__)"
```

If `pip3` and `python3` resolve to different interpreters (common on macOS with multiple Homebrew Python versions),
install and run with the exact interpreter path that has the packages, not just `python3`.

## 1. Understand the file before touching it

A `.3mf` is a standard OPC (Open Packaging Conventions) zip. Always extract and inspect first:

```bash
mkdir -p /tmp/3mf_work && cd /tmp/3mf_work
unzip -o "/path/to/model.3mf" -d extracted
find extracted -type f
```

Read `references/3mf-structure.md` for the full file-by-file breakdown. Key files:

| File | Purpose |
|---|---|
| `3D/3dmodel.model` | Top-level resources (component references) + `<build>` list of placed instances |
| `3D/Objects/object_N.model` | Actual mesh geometry (vertices/triangles) for object id N |
| `3D/_rels/3dmodel.model.rels` | OPC relationships — must list every `Objects/object_N.model` referenced |
| `Metadata/model_settings.config` | Bambu/Orca project metadata: object names, per-object part metadata, `<plate>` blocks (which objects belong to which plate), `<assemble>` block |
| `Metadata/project_settings.config` | Full print/printer/filament settings as flat JSON (bed shape, height, temps, speeds, etc.) |
| `Metadata/cut_information.xml` | Bambu's native "Cut tool" state — only relevant if you want the GUI cut-tool to recognize a cut; safe to leave empty (`<objects></objects>`) for programmatic edits |
| `Metadata/plate_N.png` etc. | Thumbnails — cosmetic only, stale thumbnails do not break loading |

Never assume a schema detail — when unsure, verify against the actual BambuStudio source
(`src/libslic3r/Format/bbs_3mf.cpp`, `src/slic3r/GUI/PartPlate.cpp` in `bambulab/BambuStudio` on GitHub) rather than
guessing. This skill's plate-offset math (Pitfall #1) was reverse-engineered from that source after a first attempt
silently failed.

## 2. Editing the mesh correctly

For real geometry edits (cutting, boolean, hollowing, etc.), never hand-edit vertex/triangle XML — parse it into a
proper mesh library, edit, then re-serialize.

1. Parse the object's vertices/triangles from `3D/Objects/object_N.model` (or the sole object file when there's no
   multi-part split) using `xml.etree.ElementTree`, build a `trimesh.Trimesh(vertices=..., faces=..., process=False)`.
2. Determine the cut/split plane from the mesh's actual bounding box — don't guess an axis. Print
   `mesh.bounds` and `mesh.extents` first. For "cut in half", pick the plane through the midpoint of the *longest*
   horizontal extent (or the axis the user specifies), and prefer a plane that lands on an already-symmetric midpoint
   (e.g. bounds like `[-127, 127]`) since that's almost always the model's natural centerline.
3. Cut with capping so each half stays a valid solid:
   ```python
   half_a = trimesh.intersections.slice_mesh_plane(mesh, plane_normal=[0,1,0], plane_origin=[0,0,0], cap=True)
   half_b = trimesh.intersections.slice_mesh_plane(mesh, plane_normal=[0,-1,0], plane_origin=[0,0,0], cap=True)
   ```
4. **Always verify before packaging**:
   - `half_a.is_watertight and half_b.is_watertight` must both be `True`.
   - `abs(half_a.volume + half_b.volume - mesh.volume) < 1e-3` (volume conservation — proves no geometry was lost
     or duplicated at the cut).
   - Bounds of each half only extend on the expected side of the cut plane.
5. Use `scripts/mesh_tools.py` (`split_mesh_plane`) to do steps 3–4 with the checks built in instead of re-deriving
   this from scratch each time.

See `references/mesh-editing-notes.md` for capping caveats, common trimesh dependency errors and fixes
(`scipy`/`shapely`/`networkx`/`rtree` ImportErrors surface one at a time — install all five up front), and how to
handle non-watertight source meshes.

## 3. Wiring edited objects back into the 3MF XML

When a cut/split produces N new sub-meshes that must become N separate placeable objects:

1. Write each mesh to its own `3D/Objects/object_<id>.model` file with a unique numeric object `id`, following the
   existing file's template (`<model>` root with the same namespaces, one `<object type="model"><mesh>...` per file).
   Keep IDs unique across the *whole package* — IDs are global, not per-file.
2. In `3D/3dmodel.model`, give each new sub-mesh a wrapping top-level `<object type="model">` with a `<component>`
   pointing at its `.model` file, then add one `<item objectid="...">` per object to `<build>` with the placement
   transform (see §4 for the coordinates that transform must use).
3. Add a `<Relationship Target="/3D/Objects/object_<id>.model" .../>` for every new object file to
   `3D/_rels/3dmodel.model.rels` — a missing relationship can cause silent load failures in strict parsers.
4. Update `Metadata/model_settings.config`: one `<object id="...">` block per top-level object (with a nested
   `<part>` for the mesh + `mesh_stat face_count=...`), one `<model_instance>` per plate assignment inside the
   matching `<plate>` block, and matching `<assemble_item>` entries in `<assemble>` using the *same* transform as the
   build item.
5. Reset or clear `Metadata/cut_information.xml` (`<objects></objects>`) when you replace geometry outside the GUI's
   own cut tool, so stale connector/cut metadata doesn't get misapplied to the new geometry.
6. `[Content_Types].xml` normally needs no change (it declares `Default Extension="model"` which covers any new
   `.model` file automatically) — only touch it if you introduce a genuinely new file extension.

## 4. Building/arranging plates correctly (read this before any multi-plate edit)

> **BambuStudio-specific.** The constants and behavior below (`LOGICAL_PART_PLATE_GAP = 0.2`, the shared-scene
> layout) are taken directly from BambuStudio's source and confirmed in BambuStudio. They are *likely* similar in
> OrcaSlicer (a BambuStudio fork) but have not been verified there, and are not guaranteed at all for PrusaSlicer or
> any other `.3mf` consumer. Do not present this formula as universal to "3D printing" or "3MF" in general — it is
> a property of this specific application's renderer/loader.

**This is the part that silently fails if you skip it.** BambuStudio renders every plate in *one shared 3D
scene*, not as independent origin-0 canvases. Every plate after the first is offset along X (and wraps to a new row
after the configured column count) by:

```
stride_x = bed_width  * 1.2   # LOGICAL_PART_PLATE_GAP = 0.2, i.e. a 20% gap
stride_y = bed_depth  * 1.2
col = plate_index % cols       # plate_index is 0-based; cols defaults such that plates fill one row unless very many
row = plate_index // cols
plate_origin = (col * stride_x, -row * stride_y)
```

Read the bed size from `Metadata/project_settings.config`'s `printable_area` (four `"XxY"` corner strings) and
`printable_height`. For the common 256×256 bed, `stride_x = stride_y = 307.2`.

**Every object's build-item transform (`3D/3dmodel.model` `<item transform="...">`) and its matching
`<assemble_item transform="...">` in `model_settings.config` must be in this shared global space**: local
plate-centered position **plus** that plate's `plate_origin` offset. If you center every object at its own plate's
local origin without adding the offset, every plate's objects land on top of each other at plate 0's location — the
first plate looks "whole" (multiple pieces stacked back together) and every other plate renders empty. This exact
bug is documented with full derivation in `references/plate-coordinate-system.md`; read it once, then use
`scripts/mesh_tools.py`'s `plate_origin(plate_index, bed_width, bed_depth, cols=...)` helper so you never
re-derive it by hand.

Assigning *which* plate an object belongs to (separately from its coordinates) is done via
`Metadata/model_settings.config`: each `<plate>` block has a `<model_instance>` child per object/instance
(`object_id`, `instance_id`, `identify_id`) that belongs on that plate. `identify_id` can be any positive integer;
it does not need to match anything else in the file (BambuStudio falls back to internal IDs when it's absent/≤0).

## 5. Setting print/project parameters

`Metadata/project_settings.config` is flat JSON (not XML) with every printer/filament/print setting as a
key → value (often the value is itself a stringified array/percentage). Common keys to look for:

- `printable_area`, `printable_height` — bed shape/size (see §4, drives plate offsets)
- `*_plate_temp`, `*_plate_temp_initial_layer` — bed temperature by plate type (cool/eng/hot/supertack/textured)
- Standard print-profile keys (layer height, speeds, supports, etc.) — treat this file as the single source of
  truth for "what will this print with"; do not assume defaults

When a user asks to "改打印设置" (change print settings), find the exact key(s) in this JSON, change only those
values, and leave the rest of the (very large) file untouched — do not reformat or reorder it.

`Metadata/slice_info.config` and `Metadata/filament_sequence.json` are usually safe to leave as-is unless the user
is specifically changing slicing/AMS filament-sequencing behavior.

## 6. Validate before delivering

Always run these checks on the rebuilt package before handing it back:

1. **XML well-formedness** on every `.model`/`.config`/`.rels` XML file (`xml.etree.ElementTree.parse`).
2. **Mesh integrity**: re-parse each `Objects/object_N.model`, confirm vertex/triangle counts are sane and
   (for solid parts) `trimesh` reports `is_watertight`.
3. **Volume/bounds sanity**: for split/cut operations, confirm combined volume matches the source and bounds fall
   on the correct side of the cut plane for each piece.
4. **Plate placement math**: recompute each object's expected global position from §4's formula and diff it
   against what you wrote into the build item — don't eyeball it.
5. **Repack as a proper zip** (`[Content_Types].xml` at minimum should be present; ordering isn't strict but keep
   the file complete) and re-extract it fresh to confirm the zip itself isn't corrupt.

Use `scripts/mesh_tools.py`'s `validate_package(dir)` to run 1–3 automatically over an extracted tree.

## 7. Non-destructive output

Never overwrite the user's original file in place. Write the result to a new file (e.g. `name_edited.3mf` or
`name_split.3mf`) alongside the original, tell the user exactly what changed, and only overwrite the original if
they explicitly ask you to.

## 8. Common pitfalls

1. **Multi-plate objects overlapping on plate 1, other plates empty** — you used plate-local coordinates instead
   of adding the shared-scene plate offset. Fix per §4.
2. **`ModuleNotFoundError` cascade when calling `trimesh.intersections.slice_mesh_plane(..., cap=True)`** — trimesh
   lazily imports `scipy`, then `shapely`, then `networkx`, then `rtree` one at a time; install all four (plus
   `manifold3d` for booleans) up front instead of iterating on import errors.
3. **`python3` without the packages** — `pip install` and `python3` can point at different interpreters on
   multi-Python-version macOS setups; always verify with the same interpreter you'll run edits with.
4. **Cut plane guessed instead of measured** — always print `mesh.bounds`/`mesh.extents` first; don't assume which
   axis is "the middle" of an asymmetric or unfamiliar model.
5. **Forgetting to update `3D/_rels/3dmodel.model.rels`** when adding new `Objects/object_N.model` files.
6. **Leaving stale `cut_information.xml`** pointing at old part/connector IDs after replacing geometry outside the
   GUI cut tool.
7. **Editing `project_settings.config` by reformatting the whole file** — it's huge; touch only the specific keys
   requested.

## References

- `references/3mf-structure.md` — full file-by-file breakdown of a Bambu/Orca `.3mf` package
- `references/plate-coordinate-system.md` — full derivation of the multi-plate offset formula, with BambuStudio
  source citations
- `references/mesh-editing-notes.md` — trimesh capping/watertight/dependency notes
- `scripts/mesh_tools.py` — reusable helpers: extract/repackage a 3mf, split a mesh with validation, compute a
  plate's origin offset, validate an extracted package
