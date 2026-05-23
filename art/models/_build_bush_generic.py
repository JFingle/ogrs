"""
Generic berry bush builder — same proven geometry as redberry v3, parameterized
by leaf color + berry color per bush type.

Usage:
  blender --background --python _build_bush_generic.py -- <bush_name>

Geometry (shared across all bushes):
  • 8 upper branches splaying to canopy + 6 lower branches splaying near soil
  • Dense leaf fill top-to-bottom (~140 leaves at full)
  • Berry clusters on 8 upper branches only
  • 6 states: 1_sapling, 2_young, 3_mature_empty, 4_mature_partial, 5_mature_full, 6_dead
"""
import bpy
import math
import os
import random
import sys


# Per-bush palettes — all leaves are RSC-palette greens, distinct hues only
BUSHES = {
    "dwellberry": {
        "leaf_dark":  (64/255,  96/255, 48/255, 1.0),   # #406030
        "leaf_light": (96/255, 136/255, 32/255, 1.0),   # #608820
        "berry":      (64/255,  96/255, 136/255, 1.0),  # #406088 blue-grey
    },
    "janger": {
        "leaf_dark":  (80/255, 112/255, 48/255, 1.0),   # #507030
        "leaf_light": (128/255, 176/255, 72/255, 1.0),  # #80B048
        "berry":      (96/255, 152/255, 40/255, 1.0),   # #609828 green
    },
    "cadava": {
        "leaf_dark":  (56/255,  72/255, 24/255, 1.0),   # #384818 sinister dark
        "leaf_light": (80/255, 104/255, 56/255, 1.0),   # #506838
        "berry":      (160/255, 64/255, 160/255, 1.0),  # #A040A0 poison magenta
    },
    "whiteberry": {
        "leaf_dark":  (120/255, 136/255, 56/255, 1.0),  # #788838 mistletoe olive-tan
        "leaf_light": (144/255, 152/255, 72/255, 1.0),  # #909848
        "berry":      (232/255, 224/255, 208/255, 1.0), # #E8E0D0 cream/white
    },
}


# Branch architecture — same as redberry v3 (proven good)
BRANCH_ENDS = [
    # UPPER (canopy) — 8
    ( 0.18,  0.10, 0.42), (-0.17,  0.13, 0.40), ( 0.15, -0.14, 0.36),
    (-0.19, -0.10, 0.38), ( 0.05,  0.20, 0.46), ( 0.07, -0.18, 0.44),
    ( 0.20, -0.02, 0.32), (-0.21,  0.02, 0.34),
    # LOWER (ground-level fill) — 6
    ( 0.22,  0.12, 0.12), (-0.21,  0.15, 0.10), ( 0.17, -0.18, 0.08),
    (-0.20, -0.16, 0.11), ( 0.10,  0.22, 0.14), ( 0.08, -0.22, 0.13),
]
BASE_POINT = (0.0, 0.0, 0.04)
UPPER_BRANCH_COUNT = 8

CORE_LEAF_ANCHORS = [
    # Top half
    (0.00, 0.00, 0.22), (0.06, 0.05, 0.28), (-0.05, 0.06, 0.26),
    (0.06, -0.05, 0.30), (-0.06, -0.06, 0.24), (0.10, 0.00, 0.32),
    (-0.10, 0.00, 0.30), (0.00, 0.10, 0.34), (0.00, -0.09, 0.28),
    (0.04, 0.04, 0.36), (-0.04, -0.03, 0.38), (0.00, 0.00, 0.40),
    # Bottom half
    (0.00, 0.00, 0.10), (0.08, 0.06, 0.12), (-0.07, 0.07, 0.13),
    (0.07, -0.08, 0.11), (-0.08, -0.07, 0.14), (0.12, 0.00, 0.10),
    (-0.12, 0.00, 0.12), (0.00, 0.12, 0.13), (0.00, -0.11, 0.10),
    (0.05, 0.05, 0.16), (-0.05, -0.04, 0.18), (0.10, 0.08, 0.08),
    (-0.10, -0.08, 0.09),
]

BARK = (111/255, 87/255, 55/255, 1.0)
SOIL = (96/255, 64/255, 32/255, 1.0)


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


def setup_mats(pal):
    return {
        "bark":       make_mat("bark", BARK),
        "soil":       make_mat("soil", SOIL),
        "leaf":       make_mat("leaf_dark", pal["leaf_dark"]),
        "leaf_light": make_mat("leaf_light", pal["leaf_light"]),
        "berry":      make_mat("berry", pal["berry"]),
    }


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


def add_branch(start, end, radius, material, verts=5):
    sx, sy, sz = start; ex, ey, ez = end
    mx, my, mz = (sx+ex)/2, (sy+ey)/2, (sz+ez)/2
    dx, dy, dz = ex-sx, ey-sy, ez-sz
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    if length < 0.001: return None
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=length, location=(mx, my, mz))
    b = bpy.context.active_object
    b.rotation_mode = "QUATERNION"
    from mathutils import Vector
    z = Vector((0, 0, 1))
    direction = Vector((dx, dy, dz)).normalized()
    b.rotation_quaternion = z.rotation_difference(direction)
    b.data.materials.append(material)
    return b


def add_leaf(center, size, rotation, material):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=size, location=center)
    leaf = bpy.context.active_object
    leaf.scale = (1.4, 0.5, 0.18)
    leaf.rotation_euler = rotation
    leaf.data.materials.append(material)
    return leaf


def add_berry_cluster(center, count, radius, material, rng):
    for _ in range(count):
        ox = rng.uniform(-radius*1.6, radius*1.6)
        oy = rng.uniform(-radius*1.6, radius*1.6)
        oz = rng.uniform(-radius*0.4, radius*0.4)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius,
                                              location=(center[0]+ox, center[1]+oy, center[2]+oz))
        bpy.context.active_object.data.materials.append(material)


def build_soil(mats):
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.18, depth=0.02, location=(0, 0, 0.01))
    bpy.context.active_object.data.materials.append(mats["soil"])


def build_branches(mats):
    for end in BRANCH_ENDS:
        add_branch(BASE_POINT, end, radius=0.012, material=mats["bark"])
    add_branch((0, 0, 0.0), (0, 0, 0.06), radius=0.022, material=mats["bark"])


def build_leaves(mats, density=1.0, rng_seed=42):
    rng = random.Random(rng_seed)
    for end in BRANCH_ENDS:
        leaf_count = int(14 * density)
        for i in range(leaf_count):
            theta = rng.uniform(0, math.pi * 2); r = rng.uniform(0.02, 0.09)
            ox = math.cos(theta) * r; oy = math.sin(theta) * r; oz = rng.uniform(-0.04, 0.07)
            mat = mats["leaf"] if i % 4 != 0 else mats["leaf_light"]
            add_leaf((end[0]+ox, end[1]+oy, end[2]+oz), size=0.065,
                     rotation=(rng.uniform(0, math.pi), rng.uniform(0, math.pi/2), rng.uniform(0, math.pi)),
                     material=mat)
    core_count = int(len(CORE_LEAF_ANCHORS) * density)
    for i, anchor in enumerate(CORE_LEAF_ANCHORS[:core_count]):
        ox = rng.uniform(-0.04, 0.04); oy = rng.uniform(-0.04, 0.04); oz = rng.uniform(-0.02, 0.02)
        mat = mats["leaf"] if i % 3 != 0 else mats["leaf_light"]
        add_leaf((anchor[0]+ox, anchor[1]+oy, anchor[2]+oz), size=0.075,
                 rotation=(rng.uniform(0, math.pi), rng.uniform(0, math.pi/2), rng.uniform(0, math.pi)),
                 material=mat)


def build_berries(mats, indices=None, rng_seed=99):
    if indices is None:
        indices = list(range(UPPER_BRANCH_COUNT))
    else:
        indices = [i for i in indices if i < UPPER_BRANCH_COUNT]
    rng = random.Random(rng_seed)
    for i in indices:
        end = BRANCH_ENDS[i]
        cluster_center = (end[0]*0.7, end[1]*0.7, end[2] - 0.04)
        add_berry_cluster(cluster_center, count=4, radius=0.022, material=mats["berry"], rng=rng)


def build_state(out_dir, state_key, pal, scale=1.0, leaves=True, berry_indices=None, dead=False):
    clear_scene()
    mats = setup_mats(pal)
    build_soil(mats)
    build_branches(mats)
    if leaves and not dead:
        build_leaves(mats, density=scale)
    if berry_indices:
        build_berries(mats, indices=berry_indices)
    obj = join_to(f"{state_key}")
    obj.scale = (scale, scale, scale)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    shade_flat_obj(obj)
    export_obj(obj.name, f"{out_dir}/{state_key}.obj")
    print(f"  ✓ {state_key}.obj  scale={scale}  tris={len(obj.data.polygons)}")


def setup_camera(ortho_scale=0.8):
    bpy.ops.object.camera_add(location=(0.6, -0.6, 0.4),
                              rotation=(math.radians(65), 0, math.radians(45)))
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho_scale
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="SUN", location=(1.5, -1.5, 2))
    light = bpy.context.active_object
    light.data.energy = 3.0
    light.rotation_euler = (math.radians(50), 0, math.radians(30))


def render_state(out_dir, bush_name, state_key, ortho_scale=0.8):
    render_dir = "/home/sparky/ogrs/art/models/_renders"
    clear_scene()
    bpy.ops.wm.obj_import(filepath=f"{out_dir}/{state_key}.obj",
                          forward_axis="NEGATIVE_Y", up_axis="Z")
    setup_camera(ortho_scale)
    scn = bpy.context.scene
    scn.render.resolution_x = 256; scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = f"{render_dir}/bush_{bush_name}_{state_key}.png"
    bpy.ops.render.render(write_still=True)


def main():
    # Args after --
    argv = sys.argv
    if "--" in argv:
        idx = argv.index("--")
        argv = argv[idx+1:]
    else:
        argv = []
    bush_name = argv[0] if argv else None
    if not bush_name or bush_name not in BUSHES:
        print(f"Usage: blender --background --python {__file__} -- <bush_name>")
        print(f"Available: {list(BUSHES.keys())}")
        return

    pal = BUSHES[bush_name]
    out_dir = f"/home/sparky/ogrs/art/models/farming/bushes/{bush_name}"
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n=== Building bush: {bush_name} ===\n")
    build_state(out_dir, "1_sapling",        pal, scale=0.30, leaves=True, berry_indices=[])
    build_state(out_dir, "2_young",          pal, scale=0.60, leaves=True, berry_indices=[])
    build_state(out_dir, "3_mature_empty",   pal, scale=1.00, leaves=True, berry_indices=[])
    build_state(out_dir, "4_mature_partial", pal, scale=1.00, leaves=True, berry_indices=[0, 4])
    build_state(out_dir, "5_mature_full",    pal, scale=1.00, leaves=True, berry_indices=[0,1,2,3,4,5,6,7])
    build_state(out_dir, "6_dead",           pal, scale=1.00, leaves=False, berry_indices=[], dead=True)

    print(f"\n=== Rendering {bush_name} ===\n")
    for s in ("1_sapling","2_young","3_mature_empty","4_mature_partial","5_mature_full","6_dead"):
        render_state(out_dir, bush_name, s, ortho_scale=0.8)
    print(f"\n=== Done: {bush_name} ===")


if __name__ == "__main__":
    main()
