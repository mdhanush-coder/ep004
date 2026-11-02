# EP004 S01 camera build v008 (hero phone v005 asset + shots A/B/C). Base: hero phone v005 (shield can open underneath like the real part; v004 = die-underside camera pulled back, stronger thin-film variation; v003 = touch grid dark at rest, under-light hidden from camera; v002 fixes: screen off at rest, organic PCB traces, softer key, die under-light): procedural smartphone with a separable stack down to a face-down die.
# Runs as EngineX blender/script (bpy, out, result, gpu, snapshot are provided).
# Scale: 1 Blender unit = 1 cm. Phone lies screen-up at the origin, +Z is the screen side.
# Layer order follows production/research/s01-invisible-brain.md:
#   cover glass > touch > OLED > TFT > midframe > shield can > DRAM (top of PoP) > AP package > face-down die > board.
# Frame 1 = assembled, frame 50 = exploded (keyed), so the push-through can reuse the same file.
import bpy, bmesh, math, os, random
from mathutils import Vector

random.seed(4)
W, H, R = 7.15, 14.7, 0.95          # phone footprint (cm) and corner radius
SOC = Vector((0.8, 4.6, 0.0))       # SoC position on the logic board
EXPLODED = 50

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
scene = bpy.context.scene

COLS = {}
def col(name):
    if name not in COLS:
        c = bpy.data.collections.new(name); scene.collection.children.link(c); COLS[name] = c
    return COLS[name]

# ---------- materials ----------
def principled(name, color, metal=0.0, rough=0.4, **extra):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    for k, v in extra.items():
        b.inputs[k].default_value = v
    return m

def link(m, a, sock_a, b, sock_b):
    m.node_tree.links.new(a.outputs[sock_a], b.inputs[sock_b])

def grid_mask(m, scale_x, scale_y, width):
    """Return a node whose Value is 1 on thin grid lines (procedural traces / electrodes)."""
    n = m.node_tree.nodes
    tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); link(m, tc, 'Object', sep, 'Vector')
    outs = []
    for axis, s in (('X', scale_x), ('Y', scale_y)):
        mul = n.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = s
        link(m, sep, axis, mul, 0)
        fr = n.new('ShaderNodeMath'); fr.operation = 'FRACT'; link(m, mul, 0, fr, 0)
        lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = width
        link(m, fr, 0, lt, 0); outs.append(lt)
    mx = n.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'
    link(m, outs[0], 0, mx, 0); link(m, outs[1], 0, mx, 1)
    return mx

M = {}
M['glass'] = principled('cover_glass', (0.9, 0.95, 1.0), 0, 0.02, **{'Transmission Weight': 1.0, 'IOR': 1.5})
M['graphite'] = principled('graphite_frame', (0.05, 0.055, 0.06), 1.0, 0.28)
M['aluminium'] = principled('midframe_aluminium', (0.55, 0.57, 0.6), 1.0, 0.38)
M['shield'] = principled('shield_can_tinplate', (0.78, 0.79, 0.8), 1.0, 0.22)
M['solder'] = principled('solder_SAC', (0.8, 0.8, 0.82), 1.0, 0.18)
M['substrate'] = principled('package_substrate', (0.12, 0.1, 0.05), 0.0, 0.45)
M['mold'] = principled('mold_compound', (0.008, 0.008, 0.009), 0.0, 0.72)
M['backglass'] = principled('back_glass_frosted', (0.03, 0.035, 0.04), 0.0, 0.35, **{'Coat Weight': 0.6})
M['battery'] = principled('battery_pouch', (0.06, 0.06, 0.065), 0.4, 0.5)
M['component'] = principled('smd_component', (0.32, 0.27, 0.2), 0.0, 0.5)
M['silicon_back'] = principled('die_silicon_backside', (0.33, 0.34, 0.36), 0.9, 0.12)

# PCB: dark solder mask with copper traces
m = principled('pcb_soldermask', (0.015, 0.035, 0.03), 0.0, 0.35); M['pcb'] = m
n = m.node_tree.nodes; waves = []
for direction, sc in (('X', 2.3), ('Y', 3.1)):   # routed traces seen through solder mask, not a tile grid
    wv = n.new('ShaderNodeTexWave'); wv.bands_direction = direction; wv.inputs['Scale'].default_value = sc
    wv.inputs['Distortion'].default_value = 1.5; wv.inputs['Detail'].default_value = 1.0
    th = n.new('ShaderNodeMath'); th.operation = 'GREATER_THAN'; th.inputs[1].default_value = 0.93
    link(m, wv, 'Fac', th, 0); waves.append(th)
mask = n.new('ShaderNodeMath'); mask.operation = 'MAXIMUM'; link(m, waves[0], 0, mask, 0); link(m, waves[1], 0, mask, 1)
mix = n.new('ShaderNodeMix'); mix.data_type = 'RGBA'
mix.inputs[6].default_value = (0.015, 0.035, 0.03, 1); mix.inputs[7].default_value = (0.05, 0.13, 0.09, 1)
link(m, mask, 0, mix, 'Factor'); link(m, mix, 2, n['Principled BSDF'], 'Base Color')

# Touch layer: near-invisible film with faint cyan ITO electrode grid
m = principled('touch_ITO', (0.8, 0.9, 1.0), 0, 0.05, **{'Transmission Weight': 1.0, 'Alpha': 0.25}); M['touch'] = m
mask = grid_mask(m, 2.2, 2.2, 0.04)
em = m.node_tree.nodes['Principled BSDF']
em.inputs['Emission Color'].default_value = (0.2, 0.9, 1.0, 1)
dim = m.node_tree.nodes.new('ShaderNodeMath'); dim.operation = 'MULTIPLY'; dim.name = 'touch_on'
dim.inputs[1].default_value = 0.0; dim.inputs[1].keyframe_insert('default_value', frame=1)
dim.inputs[1].default_value = 0.15; dim.inputs[1].keyframe_insert('default_value', frame=50)
link(m, mask, 0, dim, 0); link(m, dim, 0, em, 'Emission Strength')

# OLED: RGB sub-pixel stripes, emissive
m = bpy.data.materials.new('oled_subpixels'); m.use_nodes = True; M['oled'] = m
n = m.node_tree.nodes; b = n['Principled BSDF']
b.inputs['Base Color'].default_value = (0.01, 0.01, 0.012, 1); b.inputs['Roughness'].default_value = 0.3
tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); link(m, tc, 'Object', sep, 'Vector')
fx = n.new('ShaderNodeMath'); fx.operation = 'MULTIPLY'; fx.inputs[1].default_value = 120.0; link(m, sep, 'X', fx, 0)
fr = n.new('ShaderNodeMath'); fr.operation = 'FRACT'; link(m, fx, 0, fr, 0)
ramp = n.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
els = ramp.color_ramp.elements
els[0].position, els[0].color = 0.0, (1, 0.05, 0.05, 1)
els[1].position, els[1].color = 0.33, (0.05, 1, 0.1, 1)
e = els.new(0.66); e.color = (0.1, 0.25, 1, 1)
e = els.new(0.95); e.color = (0, 0, 0, 1)
link(m, fr, 0, ramp, 'Fac'); link(m, ramp, 'Color', b, 'Emission Color')
fy = n.new('ShaderNodeMath'); fy.operation = 'MULTIPLY'; fy.inputs[1].default_value = 120.0; link(m, sep, 'Y', fy, 0)
fry = n.new('ShaderNodeMath'); fry.operation = 'FRACT'; link(m, fy, 0, fry, 0)
gap = n.new('ShaderNodeMath'); gap.operation = 'LESS_THAN'; gap.inputs[1].default_value = 0.8; link(m, fry, 0, gap, 0)
st = n.new('ShaderNodeMath'); st.operation = 'MULTIPLY'; st.inputs[1].default_value = 1.6; link(m, gap, 0, st, 0)
link(m, st, 0, b, 'Emission Strength')
st.name = 'screen_on'   # keyed: screen dark at rest (frame 1), lit when exploded (frame 50)
st.inputs[1].default_value = 0.0; st.inputs[1].keyframe_insert('default_value', frame=1)
st.inputs[1].default_value = 0.55; st.inputs[1].keyframe_insert('default_value', frame=24)

# TFT backplane: dark film with gold gate/data lines
m = principled('tft_backplane', (0.02, 0.02, 0.025), 0.0, 0.3); M['tft'] = m
mask = grid_mask(m, 40.0, 40.0, 0.1)
mix = m.node_tree.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
mix.inputs[6].default_value = (0.02, 0.02, 0.025, 1); mix.inputs[7].default_value = (0.9, 0.7, 0.3, 1)
link(m, mask, 0, mix, 'Factor'); link(m, mix, 2, m.node_tree.nodes['Principled BSDF'], 'Base Color')
link(m, mask, 0, m.node_tree.nodes['Principled BSDF'], 'Metallic')

# Die circuit face: copper top metal with thin-film iridescence (Cycles only, per manual)
m = principled('die_topmetal_iridescent', (0.55, 0.38, 0.28), 1.0, 0.16); M['die_face'] = m
b = m.node_tree.nodes['Principled BSDF']
noise = m.node_tree.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 9.0; noise.inputs['Detail'].default_value = 4.0
rng = m.node_tree.nodes.new('ShaderNodeMapRange')
rng.inputs['To Min'].default_value = 200.0; rng.inputs['To Max'].default_value = 900.0
link(m, noise, 'Fac', rng, 'Value')
thin_film = 'Thin Film Thickness' in b.inputs
if thin_film:
    link(m, rng, 'Result', b, 'Thin Film Thickness'); b.inputs['Thin Film IOR'].default_value = 1.45
mask = grid_mask(m, 60.0, 60.0, 0.12)
rr = m.node_tree.nodes.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value = 0.12; rr.inputs['To Max'].default_value = 0.4
link(m, mask, 0, rr, 'Value'); link(m, rr, 'Result', b, 'Roughness')

# ---------- geometry helpers ----------
def rr_outline(w, h, r, seg=10):
    pts = []
    for cx, cy, a0 in ((w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)):
        for i in range(seg + 1):
            a = math.radians(a0 + 90 * i / seg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def slab(name, w, h, r, z0, z1, mat, coll, center=(0, 0)):
    bm = bmesh.new()
    vs = [bm.verts.new((x + center[0], y + center[1], z0)) for x, y in rr_outline(w, h, r)]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, vec=(0, 0, z1 - z0), verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col(coll).objects.link(o); o.data.materials.append(mat)
    return o

def ring(name, w, h, r, t, z0, z1, mat, coll):
    """Side band: outer and inner rounded outlines bridged into a closed tube."""
    bm = bmesh.new()
    outer, inner = rr_outline(w, h, r), rr_outline(w - 2*t, h - 2*t, max(r - t, 0.05))
    loops = [[bm.verts.new((x, y, z)) for x, y in pts] for pts, z in ((outer, z0), (outer, z1), (inner, z1), (inner, z0))]
    n = len(outer)
    for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((loops[a][i], loops[a][j], loops[b][j], loops[b][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col(coll).objects.link(o); o.data.materials.append(mat)
    return o

def box(name, size, loc, mat, coll, bevel=0.0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = loc; col(coll).objects.link(o); o.data.materials.append(mat)
    if bevel:
        mod = o.modifiers.new('bevel', 'BEVEL'); mod.width = bevel; mod.segments = 3
    return o

def ball_array(name, nx, ny, pitch, center, z, radius, coll, skip_inner=0):
    """Solder balls merged into one mesh (instancing double-offset them once the host was animated)."""
    bm = bmesh.new()
    for i in range(nx):
        for j in range(ny):
            if skip_inner and skip_inner <= i < nx - skip_inner and skip_inner <= j < ny - skip_inner:
                continue
            r = bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=radius)
            bmesh.ops.translate(bm, vec=((i - (nx - 1) / 2) * pitch + center[0], (j - (ny - 1) / 2) * pitch + center[1], z), verts=r['verts'])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); col(coll).objects.link(o); o.data.materials.append(M['solder'])
    return o

# ---------- build, back to front ----------
parts = {}  # name -> (object, explode z offset)
def add(o, off):
    parts[o.name] = (o, off); return o

add(slab('back_glass', W, H, R, 0.0, 0.06, M['backglass'], '02_HERO_PHONE'), -1.6)
add(ring('frame_band', W, H, R, 0.12, 0.0, 0.78, M['graphite'], '02_HERO_PHONE'), 0.0)
add(box('battery', (W - 1.2, 7.2, 0.42), (0, -3.0, 0.29), M['battery'], '02_HERO_PHONE', 0.08), -0.8)
add(box('logic_board', (W - 1.0, 4.6, 0.1), (0, 4.4, 0.25), M['pcb'], '03_LOGIC_BOARD', 0.02), 0.0)
for k in range(140):  # passives, kept clear of the SoC/shield area
    x, y = random.uniform(-2.9, 2.9), random.uniform(2.3, 6.5)
    if abs(x - SOC.x) < 1.4 and abs(y - SOC.y) < 1.4:
        continue
    s = random.choice(((0.1, 0.05, 0.05), (0.06, 0.03, 0.03), (0.3, 0.3, 0.06), (0.16, 0.08, 0.06)))
    add(box(f'smd_{k:03d}', s, (x, y, 0.3 + s[2] / 2), M['component'], '03_LOGIC_BOARD'), 0.0)

# PoP: AP balls > substrate > (die face-down on bumps, in mold) > DRAM balls > DRAM package
add(ball_array('ap_balls', 14, 14, 0.1, SOC, 0.315, 0.017, '04_POP_SOC'), 0.0)
add(box('ap_substrate', (1.45, 1.45, 0.03), (SOC.x, SOC.y, 0.345), M['substrate'], '04_POP_SOC'), 0.0)
add(ball_array('die_microbumps', 30, 30, 0.032, SOC, 0.3385, 0.006, '04_POP_SOC'), 0.0)
die = add(box('ap_die', (1.0, 1.0, 0.03), (SOC.x, SOC.y, 0.385), M['silicon_back'], '04_POP_SOC'), 0.0)
die.data.materials.append(M['die_face'])
for p in die.data.polygons:      # circuit side faces DOWN (flip-chip)
    if p.normal.z < -0.5:
        p.material_index = 1
add(box('ap_mold', (1.45, 1.45, 0.045), (SOC.x, SOC.y, 0.3825), M['mold'], '04_POP_SOC'), 0.0)
add(ball_array('dram_balls', 12, 12, 0.12, SOC, 0.418, 0.02, '04_POP_SOC', skip_inner=2), 0.55)
add(box('dram_package', (1.45, 1.45, 0.07), (SOC.x, SOC.y, 0.473), M['mold'], '04_POP_SOC', 0.01), 0.55)
can = add(box('shield_can', (2.3, 2.3, 0.24), (SOC.x, SOC.y, 0.42), M['shield'], '03_LOGIC_BOARD', 0.02), 1.1)
bm = bmesh.new(); bm.from_mesh(can.data)   # a shield can is a lid soldered over the parts: no bottom
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.normal.z < -0.5], context='FACES_ONLY')
bm.to_mesh(can.data); bm.free()
can.modifiers.new('solidify', 'SOLIDIFY').thickness = 0.01

add(slab('midframe', W - 0.3, H - 0.3, R - 0.15, 0.56, 0.64, M['aluminium'], '02_HERO_PHONE'), 2.0)
add(slab('tft_backplane', W - 0.3, H - 0.3, R - 0.15, 0.648, 0.66, M['tft'], '01_DISPLAY_STACK'), 3.0)
add(slab('oled_emitters', W - 0.3, H - 0.3, R - 0.15, 0.665, 0.68, M['oled'], '01_DISPLAY_STACK'), 3.8)
add(slab('touch_layer', W - 0.3, H - 0.3, R - 0.15, 0.685, 0.695, M['touch'], '01_DISPLAY_STACK'), 4.8)
add(slab('cover_glass', W - 0.06, H - 0.06, R - 0.03, 0.70, 0.78, M['glass'], '01_DISPLAY_STACK'), 6.0)

for o, off in parts.values():
    o['explode_offset'] = off   # keyed per shot in the v007 tail

# ---------- light, world, render ----------
lc = col('04_LIGHTING')
def area(name, loc, energy, size, color):
    d = bpy.data.lights.new(name, 'AREA'); d.energy = energy; d.size = size; d.color = color
    o = bpy.data.objects.new(name, d); o.location = loc; lc.objects.link(o)
    o.rotation_euler = (Vector((0, 2, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return o
area('key_softbox', (-25, -20, 40), 18000, 30, (1.0, 0.97, 0.92))
area('rim_cyan', (28, 32, 12), 9000, 15, (0.45, 0.85, 1.0))
area('fill_low', (20, -35, 8), 2500, 25, (0.8, 0.85, 1.0))
under = area('die_under_reflector', (SOC.x + 1.6, SOC.y + 2.2, -0.5), 2.5, 0.7, (0.95, 0.97, 1.0))
under.rotation_euler = (Vector((SOC.x, SOC.y, 0.37)) - under.location).to_track_quat('-Z', 'Y').to_euler()
under.visible_camera = False
under.hide_render = True   # only for the cutaway look at the die face
scene.world = bpy.data.worlds.new('studio_dark'); scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.006, 0.007, 0.009, 1)

scene.render.engine = 'CYCLES'; gpu(scene, 'auto')
scene.cycles.samples = 32; scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 640, 360
scene.view_settings.view_transform = 'AgX'
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, EXPLODED

# ============ v006: S01 camera shots (appended to the v005 asset build) ============
# Frames @24 fps, locked to the approved narration (production/timing-map.md; words from edit/captions/ep004_words_master.json)
#   Shot A  f001-f102  21.94-26.20 s  01-09 push-through   "Inside them, billions of microscopic switches process information."
#   Shot B  f201-f320  30.33-35.32 s  01-12 chip dive      "So why is building the chips themselves such a difficult challenge?"
#           (freeze beat 29.73-30.33 = frame 201 held in the edit; f201 pose == f102 pose)
#   Shot C  f401-f422  35.32-36.24 s  01-13 tail           die tiles outward -> wafer, hand-off to S02
import numpy as np, tempfile, json
from bpy_extras.object_utils import world_to_camera_view
scene.render.fps = 24
SX, SY = SOC.x, SOC.y

# ---- A: staged layer separation, just ahead of the camera ----
STAGE = {'cover_glass': (1, 14), 'touch_layer': (6, 24), 'oled_emitters': (10, 30), 'tft_backplane': (20, 40),
         'midframe': (30, 50), 'shield_can': (40, 62), 'dram_package': (70, 98), 'dram_balls': (70, 98),
         'back_glass': (1, 50), 'battery': (1, 50)}
for name, (f0, f1) in STAGE.items():
    o, off = parts[name]
    base = o.location.z                       # box() parts carry their height here; slab() parts are 0
    o.keyframe_insert('location', index=2, frame=1 if f0 > 1 else f0)
    if f0 > 1:
        o.keyframe_insert('location', index=2, frame=f0)
    o.location.z = base + off
    o.keyframe_insert('location', index=2, frame=f1)

def alpha_key(mat, f0, f1, a0=1.0):          # layer dissolves as the camera crosses it
    sock = mat.node_tree.nodes['Principled BSDF'].inputs['Alpha']
    sock.default_value = a0; sock.keyframe_insert('default_value', frame=f0)
    sock.default_value = 0.0; sock.keyframe_insert('default_value', frame=f1)
alpha_key(M['touch'], 22, 25, 0.25); alpha_key(M['oled'], 40, 43); alpha_key(M['tft'], 42, 45)
alpha_key(M['aluminium'], 52, 55); alpha_key(M['shield'], 64, 67)

# ---- B: board / substrate / balls drop away so the camera can see the face-down die from below ----
drop = bpy.data.objects.new('board_drop', None); col('03_LOGIC_BOARD').objects.link(drop)
for name, (o, off) in parts.items():
    if name in ('logic_board', 'ap_balls', 'ap_substrate', 'frame_band', 'battery', 'back_glass') or name.startswith('smd_'):
        o.parent = drop
drop.location.z = 0.0; drop.keyframe_insert('location', index=2, frame=205)
drop.location.z = -10.0; drop.keyframe_insert('location', index=2, frame=240)
drop.keyframe_insert('location', index=2, frame=320)
drop.location.z = -400.0; drop.keyframe_insert('location', index=2, frame=321)      # gone before the wafer pull-back
for name, (o, off) in parts.items():                                                  # C shows only the die + wafer
    if name not in ('ap_die', 'die_microbumps'):
        o.hide_render = False; o.keyframe_insert('hide_render', frame=320)
        o.hide_render = True; o.keyframe_insert('hide_render', frame=321)
# midframe window so the camera sees the board through it (real midframes have cut-outs)
cut = box('midframe_window_cutter', (3.8, 3.8, 4.2), (SX, SY, 1.5), M['aluminium'], '02_HERO_PHONE')
cut.hide_render = True; cut.display_type = 'WIRE'
bm_ = parts['midframe'][0].modifiers.new('window', 'BOOLEAN'); bm_.object = cut; bm_.operation = 'DIFFERENCE'; bm_.solver = 'EXACT'
rl = bpy.data.objects['die_under_reflector']; rl.hide_render = False
rl.data.energy = 0.0; rl.data.keyframe_insert('energy', frame=215)
rl.data.energy = 8.0; rl.data.keyframe_insert('energy', frame=235)
rl.location = (SX, SY, -3.0); rl.data.size = 2.5; rl.rotation_euler = (math.pi, 0, 0)    # straight below the die: no mirror glare
wl = area('wafer_light', (SX, SY, -20.0), 0.0, 45.0, (0.9, 0.95, 1.0)); wl.rotation_euler = (math.pi, 0, 0); wl.visible_camera = False
wl.data.keyframe_insert('energy', frame=400); wl.data.energy = 3500.0; wl.data.keyframe_insert('energy', frame=403)

mold = bpy.data.objects['ap_mold']
hole = box('mold_hole_cutter', (1.04, 1.04, 0.2), (SX, SY, 0.385), M['mold'], '04_POP_SOC')
hm = mold.modifiers.new('hole', 'BOOLEAN'); hm.object = hole; hm.operation = 'DIFFERENCE'; hm.solver = 'EXACT'
new_me = bpy.data.meshes.new_from_object(mold.evaluated_get(bpy.context.evaluated_depsgraph_get()))
mold.modifiers.remove(hm); mold.data = new_me; bpy.data.objects.remove(hole, do_unlink=True)

# ---- die metal stack, built below the die face (top metal M6 furthest from silicon) ----
T, GAP = 0.0040, 0.0005
def line_node(m, axis, scale, width):
    n = m.node_tree.nodes
    tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); link(m, tc, 'Object', sep, 'Vector')
    mul = n.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = scale; link(m, sep, axis, mul, 0)
    fr = n.new('ShaderNodeMath'); fr.operation = 'FRACT'; link(m, mul, 0, fr, 0)
    lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = width; link(m, fr, 0, lt, 0)
    return lt
def wire_mat(name, axes, width, copper):
    m = principled(name, (0.02, 0.025, 0.035), 1.0, 0.3); n = m.node_tree.nodes; b = n['Principled BSDF']
    nodes = [line_node(m, ax, sc, width) for ax, sc in axes]
    mask = nodes[0]
    if len(nodes) > 1:
        mask = n.new('ShaderNodeMath'); mask.operation = 'MAXIMUM'; link(m, nodes[0], 0, mask, 0); link(m, nodes[1], 0, mask, 1)
    mix = n.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs[6].default_value = (0.02, 0.025, 0.035, 1); mix.inputs[7].default_value = (*copper, 1)
    link(m, mask, 0, mix, 'Factor'); link(m, mix, 2, b, 'Base Color')
    return m
WIRING = {1: (('X', 420), ('Y', 420)), 2: (('X', 260),), 3: (('Y', 200),), 4: (('X', 150),), 5: (('Y', 110),)}
layers = {}
for k in range(1, 7):
    zt = 0.368 - (k - 1) * (T + GAP)
    mat = M['die_face'] if k == 6 else wire_mat(f'die_M{k}_wiring', WIRING[k], 0.45, (0.85, 0.5, 0.25) if k % 2 else (0.7, 0.55, 0.35))
    layers[k] = slab(f'die_M{k}', 1.0, 1.0, 0.01, zt - T, zt, mat, '04_POP_SOC')
bump_host = bpy.data.objects['die_microbumps']; bump_host.parent = layers[6]

# transistor field: stylised greyscale, SEM-like (illustrative; transistors are below the optical limit)
m = principled('die_transistor_field_SEM', (0.07, 0.07, 0.075), 0.2, 0.45); M['field'] = m
n = m.node_tree.nodes; b = n['Principled BSDF']
fins = line_node(m, 'X', 260, 0.38); gates = line_node(m, 'Y', 160, 0.30)
prod = n.new('ShaderNodeMath'); prod.operation = 'MAXIMUM'; link(m, fins, 0, prod, 0); link(m, gates, 0, prod, 1)
noise = n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 900.0; noise.inputs['Detail'].default_value = 6.0
mixg = n.new('ShaderNodeMix'); mixg.data_type = 'RGBA'
mixg.inputs[6].default_value = (0.05, 0.05, 0.055, 1); mixg.inputs[7].default_value = (0.62, 0.62, 0.64, 1)
fac = n.new('ShaderNodeMath'); fac.operation = 'MULTIPLY'; link(m, prod, 0, fac, 0); link(m, noise, 'Fac', fac, 1)
fac.inputs[1].default_value = 1.0
link(m, prod, 0, mixg, 'Factor'); link(m, mixg, 2, b, 'Base Color'); link(m, mixg, 2, b, 'Emission Color')
b.inputs['Emission Strength'].default_value = 0.6
bump = n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.8; bump.inputs['Distance'].default_value = 0.0004
link(m, prod, 0, bump, 'Height'); link(m, bump, 'Normal', b, 'Normal')
field = slab('die_transistor_field', 1.0, 1.0, 0.01, 0.3685, 0.3695, m, '04_POP_SOC')

PEEL = {6: 247, 5: 251, 4: 255, 3: 259, 2: 263, 1: 267}      # slide off sideways, outermost first
RET = {1: 402, 2: 403, 3: 404, 4: 405, 5: 406, 6: 407}        # slide back in C so the die matches its neighbours
for k, o in layers.items():
    for f, x in ((PEEL[k], 0.0), (PEEL[k] + 11, 1.6), (RET[k], 1.6), (RET[k] + 4, 0.0)):
        o.location.x = x; o.keyframe_insert('location', index=0, frame=f)

# ---- C: wafer of identical dies, revealed outward from the hero die ----
WP = 1.08
wb = bmesh.new(); bmesh.ops.create_circle(wb, cap_ends=True, radius=15.0, segments=96)
me = bpy.data.meshes.new('wafer_disc'); wb.to_mesh(me); wb.free()
wdisc = bpy.data.objects.new('wafer_disc', me); wdisc.location = (SX, SY, 0.4015); col('06_WAFER').objects.link(wdisc)
tb = bmesh.new()
for i in range(-14, 15):
    for j in range(-14, 15):
        cx, cy = i * WP, j * WP
        if (i == 0 and j == 0) or math.hypot(cx, cy) > 14.2:
            continue
        c = bmesh.ops.create_cube(tb, size=1.0); bmesh.ops.scale(tb, vec=(1.0, 1.0, 0.0596), verts=c['verts'])
        bmesh.ops.translate(tb, vec=(cx, cy, 0.0298), verts=c['verts'])
me = bpy.data.meshes.new('wafer_dies'); tb.to_mesh(me); tb.free()
wdies = bpy.data.objects.new('wafer_dies', me); wdies.location = (SX, SY, 0.3414); col('06_WAFER').objects.link(wdies)

def reveal(mat, radii):
    nt = mat.node_tree; nn = nt.nodes
    out = [x for x in nn if x.type == 'OUTPUT_MATERIAL'][0]
    src = out.inputs['Surface'].links[0].from_node
    tc = nn.new('ShaderNodeTexCoord'); vl = nn.new('ShaderNodeVectorMath'); vl.operation = 'LENGTH'
    nt.links.new(tc.outputs['Object'], vl.inputs[0])
    lt = nn.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; nt.links.new(vl.outputs['Value'], lt.inputs[0])
    for f, r in radii:
        lt.inputs[1].default_value = r; lt.inputs[1].keyframe_insert('default_value', frame=f)
    tr = nn.new('ShaderNodeBsdfTransparent'); mx = nn.new('ShaderNodeMixShader')
    nt.links.new(lt.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1])
    nt.links.new(src.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs['Surface'])
RAD = ((1, 0.0), (400, 0.0), (401, 0.6), (410, 3.5), (416, 9.0), (422, 17.0))
md = M['die_face'].copy(); md.name = 'wafer_die_tiles'; reveal(md, RAD); wdies.data.materials.append(md)
mw = principled('wafer_silicon', (0.30, 0.31, 0.33), 1.0, 0.1); reveal(mw, RAD); wdisc.data.materials.append(mw)

# ---- cameras: explicit euler from pos/target (no Track-To, which flips when looking straight up) ----
cc = col('05_CAMERAS')
def euler_for(pos, tgt, prev):
    d = Vector(tgt) - Vector(pos); d.normalize()
    rx = math.acos(max(-1.0, min(1.0, -d.z)))
    rz = math.atan2(-d.x, d.y) if math.hypot(d.x, d.y) > 1e-4 else prev
    while rz - prev > math.pi: rz -= 2 * math.pi
    while rz - prev < -math.pi: rz += 2 * math.pi
    return (rx, 0.0, rz)
def make_cam(name, lens, keys, lens_keys=(), prev=0.0):
    d = bpy.data.cameras.new(name); d.lens = lens; d.sensor_width = 36; d.clip_start = 0.0004; d.clip_end = 600
    o = bpy.data.objects.new(name, d); cc.objects.link(o)
    for f, pos, tgt in keys:
        e = euler_for(pos, tgt, prev); prev = e[2]
        o.location = pos; o.rotation_euler = e
        o.keyframe_insert('location', frame=f); o.keyframe_insert('rotation_euler', frame=f)
    for f, l in lens_keys:
        d.lens = l; d.keyframe_insert('lens', frame=f)
    o['last_rz'] = prev
    return o

KA = [(1, (-15, -21, 17), (0.0, 0.5, 0.4)),
      (19, (SX - 1.2, SY - 2.2, 7.4), (SX, SY, 4.5)),
      (27, (SX - 0.7, SY - 1.1, 4.85), (SX - 0.1, SY - 0.5, 4.5)),        # OLED sub-pixel macro on "billions"
      (40, (SX - 0.3, SY - 0.1, 4.72), (SX + 0.1, SY + 0.5, 4.5)),
      (50, (SX - 0.9, SY - 1.7, 3.0), (SX, SY, 1.5)),
      (62, (SX - 1.6, SY - 2.4, 1.9), (SX, SY, 0.5)),
      (78, (SX - 2.4, SY - 3.2, 0.85), (SX, SY, 0.55)),
      (102, (SX - 1.55, SY - 2.1, 0.68), (SX, SY, 0.62))]                 # ends in the PoP gap: balls + underfill
KB = [(201, KA[-1][1], KA[-1][2]),
      (217, (SX - 2.2, SY - 3.2, 0.45), (SX, SY, 0.55)),
      (231, (SX - 1.9, SY - 2.7, -0.75), (SX, SY, 0.36)),                 # "building": die face, iridescent top metal
      (247, (SX - 1.1, SY - 1.55, -0.5), (SX, SY, 0.35)),                 # "chips": peel begins
      (270, (SX - 0.55, SY - 0.8, -0.3), (SX, SY, 0.35)),
      (284, (SX - 0.28, SY - 0.4, -0.1), (SX, SY, 0.369)),               # "such a": transistor field exposed
      (300, (SX - 0.06, SY - 0.08, 0.2), (SX, SY, 0.369)),
      (320, (SX - 0.004, SY - 0.006, 0.305), (SX, SY, 0.369))]            # "challenge?": field fills the frame
KC = [(401, KB[-1][1], KB[-1][2]),
      (407, (SX - 0.01, SY - 0.02, -1.0), (SX, SY, 0.34)),
      (412, (SX, SY - 0.1, -5.0), (SX, SY, 0.34)),
      (417, (SX, SY - 0.2, -18.0), (SX, SY, 0.34)),
      (422, (SX, SY - 0.3, -46.0), (SX, SY, 0.34))]
camA = make_cam('CAM_S01_A_pushthrough', 40, KA)
camB = make_cam('CAM_S01_B_dive', 50, KB, prev=camA['last_rz'])
camC = make_cam('CAM_S01_C_wafer', 50, KC, lens_keys=((401, 50), (422, 28)), prev=camB['last_rz'])
for f, c in ((1, camA), (201, camB), (401, camC)):
    scene.timeline_markers.new(c.name[:9], frame=f).camera = c
scene.frame_start, scene.frame_end = 1, 422

# ---- verification: camera speed, framing of the subject, then 8-tile contact sheets (no video render) ----
metrics = {}
def check(cam, f0, f1, point, probes):
    scene.camera = cam; prev = None; maxd = (0, 0); pr = {}
    for f in range(f0, f1 + 1):
        scene.frame_set(f); p = cam.matrix_world.translation.copy()
        if prev is not None and (p - prev).length > maxd[0]:
            maxd = ((p - prev).length, f)
        prev = p
        if f in probes:
            v = world_to_camera_view(scene, cam, Vector(point))
            pr[f] = (round(v.x, 2), round(v.y, 2), round(v.z, 3))
    return dict(max_step_cm_per_frame=round(maxd[0], 3), at_frame=maxd[1], subject_xy_dist=pr)
metrics['A'] = check(camA, 1, 102, (SX, SY, 0.5), (19, 27, 40, 50, 62, 78, 90, 102))
metrics['B'] = check(camB, 201, 320, (SX, SY, 0.369), (201, 217, 231, 247, 270, 284, 300, 320))
metrics['C'] = check(camC, 401, 422, (SX, SY, 0.341), (401, 407, 412, 417, 422))

tmp = tempfile.mkdtemp()
def sheet(frames, cam, fname, w=480, h=270, spp=24):
    scene.render.resolution_x, scene.render.resolution_y = w, h; scene.cycles.samples = spp; scene.camera = cam
    tiles = []
    for f in frames:
        scene.frame_set(f); p = os.path.join(tmp, f'{fname}_{f}.png'); scene.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p); tiles.append(np.array(im.pixels[:]).reshape(h, w, 4))
    rows = [np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]
    sh = np.vstack(rows[::-1])                       # blender pixel rows are bottom-up
    si = bpy.data.images.new(fname, sh.shape[1], sh.shape[0], alpha=True)
    si.pixels = sh.ravel().tolist(); si.filepath_raw = os.path.join(out, fname + '.png'); si.file_format = 'PNG'; si.save()
sheet([1, 19, 30, 38, 50, 66, 84, 102], camA, 'sheet_A_pushthrough_f001-102')
sheet([201, 217, 231, 247, 262, 284, 300, 320], camB, 'sheet_B_dive_f201-320')
sheet([401, 404, 407, 410, 413, 416, 419, 422], camC, 'sheet_C_wafer_f401-422')

scene.frame_set(1); scene.camera = camA
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s01_camera_v008.blend'), copy=True)
result.update(metrics=metrics, objects=len(bpy.data.objects))
