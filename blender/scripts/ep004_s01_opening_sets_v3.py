# EP004 S01 module 2 (on top of v013): dashboard (O6), satellite over India (O7), code wall (SW), quartz bridge into S02 (Q).
# Each set lives in its own collection far from the phone; passes toggle collections. Preview-grade, generic (no brands).
# Map data: Natural Earth (public domain), via assets/references/geo_naturalearth_compact.json  (schematic, labelled as such).
import bpy, bmesh, math, os, json, random, tempfile, numpy as np
from mathutils import Vector
sc = bpy.context.scene; O = bpy.data.objects
random.seed(11)

# ---- fixes from the module-1 sheets ----
for mk_ in list(sc.timeline_markers): sc.timeline_markers.remove(mk_)           # markers overrode the per-shot cameras on other frame ranges
bpy.data.materials['table_dark'].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.62   # soften the softbox glare
for who, last in (('CAM_S01_B_dive', 320), ('CAM_S01_C_wafer', 401)):
    mt_ = bpy.data.materials['label_text_' + who].node_tree.nodes['Principled BSDF']; mp_ = bpy.data.materials['label_plate_' + who].node_tree.nodes['Principled BSDF']
    if who == 'CAM_S01_B_dive':                                                       # label stays through the end of B, then C continues it
        for f in (314, 320): mt_.inputs['Emission Strength'].default_value = 3.0; mt_.inputs['Emission Strength'].keyframe_insert('default_value', frame=f); mp_.inputs['Alpha'].default_value = 0.6; mp_.inputs['Alpha'].keyframe_insert('default_value', frame=f); mt_.inputs['Alpha'].default_value = 1.0; mt_.inputs['Alpha'].keyframe_insert('default_value', frame=f)
    else:                                                                             # C label: off before the shot (was ghosting into B), fades out at 405-410
        for f, v, a in ((380, 0.0, 0.0), (400, 0.0, 0.0), (401, 3.0, 0.6), (405, 3.0, 0.6), (410, 0.0, 0.0)):
            mt_.inputs['Emission Strength'].default_value = v; mt_.inputs['Emission Strength'].keyframe_insert('default_value', frame=f); mp_.inputs['Alpha'].default_value = a; mp_.inputs['Alpha'].keyframe_insert('default_value', frame=f); mt_.inputs['Alpha'].default_value = 1.0 if v > 0 else 0.0; mt_.inputs['Alpha'].keyframe_insert('default_value', frame=f)
for nd in bpy.data.materials['wafer_die_tiles'].node_tree.nodes:
    if nd.type == 'MATH' and nd.operation == 'MULTIPLY' and abs(nd.inputs[1].default_value - 38.0) < 1e-3: nd.inputs[1].default_value = 20.0      # gentler rainbow across the wafer
def bf(n): return n - 527
def col(name):
    c = bpy.data.collections.get(name)
    if not c: c = bpy.data.collections.new(name); sc.collection.children.link(c)
    return c
cc = col('05_CAMERAS')
def euler_for(pos, tgt, prev):
    d = Vector(tgt) - Vector(pos); d.normalize(); rx = math.acos(max(-1.0, min(1.0, -d.z)))
    rz = math.atan2(-d.x, d.y) if math.hypot(d.x, d.y) > 1e-4 else prev
    while rz - prev > math.pi: rz -= 2*math.pi
    while rz - prev < -math.pi: rz += 2*math.pi
    return (rx, 0.0, rz)
def make_cam(name, lens, keys, prev=0.0):
    d = bpy.data.cameras.new(name); d.lens = lens; d.sensor_width = 36; d.clip_start = 0.01; d.clip_end = 5000
    o = bpy.data.objects.new(name, d); cc.objects.link(o)
    for f, pos, tgt in keys:
        e = euler_for(pos, tgt, prev); prev = e[2]; o.location = pos; o.rotation_euler = e
        o.keyframe_insert('location', frame=f); o.keyframe_insert('rotation_euler', frame=f)
    return o
def emit(name, color, strength, base=(0, 0, 0), rough=0.5, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1); b.inputs['Emission Color'].default_value = (*color, 1); b.inputs['Emission Strength'].default_value = strength
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal; return m
def key_em(m, frames_vals):
    b = m.node_tree.nodes['Principled BSDF']
    for f, v in frames_vals: b.inputs['Emission Strength'].default_value = v; b.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)
def mesh_obj(name, bm, mat, c, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); o.location = loc; c.objects.link(o); return o
def box_bm(sx, sy, sz):
    bm = bmesh.new(); r = bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=r['verts']); return bm
def text_obj(s, size, loc, mat, c, parent=None, align='CENTER'):
    cu = bpy.data.curves.new('t', 'FONT'); cu.body = s; cu.size = size; cu.align_x = align; cu.align_y = 'CENTER'; cu.materials.append(mat)
    o = bpy.data.objects.new('t', cu); o.location = loc; c.objects.link(o)
    if parent: o.parent = parent
    return o

# =====================  O6: car dashboard (n 271-322, Blender frames bf(n))  =====================
dc = col('10_DASH'); D = Vector((2000, 0, 0))
root = bpy.data.objects.new('dash_root', None); root.location = D; root.rotation_euler = (math.pi/2, 0, 0); dc.objects.link(root)    # build in XY, faces -Y
panel = mesh_obj('dash_panel', box_bm(96, 40, 3), emit('dash_panel', (0, 0, 0), 0, (0.01, 0.011, 0.014), 0.5), dc); panel.parent = root; panel.location = (0, 0, -1.6)
m_tick = emit('dash_tick', (0.5, 0.85, 1.0), 0.0); m_num = emit('dash_num', (0.8, 0.92, 1.0), 0.0); m_need = emit('dash_needle', (1.0, 0.35, 0.1), 0.0); m_face = emit('dash_face', (0.2, 0.35, 0.55), 0.0, (0.008, 0.01, 0.014))
m_rim = emit('dash_rim', (0.6, 0.7, 0.8), 0.0, (0.05, 0.055, 0.06), 0.25, 1.0)
for m, v in ((m_tick, 2.5), (m_num, 2.2), (m_need, 4.0), (m_face, 0.35)): key_em(m, [(bf(271), 0.0), (bf(288), 0.0), (bf(294), v)])
def ann(r_out, r_in, seg=64):
    bm = bmesh.new(); A = [bm.verts.new((r_out*math.cos(2*math.pi*i/seg), r_out*math.sin(2*math.pi*i/seg), 0)) for i in range(seg)]
    B = [bm.verts.new((r_in*math.cos(2*math.pi*i/seg), r_in*math.sin(2*math.pi*i/seg), 0)) for i in range(seg)]
    for i in range(seg): j = (i+1) % seg; bm.faces.new((A[i], A[j], B[j], B[i]))
    return bm
needles = []
for cx, vmax, label in ((-17, 8, 'x1000 RPM'), (17, 12, 'km/h')):
    rim = mesh_obj('dial_rim', ann(9.6, 8.9), m_rim, dc); rim.parent = root; rim.location = (cx, 0, 0.1)
    bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=True, radius=8.9, segments=64)
    face = mesh_obj('dial_face', bm, m_face, dc); face.parent = root; face.location = (cx, 0, 0.05)
    for i in range(vmax*2 + 1):
        a = math.radians(225 - 270*i/(vmax*2)); big = (i % 2 == 0)
        t = mesh_obj('tick', box_bm(0.16 if big else 0.08, 1.1 if big else 0.55, 0.1), m_tick, dc); t.parent = root
        t.location = (cx + 7.9*math.cos(a), 7.9*math.sin(a), 0.12); t.rotation_euler.z = a - math.pi/2
        if big:
            n_ = text_obj(str(i//2 if vmax == 8 else (i//2)*20), 0.75, (cx + 6.1*math.cos(a), 6.1*math.sin(a), 0.12), m_num, dc, root)
    text_obj(label, 0.55, (cx, -3.2, 0.12), m_num, dc, root)
    piv = bpy.data.objects.new('needle_pivot', None); dc.objects.link(piv); piv.parent = root; piv.location = (cx, 0, 0.2)
    nd = mesh_obj('needle', box_bm(0.2, 7.2, 0.12), m_need, dc); nd.parent = piv; nd.location = (0, 3.6, 0)
    hub = bpy.data.objects.new('hub', None)
    needles.append((piv, vmax))
for piv, vmax in needles:                                  # self-test sweep then idle
    rest = math.radians(135)                               # pointing to 0 mark (225 deg minus 90)
    for f, ang in ((bf(271), rest), (bf(290), rest), (bf(297), rest - math.radians(270)), (bf(304), rest - math.radians(24 if vmax == 8 else 0)), (bf(322), rest - math.radians(22 if vmax == 8 else 0))):
        piv.rotation_euler.z = ang; piv.keyframe_insert('rotation_euler', index=2, frame=f)
warn_c = [(1.0, 0.15, 0.1), (1.0, 0.6, 0.1), (0.2, 0.9, 0.4), (1.0, 0.15, 0.1), (1.0, 0.6, 0.1)]
for i, c in enumerate(warn_c):
    m = emit(f'warn{i}', c, 0.0); key_em(m, [(bf(271), 0.0), (bf(287), 0.0), (bf(288), 4.5), (bf(305), 4.5), (bf(307), 0.0)])
    bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=True, radius=0.7, segments=24); w = mesh_obj('warn', bm, m, dc); w.parent = root; w.location = (-5 + i*2.5, 9.5, 0.12)
m_ready = emit('ready', (0.3, 1.0, 0.5), 0.0); key_em(m_ready, [(bf(271), 0.0), (bf(307), 0.0), (bf(309), 4.0)]); text_obj('READY', 1.3, (0, 0.5, 0.12), m_ready, dc, root)
camO6 = make_cam('CAM_O6', 40, [(bf(271), D + Vector((-7, -64, 3)), D + Vector((0, 0, 1))), (bf(322), D + Vector((-2, -46, 1.5)), D + Vector((0, 0, 0.5)))])

# =====================  O7: satellite over India (n 322-404)  =====================
ec = col('11_EARTH'); E = Vector((4000, 0, 0)); R = 60.0
geo = json.load(open(list(inputs.values())[0], encoding='utf8')) if False else None
GEO = json.load(open(inputs['geo.json'], encoding='utf8'))
W_, H_ = 2048, 1024
img = np.zeros((H_, W_, 3), dtype=np.float32); img[:, :] = (0.004, 0.012, 0.03)
def px(lon, lat): return (np.clip(((np.asarray(lon) + 180) / 360 * (W_ - 1)).astype(int), 0, W_ - 1), np.clip(((90 - np.asarray(lat)) / 180 * (H_ - 1)).astype(int), 0, H_ - 1))
def draw_ring(ring, c, wd=1):
    pts = np.array(ring, dtype=float)
    for a, b in zip(pts[:-1], pts[1:]):
        if abs(a[0] - b[0]) > 180: continue
        n = int(max(abs(a[0] - b[0]), abs(a[1] - b[1])) * 12) + 2; t = np.linspace(0, 1, n)
        x, y = px(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        for dx in range(-wd, wd + 1):
            for dy in range(-wd, wd + 1): img[np.clip(y + dy, 0, H_ - 1), np.clip(x + dx, 0, W_ - 1)] = np.maximum(img[np.clip(y + dy, 0, H_ - 1), np.clip(x + dx, 0, W_ - 1)], c)
for r_ in GEO['world']: draw_ring(r_, (0.05, 0.16, 0.30), 0)
for r_ in GEO['india']: draw_ring(r_, (0.95, 0.55, 0.15), 1)
def blob(lon, lat, rad, c):
    x, y = px(lon, lat); yy, xx = np.ogrid[-rad:rad + 1, -rad:rad + 1]; g = np.exp(-(xx**2 + yy**2) / (rad * rad / 2.2))[..., None] * np.array(c, dtype=np.float32)
    ys, xs = slice(max(int(y) - rad, 0), min(int(y) + rad + 1, H_)), slice(max(int(x) - rad, 0), min(int(x) + rad + 1, W_))
    sub = g[(ys.start - (int(y) - rad)):(g.shape[0] - ((int(y) + rad + 1) - ys.stop)), (xs.start - (int(x) - rad)):(g.shape[1] - ((int(x) + rad + 1) - xs.stop))]
    img[ys, xs] = np.minimum(img[ys, xs] + sub, 1.5)
for lon, lat, pop in GEO['cities']: blob(lon, lat, 4, (0.9, 0.8, 0.55))
for lon, lat, pop, nm in GEO['indian_cities']: blob(lon, lat, 6 if pop > 3e6 else 4, (1.0, 0.75, 0.3))
im = bpy.data.images.new('earth_night', W_, H_, alpha=False); rgba = np.dstack([img, np.ones((H_, W_), dtype=np.float32)])[::-1]
im.pixels = rgba.ravel().tolist(); im.pack()
def sph(lon, lat, r):
    lo, la = math.radians(lon), math.radians(lat); return E + Vector((r*math.cos(la)*math.cos(lo), r*math.cos(la)*math.sin(lo), r*math.sin(la)))
bm = bmesh.new(); uv = bm.loops.layers.uv.new('UVMap'); NLA, NLO = 48, 96; grid = {}
for i in range(NLA + 1):
    for j in range(NLO + 1):
        lat = -90 + 180*i/NLA; lon = -180 + 360*j/NLO; grid[(i, j)] = bm.verts.new(sph(lon, lat, R) - E)
for i in range(NLA):
    for j in range(NLO):
        f = bm.faces.new((grid[(i, j)], grid[(i, j+1)], grid[(i+1, j+1)], grid[(i+1, j)]))
        for l, (ii, jj) in zip(f.loops, ((i, j), (i, j+1), (i+1, j+1), (i+1, j))): l[uv].uv = (jj/NLO, ii/NLA)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
em = bpy.data.materials.new('earth_night_mat'); em.use_nodes = True; nt = em.node_tree; b = nt.nodes['Principled BSDF']
tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = im; tx.interpolation = 'Linear'
nt.links.new(tx.outputs['Color'], b.inputs['Emission Color']); nt.links.new(tx.outputs['Color'], b.inputs['Base Color']); b.inputs['Emission Strength'].default_value = 1.7; b.inputs['Roughness'].default_value = 0.9
earth = mesh_obj('earth', bm, em, ec, E)
bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=R * 1.022)
am = bpy.data.materials.new('atmos'); am.use_nodes = True; an = am.node_tree.nodes; al = am.node_tree.links
for n_ in list(an): an.remove(n_)
lw = an.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.25; emn = an.new('ShaderNodeEmission'); emn.inputs['Color'].default_value = (0.25, 0.55, 1.0, 1); emn.inputs['Strength'].default_value = 3.0
tr = an.new('ShaderNodeBsdfTransparent'); mxs = an.new('ShaderNodeMixShader'); outn = an.new('ShaderNodeOutputMaterial')
al.new(lw.outputs['Fresnel'], mxs.inputs[0]); al.new(tr.outputs[0], mxs.inputs[1]); al.new(emn.outputs[0], mxs.inputs[2]); al.new(mxs.outputs[0], outn.inputs['Surface'])
atm = mesh_obj('atmosphere', bm, am, ec, E)
sat_body = emit('sat_body', (0.9, 0.9, 0.95), 0.0, (0.55, 0.57, 0.6), 0.3, 1.0); sat_panel = emit('sat_panel', (0.1, 0.25, 0.7), 0.35, (0.02, 0.05, 0.2), 0.25, 0.8); sat_led = emit('sat_led', (0.3, 1.0, 0.6), 6.0)
sat = bpy.data.objects.new('sat', None); ec.objects.link(sat)
for nm, sz, loc, mt in (('body', (2.6, 1.6, 1.6), (0, 0, 0), sat_body), ('panelL', (0.1, 5.5, 1.8), (0, 4.4, 0), sat_panel), ('panelR', (0.1, 5.5, 1.8), (0, -4.4, 0), sat_panel), ('dish', (0.8, 0.8, 0.2), (1.6, 0, 0), sat_body), ('led', (0.3, 0.3, 0.3), (1.35, 0.5, 0.9), sat_led)):
    p = mesh_obj('sat_' + nm, box_bm(*sz), mt, ec); p.parent = sat; p.location = loc
sat.scale = (0.5, 0.5, 0.5)
def lonlat_at(n):
    t = (n - 322) / 82.0; t = t*t*(3 - 2*t)*0.35 + t*0.65; return 52 + 48*t, 23.0
camkeys = []
for n in range(322, 405, 6):
    lo, la = lonlat_at(n); sat.location = sph(lo, la, R + 8)
    sat.rotation_euler = (0, 0, math.radians(lo) + math.pi/2*0)         # roughly nadir-facing; preview-grade
    sat.keyframe_insert('location', frame=bf(n)); sat.keyframe_insert('rotation_euler', frame=bf(n))
    camkeys.append((bf(n), sph(lo - 21, la - 12, R + 38), sph(lo + 7, la - 1, R * 0.99)))
camO7 = make_cam('CAM_O7', 35, camkeys)
city = sorted(GEO['indian_cities'], key=lambda z: -z[2])[:8]
beam_m = emit('beam', (1.0, 0.7, 0.25), 7.0)
for i, (lon, lat, pop, nm) in enumerate(city):
    n0 = 350 + i*5; lo, la = lonlat_at(n0); a = sph(lo, la, R + 8); bpt = sph(lon, lat, R); L = (bpt - a).length
    bm = bmesh.new(); r_ = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.12, radius2=0.12, depth=L); bmesh.ops.translate(bm, vec=(0, 0, L/2), verts=r_['verts'])
    bo = mesh_obj('beam', bm, beam_m, ec, a); bo.rotation_euler = (bpt - a).to_track_quat('Z', 'Y').to_euler()
    for f, v in ((bf(322), True), (bf(n0), False), (bf(n0 + 14), True)): bo.hide_render = v; bo.keyframe_insert('hide_render', frame=f)

# =====================  SW: code wall (n 629-714)  =====================
kc = col('12_CODE'); K = Vector((6000, 0, 0))
toks = ['def', 'return', 'for', 'in', 'import', 'class', 'async', 'await', 'yield', 'with', 'lambda', 'try']
ids = ['render_frame', 'compile_model', 'ship_build', 'load_user', 'sync_payments', 'tokenize', 'infer', 'cache_get', 'queue_job', 'merge_tree', 'deploy', 'router', 'batch', 'encode']
colors = [(0.35, 0.8, 1.0), (1.0, 0.75, 0.3), (0.85, 0.9, 1.0), (0.4, 1.0, 0.6), (0.75, 0.5, 1.0)]
scroll = bpy.data.objects.new('code_scroll', None); scroll.location = K; kc.objects.link(scroll)
for ln in range(46):
    ind = random.choice((0, 0, 4, 8, 8, 12)); s_ = ' ' * ind + f"{random.choice(toks)} {random.choice(ids)}({random.choice(ids)}, {random.randint(0, 9999)}):"
    if random.random() < 0.35: s_ = ' ' * ind + f"{random.choice(ids)} = {random.choice(ids)}[{random.randint(0, 255)}]  # ok"
    col_ = random.choice(colors); m = emit(f'code{ln}', col_, random.uniform(1.2, 2.4))
    to_ = text_obj(s_, 0.95, (-10, 0, 24 - ln*1.15), m, kc, scroll, 'LEFT'); to_.rotation_euler = (math.pi/2, 0, 0)
for f, z in ((bf(629), 0.0), (bf(714), 11.0)): scroll.location = K + Vector((0, 0, z)); scroll.keyframe_insert('location', frame=f + 5000 - 5000)
mp = bmesh.new(); bmesh.ops.create_grid(mp, x_segments=1, y_segments=1, size=0.5); bmesh.ops.scale(mp, vec=(34, 17, 1), verts=mp.verts); bmesh.ops.rotate(mp, cent=(0, 0, 0), matrix=__import__('mathutils').Matrix.Rotation(math.pi/2, 3, 'X'), verts=mp.verts)
mm = bpy.data.materials.new('map_plane'); mm.use_nodes = True; mb = mm.node_tree.nodes['Principled BSDF']; mt_ = mm.node_tree.nodes.new('ShaderNodeTexImage'); mt_.image = im
gc_ = mm.node_tree.nodes.new('ShaderNodeTexCoord'); mm.node_tree.links.new(gc_.outputs['Generated'], mt_.inputs['Vector'])
mm.node_tree.links.new(mt_.outputs['Color'], mb.inputs['Emission Color']); mb.inputs['Emission Strength'].default_value = 2.6; mb.inputs['Base Color'].default_value = (0, 0, 0, 1)
mapo = mesh_obj('map_plane', mp, mm, kc, K + Vector((30, 6, -3)))
camSW = make_cam('CAM_SW', 40, [(bf(629), K + Vector((-4, -44, 4)), K + Vector((8, 0, 0))), (bf(714), K + Vector((3, -36, 2)), K + Vector((10, 0, -1)))])

# =====================  Q: quartz bridge into S02 (n 870-979)  =====================
qc = col('13_QUARTZ'); Q = Vector((0, 300, 0))     # near the origin: label glyphs are ~0.001 and float precision at 8000 units broke them
glass = bpy.data.materials.new('quartz'); glass.use_nodes = True; gb = glass.node_tree.nodes['Principled BSDF']
gb.inputs['Base Color'].default_value = (0.92, 0.94, 0.98, 1); gb.inputs['Transmission Weight'].default_value = 1.0; gb.inputs['Roughness'].default_value = 0.07; gb.inputs['IOR'].default_value = 1.54
for i, (dx, dy, tilt, yaw, r, h) in enumerate(((0, 0, 8, 10, 1.3, 6.5), (2.4, 1.0, -18, 40, 1.0, 5.0), (-2.2, 0.8, 22, -30, 1.1, 5.6), (1.0, -1.8, 30, 80, 0.8, 3.8), (-1.2, -1.9, -26, 130, 0.7, 3.2), (3.6, -0.6, -35, 20, 0.6, 2.6), (-3.6, -0.4, 38, -60, 0.65, 2.9))):
    bm = bmesh.new(); a = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=r, radius2=r, depth=h); bmesh.ops.translate(bm, vec=(0, 0, h/2), verts=a['verts'])
    t = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=r, radius2=0.12*r, depth=r*1.1); bmesh.ops.translate(bm, vec=(0, 0, h + r*0.55), verts=t['verts'])
    c_ = mesh_obj('quartz', bm, glass, qc, Q + Vector((dx, dy, 0))); c_.rotation_euler = (math.radians(tilt), math.radians(tilt*0.4), math.radians(yaw))
qt = bmesh.new(); bmesh.ops.create_grid(qt, x_segments=1, y_segments=1, size=60.0); mesh_obj('quartz_table', qt, emit('qtable', (0, 0, 0), 0, (0.012, 0.013, 0.016), 0.28), qc, Q + Vector((0, 0, -0.02)))
def qlight(name, loc, energy, size, color, keyf):
    d = bpy.data.lights.new(name, 'AREA'); d.size = size; d.color = color
    for f, v in keyf: d.energy = v; d.keyframe_insert('energy', frame=f)
    o = bpy.data.objects.new(name, d); o.location = Q + Vector(loc); qc.objects.link(o)
    o.rotation_euler = (Q + Vector((0, 0, 3)) - o.location).to_track_quat('-Z', 'Y').to_euler(); return o
qf = [(5000, 0.0), (5009, 0.0), (5016, 1.0)]
qlight('q_key', (-14, -18, 16), 1, 9, (1.0, 0.95, 0.88), [(f, v*5200) for f, v in qf]); qlight('q_rim', (12, 20, 9), 1, 8, (0.55, 0.85, 1.0), [(f, v*4200) for f, v in qf]); qlight('q_top', (0, -2, 22), 1, 12, (0.9, 0.95, 1.0), [(f, v*1800) for f, v in qf])
camQ = make_cam('CAM_Q', 50, [(5000, Q + Vector((-1.4, -2.3, 2.2)), Q + Vector((0.2, 0, 2.6))), (5108, Q + Vector((-11, -17, 8.5)), Q + Vector((0, 0, 3.2)))])
def qlabel(cam, text, d=0.05, y=-0.0075):
    cu = bpy.data.curves.new('lbl_Q', 'FONT'); cu.body = text; cu.size = 0.0011; cu.align_x = 'CENTER'; cu.space_character = 1.1
    t = bpy.data.objects.new('label_Q', cu); qc.objects.link(t); t.parent = cam; t.location = (0, y, -d)
    mt = bpy.data.materials.new('label_text_Q'); mt.use_nodes = True; bt = mt.node_tree.nodes['Principled BSDF']
    bt.inputs['Base Color'].default_value = (0, 0, 0, 1); bt.inputs['Emission Color'].default_value = (0.9, 0.95, 1.0, 1); cu.materials.append(mt)
    bmq = bmesh.new(); bmesh.ops.create_grid(bmq, x_segments=1, y_segments=1, size=0.5); pme = bpy.data.meshes.new('lblplateQ'); bmq.to_mesh(pme); bmq.free()
    pl = bpy.data.objects.new('labelplate_Q', pme); qc.objects.link(pl); pl.parent = cam; pl.location = (0, y + 0.0004, -d - 0.0001); pl.scale = (0.0095, 0.0032, 1)
    mp = bpy.data.materials.new('label_plate_Q'); mp.use_nodes = True; bp = mp.node_tree.nodes['Principled BSDF']; bp.inputs['Base Color'].default_value = (0.01, 0.012, 0.016, 1); pme.materials.append(mp)
    for f, vt, vp in ((5000, 0.0, 0.0), (5028, 0.0, 0.0), (5038, 3.0, 0.6), (5090, 3.0, 0.6), (5102, 0.0, 0.0)):
        bt.inputs['Emission Strength'].default_value = vt; bt.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)
        bp.inputs['Alpha'].default_value = vp; bp.inputs['Alpha'].keyframe_insert('default_value', frame=f)
        bt.inputs['Alpha'].default_value = 1.0 if vt > 0 else 0.0; bt.inputs['Alpha'].keyframe_insert('default_value', frame=f)
    for o_ in (t, pl): o_.visible_glossy = o_.visible_diffuse = o_.visible_transmission = o_.visible_shadow = False
qlabel(camQ, 'SILICON')
camQ.data.clip_start = 0.0004

# =====================  sheets  =====================
gpu(sc, 'auto'); sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.use_denoising = True
tmp = tempfile.mkdtemp()
ALL = ('08_OPEN_SET', '09_OPEN_UI', '10_DASH', '11_EARTH', '12_CODE', '13_QUARTZ', '06_WAFER')
def setpass(show):
    for c in ALL: bpy.data.collections[c].hide_render = c not in show
def sheet(items, fname, w=480, h=270):
    sc.render.resolution_x, sc.render.resolution_y = w, h; tiles = []
    for cam, f, show in items:
        setpass(show); sc.camera = cam; sc.frame_set(f); p = os.path.join(tmp, f'{fname}_{f}.png'); sc.render.filepath = p
        bpy.ops.render.render(write_still=True); imx = bpy.data.images.load(p); tiles.append(np.array(imx.pixels[:]).reshape(h, w, 4))
    rows = [np.hstack(tiles[i:i+4]) for i in range(0, len(tiles), 4)]; sh = np.vstack(rows[::-1])
    si = bpy.data.images.new(fname, sh.shape[1], sh.shape[0], alpha=True); si.pixels = sh.ravel().tolist(); si.filepath_raw = os.path.join(out, fname + '.png'); si.file_format = 'PNG'; si.save()
sheet([(camO6, bf(274), ('10_DASH',)), (camO6, bf(292), ('10_DASH',)), (camO6, bf(300), ('10_DASH',)), (camO6, bf(314), ('10_DASH',)),
       (camO7, bf(326), ('11_EARTH',)), (camO7, bf(352), ('11_EARTH',)), (camO7, bf(380), ('11_EARTH',)), (camO7, bf(402), ('11_EARTH',))], 'm2_a')
sheet([(camSW, bf(631), ('12_CODE',)), (camSW, bf(660), ('12_CODE',)), (camSW, bf(700), ('12_CODE',)),
       (camQ, 5000, ('13_QUARTZ',)), (camQ, 5014, ('13_QUARTZ',)), (camQ, 5040, ('13_QUARTZ',)), (camQ, 5070, ('13_QUARTZ',)), (camQ, 5108, ('13_QUARTZ',))], 'm2_b')
setpass(()); sc.camera = O['CAM_S01_A_pushthrough']; sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s01_camera_v014.blend'), copy=True)
result['ok'] = True
