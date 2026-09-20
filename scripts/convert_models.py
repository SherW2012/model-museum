"""Convert Apple AR Pro/Pro Max assets into standalone GLB exhibits.
Requires Blender Python bpy; source USDZ is supplied as argv[1].
"""
import sys, pathlib, math
import bpy
from mathutils import Vector, Matrix
source = sys.argv[1] if len(sys.argv)>1 else '/tmp/museum-cn.usdz'
out = pathlib.Path(__file__).resolve().parents[1]/'dist/models'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.usd_import(filepath=source,import_cameras=False,import_lights=False)
finish_materials={'hjqXePWFPwdzdEG','hrljHERKFqTtCHe','zsnfHKSIrTVTZpT','RKmqvedZQBGXvrC','NlwHIkUCIUMVlWA','NnqzKsaUupMqOcD','UnQJlgLZBfNpGFh','clMCsVkhiMFjbmm','YMNYoieHVnpIAYz','QJaWVmFHBkzLtvU','MrPnrENSHWEMvvu','zNbaqVlZUxuLDpZ','XkqdDzzVwHIQLdF'}
for m in bpy.data.materials:
 if m.name.split('.')[0] in finish_materials:
  m['finish']=True;m['finishBrightness']=.85
# Identify product roots by the official source scene hierarchy.
for rootname,slug,turn in [('hWnSpblQztGYOgB','iphone-18-pro-max',False),('DJXWYbiQXUSWOAo','iphone-18-pro',True)]:
 root=bpy.data.objects[rootname];obs=[o for o in root.children_recursive if o.type=='MESH']
 vs=[o.matrix_world@Vector(c) for o in obs for c in o.bound_box]
 center=Vector([(min(v[i] for v in vs)+max(v[i] for v in vs))/2 for i in range(3)])
 rotation=Matrix.Rotation(math.pi,4,'Z') if turn else Matrix.Identity(4)
 copied=[]
 for o in obs:
  c=o.copy();c.data=o.data.copy();c.parent=None;bpy.context.collection.objects.link(c)
  c.matrix_world=rotation@Matrix.Translation(-center)@o.matrix_world
  c.hide_set(False);c.hide_render=False;copied.append(c)
 bpy.ops.object.select_all(action='DESELECT')
 for o in copied:o.select_set(True)
 bpy.context.view_layer.objects.active=copied[0]
 bpy.ops.export_scene.gltf(filepath=str(out/(slug+'.glb')),export_format='GLB',use_selection=True,export_extras=True,export_animations=False,export_yup=True)
 if slug.endswith('max'):
  # Save a temporary source checkpoint for an offline visual geometry check.
  for o in list(bpy.data.objects):
   if o not in copied:o.hide_render=True
  bpy.ops.wm.save_as_mainfile(filepath='/tmp/museum-max-check.blend')
 for o in copied:bpy.data.objects.remove(o,do_unlink=True)
 print('EXPORTED',slug,len(obs))
