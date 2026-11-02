# EP004 S01 patch v016 (applied to v015, which has all animation shifted +600 frames). Fixes from the continuous preview analysis:
# dash no longer pure black before ignition; table fades during A so the opening->A cut keeps its environment;
# board-drop lighting starts earlier; OLED dissolve starts earlier; quartz lights ramp slowly; wafer colours less pastel / no bullseye.
import bpy, os
sc = bpy.context.scene; M = bpy.data.materials; K = 600
def fcs(act):
    out_ = []
    try:
        for ly in act.layers:
            for st in ly.strips:
                for cb in st.channelbags: out_ += list(cb.fcurves)
    except Exception: out_ = list(act.fcurves)
    return out_
def act_of(idb):
    ad = idb.animation_data; return ad.action if ad and ad.action else None
def move_key(act, x_old, x_new, path_contains=None):
    n = 0
    for fc in fcs(act):
        if path_contains and path_contains not in fc.data_path: continue
        for kp in fc.keyframe_points:
            if abs(kp.co.x - x_old) < 0.01:
                dx = x_new - kp.co.x; kp.co.x += dx; kp.handle_left.x += dx; kp.handle_right.x += dx; n += 1
        fc.keyframe_points.sort(); fc.update()
    return n
def set_key_val(act, x, val, path_contains=None):
    n = 0
    for fc in fcs(act):
        if path_contains and path_contains not in fc.data_path: continue
        for kp in fc.keyframe_points:
            if abs(kp.co.x - x) < 0.01: kp.co.y = val; kp.handle_left.y = val; kp.handle_right.y = val; n += 1
        fc.update()
    return n
log = {}
# 1. dashboard: dim, readable base glow before ignition (keys at bf(271)+K and bf(288)+K)
x1, x2 = 271 - 527 + K, 288 - 527 + K
for mn, v in (('dash_tick', 0.35), ('dash_num', 0.3), ('dash_needle', 0.5), ('dash_face', 0.1)):
    a = act_of(M[mn].node_tree); log[mn] = (set_key_val(a, x1, v), set_key_val(a, x2, v))
# 2. table fades out over the first frames of A (A pass now shows the table)
tb = M['table_dark'].node_tree.nodes['Principled BSDF'].inputs['Alpha']
for f, v in ((1 + K, 1.0), (16 + K, 0.0)): tb.default_value = v; tb.keyframe_insert('default_value', frame=f)
# 3. board-drop lighting earlier
rl = bpy.data.objects['die_under_reflector'].data; a = act_of(rl)
log['reflector'] = (move_key(a, 215 + K, 206 + K), move_key(a, 235 + K, 222 + K))
log['world'] = move_key(act_of(sc.world.node_tree), 222 + K, 214 + K)
# 4. OLED dissolve starts earlier
log['oled'] = move_key(act_of(M['oled_subpixels'].node_tree), 33 + K, 29 + K, 'Alpha') or move_key(act_of(M['oled_subpixels'].node_tree), 33 + K, 29 + K)
# 5. quartz lights ramp slowly (from 5009/5016 to 5003/5028) and a little softer
for nm in ('q_key', 'q_rim', 'q_top'):
    d = bpy.data.lights[nm]; a = act_of(d); log[nm] = (move_key(a, 5009 + K, 5003 + K), move_key(a, 5016 + K, 5028 + K))
    for fc in fcs(a):
        for kp in fc.keyframe_points:
            if kp.co.y > 100: kp.co.y *= 0.75; kp.handle_left.y *= 0.75; kp.handle_right.y *= 0.75
# 6. wafer: weaker radial rainbow, more saturated thin-film range
mt = M['wafer_die_tiles']; nn = mt.node_tree.nodes
for nd in nn:
    if nd.type == 'MATH' and nd.operation == 'MULTIPLY' and abs(nd.inputs[1].default_value - 20.0) < 1e-3: nd.inputs[1].default_value = 4.0
    if nd.type == 'MAP_RANGE' and nd.inputs['To Max'].default_value > 100: nd.inputs['To Min'].default_value = 320.0; nd.inputs['To Max'].default_value = 560.0
result['patch_log'] = log
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s01_camera_v016.blend'), copy=True)
# 7. re-render the affected segments with the same render script (A now shows the table)
src = open(inputs['r.py'], encoding='utf8').read()
exec(compile(src, 'ep004_s01_preview_render_v5.py', 'exec'), globals())
