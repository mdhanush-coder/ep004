# EP004 S01 low-res MOTION TEST render. Opens the approved ep004_s01_camera_v010.blend as-is:
# no scene, camera or timing changes; only output settings (resolution, samples, video encode).
# Run as EngineX blender/script with the .blend as `input`.
import bpy, os, time
sc = bpy.context.scene
gpu(sc, 'auto')
sc.render.engine = 'CYCLES'
sc.cycles.samples = 16
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 640, 360, 100
sc.render.fps = 24
sc.render.use_motion_blur = False

try:                                   # Blender 5.x splits "media type" from file format
    sc.render.image_settings.media_type = 'VIDEO'
except Exception as e:
    result['media_type_note'] = str(e)
sc.render.image_settings.file_format = 'FFMPEG'
ff = sc.render.ffmpeg
ff.format = 'MPEG4'; ff.codec = 'H264'; ff.constant_rate_factor = 'MEDIUM'; ff.audio_codec = 'NONE'

SHOTS = [('A_pushthrough', 1, 102, 'CAM_S01_A_pushthrough'),
         ('B_dive', 201, 320, 'CAM_S01_B_dive'),
         ('C_wafer', 401, 422, 'CAM_S01_C_wafer')]
timing = {}
for i, (name, f0, f1, cam) in enumerate(SHOTS):
    progress(i, len(SHOTS), f'rendering {name} f{f0}-{f1}')
    sc.camera = bpy.data.objects[cam]
    sc.frame_start, sc.frame_end = f0, f1
    sc.render.filepath = os.path.join(out, f'S01_{name}_motiontest_')
    t = time.time()
    bpy.ops.render.render(animation=True)
    timing[name] = dict(frames=f1 - f0 + 1, seconds=round(time.time() - t, 1))
result['timing'] = timing
result['files'] = sorted(os.listdir(out))
