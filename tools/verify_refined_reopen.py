import json
import numpy as np
from pathlib import Path
a=op('/fluid_room');m=a.op('runtime').module
base=Path(project.folder)
stages=['velocity_curl','vorticity_confinement','pressure_feedback','pigment_forward','pigment_backward','pigment_maccormack']
result={'project':project.name,'folder':project.folder,'refined_stages':{s:bool(a.op('fluid/'+s)) for s in stages},'errors':[(n.path,n.errors()) for n in a.findChildren() if n.errors()],'controls':{p.name:p.eval() for p in a.customPars if p.style!='Pulse'},'microphone_active':bool(a.op('audio/microphone').par.active),'microphone_devices':list(a.op('audio/microphone').par.device.menuLabels),'status':m.status,'channels':m.values,'asset_exists':(base/'assets/room_and_person.glb').is_file(),'finite':bool(np.isfinite(a.op('fluid/pigment').numpyArray()).all() and np.isfinite(a.op('fluid/velocity').numpyArray()).all()),'temporary_tests_removed':not a.op('refined_validation_execute')}
saved=json.loads((base/'assets/saved_controls.json').read_text())
result['saved_controls_restored']=all(result['controls'].get(k)==v for k,v in saved.items())
(base/'assets/refined_reopen_validation.json').write_text(json.dumps(result,indent=2))
a.op('fluid/OUT').save(str(base/'assets/delivered_fluid.png'))
a.op('viewing/third_person').save(str(base/'assets/delivered_room.png'))
print(json.dumps({k:v for k,v in result.items() if k not in ['channels','controls']},indent=2))
