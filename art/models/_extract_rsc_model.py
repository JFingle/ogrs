"""
Extract a single .ob3 model from OpenRSC models.orsc and convert to .obj.

The .orsc archive format (from DataOperations.java):
  [2 bytes BE]    numEntries
  per entry (10 bytes):
    [4 bytes BE]  fileHash
    [3 bytes BE]  decmp_len (decompressed size)
    [3 bytes BE]  cmp_len (compressed size)
  then concatenated entry data, each cmp_len bytes long

Hash function:
  hash = 0
  for c in filename.upper():
      hash = hash * 61 + ord(c) - 32

If decmp_len == cmp_len → raw; else needs DataFileDecrypter (bzip2-ish).

The .ob3 model format (from RSModel.java constructor):
  [2 BE]                 vertexCount
  [2 BE]                 faceCount
  [vc*2 BE signed]       vertX[]
  [vc*2 BE signed]       vertY[]
  [vc*2 BE signed]       vertZ[]
  [fc bytes]             faceIndexCount[] (verts per face)
  [fc*2 BE]              faceTextureFront[]  (color or texture id)
  [fc*2 BE]              faceTextureBack[]
  [fc bytes]             faceDiffuseLight[] (flag)
  [variable]             faceIndices[][]  (1 byte per idx if vc<256, else 2)

Color encoding (negative = solid color, positive = texture):
  When the value is negative, it's an RGB color encoded as -(rgb >> 1) or similar.
  Check RSModel.computeDiffuse() / Polygon.java for exact decode.
"""
import os, sys, struct

ARCHIVE = "/home/sparky/ogrs/client/Cache/video/models.orsc"
OUT_DIR = "/home/sparky/ogrs/art/models/_rsc_reference"
os.makedirs(OUT_DIR, exist_ok=True)


def name_hash(filename):
    h = 0
    for c in filename.upper():
        h = (h * 61 + ord(c) - 32) & 0xFFFFFFFF
    return h


def parse_archive_header(data):
    n = (data[0] << 8) | data[1]
    entries = []
    for i in range(n):
        base = 2 + i * 10
        h = (data[base] << 24) | (data[base+1] << 16) | (data[base+2] << 8) | data[base+3]
        decmp = (data[base+4] << 16) | (data[base+5] << 8) | data[base+6]
        cmp = (data[base+7] << 16) | (data[base+8] << 8) | data[base+9]
        entries.append((h, decmp, cmp))
    return entries


def find_entry(filename, data):
    want = name_hash(filename)
    entries = parse_archive_header(data)
    offset = 2 + len(entries) * 10
    for h, decmp, cmp in entries:
        if h == want:
            return offset, decmp, cmp
        offset += cmp
    return None


def read_short(buf, off):
    v = (buf[off] << 8) | buf[off + 1]
    if v >= 0x8000:
        v -= 0x10000
    return v


def read_ushort(buf, off):
    return (buf[off] << 8) | buf[off + 1]


def parse_ob3(data):
    """Parse .ob3 model bytes. Returns dict with vertices, faces, face_colors."""
    p = 0
    vc = read_ushort(data, p); p += 2
    fc = read_ushort(data, p); p += 2
    vx = [read_short(data, p + i * 2) for i in range(vc)]; p += vc * 2
    vy = [read_short(data, p + i * 2) for i in range(vc)]; p += vc * 2
    vz = [read_short(data, p + i * 2) for i in range(vc)]; p += vc * 2
    face_idx_count = list(data[p:p + fc]); p += fc
    face_tex_front = [read_short(data, p + i * 2) for i in range(fc)]; p += fc * 2
    face_tex_back = [read_short(data, p + i * 2) for i in range(fc)]; p += fc * 2
    face_diffuse = list(data[p:p + fc]); p += fc
    face_indices = []
    for i in range(fc):
        count = face_idx_count[i]
        if vc < 256:
            idx = list(data[p:p + count])
            p += count
        else:
            idx = [read_ushort(data, p + k * 2) for k in range(count)]
            p += count * 2
        face_indices.append(idx)
    return {
        "vert_count": vc, "face_count": fc,
        "vx": vx, "vy": vy, "vz": vz,
        "face_idx_count": face_idx_count,
        "face_tex_front": face_tex_front,
        "face_tex_back": face_tex_back,
        "face_diffuse": face_diffuse,
        "face_indices": face_indices,
    }


def decode_face_color(color_int):
    """Convert RSC face color value to (r,g,b)."""
    # In OpenRSC, negative values are solid RGB colors.
    # The encoding pattern: positive = texture index, negative ≈ -(color>>1)?
    # Looking at the actual ranges in models, the value is stored as a signed
    # 16-bit value; the color decode happens in Polygon.java / Scanline.java.
    # Common pattern: actual_color = ((value & 0xff) << 16) | (value & 0xff00) | ((value & 0xff0000) >> 16)?
    # Simpler: many RSC models use the lower 16 bits directly as RGB-565-ish.
    # For our purposes: treat negative as solid color, positive as texture.
    if color_int >= 0:
        return ("texture", color_int)
    # Try: actual = -color * 2  (most common RSC pattern)
    c = -color_int
    r = (c >> 10) & 0x1F
    g = (c >> 5) & 0x1F
    b = c & 0x1F
    return ("color_rgb15", c, (r << 3, g << 3, b << 3))


def export_obj(model, out_path, name="model"):
    """Export parsed model to Wavefront .obj + .mtl with per-face colors."""
    mtl_path = out_path.rsplit(".", 1)[0] + ".mtl"
    # Build unique material list from face colors
    unique_colors = sorted(set(model["face_tex_front"]))
    color_to_matname = {}
    with open(mtl_path, "w") as fm:
        for c in unique_colors:
            if c >= 0:
                # texture id — fallback to magenta so we notice
                name_m = f"tex_{c}"
                rgb = (1.0, 0.0, 1.0)
            else:
                ci = -c
                r = ((ci >> 10) & 31) << 3
                g = ((ci >> 5) & 31) << 3
                b = (ci & 31) << 3
                name_m = f"rsc_{r:02x}{g:02x}{b:02x}"
                rgb = (r / 255.0, g / 255.0, b / 255.0)
            color_to_matname[c] = name_m
            fm.write(f"newmtl {name_m}\n")
            fm.write(f"Kd {rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f}\n")
            fm.write(f"Ka {rgb[0]*0.2:.4f} {rgb[1]*0.2:.4f} {rgb[2]*0.2:.4f}\n")
            fm.write(f"Ks 0 0 0\nNs 1\nillum 1\n\n")

    with open(out_path, "w") as f:
        f.write(f"# OGRS RSC model extracted from .ob3\n")
        f.write(f"# vertices: {model['vert_count']}  faces: {model['face_count']}\n")
        f.write(f"mtllib {os.path.basename(mtl_path)}\n\n")
        f.write(f"o {name}\n")
        # OB3 uses Y as up; convert to Z-up for Blender by swapping.
        scale = 0.01
        for x, y, z in zip(model["vx"], model["vy"], model["vz"]):
            f.write(f"v {x * scale} {-z * scale} {-y * scale}\n")
        f.write("\n")
        # Group faces by material for cleaner output
        from collections import defaultdict
        faces_by_color = defaultdict(list)
        for idxs, c in zip(model["face_indices"], model["face_tex_front"]):
            faces_by_color[c].append(idxs)
        for c, faces in faces_by_color.items():
            f.write(f"usemtl {color_to_matname[c]}\n")
            for idxs in faces:
                f.write("f " + " ".join(str(i + 1) for i in idxs) + "\n")


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "tomatoplant"
    fname = name + ".ob3"
    with open(ARCHIVE, "rb") as f:
        raw = f.read()
    # Skip the 6-byte file header (decmp_len, cmp_len) — see mudclient.unpackData
    file_decmp = (raw[0] << 16) | (raw[1] << 8) | raw[2]
    file_cmp = (raw[3] << 16) | (raw[4] << 8) | raw[5]
    print(f"File header: decmp={file_decmp}  cmp={file_cmp}  compressed={'YES' if file_decmp != file_cmp else 'NO'}")
    if file_decmp != file_cmp:
        print("⚠ File-level compression needs DataFileDecrypter port — bailing.")
        return
    data = raw[6:]
    entries = parse_archive_header(data)
    print(f"Archive entries: {len(entries)}")
    hit = find_entry(fname, data)
    if not hit:
        print(f"NOT FOUND: {fname}")
        print(f"Some entries (first 8 hashes): {[hex(e[0]) for e in entries[:8]]}")
        return
    offset, decmp, cmp = hit
    print(f"Found {fname}: offset=0x{offset:x}  decmp={decmp}  cmp={cmp}  compressed={'YES' if cmp != decmp else 'NO'}")
    if cmp != decmp:
        print("⚠ Data is compressed — need DataFileDecrypter port to extract.")
        return
    body = data[offset:offset + cmp]
    # Save raw .ob3
    raw_out = f"{OUT_DIR}/{name}.ob3"
    with open(raw_out, "wb") as f:
        f.write(body)
    print(f"Saved raw: {raw_out}")
    # Parse + dump info
    model = parse_ob3(body)
    print(f"Vertices: {model['vert_count']}, Faces: {model['face_count']}")
    # Unique face colors
    color_counts = {}
    for c in model["face_tex_front"]:
        color_counts[c] = color_counts.get(c, 0) + 1
    print(f"\nUnique face colors (top 20 by frequency):")
    for c, count in sorted(color_counts.items(), key=lambda x: -x[1])[:20]:
        decoded = decode_face_color(c)
        print(f"  raw={c} ({c & 0xFFFF:#06x})  count={count}  decoded={decoded}")
    # Export as obj
    obj_out = f"{OUT_DIR}/{name}.obj"
    export_obj(model, obj_out, name=name)
    print(f"Saved .obj: {obj_out}")
    # Bounding box info
    print(f"X range: {min(model['vx'])} .. {max(model['vx'])}")
    print(f"Y range: {min(model['vy'])} .. {max(model['vy'])}")
    print(f"Z range: {min(model['vz'])} .. {max(model['vz'])}")


if __name__ == "__main__":
    main()
