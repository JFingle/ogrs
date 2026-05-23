"""
Tomato growth stages v3 — derived ENTIRELY from vanilla RSC geometry.

Stage 4 (ripe, perfect)   = vanilla tomatoplant.obj           — copy
Stage 3 (almost ripe)     = tomatoplant with red faces recolored to unripe-green
Stage 2 (growing)         = depletedtomato.obj scaled 60%
Stage 1 (seedling)        = depletedtomato.obj scaled 25%

This guarantees the silhouette / face density / topology / palette match
the vanilla RSC look exactly. The only stage-specific changes are color
(stage 3) and uniform scale (stages 1-2).
"""
import bpy
import math
import os
import shutil

OUT_DIR  = "/home/sparky/ogrs/art/models/farming/tomato_v3"
REF_DIR  = "/home/sparky/ogrs/art/models/_rsc_reference"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)

# RSC palette (extracted)
RSC_RED    = "#F80008"
RSC_UNRIPE = "#78B038"


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


# ----------------------------------------------------------------
# Stage 4 — vanilla copy
# ----------------------------------------------------------------

def build_stage_4():
    """Direct copy of vanilla tomatoplant.obj + .mtl."""
    src_obj = f"{REF_DIR}/tomatoplant.obj"
    src_mtl = f"{REF_DIR}/tomatoplant.mtl"
    dst_obj = f"{OUT_DIR}/stage_4.obj"
    dst_mtl = f"{OUT_DIR}/stage_4.mtl"
    shutil.copy(src_obj, dst_obj)
    shutil.copy(src_mtl, dst_mtl)
    with open(dst_obj, "r") as f: txt = f.read()
    txt = txt.replace("mtllib tomatoplant.mtl", "mtllib stage_4.mtl")
    with open(dst_obj, "w") as f: f.write(txt)
    print(f"  ✓ stage_4.obj  (vanilla tomatoplant, untouched)")


# ----------------------------------------------------------------
# Stage 3 — tomatoplant with red faces recolored to unripe-green
# ----------------------------------------------------------------

def build_stage_3():
    """Copy tomatoplant.obj + .mtl, then swap the RED material to UNRIPE-GREEN."""
    src_obj = f"{REF_DIR}/tomatoplant.obj"
    src_mtl = f"{REF_DIR}/tomatoplant.mtl"
    dst_obj = f"{OUT_DIR}/stage_3.obj"
    dst_mtl = f"{OUT_DIR}/stage_3.mtl"
    shutil.copy(src_obj, dst_obj)
    shutil.copy(src_mtl, dst_mtl)

    # Rewrite the obj's mtllib reference
    with open(dst_obj, "r") as f: txt = f.read()
    txt = txt.replace("mtllib tomatoplant.mtl", "mtllib stage_3.mtl")
    with open(dst_obj, "w") as f: f.write(txt)

    # In the .mtl, find the red material (Kd ~ 0.97, 0.0, 0.03) and recolor it.
    # The extracted material name is rsc_f80008 (lowercase hex). Replace its Kd line.
    with open(dst_mtl, "r") as f:
        mtl_lines = f.readlines()
    new_lines = []
    in_red_mat = False
    for ln in mtl_lines:
        if ln.startswith("newmtl "):
            in_red_mat = "f80008" in ln.lower() or "F80008" in ln
        if in_red_mat and ln.startswith("Kd "):
            # Replace with unripe-green RGB(120, 176, 56) -> 0.4706, 0.6902, 0.2196
            new_lines.append("Kd 0.4706 0.6902 0.2196\n")
            continue
        if in_red_mat and ln.startswith("Ka "):
            new_lines.append("Ka 0.0941 0.1380 0.0439\n")
            continue
        new_lines.append(ln)
    with open(dst_mtl, "w") as f:
        f.writelines(new_lines)
    print(f"  ✓ stage_3.obj  (red faces -> unripe green {RSC_UNRIPE})")


# ----------------------------------------------------------------
# Stages 1 + 2 — scaled depletedtomato
# ----------------------------------------------------------------

def build_scaled_stage(num, scale):
    """Import depletedtomato.obj, scale, save as stage_{num}.obj."""
    clear_scene()
    import_obj(f"{REF_DIR}/depletedtomato.obj")
    obj = join_to(f"Tomato_Stage{num}_v3")
    # Apply scale around base (z=0) so plant sits on ground
    obj.scale = (scale, scale, scale)
    # Bake transform
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    export_obj(obj.name, f"{OUT_DIR}/stage_{num}.obj")
    # Also rewrite the obj's mtllib to point to its own .mtl name (Blender export does this already, but be safe)
    print(f"  ✓ stage_{num}.obj  (depletedtomato @ {scale*100:.0f}%, tris={len(obj.data.polygons)})")


# ----------------------------------------------------------------
# Render
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


def render_stage(num):
    clear_scene()
    import_obj(f"{OUT_DIR}/stage_{num}.obj")
    render_to(f"{RENDER_DIR}/v3_tomato_{num}.png")
    print(f"  ✓ render: v3_tomato_{num}.png")


def main():
    print(f"\n=== Tomato v3 — derived from vanilla geometry ===\n")
    print("[Stage 4 — vanilla copy]")
    build_stage_4()
    print("\n[Stage 3 — recolored red->unripe]")
    build_stage_3()
    print("\n[Stage 2 — depletedtomato 60%]")
    build_scaled_stage(2, 0.60)
    print("\n[Stage 1 — depletedtomato 25%]")
    build_scaled_stage(1, 0.25)

    print("\n=== Rendering ===")
    for n in (1, 2, 3, 4):
        render_stage(n)
    # Also re-render reference for the strip
    clear_scene()
    import_obj(f"{REF_DIR}/tomatoplant.obj")
    render_to(f"{RENDER_DIR}/v3_tomato_reference.png")
    print(f"  ✓ render: v3_tomato_reference.png")
    print(f"\n=== Tomato v3 complete ===")


if __name__ == "__main__":
    main()
