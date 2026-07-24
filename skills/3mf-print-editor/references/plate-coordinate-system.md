# The multi-plate shared-scene coordinate system

> **Verified against BambuStudio only.** Everything below is derived from BambuStudio's own source
> (`bambulab/BambuStudio`) and confirmed against real BambuStudio behavior. It is likely close for OrcaSlicer (a
> BambuStudio fork) but unverified there, and not guaranteed for any other `.3mf`-consuming application — do not
> apply these constants to another tool without re-checking that tool's own source/behavior first.

## The bug this document prevents

Symptom: you script a "put half A on plate 1 and half B on plate 2" edit. Each half gets centered on its own
256×256 (or whatever bed size) local coordinate space, e.g. `(bed_w/2, bed_h/2)`. You wire up
`Metadata/model_settings.config` so plate 1's `<model_instance>` references object A and plate 2's references
object B. On open: **plate 1 shows what looks like the complete, uncut model** (both halves rendered stacked
exactly back together) and **plate 2 is empty**.

## Root cause

BambuStudio/OrcaSlicer do not give each plate an independent origin-0 coordinate space. All plates are rendered
in **one shared 3D scene**, side by side, and every object's actual stored transform (`3D/3dmodel.model`
`<build><item transform="...">`, mirrored in `Metadata/model_settings.config`'s `<assemble_item transform="...">`)
must already be in that shared space — i.e. **plate-local position PLUS that plate's offset in the shared scene**.

This is implemented in `bambulab/BambuStudio`, `src/slic3r/GUI/PartPlate.cpp`:

```cpp
static const double LOGICAL_PART_PLATE_GAP = 1. / 5.;   // 20% gap between plates

double PartPlateList::plate_stride_x() { return m_plate_width * (1. + LOGICAL_PART_PLATE_GAP); }
double PartPlateList::plate_stride_y() { return m_plate_depth * (1. + LOGICAL_PART_PLATE_GAP); }

Vec2d PartPlateList::compute_shape_position(int index, int cols) {
    int col = index % cols;
    int row = index / cols;
    Vec2d pos;
    pos(0) = col * plate_stride_x();
    pos(1) = -row * plate_stride_y();
    return pos;
}
```

(`plate_data_list`/`obj_inst_map` parsing that ties an object to a specific plate index lives in
`src/libslic3r/Format/bbs_3mf.cpp`, functions `_handle_start_config_plater*` and the `obj_inst_map` consumers —
that mechanism decides *which* plate owns an object, completely independently from *where* it renders, which is
why getting the plate assignment right (§4 of `model_settings.config`) is not enough on its own; the coordinates
must independently encode which plate cell they fall into.)

## The formula

```
plate_index      # 0-based: first plate = 0, second plate = 1, ...
cols              # number of plate columns before wrapping to a new row (small multi-plate
                  # projects are effectively always 1 row; don't assume a value — infer from how
                  # many plates the project defines, or default to "all plates in one row" unless
                  # told otherwise)

stride_x = bed_width * 1.2     # LOGICAL_PART_PLATE_GAP = 0.2
stride_y = bed_depth * 1.2

col = plate_index % cols
row = plate_index // cols

plate_origin_x =  col * stride_x
plate_origin_y = -row * stride_y
```

For a standard 256×256 Bambu bed: `stride_x = stride_y = 307.2`.

**Every object's global placement = its plate-local placement + `plate_origin` for the plate it belongs to.**

Worked example (256×256 bed, 2 plates in one row, each holding one half of a model that's 198mm × 254mm, split
along Y into two 198×127mm halves):

```
plate 0 (index 0): plate_origin = (0, 0)
plate 1 (index 1): plate_origin = (307.2, 0)

half A, local mesh Y range [0, 127], centered at local bed pos (128, 64.5):
  global build-item translation = (128 + 0, 64.5 + 0) = (128, 64.5)

half B, local mesh Y range [-127, 0], centered at local bed pos (128, 191.5):
  global build-item translation = (128 + 307.2, 191.5 + 0) = (435.2, 191.5)
```

Both the `3D/3dmodel.model` `<item transform="...">` translation and the matching `Metadata/model_settings.config`
`<assemble_item transform="...">` must use these **global** numbers, not the local ones.

## How to compute bed size and plate offset in Python

```python
import json

def bed_size(project_settings_path):
    with open(project_settings_path) as f:
        cfg = json.load(f)
    corners = [tuple(map(float, c.split("x"))) for c in cfg["printable_area"]]
    xs = [c[0] for c in corners]
    ys = [c[1] for c in corners]
    return max(xs) - min(xs), max(ys) - min(ys)

def plate_origin(plate_index, bed_width, bed_depth, cols=1):
    stride_x = bed_width * 1.2
    stride_y = bed_depth * 1.2
    col = plate_index % cols
    row = plate_index // cols
    return (col * stride_x, -row * stride_y)
```

(Also available as `scripts/mesh_tools.py:plate_origin` / `bed_size` in this skill.)

## Checklist before trusting a multi-plate edit

1. Read bed width/depth from `printable_area` in `project_settings.config` — never hardcode 256.
2. For every object, compute `plate_origin(that object's plate_index, bed_w, bed_h, cols)`.
3. Add that offset to the object's intended local-plate position to get the transform you write into
   `3D/3dmodel.model`'s `<item>` and `model_settings.config`'s `<assemble_item>`.
4. Sanity-check: no two objects assigned to *different* plates should end up with overlapping global bounding
   boxes; every object assigned to the *same* plate should have global bounds inside that plate's own
   `[plate_origin, plate_origin + (bed_w, bed_h)]` rectangle.
5. If you genuinely don't know `cols` for a given project (very large plate counts sometimes wrap to multiple
   rows), keep new plates in a single row (increasing `plate_index` only, `cols` large enough to never wrap)
   unless the source file already shows a multi-row layout to match.
