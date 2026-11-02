# EP004 S01 module 1 (on top of v012): small fixes + the phone-UI opening shots O1-O5 and O8 + freeze camera.
# Preview-grade UI (generic, no real app branding). Timeline: preview frame n (24 fps) <-> Blender frame n - 527.
import bpy, bmesh, math, os, random, tempfile, numpy as np
from mathutils import Vector
sc = bpy.context.scene; M = bpy.data.materials; O = bpy.data.objects
SX, SY = 0.8, 4.6
random.seed(7)
def bf(n): return n - 527
def col(name):
    c = bpy.data.collections.get(name)
    if not c: c = bpy.data.collections.new(name); sc.collection.children.link(c)
    return c
def lk(m, a, sa, b, sb): m.node_tree.links.new(a.outputs[sa], b.inputs[sb])

# ---------------- fixes found in the v012 sheets ----------------
wt = sc.world.node_tree; wout = wt.nodes['World Output']; bg = wt.nodes['Background']
lp = wt.nodes.new('ShaderNodeLightPath'); bg2 = wt.nodes.new('ShaderNodeBackground'); bg2.inputs['Color'].default_value = (0, 0, 0, 1); bg2.inputs['Strength'].default_value = 0.0
mx = wt.nodes.new('ShaderNodeMixShader')
wt.links.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); wt.links.new(bg.outputs[0], mx.inputs[1]); wt.links.new(bg2.outputs[0], mx.inputs[2]); wt.links.new(mx.outputs[0], wout.inputs['Surface'])
for o in O:
    if o.name.startswith(('label_', 'labelplate_')):
        o.visible_glossy = o.visible_diffuse = o.visible_transmission = o.visible_shadow = False
rl = O['die_under_reflector'].data
for f, v in ((235, 140.0), (270, 140.0), (292, 55.0), (320, 55.0), (400, 55.0)):
    rl.energy = v; rl.keyframe_insert('energy', frame=f)
mt = M['wafer_die_tiles']; nn = mt.node_tree.nodes; b = nn['Principled BSDF']
rng = [x for x in nn if x.type == 'MAP_RANGE' and x.inputs['To Max'].default_value > 100][0]
rng.inputs['To Min'].default_value = 260.0; rng.inputs['To Max'].default_value = 700.0
tcn = nn.new('ShaderNodeTexCoord'); vl = nn.new('ShaderNodeVectorMath'); vl.operation = 'LENGTH'; mt.node_tree.links.new(tcn.outputs['Object'], vl.inputs[0])
mu = nn.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 38.0; mt.node_tree.links.new(vl.outputs['Value'], mu.inputs[0])
ad = nn.new('ShaderNodeMath'); ad.operation = 'ADD'; mt.node_tree.links.new(rng.outputs[0], ad.inputs[0]); mt.node_tree.links.new(mu.outputs[0], ad.inputs[1])
mt.node_tree.links.new(ad.outputs[0], b.inputs['Thin Film Thickness'])

# ---------------- phone root, table, UI scaffolding ----------------
root = bpy.data.objects.new('phone_root', None); col('02_HERO_PHONE').objects.link(root)
for cn in ('01_DISPLAY_STACK', '02_HERO_PHONE', '03_LOGIC_BOARD', '04_POP_SOC'):
    for o in list(bpy.data.collections[cn].objects):
        if o.parent is None and o is not root: o.parent = root
setc, uic = col('08_OPEN_SET'), col('09_OPEN_UI')
def mk_mat(name, color, metal=0.0, rough=0.4):
    m = bpy.data.materials.new(name); m.use_nodes = True; b2 = m.node_tree.nodes['Principled BSDF']
    b2.inputs['Base Color'].default_value = (*color, 1); b2.inputs['Metallic'].default_value = metal; b2.inputs['Roughness'].default_value = rough; return m
tb = bmesh.new(); bmesh.ops.create_grid(tb, x_segments=1, y_segments=1, size=120.0)
tm = bpy.data.meshes.new('open_table'); tb.to_mesh(tm); tb.free()
table = bpy.data.objects.new('open_table', tm); table.location = (0, 0, -0.01); setc.objects.link(table); tm.materials.append(mk_mat('table_dark', (0.012, 0.013, 0.016), 0.0, 0.32))
ui_root = bpy.data.objects.new('ui_root', None); uic.objects.link(ui_root); ui_root.parent = root; ui_root.location = (0, 0, 0.782)
_em = {}
def emat(color, strength=1.5, base=(0, 0, 0)):
    k = (color, strength, base)
    if k not in _em:
        m = bpy.data.materials.new(f'ui_{len(_em)}'); m.use_nodes = True; b2 = m.node_tree.nodes['Principled BSDF']
        b2.inputs['Base Color'].default_value = (*base, 1); b2.inputs['Emission Color'].default_value = (*color, 1); b2.inputs['Emission Strength'].default_value = strength; b2.inputs['Roughness'].default_value = 0.6
        _em[k] = m
    return _em[k]
def put(o, loc, z=0.0):
    uic.objects.link(o); o.parent = ui_root; o.location = (loc[0], loc[1], z); return o
def rrect(w, h, r, loc, color, strength=1.4, z=0.0, base=(0, 0, 0)):
    pts = []
    for cx, cy, a0 in ((w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)):
        for i in range(7): a = math.radians(a0 + 90*i/6); pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    bm = bmesh.new(); bm.faces.new([bm.verts.new((x, y, 0)) for x, y in pts]); me = bpy.data.meshes.new('rr'); bm.to_mesh(me); bm.free()
    me.materials.append(emat(color, strength, base)); return put(bpy.data.objects.new('rr', me), loc, z)
def disc(r, loc, color, strength=1.5, z=0.0):
    bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=True, radius=r, segments=40); me = bpy.data.meshes.new('d'); bm.to_mesh(me); bm.free()
    me.materials.append(emat(color, strength)); return put(bpy.data.objects.new('d', me), loc, z)
def ring(r_out, r_in, loc, color, strength=2.0, z=0.001):
    bm = bmesh.new(); seg = 48
    A = [bm.verts.new((r_out*math.cos(2*math.pi*i/seg), r_out*math.sin(2*math.pi*i/seg), 0)) for i in range(seg)]
    B = [bm.verts.new((r_in*math.cos(2*math.pi*i/seg), r_in*math.sin(2*math.pi*i/seg), 0)) for i in range(seg)]
    for i in range(seg): j = (i+1) % seg; bm.faces.new((A[i], A[j], B[j], B[i]))
    me = bpy.data.meshes.new('ring'); bm.to_mesh(me); bm.free(); me.materials.append(emat(color, strength)); return put(bpy.data.objects.new('ring', me), loc, z)
def bar(w, h, loc, color, strength=1.5, z=0.002, rot=0.0):
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5); bmesh.ops.scale(bm, vec=(w*2*0.5/0.5*0.5, h*2*0.5/0.5*0.5, 1), verts=bm.verts)
    me = bpy.data.meshes.new('bar'); bm.to_mesh(me); bm.free(); me.materials.append(emat(color, strength)); o = put(bpy.data.objects.new('bar', me), loc, z); o.rotation_euler.z = rot; return o
def text(s, size, loc, color=(1, 1, 1), strength=2.0, z=0.003, align='CENTER'):
    cu = bpy.data.curves.new('t', 'FONT'); cu.body = s; cu.size = size; cu.align_x = align; cu.align_y = 'CENTER'
    cu.materials.append(emat(color, strength, (0, 0, 0)) if strength > 0 else emat((0, 0, 0), 0.0)); return put(bpy.data.objects.new('t', cu), loc, z)
def vis(objs, windows):
    for o in (objs if isinstance(objs, (list, tuple)) else [objs]):
        o.hide_render = True; o.keyframe_insert('hide_render', frame=-3000)
        for on, off in windows:
            o.hide_render = False; o.keyframe_insert('hide_render', frame=bf(on)); o.hide_render = True; o.keyframe_insert('hide_render', frame=bf(off))
def pop(o, n0, n1, s0=0.0, s1=1.0, overshoot=1.12):
    o.scale = (s0, s0, 1); o.keyframe_insert('scale', frame=bf(n0)); o.scale = (overshoot*s1, overshoot*s1, 1); o.keyframe_insert('scale', frame=bf(n0 + (n1-n0)//2))
    o.scale = (s1, s1, 1); o.keyframe_insert('scale', frame=bf(n1))
BG_W, BG_H = 6.9, 14.4
# ---- pages (window = preview frames when visible) ----
P = {}   # name -> list of objects
def page(name, objs): P[name] = objs; return objs
bg_lock = rrect(BG_W, BG_H, 0.9, (0, 0), (0.03, 0.05, 0.12), 0.7, z=0.0)
lock = page('lock', [text('09:41', 1.9, (0, 4.4)), text('MONDAY 2 NOVEMBER', 0.36, (0, 3.0), (0.7, 0.8, 1.0), 1.6)]
            + [ring(1.6 - 0.35*i, 1.6 - 0.35*i - 0.08, (0, -5.4), (0.75, 0.85, 1.0), 2.0) for i in range(4)] + [disc(0.14, (0, -5.4), (0.75, 0.85, 1.0), 2.0)])
notif = page('notif', [rrect(6.0, 1.3, 0.35, (0, 6.1), (0.12, 0.16, 0.26), 1.4), text('PAYMENT RECEIVED', 0.38, (0, 6.25), (1, 1, 1), 2.0), text('now', 0.26, (0, 5.85), (0.6, 0.7, 0.9), 1.5)])
unlock_ok = page('unlock_ok', [ring(1.6 - 0.35*i, 1.6 - 0.35*i - 0.08, (0, -5.4), (0.2, 1.0, 0.45), 3.0, z=0.0015) for i in range(4)] + [disc(0.14, (0, -5.4), (0.2, 1.0, 0.45), 3.0, z=0.0015)])
tiles = []
cols_ = [(1.0, 0.35, 0.3), (0.25, 0.7, 1.0), (1.0, 0.8, 0.25), (0.35, 0.9, 0.5), (0.7, 0.45, 1.0), (1.0, 0.55, 0.2), (0.3, 0.85, 0.9)]
for r_ in range(5):
    for c_ in range(4): tiles.append(rrect(1.15, 1.15, 0.3, (-2.25 + c_*1.5, 5.4 - r_*1.7), random.choice(cols_), 1.1, z=0.001))
home = page('home', tiles + [rrect(5.6, 1.4, 0.5, (0, -6.2), (0.15, 0.2, 0.32), 1.0, z=0.001)])
upi_bg = rrect(BG_W, BG_H, 0.9, (0, 0), (0.01, 0.07, 0.05), 0.8, z=0.0005)
upi_c = disc(1.6, (0, 2.8), (0.1, 0.9, 0.45), 2.2, z=0.002)
chk1 = bar(0.22, 0.95, (-0.45, 2.55), (1, 1, 1), 3.0, 0.004, math.radians(40)); chk2 = bar(0.22, 1.6, (0.4, 2.8), (1, 1, 1), 3.0, 0.004, math.radians(-40))
upi = page('upi', [upi_bg, upi_c, text('PAYMENT SUCCESSFUL', 0.46, (0, -0.4), (0.7, 1, 0.8), 2.2), text('250.00', 1.3, (0, -1.9), (1, 1, 1), 2.4),
                   text('Paid to  CHAI POINT', 0.4, (0, -3.3), (0.7, 0.85, 0.8), 1.6), text('Ref 4821 9930 1127', 0.3, (0, -4.1), (0.5, 0.7, 0.6), 1.4), rrect(4.6, 1.1, 0.5, (0, -6.0), (0.1, 0.8, 0.4), 1.6, z=0.002), text('DONE', 0.5, (0, -6.0), (0, 0.1, 0.05), 0.0)])
tk_bg = rrect(BG_W, BG_H, 0.9, (0, 0), (0.02, 0.03, 0.07), 0.7, z=0.0005)
tk_card = rrect(5.9, 8.2, 0.5, (0, 0.8), (0.92, 0.94, 0.98), 1.0, z=0.002)
tk_head = rrect(5.9, 1.5, 0.5, (0, 4.1), (0.15, 0.35, 0.9), 1.3, z=0.003)
bars = [bar(random.choice((0.05, 0.1, 0.16)), 1.1, (-2.3 + i*0.16, -2.6), (0, 0, 0), 0.0, 0.004) for i in range(28)]
tk_txt = [text('TRAIN TICKET', 0.5, (0, 4.1), (1, 1, 1), 2.4), text('CONFIRMED', 0.42, (0, 2.9), (0.05, 0.6, 0.2), 0.0), text('MUMBAI  >>  DELHI', 0.52, (0, 1.7), (0, 0, 0), 0.0), text('16:35        08:15', 0.5, (0, 0.7), (0.1, 0.1, 0.15), 0.0),
          text('COACH B2    SEAT 41', 0.4, (0, -0.5), (0.1, 0.1, 0.15), 0.0), text('PNR 2308 1193', 0.38, (0, -1.4), (0.2, 0.2, 0.3), 0.0)]
ticket = page('ticket', [tk_bg, tk_card, tk_head, tk_txt[0]])
ch_bg = rrect(BG_W, BG_H, 0.9, (0, 0), (0.012, 0.018, 0.04), 0.7, z=0.0005)
ub = rrect(4.6, 1.2, 0.5, (0.9, 4.6), (0.15, 0.4, 0.95), 1.5, z=0.002); ut = text('How do chips work?', 0.4, (0.9, 4.6), (1, 1, 1), 2.4)
ab = rrect(5.6, 4.2, 0.5, (-0.5, 1.2), (0.12, 0.15, 0.24), 1.1, z=0.002)
al = [text('Tiny switches called', 0.38, (-0.5, 2.5), (0.9, 0.95, 1), 2.0), text('transistors, billions of', 0.38, (-0.5, 1.7), (0.9, 0.95, 1), 2.0), text('them, etched in silicon.', 0.38, (-0.5, 0.9), (0.9, 0.95, 1), 2.0), text('Fast, small, everywhere.', 0.38, (-0.5, 0.1), (0.5, 0.9, 1.0), 2.2)]
dots = [disc(0.18, (-2.4 + i*0.55, 1.4), (0.7, 0.8, 1.0), 2.0, z=0.003) for i in range(3)]
inb = rrect(5.8, 1.1, 0.5, (0, -6.2), (0.1, 0.13, 0.2), 1.0, z=0.002)
chat = page('chat', [ch_bg, inb])
# chip outline on the dark screen (recap end)
chip = [bar(2.6, 0.08, (0, 1.3), (0.3, 0.9, 1), 4, 0.003), bar(2.6, 0.08, (0, -1.3), (0.3, 0.9, 1), 4, 0.003), bar(0.08, 2.6, (-1.3, 0), (0.3, 0.9, 1), 4, 0.003), bar(0.08, 2.6, (1.3, 0), (0.3, 0.9, 1), 4, 0.003), disc(0.5, (0, 0), (0.3, 0.9, 1), 3, z=0.003)]
for i in range(8):
    x = -1.0 + i*0.285
    chip += [bar(0.07, 0.35, (x, 1.6), (0.3, 0.9, 1), 3, 0.003), bar(0.07, 0.35, (x, -1.6), (0.3, 0.9, 1), 3, 0.003), bar(0.35, 0.07, (-1.6, x), (0.3, 0.9, 1), 3, 0.003), bar(0.35, 0.07, (1.6, x), (0.3, 0.9, 1), 3, 0.003)]
page('chip', chip)

# ---- schedule (preview frames n) ----
bgl_win = [(20, 110), (404, 446)]                      # lock bg also used for home
vis(bg_lock, [(20, 150), (404, 470)])
vis(P['lock'], [(20, 78)]); vis(P['notif'], [(20, 50)])
vis(P['unlock_ok'], [(70, 78)]); vis(P['home'], [(78, 96), (434, 452)])
vis(P['upi'], [(96, 150), (404, 414)]); vis(P['ticket'], [(150, 194), (414, 424)]); vis(P['chat'], [(194, 271), (424, 434)])
pop(upi_c, 98, 108)
# staged reveals inside pages
for o in (chk1, chk2): vis(o, [(108, 150), (406, 414)])
for o in tk_txt[1:] + bars: vis(o, [(166, 194), (418, 424)])
for i, o in enumerate(al): vis(o, [(222 + i*12, 271), (426 + i, 434)] if True else [])
vis(ut, [(200, 271), (424, 434)]); vis(ub, [(198, 271), (424, 434)]); vis(ab, [(220, 271), (426, 434)])
for i, o in enumerate(dots):
    vis(o, [(208 + 3*k + (k % 3 == i)*0, 208 + 3*k + 2) for k in range(0, 4)])        # blink while 'typing'
vis(P['chip'], [(486, 520)])
# slide/pop motion
tk_all = [tk_card, tk_head] + tk_txt + bars
ui_slide = bpy.data.objects.new('ticket_slide', None); uic.objects.link(ui_slide)
for o in tk_all:
    y1 = o.location.y
    o.location.y = y1 - 9.0; o.keyframe_insert('location', index=1, frame=bf(150)); o.location.y = y1; o.keyframe_insert('location', index=1, frame=bf(162))
# screen glow for fingerprint pulse
for o in P['lock'][2:]:
    o.scale = (1, 1, 1); o.keyframe_insert('scale', frame=bf(58)); o.scale = (1.08, 1.08, 1); o.keyframe_insert('scale', frame=bf(64)); o.scale = (1, 1, 1); o.keyframe_insert('scale', frame=bf(70))
# phone buzz (n 12..34), recap screen dimming is handled by the page windows above
random.seed(3)
for i, n in enumerate(range(12, 36, 2)):
    amp = 1.0 - (n - 12) / 28.0
    root.location = (random.uniform(-0.09, 0.09)*amp, random.uniform(-0.06, 0.06)*amp, 0); root.rotation_euler = (0, 0, math.radians(random.uniform(-0.8, 0.8)*amp))
    root.keyframe_insert('location', frame=bf(n)); root.keyframe_insert('rotation_euler', frame=bf(n))
root.location = (0, 0, 0); root.rotation_euler = (0, 0, 0)
root.keyframe_insert('location', frame=bf(36)); root.keyframe_insert('rotation_euler', frame=bf(36))
root.keyframe_insert('location', frame=bf(0)); root.keyframe_insert('rotation_euler', frame=bf(0))

# ---------------- cameras (same euler method as the existing studio) ----------------
cc = col('05_CAMERAS')
def euler_for(pos, tgt, prev):
    d = Vector(tgt) - Vector(pos); d.normalize(); rx = math.acos(max(-1.0, min(1.0, -d.z)))
    rz = math.atan2(-d.x, d.y) if math.hypot(d.x, d.y) > 1e-4 else prev
    while rz - prev > math.pi: rz -= 2*math.pi
    while rz - prev < -math.pi: rz += 2*math.pi
    return (rx, 0.0, rz)
def make_cam(name, lens, keys, prev=0.0):
    d = bpy.data.cameras.new(name); d.lens = lens; d.sensor_width = 36; d.clip_start = 0.01; d.clip_end = 3000
    o = bpy.data.objects.new(name, d); cc.objects.link(o)
    for n, pos, tgt in keys:
        e = euler_for(pos, tgt, prev); prev = e[2]; o.location = pos; o.rotation_euler = e
        o.keyframe_insert('location', frame=bf(n)); o.keyframe_insert('rotation_euler', frame=bf(n))
    return o
HERO = ((-15, -21, 17), (0.0, 0.5, 0.4))
cams = {
 'O1': make_cam('CAM_O1', 40, [(0, (-16, -22, 15), HERO[1]), (60, (-11, -15, 12), (0, 0.3, 0.7))]),
 'O2': make_cam('CAM_O2', 50, [(60, (0.8, -2.6, 6.2), (0, -5.0, 0.78)), (84, (0.3, -3.2, 7.6), (0, -4.4, 0.78)), (96, (0.0, -1.4, 11), (0, 0.4, 0.78))]),
 'O3': make_cam('CAM_O3', 40, [(96, (0.0, -3.4, 11), (0, 0.6, 0.78)), (150, (0.6, -2.4, 9.5), (0, 0.9, 0.78))]),
 'O4': make_cam('CAM_O4', 40, [(150, (-1.8, -4.0, 10.5), (0, 0.9, 0.78)), (194, (-0.6, -3.0, 9.5), (0, 0.9, 0.78))]),
 'O5': make_cam('CAM_O5', 40, [(194, (1.2, -3.2, 10.5), (0, 0.8, 0.78)), (271, (0.4, -2.6, 8.8), (0, 1.4, 0.78))]),
 'O8': make_cam('CAM_O8', 40, [(404, (0.0, -1.6, 10.0), (0, 0.4, 0.78)), (470, (-4.0, -7.0, 12.0), (0, 0.4, 0.5)), (527, HERO[0], HERO[1])]),
}
fz = bpy.data.cameras.new('CAM_S01_FREEZE'); fz.lens = 40; fz.sensor_width = 36; fz.clip_start = 0.0004; fz.clip_end = 600
fo = bpy.data.objects.new('CAM_S01_FREEZE', fz); cc.objects.link(fo)
sc.frame_set(102); rzA = O['CAM_S01_A_pushthrough'].rotation_euler.z
fo.location = (SX - 2.0, SY - 2.7, 0.72); fo.rotation_euler = euler_for(fo.location, (SX, SY, 0.78), rzA)   # A_END pose (v012 key at f102)

# ---------------- sheets ----------------
gpu(sc, 'auto'); sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.use_denoising = True
tmp = tempfile.mkdtemp()
def setpass(opening):
    for c in ('08_OPEN_SET', '09_OPEN_UI'): bpy.data.collections[c].hide_render = not opening
def sheet(items, fname, w=480, h=270):
    sc.render.resolution_x, sc.render.resolution_y = w, h; tiles_ = []
    for cam, n, opening in items:
        setpass(opening); sc.camera = cam; sc.frame_set(n if not opening else bf(n)); p = os.path.join(tmp, f'{fname}_{n}.png'); sc.render.filepath = p
        bpy.ops.render.render(write_still=True); im = bpy.data.images.load(p); tiles_.append(np.array(im.pixels[:]).reshape(h, w, 4))
    rows = [np.hstack(tiles_[i:i+4]) for i in range(0, len(tiles_), 4)]; sh = np.vstack(rows[::-1])
    si = bpy.data.images.new(fname, sh.shape[1], sh.shape[0], alpha=True); si.pixels = sh.ravel().tolist(); si.filepath_raw = os.path.join(out, fname + '.png'); si.file_format = 'PNG'; si.save()
C = cams
sheet([(C['O1'], 2, True), (C['O1'], 22, True), (C['O1'], 40, True), (C['O1'], 58, True), (C['O2'], 66, True), (C['O2'], 74, True), (C['O2'], 86, True), (C['O2'], 94, True)], 'm1_a')
sheet([(C['O3'], 100, True), (C['O3'], 110, True), (C['O3'], 128, True), (C['O3'], 146, True), (C['O4'], 156, True), (C['O4'], 168, True), (C['O4'], 184, True), (C['O4'], 192, True)], 'm1_b')
sheet([(C['O5'], 200, True), (C['O5'], 216, True), (C['O5'], 232, True), (C['O5'], 262, True), (C['O8'], 408, True), (C['O8'], 420, True), (C['O8'], 438, True), (C['O8'], 452, True)], 'm1_c')
sheet([(C['O8'], 466, True), (C['O8'], 482, True), (C['O8'], 496, True), (C['O8'], 510, True), (C['O8'], 523, True), (O['CAM_S01_A_pushthrough'], 1, False), (O['CAM_S01_B_dive'], 304, False), (O['CAM_S01_C_wafer'], 410, False)], 'm1_d')
setpass(False); sc.camera = O['CAM_S01_A_pushthrough']; sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s01_camera_v013.blend'), copy=True)
result['ok'] = True
