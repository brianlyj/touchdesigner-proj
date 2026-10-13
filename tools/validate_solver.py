import numpy as np,json
from pathlib import Path
a=op('/fluid_room');f=a.op('fluid')
if a.op('solver_test'): a.op('solver_test').destroy()
t=a.create(baseCOMP,'solver_test')
seed=t.create(glslTOP,'test_velocity');seed.par.outputresolution='custom';seed.par.resolutionw=512;seed.par.resolutionh=512;seed.par.format='rgba32float'
d=t.create(textDAT,'test_shader');d.text='out vec4 fragColor; void main(){vec2 q=vUV.st*6.283185;vec2 v=.1*vec2(sin(q.x*32.)*sin(q.y*24.),cos(q.x*16.)*sin(q.y*32.));fragColor=TDOutputSwizzle(vec4(v,0,1));}'
seed.par.pixeldat=d
results={}
for name,viscosity in [('low',0),('high',1)]:
    prev=seed
    for i in range(12):
        n=t.copy(f.op('viscosity_00'),name=name+'_'+str(i));n.par.pixeldat=f.op('diffuse_shader');n.inputConnectors[0].connect(prev);n.inputConnectors[1].connect(seed)
        n.par.vec1valuex=viscosity;n.par.vec1valuew=512;n.par.resolutionw=512;n.par.resolutionh=512
        prev=n
    data=prev.numpyArray()[:,:,:2]
    results[name]=dict(velocity_rms=float(np.sqrt(np.mean(data*data))),spatial_gradient_rms=float(np.sqrt(np.mean(np.diff(data,axis=0)**2))),finite=bool(np.isfinite(data).all()))
results['viscosity_diffuses']=results['high']['spatial_gradient_rms']<results['low']['spatial_gradient_rms']*.9
results['seed_rms']=float(np.sqrt(np.mean(seed.numpyArray()[:,:,:2]**2)))
results['operators_error_free']=not any(n.errors() for n in t.children)
Path(project.folder+'/assets/viscosity_validation.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results))
t.destroy()
