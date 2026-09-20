"""Reference-based exterior studies, NOT official CAD/AR assets.
Overall dimensions follow linked manufacturer specs; small hardware details are approximations.
Blender 4.5 bpy. Millimetres converted to metres on glTF export.
"""
import bpy, bmesh, math, pathlib
from mathutils import Vector
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'dist/models'
def mat(name,color,metal=0,rough=.3,finish=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if finish:m['finish']=True;m['finishBrightness']=.85
 return m
def material(o,m):o.data.materials.append(m);return o
def smooth(o):
 for p in o.data.polygons:p.use_smooth=True
 return o
def poly(name,points,depth,y,m,bevel=.2):
 n=len(points);vs=[(x,y+d,z) for d in [-depth/2,depth/2] for x,z in points];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
 if bevel:
  mod=o.modifiers.new('Machined edge bevel','BEVEL');mod.width=bevel;mod.segments=3
  mod=o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL');mod.keep_sharp=True
 uv=mesh.uv_layers.new(name='SurfaceUV');xs=[v.co.x for v in mesh.vertices];zs=[v.co.z for v in mesh.vertices]
 for face in mesh.polygons:
  for li in face.loop_indices:
   v=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=((v.x-min(xs))/max(.001,max(xs)-min(xs)),(v.z-min(zs))/max(.001,max(zs)-min(zs)))
 material(o,m);smooth(o);return o
def rounded(name,w,h,d,r,x,y,z,m):
 pts=[]
 for cx,cz,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for i in range(25):
   a=math.radians(start+i*90/24);pts.append((x+cx+r*math.cos(a),z+cz+r*math.sin(a)))
 return poly(name,pts,d,y,m,min(d*.2,.35))
def cube(name,dim,loc,m,bevel=.15):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);material(o,m)
 if bevel:
  mod=o.modifiers.new('Edge radii','BEVEL');mod.width=bevel;mod.segments=4
  o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def cylinder(name,x,y,z,r,d,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=r,depth=d,location=(x,y,z),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=name;material(o,m);smooth(o)
 mod=o.modifiers.new('Lens edge','BEVEL');mod.width=min(.12,d/4);mod.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o
def torus(name,x,y,z,r,t,m):
 bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=t,major_segments=96,minor_segments=10,location=(x,y,z),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=name;return material(smooth(o),m)
def text(name,value,x,y,z,size,m,rotation=0):
 bpy.ops.object.text_add(location=(x,y,z),rotation=(math.pi/2,0,math.pi+rotation));o=bpy.context.object;o.name=name;o['lettering']=True;o.data.body=value;o.data.align_x='CENTER';o.data.size=size;o.data.extrude=.012;o.data.materials.append(m);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH');return o

def lens(label,x,z,r,y,ring,black,glass,inner,periscope=False):
 cylinder(label+'_Housing',x,y,z,r,1.2,ring);torus(label+'_PolishedLip',x,y+.7,z,r-.22,.2,ring)
 cylinder(label+'_BlackGlass',x,y+.75,z,r-.5,.32,black)
 for i in range(3):torus(label+'_OpticalRing'+str(i),x,y+1.0+i*.03,z,(r-.9)*(1-i*.17),.08,inner)
 if periscope:rounded(label+'_Periscope',r*.95,r*.8,.14,r*.2,x,y+1.12,z,inner)
 else:cylinder(label+'_Optic',x,y+1.1,z,r*.35,.2,glass)
 cylinder(label+'_Pupil',x,y+1.24,z,r*.17,.1,black)
 # Coating glints, small polished dielectric elements rather than baked reflections.
 cylinder(label+'_Coating',x-r*.12,y+1.32,z+r*.13,r*.07,.06,glass)

def hull(points):
 p=sorted(set(points));a=[]
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 for v in p:
  while len(a)>1 and cross(a[-2],a[-1],v)<=0:a.pop()
  a.append(v)
 b=[]
 for v in reversed(p):
  while len(b)>1 and cross(b[-2],b[-1],v)<=0:b.pop()
  b.append(v)
 return a[:-1]+b[:-1]

def build(kind,w,h,d,color,brand):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 body=mat('BodyFinish',color,.3,.33,True);frame=mat('FrameFinish',color,.78,.23,True);ring=mat('PolishedBezel',(.42,.43,.46),.95,.16);black=mat('OpticalBlack',(.003,.004,.006),.12,.14);gasket=mat('Seal',(.008,.009,.012),0,.6);glass=mat('LensCoating',(.008,.032,.075),.65,.075);inner=mat('OpticalBarrel',(.018,.021,.026),.75,.22);white=mat('FlashCeramic',(.8,.78,.67),.05,.23);ink=mat('BrandEtching',(.45,.47,.48),.65,.36)
 rad=8 if kind!='samsung' else 6.5
 rounded('MetalChassis',w,h,d,rad,0,0,0,frame)
 rounded('RearSeal',w-.6,h-.6,.35,rad,0,d/2-.25,0,gasket)
 rounded('RearGlass',w-1.1,h-1.1,.6,rad-.1,0,d/2,0,body)
 rounded('DisplaySeal',w-.5,h-.5,.3,rad,0,-d/2,0,gasket)
 rounded('OLEDGlass',w-1.1,h-1.1,.4,rad-.2,0,-d/2-.2,0,black)
 oled=mat('OLED_Screen',(.009,.013,.018),.05,.13)
 rounded('ActiveDisplay',w-3.2,h-3.2,.05,rad-1,0,-d/2-.43,0,oled)
 cylinder('FrontCamera',0,-d/2-.5,h/2-6,1.65,.15,gasket);cylinder('FrontOptic',0,-d/2-.6,h/2-6,1,.05,glass)
 cube('Earpiece',(12,.3,.4),(0,-d/2-.3,h/2-1.7),gasket,.13)
 for x in [-w/2,w/2]:
  for z in [-h/2+17,h/2-15]:cube('AntennaBreak',(.12,d-.5,.65),(x,0,z),gasket,.05)
 for z,len_ in [(25,11),(48,21)]:cube('SideButton',(1.1,2.8,len_),(w/2+.25,0,z),frame,.55)
 # Bottom ports and small engraved openings.
 cube('USB_C_Rim',(10,3.7,.16),(0,0,-h/2-.02),ring,.08);cube('USB_C_Opening',(8.7,2.5,.22),(0,0,-h/2-.13),gasket,.1);cube('USB_C_Tongue',(5.3,.55,.24),(0,.15,-h/2-.28),inner,.05)
 for x in [-28,-25,-22,-19,17,20,23,26]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.68,depth=.2,location=(x,0,-h/2-.08));material(bpy.context.object,gasket);bpy.context.object.name='SpeakerPort'
 cube('SIMTray',(14,2.6,.1),(-16,0,h/2+.02),inner,.05)
 for x in [-5.8,5.8]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.48,depth=.1,location=(x,0,-h/2-.1));material(bpy.context.object,ring)
 if kind=='xiaomi':
  cylinder('LeicaCameraBase',0,d/2+1.1,46,31,2.1,frame);torus('LeicaOuterRing',0,d/2+2.25,46,30.5,.36,ring);cylinder('LeicaBlackPlate',0,d/2+2.4,46,29.7,.5,black)
  for x,z,r,p in [(-14,34,5.1,False),(14,34,5.1,False),(-14,58,8,True)]:lens('LeicaLens',x,z,r,d/2+2.7,inner,black,glass,inner,p)
  cylinder('AuxiliarySensor',14,d/2+3.1,58,7.7,.3,inner);cylinder('AuxiliaryCenter',14,d/2+3.35,58,3,.1,black)
  for x in [-2,2]:cylinder('DualFlash',x,d/2+3,70,1.1,.2,white)
  text('LeicaWordmark','LEICA',0,d/2+3.1,44,2.6,ink)
  text('OpticsLabel','VARIO-APO-SUMMILUX',0,d/2+3.1,40.5,1.05,ink)
  text('Brand',brand,0,d/2+.36,-59,4,ink)
 elif kind=='huawei':
  centers=[(-20,62),(-20,29),(14,45.5)];points=hull([(x+12*math.cos(i*math.pi/48),z+12*math.sin(i*math.pi/48)) for x,z in centers for i in range(96)])
  poly('XMAGE_TriangleMetal',points,2.1,d/2+1.25,ring,.4)
  inside=hull([(x+11.2*math.cos(i*math.pi/48),z+11.2*math.sin(i*math.pi/48)) for x,z in centers for i in range(96)])
  poly('XMAGE_TriangleFinish',inside,.65,d/2+2.55,body,.25)
  for x,z,r,p in [(-20,62,9,False),(-20,29,9,False),(14,45.5,11.7,True)]:lens('XMAGE_Lens',x,z,r,d/2+3,ring,black,glass,inner,p)
  rounded('DualLEDFlash',6.3,1.8,.24,.7,-21,d/2+3.15,46,white)
  text('XMAGELabel','XMAGE',-9,d/2+3.25,46,1.9,ink);text('Brand',brand,0,d/2+.35,-59,3.7,ink)
 else:
  rounded('CameraIsland',21.2,58,2.5,10.5,-22,d/2+1.4,45,frame)
  for z in [65,45,25]:lens('MainCamera',-22,z,9.3,d/2+2.7,frame,black,glass,inner)
  lens('TeleCamera',-4,45,4.8,d/2+1.1,frame,black,glass,inner)
  cylinder('LaserFocusHousing',-4,d/2+1.1,65,4.8,1,frame);cylinder('LaserFocus',-4,d/2+1.65,65,4.2,.15,black)
  for z in [63.3,66.7]:cylinder('LaserEmitter',-4,d/2+1.8,z,.7,.1,glass)
  cylinder('Flash',-4,d/2+.7,54.8,1.9,.3,white)
  cube('SPenCap',(5,3.5,.3),(-29,0,-h/2-.16),frame,.12)
  text('Brand',brand,0,d/2+.35,-60,3.3,ink)
 # Bake geometry in metres. Keep local assets ready for standard glTF Y-up viewers.
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 for o in meshes:
  o.scale*=.001;o.location*=.001
  o.location.x*=-1
  if not o.get('lettering'):o.scale.x*=-1
 bpy.ops.object.select_all(action='SELECT')
 bpy.ops.export_scene.gltf(filepath=str(OUT/(kind+'-flagship.glb')),export_format='GLB',export_apply=True,export_extras=True,export_animations=False,export_yup=True)
 print('BUILT',kind,len(meshes))

if __name__=='__main__':
 build('xiaomi',77.6,162.9,8.29,(.025,.16,.105),'xiaomi')
 build('huawei',77.1,164,8.1,(.023,.026,.03),'HUAWEI')
 build('samsung',78.1,163.6,7.9,(.23,.19,.34),'SAMSUNG')
