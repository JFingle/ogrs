"""
Farming Batch 2 — 5 remaining items derived from vanilla geometry.

  pineapple    — pineappleplant + depletedplant
                 (fruit body color: #B88838 yellow-tan, 802 faces is fruit+spikes)
  dragonfruit  — dragonfruit + depleteddragonfruit
                 (fruit color: #880830 deep red-pink, 225 faces)
  coconut      — coconutpalm + exhaustedpalm
                 (coconut color: #D0B058 tan-cream, 528 faces — fruit+trunk mix)
  papaya       — papayapalm + exhaustedpalm (fallback, structurally close)
                 (fruit color: #A88010 yellow-orange, 528 faces — fruit+trunk mix)
  herb         — herb (4-stage only, scale progression, no fruit logic)

For palms (coconut/papaya), the dominant 528-face material includes both fruit
and trunk, so removing 60% leaves a sparse-fruit look that reads as partial-harvest.
"""
import bpy
import bmesh
import math
import os
import shutil
import random

REF_DIR = "/home/sparky/ogrs/art/models/_rsc_reference"
FARMING_DIR = "/home/sparky/ogrs/art/models/farming"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"


CROPS = [
    {
        "name": "pineapple",
        "ripe":      "pineappleplant",
        "depleted":  "depletedplant",
        "fruit_hex": "b88838",      # yellow-tan pineapple body
        "ortho":     1.0,
        "states": 6,
    },
    {
        "name": "dragonfruit",
        "ripe":      "dragonfruit",
        "depleted":  "depleteddragonfruit",
        "fruit_hex": "880830",      # deep red-pink dragonfruit
        "ortho":     4.5,
        "states": 6,
    },
    {
        "name": "coconut",
        "ripe":      "coconutpalm",
        "depleted":  "exhaustedpalm",
        "fruit_hex": "d0b058",      # coconut tan-cream
        "ortho":     4.0,
        "states": 6,
    },
    {
        "name": "papaya",
        "ripe":      "papayapalm",
        "depleted":  "exhaustedpalm",
        "fruit_hex": "a88010",      # papaya yellow-orange
        "ortho":     4.0,
        "states": 6,
    },
    {
        "name": "herb",
        "ripe":      "herb",
        "depleted":  None,
        "fruit_hex": None,
        "ortho":     1.5,
        "states": 4,                # sapling, growing, mature, picked
    },
]


def ensure_ref(name):
    obj_path = f"{REF_DIR}/{name}.obj"
    mtl_path = f"{REF_DIR}/{name}.mtl"
    if not os.path.exists(obj_path):
        import subprocess
        subprocess.run(
            ["python3", "/home/sparky/ogrs/art/models/_extract_rsc_model.py", name],
            cwd="/home/sparky/ogrs/art/models", check=True,
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


def remove_fraction_of_faces(obj, material_token, keep_fraction=0.4, seed=0):
    rng = random.Random(seed)
    me = obj.data
    target_slots = set()
    for i, slot in enumerate(obj.material_slots):
        if slot.material and material_token.lower() in slot.material.name.lower():
            target_slots.add(i)
    if not target_slots:
        print(f"  ⚠ No slot matching '{material_token}' on {obj.name}")
        return
    fi = [f.index for f in me.polygons if f.material_index in target_slots]
    n_to_delete = int(len(fi) * (1.0 - keep_fraction))
    to_delete = set(rng.sample(fi, n_to_delete))
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    bm.faces.ensure_lookup_table()
    faces_to_delete = [f for f in bm.faces if f.index in to_delete]
    bmesh.ops.delete(bm, geom=faces_to_delete, context="FACES")
    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode="OBJECT")
    print(f"  ✓ removed {n_to_delete}/{len(fi)} fruit-color faces")


# ----------------------------------------------------------------
# Per-crop build
# ----------------------------------------------------------------

def build_6_state_crop(cfg, out_dir):
    """For pineapple/dragonfruit/coconut/papaya — 6 states with partial fruit logic."""
    ripe_obj, ripe_mtl = ensure_ref(cfg["ripe"])
    if cfg["depleted"]:
        ex_obj, ex_mtl = ensure_ref(cfg["depleted"])
    else:
        ex_obj, ex_mtl = ripe_obj, ripe_mtl

    # 5_mature_full — vanilla copy
    copy_with_renamed_mtl(ripe_obj, ripe_mtl,
                          f"{out_dir}/5_mature_full.obj", f"{out_dir}/5_mature_full.mtl")
    print(f"  ✓ 5_mature_full.obj  (vanilla {cfg['ripe']})")

    # 4_mature_partial — vanilla, ~60% of fruit-color faces deleted
    clear_scene()
    import_obj(ripe_obj)
    obj = join_to(f"{cfg['name']}_4_partial")
    if cfg["fruit_hex"]:
        remove_fraction_of_faces(obj, cfg["fruit_hex"], keep_fraction=0.40,
                                  seed=hash(cfg["name"]) & 0xffff)
    export_obj(obj.name, f"{out_dir}/4_mature_partial.obj")
    print(f"  ✓ 4_mature_partial.obj")

    # 3_mature_empty — vanilla depleted copy (or fallback)
    copy_with_renamed_mtl(ex_obj, ex_mtl,
                          f"{out_dir}/3_mature_empty.obj", f"{out_dir}/3_mature_empty.mtl")
    print(f"  ✓ 3_mature_empty.obj  ({cfg['depleted'] or 'fallback'})")

    # 2_young @ 55%
    clear_scene()
    import_obj(ex_obj)
    obj = join_to(f"{cfg['name']}_2_young")
    obj.scale = (0.55, 0.55, 0.55)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    export_obj(obj.name, f"{out_dir}/2_young.obj")
    print(f"  ✓ 2_young.obj  (@55%)")

    # 1_sapling @ 25%
    clear_scene()
    import_obj(ex_obj)
    obj = join_to(f"{cfg['name']}_1_sapling")
    obj.scale = (0.25, 0.25, 0.25)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    export_obj(obj.name, f"{out_dir}/1_sapling.obj")
    print(f"  ✓ 1_sapling.obj  (@25%)")

    # 6_dead — vanilla treestump shared OR none for non-tree crops
    # For palms, use treestump. For pineapple/dragonfruit, use depleted at 50% as "gone"
    stump_obj, stump_mtl = ensure_ref("treestump")
    if cfg["name"] in ("coconut", "papaya"):
        copy_with_renamed_mtl(stump_obj, stump_mtl,
                              f"{out_dir}/6_stump.obj", f"{out_dir}/6_stump.mtl")
        print(f"  ✓ 6_stump.obj  (vanilla treestump)")
    else:
        # For non-tree crops, "dead" = empty depleted state at smaller scale
        clear_scene()
        import_obj(ex_obj)
        obj = join_to(f"{cfg['name']}_6_dead")
        obj.scale = (0.65, 0.65, 0.65)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        export_obj(obj.name, f"{out_dir}/6_dead.obj")
        print(f"  ✓ 6_dead.obj  ({cfg['depleted']} @65%)")


def build_4_state_herb(cfg, out_dir):
    """Herb: 4 stages only — sapling, growing, mature, picked."""
    ripe_obj, ripe_mtl = ensure_ref(cfg["ripe"])

    # 4_mature — full vanilla copy
    copy_with_renamed_mtl(ripe_obj, ripe_mtl,
                          f"{out_dir}/4_mature.obj", f"{out_dir}/4_mature.mtl")
    print(f"  ✓ 4_mature.obj  (vanilla {cfg['ripe']})")

    # 3_growing @ 70%
    clear_scene()
    import_obj(ripe_obj)
    obj = join_to(f"{cfg['name']}_3_growing")
    obj.scale = (0.7, 0.7, 0.7)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    export_obj(obj.name, f"{out_dir}/3_growing.obj")
    print(f"  ✓ 3_growing.obj  (@70%)")

    # 2_sprouting @ 40%
    clear_scene()
    import_obj(ripe_obj)
    obj = join_to(f"{cfg['name']}_2_sprouting")
    obj.scale = (0.4, 0.4, 0.4)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    export_obj(obj.name, f"{out_dir}/2_sprouting.obj")
    print(f"  ✓ 2_sprouting.obj  (@40%)")

    # 1_seedling @ 20%
    clear_scene()
    import_obj(ripe_obj)
    obj = join_to(f"{cfg['name']}_1_seedling")
    obj.scale = (0.2, 0.2, 0.2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    export_obj(obj.name, f"{out_dir}/1_seedling.obj")
    print(f"  ✓ 1_seedling.obj  (@20%)")


# ----------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------

def setup_camera(ortho_scale, cam_height):
    bpy.ops.object.camera_add(
        location=(cam_height * 1.5, -cam_height * 1.5, cam_height * 0.8),
        rotation=(math.radians(65), 0, math.radians(45)),
    )
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="SUN", location=(2, -2, 3))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


def render_state(out_dir, name, fname, ortho_scale, cam_height):
    state_key = fname.replace(".obj", "")
    clear_scene()
    import_obj(f"{out_dir}/{fname}")
    setup_camera(ortho_scale, cam_height)
    scn = bpy.context.scene
    scn.render.resolution_x = 256
    scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = f"{RENDER_DIR}/v3_{name}_{state_key}.png"
    bpy.ops.render.render(write_still=True)


def render_crop(cfg, out_dir):
    name = cfg["name"]
    ortho = cfg["ortho"]
    cam_h = max(0.6, ortho * 0.5)
    if cfg["states"] == 6:
        for fname in ("1_sapling.obj", "2_young.obj", "3_mature_empty.obj",
                      "4_mature_partial.obj", "5_mature_full.obj"):
            # Scale ortho per state — saplings tighter, mature wider
            if "sapling" in fname:
                s = ortho * 0.5
            elif "young" in fname:
                s = ortho * 0.75
            else:
                s = ortho
            render_state(out_dir, name, fname, s, cam_h)
        # 6: stump or dead
        last_file = "6_stump.obj" if cfg["name"] in ("coconut", "papaya") else "6_dead.obj"
        render_state(out_dir, name, last_file, ortho * 0.5, cam_h * 0.4)
    else:
        for fname in ("1_seedling.obj", "2_sprouting.obj", "3_growing.obj", "4_mature.obj"):
            if "seedling" in fname:
                s = ortho * 0.4
            elif "sprouting" in fname:
                s = ortho * 0.6
            elif "growing" in fname:
                s = ortho * 0.85
            else:
                s = ortho
            render_state(out_dir, name, fname, s, cam_h)
    print(f"  ✓ rendered {cfg['states']} states for {name}")


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------

def main():
    print(f"\n=== Farming Batch 2 — {len(CROPS)} items ===\n")
    for cfg in CROPS:
        out_dir = f"{FARMING_DIR}/{cfg['name']}"
        os.makedirs(out_dir, exist_ok=True)
        print(f"\n=== {cfg['name']} ({cfg['ripe']} + {cfg['depleted']}, {cfg['states']} states) ===")
        if cfg["states"] == 6:
            build_6_state_crop(cfg, out_dir)
        else:
            build_4_state_herb(cfg, out_dir)

    print(f"\n=== Rendering ===")
    for cfg in CROPS:
        out_dir = f"{FARMING_DIR}/{cfg['name']}"
        render_crop(cfg, out_dir)
    print(f"\n=== Batch 2 complete ===")


if __name__ == "__main__":
    main()
