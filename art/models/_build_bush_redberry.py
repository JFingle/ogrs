"""
Redberry Bush — hand-authored unique silhouette.

Goal: distinctly different from the vanilla "round bush blob" — spreading
branching shape with woody stems, berry CLUSTERS (not embedded in foliage),
serrated angular leaves. Reads as a recognizable berry bush, not a green
sphere with red dots.

6 growth states:
  1_sapling      — single tiny stem + 2 leaves
  2_young        — 3-4 stems, more leaves, no berries
  3_mature_empty — full branching, full leaves, no berries
  4_mature_partial — full branching, 2-3 berry clusters left
  5_mature_full  — full branching, all 6 berry clusters
  6_dead         — bare branching frame, no leaves (player removed)

Palette (RSC-extracted):
  bark:        #6F5737  RGB(111, 87, 55)  brown
  leaf:        #507030  RGB(80, 112, 48)  olive
  leaf_light:  #78B038  RGB(120, 176, 56) brighter green accent
  berry:       #F80008  RGB(248, 0, 8)    pure red
"""
import bpy
import bmesh
import math
import os
import random

OUT_DIR = "/home/sparky/ogrs/art/models/farming/bushes/redberry"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)

PAL = {
    "bark":       (111/255,  87/255, 55/255, 1.0),
    "leaf":       ( 80/255, 112/255, 48/255, 1.0),
    "leaf_light": (120/255, 176/255, 56/255, 1.0),
    "berry":      (248/255,   0/255,  8/255, 1.0),
}


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


def setup_pal():
    return {k: make_mat(f"rsc_{k}", v) for k, v in PAL.items()}


def shade_flat_obj(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.faces_shade_flat()
    bpy.ops.object.mode_set(mode="OBJECT")


def join_to(name):
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not objs:
        return None
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
# Primitives — angular, RSC-feel
# ----------------------------------------------------------------

def add_branch(start, end, radius, material, verts=5):
    """Woody stem cylinder between two points."""
    sx, sy, sz = start; ex, ey, ez = end
    mx, my, mz = (sx+ex)/2, (sy+ey)/2, (sz+ez)/2
    dx, dy, dz = ex-sx, ey-sy, ez-sz
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    if length < 0.001: return None
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=radius, depth=length, location=(mx, my, mz)
    )
    branch = bpy.context.active_object
    # Orient cylinder to point from start->end
    branch.rotation_mode = "QUATERNION"
    from mathutils import Vector
    z = Vector((0, 0, 1))
    direction = Vector((dx, dy, dz)).normalized()
    branch.rotation_quaternion = z.rotation_difference(direction)
    branch.data.materials.append(material)
    return branch


def add_leaf(center, size, rotation, material):
    """Angular leaf — flattened diamond (low-poly, faceted)."""
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1, radius=size, location=center,
    )
    leaf = bpy.context.active_object
    # Elongate into leaf shape — long, narrow, flat
    leaf.scale = (1.4, 0.5, 0.18)
    leaf.rotation_euler = rotation
    leaf.data.materials.append(material)
    return leaf


def add_berry_cluster(center, count, radius, material, rng):
    """Tight cluster of small berries (3-5 spheres)."""
    for _ in range(count):
        ox = rng.uniform(-radius*1.6, radius*1.6)
        oy = rng.uniform(-radius*1.6, radius*1.6)
        oz = rng.uniform(-radius*0.4, radius*0.4)
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1, radius=radius, location=(center[0]+ox, center[1]+oy, center[2]+oz),
        )
        berry = bpy.context.active_object
        berry.data.materials.append(material)


# ----------------------------------------------------------------
# Composition — the bush itself
# ----------------------------------------------------------------

# Bush architecture: 6 main branching stems splaying outward from base, each
# topping out in a leaf+berry node. Branches are visible as woody stems
# unlike the vanilla "leaf blob".

BRANCH_ENDS = [
    # UPPER branches — canopy tips (8)
    ( 0.18,  0.10, 0.42),
    (-0.17,  0.13, 0.40),
    ( 0.15, -0.14, 0.36),
    (-0.19, -0.10, 0.38),
    ( 0.05,  0.20, 0.46),
    ( 0.07, -0.18, 0.44),
    ( 0.20, -0.02, 0.32),
    (-0.21,  0.02, 0.34),
    # LOWER branches — splay outward near the ground (6)
    ( 0.22,  0.12, 0.12),
    (-0.21,  0.15, 0.10),
    ( 0.17, -0.18, 0.08),
    (-0.20, -0.16, 0.11),
    ( 0.10,  0.22, 0.14),
    ( 0.08, -0.22, 0.13),
]
BASE_POINT = (0.0, 0.0, 0.04)
# Core foliage anchor points — fill the inside so no gaps top-to-bottom
CORE_LEAF_ANCHORS = [
    # Top half (Z 0.22..0.40)
    (0.00, 0.00, 0.22), (0.06, 0.05, 0.28), (-0.05, 0.06, 0.26),
    (0.06, -0.05, 0.30), (-0.06, -0.06, 0.24), (0.10, 0.00, 0.32),
    (-0.10, 0.00, 0.30), (0.00, 0.10, 0.34), (0.00, -0.09, 0.28),
    (0.04, 0.04, 0.36), (-0.04, -0.03, 0.38), (0.00, 0.00, 0.40),
    # Bottom half (Z 0.06..0.20) — fills the lower bush, sits just above soil
    (0.00, 0.00, 0.10), (0.08, 0.06, 0.12), (-0.07, 0.07, 0.13),
    (0.07, -0.08, 0.11), (-0.08, -0.07, 0.14), (0.12, 0.00, 0.10),
    (-0.12, 0.00, 0.12), (0.00, 0.12, 0.13), (0.00, -0.11, 0.10),
    (0.05, 0.05, 0.16), (-0.05, -0.04, 0.18), (0.10, 0.08, 0.08),
    (-0.10, -0.08, 0.09),
]


def build_branches(mats):
    """Add the 6 main woody branches splaying from base."""
    for end in BRANCH_ENDS:
        add_branch(BASE_POINT, end, radius=0.012, material=mats["bark"])
    # Central trunk stub
    add_branch((0, 0, 0.0), (0, 0, 0.06), radius=0.022, material=mats["bark"])


def build_leaves(mats, density=1.0, rng_seed=42):
    """Build a DENSE foliage canopy — leaves on branch tips + leaves filling the core."""
    rng = random.Random(rng_seed)
    # 1. Leaf clusters at branch tips (dense)
    for end in BRANCH_ENDS:
        leaf_count = int(14 * density)  # was 5 — almost 3x denser
        for i in range(leaf_count):
            theta = rng.uniform(0, math.pi * 2)
            r = rng.uniform(0.02, 0.09)
            ox = math.cos(theta) * r
            oy = math.sin(theta) * r
            oz = rng.uniform(-0.04, 0.07)
            mat = mats["leaf"] if i % 4 != 0 else mats["leaf_light"]
            add_leaf(
                (end[0]+ox, end[1]+oy, end[2]+oz),
                size=0.065,  # was 0.045 — ~50% bigger
                rotation=(rng.uniform(0, math.pi), rng.uniform(0, math.pi/2), rng.uniform(0, math.pi)),
                material=mat,
            )
    # 2. Core fill leaves — hide the branch skeleton from showing through
    core_count = int(len(CORE_LEAF_ANCHORS) * density)
    for i, anchor in enumerate(CORE_LEAF_ANCHORS[:core_count]):
        ox = rng.uniform(-0.04, 0.04)
        oy = rng.uniform(-0.04, 0.04)
        oz = rng.uniform(-0.02, 0.02)
        mat = mats["leaf"] if i % 3 != 0 else mats["leaf_light"]
        add_leaf(
            (anchor[0]+ox, anchor[1]+oy, anchor[2]+oz),
            size=0.075,  # core leaves are largest
            rotation=(rng.uniform(0, math.pi), rng.uniform(0, math.pi/2), rng.uniform(0, math.pi)),
            material=mat,
        )


def build_berries(mats, indices=None, rng_seed=99):
    """Add berry clusters at selected UPPER branch tips only — fruit grows on top."""
    UPPER_BRANCH_COUNT = 8  # first 8 in BRANCH_ENDS are the upper canopy
    if indices is None:
        indices = list(range(UPPER_BRANCH_COUNT))
    else:
        # Filter to upper branches only — berries don't grow at ground level
        indices = [i for i in indices if i < UPPER_BRANCH_COUNT]
    rng = random.Random(rng_seed)
    for i in indices:
        end = BRANCH_ENDS[i]
        cluster_center = (end[0]*0.7, end[1]*0.7, end[2] - 0.04)
        add_berry_cluster(cluster_center, count=4, radius=0.022, material=mats["berry"], rng=rng)


def build_soil(mats):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=10, radius=0.18, depth=0.02, location=(0, 0, 0.01),
    )
    obj = bpy.context.active_object
    # Use bark color tone for soil to keep palette tight, or could add soil mat
    soil_mat = make_mat("rsc_soil", (96/255, 64/255, 32/255, 1.0))
    obj.data.materials.append(soil_mat)


# ----------------------------------------------------------------
# Stage builders
# ----------------------------------------------------------------

def build_state(state_key, scale=1.0, leaves=True, berry_indices=None, dead=False):
    clear_scene()
    mats = setup_pal()
    build_soil(mats)
    build_branches(mats)
    if leaves and not dead:
        # Less density for early stages
        density = scale  # scale=0.3 → fewer leaves
        build_leaves(mats, density=density)
    if berry_indices:
        build_berries(mats, indices=berry_indices)
    obj = join_to(f"redberry_{state_key}")
    # Scale around z=0 base so plant remains rooted in soil
    obj.scale = (scale, scale, scale)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/{state_key}.obj")
    print(f"  ✓ {state_key}.obj  scale={scale}  tris={len(obj.data.polygons)}")


# ----------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------

def setup_camera(ortho_scale=0.7):
    bpy.ops.object.camera_add(
        location=(0.6, -0.6, 0.4),
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


def render_state(state_key, ortho_scale=0.7):
    clear_scene()
    bpy.ops.wm.obj_import(filepath=f"{OUT_DIR}/{state_key}.obj", forward_axis="NEGATIVE_Y", up_axis="Z")
    setup_camera(ortho_scale)
    scn = bpy.context.scene
    scn.render.resolution_x = 256
    scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = f"{RENDER_DIR}/bush_redberry_{state_key}.png"
    bpy.ops.render.render(write_still=True)


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------

def main():
    print(f"\n=== Redberry bush — 6 states (hand-authored) ===\n")
    # 1 — sapling: tiny, 1 branch's worth at 30% scale, no berries, few leaves
    build_state("1_sapling",        scale=0.30, leaves=True, berry_indices=[])
    # 2 — young: 60% scale, no berries, more leaves
    build_state("2_young",          scale=0.60, leaves=True, berry_indices=[])
    # 3 — mature, empty: 100% scale, full foliage, no berries
    build_state("3_mature_empty",   scale=1.00, leaves=True, berry_indices=[])
    # 4 — mature, partial: 100% scale, full foliage, 2 berry clusters left (of 6)
    build_state("4_mature_partial", scale=1.00, leaves=True, berry_indices=[0, 4])
    # 5 — mature, full: 100% scale, full foliage, all 8 UPPER berry clusters
    build_state("5_mature_full",    scale=1.00, leaves=True, berry_indices=[0, 1, 2, 3, 4, 5, 6, 7])
    # 6 — dead: full size but no leaves, no berries (just branches showing)
    build_state("6_dead",           scale=1.00, leaves=False, berry_indices=[], dead=True)

    print(f"\n=== Rendering ===")
    for s in ("1_sapling", "2_young", "3_mature_empty", "4_mature_partial", "5_mature_full", "6_dead"):
        render_state(s, ortho_scale=0.8)
    print(f"\n=== Redberry bush complete ===")


if __name__ == "__main__":
    main()
