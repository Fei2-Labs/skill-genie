# Anatomy of a Bambu/Orca `.3mf` package

A `.3mf` file is a ZIP archive following the OPC (Open Packaging Conventions) standard, extended by Bambu Lab /
OrcaSlicer with project-specific metadata. Extract it like any zip:

```bash
unzip -o model.3mf -d extracted
```

## File-by-file breakdown

```
extracted/
├── [Content_Types].xml            # OPC content-type declarations (Default Extension="model" covers all *.model files)
├── _rels/.rels                    # OPC root relationships: points to /3D/3dmodel.model + thumbnail relationships
├── 3D/
│   ├── 3dmodel.model              # Top-level model: <resources> (component refs) + <build> (placed instances)
│   ├── _rels/3dmodel.model.rels   # Relationships from 3dmodel.model to each Objects/object_N.model
│   └── Objects/
│       ├── object_1.model         # Actual mesh geometry: <object id="1"><mesh><vertices/><triangles/></mesh></object>
│       └── object_N.model         # One file per mesh "part" (BambuStudio splits geometry into its own file per part)
└── Metadata/
    ├── model_settings.config      # Bambu/Orca project metadata: object/part names, plate assignment, assemble transforms
    ├── project_settings.config    # Full print/printer/filament settings, flat JSON (not XML!)
    ├── slice_info.config          # Header only in most projects (client type/version); slicing cache in sliced projects
    ├── cut_information.xml        # State of BambuStudio's native "Cut tool" (connectors, cut ids) — optional
    ├── filament_sequence.json     # AMS filament-change sequencing per plate
    ├── plate_N.png / plate_N_small.png / plate_no_light_N.png / top_N.png / pick_N.png
    │                               # Thumbnails per plate — cosmetic, safe to leave stale after an edit
```

## `3D/3dmodel.model` — the core structure

```xml
<model unit="millimeter" ... xmlns:p="...production/2015/06" requiredextensions="p">
 <metadata name="Application">BambuStudio-...</metadata>
 <!-- more <metadata> for Title/Designer/CreationDate/etc -->
 <resources>
  <object id="2" type="model">
   <components>
    <component p:path="/3D/Objects/object_1.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>
   </components>
  </object>
  <!-- one <object type="model"> per top-level placeable "thing", each wrapping a component -->
 </resources>
 <build p:UUID="...">
  <item objectid="2" transform="1 0 0 0 1 0 0 0 1 <tx> <ty> <tz>" printable="1"/>
  <!-- one <item> per placed instance; transform is row-major 3x3 rotation/scale + translation as the last 3 numbers -->
 </build>
</model>
```

- `<resources><object>` entries are indirection: a top-level object id (e.g. `2`) wraps a `<component>` that points
  at the file containing the real mesh (object id `1` inside `object_1.model`). This lets BambuStudio reuse the
  same mesh file across multiple top-level objects/instances if needed.
- The **transform string is 12 numbers**: `m00 m01 m02 m10 m11 m12 m20 m21 m22 tx ty tz` (row-major 3x3 linear part,
  then translation). For simple axis-aligned placement you only need to change `tx ty tz` and can leave the
  identity `1 0 0 0 1 0 0 0 1` linear part alone.
- `<build><item>` is where an object is actually *placed* on a plate — this is the transform that must include the
  plate offset described in `plate-coordinate-system.md`.

## `3D/Objects/object_N.model` — mesh geometry

```xml
<model ...>
 <resources>
  <object id="1" type="model">
   <mesh>
    <vertices>
     <vertex x="49.5" y="-127" z="2.82499981"/>
     <!-- one per vertex, indices are implicit (0-based, in document order) -->
    </vertices>
    <triangles>
     <triangle v1="0" v2="1" v3="2"/>
     <!-- vN are 0-based vertex indices, winding determines outward normal -->
    </triangles>
   </mesh>
  </object>
 </resources>
 <build/>  <!-- empty; object files don't place themselves -->
</model>
```

Parse this with a plain XML parser (`xml.etree.ElementTree`) to pull out vertices/triangles as arrays, feed them
into `trimesh.Trimesh(vertices=..., faces=..., process=False)` for any real geometric edit, then re-serialize with
the same tag structure.

## `Metadata/model_settings.config` — project metadata (this is Bambu/Orca-specific, not core 3MF spec)

```xml
<config>
  <object id="2">                                   <!-- matches the top-level object id in 3dmodel.model -->
    <metadata key="name" value="part.stl"/>
    <metadata key="extruder" value="1"/>
    <metadata face_count="3192"/>
    <part id="1" subtype="normal_part">              <!-- matches the mesh object id inside object_1.model -->
      <metadata key="name" value="part.stl"/>
      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>  <!-- 4x4, part-local -->
      <metadata key="source_file" value="part.stl"/>
      <mesh_stat face_count="3192" .../>
    </part>
  </object>

  <plate>
    <metadata key="plater_id" value="1"/>
    <metadata key="thumbnail_file" value="Metadata/plate_1.png"/>
    <model_instance>
      <metadata key="object_id" value="2"/>          <!-- which top-level object is on this plate -->
      <metadata key="instance_id" value="0"/>
      <metadata key="identify_id" value="1643"/>      <!-- arbitrary positive int; not required to match anything -->
    </model_instance>
  </plate>
  <!-- one <plate> block per plate, in order; each with zero or more <model_instance> children -->

  <assemble>
   <assemble_item object_id="2" instance_id="0" transform="..." offset="0 0 0" />
   <!-- mirrors build items; keep transform identical to the corresponding <build><item> in 3dmodel.model -->
  </assemble>
</config>
```

Plate membership is decided by which `<plate>` block an object's `<model_instance>` appears in — **not** by its
coordinates. Coordinates only decide *where inside the shared scene* it renders (see
`plate-coordinate-system.md` for why both matter together).

## `Metadata/project_settings.config` — print settings (JSON, not XML)

A large flat JSON object, one key per setting, e.g.:

```json
{
  "printable_area": ["0x0", "256x0", "256x256", "0x256"],
  "printable_height": "250",
  "hot_plate_temp": ["70", "70", "70", "70"],
  ...
}
```

`printable_area` is four `"XxY"` corner strings defining the bed polygon (usually a rectangle) — parse the max X/Y
to get bed width/depth for the plate-offset math. Treat this file as the single source of truth for what a plate
will actually print with; edit only the specific key(s) requested, never reformat the whole file.

## `Metadata/cut_information.xml` — native Cut tool state

```xml
<objects>
 <object id="1">
  <cut_id id="0" check_sum="1" connectors_cnt="0"/>
 </object>
</objects>
```

This tracks BambuStudio's built-in Cut Tool state (for re-opening the cut dialog on a previously-cut part with its
connectors). When you replace geometry programmatically (not through the GUI cut tool), reset this to
`<objects></objects>` so stale part/connector references don't get misapplied.

## `[Content_Types].xml` and the `.rels` files

Standard OPC plumbing:
- `[Content_Types].xml` declares `Default Extension="model"` (and `rels`, `png`, `gcode`) — any new `.model` file
  is automatically covered, no edit needed there when adding objects.
- `_rels/.rels` (package root) points to `/3D/3dmodel.model` plus thumbnail relationships.
- `3D/_rels/3dmodel.model.rels` must have one `<Relationship>` per `Objects/object_N.model` referenced from
  `3dmodel.model` — **add one for every new object file you create**, or some parsers will fail to resolve it.
