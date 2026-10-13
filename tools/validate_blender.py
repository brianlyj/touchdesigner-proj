import bpy,json
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'Anamorphic_Fluid_Room.blend'))
room=bpy.data.collections['Room_Surfaces']
points=[o.matrix_world@Vector(v) for o in room.objects for v in o.bound_box]
extent=[max(p[i] for p in points)-min(p[i] for p in points) for i in range(3)]
report={'room_blender_xyz_m':extent,'metre_scale':bpy.context.scene.unit_settings.scale_length,'named_surfaces':sorted(o.name for o in room.objects),'human_height_m':bpy.data.objects['Mannequin'].dimensions.z,'opens_successfully':True}
assert max(abs(a-b) for a,b in zip(extent,[6,5,3]))<1e-5
assert abs(report['human_height_m']-1.76)<1e-5
(root/'assets/blender_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
