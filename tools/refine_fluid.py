"""Upgrade the live native fluid network with detail-preserving pigment transport."""
from pathlib import Path
a=op('/fluid_room');f=a.op('fluid');src=Path(project.folder)/'src'
page=next(p for p in a.customPages if p.name=='Fluid')
for name,label,value,lo,hi in [('Vorticity','Curl strength',1,0,2.5),('Filaments','Filament detail',1,0,2),('Sheen','Pigment surface sheen',.35,0,2)]:
    if not hasattr(a.par,name):
        p=page.appendFloat(name,label=label)[0];p.default=value;p.val=value;p.min=lo;p.max=hi;p.normMin=lo;p.normMax=hi;p.clampMin=True;p.clampMax=True
if not hasattr(a.par,'Palette'):
    p=page.appendMenu('Palette',label='Palette audition')[0];p.menuNames=['audio','calm','wonder','joy','intensity'];p.menuLabels=['Follow voice','Calm','Wonder','Joy','Intensity'];p.default='audio';p.val='audio'
for c,mood in zip('xyzw',['calm','wonder','joy','intensity']):
    getattr(f.op('emotional_palette').par,'vec0value'+c).expr=f"parent.App.op('emotion/OUT')['{mood}'][0] if parent.App.par.Palette == 'audio' else (1.0 if parent.App.par.Palette == '{mood}' else 0.0)"
common=(src/'fluid_common.glsl').read_text()
names=['force','diffuse','divergence','pressure','project_velocity','dye','dye_seed','curl','vorticity','pigment_transport','pigment_correct']
for name in names:
    d=f.op(name+'_shader') or f.create(textDAT,name+'_shader')
    d.text=common+(src/(name+'.glsl')).read_text()
f.op('palette_shader').text=(src/'palette.glsl').read_text()
for n in f.children:
    if isinstance(n,(glslTOP,glslmultiTOP)):
        index=2 if n.name=='emotional_palette' else 5
        n.seq.vec.numBlocks=max(n.seq.vec.numBlocks,index+1)
        getattr(n.par,f'vec{index}name').val='uStyle'
        for c,p in zip('xyz',['Vorticity','Filaments','Sheen']):getattr(n.par,f'vec{index}value{c}').expr='parent.App.par.'+p
        getattr(n.par,f'vec{index}valuew').val=0
def stage(name,shader,inputs):
    n=f.op(name) or f.copy(f.op('pigment_seed'),name=name)
    n.par.pixeldat=f.op(shader+'_shader')
    for i,o in enumerate(inputs): n.inputConnectors[i].connect(o)
    n.viewer=False
    return n
curl=stage('velocity_curl','curl',[f.op('advect_and_force')])
confined=stage('vorticity_confinement','vorticity',[f.op('advect_and_force'),curl])
for i in range(12):
    n=f.op('viscosity_%02d'%i)
    if i==0:n.inputConnectors[0].connect(confined)
    n.inputConnectors[1].connect(confined)
old=f.op('pigment_feedback');velocity=f.op('velocity')
pressure_history=f.op('pressure_feedback') or f.create(feedbackTOP,'pressure_feedback')
pressure_history.inputConnectors[0].connect(f.op('zero'));pressure_history.par.top=f.op('pressure_23')
f.op('pressure_00').inputConnectors[0].connect(pressure_history)
forward=stage('pigment_forward','pigment_transport',[old,velocity])
reverse=stage('pigment_backward','pigment_transport',[forward,velocity])
for n,sign in [(forward,1),(reverse,-1)]:
    n.seq.vec.numBlocks=7;n.par.vec6name='uAdvection';n.par.vec6valuex=sign
correct=stage('pigment_maccormack','pigment_correct',[old,forward,reverse,velocity])
f.op('advect_and_inject_pigment').inputConnectors[0].connect(correct)
for i,n in enumerate(f.children):n.nodeX=(i%8)*190;n.nodeY=-(i//8)*120
# Re-initialise only for this solver upgrade; ordinary mood/view changes never reset it.
a.op('runtime').module.pulse('Resetfluid')
print('REFINED_FLUID_INSTALLED',len(f.children))
