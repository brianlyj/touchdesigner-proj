"""Save to a fresh name and verify the actual project.save result."""
import json,time
from pathlib import Path
a=op('/fluid_room')
for name in ['refined_validation_execute','refined_validation']:
    if a.op(name):a.op(name).destroy()
a.op('runtime').module.test_input=None
base=Path('C:/Users/ASUS/Downloads/TD-proj')
settings={p.name:p.eval() for p in a.customPars if p.style!='Pulse'}
(base/'assets/saved_controls.json').write_text(json.dumps(settings,indent=2))
errors=[(n.path,n.errors()) for n in a.findChildren() if n.errors()]
if errors:raise RuntimeError(errors)
target=base/('Anamorphic_Fluid_Room_refined_'+time.strftime('%H%M%S')+'.toe')
success=project.save(str(target).replace('\\','/'))
if not success or not target.is_file():raise RuntimeError('Native project save did not write the requested file')
result={'path':str(target),'success':bool(success),'bytes':target.stat().st_size,'errors':errors}
(base/'assets/native_save_result.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
