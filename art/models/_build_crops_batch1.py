"""
Farming 3D growth stages — Batch 1 (6 crops, derived from vanilla RSC geometry).

For each crop:
  stage_4 = vanilla ripe model (untouched copy)
  stage_3 = either recolor ripe (if there's a "fruit"-vs-"foliage" color split)
            OR scale ripe to ~85% (no color differentiation)
  stage_2 = either depleted @ 60% (if vanilla has a depleted model)
            OR ripe @ 55%
  stage_1 = either depleted @ 25%
            OR ripe @ 25%

Config-driven so adding new crops later is trivial.
"""
import bpy
import os
import shutil

REF_DIR  = "/home/sparky/ogrs/art/models/_rsc_reference"
MODELS_DIR = "/home/sparky/ogrs/art/models/farming"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"

# Per-crop config
CROPS = [
    {
        "name": "corn",
        "ripe":     "cornplant",       # 415 faces
        "depleted": "depletedcorn",    # 168 faces
        # Stage 3: recolor yellow corn-tassel into unripe husk-tan (drop the yellow)
        # tassel raw=-28358 -> RGB(216,176,48) yellow
        # replace with husk-tan raw=-25263 -> RGB(192,168,120)
        "ripening_recolor": {
            "from_hex": "d8b030",      # corn tassel yellow
            "to_rgb":   (192/255, 168/255, 120/255),
            "to_ka":    (38/255,  33/255,  24/255),
        },
    },
    {
        "name": "potato",
        "ripe":     "potatoplant",
        "depleted": None,
        "ripening_recolor": None,
    },
    {
        "name": "onion",
        "ripe":     "onionplant",
        "depleted": None,
        "ripening_recolor": None,
    },
    {
        "name": "garlic",
        "ripe":     "garlicplant",
        "depleted": None,
        "ripening_recolor": None,
    },
    {
        "name": "cabbage_green",
        "ripe":     "greencabbage",
        "depleted": None,
        "ripening_recolor": None,
    },
    {
        "name": "cabbage_red",
        "ripe":     "redcabbage",
        "depleted": None,
        "ripening_recolor": None,
    },
]


def ensure_ref(name):
    """Make sure the vanilla .obj is extracted; return paths."""
    obj_path = f"{REF_DIR}/{name}.obj"
    mtl_path = f"{REF_DIR}/{name}.mtl"
    if not os.path.exists(obj_path):
        # Run the extractor on the fly
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
    for block in list(bpy.data.meshes):
        bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        bpy.data.materials.remove(block)


def import_obj(path):
    bpy.ops.wm.obj_import(filepath=path, forward_axis="NEGATIVE_Y", up_axis="Z")
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


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


def join_to(name):
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    final = bpy.context.active_object
    final.name = name
    return final


def copy_obj_with_renamed_mtl(src_obj, src_mtl, dst_obj, dst_mtl):
    shutil.copy(src_obj, dst_obj)
    shutil.copy(src_mtl, dst_mtl)
    src_mtl_name = os.path.basename(src_mtl)
    dst_mtl_name = os.path.basename(dst_mtl)
    with open(dst_obj, "r") as f: txt = f.read()
    txt = txt.replace(f"mtllib {src_mtl_name}", f"mtllib {dst_mtl_name}")
    with open(dst_obj, "w") as f: f.write(txt)


def recolor_material(mtl_path, from_hex, to_rgb, to_ka):
    """In a .mtl file, find the material named rsc_<from_hex> and replace its Kd/Ka."""
    from_marker = from_hex.lower()
    with open(mtl_path, "r") as f:
        lines = f.readlines()
    new_lines = []
    in_match = False
    for ln in lines:
        if ln.startswith("newmtl "):
            in_match = from_marker in ln.lower()
        if in_match and ln.startswith("Kd "):
            new_lines.append(f"Kd {to_rgb[0]:.4f} {to_rgb[1]:.4f} {to_rgb[2]:.4f}\n")
            continue
        if in_match and ln.startswith("Ka "):
            new_lines.append(f"Ka {to_ka[0]:.4f} {to_ka[1]:.4f} {to_ka[2]:.4f}\n")
            continue
        new_lines.append(ln)
    with open(mtl_path, "w") as f:
        f.writelines(new_lines)


def build_crop(cfg):
    name = cfg["name"]
    ripe = cfg["ripe"]
    depleted = cfg["depleted"]
    recolor = cfg["ripening_recolor"]

    out_dir = f"{MODELS_DIR}/{name}"
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n=== Crop: {name} (ripe={ripe}, depleted={depleted}) ===")

    # Make sure reference .obj exists
    ripe_obj, ripe_mtl = ensure_ref(ripe)
    if depleted:
        dep_obj, dep_mtl = ensure_ref(depleted)

    # ----- Stage 4 — vanilla copy -----
    copy_obj_with_renamed_mtl(
        ripe_obj, ripe_mtl,
        f"{out_dir}/stage_4.obj", f"{out_dir}/stage_4.mtl",
    )
    print(f"  ✓ stage_4.obj  (vanilla {ripe} copy)")

    # ----- Stage 3 — either recolor or scale -----
    s3_obj = f"{out_dir}/stage_3.obj"
    s3_mtl = f"{out_dir}/stage_3.mtl"
    if recolor:
        copy_obj_with_renamed_mtl(ripe_obj, ripe_mtl, s3_obj, s3_mtl)
        recolor_material(s3_mtl, recolor["from_hex"], recolor["to_rgb"], recolor["to_ka"])
        print(f"  ✓ stage_3.obj  ({ripe} with #{recolor['from_hex']} -> unripe)")
    else:
        # Scale to 85%
        clear_scene()
        import_obj(ripe_obj)
        obj = join_to(f"{name}_stage3")
        obj.scale = (0.85, 0.85, 0.85)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        export_obj(obj.name, s3_obj)
        print(f"  ✓ stage_3.obj  ({ripe} @ 85%, tris={len(obj.data.polygons)})")

    # ----- Stages 1 + 2 — scaled depleted (if available) or scaled ripe -----
    src_for_early = (dep_obj, dep_mtl) if depleted else (ripe_obj, ripe_mtl)
    src_obj, _ = src_for_early
    src_name = depleted or ripe

    for stage_num, scale in [(2, 0.55), (1, 0.25)]:
        clear_scene()
        import_obj(src_obj)
        obj = join_to(f"{name}_stage{stage_num}")
        obj.scale = (scale, scale, scale)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        export_obj(obj.name, f"{out_dir}/stage_{stage_num}.obj")
        print(f"  ✓ stage_{stage_num}.obj  ({src_name} @ {scale*100:.0f}%, tris={len(obj.data.polygons)})")


# ----------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------

import math

def setup_preview_camera_and_light(ortho_scale=0.7):
    bpy.ops.object.camera_add(
        location=(0.6, -0.6, 0.5),
        rotation=(math.radians(65), 0, math.radians(45)),
    )
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="SUN", location=(1.5, -1.5, 2))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


def render_to(png_path, ortho_scale=0.7):
    setup_preview_camera_and_light(ortho_scale)
    scn = bpy.context.scene
    scn.render.resolution_x = 256
    scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = png_path
    bpy.ops.render.render(write_still=True)


def crop_ortho_scale(name):
    """Different crops have different sizes. Corn is huge (1.92m), cabbage low/wide."""
    if name.startswith("cabbage"):
        return 0.85
    if name == "corn":
        return 2.2
    return 0.7


def render_crop_stages(cfg):
    name = cfg["name"]
    out_dir = f"{MODELS_DIR}/{name}"
    sc = crop_ortho_scale(name)
    for n in (1, 2, 3, 4):
        clear_scene()
        import_obj(f"{out_dir}/stage_{n}.obj")
        render_to(f"{RENDER_DIR}/v3_{name}_{n}.png", ortho_scale=sc)
    # Also reference render (in case different from stage_4)
    clear_scene()
    import_obj(f"{REF_DIR}/{cfg['ripe']}.obj")
    render_to(f"{RENDER_DIR}/v3_{name}_ref.png", ortho_scale=sc)
    print(f"  ✓ rendered 5 PNGs for {name}")


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------

def main():
    print(f"\n=== Farming Batch 1 — {len(CROPS)} crops × 4 stages ===\n")
    for cfg in CROPS:
        build_crop(cfg)

    print(f"\n=== Rendering all stages ===")
    for cfg in CROPS:
        render_crop_stages(cfg)

    print(f"\n=== Batch 1 complete ===")


if __name__ == "__main__":
    main()
