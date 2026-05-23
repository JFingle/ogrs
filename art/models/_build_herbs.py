"""
13 distinct herb types — each 4 growth stages.

Geometry: vanilla `herb.ob3` (78 faces) — scaled per stage.
Color:    per-herb RSC-palette recolor of the single material slot.

States: 1_seedling (20%), 2_sprouting (40%), 3_growing (70%), 4_mature (100%)
"""
import bpy
import os
import math
import shutil

REF_DIR = "/home/sparky/ogrs/art/models/_rsc_reference"
OUT_BASE = "/home/sparky/ogrs/art/models/farming/herbs"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"

HERBS = [
    ("guam",       0x209830),
    ("marrentill", 0x308878),
    ("tarromin",   0x90A848),
    ("harralander",0xA89028),
    ("ranarr",     0x5098A0),
    ("toadflax",   0x9038A0),
    ("irit",       0x385878),
    ("avantoe",    0xA89868),
    ("kwuarm",     0xA0A0A8),
    ("cadantine",  0x5038A0),
    ("lantadyme",  0xA8B048),
    ("dwarfweed",  0x8898A0),
    ("torstol",    0xD8B028),
]

STAGES = [
    ("1_seedling",  0.20),
    ("2_sprouting", 0.40),
    ("3_growing",   0.70),
    ("4_mature",    1.00),
]


def hex_to_rgba(h):
    r = ((h >> 16) & 0xFF) / 255.0
    g = ((h >> 8) & 0xFF) / 255.0
    b = (h & 0xFF) / 255.0
    return (r, g, b, 1.0)


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


def recolor_all_materials(obj, rgba):
    """Set all of obj's materials to the given color (herb is single-color)."""
    for slot in obj.material_slots:
        mat = slot.material
        if mat is None: continue
        mat.diffuse_color = rgba
        if mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = rgba
                bsdf.inputs["Roughness"].default_value = 1.0
                bsdf.inputs["Specular IOR Level"].default_value = 0.0


def build_herb_stages(name, color_hex):
    out_dir = f"{OUT_BASE}/{name}"
    os.makedirs(out_dir, exist_ok=True)
    rgba = hex_to_rgba(color_hex)
    print(f"\n=== {name}  color=#{color_hex:06X} ===")
    for stage_key, scale in STAGES:
        clear_scene()
        import_obj(f"{REF_DIR}/herb.obj")
        obj = join_to(f"{name}_{stage_key}")
        # Apply scale around base
        obj.scale = (scale, scale, scale)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        # Recolor
        recolor_all_materials(obj, rgba)
        # Export — the OBJ exporter will write a new .mtl beside it with the new color
        export_obj(obj.name, f"{out_dir}/{stage_key}.obj")
        print(f"  ✓ {stage_key}.obj  scale={scale}  tris={len(obj.data.polygons)}")


# ----------------------------------------------------------------
# Render
# ----------------------------------------------------------------

def setup_camera(ortho_scale=1.5):
    bpy.ops.object.camera_add(location=(1.0, -1.0, 0.7),
                              rotation=(math.radians(65), 0, math.radians(45)))
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="SUN", location=(2, -2, 3))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


def render_herb_stage(name, stage_key, ortho_scale):
    out_dir = f"{OUT_BASE}/{name}"
    clear_scene()
    bpy.ops.wm.obj_import(filepath=f"{out_dir}/{stage_key}.obj",
                          forward_axis="NEGATIVE_Y", up_axis="Z")
    setup_camera(ortho_scale)
    scn = bpy.context.scene
    scn.render.resolution_x = 256
    scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = f"{RENDER_DIR}/herb_{name}_{stage_key}.png"
    bpy.ops.render.render(write_still=True)


# Different ortho per stage (smaller plants need tighter camera)
STAGE_ORTHO = {"1_seedling": 0.5, "2_sprouting": 0.9, "3_growing": 1.3, "4_mature": 1.7}


def main():
    print(f"\n=== {len(HERBS)} distinct herb types × {len(STAGES)} stages ===\n")
    for name, color in HERBS:
        build_herb_stages(name, color)
    print(f"\n=== Rendering ===\n")
    for name, _ in HERBS:
        for stage_key, _ in STAGES:
            render_herb_stage(name, stage_key, STAGE_ORTHO[stage_key])
    print(f"\n=== Herbs complete: {len(HERBS) * len(STAGES)} models ===")


if __name__ == "__main__":
    main()
