# EP004 S01 patch v012: corrections after motion test v2. Applied IN PLACE to ep004_s01_camera_v011.blend.
# Keeps: shot ranges (A 1-102, B 201-320, C 401-422), narration timing, the camera path overall.
# Targeted camera edits only: A macro keys (27, 40), A end key (102) + B start key (201, same pose), C pull-back speed within its 22 frames.
import bpy, bmesh, math, os, numpy as np
from mathutils import Vector
sc = bpy.context.scene; M = bpy.data.materials; O = bpy.data.objects
SX, SY = 0.8, 4.6
def col(name):
    c = bpy.data.collections.get(name)
    if not c: c = bpy.data.collections.new(name); sc.collection.children.link(c)
    return c
def link(m, a, sa, b, sb): m.node_tree.links.new(a.outputs[sa], b.inputs[sb])

# ---------- helpers ----------
def euler_for(pos, tgt, prev):
    d = Vector(tgt) - Vector(pos); d.normalize()
    rx = math.acos(max(-1.0, min(1.0, -d.z)))
    rz = math.atan2(-d.x, d.y) if math.hypot(d.x, d.y) > 1e-4 else prev
    while rz - prev > math.pi: rz -= 2 * math.pi
    while rz - prev < -math.pi: rz += 2 * math.pi
    return (rx, 0.0, rz)
def rz_at(cam, f):
    sc.frame_set(f); return cam.rotation_euler.z
def set_key(cam, f, pos, tgt, prev):
    e = euler_for(pos, tgt, prev); cam.location = pos; cam.rotation_euler = e
    cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f); return e[2]

# =====================  A: OLED macro, glare, DRAM framing  =====================
camA = O['CAM_S01_A_pushthrough']
rz = rz_at(camA, 19)
rz = set_key(camA, 27, (SX - 0.12, SY - 0.30, 4.80), (SX, SY - 0.05, 4.48), rz)       # steeper, near top-down on the pixels
rz = set_key(camA, 40, (SX + 0.35, SY - 0.10, 4.74), (SX + 0.58, SY + 0.12, 4.48), rz) # slides across with the pixel wave
rz78 = rz_at(camA, 78)
A_END = ((SX - 2.0, SY - 2.7, 0.72), (SX, SY, 0.78))
set_key(camA, 102, A_END[0], A_END[1], rz78)                                         # DRAM + AP both in frame
camB = O['CAM_S01_B_dive']; rzB = rz_at(camB, 217)
set_key(camB, 201, A_END[0], A_END[1], rzB)                                          # B still starts on A's last pose

# glare: dim the key lights while the camera is among the glossy screen layers; drop the exposure dips from v011
for name, base, low in (('key_softbox', 18000.0, 4500.0), ('rim_cyan', 9000.0, 2300.0), ('fill_low', 2500.0, 1250.0)):
    d = O[name].data
    for f, v in ((14, base), (24, low), (52, low), (66, base)):
        d.energy = v; d.keyframe_insert('energy', frame=f)
for f in (1, 14, 26, 40, 50, 62):
    sc.view_settings.exposure = 0.0; sc.keyframe_insert('view_settings.exposure', frame=f)
sc.view_settings.exposure = 0.0

# OLED material: readable coloured pixels, low specular, moving brightness wave
m = M['oled_subpixels']; n = m.node_tree.nodes; b = n['Principled BSDF']
b.inputs['Roughness'].default_value = 0.7
for key in ('Specular IOR Level',):
    if key in b.inputs: b.inputs[key].default_value = 0.03
for nd in n:
    if nd.type == 'MATH' and nd.operation == 'MULTIPLY' and abs(nd.inputs[1].default_value - 120.0) < 1e-3:
        nd.inputs[1].default_value = 70.0                                      # coarser sub-pixels: ~14 across the macro frame
st = n['screen_on']
st.inputs[1].default_value = 0.0; st.inputs[1].keyframe_insert('default_value', frame=1)
st.inputs[1].default_value = 2.4; st.inputs[1].keyframe_insert('default_value', frame=24)
tc = n.new('ShaderNodeTexCoord'); sp = n.new('ShaderNodeSeparateXYZ'); link(m, tc, 'Object', sp, 'Vector')
ph = n.new('ShaderNodeValue'); ph.name = 'wave_phase'
for f, v in ((22, SX - 0.35), (46, SX + 0.95)):
    ph.outputs[0].default_value = v; ph.outputs[0].keyframe_insert('default_value', frame=f)
sub = n.new('ShaderNodeMath'); sub.operation = 'SUBTRACT'; link(m, sp, 'X', sub, 0); link(m, ph, 0, sub, 1)
ab = n.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; link(m, sub, 0, ab, 0)
k = n.new('ShaderNodeMath'); k.operation = 'MULTIPLY'; k.inputs[1].default_value = 7.0; link(m, ab, 0, k, 0)
inv = n.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; inv.use_clamp = True; link(m, k, 0, inv, 1)
lift = n.new('ShaderNodeMath'); lift.operation = 'MULTIPLY_ADD'; lift.inputs[1].default_value = 0.8; lift.inputs[2].default_value = 0.25; link(m, inv, 0, lift, 0)
fin = n.new('ShaderNodeMath'); fin.operation = 'MULTIPLY'; link(m, st, 0, fin, 0); link(m, lift, 0, fin, 1)
link(m, fin, 0, b, 'Emission Strength')

# =====================  B: lighting, copper layers, 3D lattice, label  =====================
bgn = sc.world.node_tree.nodes['Background'].inputs['Strength']
for f, v in ((1, 1.0), (200, 1.0), (222, 7.0), (300, 7.0), (320, 5.0), (401, 3.0), (422, 3.0)):
    bgn.default_value = v; bgn.keyframe_insert('default_value', frame=f)
rl = O['die_under_reflector'].data
for f, v in ((235, 140.0), (400, 140.0)):
    rl.energy = v; rl.keyframe_insert('energy', frame=f)
# die top metal: blur reflections so it is lit rather than a black mirror
for nd in M['die_topmetal_iridescent'].node_tree.nodes:
    if nd.type == 'MAP_RANGE' and abs(nd.inputs['To Max'].default_value - 0.4) < 1e-3:
        nd.inputs['To Min'].default_value = 0.22; nd.inputs['To Max'].default_value = 0.5

def wire_mat(name, axes, tint):
    mm = bpy.data.materials.new(name); mm.use_nodes = True; nn = mm.node_tree.nodes; bb = nn['Principled BSDF']
    tcn = nn.new('ShaderNodeTexCoord'); spn = nn.new('ShaderNodeSeparateXYZ'); link(mm, tcn, 'Object', spn, 'Vector')
    masks = []
    for ax, sc_ in axes:
        mu = nn.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = sc_; link(mm, spn, ax, mu, 0)
        fr = nn.new('ShaderNodeMath'); fr.operation = 'FRACT'; link(mm, mu, 0, fr, 0)
        lt = nn.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.42; link(mm, fr, 0, lt, 0); masks.append(lt)
    mask = masks[0]
    if len(masks) > 1:
        mask = nn.new('ShaderNodeMath'); mask.operation = 'MAXIMUM'; link(mm, masks[0], 0, mask, 0); link(mm, masks[1], 0, mask, 1)
    mix = nn.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs[6].default_value = (0.03, 0.035, 0.05, 1); mix.inputs[7].default_value = (*tint, 1)
    link(mm, mask, 0, mix, 'Factor'); link(mm, mix, 2, bb, 'Base Color'); link(mm, mask, 0, bb, 'Metallic')
    rr = nn.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value = 0.65; rr.inputs['To Max'].default_value = 0.26
    link(mm, mask, 0, rr, 'Value'); link(mm, rr, 'Result', bb, 'Roughness')
    bp = nn.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 1.6; bp.inputs['Distance'].default_value = 0.0007
    link(mm, mask, 0, bp, 'Height'); link(mm, bp, 'Normal', bb, 'Normal')
    return mm
WIRING = {1: ((('X', 95), ('Y', 95)), (0.80, 0.46, 0.24)), 2: ((('X', 70),), (0.76, 0.48, 0.28)), 3: ((('Y', 56),), (0.72, 0.50, 0.32)),
          4: ((('X', 44),), (0.68, 0.52, 0.36)), 5: ((('Y', 34),), (0.64, 0.54, 0.40))}
for kk, (axes, tint) in WIRING.items():
    o = O[f'die_M{kk}']; o.data.materials[0] = wire_mat(f'die_M{kk}_wiring_v2', axes, tint)
for kk in range(1, 7):
    o = O[f'die_M{kk}']; bv = o.modifiers.new('edge', 'BEVEL'); bv.width = 0.0007; bv.segments = 2

# 3D transistor lattice patch (illustrative: fins, gates, contacts) under the field plane, camera-facing side
cl = col('04_POP_SOC'); ZP = 0.3685; P = 0.0045; HALF = 0.25
def mk(name, color, metal, rough):
    mm = bpy.data.materials.new(name); mm.use_nodes = True; b2 = mm.node_tree.nodes['Principled BSDF']
    b2.inputs['Base Color'].default_value = (*color, 1); b2.inputs['Metallic'].default_value = metal; b2.inputs['Roughness'].default_value = rough
    return mm
def obj_from(bm, name, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p_ in me.polygons: p_.use_smooth = False
    o = bpy.data.objects.new(name, me); cl.objects.link(o); o.data.materials.append(mat); return o
bf, bg, bc = bmesh.new(), bmesh.new(), bmesh.new()
def box(bm, cx, cy, cz, sx, sy, sz):
    r = bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=r['verts']); bmesh.ops.translate(bm, vec=(cx, cy, cz), verts=r['verts'])
NF = int(HALF / P)
for i in range(-NF, NF + 1):                                   # fins run along X
    box(bf, SX, SY + i * P, ZP - 0.0007, 2 * HALF, 0.0016, 0.0014)
for j in range(-NF // 2, NF // 2 + 1):                         # gates cross the fins along Y, standing proud of them
    box(bg, SX + j * 2 * P, SY, ZP - 0.0014 - 0.0006, 0.0016, 2 * HALF, 0.0012)
    for i in range(-NF, NF + 1, 3):                            # contacts on the gates
        r = bmesh.ops.create_cone(bc, cap_ends=True, segments=8, radius1=0.00055, radius2=0.00055, depth=0.0011)
        bmesh.ops.translate(bc, vec=(SX + j * 2 * P, SY + i * P, ZP - 0.0014 - 0.0012 - 0.00055), verts=r['verts'])
fins = obj_from(bf, 'lattice_fins', mk('lattice_fin_grey', (0.30, 0.31, 0.33), 0.5, 0.4))
gates = obj_from(bg, 'lattice_gates', mk('lattice_gate_grey', (0.55, 0.56, 0.58), 0.7, 0.3))
cons = obj_from(bc, 'lattice_contacts', mk('lattice_contact_white', (0.82, 0.83, 0.86), 0.8, 0.25))

# label: ILLUSTRATIVE · NOT TO SCALE, camera-parented, fades in and out
def label(cam, text, keys, d=0.05, y=-0.0075):
    cu = bpy.data.curves.new('lbl_' + cam.name, 'FONT'); cu.body = text; cu.size = 0.0011; cu.align_x = 'CENTER'; cu.space_character = 1.1
    t = bpy.data.objects.new('label_' + cam.name, cu); cl.objects.link(t); t.parent = cam; t.location = (0, y, -d)
    mt = bpy.data.materials.new('label_text_' + cam.name); mt.use_nodes = True; bt = mt.node_tree.nodes['Principled BSDF']
    bt.inputs['Base Color'].default_value = (0, 0, 0, 1); bt.inputs['Emission Color'].default_value = (0.9, 0.95, 1.0, 1)
    cu.materials.append(mt)
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    pl_me = bpy.data.meshes.new('lblplate'); bm.to_mesh(pl_me); bm.free()
    pl = bpy.data.objects.new('labelplate_' + cam.name, pl_me); cl.objects.link(pl); pl.parent = cam
    pl.location = (0, y + 0.0004, -d - 0.0001); pl.scale = (0.0215, 0.0032, 1)
    mp = bpy.data.materials.new('label_plate_' + cam.name); mp.use_nodes = True; bp = mp.node_tree.nodes['Principled BSDF']
    bp.inputs['Base Color'].default_value = (0.01, 0.012, 0.016, 1); pl_me.materials.append(mp)
    for (f, vt, vp) in keys:
        bt.inputs['Emission Strength'].default_value = vt; bt.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)
        bp.inputs['Alpha'].default_value = vp; bp.inputs['Alpha'].keyframe_insert('default_value', frame=f)
        bt.inputs['Alpha'].default_value = 1.0 if vt > 0 else 0.0; bt.inputs['Alpha'].keyframe_insert('default_value', frame=f)
label(camB, 'ILLUSTRATIVE · NOT TO SCALE', ((220, 0.0, 0.0), (228, 3.0, 0.6), (314, 3.0, 0.6), (320, 0.0, 0.0)))
camC = O['CAM_S01_C_wafer']
label(camC, 'ILLUSTRATIVE · NOT TO SCALE', ((401, 3.0, 0.6), (406, 0.0, 0.0)))

# =====================  C: wafer arrives early, vivid identical dies  =====================
camC.animation_data_clear(); camC.data.animation_data_clear()
rz = camB['last_rz'] if 'last_rz' in camB else 0.0
sc.frame_set(320); rzc = camB.rotation_euler.z
CK = ((401, (SX - 0.004, SY - 0.006, 0.305), (SX, SY, 0.369)), (405, (SX - 0.01, SY - 0.03, -6.0), (SX, SY, 0.34)),
      (409, (SX, SY - 0.1, -22.0), (SX, SY, 0.34)), (413, (SX, SY - 0.2, -42.0), (SX, SY, 0.34)), (422, (SX, SY - 0.3, -49.0), (SX, SY, 0.34)))
prev = rzc
for f, p, t in CK: prev = set_key(camC, f, p, t, prev)
for f, l in ((401, 50.0), (413, 28.0), (422, 28.0)):
    camC.data.lens = l; camC.data.keyframe_insert('lens', frame=f)
for f, v in ((1, 0.0), (400, 0.0), (401, 0.6), (404, 3.0), (407, 10.0), (410, 24.0)):
    for mn in ('wafer_die_tiles', 'wafer_silicon'):
        for nd in M[mn].node_tree.nodes:
            if nd.type == 'MATH' and nd.operation == 'LESS_THAN':
                nd.inputs[1].default_value = v; nd.inputs[1].keyframe_insert('default_value', frame=f)
for f in (416, 422):                                         # drop the old late keys
    for mn in ('wafer_die_tiles', 'wafer_silicon'):
        for nd in M[mn].node_tree.nodes:
            if nd.type == 'MATH' and nd.operation == 'LESS_THAN':
                try: nd.inputs[1].keyframe_delete('default_value', frame=f)
                except Exception: pass
# identical dies: every die uses the same local coordinates; thin-film colours more saturated
def iridescent_vector(mat, offset, pitch):
    nn = mat.node_tree.nodes; tcn = nn.new('ShaderNodeTexCoord'); spn = nn.new('ShaderNodeSeparateXYZ'); link(mat, tcn, 'Object', spn, 'Vector')
    comps = []
    for ax, off in zip(('X', 'Y'), offset):
        a = nn.new('ShaderNodeMath'); a.operation = 'ADD'; a.inputs[1].default_value = off; link(mat, spn, ax, a, 0)
        if pitch:
            w = nn.new('ShaderNodeMath'); w.operation = 'FLOORED_MODULO'; w.inputs[1].default_value = pitch; link(mat, a, 0, w, 0)
            comps.append(w)
        else: comps.append(a)
    cmb = nn.new('ShaderNodeCombineXYZ'); link(mat, comps[0], 0, cmb, 'X'); link(mat, comps[1], 0, cmb, 'Y')
    for nd in nn:
        if nd.type == 'TEX_NOISE': link(mat, cmb, 0, nd, 'Vector'); nd.inputs['Scale'].default_value = 5.0
        if nd.type == 'MAP_RANGE' and nd.inputs['To Max'].default_value > 100:
            nd.inputs['To Min'].default_value = 230.0; nd.inputs['To Max'].default_value = 640.0
iridescent_vector(M['wafer_die_tiles'], (0.54, 0.54), 1.08)           # per-die local coords (die pitch 1.08 cm)
iridescent_vector(M['die_topmetal_iridescent'], (-SX, -SY), None)     # hero die uses the same local frame
sw = M['wafer_silicon'].node_tree.nodes['Principled BSDF']
sw.inputs['Base Color'].default_value = (0.03, 0.035, 0.045, 1); sw.inputs['Roughness'].default_value = 0.3
wl = O['wafer_light'].data
for f, v in ((400, 0.0), (403, 3200.0)):
    wl.energy = v; wl.keyframe_insert('energy', frame=f)

# =====================  verification sheets (not video)  =====================
import tempfile
gpu(sc, 'auto'); sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.use_denoising = True
tmp = tempfile.mkdtemp()
def sheet(frames, cam, fname, w=480, h=270):
    sc.render.resolution_x, sc.render.resolution_y = w, h; sc.camera = cam; tiles = []
    for f in frames:
        sc.frame_set(f); p = os.path.join(tmp, f'{fname}_{f}.png'); sc.render.filepath = p
        bpy.ops.render.render(write_still=True); im = bpy.data.images.load(p); tiles.append(np.array(im.pixels[:]).reshape(h, w, 4))
    rows = [np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]; sh = np.vstack(rows[::-1])
    si = bpy.data.images.new(fname, sh.shape[1], sh.shape[0], alpha=True); si.pixels = sh.ravel().tolist()
    si.filepath_raw = os.path.join(out, fname + '.png'); si.file_format = 'PNG'; si.save()
sheet([24, 28, 32, 36, 40, 44, 90, 102], camA, 'v012_A')
sheet([205, 222, 240, 258, 272, 288, 304, 320], camB, 'v012_B')
sheet([401, 404, 406, 408, 410, 412, 416, 422], camC, 'v012_C')
sc.camera = camA; sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s01_camera_v012.blend'), copy=True)
result['ok'] = True
