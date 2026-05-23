"""
Tomato growth stages v2 — built from RSC reference.

Strategy (after extracting vanilla tomatoplant.ob3 + depletedtomato.ob3):
  • Stage 4 (ripe)      → REUSE vanilla `tomatoplant` (498 faces, model already in cache)
  • Stage 3 (mature)    → smaller derivative bush, green-only with a few green fruit
  • Stage 2 (growing)   → small bush, leaves only
  • Stage 1 (seedling)  → 2-3 tiny leaves poking from soil

Reference palette (extracted from .ob3 face colors via RGB15 decode):
  • Foliage green:  RGB(80, 112, 48)  = #507030  (muted olive, NOT bright lime)
  • Tomato red:     RGB(248, 0, 8)    = #F80008  (saturated pure red)
  • Green-fruit:    RGB(120, 176, 56) = #78B038  (garlic-plant green, used as unripe)
  • Soil:           RGB(96, 64, 32)   = #604020

The bush silhouette mimics the vanilla model bounds (X: -22..15, Y: -49..0 game-units).
Game scale = 0.01 → meters. Vanilla plant is ~0.49m tall × ~0.37m wide.

Output:
  ~/ogrs/art/models/farming/tomato_v2/stage_{1,2,3}.obj + .mtl   (newly authored)
  ~/ogrs/art/models/farming/tomato_v2/stage_4.obj                (copy of vanilla)
  ~/ogrs/art/models/_renders/v2_tomato_{1,2,3,4,reference}.png
  ~/ogrs/art/models/_renders/v2_tomato_strip.png
"""
import bpy
import bmesh
import math
import os
import shutil
import random

OUT_DIR = "/home/sparky/ogrs/art/models/farming/tomato_v2"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
RSC_REF_DIR = "/home/sparky/ogrs/art/models/_rsc_reference"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)

# RSC palette (extracted from .ob3)
PAL = {
    "foliage":  (80/255, 112/255, 48/255, 1.0),   # #507030
    "fruit":    (248/255, 0/255, 8/255, 1.0),     # #F80008
    "unripe":   (120/255, 176/255, 56/255, 1.0),  # #78B038
    "soil":     (96/255, 64/255, 32/255, 1.0),    # #604020
}


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in list(bpy.data.meshes):
        bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        bpy.data.materials.remove(block)


def make_material(name, rgba):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Roughness"].default_value = 1.0
        bsdf.inputs["Specular IOR Level"].default_value = 0.0
    mat.diffuse_color = rgba
    return mat


def setup_palette():
    return {k: make_material(f"rsc_{k}", v) for k, v in PAL.items()}


# ----------------------------------------------------------------
# Leaf primitive — small angular wedge resembling a tomato leaflet
# ----------------------------------------------------------------

def add_leaf_cluster(center, scale, count, material, jitter=0.04, seed=0):
    """
    Build a leaf cluster by adding `count` small angular wedges in random
    orientations around a center point. Mimics the dense bushy look of the
    vanilla tomatoplant.
    """
    rng = random.Random(seed)
    for i in range(count):
        # Random direction (mostly up + outward)
        theta = rng.uniform(0, 2 * math.pi)
        phi = rng.uniform(0.2, 1.2)  # bias upward
        r = rng.uniform(0.6, 1.0) * scale
        ox = center[0] + math.cos(theta) * math.sin(phi) * r + rng.uniform(-jitter, jitter)
        oy = center[1] + math.sin(theta) * math.sin(phi) * r + rng.uniform(-jitter, jitter)
        oz = center[2] + math.cos(phi) * r + rng.uniform(-jitter, jitter)
        # Use icosphere subsurf=1 (20 tris) — gives angular faceting like RSC
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1,
            radius=scale * 0.45,
            location=(ox, oy, oz),
        )
        leaf = bpy.context.active_object
        # Flatten slightly so it reads as foliage cluster, not balls
        leaf.scale = (1.0, 1.0, 0.55)
        leaf.rotation_euler = (
            rng.uniform(0, math.pi/4),
            rng.uniform(0, math.pi/4),
            rng.uniform(0, math.pi*2),
        )
        leaf.data.materials.append(material)


def add_fruit(center, radius, material, seed=0):
    """Add a single tomato fruit (low-poly sphere)."""
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,
        radius=radius,
        location=center,
    )
    fruit = bpy.context.active_object
    fruit.data.materials.append(material)
    return fruit


def build_soil_disc(mats, radius=0.20):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=radius, depth=0.02, location=(0, 0, 0.01)
    )
    obj = bpy.context.active_object
    obj.data.materials.append(mats["soil"])
    return obj


def join_visible(target_name):
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
    if not obj or obj.type != "MESH": return
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


# ----------------------------------------------------------------
# Stage builders
# ----------------------------------------------------------------

def build_stage_1():
    """Seedling — 2-3 tiny leaves on soil."""
    clear_scene()
    mats = setup_palette()
    build_soil_disc(mats, radius=0.12)
    # 3 tiny leaf wedges
    add_leaf_cluster((0, 0, 0.04), scale=0.05, count=3, material=mats["foliage"], jitter=0.01, seed=11)
    obj = join_visible("Tomato_Stage1_v2")
    shade_flat(obj)
    export_obj("Tomato_Stage1_v2", f"{OUT_DIR}/stage_1.obj")
    print(f"  ✓ stage_1.obj  tris={len(obj.data.polygons)}")


def build_stage_2():
    """Growing — small bush, leaves only."""
    clear_scene()
    mats = setup_palette()
    build_soil_disc(mats)
    # Dense leaf cluster filling the lower half of the silhouette
    # Bush bounds: X ±0.10, Y ±0.10, Z 0.02..0.20 (~half final height)
    add_leaf_cluster((0, 0, 0.10), scale=0.10, count=8, material=mats["foliage"], jitter=0.04, seed=22)
    add_leaf_cluster((0, 0, 0.07), scale=0.10, count=6, material=mats["foliage"], jitter=0.04, seed=23)
    obj = join_visible("Tomato_Stage2_v2")
    shade_flat(obj)
    export_obj("Tomato_Stage2_v2", f"{OUT_DIR}/stage_2.obj")
    print(f"  ✓ stage_2.obj  tris={len(obj.data.polygons)}")


def build_stage_3():
    """Mature/ripening — larger bush, leaves + small green fruit."""
    clear_scene()
    mats = setup_palette()
    build_soil_disc(mats)
    # Bush bounds: X ±0.18, Y ±0.16, Z 0.02..0.40 (close to vanilla scale)
    add_leaf_cluster((0, 0, 0.25), scale=0.18, count=14, material=mats["foliage"], jitter=0.06, seed=31)
    add_leaf_cluster((0, 0, 0.15), scale=0.16, count=10, material=mats["foliage"], jitter=0.06, seed=32)
    # 4-5 small unripe green fruit mixed in
    fruit_positions = [
        (0.10, 0.04, 0.18),
        (-0.08, 0.07, 0.22),
        (0.06, -0.09, 0.28),
        (-0.05, -0.08, 0.32),
        (0.09, 0.10, 0.34),
    ]
    for p in fruit_positions:
        add_fruit(p, 0.035, mats["unripe"], seed=int(p[0]*100))
    obj = join_visible("Tomato_Stage3_v2")
    shade_flat(obj)
    export_obj("Tomato_Stage3_v2", f"{OUT_DIR}/stage_3.obj")
    print(f"  ✓ stage_3.obj  tris={len(obj.data.polygons)}")


def copy_stage_4_from_vanilla():
    """Stage 4 is the vanilla tomatoplant model — copy reference files in place."""
    src_obj = f"{RSC_REF_DIR}/tomatoplant.obj"
    src_mtl = f"{RSC_REF_DIR}/tomatoplant.mtl"
    dst_obj = f"{OUT_DIR}/stage_4.obj"
    dst_mtl = f"{OUT_DIR}/stage_4.mtl"
    if os.path.exists(src_obj):
        shutil.copy(src_obj, dst_obj)
        # Rewrite mtllib reference inside the .obj to point to stage_4.mtl
        with open(dst_obj, "r") as f: txt = f.read()
        txt = txt.replace("mtllib tomatoplant.mtl", "mtllib stage_4.mtl")
        with open(dst_obj, "w") as f: f.write(txt)
    if os.path.exists(src_mtl):
        shutil.copy(src_mtl, dst_mtl)
    print(f"  ✓ stage_4.obj  (vanilla tomatoplant, 498 faces)")


# ----------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------

def setup_preview_camera_and_light():
    bpy.ops.object.camera_add(
        location=(0.6, -0.6, 0.5),
        rotation=(math.radians(65), 0, math.radians(45)),
    )
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 0.7
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="SUN", location=(1.5, -1.5, 2))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


def render_to(png_path):
    setup_preview_camera_and_light()
    scn = bpy.context.scene
    scn.render.resolution_x = 256
    scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = png_path
    bpy.ops.render.render(write_still=True)


def import_obj_for_render(obj_path):
    """Import an .obj into a clean scene, return the imported object."""
    clear_scene()
    bpy.ops.wm.obj_import(filepath=obj_path, forward_axis="NEGATIVE_Y", up_axis="Z")
    # The imported objects will have materials from the .mtl. Position at origin.
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def render_reference():
    """Render the vanilla tomatoplant.obj for comparison."""
    print("[Reference — vanilla tomatoplant]")
    import_obj_for_render(f"{RSC_REF_DIR}/tomatoplant.obj")
    render_to(f"{RENDER_DIR}/v2_tomato_reference.png")
    print(f"  ✓ render: v2_tomato_reference.png")


def render_v2_stage(num):
    obj_path = f"{OUT_DIR}/stage_{num}.obj"
    print(f"[V2 — stage {num}]")
    import_obj_for_render(obj_path)
    render_to(f"{RENDER_DIR}/v2_tomato_{num}.png")
    print(f"  ✓ render: v2_tomato_{num}.png")


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------

def main():
    print(f"\n=== Tomato v2 — using extracted RSC palette ===")

    # Author stages 1-3
    print("\n[Stage 1 — Seedling]")
    build_stage_1()
    print("\n[Stage 2 — Growing]")
    build_stage_2()
    print("\n[Stage 3 — Ripening]")
    build_stage_3()

    # Stage 4 = vanilla copy
    print("\n[Stage 4 — Harvest (vanilla)]")
    copy_stage_4_from_vanilla()

    # Render
    print("\n=== Rendering ===")
    render_reference()
    for n in (1, 2, 3, 4):
        render_v2_stage(n)

    print("\n=== Tomato v2 complete ===")


if __name__ == "__main__":
    main()
