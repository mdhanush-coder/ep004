# EP004 S01 patch v018 (on v017; animation shifted +600). Targeted: dark beat, OLED trough, wafer hue, freeze noise lock.
import bpy, os
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
def move_key(act, x_old, x_new):
    n = 0
    for fc in fcs(act):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - x_old) < 0.01:
                dx = x_new - kp.co.x; kp.co.x += dx; kp.handle_left.x += dx; kp.handle_right.x += dx; n += 1
        fc.keyframe_points.sort(); fc.update()
    return n
# 1. dark beat (B frames ~805-835): lighter mould so the slab reads, faint backdrop in that window only, grazing fill
mp = M['mold_compound'].node_tree.nodes['Principled BSDF']
mp.inputs['Base Color'].default_value = (0.07, 0.075, 0.085, 1); mp.inputs['Roughness'].default_value = 0.45
wt = sc.world.node_tree; mix = [n for n in wt.nodes if n.type == 'MIX_SHADER'][0]; src = mix.inputs[0].links[0].from_socket
mul = wt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.name = 'cam_black'
wt.links.new(src, mul.inputs[0]); wt.links.new(mul.outputs[0], mix.inputs[0])
for f, v in ((795, 1.0), (803, 0.55), (822, 0.55), (840, 1.0)):
    mul.inputs[1].default_value = v; mul.inputs[1].keyframe_insert('default_value', frame=f)
d = bpy.data.lights.new('drop_fill', 'AREA'); d.size = 14.0; d.color = (0.75, 0.85, 1.0)
for f, v in ((797, 0.0), (803, 2600.0), (826, 2600.0), (846, 0.0)): d.energy = v; d.keyframe_insert('energy', frame=f)
o = bpy.data.objects.new('drop_fill', d); o.location = (0.8 - 9.0, 4.6 - 11.0, 2.2); bpy.data.collections['04_LIGHTING'].objects.link(o)
from mathutils import Vector
o.rotation_euler = (Vector((0.8, 4.6, 0.4)) - o.location).to_track_quat('-Z', 'Y').to_euler()
# 2. OLED trough: key lights come back as the OLED/TFT layers dissolve (was f52/f66)
for nm in ('key_softbox', 'rim_cyan', 'fill_low'):
    a = act_of(bpy.data.lights[nm]); log[nm] = (move_key(a, 652, 638), move_key(a, 666, 650))
# 3. wafer: blue-violet thin film, deeper dies, brighter polished lanes
for nd in M['wafer_die_tiles'].node_tree.nodes:
    if nd.type == 'MAP_RANGE' and nd.inputs['To Max'].default_value > 100: nd.inputs['To Min'].default_value = 105.0; nd.inputs['To Max'].default_value = 185.0
    if nd.type == 'BSDF_PRINCIPLED': nd.inputs['Base Color'].default_value = (0.10, 0.12, 0.2, 1)
sc.cycles.use_animated_seed = True
result['patch_log'] = log
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s01_camera_v018.blend'), copy=True)
src_ = open(inputs['r.py'], encoding='utf8').read()
exec(compile(src_, 'ep004_s01_preview_render_v7.py', 'exec'), globals())
