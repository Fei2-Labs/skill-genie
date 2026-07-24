# Mesh editing notes (trimesh)

## Dependency chain for `slice_mesh_plane(..., cap=True)`

`trimesh.intersections.slice_mesh_plane` with `cap=True` lazily imports, in order:

1. `scipy` (`scipy.spatial.cKDTree`)
2. `shapely` (`shapely.ops`, for 2D polygon reconstruction of the cut cross-section)
3. `networkx` (graph structure to figure out polygon nesting/enclosure — holes vs outer boundary)
4. `rtree` (spatial index used by the enclosure-tree computation)

Each missing package surfaces as a separate `ModuleNotFoundError` **one at a time** as you fix the previous one —
easy to mistake for a chain of unrelated bugs. Install all of them up front:

```bash
python3 -m pip install trimesh numpy scipy shapely networkx rtree manifold3d
```

(`manifold3d` is trimesh's preferred backend for real boolean operations — union/difference/intersection — used
implicitly for some complex cuts and always useful to have for other mesh-editing tasks.)

## Parsing a raw `.model` file (trimesh can't load `.model` directly)

`trimesh.load()` does not recognize the bare `.model` extension used inside a 3MF's `3D/Objects/` folder (it's
only wired up to load a *complete* `.3mf`/`.zip`). Parse it manually:

```python
import xml.etree.ElementTree as ET
import numpy as np
import trimesh

ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
tree = ET.parse("3D/Objects/object_1.model")
obj = tree.getroot().find(".//m:object", ns)
mesh_el = obj.find("m:mesh", ns)
verts = np.array([[float(v.get(a)) for a in ("x", "y", "z")]
                  for v in mesh_el.find("m:vertices", ns)], dtype=float)
tris = np.array([[int(t.get(a)) for a in ("v1", "v2", "v3")]
                  for t in mesh_el.find("m:triangles", ns)], dtype=int)

mesh = trimesh.Trimesh(vertices=verts, faces=tris, process=False)
```

Use `process=False` so trimesh doesn't merge/reorder vertices — keep the geometry exactly as authored unless you
intend to clean it up.

## Splitting/cutting

```python
half_a = trimesh.intersections.slice_mesh_plane(
    mesh, plane_normal=[0, 1, 0], plane_origin=[0, 0, 0], cap=True
)
half_b = trimesh.intersections.slice_mesh_plane(
    mesh, plane_normal=[0, -1, 0], plane_origin=[0, 0, 0], cap=True
)
```

- `plane_normal` points toward the half you want to **keep**.
- Cut both directions from the same plane so the two halves are complementary.
- `cap=True` fills the exposed cross-section with a triangulated cap so each half stays watertight/solid. Without
  it you get an open shell that won't slice or print correctly.

## Always verify after cutting

```python
assert half_a.is_watertight and half_b.is_watertight
assert abs((half_a.volume + half_b.volume) - mesh.volume) < 1e-3
```

If either half is not watertight, the source mesh likely had its own defects (non-manifold edges, gaps) —
check `mesh.is_watertight` on the *original* first; don't assume the cut introduced the problem.

## Choosing the cut plane

Don't guess an axis. Print the source mesh's bounding box first:

```python
print(mesh.bounds)    # [[minx, miny, minz], [maxx, maxy, maxz]]
print(mesh.extents)   # [dx, dy, dz]
```

Pick the axis with the largest extent for a "split roughly in half" request, and use the true midpoint of that
axis's range as `plane_origin` (not necessarily 0 — only use 0 if the bounds are already symmetric around it,
e.g. `[-127, 127]`). For a user-specified cut location or orientation, use their spec directly instead of the
longest-axis heuristic.

## Writing the mesh back out

Serialize vertices/triangles back into the same `.model` XML shape used by the source file (see
`references/3mf-structure.md`) rather than trying to reuse trimesh's own 3MF exporter, which does not preserve the
Bambu/Orca-specific project structure (`model_settings.config`, plate assignment, etc.) — those must be hand-wired
per §3–4 of `SKILL.md`.
