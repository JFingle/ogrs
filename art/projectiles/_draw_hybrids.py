#!/usr/bin/env python3
"""
Hybrid impact builder — for each debuff, combine the triple-helix swirl
(frames 0-3) with the radial-dissipate explosion (frames 4-7) into an
8-frame animation.

Reads from each spell's existing _draw_impact_swirl.py + _draw_impact.py
modules — those scripts must define draw_frame(i) returning a PIL Image.
"""
import importlib.util, os, sys
from PIL import Image

ROOT = "/home/sparky/ogrs/art/projectiles"
W = H = 48

SPELLS = ["debuff_stun", "debuff_enfeeble", "debuff_vulnerability",
          "debuff_confuse", "debuff_weaken"]


def load(folder, module_basename):
    path = os.path.join(ROOT, folder, f"{module_basename}.py")
    spec = importlib.util.spec_from_file_location(f"{folder}_{module_basename}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_hybrid(folder):
    swirl_mod  = load(folder, "_draw_impact_swirl")
    radial_mod = load(folder, "_draw_impact")
    out_dir = os.path.join(ROOT, folder, "impact_hybrid")
    os.makedirs(out_dir, exist_ok=True)
    print(f"=== {folder} ===")
    for i in range(4):
        img = swirl_mod.draw_frame(i)
        img.save(f"{out_dir}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{out_dir}/frame_{i:02d}_x6.png")
        print(f"  hybrid frame_{i:02d} <- swirl frame_{i:02d}")
    for j in range(4):
        img = radial_mod.draw_frame(j)
        idx = 4 + j
        img.save(f"{out_dir}/frame_{idx:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{out_dir}/frame_{idx:02d}_x6.png")
        print(f"  hybrid frame_{idx:02d} <- radial frame_{j:02d}")
    return out_dir


if __name__ == "__main__":
    for folder in SPELLS:
        build_hybrid(folder)
