"""
Hops — 5 varieties × 4 growth stages. Hand-authored geometry.

Architecture (replaces "scaled blob" with a recognizable hops silhouette):
  • Vertical wooden pole/stake — central support (~0.65m tall)
  • Leaf clusters at 4 height levels spiraling up the pole
  • Hop cones (small downward-pointing cones) clustered at upper levels
  • Leaves are palm-shaped (5 small ellipsoids in a fan)
  • Cones are tiny cylinder-cones, drooping down from branch tips

Growth stages:
  1_sapling — just pole + 1 bottom leaf level, no cones
  2_growing — pole + 3 leaf levels, no cones
  3_partial — pole + all 4 leaf levels + 1 of 3 cone clusters left (mid-harvest)
  4_mature  — full plant + all 3 cone clusters

5 hop varieties (cone color is the only difference):
  hammerstone (red), asgarnian (gold), yanillian (green),
  krandorian (purple), wildblood (dark red)
"""
import bpy
import math
import os
import random

OUT_BASE = "/home/sparky/ogrs/art/models/farming/hops"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
os.makedirs(RENDER_DIR, exist_ok=True)

HOPS = [
    ("hammerstone", 0xB04020),  # red copper
    ("asgarnian",   0xD0A028),  # gold amber
    ("yanillian",   0x60A028),  # bright green
    ("krandorian",  0x603098),  # deep purple
    ("wildblood",   0x803030),  # dark red wine
]

BARK = (96/255, 64/255, 32/255, 1.0)
SOIL = (80/255, 56/255, 28/255, 1.0)
LEAF_DARK = (64/255, 96/255, 40/255, 1.0)    # #406028
LEAF_LIGHT = (96/255, 136/255, 56/255, 1.0)  # #608838


def hex_to_rgba(h):
    return (((h >> 16) & 0xFF) / 255, ((h >> 8) & 0xFF) / 255, (h & 0xFF) / 255, 1.0)


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

def add_pole(mat, height=0.65, radius=0.018):
    """Central vertical wooden stake."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=radius, depth=height,
                                        location=(0, 0, height / 2 + 0.02))
    obj = bpy.context.active_object
    obj.data.materials.append(mat)


def add_soil(mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.15, depth=0.02, location=(0, 0, 0.01))
    bpy.context.active_object.data.materials.append(mat)


def add_palm_leaf(center, angle_around_pole, level_radius, mat_dark, mat_light):
    """
    Palm-shaped leaf cluster: 5 elongated ellipsoids fanning out from a node.
    Position is around the pole at radius `level_radius`, angle `angle_around_pole`.
    """
    # Node position
    node_x = math.cos(angle_around_pole) * level_radius
    node_y = math.sin(angle_around_pole) * level_radius
    node_z = center[2]
    # 5 finger-leaves splaying outward from the node
    for finger in range(5):
        # Finger fans outward by `finger_angle` from the outward direction
        finger_angle = (finger - 2) * (math.pi / 12)  # -30..+30 deg
        # Outward direction
        out_x = math.cos(angle_around_pole + finger_angle) * 0.06
        out_y = math.sin(angle_around_pole + finger_angle) * 0.06
        # Leaf center offset outward
        lx = node_x + out_x
        ly = node_y + out_y
        lz = node_z + 0.005  # slight upward tilt
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1, radius=0.035, location=(lx, ly, lz),
        )
        leaf = bpy.context.active_object
        # Elongate radially outward
        leaf.scale = (2.0, 0.6, 0.18)
        leaf.rotation_euler = (0, 0, angle_around_pole + finger_angle)
        mat = mat_dark if finger % 2 == 0 else mat_light
        leaf.data.materials.append(mat)


def add_hop_cone(location, mat):
    """One hop cone — cylinder narrowed at bottom (pinecone shape), hanging down."""
    # Use cone primitive
    bpy.ops.mesh.primitive_cone_add(
        vertices=6, radius1=0.018, radius2=0.005, depth=0.04, location=location,
    )
    cone = bpy.context.active_object
    # Rotate so the wide end is at top, narrow at bottom (default cone has wide bottom)
    cone.rotation_euler = (math.pi, 0, 0)
    cone.data.materials.append(mat)


def add_hop_cluster(angle_around_pole, level_radius, level_z, mat, count=4, seed=0):
    """Cluster of `count` hop cones hanging together near a branch tip."""
    rng = random.Random(seed)
    base_x = math.cos(angle_around_pole) * (level_radius + 0.04)
    base_y = math.sin(angle_around_pole) * (level_radius + 0.04)
    for i in range(count):
        ox = rng.uniform(-0.015, 0.015)
        oy = rng.uniform(-0.015, 0.015)
        oz = -0.04 - rng.uniform(0, 0.025)
        add_hop_cone((base_x + ox, base_y + oy, level_z + oz), mat)


# ----------------------------------------------------------------
# Composition
# ----------------------------------------------------------------

# 4 spiral levels going up the pole — angle rotates each level
LEAF_LEVELS = [
    # (z, angle_offset, level_radius)
    (0.14, 0.0,           0.05),
    (0.28, math.pi * 0.6, 0.07),
    (0.42, math.pi * 1.2, 0.08),
    (0.56, math.pi * 1.8, 0.07),
]
# Cone clusters live at upper 3 levels
CONE_LEVELS = [1, 2, 3]  # indices into LEAF_LEVELS


def build_state(name, cone_rgba, stage_key,
                leaf_level_count, cone_cluster_indices):
    clear_scene()
    mat_pole = make_mat("pole", BARK)
    mat_soil = make_mat("soil", SOIL)
    mat_leaf_dark = make_mat("leaf_dark", LEAF_DARK)
    mat_leaf_light = make_mat("leaf_light", LEAF_LIGHT)
    mat_cone = make_mat(f"cone_{name}", cone_rgba)

    add_soil(mat_soil)
    # Pole height matches the highest active leaf level + a bit
    if leaf_level_count > 0:
        top_z = LEAF_LEVELS[min(leaf_level_count, len(LEAF_LEVELS)) - 1][0] + 0.08
    else:
        top_z = 0.20
    add_pole(mat_pole, height=top_z, radius=0.018)

    # Leaves at each active level — 2 fan clusters per level (opposite sides) for density
    for i in range(min(leaf_level_count, len(LEAF_LEVELS))):
        z, base_ang, rad = LEAF_LEVELS[i]
        add_palm_leaf((0, 0, z), base_ang, rad, mat_leaf_dark, mat_leaf_light)
        add_palm_leaf((0, 0, z), base_ang + math.pi, rad, mat_leaf_dark, mat_leaf_light)

    # Hop cone clusters at requested levels
    for cluster_idx in cone_cluster_indices:
        if cluster_idx >= leaf_level_count: continue
        z, base_ang, rad = LEAF_LEVELS[cluster_idx]
        add_hop_cluster(base_ang + math.pi/3, rad, z, mat_cone, count=4, seed=cluster_idx)
        add_hop_cluster(base_ang - math.pi/3, rad, z, mat_cone, count=4, seed=cluster_idx + 100)

    out_dir = f"{OUT_BASE}/{name}"
    os.makedirs(out_dir, exist_ok=True)
    obj = join_to(f"{name}_{stage_key}")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{out_dir}/{stage_key}.obj")
    return len(obj.data.polygons)


# ----------------------------------------------------------------
# Per-stage configuration
# ----------------------------------------------------------------

# (stage_key, leaf_level_count, cone_cluster_indices)
STAGES = [
    ("1_sapling",  1, []),
    ("2_growing",  3, []),
    ("3_partial",  4, [1]),                # mid-harvest: 1 of 3 cone clusters left
    ("4_mature",   4, [1, 2, 3]),
]


# ----------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------

def setup_camera(ortho_scale):
    bpy.ops.object.camera_add(location=(0.7, -0.7, 0.5),
                              rotation=(math.radians(65), 0, math.radians(45)))
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="SUN", location=(2, -2, 3))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


STAGE_ORTHO = {"1_sapling": 0.55, "2_growing": 0.75, "3_partial": 0.95, "4_mature": 0.95}


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
    scn.render.filepath = f"{RENDER_DIR}/hops_{name}_{stage_key}.png"
    bpy.ops.render.render(write_still=True)


def main():
    print(f"\n=== Hops — {len(HOPS)} varieties × {len(STAGES)} stages ===\n")
    for name, color in HOPS:
        rgba = hex_to_rgba(color)
        print(f"\n=== {name}  #{color:06X} ===")
        for stage_key, leaf_levels, cone_clusters in STAGES:
            tris = build_state(name, rgba, stage_key, leaf_levels, cone_clusters)
            print(f"  ✓ {stage_key}.obj  leaves={leaf_levels} cones={cone_clusters}  tris={tris}")
    print(f"\n=== Rendering ===\n")
    for name, _ in HOPS:
        for stage_key, _, _ in STAGES:
            render_state(name, stage_key, STAGE_ORTHO[stage_key])
    print(f"\n=== Complete: {len(HOPS) * len(STAGES)} models ===")


if __name__ == "__main__":
    main()
