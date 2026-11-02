# EP004 S01 patch v011: fixes found in motion test v1. Applied IN PLACE to ep004_s01_camera_v010.blend.
# NO camera keys, shot ranges or narration timing are touched.
#   A: layer dissolves 3 -> 8 frames (ending at the same crossing frames) + exposure dip over the bright screen layers
#   B: die underside was ~12/255 for 2.3 s -> stronger, softer under-light + brighter copper layers
#      transistor field faded in over the peel (was a flash 12 -> 125) + contacts + stronger relief
import bpy, os, time
sc = bpy.context.scene
M = bpy.data.materials

def sock_keys(mat, name, old, new, a0=1.0):
    s = M[mat].node_tree.nodes['Principled BSDF'].inputs['Alpha']
    for f in old:
        try: s.keyframe_delete('default_value', frame=f)
        except Exception as e: result.setdefault('warn', []).append(f'{mat} del {f}: {e}')
    s.default_value = a0; s.keyframe_insert('default_value', frame=new[0])
    s.default_value = 0.0; s.keyframe_insert('default_value', frame=new[1])
# (old window) -> (new window); the END frame stays at or before the camera crossing
sock_keys('touch_ITO',            'touch',  (22, 25), (19, 25), 0.25)
sock_keys('oled_subpixels',       'oled',   (40, 43), (33, 41))
sock_keys('tft_backplane',        'tft',    (42, 45), (38, 46))
sock_keys('midframe_aluminium',   'mid',    (52, 55), (47, 55))
sock_keys('shield_can_tinplate',  'can',    (64, 67), (58, 66))

# A: exposure dip while the camera is among the bright, glossy screen layers
for f, ev in ((1, 0.0), (14, 0.0), (26, -1.4), (40, -1.4), (50, -0.6), (62, 0.0)):
    sc.view_settings.exposure = ev; sc.keyframe_insert('view_settings.exposure', frame=f)
sc.view_settings.exposure = 0.0

# B: underside light, copper wiring
rl = bpy.data.objects['die_under_reflector']
rl.data.size = 3.5
for f, e in ((235, 80.0), (400, 80.0)):
    rl.data.energy = e; rl.data.keyframe_insert('energy', frame=f)
for k in range(1, 6):
    m = M[f'die_M{k}_wiring']; n = m.node_tree.nodes
    for nd in n:
        if nd.type == 'MIX' and nd.data_type == 'RGBA':
            nd.inputs[7].default_value = (1.0, 0.62, 0.30, 1.0)
    b = n['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.30
    b.inputs['Emission Color'].default_value = (1.0, 0.55, 0.25, 1.0)
    b.inputs['Emission Strength'].default_value = 0.12

# B: transistor field, fades in as the last metal layer leaves, with contacts and relief
m = M['die_transistor_field_SEM']; n = m.node_tree.nodes; L = m.node_tree.links
b = n['Principled BSDF']
def line_node(axis, scale, width):
    tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sep.inputs['Vector'])
    mul = n.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = scale; L.new(sep.outputs[axis], mul.inputs[0])
    fr = n.new('ShaderNodeMath'); fr.operation = 'FRACT'; L.new(mul.outputs[0], fr.inputs[0])
    lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = width; L.new(fr.outputs[0], lt.inputs[0])
    return lt
cm = n.new('ShaderNodeMath'); cm.operation = 'MULTIPLY'
L.new(line_node('X', 65, 0.22).outputs[0], cm.inputs[0]); L.new(line_node('Y', 40, 0.28).outputs[0], cm.inputs[1])
base_mix = [x for x in n if x.type == 'MIX' and x.data_type == 'RGBA'][0]
mix2 = n.new('ShaderNodeMix'); mix2.data_type = 'RGBA'
L.new(base_mix.outputs[2], mix2.inputs[6]); mix2.inputs[7].default_value = (0.95, 0.96, 1.0, 1.0); L.new(cm.outputs[0], mix2.inputs[0])
L.new(mix2.outputs[2], b.inputs['Base Color']); L.new(mix2.outputs[2], b.inputs['Emission Color'])
for nd in n:
    if nd.type == 'BUMP': nd.inputs['Strength'].default_value = 2.5
b.inputs['Emission Strength'].default_value = 0.0; b.inputs['Emission Strength'].keyframe_insert('default_value', frame=270)
b.inputs['Emission Strength'].default_value = 0.22; b.inputs['Emission Strength'].keyframe_insert('default_value', frame=292)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'ep004_s01_camera_v011.blend'), copy=True)

# ---- low-res motion test v2 (same output settings as v1) ----
gpu(sc, 'auto')
sc.render.engine = 'CYCLES'; sc.cycles.samples = 16; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 640, 360, 100
sc.render.fps = 24; sc.render.use_motion_blur = False
try: sc.render.image_settings.media_type = 'VIDEO'
except Exception as e: result['media_type_note'] = str(e)
sc.render.image_settings.file_format = 'FFMPEG'
ff = sc.render.ffmpeg; ff.format = 'MPEG4'; ff.codec = 'H264'; ff.constant_rate_factor = 'MEDIUM'; ff.audio_codec = 'NONE'
timing = {}
for i, (name, f0, f1, cam) in enumerate((('A_pushthrough', 1, 102, 'CAM_S01_A_pushthrough'), ('B_dive', 201, 320, 'CAM_S01_B_dive'), ('C_wafer', 401, 422, 'CAM_S01_C_wafer'))):
    progress(i, 3, f'v2 {name}')
    sc.camera = bpy.data.objects[cam]; sc.frame_start, sc.frame_end = f0, f1
    sc.render.filepath = os.path.join(out, f'S01_{name}_motiontest_v2_')
    t = time.time(); bpy.ops.render.render(animation=True)
    timing[name] = round(time.time() - t, 1)
result['timing'] = timing
result['files'] = sorted(os.listdir(out))
