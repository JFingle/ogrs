"""
Common flowers — 7 species × 4 growth stages.

Each species has hand-authored mature geometry (researched from real-world
appearance). Earlier stages derived by removing parts (working backwards).

Daisy       — 15cm, ring of white petals + yellow disc, low growing
Lavender    — 60cm, purple flower-spike at top of tall thin stem
Marigold    — 30cm, multi-layer orange pompom blooms, bushy
Poppy       — 40cm, 4 red cup-petals + black center, thin hairy stem
Rose        — 50cm, tight spiral-petal red bloom, thorny branching stem
Sunflower   — 150cm, single huge bloom with ray petals + disc center
Tulip       — 35cm, cup-shaped 6-petal bloom on smooth tall stem

Stages (work backwards from mature):
  1_seedling — leaf nub at base only
  2_growing  — stem + leaves, no bloom
  3_budding  — stem + leaves + small closed bud at tip
  4_mature   — full bloom
"""
import bpy
import math
import os
import random

OUT_BASE = "/home/sparky/ogrs/art/models/farming/flowers"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
os.makedirs(RENDER_DIR, exist_ok=True)

# Palette
BARK = (96/255, 64/255, 32/255, 1.0)
SOIL = (80/255, 56/255, 28/255, 1.0)
STEM_GREEN = (64/255, 96/255, 40/255, 1.0)
LEAF_DARK = (64/255, 96/255, 40/255, 1.0)
LEAF_LIGHT = (96/255, 136/255, 56/255, 1.0)


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
# Shared primitives
# ----------------------------------------------------------------

def add_soil(mat, radius=0.10):
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=radius, depth=0.02, location=(0, 0, 0.01))
    bpy.context.active_object.data.materials.append(mat)


def add_stem(mat, height, radius=0.008, base_z=0.02):
    """Vertical stem cylinder."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=5, radius=radius, depth=height,
                                        location=(0, 0, base_z + height/2))
    bpy.context.active_object.data.materials.append(mat)


def add_basal_leaf(mat, angle, length=0.10, width=0.025, tilt=0.6, z=0.04):
    """Long narrow leaf splaying outward from base."""
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=length/2,
                                          location=(math.cos(angle)*length*0.45,
                                                    math.sin(angle)*length*0.45, z))
    leaf = bpy.context.active_object
    leaf.scale = (1.6, width/length, 0.15)
    leaf.rotation_euler = (tilt, 0, angle)
    leaf.data.materials.append(mat)


def add_petal(mat, center, angle_around, tilt_up, petal_length=0.04, petal_width=0.025, flat=True):
    """One flat oval-shaped petal radiating from center."""
    cx, cy, cz = center
    # Petal center is offset outward from flower center
    offset = petal_length * 0.4
    ox = cx + math.cos(angle_around) * offset
    oy = cy + math.sin(angle_around) * offset
    oz = cz + math.sin(tilt_up) * offset * 0.5
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=petal_length/2, location=(ox, oy, oz))
    petal = bpy.context.active_object
    petal.scale = (1.5, petal_width/petal_length, 0.10 if flat else 0.20)
    petal.rotation_euler = (tilt_up, 0, angle_around)
    petal.data.materials.append(mat)


def add_disc_center(mat, center, radius=0.022):
    """Flat disc for flower center (sunflower, daisy)."""
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=center)
    disc = bpy.context.active_object
    disc.scale = (1, 1, 0.3)
    disc.data.materials.append(mat)


def add_bud(mat, center, radius=0.018, tall=False):
    """Closed flower bud — small ellipsoid pointed upward."""
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=center)
    bud = bpy.context.active_object
    bud.scale = (0.7, 0.7, 1.4 if tall else 1.0)
    bud.data.materials.append(mat)


# ----------------------------------------------------------------
# Per-flower MATURE builders
# ----------------------------------------------------------------

def build_daisy_mature(mats):
    stem_h = 0.13
    add_stem(mats["stem"], stem_h)
    # 2 oval basal leaves
    for ang in (0, math.pi):
        add_basal_leaf(mats["leaf"], ang, length=0.08, width=0.025, tilt=0.7, z=0.04)
    bloom_z = stem_h + 0.03
    # Yellow disc
    add_disc_center(mats["bloom_center"], (0, 0, bloom_z), radius=0.020)
    # 10 white petals
    for i in range(10):
        ang = (i / 10) * 2 * math.pi
        add_petal(mats["bloom_petal"], (0, 0, bloom_z), ang, tilt_up=0.0,
                  petal_length=0.045, petal_width=0.020, flat=True)


def build_lavender_mature(mats):
    stem_h = 0.50
    add_stem(mats["stem"], stem_h, radius=0.005)
    # Narrow grey-green leaves at base
    for i in range(4):
        ang = (i / 4) * 2 * math.pi
        add_basal_leaf(mats["leaf"], ang, length=0.10, width=0.012, tilt=0.5, z=0.04)
    # Purple flower spike — cluster of small cones stacked from 0.40 to 0.55
    for z in [0.40, 0.43, 0.46, 0.49, 0.52]:
        for ang_off in (0, math.pi):
            bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions=1, radius=0.015,
                location=(math.cos(ang_off)*0.012, math.sin(ang_off)*0.012, z),
            )
            bud = bpy.context.active_object
            bud.scale = (0.8, 0.8, 1.2)
            bud.data.materials.append(mats["bloom_petal"])


def build_marigold_mature(mats):
    stem_h = 0.25
    add_stem(mats["stem"], stem_h, radius=0.008)
    # Fern-like base leaves — multiple small leaves
    for i in range(6):
        ang = (i / 6) * 2 * math.pi
        add_basal_leaf(mats["leaf"], ang, length=0.08, width=0.02, tilt=0.6, z=0.04)
    # 3 round orange pompom blooms at top
    bloom_positions = [(0, 0, 0.27), (0.04, 0.03, 0.22), (-0.04, -0.02, 0.24)]
    for bx, by, bz in bloom_positions:
        # Outer petal ring (10 petals)
        for i in range(10):
            ang = (i / 10) * 2 * math.pi
            add_petal(mats["bloom_petal"], (bx, by, bz), ang, tilt_up=0.2,
                      petal_length=0.035, petal_width=0.020, flat=False)
        # Inner petal ring (6 petals, smaller)
        for i in range(6):
            ang = (i / 6) * 2 * math.pi + math.pi/6
            add_petal(mats["bloom_center"], (bx, by, bz), ang, tilt_up=0.4,
                      petal_length=0.022, petal_width=0.015, flat=False)


def build_poppy_mature(mats):
    stem_h = 0.35
    add_stem(mats["stem"], stem_h, radius=0.006)
    # Lobed basal leaves
    for ang in (0, math.pi/2, math.pi, 3*math.pi/2):
        add_basal_leaf(mats["leaf"], ang, length=0.10, width=0.040, tilt=0.7, z=0.04)
    bloom_z = stem_h + 0.04
    # 4 large red petals in cup shape
    for i in range(4):
        ang = (i / 4) * 2 * math.pi
        add_petal(mats["bloom_petal"], (0, 0, bloom_z), ang, tilt_up=0.5,
                  petal_length=0.060, petal_width=0.050, flat=False)
    # Black center cluster (small dark spheres)
    for _ in range(3):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.012, location=(0, 0, bloom_z + 0.005))
        bpy.context.active_object.data.materials.append(mats["bloom_center"])


def build_rose_mature(mats):
    # Branching stem with thorns — simplified as 1 main + 2 side stems
    add_stem(mats["stem"], 0.40, radius=0.010)
    # Side stems
    for ang, h in ((math.pi/4, 0.30), (-math.pi/4 + math.pi, 0.32)):
        ox = math.cos(ang) * 0.08
        oy = math.sin(ang) * 0.08
        bpy.ops.mesh.primitive_cylinder_add(vertices=5, radius=0.008, depth=h,
                                            location=(ox, oy, h/2 + 0.02))
        s = bpy.context.active_object
        s.rotation_euler = (0.3, 0, ang)
        s.data.materials.append(mats["stem"])
    # Compound leaves at base + mid
    for ang in (0, math.pi/2, math.pi, 3*math.pi/2):
        add_basal_leaf(mats["leaf"], ang, length=0.08, width=0.035, tilt=0.6, z=0.06)
    for ang in (math.pi/4, 5*math.pi/4):
        add_basal_leaf(mats["leaf"], ang, length=0.06, width=0.025, tilt=0.4, z=0.20)
    # 3 rose blooms at branch tips
    bloom_positions = [(0, 0, 0.44), (0.08, 0.05, 0.34), (-0.07, -0.04, 0.36)]
    for bx, by, bz in bloom_positions:
        # Tightly packed petals — 5 outer + 5 middle + 3 inner
        for ring, count, length_scale, tilt in [(0, 5, 1.0, 0.3),
                                                  (1, 5, 0.7, 0.5),
                                                  (2, 3, 0.4, 0.7)]:
            for i in range(count):
                ang = (i / count) * 2 * math.pi + ring * math.pi/(count*2)
                add_petal(mats["bloom_petal"], (bx, by, bz), ang, tilt_up=tilt,
                          petal_length=0.035 * length_scale, petal_width=0.030 * length_scale,
                          flat=False)


def build_sunflower_mature(mats):
    stem_h = 1.40
    add_stem(mats["stem"], stem_h, radius=0.014)
    # Large heart-shaped leaves at 2 levels on stem
    for h in (0.25, 0.65, 1.0):
        for ang in (0, math.pi):
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.07,
                                                  location=(math.cos(ang)*0.06, math.sin(ang)*0.06, h))
            leaf = bpy.context.active_object
            leaf.scale = (1.4, 0.9, 0.12)
            leaf.rotation_euler = (0.4, 0, ang)
            leaf.data.materials.append(mats["leaf"])
    bloom_z = stem_h + 0.08
    # Brown disc center (large)
    add_disc_center(mats["bloom_center"], (0, 0, bloom_z), radius=0.060)
    # 14 yellow ray petals (long pointed)
    for i in range(14):
        ang = (i / 14) * 2 * math.pi
        add_petal(mats["bloom_petal"], (0, 0, bloom_z), ang, tilt_up=0.0,
                  petal_length=0.080, petal_width=0.030, flat=True)


def build_tulip_mature(mats):
    stem_h = 0.30
    add_stem(mats["stem"], stem_h, radius=0.007)
    # 3 long narrow basal leaves
    for i in range(3):
        ang = (i / 3) * 2 * math.pi
        add_basal_leaf(mats["leaf"], ang, length=0.18, width=0.035, tilt=0.4, z=0.06)
    bloom_z = stem_h + 0.04
    # Cup-shaped 6 petals (more upright, less spread)
    for i in range(6):
        ang = (i / 6) * 2 * math.pi
        add_petal(mats["bloom_petal"], (0, 0, bloom_z), ang, tilt_up=0.9,
                  petal_length=0.050, petal_width=0.030, flat=False)
    # Slight top closure
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.014,
                                          location=(0, 0, bloom_z + 0.03))
    cap = bpy.context.active_object
    cap.scale = (0.5, 0.5, 0.8)
    cap.data.materials.append(mats["bloom_petal"])


# ----------------------------------------------------------------
# Per-flower BUDDING stage builders (stage 3)
# ----------------------------------------------------------------

def build_budding(mats, flower_name, stem_h, leaf_count=2, leaf_length=0.10, leaf_z=0.04, bud_color="bloom_petal"):
    """Generic budding: stem + leaves + tight bud at top."""
    add_stem(mats["stem"], stem_h)
    for i in range(leaf_count):
        ang = (i / leaf_count) * 2 * math.pi
        add_basal_leaf(mats["leaf"], ang, length=leaf_length, width=leaf_length*0.25, tilt=0.6, z=leaf_z)
    # Bud at stem tip
    add_bud(mats[bud_color], (0, 0, stem_h + 0.025), radius=0.015,
            tall=flower_name in ("tulip", "lavender", "poppy"))


# Per-flower configs for stages 1-3 (work backwards from mature)
FLOWERS = {
    "daisy": {
        "stem_h":     0.13,
        "leaf_count": 2,
        "leaf_len":   0.08,
        "ortho":      0.4,
        "palette": {
            "stem":          STEM_GREEN,
            "leaf":          LEAF_DARK,
            "bloom_petal":   (240/255, 240/255, 248/255, 1.0),  # white
            "bloom_center":  (240/255, 200/255, 48/255, 1.0),   # yellow disc
        },
        "build_mature": build_daisy_mature,
    },
    "lavender": {
        "stem_h":     0.50,
        "leaf_count": 4,
        "leaf_len":   0.10,
        "ortho":      0.7,
        "palette": {
            "stem":          (104/255, 112/255, 80/255, 1.0),  # grey-green stem
            "leaf":          (104/255, 112/255, 80/255, 1.0),
            "bloom_petal":   (144/255, 96/255, 200/255, 1.0),  # lavender purple
            "bloom_center":  (144/255, 96/255, 200/255, 1.0),
        },
        "build_mature": build_lavender_mature,
    },
    "marigold": {
        "stem_h":     0.25,
        "leaf_count": 6,
        "leaf_len":   0.08,
        "ortho":      0.55,
        "palette": {
            "stem":          STEM_GREEN,
            "leaf":          LEAF_DARK,
            "bloom_petal":   (240/255, 144/255, 32/255, 1.0),  # orange
            "bloom_center":  (208/255, 96/255, 16/255, 1.0),   # darker orange center
        },
        "build_mature": build_marigold_mature,
    },
    "poppy": {
        "stem_h":     0.35,
        "leaf_count": 4,
        "leaf_len":   0.10,
        "ortho":      0.55,
        "palette": {
            "stem":          STEM_GREEN,
            "leaf":          LEAF_DARK,
            "bloom_petal":   (224/255, 32/255, 32/255, 1.0),   # bright red
            "bloom_center":  (24/255, 16/255, 16/255, 1.0),    # near-black
        },
        "build_mature": build_poppy_mature,
    },
    "rose": {
        "stem_h":     0.40,
        "leaf_count": 4,
        "leaf_len":   0.08,
        "ortho":      0.6,
        "palette": {
            "stem":          (96/255, 64/255, 48/255, 1.0),   # brown thorny stem
            "leaf":          LEAF_DARK,
            "bloom_petal":   (200/255, 48/255, 64/255, 1.0),  # rose red
            "bloom_center":  (160/255, 32/255, 48/255, 1.0),
        },
        "build_mature": build_rose_mature,
    },
    "sunflower": {
        "stem_h":     1.40,
        "leaf_count": 2,
        "leaf_len":   0.14,
        "ortho":      1.8,
        "palette": {
            "stem":          STEM_GREEN,
            "leaf":          LEAF_DARK,
            "bloom_petal":   (248/255, 208/255, 48/255, 1.0),  # bright yellow
            "bloom_center":  (96/255, 56/255, 24/255, 1.0),    # brown disc
        },
        "build_mature": build_sunflower_mature,
    },
    "tulip": {
        "stem_h":     0.30,
        "leaf_count": 3,
        "leaf_len":   0.18,
        "ortho":      0.55,
        "palette": {
            "stem":          STEM_GREEN,
            "leaf":          LEAF_DARK,
            "bloom_petal":   (224/255, 48/255, 96/255, 1.0),   # pink-red tulip
            "bloom_center":  (180/255, 32/255, 80/255, 1.0),
        },
        "build_mature": build_tulip_mature,
    },
}


def make_mats(palette):
    return {
        "stem":          make_mat("stem", palette["stem"]),
        "leaf":          make_mat("leaf", palette["leaf"]),
        "bloom_petal":   make_mat("petal", palette["bloom_petal"]),
        "bloom_center":  make_mat("center", palette["bloom_center"]),
        "soil":          make_mat("soil", SOIL),
    }


def build_state(flower_name, stage_key):
    cfg = FLOWERS[flower_name]
    clear_scene()
    mats = make_mats(cfg["palette"])
    add_soil(mats["soil"], radius=0.10)

    if stage_key == "1_seedling":
        # Just one small leaf nub at base
        add_basal_leaf(mats["leaf"], 0.0, length=cfg["leaf_len"]*0.4,
                       width=cfg["leaf_len"]*0.15, tilt=0.5, z=0.03)
        add_basal_leaf(mats["leaf"], math.pi, length=cfg["leaf_len"]*0.4,
                       width=cfg["leaf_len"]*0.15, tilt=0.5, z=0.03)
    elif stage_key == "2_growing":
        # Stem + leaves, no bloom. Use ~70% of mature stem height
        add_stem(mats["stem"], cfg["stem_h"] * 0.7)
        for i in range(cfg["leaf_count"]):
            ang = (i / cfg["leaf_count"]) * 2 * math.pi
            add_basal_leaf(mats["leaf"], ang, length=cfg["leaf_len"]*0.8,
                           width=cfg["leaf_len"]*0.25, tilt=0.6, z=0.04)
    elif stage_key == "3_budding":
        # Stem + leaves + tight bud
        build_budding(mats, flower_name, cfg["stem_h"] * 0.9, cfg["leaf_count"], cfg["leaf_len"])
    elif stage_key == "4_mature":
        cfg["build_mature"](mats)

    out_dir = f"{OUT_BASE}/{flower_name}"
    os.makedirs(out_dir, exist_ok=True)
    obj = join_to(f"{flower_name}_{stage_key}")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{out_dir}/{stage_key}.obj")
    return len(obj.data.polygons)


# ----------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------

STAGE_NAMES = ["1_seedling", "2_growing", "3_budding", "4_mature"]


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


def render_state(flower_name, stage_key, ortho_scale):
    out_dir = f"{OUT_BASE}/{flower_name}"
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
    scn.render.filepath = f"{RENDER_DIR}/flower_{flower_name}_{stage_key}.png"
    bpy.ops.render.render(write_still=True)


def main():
    print(f"\n=== Common flowers — {len(FLOWERS)} species × {len(STAGE_NAMES)} stages ===\n")
    for fname in FLOWERS:
        print(f"\n=== {fname} ===")
        for stage in STAGE_NAMES:
            tris = build_state(fname, stage)
            print(f"  ✓ {stage}.obj  tris={tris}")
    print(f"\n=== Rendering ===\n")
    for fname, cfg in FLOWERS.items():
        # Per-stage ortho — shorter stages need tighter camera
        for stage in STAGE_NAMES:
            base = cfg["ortho"]
            if "seedling" in stage:   s = base * 0.30
            elif "growing" in stage:  s = base * 0.65
            elif "budding" in stage:  s = base * 0.85
            else:                     s = base
            render_state(fname, stage, s)
    print(f"\n=== Complete: {len(FLOWERS) * len(STAGE_NAMES)} models ===")


if __name__ == "__main__":
    main()
