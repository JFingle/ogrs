"""
Farm patches + scenery — 12 models.

Patch states (where crops grow, 3x3 tile footprint):
  patch_weeds    — natural overgrown (grass + weed sprigs scattered)
  patch_weeded   — half cleared (some weeds + brown dirt)
  patch_cleared  — raked brown soil, ridges
  patch_planted  — brown soil with small mound + seed marker stake

Scenery (single objects):
  scarecrow      — cross wooden frame + straw head + tattered clothes + hat
  leprechaun_stand — small signpost with green hat decoration
  compost_bin    — wooden slat bin with compost inside
  water_can_stand — post with hanging metal watering can
  tool_rack      — post with hoe + rake + spade hanging
  fence_section  — 2 posts + 4 slats + top rail
  corner_stake   — small twine-wrapped stake (patch boundary marker)
  bonemeal_pile  — small heap of white-beige chunks
"""
import bpy
import math
import os
import random

OUT_DIR = "/home/sparky/ogrs/art/models/farming/patches"
RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)

# Palette
SOIL_DARK   = (72/255, 48/255, 24/255, 1.0)    # rich dirt
SOIL_LIGHT  = (112/255, 80/255, 48/255, 1.0)   # dried/raked top
GRASS_DARK  = (64/255, 96/255, 40/255, 1.0)
GRASS_LIGHT = (96/255, 136/255, 56/255, 1.0)
WEED_GREEN  = (104/255, 128/255, 48/255, 1.0)
BARK        = (96/255, 64/255, 40/255, 1.0)
BARK_DARK   = (64/255, 40/255, 24/255, 1.0)
STRAW       = (216/255, 184/255, 96/255, 1.0)
STRAW_DARK  = (160/255, 128/255, 56/255, 1.0)
CLOTH       = (152/255, 96/255, 64/255, 1.0)   # tattered brown
CLOTH_DARK  = (96/255, 48/255, 32/255, 1.0)
METAL       = (152/255, 152/255, 168/255, 1.0)
METAL_DARK  = (104/255, 104/255, 120/255, 1.0)
LEP_GREEN   = (40/255, 144/255, 56/255, 1.0)
BONE_WHITE  = (232/255, 224/255, 208/255, 1.0)
TWINE       = (200/255, 168/255, 96/255, 1.0)
COMPOST     = (64/255, 44/255, 28/255, 1.0)


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

def add_box(mat, location, scale):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


def add_cyl(mat, radius, depth, location, rotation=(0, 0, 0), verts=8):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
                                        location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.data.materials.append(mat)
    return obj


def add_ico(mat, radius, location, scale=(1, 1, 1), rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


# ----------------------------------------------------------------
# Patch states (3x3 tile footprint = ~1.5m square)
# ----------------------------------------------------------------

PATCH_HALF = 0.75   # half-extent in X/Y (1.5m square)
PATCH_THICKNESS = 0.02


def build_patch_base(mats, top_color):
    """Flat soil square — the patch's ground layer."""
    add_box(top_color, (0, 0, PATCH_THICKNESS/2),
            (PATCH_HALF*2, PATCH_HALF*2, PATCH_THICKNESS))


def add_weed_sprig(mat, x, y, height=0.10, lean=0.0):
    """Small upright weed grass blade."""
    add_cyl(mat, 0.006, height, (x, y, PATCH_THICKNESS + height/2),
            rotation=(lean, 0, random.random()*math.pi), verts=4)


def add_grass_tuft(mat, x, y, count=4):
    """Small grass blade tuft — narrow upward icospheres."""
    rng = random.Random(int((x*1000 + y*1000)))
    for _ in range(count):
        ox = x + rng.uniform(-0.04, 0.04)
        oy = y + rng.uniform(-0.04, 0.04)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.04,
                                              location=(ox, oy, PATCH_THICKNESS + 0.03))
        b = bpy.context.active_object
        b.scale = (0.4, 0.2, 1.0)
        b.rotation_euler = (rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), rng.uniform(0, math.pi))
        b.data.materials.append(mat)


def add_rake_ridge(mat, y, length=PATCH_HALF*1.8, height=0.02):
    """Horizontal raised ridge running along X, for the raked-soil look."""
    add_box(mat, (0, y, PATCH_THICKNESS + height/2),
            (length, 0.06, height))


def build_patch_weeds():
    """Overgrown: full grass coverage + weed sprigs everywhere."""
    clear_scene()
    mats = {
        "grass_dark":  make_mat("grass_dark", GRASS_DARK),
        "grass_light": make_mat("grass_light", GRASS_LIGHT),
        "weed":        make_mat("weed", WEED_GREEN),
        "soil":        make_mat("soil", SOIL_DARK),
    }
    build_patch_base(mats, mats["grass_dark"])
    # Lots of grass tufts
    rng = random.Random(11)
    for _ in range(40):
        x = rng.uniform(-PATCH_HALF + 0.05, PATCH_HALF - 0.05)
        y = rng.uniform(-PATCH_HALF + 0.05, PATCH_HALF - 0.05)
        add_grass_tuft(mats["grass_light"] if rng.random() < 0.6 else mats["grass_dark"], x, y, count=2)
    # Weed sprigs (taller)
    for _ in range(20):
        x = rng.uniform(-PATCH_HALF + 0.1, PATCH_HALF - 0.1)
        y = rng.uniform(-PATCH_HALF + 0.1, PATCH_HALF - 0.1)
        add_weed_sprig(mats["weed"], x, y, height=rng.uniform(0.08, 0.14),
                       lean=rng.uniform(-0.2, 0.2))
    obj = join_to("patch_weeds")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/patch_weeds.obj")
    return len(obj.data.polygons)


def build_patch_weeded():
    """Half cleared — patches of dirt + remaining grass + weed roots."""
    clear_scene()
    mats = {
        "soil":  make_mat("soil", SOIL_LIGHT),
        "grass_dark":  make_mat("grass_dark", GRASS_DARK),
        "grass_light": make_mat("grass_light", GRASS_LIGHT),
        "weed":  make_mat("weed", WEED_GREEN),
    }
    build_patch_base(mats, mats["soil"])
    rng = random.Random(22)
    # Half the patch has grass tufts remaining (in clumps)
    for _ in range(12):
        x = rng.uniform(-PATCH_HALF + 0.1, PATCH_HALF - 0.1)
        y = rng.uniform(-PATCH_HALF + 0.1, PATCH_HALF - 0.1)
        add_grass_tuft(mats["grass_dark"], x, y, count=3)
    # A few weed sprigs
    for _ in range(8):
        x = rng.uniform(-PATCH_HALF + 0.1, PATCH_HALF - 0.1)
        y = rng.uniform(-PATCH_HALF + 0.1, PATCH_HALF - 0.1)
        add_weed_sprig(mats["weed"], x, y, height=rng.uniform(0.06, 0.10))
    obj = join_to("patch_weeded")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/patch_weeded.obj")
    return len(obj.data.polygons)


def build_patch_cleared():
    """Fully cleared raked brown soil — visible ridges from raking."""
    clear_scene()
    mats = {
        "soil_dark":  make_mat("soil_dark", SOIL_DARK),
        "soil_light": make_mat("soil_light", SOIL_LIGHT),
    }
    build_patch_base(mats, mats["soil_light"])
    # Rake ridges — 5 parallel raised strips
    for y in (-0.5, -0.25, 0.0, 0.25, 0.5):
        add_rake_ridge(mats["soil_dark"], y, length=PATCH_HALF*1.8, height=0.025)
    obj = join_to("patch_cleared")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/patch_cleared.obj")
    return len(obj.data.polygons)


def build_patch_planted():
    """Cleared soil with central mound + seed marker stake."""
    clear_scene()
    mats = {
        "soil_dark":  make_mat("soil_dark", SOIL_DARK),
        "soil_light": make_mat("soil_light", SOIL_LIGHT),
        "bark":       make_mat("bark", BARK),
        "twine":      make_mat("twine", TWINE),
    }
    build_patch_base(mats, mats["soil_light"])
    # Some rake ridges
    for y in (-0.4, 0.0, 0.4):
        add_rake_ridge(mats["soil_dark"], y, length=PATCH_HALF*1.6, height=0.020)
    # Central mound — small ico flattened
    add_ico(mats["soil_dark"], 0.10, (0, 0, PATCH_THICKNESS + 0.03), scale=(1.4, 1.4, 0.35))
    # Seed marker stake
    add_cyl(mats["bark"], 0.012, 0.20, (0, 0, PATCH_THICKNESS + 0.10), verts=5)
    # Twine wrap
    add_cyl(mats["twine"], 0.018, 0.015, (0, 0, PATCH_THICKNESS + 0.16), verts=6)
    obj = join_to("patch_planted")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/patch_planted.obj")
    return len(obj.data.polygons)


# ----------------------------------------------------------------
# Scenery
# ----------------------------------------------------------------

def build_scarecrow():
    clear_scene()
    mats = {
        "bark":       make_mat("bark", BARK),
        "straw":      make_mat("straw", STRAW),
        "straw_dark": make_mat("straw_dark", STRAW_DARK),
        "cloth":      make_mat("cloth", CLOTH),
        "cloth_dark": make_mat("cloth_dark", CLOTH_DARK),
    }
    # Vertical pole
    add_cyl(mats["bark"], 0.020, 1.20, (0, 0, 0.60), verts=6)
    # Horizontal crossbar at ~0.75m
    add_cyl(mats["bark"], 0.015, 0.50, (0, 0, 0.85),
            rotation=(0, math.pi/2, 0), verts=5)
    # Body — straw-stuffed cloth on the cross
    add_box(mats["cloth"], (0, 0, 0.65), (0.30, 0.16, 0.28))
    # Cloth patches (tattered look)
    add_box(mats["cloth_dark"], (0.10, 0.08, 0.55), (0.10, 0.04, 0.10))
    add_box(mats["cloth_dark"], (-0.08, 0.08, 0.72), (0.08, 0.04, 0.08))
    # Stuffed head — straw-colored sphere
    add_ico(mats["straw"], 0.13, (0, 0, 1.00), scale=(1, 1, 1.1))
    # Hat — wide brim + cone
    add_cyl(mats["cloth_dark"], 0.16, 0.02, (0, 0, 1.13), verts=8)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.10, radius2=0.02, depth=0.10,
                                    location=(0, 0, 1.18))
    bpy.context.active_object.data.materials.append(mats["cloth_dark"])
    # Straw sticking out at ends of crossbar (arms)
    add_ico(mats["straw_dark"], 0.04, (0.22, 0, 0.85), scale=(1.5, 0.5, 0.5))
    add_ico(mats["straw_dark"], 0.04, (-0.22, 0, 0.85), scale=(1.5, 0.5, 0.5))
    obj = join_to("scarecrow")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/scarecrow.obj")
    return len(obj.data.polygons)


def build_leprechaun_stand():
    clear_scene()
    mats = {
        "bark":     make_mat("bark", BARK),
        "lep_green": make_mat("lep_green", LEP_GREEN),
        "metal":    make_mat("metal", METAL_DARK),
    }
    # Signpost
    add_cyl(mats["bark"], 0.025, 0.80, (0, 0, 0.40), verts=6)
    # Plaque
    add_box(mats["bark"], (0, 0, 0.70), (0.30, 0.04, 0.20))
    # Green hat decoration (cone) on top
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.08, radius2=0.02, depth=0.14,
                                    location=(0, 0, 0.92))
    bpy.context.active_object.data.materials.append(mats["lep_green"])
    # Hat brim
    add_cyl(mats["lep_green"], 0.10, 0.02, (0, 0, 0.85), verts=8)
    # Hat band (metal buckle stripe)
    add_box(mats["metal"], (0, 0, 0.88), (0.16, 0.02, 0.03))
    obj = join_to("leprechaun_stand")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/leprechaun_stand.obj")
    return len(obj.data.polygons)


def build_compost_bin():
    clear_scene()
    mats = {
        "bark":    make_mat("bark", BARK),
        "compost": make_mat("compost", COMPOST),
        "soil":    make_mat("soil", SOIL_DARK),
    }
    # 4 corner posts (vertical)
    for x in (-0.20, 0.20):
        for y in (-0.20, 0.20):
            add_cyl(mats["bark"], 0.018, 0.40, (x, y, 0.20), verts=5)
    # Horizontal slats — 3 levels per side
    for z in (0.10, 0.22, 0.35):
        # Front + back
        for y in (-0.20, 0.20):
            add_box(mats["bark"], (0, y, z), (0.42, 0.025, 0.025))
        # Left + right
        for x in (-0.20, 0.20):
            add_box(mats["bark"], (x, 0, z), (0.025, 0.42, 0.025))
    # Compost inside (lumpy heap)
    rng = random.Random(33)
    for _ in range(8):
        ox = rng.uniform(-0.13, 0.13)
        oy = rng.uniform(-0.13, 0.13)
        oz = rng.uniform(0.04, 0.18)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.05, 0.08),
                                              location=(ox, oy, oz))
        c = bpy.context.active_object
        c.scale = (1, 1, 0.7)
        c.data.materials.append(mats["compost"])
    obj = join_to("compost_bin")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/compost_bin.obj")
    return len(obj.data.polygons)


def build_water_can_stand():
    clear_scene()
    mats = {
        "bark":  make_mat("bark", BARK),
        "metal": make_mat("metal", METAL),
        "metal_dark": make_mat("metal_dark", METAL_DARK),
    }
    # Post
    add_cyl(mats["bark"], 0.022, 0.80, (0, 0, 0.40), verts=6)
    # Peg sticking out
    add_cyl(mats["bark"], 0.012, 0.10, (0.08, 0, 0.55),
            rotation=(0, math.pi/2, 0), verts=4)
    # Watering can body (hanging slightly below peg)
    add_box(mats["metal"], (0.15, 0, 0.40), (0.16, 0.10, 0.14))
    # Spout (long thin tube)
    add_cyl(mats["metal_dark"], 0.015, 0.18, (0.27, 0, 0.45),
            rotation=(0, math.pi/2.4, 0), verts=5)
    # Handle (loop on top)
    add_cyl(mats["metal_dark"], 0.015, 0.08, (0.15, 0, 0.50),
            rotation=(math.pi/2, 0, 0), verts=4)
    obj = join_to("water_can_stand")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/water_can_stand.obj")
    return len(obj.data.polygons)


def build_tool_rack():
    clear_scene()
    mats = {
        "bark":  make_mat("bark", BARK),
        "metal": make_mat("metal", METAL),
    }
    # Vertical post
    add_cyl(mats["bark"], 0.025, 1.00, (0, 0, 0.50), verts=6)
    # 3 horizontal pegs
    for z, x_off in [(0.30, 0.10), (0.55, 0.10), (0.80, 0.10)]:
        add_cyl(mats["bark"], 0.010, 0.10, (x_off/2, 0, z),
                rotation=(0, math.pi/2, 0), verts=4)
    # Tool 1 — hoe (handle + triangular blade)
    add_cyl(mats["bark"], 0.012, 0.40, (0.20, 0, 0.30), verts=4)
    add_box(mats["metal"], (0.20, 0, 0.10), (0.08, 0.02, 0.04))
    # Tool 2 — rake (handle + prongs)
    add_cyl(mats["bark"], 0.012, 0.40, (0.20, 0, 0.55), verts=4)
    for px in (-0.06, -0.02, 0.02, 0.06):
        add_cyl(mats["metal"], 0.006, 0.06, (0.20 + px, 0, 0.32), verts=3)
    # Tool 3 — spade (handle + flat blade)
    add_cyl(mats["bark"], 0.012, 0.40, (0.20, 0, 0.80), verts=4)
    add_box(mats["metal"], (0.20, 0, 0.58), (0.06, 0.02, 0.08))
    obj = join_to("tool_rack")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/tool_rack.obj")
    return len(obj.data.polygons)


def build_fence_section():
    clear_scene()
    mats = {"bark": make_mat("bark", BARK)}
    # 2 vertical posts
    for x in (-0.50, 0.50):
        add_cyl(mats["bark"], 0.025, 0.60, (x, 0, 0.30), verts=5)
    # 4 vertical slats between
    for x in (-0.30, -0.10, 0.10, 0.30):
        add_box(mats["bark"], (x, 0, 0.25), (0.025, 0.02, 0.40))
    # Top horizontal rail
    add_box(mats["bark"], (0, 0, 0.50), (1.05, 0.025, 0.025))
    # Bottom horizontal rail (smaller)
    add_box(mats["bark"], (0, 0, 0.10), (1.05, 0.025, 0.025))
    obj = join_to("fence_section")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/fence_section.obj")
    return len(obj.data.polygons)


def build_corner_stake():
    clear_scene()
    mats = {
        "bark":  make_mat("bark", BARK),
        "twine": make_mat("twine", TWINE),
    }
    # Single small upright stake
    add_cyl(mats["bark"], 0.014, 0.30, (0, 0, 0.15), verts=5)
    # Twine wrapping near the top
    for z in (0.20, 0.225, 0.25):
        add_cyl(mats["twine"], 0.020, 0.008, (0, 0, z), verts=6)
    # Pointed top (cone)
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.014, radius2=0.0,
                                    depth=0.04, location=(0, 0, 0.32))
    bpy.context.active_object.data.materials.append(mats["bark"])
    obj = join_to("corner_stake")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/corner_stake.obj")
    return len(obj.data.polygons)


def build_bonemeal_pile():
    clear_scene()
    mats = {"bone": make_mat("bone", BONE_WHITE)}
    rng = random.Random(44)
    # Small heap of bone chunks
    for _ in range(8):
        ox = rng.uniform(-0.12, 0.12)
        oy = rng.uniform(-0.12, 0.12)
        oz = rng.uniform(0.02, 0.08)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.025, 0.045),
                                              location=(ox, oy, oz))
        c = bpy.context.active_object
        c.scale = (rng.uniform(0.8, 1.3), rng.uniform(0.6, 1.0), rng.uniform(0.5, 0.9))
        c.rotation_euler = (rng.uniform(0, math.pi), rng.uniform(0, math.pi), rng.uniform(0, math.pi))
        c.data.materials.append(mats["bone"])
    obj = join_to("bonemeal_pile")
    shade_flat_obj(obj)
    export_obj(obj.name, f"{OUT_DIR}/bonemeal_pile.obj")
    return len(obj.data.polygons)


# ----------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------

ITEMS = [
    ("patch_weeds",       build_patch_weeds,       2.2, 0.5),
    ("patch_weeded",      build_patch_weeded,      2.2, 0.5),
    ("patch_cleared",     build_patch_cleared,     2.2, 0.5),
    ("patch_planted",     build_patch_planted,     2.2, 0.5),
    ("scarecrow",         build_scarecrow,         2.0, 1.2),
    ("leprechaun_stand",  build_leprechaun_stand,  1.5, 0.7),
    ("compost_bin",       build_compost_bin,       1.0, 0.5),
    ("water_can_stand",   build_water_can_stand,   1.4, 0.7),
    ("tool_rack",         build_tool_rack,         1.6, 0.8),
    ("fence_section",     build_fence_section,     1.6, 0.7),
    ("corner_stake",      build_corner_stake,      0.6, 0.3),
    ("bonemeal_pile",     build_bonemeal_pile,     0.5, 0.2),
]


def setup_camera(ortho_scale, cam_height):
    bpy.ops.object.camera_add(
        location=(cam_height * 1.5, -cam_height * 1.5, cam_height * 0.9),
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


def render_item(name, ortho_scale, cam_height):
    clear_scene()
    bpy.ops.wm.obj_import(filepath=f"{OUT_DIR}/{name}.obj",
                          forward_axis="NEGATIVE_Y", up_axis="Z")
    setup_camera(ortho_scale, cam_height)
    scn = bpy.context.scene
    scn.render.resolution_x = 256
    scn.render.resolution_y = 256
    scn.render.image_settings.file_format = "PNG"
    scn.render.film_transparent = True
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.filepath = f"{RENDER_DIR}/scenery_{name}.png"
    bpy.ops.render.render(write_still=True)


def main():
    print(f"\n=== Farm scenery — {len(ITEMS)} items ===\n")
    for name, builder, _, _ in ITEMS:
        print(f"\n=== {name} ===")
        tris = builder()
        print(f"  ✓ {name}.obj  tris={tris}")
    print(f"\n=== Rendering ===\n")
    for name, _, ortho, cam_h in ITEMS:
        render_item(name, ortho, cam_h)
    print(f"\n=== Complete: {len(ITEMS)} models ===")


if __name__ == "__main__":
    main()
