# EP004 S02 "From Quartz to a Chip" v003 (v002 review: melt raised above crucible rim, polish camera pulled back, transistor camera higher with thicker channel); v002 (v001 review: glassy quartz + backlight, round sand heap, smooth bright polysilicon, camera above melt, soft polish band, cross-section transistor, calmer array exposure): procedural Blender build, nine stages, one camera per stage, frames locked to the narration.
# Local frame f = (global_seconds - 36.24) * 24 + 1  (S02 = 0:36.24-1:14.75, see production/timing-map.md). 24 fps, 1 unit = 1 m (stylised scale).
# Stages sit 100 units apart on X so lights never leak between them. Runs as EngineX blender/script. Preview only.
import bpy, bmesh, math, os, random, tempfile
import numpy as np
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

random.seed(7)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
sc = bpy.context.scene
sc.render.fps = 24
gpu(sc, 'auto'); sc.render.engine = 'CYCLES'
sc.cycles.samples = 16; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6
sc.view_settings.view_transform = 'AgX'
w = bpy.data.worlds.new('w'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.004, 0.005, 0.008, 1); sc.world = w

# ---------------- helpers ----------------
def mat(name, color, metal=0.0, rough=0.4, emit=None, emit_k=0.0, **extra):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if emit: b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = emit_k
    for k, v in extra.items(): b.inputs[k].default_value = v
    return m

def drv(sock, expr, name='default_value'):
    d = sock.driver_add(name).driver; d.type = 'SCRIPTED'; d.expression = expr

def prim(kind, loc, scale=(1, 1, 1), m=None, rot=(0, 0, 0), name=None, **kw):
    getattr(bpy.ops.mesh, f'primitive_{kind}_add')(location=loc, rotation=rot, **kw)
    o = bpy.context.active_object; o.scale = scale
    if name: o.name = name
    if m: o.data.materials.append(m)
    return o

def key(o, path, frames_vals, idx=-1):
    for f, v in frames_vals:
        if idx < 0: setattr(o, path, v)
        else: getattr(o, path)[idx] = v
        o.keyframe_insert(path, frame=f, index=idx)

def light(kind, loc, energy, size, color=(1, 1, 1), target=None):
    l = bpy.data.lights.new('L', kind); l.energy = energy; l.color = color
    if kind == 'AREA': l.size = size
    o = bpy.data.objects.new('L', l); sc.collection.objects.link(o); o.location = loc
    if target:
        c = o.constraints.new('TRACK_TO'); c.target = target; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    return o

def empty(loc):
    e = bpy.data.objects.new('E', None); sc.collection.objects.link(e); e.location = loc; return e

def make_cam(name, lens, keys, ox, lens_keys=None):
    c = bpy.data.cameras.new(name); c.lens = lens; c.clip_end = 2000
    o = bpy.data.objects.new(name, c); sc.collection.objects.link(o)
    tg = empty((ox, 0, 0)); tg.name = name + '_T'
    cn = o.constraints.new('TRACK_TO'); cn.target = tg; cn.track_axis = 'TRACK_NEGATIVE_Z'; cn.up_axis = 'UP_Y'
    for f, loc, tgt in keys:
        o.location = (loc[0] + ox, loc[1], loc[2]); o.keyframe_insert('location', frame=f)
        tg.location = (tgt[0] + ox, tgt[1], tgt[2]); tg.keyframe_insert('location', frame=f)
    for f, l in (lens_keys or []):
        c.lens = l; c.keyframe_insert('lens', frame=f)
    return o

floor_m = mat('floor', (0.02, 0.022, 0.03), 0.0, 0.18)
def floor(ox, size=60):
    prim('plane', (ox, 0, 0), (size, size, 1), floor_m)

def stage_light(ox, kc=(1.0, 0.95, 0.9), e=900, h=6, soft=True):
    t = empty((ox, 0, 0.5))
    light('AREA', (ox - 4, -5, h), e, 4, kc, t)
    light('AREA', (ox + 5, 4, h * 0.7), e * 0.6, 3, (0.55, 0.7, 1.0), t)
    if soft: light('AREA', (ox, 0, h * 1.6), e * 0.5, 7, (1, 1, 1), t)     # big overhead softbox so metals reflect something

cams = {}
SHOTS = []     # (name, f0, f1)
def shot(name, f0, f1, cam): SHOTS.append((name, f0, f1)); cams[name] = cam

# ---------------- materials ----------------
M_quartz = mat('quartz', (0.82, 0.8, 0.78), 0, 0.04, **{'Transmission Weight': 1.0, 'IOR': 1.54})
M_sand = mat('sand', (0.62, 0.45, 0.25), 0, 0.95)
nt = M_sand.node_tree; n = nt.nodes; vo = n.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 900
bm = n.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.6
nt.links.new(vo.outputs['Distance'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], n['Principled BSDF'].inputs['Normal'])
M_substrate = mat('substrate', (0.06, 0.1, 0.06), 0, 0.4)
M_gold = mat('gold', (0.9, 0.62, 0.2), 1.0, 0.25)

def circuit_mat(name, scale=14, glow=1.5):
    m = mat(name, (0.02, 0.03, 0.06), 0.7, 0.3, (0.1, 0.8, 1.0), 0.0)
    n = m.node_tree.nodes; L = m.node_tree.links; b = n['Principled BSDF']
    tc = n.new('ShaderNodeTexCoord'); sp = n.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sp.inputs[0])
    outs = []
    for ax, s in (('X', scale), ('Y', scale * 1.3)):
        mu = n.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = s; L.new(sp.outputs[ax], mu.inputs[0])
        fr = n.new('ShaderNodeMath'); fr.operation = 'FRACT'; L.new(mu.outputs[0], fr.inputs[0])
        lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.22; L.new(fr.outputs[0], lt.inputs[0]); outs.append(lt)
    mx = n.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; L.new(outs[0].outputs[0], mx.inputs[0]); L.new(outs[1].outputs[0], mx.inputs[1])
    ms = n.new('ShaderNodeMath'); ms.operation = 'MULTIPLY'; ms.inputs[1].default_value = glow; L.new(mx.outputs[0], ms.inputs[0])
    L.new(ms.outputs[0], b.inputs['Emission Strength'])
    return m

# =============== S1  02-01 quartz crystal (f1-120) ===============
ox = 0; floor(ox)
for i in range(11):
    a = random.uniform(0, 6.28); r = random.uniform(0.0, 0.7) * (0.3 + i / 10); h = random.uniform(0.8, 2.1) * (1.2 - r * 0.5)
    tilt = (random.uniform(-0.35, 0.35), random.uniform(-0.35, 0.35), random.uniform(0, 1))
    body = prim('cylinder', (ox + r * math.cos(a), r * math.sin(a), h / 2), (0.16, 0.16, h / 2), M_quartz, tilt, vertices=6, radius=1)
    tip = prim('cone', (0, 0, 0), (0.16, 0.16, 0.14), M_quartz, tilt, vertices=6, radius1=1, radius2=0, depth=1)
    tip.location = body.matrix_world @ Vector((0, 0, 1.0 + 0.5 * 0.14 / (h / 2)))
    tip.scale = (0.16, 0.16, 0.2)
stage_light(ox, e=1200)
light('AREA', (ox + 1.5, 4.5, 2.2), 2500, 3, (1.0, 0.85, 0.65), empty((ox, 0, 1.0)))   # warm backlight so the crystal glows
shot('S02_01_quartz', 1, 120, make_cam('CAM_S02_01_quartz', 40, [(1, (5.5, -5.0, 0.7), (0, 0, 1.0)), (60, (2.0, -5.0, 1.0), (0, 0, 1.1)), (120, (-1.6, -4.0, 1.5), (0, 0, 1.2))], ox))

# =============== S2  02-02 sand vs processor (f121-200) ===============
ox = 100; floor(ox)
bm_ = bmesh.new(); N = 130; L_ = 5.0
for i in range(N + 1):
    for j in range(N + 1):
        x = (i / N - 0.5) * L_; y = (j / N - 0.5) * L_; r2 = x * x + y * y
        bm_.verts.new((x, y, 1.15 * math.exp(-r2 / 0.55) + random.uniform(0, 0.02) * (r2 < 4.0)))
bm_.verts.ensure_lookup_table()
for i in range(N):
    for j in range(N):
        a = i * (N + 1) + j
        if min(math.hypot(bm_.verts[k].co.x, bm_.verts[k].co.y) for k in (a, a + N + 1, a + N + 2, a + 1)) < 2.0:
            bm_.faces.new((bm_.verts[a], bm_.verts[a + N + 1], bm_.verts[a + N + 2], bm_.verts[a + 1]))
me = bpy.data.meshes.new('sand'); bm_.to_mesh(me); bm_.free(); sand = bpy.data.objects.new('sand', me); sand.location = (ox - 2.4, 0, 0)
sc.collection.objects.link(sand); me.materials.append(M_sand)
for p in me.polygons: p.use_smooth = True
CH = circuit_mat('chip_die', 10, 1.2)
prim('cube', (ox + 2.4, 0, 0.07), (1.3, 1.3, 0.07), M_substrate)
prim('cube', (ox + 2.4, 0, 0.19), (0.62, 0.62, 0.05), CH)
for sx in (-1, 1):
    for sy in (-1, 1): prim('cube', (ox + 2.4 + sx * 1.08, sy * 1.08, 0.15), (0.07, 0.07, 0.015), M_gold)
stage_light(ox, e=1200)
shot('S02_02_sand', 121, 200, make_cam('CAM_S02_02_sand', 40, [(121, (-3, -6.5, 1.6), (-2.4, 0, 0.5)), (165, (0, -8.5, 1.8), (0, 0, 0.4)), (200, (2.8, -5.0, 1.4), (2.4, 0, 0.2))], ox))

# =============== S3  02-03 refined: grey lumps become bright polysilicon (f213-282) ===============
ox = 200; floor(ox)
M_poly = mat('poly', (0.16, 0.15, 0.14), 0.0, 0.9)
b = M_poly.node_tree.nodes['Principled BSDF']
for sock, v0, v1 in ((b.inputs['Base Color'], (0.16, 0.15, 0.14, 1), (0.78, 0.8, 0.85, 1)), (b.inputs['Metallic'], 0.0, 1.0), (b.inputs['Roughness'], 0.9, 0.16)):
    sock.default_value = v0; sock.keyframe_insert('default_value', frame=225); sock.default_value = v1; sock.keyframe_insert('default_value', frame=262)
for i in range(9):
    a = i * 2.4; r = 0.25 + 0.55 * random.random() * (i > 0)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=random.uniform(0.28, 0.46), location=(ox + r * math.cos(a), r * math.sin(a), 0.3))
    o = bpy.context.active_object; o.data.materials.append(M_poly)
    for v in o.data.vertices: v.co *= random.uniform(0.7, 1.15)
    o.rotation_euler = (random.random() * 3, random.random() * 3, random.random() * 3); o.scale = (1.1, 0.9, 0.8)
    for p_ in o.data.polygons: p_.use_smooth = True
stage_light(ox, e=1300)
shot('S02_03_purity', 213, 282, make_cam('CAM_S02_03_purity', 45, [(213, (3, -4, 1.2), (0, 0, 0.4)), (282, (-1.5, -3.2, 0.9), (0, 0, 0.4))], ox))

# =============== S4  02-04 Czochralski pull (f282-342) ===============
ox = 300; floor(ox)
M_graph = mat('graphite', (0.04, 0.04, 0.045), 0.3, 0.5)
M_melt = mat('melt', (1, 0.5, 0.15), 0, 0.2, (1.0, 0.5, 0.12), 12.0)
M_ingot = mat('ingot', (0.62, 0.64, 0.7), 1.0, 0.3)
prim('cylinder', (ox, 0, 0.4), (1.0, 1.0, 0.4), M_graph, vertices=48, radius=1, depth=2)
prim('cylinder', (ox, 0, 0.82), (0.9, 0.9, 1), M_melt, vertices=48, radius=1, depth=0.02)
prim('cylinder', (ox, 0, 0.2), (1.35, 1.35, 0.2), M_graph, vertices=48, radius=1, depth=1)
ing = prim('cylinder', (ox, 0, 1.0), (0.42, 0.42, 1), M_ingot, vertices=48, radius=1, depth=1)
ing.data.transform(Matrix.Translation((0, 0, -0.5)))          # origin at the top so scale grows downward
rod = prim('cylinder', (ox, 0, 1.0), (0.05, 0.05, 1), M_graph, vertices=16, radius=1, depth=2); rod.data.transform(Matrix.Translation((0, 0, 1.0)))
for o in (ing, rod):
    key(o, 'rotation_euler', [(282, 0.0), (342, 9.4)], 2)
key(ing, 'location', [(282, ox), (342, ox)], 0)
for f, zt in ((282, 1.1), (342, 2.8)):
    ing.location.z = zt; ing.keyframe_insert('location', frame=f, index=2); ing.scale.z = zt - 0.82; ing.keyframe_insert('scale', frame=f, index=2)
    rod.location.z = zt; rod.keyframe_insert('location', frame=f, index=2)
light('POINT', (ox, 0, 1.4), 600, 0, (1, 0.5, 0.2))
stage_light(ox, (1, 0.85, 0.7), 500)
shot('S02_04_crystal', 282, 342, make_cam('CAM_S02_04_crystal', 40, [(282, (3.0, -3.4, 2.6), (0, 0, 0.9)), (342, (2.6, -3.2, 3.2), (0, 0, 1.7))], ox))

# =============== S5  02-05 sliced into wafers (f342-390) ===============
ox = 400; floor(ox)
NW = 14; PITCH = 0.2
discs = []
for i in range(NW):
    d = prim('cylinder', (ox - 1.3 + i * PITCH, 0, 0.7), (0.6, 0.6, 1), M_ingot, rot=(0, math.pi / 2, 0), vertices=48, radius=1, depth=PITCH * 0.98)
    discs.append(d)
M_wire = mat('wire', (0.9, 0.9, 0.95), 1, 0.2, (1, 1, 1), 0.5)
wires = []
for i in range(NW + 1):
    w_ = prim('cylinder', (ox - 1.4 + i * PITCH, 0, 2.2), (0.012, 0.012, 0.8), M_wire, rot=(math.pi / 2, 0, 0), vertices=8, radius=1, depth=2); wires.append(w_)
    key(w_, 'location', [(342, 2.2), (372, 0.0)], 2)
    w_.location.z = 0.0; w_.keyframe_insert('location', frame=382, index=2); w_.location.z = 2.2; w_.keyframe_insert('location', frame=390, index=2)
for i, d in enumerate(discs):
    x0 = ox - 1.3 + i * PITCH; x1 = ox - 1.3 + (i - 6.5) * 0.46 + 6.5 * PITCH
    d.location.x = x0; d.keyframe_insert('location', frame=372, index=0); d.location.x = x1; d.keyframe_insert('location', frame=390, index=0)
last = discs[-1]
last.location = (last.location.x, 0, 0.7); last.keyframe_insert('location', frame=378)
last.location = (ox + 1.4, -1.3, 0.35); last.keyframe_insert('location', frame=390)
last.rotation_euler = (0, math.pi / 2, 0); last.keyframe_insert('rotation_euler', frame=378)
last.rotation_euler = (0.8, math.pi / 2, 0); last.keyframe_insert('rotation_euler', frame=390)
stage_light(ox, e=1300)
shot('S02_05_slice', 342, 390, make_cam('CAM_S02_05_slice', 40, [(342, (0.6, -3.8, 1.1), (0, 0, 0.7)), (390, (-0.6, -3.6, 0.9), (0, 0, 0.6))], ox))

# =============== S6  02-06 polished mirror wafer, sweeping reflection (f390-421) ===============
ox = 500; floor(ox)
Mw = mat('mirror_wafer', (0.55, 0.58, 0.66), 1.0, 0.08, (0.9, 0.95, 1.0), 0.0)
n = Mw.node_tree.nodes; L = Mw.node_tree.links; b = n['Principled BSDF']
tc = n.new('ShaderNodeTexCoord'); sp = n.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sp.inputs[0])
off = n.new('ShaderNodeMath'); off.operation = 'ADD'; L.new(sp.outputs['X'], off.inputs[0]); drv(off.inputs[1], '-1.6 + (frame-390)*0.11')
ab = n.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; L.new(off.outputs[0], ab.inputs[0])
cr = n.new('ShaderNodeMath'); cr.operation = 'SMOOTH_MIN' if False else 'SUBTRACT'; cr.inputs[0].default_value = 1.0; L.new(ab.outputs[0], cr.inputs[1])
cc = n.new('ShaderNodeMath'); cc.operation = 'MAXIMUM'; cc.inputs[1].default_value = 0.0; L.new(cr.outputs[0], cc.inputs[0]); cr = cc
sm = n.new('ShaderNodeMath'); sm.operation = 'MULTIPLY'; sm.inputs[1].default_value = 0.9; L.new(cr.outputs[0], sm.inputs[0]); L.new(sm.outputs[0], b.inputs['Emission Strength'])
wf = prim('cylinder', (ox, 0, 1.4), (1.4, 1.4, 1), Mw, rot=(math.pi / 2 + 0.25, 0, 0), vertices=96, radius=1, depth=0.03)
wf.rotation_euler = (math.pi / 2, 0, 0)
stage_light(ox, e=2500)
shot('S02_06_polish', 390, 421, make_cam('CAM_S02_06_polish', 40, [(390, (0, -8.5, 1.6), (0, 0, 1.4)), (421, (0, -7.0, 1.6), (0, 0, 1.4))], ox))

# =============== S7  02-07 wafer grid, one die selected (f432-511) ===============
ox = 600; floor(ox)
P = 0.18
Mg = mat('wafer_dies', (0.1, 0.05, 0.2), 0.9, 0.25)
n = Mg.node_tree.nodes; L = Mg.node_tree.links; b = n['Principled BSDF']
tc = n.new('ShaderNodeTexCoord'); sp = n.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sp.inputs[0])
lines = []
for ax in 'XY':
    mu = n.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 1 / P; L.new(sp.outputs[ax], mu.inputs[0])
    fr = n.new('ShaderNodeMath'); fr.operation = 'FRACT'; L.new(mu.outputs[0], fr.inputs[0])
    lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.07; L.new(fr.outputs[0], lt.inputs[0]); lines.append(lt)
sc_ = n.new('ShaderNodeMath'); sc_.operation = 'MAXIMUM'; L.new(lines[0].outputs[0], sc_.inputs[0]); L.new(lines[1].outputs[0], sc_.inputs[1])
ve = n.new('ShaderNodeVectorMath'); ve.operation = 'LENGTH'; L.new(tc.outputs['Object'], ve.inputs[0])
rp = n.new('ShaderNodeValToRGB'); L.new(ve.outputs['Value'], rp.inputs[0])
rp.color_ramp.elements[0].position = 0.0; rp.color_ramp.elements[0].color = (0.25, 0.1, 0.55, 1)
rp.color_ramp.elements[1].position = 3.0; rp.color_ramp.elements[1].color = (0.05, 0.45, 0.5, 1)
e = rp.color_ramp.elements.new(1.5); e.color = (0.7, 0.45, 0.15, 1)
mix = n.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs[7].default_value = (0.01, 0.01, 0.015, 1)
L.new(sc_.outputs[0], mix.inputs['Factor']); L.new(rp.outputs['Color'], mix.inputs[6]); L.new(mix.outputs[2], b.inputs['Base Color'])
prim('cylinder', (ox, 0, 0), (3.0, 3.0, 1), Mg, vertices=128, radius=1, depth=0.04)
SEL = (ox + 2.5 * P, 1.5 * P)                                   # die cell (2,1)
hl = prim('plane', (SEL[0], SEL[1], 0.025), (P * 0.86, P * 0.86, 1), mat('sel', (0.2, 0.8, 1), 0, 0.3, (0.2, 0.9, 1.0), 0.0))
b2 = hl.data.materials[0].node_tree.nodes['Principled BSDF']
for f, v in ((476, 0.0), (492, 2.0)): b2.inputs['Emission Strength'].default_value = v; b2.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)
stage_light(ox, e=1000, h=5)
shot('S02_07_wafergrid', 432, 511, make_cam('CAM_S02_07_wafergrid', 35, [
    (432, (-3.2, -3.4, 0.45), (-0.4, -0.4, 0)), (470, (-1.0, -1.6, 1.1), (0.2, 0.0, 0)), (511, (SEL[0] - ox + 0.01, SEL[1] - 0.45, 0.8), (SEL[0] - ox, SEL[1], 0))], ox))

# =============== S8/9  02-08/09 one transistor, gate off -> on, then one clean toggle (f521-656) ===============
ox = 700; floor(ox)
ON = 'max(0,min(1,(frame-570)/5)) - max(0,min(1,(frame-632)/4)) + max(0,min(1,(frame-646)/4))'
M_si = mat('si_sub', (0.1, 0.12, 0.2), 0.3, 0.35)
M_nd = mat('n_plus', (0.05, 0.4, 0.5), 0.2, 0.3)
M_ox = mat('gate_oxide', (0.9, 0.92, 1.0), 0, 0.1, **{'Transmission Weight': 0.6})
M_gate = mat('gate_poly', (0.8, 0.5, 0.2), 1.0, 0.25, (1.0, 0.6, 0.2), 0.3)
drv(M_gate.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], '0.2 + 1.3*(' + ON + ')')
M_ch = mat('channel', (0.2, 0.7, 1.0), 0, 0.3, (0.2, 0.8, 1.0), 0.0)
drv(M_ch.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], '14*(' + ON + ')')
M_el = mat('electron', (0.3, 0.9, 1), 0, 0.2, (0.3, 0.9, 1.0), 8.0)
# half-section: everything y >= 0, so the cut face toward the camera shows the layers and the channel
Y0 = 0.55
prim('cube', (ox, Y0, -0.35), (1.9, Y0, 0.35), M_si)
for sx in (-1, 1): prim('cube', (ox + sx * 1.35, Y0, -0.09), (0.55, Y0, 0.11), M_nd)
prim('cube', (ox, Y0, -0.04), (0.8, Y0, 0.045), M_ch)
prim('cube', (ox, Y0, 0.045), (0.82, Y0, 0.03), M_ox)
prim('cube', (ox, Y0, 0.17), (0.5, Y0, 0.1), M_gate)
prim('cylinder', (ox, Y0, 0.7), (0.07, 0.07, 0.5), M_gold, vertices=16, radius=1, depth=2)
for sx in (-1, 1):
    prim('cylinder', (ox + sx * 1.35, Y0, 0.35), (0.07, 0.07, 0.42), M_gold, vertices=16, radius=1, depth=2)
for i in range(16):
    el = prim('uv_sphere', (ox, 0.04 + (i % 4) * 0.1, -0.03), (0.045, 0.045, 0.045), M_el, segments=12, ring_count=8, radius=1)
    dx = el.driver_add('location', 0).driver; dx.type = 'SCRIPTED'; dx.expression = f'{ox} - 1.5 + 3.0*((frame*0.07 + {i/16:.4f}) % 1)'
    d = el.driver_add('scale', 0).driver; d.type = 'SCRIPTED'; d.expression = f'0.045*({ON})'
    d = el.driver_add('scale', 1).driver; d.type = 'SCRIPTED'; d.expression = f'0.045*({ON})'
    d = el.driver_add('scale', 2).driver; d.type = 'SCRIPTED'; d.expression = f'0.045*({ON})'
for i in range(4):                                              # + charges on the gate when it is ON
    pc = prim('uv_sphere', (ox + (i - 1.5) * 0.2, Y0 - 0.2, 0.32), (0.05, 0.05, 0.05), M_gate, segments=10, ring_count=6, radius=1)
    for k in range(3):
        d = pc.driver_add('scale', k).driver; d.type = 'SCRIPTED'; d.expression = f'0.05*({ON})'
stage_light(ox, e=900, h=4)
shot('S02_08_transistor', 521, 656, make_cam('CAM_S02_08_transistor', 40, [
    (521, (1.8, -5.0, 2.2), (0, 0.4, 0)), (560, (1.0, -3.4, 1.4), (0, 0.4, 0.05)), (600, (-0.6, -3.0, 1.0), (0.2, 0.4, 0)),
    (632, (0.0, -3.4, 1.1), (0, 0.4, 0.05)), (656, (0.1, -3.9, 1.5), (0, 0.4, 0.05))], ox))

# =============== S10/11  02-10 billions: pull back from one transistor to a huge array, hold (f670-766) ===============
ox = 800; floor(ox, 400)
NA, PA = 64, 2.0
bm_ = bmesh.new()
def box(c, s, mi):
    r = bmesh.ops.create_cube(bm_, size=1.0, matrix=Matrix.Translation(c) @ Matrix.Diagonal((*s, 1)))
    for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = mi
for i in range(NA):
    for j in range(NA):
        cx = (i - NA / 2 + 0.5) * PA; cy = (j - NA / 2 + 0.5) * PA
        box((cx, cy, -0.08), (1.7, 1.7, 0.16), 0)
        box((cx - 0.62, cy, 0.0), (0.45, 1.4, 0.05), 1); box((cx + 0.62, cy, 0.0), (0.45, 1.4, 0.05), 1)
        box((cx, cy, 0.12), (0.7, 1.5, 0.22), 2)
me = bpy.data.meshes.new('array'); bm_.to_mesh(me); bm_.free()
arr = bpy.data.objects.new('array', me); arr.location = (ox, 0, 0); sc.collection.objects.link(arr)
M_g2 = mat('gate_poly_arr', (0.8, 0.5, 0.2), 1.0, 0.25, (1.0, 0.6, 0.2), 0.3)
drv(M_g2.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], '0.3 + 1.6*max(0,min(1,(frame-738)/8))')
for m in (M_si, M_nd, M_g2): me.materials.append(m)
for p in me.polygons: p.use_smooth = False
stage_light(ox, e=14000, h=60, soft=False)
shot('S02_10_array', 670, 766, make_cam('CAM_S02_10_array', 35, [
    (670, (0.3, -4.2, 1.6), (0, 0, 0.05)), (690, (0, -7, 5), (0, 0, 0)), (712, (0, -14, 22), (0, 0, 0)), (736, (0, -10, 70), (0, 0, 0)), (752, (0, -4, 125), (0, 0, 0)), (766, (0, -4, 125), (0, 0, 0))], ox))

# =============== S12  02-12 the array becomes the hero chip, which glides into the lithography optic (f771-917) ===============
ox = 900; floor(ox)
chip = empty((ox, 0, 0)); chip.name = 'hero_chip'
for nm, c, s, m in (('sub', (0, 0, 0.1), (3.0, 3.0, 0.2), M_substrate), ('die', (0, 0, 0.3), (1.6, 1.6, 0.2), circuit_mat('hero_die', 14, 1.8))):
    o = prim('cube', c, s, m, name=nm); o.parent = chip
    o.location = c
for sx in range(-6, 7):
    for sy in (-1, 1):
        o = prim('cube', (sx * 0.2, sy * 1.35, 0.21), (0.08, 0.08, 0.02), M_gold); o.parent = chip
for f, x in ((771, 0.0), (850, 0.0), (917, 22.0)):
    chip.location = (ox + x, 0, 0); chip.keyframe_insert('location', frame=f)
M_lens = mat('lens_ring', (0.1, 0.1, 0.15), 0.8, 0.1, (0.5, 0.7, 1.0), 0.0)
drv(M_lens.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], '12*max(0,min(1,(frame-870)/40))')
for k in range(5):
    prim('torus', (ox + 28 + k * 0.6, 0, 1.2), (1, 1, 1), M_lens, rot=(0, math.pi / 2, 0), major_radius=2.6 - k * 0.45, minor_radius=0.07 + 0.01 * k)
stage_light(ox, e=900, h=6)
light('POINT', (ox + 26, 0, 1.2), 4000, 0, (0.6, 0.75, 1))
shot('S02_12_chip', 771, 917, make_cam('CAM_S02_12_chip', 40, [
    (771, (0, -0.2, 9.5), (0, 0, 0.3)), (815, (3.5, -7.5, 5.5), (0, 0, 0.3)), (850, (4.5, -8.5, 4.0), (0, 0, 0.3)), (917, (12, -11.5, 3.5), (26, 0, 1.0))], ox))

# markers, range
for nm, f0, f1 in SHOTS: sc.timeline_markers.new(nm[:12], frame=f0).camera = cams[nm]
sc.frame_start, sc.frame_end = 1, 917

# ---------------- verification: contact sheets (no video render), subject-in-frame probe ----------------
tmp = tempfile.mkdtemp()
def sheet(nm, f0, f1, w=480, h=270, spp=16):
    cam = cams[nm]; sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = w, h; sc.cycles.samples = spp
    fr = [int(round(f0 + (f1 - 1 - f0) * k / 7)) for k in range(8)]; tiles = []
    for f in fr:
        sc.frame_set(f); p = os.path.join(tmp, f'{nm}_{f}.png'); sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        tiles.append(np.array(bpy.data.images.load(p).pixels[:]).reshape(h, w, 4))
    sh = np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, 8, 4)][::-1])
    im = bpy.data.images.new(nm, sh.shape[1], sh.shape[0], alpha=True); im.pixels = sh.ravel().tolist()
    im.filepath_raw = os.path.join(out, f'sheet_{nm}_f{f0:03d}-{f1:03d}.png'); im.file_format = 'PNG'; im.save()
    return fr, [round(float(t[..., :3].mean()), 3) for t in tiles]
lum = {}
for i, (nm, f0, f1) in enumerate(SHOTS):
    progress(i, len(SHOTS), nm); lum[nm] = sheet(nm, f0, f1)
result['mean_luminance_per_tile'] = lum
# 1280x720 look-reference stills: these seed the AI-generated plates so GEN matches the Blender look
sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.cycles.samples = 48
for nm, f in (('S02_04_crystal', 335), ('S02_08_transistor', 600)):
    sc.camera = cams[nm]; sc.frame_set(f); sc.render.filepath = os.path.join(out, f'ref_{nm}_f{f}.png'); bpy.ops.render.render(write_still=True)
sc.frame_set(1); sc.camera = cams[SHOTS[0][0]]
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s02_v003.blend'), copy=True)
result['objects'] = len(bpy.data.objects)
