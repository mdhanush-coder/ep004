# EP004 S02 "From Quartz to a Chip": first-pass build on top of the S01 studio (v018). Preview-grade geometry, labelled illustrative.
# S02 frame f = 20000 + (n - 979), n = preview frame at 24 fps from the start of the video (the quartz bridge already played 36.25-40.79 s).
# Beats are locked to the approved narration word times (production/research/s02-quartz-to-chip.md).
import bpy, bmesh, math, os, random, time, tempfile, numpy as np
from mathutils import Vector
sc = bpy.context.scene; M = bpy.data.materials; O = bpy.data.objects
random.seed(21); SX, SY = 0.8, 4.6
def f2(n): return 20000 + n - 979
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
def make_cam(name, lens, keys, clip=0.01):
    d = bpy.data.cameras.new(name); d.lens = lens; d.sensor_width = 36; d.clip_start = clip; d.clip_end = 3000
    o = bpy.data.objects.new(name, d); cc.objects.link(o); prev = 0.0
    for n, pos, tgt in keys:
        e = euler_for(pos, tgt, prev); prev = e[2]; o.location = pos; o.rotation_euler = e
        o.keyframe_insert('location', frame=f2(n)); o.keyframe_insert('rotation_euler', frame=f2(n))
    return o
def em(name, color, strength, base=(0, 0, 0), rough=0.5, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1); b.inputs['Emission Color'].default_value = (*color, 1); b.inputs['Emission Strength'].default_value = strength
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal; return m
def key_em(m, kv):
    b = m.node_tree.nodes['Principled BSDF']
    for n, v in kv: b.inputs['Emission Strength'].default_value = v; b.inputs['Emission Strength'].keyframe_insert('default_value', frame=f2(n))
def obj(name, bm, mat, c, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); o.location = loc; c.objects.link(o); return o
def box(sx, sy, sz):
    bm = bmesh.new(); r = bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=r['verts']); return bm
def cyl(r, depth, seg=48, r2=None, caps=True):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=caps, segments=seg, radius1=r, radius2=(r if r2 is None else r2), depth=depth); return bm
def light(name, loc, energy, size, color, c, tgt=(0, 0, 0), keys=None, shape='AREA'):
    d = bpy.data.lights.new(name, 'AREA'); d.size = size; d.color = color
    for n, v in (keys or [(0, energy)]): d.energy = v; d.keyframe_insert('energy', frame=f2(n))
    o = bpy.data.objects.new(name, d); o.location = loc; c.objects.link(o)
    o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
def ground(c, base, z, rough=0.3, size=200.0):
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size); return obj('ground', bm, em('ground', (0, 0, 0), 0, base, rough), c, (0, 0, z))
# beat boundaries (preview frames n)
B = dict(b1=(979, 1083), b2=(1083, 1176), b3=(1176, 1231), b4=(1231, 1279), b5=(1279, 1301), b6=(1301, 1385), b7=(1385, 1498), b8=(1498, 1534), b9=(1534, 1634), b10=(1634, 1794))
cams = {}

# ---------- b1 sand -> arc furnace ----------
c1 = col('S2_SAND'); o1 = Vector((0, 600, 0)); ground(c1, (0.01, 0.01, 0.012), 0).location = o1
bm = bmesh.new()
for _ in range(520):
    r = 11 * math.sqrt(random.random()); a = random.uniform(0, 6.283); h = max(0.0, 5.5 * (1 - r / 11.5)) * random.uniform(0.3, 1.0)
    s = random.uniform(0.28, 0.55); g = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=s)
    bmesh.ops.translate(bm, vec=(r * math.cos(a), r * math.sin(a), h + s * 0.6), verts=g['verts'])
sand = obj('sand', bm, em('sand', (1.0, 0.45, 0.12), 0.0, (0.55, 0.45, 0.3), 0.9), c1, o1)
key_em(sand.data.materials[0], [(980, 0.0), (1030, 0.0), (1075, 1.4)])           # grains heat up under the arc
for sx_ in (-1, 1):
    obj('electrode', cyl(0.9, 9, 24), em('graphite', (0, 0, 0), 0, (0.02, 0.02, 0.025), 0.5), c1, o1 + Vector((sx_ * 7, 0, 8.5))).rotation_euler = (0, math.pi/2, 0)
arc = obj('arc', cyl(0.5, 5, 12), em('arc', (0.7, 0.85, 1.0), 0.0), c1, o1 + Vector((0, 0, 8.5))); arc.rotation_euler = (0, math.pi/2, 0)
key_em(arc.data.materials[0], [(979, 0.0), (1040, 0.0), (1046, 90.0), (1060, 40.0), (1068, 110.0), (1083, 70.0)])
light('arc_light', tuple(o1 + Vector((0, 0, 11))), 1, 6, (1.0, 0.7, 0.4), c1, tuple(o1), [(979, 0), (1040, 0), (1046, 60000), (1083, 90000)])
light('sand_key', tuple(o1 + Vector((-18, -22, 14))), 5000, 12, (0.8, 0.85, 1.0), c1, tuple(o1))
cams['b1'] = make_cam('CAM_S2_b1', 32, [(979, o1 + Vector((-17, -24, 7)), o1 + Vector((0, 0, 4.5))), (1083, o1 + Vector((-11, -16, 8.5)), o1 + Vector((0, 0, 6.5)))])

# ---------- b2 polysilicon ----------
c2 = col('S2_POLY'); o2 = Vector((0, 700, 0)); ground(c2, (0.012, 0.012, 0.015), 0, 0.25).location = o2
mp = em('poly', (0, 0, 0), 0, (0.6, 0.62, 0.68), 0.22, 1.0)
for i in range(46):
    bm = bmesh.new(); g = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=random.uniform(1.4, 3.0))
    for v in bm.verts: v.co += Vector((random.uniform(-.5, .5), random.uniform(-.5, .5), random.uniform(-.5, .5)))
    a = random.uniform(0, 6.283); r = 9 * math.sqrt(random.random())
    obj('poly', bm, mp, c2, o2 + Vector((r * math.cos(a), r * math.sin(a), random.uniform(1.2, 4.0)))).rotation_euler = (random.random()*3, random.random()*3, random.random()*3)
light('poly_key', tuple(o2 + Vector((-14, -18, 14))), 1, 9, (1.0, 0.97, 0.92), c2, tuple(o2), [(1083, 4000), (1176, 9000)])
light('poly_rim', tuple(o2 + Vector((16, 14, 8))), 4500, 8, (0.55, 0.85, 1.0), c2, tuple(o2))
cams['b2'] = make_cam('CAM_S2_b2', 45, [(1083, o2 + Vector((-16, -22, 9)), o2 + Vector((0, 0, 2))), (1176, o2 + Vector((-9, -14, 6)), o2 + Vector((0, 0, 2.5)))])

# ---------- b3 Czochralski pull ----------
c3 = col('S2_CZ'); o3 = Vector((0, 800, 0)); ground(c3, (0.008, 0.008, 0.01), 0, 0.4).location = o3
obj('crucible', cyl(14, 12, 48, caps=False), em('crucible', (0, 0, 0), 0, (0.03, 0.03, 0.035), 0.45), c3, o3 + Vector((0, 0, 6)))
melt = obj('melt', cyl(13.2, 0.3, 48), em('melt', (1.0, 0.42, 0.08), 7.0), c3, o3 + Vector((0, 0, 9)))
root = bpy.data.objects.new('ingot_root', None); c3.objects.link(root); root.location = o3 + Vector((0, 0, 20)); root.rotation_mode = 'XYZ'
mi = em('ingot', (0, 0, 0), 0, (0.5, 0.52, 0.56), 0.3, 1.0)
neck = obj('neck', cyl(0.8, 6, 24), mi, c3); neck.parent = root; neck.location = (0, 0, 3)
sh = obj('shoulder', cyl(10, 5, 48, r2=0.8), mi, c3); sh.parent = root; sh.location = (0, 0, -2.5)
bd = obj('body', cyl(10, 30, 48), mi, c3); bd.parent = root; bd.location = (0, 0, -5); bd.scale = (1, 1, 0.01)
# body origin at its centre; keep its TOP at z=-5 by moving it down as it grows
for n, s in ((1176, 0.01), (1231, 1.0)):
    bd.scale = (1, 1, s); bd.location = (0, 0, -5 - 15 * s); bd.keyframe_insert('scale', frame=f2(n)); bd.keyframe_insert('location', frame=f2(n))
for n, z in ((1176, 20.0), (1231, 20.0 + 30.0)):
    root.location = o3 + Vector((0, 0, z)); root.keyframe_insert('location', frame=f2(n))
for n, a in ((1176, 0.0), (1231, 6.0)): root.rotation_euler.z = a; root.keyframe_insert('rotation_euler', index=2, frame=f2(n))
light('cz_rim', tuple(o3 + Vector((18, -20, 22))), 6000, 10, (0.7, 0.85, 1.0), c3, tuple(o3 + Vector((0, 0, 16))))
cams['b3'] = make_cam('CAM_S2_b3', 40, [(1176, o3 + Vector((-30, -42, 14)), o3 + Vector((0, 0, 17))), (1231, o3 + Vector((-27, -38, 20)), o3 + Vector((0, 0, 22)))])

# ---------- b4 wire saw ----------
c4 = col('S2_SLICE'); o4 = Vector((0, 900, 0)); ground(c4, (0.01, 0.01, 0.012), -14, 0.3).location = o4
md = em('disc', (0, 0, 0), 0, (0.5, 0.52, 0.56), 0.32, 1.0); discs = []
for i in range(14):
    d_ = obj('disc', cyl(10, 1.9, 64), md, c4, o4 + Vector((-14.3 + i * 2.2, 0, 0))); d_.rotation_euler = (0, math.pi/2, 0); discs.append(d_)
mw = em('wire', (1.0, 0.75, 0.3), 2.5, (0.8, 0.62, 0.3), 0.25, 1.0)
for i in range(15):
    w = obj('wire', box(0.14, 30, 0.14), mw, c4, o4 + Vector((-15.4 + i * 2.2, 0, 13)))
    for n, z in ((1231, 13.0), (1262, -11.0), (1279, -11.0)): w.location.z = o4.z + z; w.keyframe_insert('location', index=2, frame=f2(n))
for i, d_ in enumerate(discs):                                   # wafers fan out after the cut
    x0 = o4.x - 14.3 + i * 2.2
    for n, dx in ((1231, 0.0), (1262, 0.0), (1279, (i - 6.5) * 1.1)): d_.location.x = x0 + dx; d_.keyframe_insert('location', index=0, frame=f2(n))
light('sl_key', tuple(o4 + Vector((-22, -28, 20))), 8000, 12, (1.0, 0.97, 0.92), c4, tuple(o4)); light('sl_rim', tuple(o4 + Vector((20, 18, 10))), 5000, 8, (0.55, 0.85, 1.0), c4, tuple(o4))
cams['b4'] = make_cam('CAM_S2_b4', 40, [(1231, o4 + Vector((-34, -40, 8)), o4 + Vector((0, 0, 2))), (1279, o4 + Vector((-26, -34, 7)), o4 + Vector((0, 0, 1)))])

# ---------- b5 polished wafer ----------
c5 = col('S2_POLISH'); o5 = Vector((0, 1000, 0)); ground(c5, (0.006, 0.006, 0.008), -0.02, 0.15).location = o5
wm = em('wafer_mirror', (0, 0, 0), 0, (0.9, 0.92, 0.96), 0.02, 1.0)
wf = obj('polished_wafer', cyl(15, 0.8, 96), wm, c5, o5 + Vector((0, 0, 0.4)))
obj('notch', box(1.2, 0.9, 0.9), em('notch', (0, 0, 0), 0, (0.02, 0.02, 0.025), 0.5), c5, o5 + Vector((0, -15, 0.4)))
for n, a in ((1279, 0.0), (1301, 0.6)): wf.rotation_euler.z = a; wf.keyframe_insert('rotation_euler', index=2, frame=f2(n))
sl = bpy.data.lights.new('strip', 'AREA'); sl.shape = 'RECTANGLE'; sl.size = 60; sl.size_y = 2.5; sl.color = (1, 0.98, 0.95)
for n, x in ((1279, -45.0), (1301, 45.0)): sl.energy = 60000; sl.keyframe_insert('energy', frame=f2(n))
so = bpy.data.objects.new('strip', sl); c5.objects.link(so); so.rotation_euler = (math.radians(35), 0, 0)
for n, x in ((1279, -45.0), (1301, 45.0)): so.location = o5 + Vector((x, 22, 20)); so.keyframe_insert('location', frame=f2(n))
cams['b5'] = make_cam('CAM_S2_b5', 50, [(1279, o5 + Vector((-24, -34, 9)), o5 + Vector((0, -4, 0))), (1301, o5 + Vector((-16, -30, 8)), o5 + Vector((0, -6, 0)))])

# ---------- b7/b8 illustrative transistor (MOSFET as a switch) ----------
c7 = col('S2_FET'); o7 = Vector((0, 1100, 0)); ground(c7, (0.008, 0.009, 0.012), -3.2, 0.3).location = o7
obj('substrate', box(44, 26, 6), em('substrate', (0, 0, 0), 0, (0.16, 0.17, 0.2), 0.4, 0.4), c7, o7)
msrc = em('sd', (0.2, 0.5, 1.0), 0.6, (0.08, 0.2, 0.55), 0.35, 0.3)
obj('source', box(11, 16, 3.2), msrc, c7, o7 + Vector((-14, 0, 2.6))); obj('drain', box(11, 16, 3.2), msrc, c7, o7 + Vector((14, 0, 2.6)))
obj('oxide', box(13, 18, 0.7), em('oxide', (0, 0, 0), 0, (0.6, 0.65, 0.75), 0.15, 0.0), c7, o7 + Vector((0, 0, 3.55)))
mg = em('gate', (0.3, 0.9, 1.0), 0.0, (0.75, 0.78, 0.82), 0.2, 1.0)
obj('gate', box(13, 18, 3.4), mg, c7, o7 + Vector((0, 0, 5.6)))
ON = ((1385, 0.0), (1420, 0.0), (1428, 5.0), (1470, 5.0), (1478, 0.0), (1498, 0.0), (1503, 5.0), (1522, 5.0), (1528, 0.0))
key_em(mg, ON)
mch = em('channel', (0.3, 0.95, 1.0), 0.0); key_em(mch, ON); obj('channel', box(13, 16, 0.5), mch, c7, o7 + Vector((0, 0, 3.0)))
me_ = em('electron', (0.4, 1.0, 1.0), 9.0)
for i in range(16):
    e = obj('e', cyl(0.45, 0.9, 10), me_, c7, o7); e.hide_render = True
    for n0, n1 in ((1428, 1470), (1503, 1522)):
        t0 = n0 + i * 1.4;
        for k, (fr, x, h) in enumerate(((t0, -16.0, False), (min(t0 + 24, n1), 16.0, False), (min(t0 + 25, n1 + 1), 16.0, True))):
            e.location = o7 + Vector((x, random.uniform(-6, 6) if k == 0 else e.location.y - o7.y + o7.y, 3.2)); e.hide_render = h
            e.keyframe_insert('location', frame=f2(fr)); e.keyframe_insert('hide_render', frame=f2(fr))
light('fet_key', tuple(o7 + Vector((-30, -38, 30))), 20000, 16, (1.0, 0.97, 0.92), c7, tuple(o7)); light('fet_rim', tuple(o7 + Vector((28, 26, 14))), 9000, 12, (0.5, 0.8, 1.0), c7, tuple(o7))
cams['b7'] = make_cam('CAM_S2_b7', 40, [(1385, o7 + Vector((-45, -58, 28)), o7 + Vector((0, 0, 3))), (1498, o7 + Vector((-30, -44, 20)), o7 + Vector((0, 0, 4)))])
cams['b8'] = make_cam('CAM_S2_b8', 40, [(1498, o7 + Vector((-30, -44, 20)), o7 + Vector((0, 0, 4))), (1534, o7 + Vector((-24, -34, 16)), o7 + Vector((0, 0, 4)))])

# ---------- wafer / die shots reuse the S01 wafer, die and lattice (b6, b9, b10) ----------
for mn in ('wafer_die_tiles', 'wafer_silicon'):                  # b6: the die pattern is "created" outward from the hero die
    for nd in M[mn].node_tree.nodes:
        if nd.type == 'MATH' and nd.operation == 'LESS_THAN':
            for fr, v in ((f2(1300), 24.0), (f2(1301), 0.0), (f2(1370), 24.0)): nd.inputs[1].default_value = v; nd.inputs[1].keyframe_insert('default_value', frame=fr)
LAY = [O[f'die_M{k}'] for k in range(1, 7)]
for o in LAY:                                                    # b9: metal layers peeled so the lattice shows; restored for b10
    for fr, x in ((f2(1533), 0.0), (f2(1534), 1.6), (f2(1633), 1.6), (f2(1634), 0.0)): o.location.x = x; o.keyframe_insert('location', index=0, frame=fr)
def wafer_cam(name, lens, nkeys): return make_cam(name, lens, nkeys, clip=0.0004)
up = lambda z, dy=-0.3: (SX, SY + dy, z)
cams['b6'] = wafer_cam('CAM_S2_b6', 40, [(1301, up(-49), (SX, SY, 0.34)), (1329, up(-22), (SX, SY, 0.34)), (1353, up(-6), (SX, SY, 0.34)), (1371, up(-1.0, -0.02), (SX, SY, 0.34)), (1385, (SX - 0.004, SY - 0.006, 0.305), (SX, SY, 0.369))])
cams['b9'] = wafer_cam('CAM_S2_b9', 50, [(1534, (SX - 0.004, SY - 0.006, 0.305), (SX, SY, 0.369)), (1560, (SX - 0.28, SY - 0.4, -0.1), (SX, SY, 0.369)), (1590, up(-6), (SX, SY, 0.34)), (1634, up(-46), (SX, SY, 0.34))])
cams['b10'] = wafer_cam('CAM_S2_b10', 36, [(1634, up(-49), (SX, SY, 0.34)), (1700, up(-30), (SX, SY, 0.34)), (1760, up(-8), (SX, SY, 0.34)), (1794, up(-3.0, -0.05), (SX, SY, 0.34))])
ch = col('S2_HILITE'); mh = em('die_hilite', (0.3, 0.9, 1.0), 0.0, (0, 0, 0), 0.4); key_em(mh, [(1634, 0.0), (1664, 0.0), (1690, 9.0), (1794, 9.0)])
for (bx, by, sx_, sy_) in ((0, 0.56, 1.2, 0.05), (0, -0.56, 1.2, 0.05), (0.56, 0, 0.05, 1.2), (-0.56, 0, 0.05, 1.2)):
    h = obj('hilite', box(sx_, sy_, 0.01), mh, ch, Vector((SX + bx, SY + by, 0.3412)))
# label for the wafer / lattice shots (camera-parented, same recipe as S01) and for the FET set (scaled up)
def label(cam, text, s, keys):
    d = 0.05 * s; cu = bpy.data.curves.new('lbl', 'FONT'); cu.body = text; cu.size = 0.0011 * s; cu.align_x = 'CENTER'; cu.space_character = 1.1
    t = bpy.data.objects.new('lbl2_' + cam.name, cu); col('04_POP_SOC').objects.link(t); t.parent = cam; t.location = (0, -0.0075 * s, -d)
    mt = bpy.data.materials.new('l2t_' + cam.name); mt.use_nodes = True; bt = mt.node_tree.nodes['Principled BSDF']; bt.inputs['Base Color'].default_value = (0, 0, 0, 1); bt.inputs['Emission Color'].default_value = (0.9, 0.95, 1, 1); cu.materials.append(mt)
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5); pme = bpy.data.meshes.new('lp'); bm.to_mesh(pme); bm.free()
    pl = bpy.data.objects.new('lp2_' + cam.name, pme); col('04_POP_SOC').objects.link(pl); pl.parent = cam; pl.location = (0, (-0.0075 + 0.0004) * s, -d - 0.0001 * s); pl.scale = (0.0215 * s, 0.0032 * s, 1)
    mp = bpy.data.materials.new('l2p_' + cam.name); mp.use_nodes = True; bp = mp.node_tree.nodes['Principled BSDF']; bp.inputs['Base Color'].default_value = (0.01, 0.012, 0.016, 1); pme.materials.append(mp)
    keys = [(keys[0][0] - 1, 0.0, 0.0)] + list(keys)
    for n, vt, vp in keys:
        bt.inputs['Emission Strength'].default_value = vt; bt.inputs['Emission Strength'].keyframe_insert('default_value', frame=f2(n))
        bp.inputs['Alpha'].default_value = vp; bp.inputs['Alpha'].keyframe_insert('default_value', frame=f2(n)); bt.inputs['Alpha'].default_value = 1.0 if vt > 0 else 0.0; bt.inputs['Alpha'].keyframe_insert('default_value', frame=f2(n))
    for o_ in (t, pl): o_.visible_glossy = o_.visible_diffuse = o_.visible_transmission = o_.visible_shadow = False
label(cams['b7'], 'ILLUSTRATIVE · NOT TO SCALE', 20, [(1385, 0.0, 0.0), (1395, 3.0, 0.6), (1498, 3.0, 0.6)]); label(cams['b8'], 'ILLUSTRATIVE · NOT TO SCALE', 20, [(1498, 3.0, 0.6), (1534, 3.0, 0.6)])
label(cams['b9'], 'ILLUSTRATIVE · NOT TO SCALE', 1, [(1534, 3.0, 0.6), (1560, 3.0, 0.6), (1575, 0.0, 0.0)])

# ---------- generated-image plates (AI stills used as shots: arc furnace, polished wafer) ----------
cp = col('S2_PLATES')
def plate(name, key, o, cam_name, n0, n1, d0, d1, dx=0.0):
    img = bpy.data.images.load(inputs[key]); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0, 0, 0, 1)
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = img; tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Generated'], t.inputs['Vector']); nt.links.new(t.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = 1.0; me.materials.append(m)
    p = bpy.data.objects.new(name, me); cp.objects.link(p); p.location = o; p.rotation_euler = (math.pi / 2, 0, 0); p.scale = (17.78, 10.0, 1)
    cam = make_cam(cam_name, 50, [(n0, o + Vector((0, -d0, 0)), o), (n1, o + Vector((dx, -d1, 0)), o + Vector((dx, 0, 0)))]); return cam
cams['p1'] = plate('plate_furnace', 'furnace', Vector((0, 1200, 0)), 'CAM_S2_p1', 1030, 1083, 25.5, 23.0, 0.0)
cams['p5'] = plate('plate_wafer', 'wafer', Vector((0, 1300, 0)), 'CAM_S2_p5', 1279, 1301, 25.5, 22.8, 0.0)

# ---------- preview render (segments passed in args) ----------
gpu(sc, 'auto'); sc.render.engine = 'CYCLES'; sc.cycles.samples = 16; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 640, 360, 100; sc.render.fps = 24; sc.render.use_motion_blur = False
try: sc.render.image_settings.media_type = 'VIDEO'
except Exception as e: result['media_type_note'] = str(e)
sc.render.image_settings.file_format = 'FFMPEG'; ff = sc.render.ffmpeg; ff.format = 'MPEG4'; ff.codec = 'H264'; ff.constant_rate_factor = 'MEDIUM'; ff.audio_codec = 'NONE'
SETS = ('S2_SAND', 'S2_POLY', 'S2_CZ', 'S2_SLICE', 'S2_POLISH', 'S2_FET', 'S2_HILITE', 'S2_PLATES', '08_OPEN_SET', '09_OPEN_UI', '10_DASH', '11_EARTH', '12_CODE', '13_QUARTZ', '06_WAFER')
W = ('06_WAFER',)
SEGS = {
 'P01_sand': ('b1', 979, 1029, ('S2_SAND',)), 'P02_furnace': ('p1', 1030, 1082, ('S2_PLATES',)), 'P03_poly': ('b2', 1083, 1175, ('S2_POLY',)),
 'P04_cz': ('b3', 1176, 1230, ('S2_CZ',)), 'P05_slice': ('b4', 1231, 1278, ('S2_SLICE',)), 'P06_polish': ('p5', 1279, 1300, ('S2_PLATES',)),
 'P07_fly': ('b6', 1301, 1384, W), 'P08_fet': ('b7', 1385, 1497, ('S2_FET',)), 'P09_fet_on': ('b8', 1498, 1533, ('S2_FET',)),
 'P10_lattice': ('b9', 1534, 1633, W), 'P11_hero': ('b10', 1634, 1793, W + ('S2_HILITE',)),
}
timing = {}
for name in args['segs']:
    ck, n0, n1, show = SEGS[name]
    for c in SETS: bpy.data.collections[c].hide_render = c not in show
    sc.camera = cams[ck]; sc.frame_start, sc.frame_end = f2(n0), f2(n1); sc.render.filepath = os.path.join(out, f'S02v1_{name}_')
    t = time.time(); bpy.ops.render.render(animation=True); timing[name] = dict(frames=n1 - n0 + 1, seconds=round(time.time() - t, 1))
result['timing'] = timing; result['files'] = sorted(os.listdir(out))
