"""
OGRS Farming — Tomato plant growth stages (3D, Blender 4.x bpy)

Run via:
  blender --background --python _build_tomato_stages.py

Output:
  ~/ogrs/art/models/farming/tomato/stage_{1..4}.obj  (low-poly meshes + .mtl)
  ~/ogrs/art/models/_renders/tomato_stage_{1..4}.png (orthographic preview renders)
  ~/ogrs/art/models/_renders/tomato_stages_strip.png (4-up comparison strip)

Stage progression (matches RSC farming convention):
  1 — Seedling      : 2 small leaves, ~0.15m tall
  2 — Growing       : Stalk + 6 leaves, no fruit, ~0.4m tall
  3 — Ripening      : Mature stalk + green tomatoes, ~0.6m tall
  4 — Harvest-ready : Mature stalk + ripe red tomatoes, ~0.6m tall

Style: Low-poly (RSC scenery aesthetic, ~50-200 tris per stage). Flat-shaded.
Materials: limited palette, flat colors (no PBR).
"""
import bpy
import bmesh
import math
import os
import sys

OUT_DIR = "/home/sparky/ogrs/art/models/farming/tomato"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)


# ============================================================
# Helpers
# ============================================================

def clear_scene():
    """Remove everything from the current scene."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in list(bpy.data.meshes):
        bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        bpy.data.materials.remove(block)


def make_material(name, rgba):
    """Create or get a flat-shaded material."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = rgba
            bsdf.inputs["Roughness"].default_value = 0.9
            bsdf.inputs["Specular IOR Level"].default_value = 0.0
    # Also set viewport color for viewport solid shading
    mat.diffuse_color = rgba
    return mat


def add_cylinder(name, radius, depth, location, rotation=(0, 0, 0), material=None, verts=8):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj


def add_uv_sphere(name, radius, location, material=None, segments=6, rings=4):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        radius=radius,
        location=location,
    )
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj


def add_leaf(name, scale, location, rotation, material):
    """Flattened ellipsoid as a leaf (low-poly)."""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=6,
        ring_count=4,
        radius=1.0,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    if material:
        obj.data.materials.append(material)
    return obj


def join_visible(target_name):
    """Join all currently-visible mesh objects into one."""
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not objs:
        return None
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    final = bpy.context.active_object
    final.name = target_name
    return final


def shade_flat(obj):
    """Force flat shading on all faces."""
    if not obj or obj.type != "MESH":
        return
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.faces_shade_flat()
    bpy.ops.object.mode_set(mode="OBJECT")


def export_obj(obj_name, out_path):
    bpy.ops.object.select_all(action="DESELECT")
    obj = bpy.data.objects[obj_name]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.obj_export(
        filepath=out_path,
        export_selected_objects=True,
        export_materials=True,
        forward_axis="NEGATIVE_Y",
        up_axis="Z",
    )


# ============================================================
# Materials (limited RSC-style palette)
# ============================================================

def setup_materials():
    return {
        "soil": make_material("Soil", (0.35, 0.22, 0.12, 1.0)),
        "stem": make_material("Stem", (0.30, 0.55, 0.22, 1.0)),
        "leaf": make_material("Leaf", (0.20, 0.62, 0.20, 1.0)),
        "leaf_dark": make_material("LeafDark", (0.15, 0.45, 0.15, 1.0)),
        "fruit_green": make_material("TomatoGreen", (0.45, 0.65, 0.25, 1.0)),
        "fruit_red": make_material("TomatoRed", (0.85, 0.18, 0.15, 1.0)),
        "fruit_red_hi": make_material("TomatoRedHi", (0.95, 0.35, 0.25, 1.0)),
    }


# ============================================================
# Soil base — present at every stage
# ============================================================

def build_soil(mats):
    """Small flat soil disc the patch sits on."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=0.5,
        depth=0.05,
        location=(0, 0, 0.025),
    )
    soil = bpy.context.active_object
    soil.name = "Soil"
    soil.data.materials.append(mats["soil"])
    return soil


# ============================================================
# Stage 1 — Seedling
# ============================================================

def build_stage_1(_):
    clear_scene()
    mats = setup_materials()
    build_soil(mats)
    # Two tiny leaves poking out
    add_leaf("Leaf1", scale=(0.08, 0.04, 0.03), location=(-0.05, 0, 0.08),
             rotation=(0, math.radians(20), math.radians(-30)), material=mats["leaf"])
    add_leaf("Leaf2", scale=(0.08, 0.04, 0.03), location=(0.05, 0, 0.08),
             rotation=(0, math.radians(-20), math.radians(30)), material=mats["leaf"])
    # Tiny stem
    add_cylinder("Stem", 0.012, 0.06, (0, 0, 0.08), material=mats["stem"], verts=6)

    obj = join_visible("Tomato_Stage1")
    shade_flat(obj)
    export_obj("Tomato_Stage1", f"{OUT_DIR}/stage_1.obj")
    print(f"  ✓ stage_1.obj  tris={len(obj.data.polygons)}")


# ============================================================
# Stage 2 — Growing (stalk + foliage, no fruit)
# ============================================================

def build_stage_2(_):
    clear_scene()
    mats = setup_materials()
    build_soil(mats)
    # Main stalk
    add_cylinder("Stem", 0.022, 0.40, (0, 0, 0.22), material=mats["stem"], verts=6)
    # 6 leaves at 3 height levels
    leaf_height_levels = [0.15, 0.28, 0.38]
    for i, h in enumerate(leaf_height_levels):
        for j, angle in enumerate([0, math.pi]):
            ox = math.cos(angle) * 0.12
            oy = math.sin(angle) * 0.12
            leaf_mat = mats["leaf"] if (i + j) % 2 == 0 else mats["leaf_dark"]
            add_leaf(f"Leaf_{i}_{j}",
                     scale=(0.13, 0.07, 0.04),
                     location=(ox, oy, h),
                     rotation=(0, math.radians(-15), angle),
                     material=leaf_mat)
    obj = join_visible("Tomato_Stage2")
    shade_flat(obj)
    export_obj("Tomato_Stage2", f"{OUT_DIR}/stage_2.obj")
    print(f"  ✓ stage_2.obj  tris={len(obj.data.polygons)}")


# ============================================================
# Stage 3 — Ripening (stalk + foliage + GREEN tomatoes)
# ============================================================

def build_stage_3(_):
    clear_scene()
    mats = setup_materials()
    build_soil(mats)
    add_cylinder("Stem", 0.025, 0.55, (0, 0, 0.30), material=mats["stem"], verts=6)
    # More foliage (4 height levels)
    leaf_levels = [0.18, 0.32, 0.45, 0.55]
    for i, h in enumerate(leaf_levels):
        for j, angle in enumerate([0, math.pi/2, math.pi, 3*math.pi/2]):
            ox = math.cos(angle) * 0.14
            oy = math.sin(angle) * 0.14
            leaf_mat = mats["leaf"] if (i + j) % 2 == 0 else mats["leaf_dark"]
            add_leaf(f"Leaf_{i}_{j}",
                     scale=(0.14, 0.075, 0.045),
                     location=(ox, oy, h),
                     rotation=(0, math.radians(-15), angle),
                     material=leaf_mat)
    # 4 green tomatoes at mid level
    fruit_positions = [
        ( 0.10, 0.06, 0.28),
        (-0.09, 0.05, 0.36),
        ( 0.08,-0.07, 0.42),
        (-0.07,-0.06, 0.50),
    ]
    for i, (x, y, z) in enumerate(fruit_positions):
        add_uv_sphere(f"Fruit_{i}", 0.06, (x, y, z), material=mats["fruit_green"])
    obj = join_visible("Tomato_Stage3")
    shade_flat(obj)
    export_obj("Tomato_Stage3", f"{OUT_DIR}/stage_3.obj")
    print(f"  ✓ stage_3.obj  tris={len(obj.data.polygons)}")


# ============================================================
# Stage 4 — Harvest-ready (stalk + foliage + RIPE RED tomatoes)
# ============================================================

def build_stage_4(_):
    clear_scene()
    mats = setup_materials()
    build_soil(mats)
    add_cylinder("Stem", 0.025, 0.55, (0, 0, 0.30), material=mats["stem"], verts=6)
    # Same foliage as stage 3
    leaf_levels = [0.18, 0.32, 0.45, 0.55]
    for i, h in enumerate(leaf_levels):
        for j, angle in enumerate([0, math.pi/2, math.pi, 3*math.pi/2]):
            ox = math.cos(angle) * 0.14
            oy = math.sin(angle) * 0.14
            leaf_mat = mats["leaf"] if (i + j) % 2 == 0 else mats["leaf_dark"]
            add_leaf(f"Leaf_{i}_{j}",
                     scale=(0.14, 0.075, 0.045),
                     location=(ox, oy, h),
                     rotation=(0, math.radians(-15), angle),
                     material=leaf_mat)
    # 6 ripe red tomatoes (bigger, more prominent)
    fruit_positions = [
        ( 0.11, 0.07, 0.25),
        (-0.10, 0.06, 0.34),
        ( 0.09,-0.08, 0.40),
        (-0.08,-0.07, 0.47),
        ( 0.07, 0.09, 0.52),
        (-0.06,-0.04, 0.55),
    ]
    for i, (x, y, z) in enumerate(fruit_positions):
        # Alternate slightly between red and red-hi for visual variety
        mat = mats["fruit_red"] if i % 2 == 0 else mats["fruit_red_hi"]
        add_uv_sphere(f"Fruit_{i}", 0.07, (x, y, z), material=mat)
    obj = join_visible("Tomato_Stage4")
    shade_flat(obj)
    export_obj("Tomato_Stage4", f"{OUT_DIR}/stage_4.obj")
    print(f"  ✓ stage_4.obj  tris={len(obj.data.polygons)}")


# ============================================================
# Render preview
# ============================================================

def setup_preview_camera_and_light():
    # Camera — orthographic, looking at the plant from a 30deg elevation
    bpy.ops.object.camera_add(location=(1.4, -1.4, 1.0), rotation=(math.radians(60), 0, math.radians(45)))
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 1.4
    bpy.context.scene.camera = cam

    # Sun light from upper-front
    bpy.ops.object.light_add(type="SUN", location=(2, -2, 3))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


def render_stage(stage_num, png_path):
    setup_preview_camera_and_light()
    scn = bpy.context.scene
    scn.render.resolution_x = 256
    scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = png_path
    bpy.ops.render.render(write_still=True)


# ============================================================
# Build all stages
# ============================================================

def main():
    print(f"\n=== Building tomato growth stages → {OUT_DIR} ===")

    stages = [
        ("Stage 1 — Seedling", build_stage_1, 1),
        ("Stage 2 — Growing",  build_stage_2, 2),
        ("Stage 3 — Ripening", build_stage_3, 3),
        ("Stage 4 — Harvest",  build_stage_4, 4),
    ]

    for label, builder, num in stages:
        print(f"\n[{label}]")
        builder(None)
        # Render preview
        render_stage(num, f"{RENDER_DIR}/tomato_stage_{num}.png")
        print(f"  ✓ render: {RENDER_DIR}/tomato_stage_{num}.png")

    print(f"\n=== Tomato stages complete ===")


if __name__ == "__main__":
    main()
