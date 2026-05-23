"""
Fruit-tree growth/harvest stages — Batch 1 (6 trees × 6 states = 36 models).

Vanilla insight: all 5 OSRS-style fruit trees (apple/lemon/lime/orange/grapefruit)
share the same 156-face base structure (126 textured + 330 fruit). `exhaustedtree`
IS that base with the 330 fruit faces removed. `treestump` is a shared post-cut
model. Banana palm is structurally different but follows the same pattern with
`exhaustedpalm`.

States per tree:
  1_sapling          = exhausted @ 25%
  2_young            = exhausted @ 55%
  3_mature_empty     = exhausted (canonical, after harvest / before next fruiting)
  4_mature_partial   = full tree, ~60% of fruit faces removed (mid-harvest)
  5_mature_full      = vanilla copy (the harvest-ready perfect one)
  6_stump            = treestump (vanilla shared)
"""
import bpy
import bmesh
import os
import shutil
import math
import random

REF_DIR  = "/home/sparky/ogrs/art/models/_rsc_reference"
TREES_DIR = "/home/sparky/ogrs/art/models/farming/trees"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
os.makedirs(TREES_DIR, exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)


# Per-tree config. fruit_color_hex is the per-tree dominant face color we'll
# detect/remove when building "partial" state.
TREES = [
    {
        "name": "apple",
        "ripe":      "appletree",
        "exhausted": "exhaustedtree",
        "fruit_hex": "b01820",   # RGB(176,24,32) — apple red
    },
    {
        "name": "lemon",
        "ripe":      "lemontree",
        "exhausted": "exhaustedtree",
        "fruit_hex": "e8d038",   # RGB(232,208,56) — lemon yellow
    },
    {
        "name": "lime",
        "ripe":      "limetree",
        "exhausted": "exhaustedtree",
        "fruit_hex": "388010",   # RGB(56,128,16) — lime green
    },
    {
        "name": "orange",
        "ripe":      "orangetree",
        "exhausted": "exhaustedtree",
        "fruit_hex": "f8a010",   # RGB(248,160,16) — orange
    },
    {
        "name": "grapefruit",
        "ripe":      "grapefruittree",
        "exhausted": "exhaustedtree",
        "fruit_hex": "f08838",   # RGB(240,136,56) — grapefruit pink/peach
    },
    {
        "name": "banana",
        "ripe":      "bananapalm",
        "exhausted": "exhaustedpalm",
        "fruit_hex": "98a020",   # RGB(152,160,32) — banana yellow-green
    },
]


def ensure_ref(name):
    obj_path = f"{REF_DIR}/{name}.obj"
    mtl_path = f"{REF_DIR}/{name}.mtl"
    if not os.path.exists(obj_path):
        import subprocess
        subprocess.run(
            ["python3", "/home/sparky/ogrs/art/models/_extract_rsc_model.py", name],
            cwd="/home/sparky/ogrs/art/models",
            check=True,
        )
    return obj_path, mtl_path


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in list(bpy.data.meshes): bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials): bpy.data.materials.remove(block)


def import_obj(path):
    bpy.ops.wm.obj_import(filepath=path, forward_axis="NEGATIVE_Y", up_axis="Z")
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def export_obj(obj_name, out_path):
    bpy.ops.object.select_all(action="DESELECT")
    obj = bpy.data.objects[obj_name]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.obj_export(
        filepath=out_path, export_selected_objects=True, export_materials=True,
        forward_axis="NEGATIVE_Y", up_axis="Z",
    )


def join_to(name):
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    final = bpy.context.active_object
    final.name = name
    return final


def copy_with_renamed_mtl(src_obj, src_mtl, dst_obj, dst_mtl):
    shutil.copy(src_obj, dst_obj)
    shutil.copy(src_mtl, dst_mtl)
    with open(dst_obj, "r") as f: txt = f.read()
    txt = txt.replace(f"mtllib {os.path.basename(src_mtl)}", f"mtllib {os.path.basename(dst_mtl)}")
    with open(dst_obj, "w") as f: f.write(txt)


def remove_fraction_of_fruit_faces(obj, fruit_material_token, keep_fraction=0.4, seed=0):
    """
    Delete a random fraction of faces whose material name matches the fruit token.
    Keep `keep_fraction` of the fruit faces (e.g. 0.4 = keep 40%, remove 60%).
    """
    rng = random.Random(seed)
    me = obj.data
    # Build map of material slot index -> material name
    fruit_slots = set()
    for i, slot in enumerate(obj.material_slots):
        if slot.material and fruit_material_token.lower() in slot.material.name.lower():
            fruit_slots.add(i)
    if not fruit_slots:
        print(f"  ⚠ No fruit material slot matching '{fruit_material_token}' on {obj.name}")
        return
    # Pick faces to delete
    fruit_face_indices = [f.index for f in me.polygons if f.material_index in fruit_slots]
    n_to_delete = int(len(fruit_face_indices) * (1.0 - keep_fraction))
    to_delete = set(rng.sample(fruit_face_indices, n_to_delete))
    # Use bmesh to delete
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    bm.faces.ensure_lookup_table()
    faces_to_delete = [f for f in bm.faces if f.index in to_delete]
    bmesh.ops.delete(bm, geom=faces_to_delete, context="FACES")
    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode="OBJECT")
    print(f"  ✓ removed {n_to_delete}/{len(fruit_face_indices)} fruit faces ({keep_fraction*100:.0f}% kept)")


def build_tree(cfg):
    name = cfg["name"]
    ripe = cfg["ripe"]
    exhausted = cfg["exhausted"]
    fruit_hex = cfg["fruit_hex"]

    out_dir = f"{TREES_DIR}/{name}"
    os.makedirs(out_dir, exist_ok=True)
    print(f"\n=== Tree: {name} ({ripe} + {exhausted}) ===")

    ripe_obj, ripe_mtl = ensure_ref(ripe)
    ex_obj, ex_mtl = ensure_ref(exhausted)
    stump_obj, stump_mtl = ensure_ref("treestump")

    # State 5 — full fruit (vanilla copy)
    copy_with_renamed_mtl(
        ripe_obj, ripe_mtl,
        f"{out_dir}/5_mature_full.obj", f"{out_dir}/5_mature_full.mtl",
    )
    print(f"  ✓ 5_mature_full.obj  (vanilla {ripe})")

    # State 4 — partial fruit (vanilla, with ~60% of fruit faces removed)
    clear_scene()
    import_obj(ripe_obj)
    obj = join_to(f"{name}_4_partial")
    remove_fraction_of_fruit_faces(obj, fruit_hex, keep_fraction=0.40, seed=hash(name) & 0xffff)
    export_obj(obj.name, f"{out_dir}/4_mature_partial.obj")
    print(f"  ✓ 4_mature_partial.obj  (~40% fruit kept)")

    # State 3 — mature, no fruit (vanilla exhausted copy)
    copy_with_renamed_mtl(
        ex_obj, ex_mtl,
        f"{out_dir}/3_mature_empty.obj", f"{out_dir}/3_mature_empty.mtl",
    )
    print(f"  ✓ 3_mature_empty.obj  (vanilla {exhausted})")

    # State 2 — young @ 55%
    clear_scene()
    import_obj(ex_obj)
    obj = join_to(f"{name}_2_young")
    obj.scale = (0.55, 0.55, 0.55)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    export_obj(obj.name, f"{out_dir}/2_young.obj")
    print(f"  ✓ 2_young.obj  ({exhausted} @ 55%, tris={len(obj.data.polygons)})")

    # State 1 — sapling @ 25%
    clear_scene()
    import_obj(ex_obj)
    obj = join_to(f"{name}_1_sapling")
    obj.scale = (0.25, 0.25, 0.25)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    export_obj(obj.name, f"{out_dir}/1_sapling.obj")
    print(f"  ✓ 1_sapling.obj  ({exhausted} @ 25%, tris={len(obj.data.polygons)})")

    # State 6 — stump (vanilla, shared)
    copy_with_renamed_mtl(
        stump_obj, stump_mtl,
        f"{out_dir}/6_stump.obj", f"{out_dir}/6_stump.mtl",
    )
    print(f"  ✓ 6_stump.obj  (vanilla treestump)")


# ----------------------------------------------------------------
# Rendering — trees are TALL (2.48m), need bigger camera
# ----------------------------------------------------------------

def setup_camera(ortho_scale=4.0, cam_height=2.0):
    bpy.ops.object.camera_add(
        location=(3.0, -3.0, cam_height),
        rotation=(math.radians(70), 0, math.radians(45)),
    )
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="SUN", location=(2, -2, 4))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


def render_to(png_path, ortho_scale=4.0, cam_height=2.0):
    setup_camera(ortho_scale, cam_height)
    scn = bpy.context.scene
    scn.render.resolution_x = 256
    scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = png_path
    bpy.ops.render.render(write_still=True)


def render_state(out_dir, name, state_filename, cam_scale=4.0, cam_height=2.0):
    state_key = state_filename.replace(".obj", "")
    clear_scene()
    import_obj(f"{out_dir}/{state_filename}")
    render_to(f"{RENDER_DIR}/trees_{name}_{state_key}.png", cam_scale, cam_height)


def render_tree_states(cfg):
    name = cfg["name"]
    out_dir = f"{TREES_DIR}/{name}"
    # Different scales per state
    states_scales = [
        ("1_sapling.obj",          1.6, 0.6),  # tiny
        ("2_young.obj",            2.5, 1.0),  # medium
        ("3_mature_empty.obj",     4.0, 2.0),  # full size
        ("4_mature_partial.obj",   4.0, 2.0),
        ("5_mature_full.obj",      4.0, 2.0),
        ("6_stump.obj",            1.2, 0.3),  # very small
    ]
    for fname, scale, height in states_scales:
        render_state(out_dir, name, fname, scale, height)
    print(f"  ✓ rendered 6 states for {name}")


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------

def main():
    print(f"\n=== Fruit Trees Batch 1 — {len(TREES)} trees × 6 states ===\n")
    for cfg in TREES:
        build_tree(cfg)
    print(f"\n=== Rendering ===")
    for cfg in TREES:
        render_tree_states(cfg)
    print(f"\n=== Batch complete ===")


if __name__ == "__main__":
    main()
