# EP004 hero phone v004 (die-underside camera pulled back, stronger thin-film variation; v003 = touch grid dark at rest, under-light hidden from camera; v002 fixes: screen off at rest, organic PCB traces, softer key, die under-light): procedural smartphone with a separable stack down to a face-down die.
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
st.inputs[1].default_value = 1.6; st.inputs[1].keyframe_insert('default_value', frame=50)

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
    """Solder balls as vertex instances of one sphere (cheap for hundreds)."""
    bm = bmesh.new()
    for i in range(nx):
        for j in range(ny):
            if skip_inner and skip_inner <= i < nx - skip_inner and skip_inner <= j < ny - skip_inner:
                continue
            bm.verts.new((center[0] + (i - (nx - 1) / 2) * pitch, center[1] + (j - (ny - 1) / 2) * pitch, z))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    host = bpy.data.objects.new(name, me); col(coll).objects.link(host); host.instance_type = 'VERTS'
    sbm = bmesh.new(); bmesh.ops.create_uvsphere(sbm, u_segments=12, v_segments=8, radius=radius)
    sme = bpy.data.meshes.new(name + '_ball'); sbm.to_mesh(sme); sbm.free()
    for p in sme.polygons: p.use_smooth = True
    ball = bpy.data.objects.new(name + '_ball', sme); ball.data.materials.append(M['solder'])
    col(coll).objects.link(ball); ball.parent = host
    return host

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
add(ball_array('die_microbumps', 30, 30, 0.032, SOC, 0.364, 0.006, '04_POP_SOC'), 0.0)
die = add(box('ap_die', (1.0, 1.0, 0.03), (SOC.x, SOC.y, 0.385), M['silicon_back'], '04_POP_SOC'), 0.0)
die.data.materials.append(M['die_face'])
for p in die.data.polygons:      # circuit side faces DOWN (flip-chip)
    if p.normal.z < -0.5:
        p.material_index = 1
add(box('ap_mold', (1.45, 1.45, 0.045), (SOC.x, SOC.y, 0.3825), M['mold'], '04_POP_SOC'), 0.0)
add(ball_array('dram_balls', 12, 12, 0.12, SOC, 0.418, 0.02, '04_POP_SOC', skip_inner=2), 0.55)
add(box('dram_package', (1.45, 1.45, 0.07), (SOC.x, SOC.y, 0.473), M['mold'], '04_POP_SOC', 0.01), 0.55)
add(box('shield_can', (2.3, 2.3, 0.24), (SOC.x, SOC.y, 0.42), M['shield'], '03_LOGIC_BOARD', 0.02), 1.1)

add(slab('midframe', W - 0.3, H - 0.3, R - 0.15, 0.56, 0.64, M['aluminium'], '02_HERO_PHONE'), 2.0)
add(slab('tft_backplane', W - 0.3, H - 0.3, R - 0.15, 0.648, 0.66, M['tft'], '01_DISPLAY_STACK'), 3.0)
add(slab('oled_emitters', W - 0.3, H - 0.3, R - 0.15, 0.665, 0.68, M['oled'], '01_DISPLAY_STACK'), 3.8)
add(slab('touch_layer', W - 0.3, H - 0.3, R - 0.15, 0.685, 0.695, M['touch'], '01_DISPLAY_STACK'), 4.8)
add(slab('cover_glass', W - 0.06, H - 0.06, R - 0.03, 0.70, 0.78, M['glass'], '01_DISPLAY_STACK'), 6.0)

for o, off in parts.values():  # frame 1 assembled, frame 50 exploded
    o.keyframe_insert('location', index=2, frame=1)
    o.location.z += off
    o.keyframe_insert('location', index=2, frame=EXPLODED)
    o.location.z -= off
    o['explode_offset'] = off
    if o.animation_data and o.animation_data.action:
        for fc in getattr(o.animation_data.action, 'fcurves', []):
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'; kp.easing = 'EASE_IN_OUT'

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

# ---------- preview stills ----------
cc = col('05_CAMERAS')
def cam(name, loc, target, lens):
    d = bpy.data.cameras.new(name); d.lens = lens; d.clip_start = 0.005; d.clip_end = 500
    o = bpy.data.objects.new(name, d); o.location = loc; cc.objects.link(o)
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return o

hide_for_underside = ['logic_board', 'back_glass', 'frame_band', 'battery', 'ap_substrate', 'ap_mold', 'ap_balls']
STILLS = [
    ('a_hero_assembled', cam('CAM_hero', (-17, -24, 19), (0, 0.5, 0), 50), 1, []),
    ('b_exploded_stack', cam('CAM_exploded', (-17, -21, 15), (0, 1.0, 2.6), 40), EXPLODED, []),
    ('c_pop_closeup', cam('CAM_pop', (SOC.x - 2.4, SOC.y - 3.0, 2.0), (SOC.x, SOC.y, 0.5), 60), EXPLODED, ['shield_can']),
    ('d_die_underside', cam('CAM_die_under', (SOC.x - 2.0, SOC.y - 2.9, -0.55), (SOC.x, SOC.y, 0.37), 70), 1, hide_for_underside),
]
os.makedirs(os.path.join(out, 'stills'), exist_ok=True)
paths = []
for i, (label, c, frame, hide) in enumerate(STILLS):
    progress(i, len(STILLS), label)
    for name in hide: bpy.data.objects[name].hide_render = True
    bpy.data.objects['die_under_reflector'].hide_render = label != 'd_die_underside'
    scene.camera = c; scene.frame_set(frame)
    p = os.path.join(out, 'stills', label + '.png'); scene.render.filepath = p
    bpy.ops.render.render(write_still=True); paths.append(p)
    for name in hide: bpy.data.objects[name].hide_render = False

import numpy as np
tiles = []
for p in paths:
    img = bpy.data.images.load(p); px = np.array(img.pixels[:]).reshape(img.size[1], img.size[0], 4); tiles.append(px)
sheet = np.vstack([np.hstack([tiles[2], tiles[3]]), np.hstack([tiles[0], tiles[1]])])  # pixels are bottom-up
si = bpy.data.images.new('sheet', sheet.shape[1], sheet.shape[0], alpha=True)
si.pixels = sheet.ravel().tolist(); si.filepath_raw = os.path.join(out, 'contact_sheet_v004.png'); si.file_format = 'PNG'; si.save()

scene.camera = STILLS[0][1]; scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_hero_phone_v004.blend'), copy=True)
result.update(objects=len(bpy.data.objects), thin_film=thin_film, parts=len(parts))
