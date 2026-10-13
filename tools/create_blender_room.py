import bpy,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from room_geometry import room,mannequin
# This runs in a fresh background process, leaving any user's open scene alone.
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene.unit_settings.scale_length=1.0
room_collection=bpy.data.collections.new('Room_Surfaces')
scene.collection.children.link(room_collection)
def mesh(name,data,collection,colour):
    verts=[(x,-z,y) for x,y,z in data['vertices']]
    m=bpy.data.meshes.new(name+'_mesh');m.from_pydata(verts,[],data['faces']);m.update()
    ob=bpy.data.objects.new(name,m);collection.objects.link(ob)
    mat=bpy.data.materials.new(name+'_material');mat.diffuse_color=(*colour,1)
    ob.data.materials.append(mat)
    return ob
for name,data in room().items(): mesh(name,data,room_collection,(.31,.35,.40))
human=mesh('Mannequin',mannequin(),scene.collection,(.72,.73,.69))
human.location=(0,-1.25,0)
for name,loc in [('Sweet_Spot',(0,-1.25,1.65)),('Room_Origin',(0,0,0))]:
    ob=bpy.data.objects.new(name,None);scene.collection.objects.link(ob);ob.location=loc;ob.empty_display_type='ARROWS'
scene['coordinate_contract']='Blender (x,y,z) -> TouchDesigner/glTF (x,z,-y), metres'
scene['room_controls']='Canonical generator: src/room_geometry.py; matching controls in TouchDesigner Room page'
scene.world=bpy.data.worlds.new('World');scene.world.color=(.07,.07,.07)
(ROOT/'assets').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Anamorphic_Fluid_Room.blend'))
bpy.ops.export_scene.gltf(filepath=str(ROOT/'assets'/'room_and_person.glb'),export_format='GLB',export_yup=True)
(ROOT/'assets'/'geometry_contract.json').write_text(json.dumps({'units':'metres','td_axes':'Y up, camera forward -Z','room_default':[6,5,3],'surfaces':list(room()),'mannequin_height':1.76},indent=2))
print('ROOM_ASSETS_COMPLETE')
