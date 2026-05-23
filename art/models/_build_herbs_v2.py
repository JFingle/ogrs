"""
Herbs v2 — hand-authored herb silhouette (replaces vanilla scaled model).

Geometry:
  • Central low base nub (cylinder)
  • Long narrow leaves splaying UPWARD and outward in a cup formation
  • Each leaf = flat elongated diamond shape (icosphere stretched)
  • Mature stage adds a small flower/seed cluster at the top

Growth progression isn't just scale — leaf COUNT increases per stage:
  1_seedling   — 3 small leaves, 25% height
  2_sprouting  — 6 leaves, 50% height
  3_growing    — 9 leaves, 75% height
  4_mature     — 12 leaves + flower cluster, 100% height

Per-herb color comes from the same 13-color palette as v1, applied to leaves.
Base nub is bark/soil-brown; flower cluster uses lighter herb color.
"""
import bpy
import math
import os
import random

OUT_BASE = "/home/sparky/ogrs/art/models/farming/herbs"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
os.makedirs(RENDER_DIR, exist_ok=True)

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

# Stages: (key, leaf_count, height_scale, has_flower)
STAGES = [
    ("1_seedling",  3,  0.30, False),
    ("2_sprouting", 6,  0.55, False),
    ("3_growing",   9,  0.80, False),
    ("4_mature",    12, 1.00, True),
]

BARK = (96/255, 64/255, 32/255, 1.0)


def hex_to_rgba(h):
    r = ((h >> 16) & 0xFF) / 255.0
    g = ((h >> 8) & 0xFF) / 255.0
    b = (h & 0xFF) / 255.0
    return (r, g, b, 1.0)


def lighter(rgba, amount=0.25):
    """Lighten an RGBA towards white by `amount`."""
    return (
        min(1.0, rgba[0] + amount),
        min(1.0, rgba[1] + amount),
        min(1.0, rgba[2] + amount),
        rgba[3],
    )


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in list(bpy.data.meshes): bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials): bpy.data.materials.remove(block)


def make_mat(name, rgba):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Roughness"].default_value = 1.0
        bsdf.inputs["Specular IOR Level"].default_value = 0.0
    mat.diffuse_color = rgba
    return mat


def shade_flat_obj(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.faces_shade_flat()
    bpy.ops.object.mode_set(mode="OBJECT")


def join_to(name):
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not objs: return None
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    final = bpy.context.active_object
    final.name = name
    return final


def export_obj(obj_name, out_path):
    bpy.ops.object.select_all(action="DESELECT")
    obj = bpy.data.objects[obj_name]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.obj_export(
        filepath=out_path, export_selected_objects=True, export_materials=True,
        forward_axis="NEGATIVE_Y", up_axis="Z",
    )


# ----------------------------------------------------------------
# Primitives
# ----------------------------------------------------------------

def add_base_nub(mat):
    """Small dark base where the leaves emerge."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=0.04, location=(0, 0, 0.02))
    obj = bpy.context.active_object
    obj.data.materials.append(mat)


def add_leaf(angle, tilt_out, height, length, width, mat):
    """
    One herb leaf — flat elongated diamond pointing upward and outward.
    `angle`: rotation around Z (radial position)
    `tilt_out`: how much the leaf splays outward (radians from vertical)
    `height`: base Z of leaf tip
    `length`, `width`: leaf size
    """
    # Position center of leaf at offset from base, splayed outward
    offset = math.sin(tilt_out) * length * 0.4
    ox = math.cos(angle) * offset
    oy = math.sin(angle) * offset
    oz = height * 0.5
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1, radius=length / 2,
        location=(ox, oy, oz),
    )
    leaf = bpy.context.active_object
    # Shape: long, narrow, flat — elongated along Z (will rotate)
    leaf.scale = (width / length, width / length * 0.25, 1.0)
    # Orient: rotate around the radial axis so leaf points up+out
    # First rotate so its long axis points up, then tilt outward by `tilt_out`,
    # then spin around Z by `angle`.
    leaf.rotation_euler = (tilt_out, 0, angle)
    leaf.data.materials.append(mat)
    return leaf


def add_flower_cluster(mat, count=5):
    """Small cluster of color dots at the top — flowers/seeds."""
    rng = random.Random(7)
    base_z = 0.42
    for _ in range(count):
        ox = rng.uniform(-0.04, 0.04)
        oy = rng.uniform(-0.04, 0.04)
        oz = base_z + rng.uniform(0.0, 0.05)
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1, radius=0.022, location=(ox, oy, oz),
        )
        bpy.context.active_object.data.materials.append(mat)


def build_herb_state(name, color_hex, stage_key, leaf_count, height_scale, has_flower):
    clear_scene()
    rgba = hex_to_rgba(color_hex)
    rgba_light = lighter(rgba, 0.20)
    mat_leaf = make_mat(f"leaf_{name}", rgba)
    mat_leaf_light = make_mat(f"leaf_light_{name}", rgba_light)
    mat_bark = make_mat("bark", BARK)
    mat_flower = make_mat(f"flower_{name}", lighter(rgba, 0.35))

    add_base_nub(mat_bark)

    # Leaves radiate around the base
    leaf_length = 0.18 * height_scale + 0.05
    leaf_width = 0.05
    for i in range(leaf_count):
        angle = (i / leaf_count) * 2 * math.pi
        # Tilt: small variation, mostly upright but splaying outward
        tilt = 0.55 + (i % 3) * 0.06  # 0.55..0.73 radians (~31-42deg from vertical)
        # Alternate leaf color hue for variety
        mat = mat_leaf if i % 3 != 0 else mat_leaf_light
        add_leaf(angle, tilt_out=tilt, height=leaf_length, length=leaf_length,
                 width=leaf_width, mat=mat)

    if has_flower:
        add_flower_cluster(mat_flower, count=5)

    out_dir = f"{OUT_BASE}/{name}"
    os.makedirs(out_dir, exist_ok=True)
    obj = join_to(f"{name}_{stage_key}")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{out_dir}/{stage_key}.obj")
    return len(obj.data.polygons)


# ----------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------

def setup_camera(ortho_scale):
    bpy.ops.object.camera_add(location=(0.5, -0.5, 0.4),
                              rotation=(math.radians(65), 0, math.radians(45)))
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="SUN", location=(2, -2, 3))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


# Per-stage ortho — smaller plants need tighter cam
STAGE_ORTHO = {"1_seedling": 0.45, "2_sprouting": 0.55, "3_growing": 0.7, "4_mature": 0.85}


def render_state(name, stage_key, ortho_scale):
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


def main():
    print(f"\n=== Herbs v2 — hand-authored silhouette, {len(HERBS)} types × {len(STAGES)} stages ===\n")
    for name, color in HERBS:
        print(f"\n=== {name}  #{color:06X} ===")
        for stage_key, leaf_count, h_scale, has_flower in STAGES:
            tris = build_herb_state(name, color, stage_key, leaf_count, h_scale, has_flower)
            print(f"  ✓ {stage_key}.obj  leaves={leaf_count} flower={has_flower}  tris={tris}")
    print(f"\n=== Rendering ===\n")
    for name, _ in HERBS:
        for stage_key, _, _, _ in STAGES:
            render_state(name, stage_key, STAGE_ORTHO[stage_key])
    print(f"\n=== Complete: {len(HERBS) * len(STAGES)} models ===")


if __name__ == "__main__":
    main()
