import json
import numpy as np
a=op('/fluid_room');m=a.op('runtime').module
r={'project':project.name,'folder':project.folder,'status':m.status,'sim_time':m.sim_time,'controls':{p.name:p.eval() for p in a.customPars if p.style!='Pulse'},'errors':[(n.path,n.errors()) for n in a.findChildren() if n.errors()]}
r['feedback']={name:{p.name:str(p.eval()) for p in a.op('fluid/'+name).pars() if 'reset' in p.name or p.name in ['top','active']} for name in ['velocity_feedback','pigment_feedback','pressure_feedback']}
r['callbacks']={n.path:n.text for n in a.children if n.type in ['execute','parexec']}
r['finite']=bool(np.isfinite(a.op('fluid/pigment').numpyArray()).all())
print(json.dumps(r,indent=2))
