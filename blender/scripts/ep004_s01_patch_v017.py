# EP004 S01 patch v017 (on v016; animation is shifted +600). Targeted fixes only; no approved camera path or shot duration changes.
import bpy, os, math
from mathutils import Vector
sc = bpy.context.scene; M = bpy.data.materials; K = 600; log = {}
def fcs(act):
    o = []
    try:
        for ly in act.layers:
            for st in ly.strips:
                for cb in st.channelbags: o += list(cb.fcurves)
    except Exception: o = list(act.fcurves)
    return o
def act_of(idb):
    ad = idb.animation_data; return ad.action if ad and ad.action else None
def move_key(act, x_old, x_new, val=None):
    n = 0
    for fc in fcs(act):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - x_old) < 0.01:
                dx = x_new - kp.co.x; kp.co.x += dx; kp.handle_left.x += dx; kp.handle_right.x += dx
                if val is not None: kp.co.y = val; kp.handle_left.y = val; kp.handle_right.y = val
                n += 1
        fc.keyframe_points.sort(); fc.update()
    return n
# 1. chip dive: light the die underside as soon as the board starts to drop
rl = bpy.data.lights['die_under_reflector']; a = act_of(rl)
log['refl'] = (move_key(a, 806, 801, 45.0), move_key(a, 822, 808))
log['world'] = move_key(act_of(sc.world.node_tree), 814, 806)
for f, v in ((801, 0.0), (808, 0.9), (842, 0.9), (866, 0.0)):
    sc.view_settings.exposure = v; sc.keyframe_insert('view_settings.exposure', frame=f)
sc.view_settings.exposure = 0.0
# 2. OLED macro: dim the pixel emission slowly while they are still visible, dissolve the layer only once it is dim
st = M['oled_subpixels'].node_tree.nodes['screen_on']
for f, v in ((634, 2.4), (644, 0.5)): st.inputs[1].default_value = v; st.inputs[1].keyframe_insert('default_value', frame=f)
oa = act_of(M['oled_subpixels'].node_tree); log['oled'] = (move_key(oa, 629, 637), move_key(oa, 641, 645))
# 3. wafer: silicon look (bright polished lanes/rim, deeper blue-violet thin-film dies, brighter sheen)
ws = M['wafer_silicon'].node_tree.nodes['Principled BSDF']
ws.inputs['Base Color'].default_value = (0.66, 0.68, 0.72, 1); ws.inputs['Metallic'].default_value = 1.0; ws.inputs['Roughness'].default_value = 0.16
for nd in M['wafer_die_tiles'].node_tree.nodes:
    if nd.type == 'MAP_RANGE' and nd.inputs['To Max'].default_value > 100: nd.inputs['To Min'].default_value = 235.0; nd.inputs['To Max'].default_value = 400.0
    if nd.type == 'BSDF_PRINCIPLED':
        nd.inputs['Base Color'].default_value = (0.38, 0.4, 0.5, 1); nd.inputs['Coat Weight'].default_value = 0.5; nd.inputs['Coat Roughness'].default_value = 0.08
wl = bpy.data.lights['wafer_light']; wa = act_of(wl)
for fc in fcs(wa):
    for kp in fc.keyframe_points:
        if kp.co.y > 100: kp.co.y = 2100.0; kp.handle_left.y = 2100.0; kp.handle_right.y = 2100.0
wo = bpy.data.objects['wafer_light']; wo.location = (0.8 + 9.0, 4.6 - 12.0, -20.0)      # off-axis: soft gradient sheen across the wafer
# 4/5. Scene 02 bridge: no facet flash, cluster fully framed, gentle drift to the end
q = bpy.data.objects['CAM_Q']; q.animation_data_clear(); q.data.animation_data_clear()
Q = Vector((0, 300, 0))
def euler_for(pos, tgt, prev):
    d = Vector(tgt) - Vector(pos); d.normalize(); rx = math.acos(max(-1.0, min(1.0, -d.z)))
    rz = math.atan2(-d.x, d.y) if math.hypot(d.x, d.y) > 1e-4 else prev
    while rz - prev > math.pi: rz -= 2*math.pi
    while rz - prev < -math.pi: rz += 2*math.pi
    return (rx, 0.0, rz)
keys = ((5600, (-2.8, -4.4, 2.7), (0.3, 0, 2.9)), (5640, (-7.0, -11.0, 6.0), (0, 0, 2.7)), (5672, (-11.8, -18.6, 9.4), (0, 0, 2.3)), (5708, (-9.4, -19.4, 9.0), (0.4, 0, 2.3)))
prev = 0.0
for f, p, t in keys:
    e = euler_for(Q + Vector(p), Q + Vector(t), prev); prev = e[2]; q.location = Q + Vector(p); q.rotation_euler = e
    q.keyframe_insert('location', frame=f); q.keyframe_insert('rotation_euler', frame=f)
for f, l in ((5600, 50.0), (5672, 38.0), (5708, 38.0)): q.data.lens = l; q.data.keyframe_insert('lens', frame=f)
for nm in ('q_key', 'q_top'):
    d = bpy.data.lights[nm]; a = act_of(d)
    for fc in fcs(a):
        for kp in fc.keyframe_points:
            if kp.co.y > 100: kp.co.y *= 0.6; kp.handle_left.y *= 0.6; kp.handle_right.y *= 0.6
result['patch_log'] = log
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s01_camera_v017.blend'), copy=True)
src = open(inputs['r.py'], encoding='utf8').read()
exec(compile(src, 'ep004_s01_preview_render_v6.py', 'exec'), globals())
