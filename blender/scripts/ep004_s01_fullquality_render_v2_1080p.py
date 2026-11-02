# EP004 S01 FULL-QUALITY render (1920x1080, 128 spp, denoise, H.264 high) (segment-wise, same studio file v014). args = {"segs": [names]}
# Frame map: preview frame n (24 fps) <-> Blender frame n-527 for the opening; A 1-102, SW 102-186, freeze 103-116 (static A end pose),
# B 201-320, C 401-422, quartz bridge 5000-5108. Nothing about camera timing or narration is changed here.
import bpy, os, time
sc = bpy.context.scene
gpu(sc, 'auto'); sc.render.engine = 'CYCLES'; sc.cycles.samples = 128; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
sc.render.fps = 24
try: sc.render.image_settings.media_type = 'VIDEO'
except Exception as e: result['media_type_note'] = str(e)
sc.render.image_settings.file_format = 'FFMPEG'
ff = sc.render.ffmpeg; ff.format = 'MPEG4'; ff.codec = 'H264'; ff.constant_rate_factor = 'HIGH'; ff.ffmpeg_preset = 'GOOD'; ff.audio_codec = 'NONE'
ALL = ('08_OPEN_SET', '09_OPEN_UI', '10_DASH', '11_EARTH', '12_CODE', '13_QUARTZ', '06_WAFER')
K = 600
def bf(n): return n - 527 + K
UI = ('08_OPEN_SET', '09_OPEN_UI')
SEGS = {
 '01_O1': ('CAM_O1', bf(0), bf(59), UI, False), '02_O2': ('CAM_O2', bf(60), bf(95), UI, False), '03_O3': ('CAM_O3', bf(96), bf(149), UI, False),
 '04_O4': ('CAM_O4', bf(150), bf(193), UI, False), '05_O5': ('CAM_O5', bf(194), bf(270), UI, False), '06_O6': ('CAM_O6', bf(271), bf(321), ('10_DASH',), False),
 '07_O7': ('CAM_O7', bf(322), bf(403), ('11_EARTH',), False), '08_O8': ('CAM_O8', bf(404), bf(526), UI, False),
 '09_A': ('CAM_S01_A_pushthrough', 1 + K, 102 + K, ('08_OPEN_SET',), False), '10_SW': ('CAM_SW', bf(629), bf(713), ('12_CODE',), False),
 '11_FZ': ('CAM_S01_A_pushthrough', 70200, 70213, ('08_OPEN_SET',), False), '12_B': ('CAM_S01_B_dive', 201 + K, 320 + K, (), False),
 '13_C': ('CAM_S01_C_wafer', 401 + K, 422 + K, ('06_WAFER',), True), '14_Q': ('CAM_Q', 5000 + K, 5108 + K, ('13_QUARTZ',), False),
}
timing = {}
for name in args['segs']:
    cam, f0, f1, show, mb = SEGS[name]
    for c in ALL: bpy.data.collections[c].hide_render = c not in show
    sc.render.use_motion_blur = mb
    sc.cycles.use_animated_seed = (name != '11_FZ')      # freeze: identical noise on every frame -> a true hold
    sc.render.frame_map_old, sc.render.frame_map_new = (1, 100) if name == '11_FZ' else (100, 100)
    if mb: sc.render.motion_blur_shutter = 0.6
    sc.camera = bpy.data.objects[cam]; sc.frame_start, sc.frame_end = f0, f1
    sc.render.filepath = os.path.join(out, f'S01FQ1080_{name}_')
    progress(list(args['segs']).index(name), len(args['segs']), name)
    t = time.time(); bpy.ops.render.render(animation=True); timing[name] = dict(frames=f1 - f0 + 1, seconds=round(time.time() - t, 1))
result['timing'] = timing; result['files'] = sorted(os.listdir(out))
