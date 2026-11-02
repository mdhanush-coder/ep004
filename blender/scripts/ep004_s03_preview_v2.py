# EP004 S03 "The Precision Problem": generated-then-restyled CGI stills as plates with camera moves, cuts on spoken words.
# v2: Added "ILLUSTRATIVE · NOT TO SCALE" labels to microscopic shots for technical accuracy per research.
# preview frame n = t*24 from video start; S03 = 1794..3233. Scene frame f = 30000 + n - 1794. args = {"segs": [...], "fq": bool}
import bpy, bmesh, math, os, time
from mathutils import Vector
sc = bpy.context.scene
for c in list(sc.collection.children): c.hide_render = True
col = bpy.data.collections.new('S3'); sc.collection.children.link(col)
fq = args.get('fq', False)
def f3(n): return 30000 + n - 1794
def T(t): return round(t * 24)
# (name, image key, t0, t1, d0, d1, dx0, dx1, dy0, dy1)  d = camera distance (plane 17.78 wide at 25.5 fills frame)
SH = [
 ('map', 'map', 74.75, 78.20, 27.0, 24.5, 0, 0, 0, 0), ('layers', 'layers', 78.20, 83.80, 27.0, 24.5, -1.0, 1.0, 0, 0),
 ('spin', 'spincoat', 83.80, 88.55, 26.0, 23.5, 0, 0, 0.4, -0.2), ('uv', 'uvmask', 88.55, 91.45, 26.0, 24.0, 0.6, -0.6, 0, 0),
 ('dev', 'layers', 91.45, 97.65, 22.0, 19.5, 1.5, -1.5, 0.8, 0.3), ('robot', 'robot', 97.65, 102.20, 26.0, 24.0, -0.8, 0.8, 0, 0),
 ('align', 'align', 102.20, 106.40, 26.0, 23.0, 0, 0, 0, 0), ('part1', 'particle', 106.40, 111.00, 27.0, 25.0, 0, 0, 0, 0),
 ('part2', 'particle', 111.00, 118.65, 25.0, 17.0, 0, 0.3, 0, -0.2), ('clean', 'cleanroom', 118.65, 123.40, 26.0, 23.5, -0.6, 0.6, 0, 0),
 ('scan', 'scanner', 123.40, 125.15, 26.0, 24.5, 0.4, -0.4, 0, 0), ('gas', 'gaslines', 125.15, 127.15, 26.0, 24.5, -0.5, 0.5, 0, 0),
 ('eng', 'engineer', 127.15, 129.30, 26.0, 24.5, 0.4, -0.4, 0, 0), ('dice', 'dicing', 129.30, 132.10, 26.0, 23.5, 0, 0, 0, 0),
 ('probe', 'probe', 132.10, 134.75, 26.0, 23.0, -0.4, 0.4, 0, 0),
]
# Main labels that fade in on spoken word
LABELS = {'spin': ('PHOTOLITHOGRAPHY', 84.11), 'dice': ('ASSEMBLY & TESTING', 129.30)}
# "ILLUSTRATIVE · NOT TO SCALE" labels for microscopic shots (per research)
ILLUSTRATIVE = ['layers', 'spin', 'uv', 'dev', 'align', 'part1', 'part2']
def euler_for(pos, tgt):
    d = Vector(tgt) - Vector(pos); d.normalize(); return (math.acos(max(-1.0, min(1.0, -d.z))), 0.0, 0.0)
cams = {}; planes = {}
for i, (nm, key, t0, t1, d0, d1, x0, x1, y0, y1) in enumerate(SH):
    o = Vector((0, 2000 + i * 40, 0))
    img = bpy.data.images.load(inputs[key]); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5); me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
    m = bpy.data.materials.new(nm); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0, 0, 0, 1)
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = img; tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Generated'], t.inputs['Vector'])
    nt.links.new(t.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = 1.0; me.materials.append(m)
    p = bpy.data.objects.new(nm, me); col.objects.link(p); p.location = o; p.rotation_euler = (math.pi / 2, 0, 0); p.scale = (17.78, 10.0, 1)
    cd = bpy.data.cameras.new('C_' + nm); cd.lens = 50; cd.sensor_width = 36; cd.clip_end = 500; cam = bpy.data.objects.new('C_' + nm, cd); col.objects.link(cam)
    for n, d, x, y in ((T(t0), d0, x0, y0), (T(t1), d1, x1, y1)):
        cam.location = o + Vector((x, -d, y)); cam.rotation_euler = (math.pi / 2, 0, 0)
        cam.keyframe_insert('location', frame=f3(n)); cam.keyframe_insert('rotation_euler', frame=f3(n))
    for fc in cam.animation_data.action.layers[0].strips[0].channelbags[0].fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'
    cams[nm] = cam
    # Main label (PHOTOLITHOGRAPHY, ASSEMBLY & TESTING)
    if nm in LABELS:
        txt, tl = LABELS[nm]; cu = bpy.data.curves.new('lbl', 'FONT'); cu.body = txt; cu.size = 0.055; cu.align_x = 'CENTER'; cu.space_character = 1.15
        tobj = bpy.data.objects.new('lbl_' + nm, cu); col.objects.link(tobj); tobj.parent = cam; tobj.location = (0, -0.31, -1.2)
        mt = bpy.data.materials.new('lt_' + nm); mt.use_nodes = True; bt = mt.node_tree.nodes['Principled BSDF']; bt.inputs['Base Color'].default_value = (0, 0, 0, 1); bt.inputs['Emission Color'].default_value = (0.9, 0.97, 1, 1); cu.materials.append(mt)
        bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5); pm = bpy.data.meshes.new('lp'); bm.to_mesh(pm); bm.free()
        pl = bpy.data.objects.new('lp_' + nm, pm); col.objects.link(pl); pl.parent = cam; pl.location = (0, -0.305, -1.201); pl.scale = (0.1 * len(txt) * 0.62 + 0.1, 0.1, 1)
        mp = bpy.data.materials.new('lpm_' + nm); mp.use_nodes = True; bp = mp.node_tree.nodes['Principled BSDF']; bp.inputs['Base Color'].default_value = (0.01, 0.012, 0.016, 1); pm.materials.append(mp)
        for fr, vt, vp in ((T(t0), 0.0, 0.0), (T(tl), 0.0, 0.0), (T(tl) + 8, 3.0, 0.75), (T(t1) - 6, 3.0, 0.75), (T(t1), 0.0, 0.0)):
            bt.inputs['Emission Strength'].default_value = vt; bt.inputs['Emission Strength'].keyframe_insert('default_value', frame=f3(fr))
            bt.inputs['Alpha'].default_value = 1.0 if vt else 0.0; bt.inputs['Alpha'].keyframe_insert('default_value', frame=f3(fr))
            bp.inputs['Alpha'].default_value = vp; bp.inputs['Alpha'].keyframe_insert('default_value', frame=f3(fr))
        for q in (tobj, pl): q.visible_glossy = q.visible_diffuse = q.visible_transmission = q.visible_shadow = False
    # "ILLUSTRATIVE · NOT TO SCALE" label for microscopic shots (smaller, lower, stays on longer)
    if nm in ILLUSTRATIVE:
        ill_txt = 'ILLUSTRATIVE · NOT TO SCALE'; cu_ill = bpy.data.curves.new('ill', 'FONT'); cu_ill.body = ill_txt; cu_ill.size = 0.025; cu_ill.align_x = 'CENTER'
        tobj_ill = bpy.data.objects.new('ill_' + nm, cu_ill); col.objects.link(tobj_ill); tobj_ill.parent = cam; tobj_ill.location = (0, -0.31, 1.0)
        mt_ill = bpy.data.materials.new('illt_' + nm); mt_ill.use_nodes = True; bt_ill = mt_ill.node_tree.nodes['Principled BSDF']; bt_ill.inputs['Base Color'].default_value = (0, 0, 0, 1); bt_ill.inputs['Emission Color'].default_value = (0.7, 0.75, 0.8, 1); cu_ill.materials.append(mt_ill)
        bm_ill = bmesh.new(); bmesh.ops.create_grid(bm_ill, x_segments=1, y_segments=1, size=0.5); pm_ill = bpy.data.meshes.new('illp'); bm_ill.to_mesh(pm_ill); bm_ill.free()
        pl_ill = bpy.data.objects.new('illp_' + nm, pm_ill); col.objects.link(pl_ill); pl_ill.parent = cam; pl_ill.location = (0, -0.309, 1.001); pl_ill.scale = (0.1 * len(ill_txt) * 0.55 + 0.08, 0.06, 1)
        mp_ill = bpy.data.materials.new('illpm_' + nm); mp_ill.use_nodes = True; bp_ill = mp_ill.node_tree.nodes['Principled BSDF']; bp_ill.inputs['Base Color'].default_value = (0.01, 0.012, 0.016, 1); pm_ill.materials.append(mp_ill)
        # Fade in shortly after shot start, stay visible until end
        for fr, vt, vp in ((T(t0), 0.0, 0.0), (T(t0) + 6, 1.5, 0.5), (T(t1) - 4, 1.5, 0.5), (T(t1), 0.0, 0.0)):
            bt_ill.inputs['Emission Strength'].default_value = vt; bt_ill.inputs['Emission Strength'].keyframe_insert('default_value', frame=f3(fr))
            bt_ill.inputs['Alpha'].default_value = 1.0 if vt else 0.0; bt_ill.inputs['Alpha'].keyframe_insert('default_value', frame=f3(fr))
            bp_ill.inputs['Alpha'].default_value = vp; bp_ill.inputs['Alpha'].keyframe_insert('default_value', frame=f3(fr))
        for q in (tobj_ill, pl_ill): q.visible_glossy = q.visible_diffuse = q.visible_transmission = q.visible_shadow = False
gpu(sc, 'auto'); sc.render.engine = 'CYCLES'; sc.cycles.samples = 64 if fq else 8; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = (1920, 1080, 100) if fq else (640, 360, 100); sc.render.fps = 24; sc.render.use_motion_blur = False
try: sc.render.image_settings.media_type = 'VIDEO'
except Exception as e: result['media_type_note'] = str(e)
sc.render.image_settings.file_format = 'FFMPEG'; ff = sc.render.ffmpeg; ff.format = 'MPEG4'; ff.codec = 'H264'; ff.constant_rate_factor = 'HIGH' if fq else 'MEDIUM'; ff.audio_codec = 'NONE'
sc.view_settings.view_transform = 'Standard'
timing = {}
for i, (nm, key, t0, t1, *_r) in enumerate(SH):
    if nm not in args['segs']: continue
    n0, n1 = T(t0), T(t1) - 1; sc.camera = cams[nm]; sc.frame_start, sc.frame_end = f3(n0), f3(n1)
    sc.render.filepath = os.path.join(out, f"S03{'FQ' if fq else 'v2'}_{i:02d}_{nm}_"); t = time.time(); bpy.ops.render.render(animation=True); timing[nm] = dict(frames=n1 - n0 + 1, seconds=round(time.time() - t, 1))
result['timing'] = timing; result['files'] = sorted(os.listdir(out))
