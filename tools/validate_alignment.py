from pathlib import Path
a=op('/fluid_room')
a.op('projection/reference_depth').par.resolutionh.expr='round(960/parent.App.par.Anchoraspect)'
for name in ['alignment_test','alignment_execute']:
    if a.op(name): a.op(name).destroy()
d=a.create(textDAT,'alignment_test')
d.text='''import numpy as np,json
from pathlib import Path
a=parent();m=a.op('runtime').module
names=['Personx','Personz','Heading','Lookpitch','Anchorx','Anchory','Anchorz','Anchoryaw','Anchorpitch','Anchorfov','Anchoraspect','Pattern','View']
saved={}
count=0;results={};initial=None;depth=None
def imagecheck(label):
    n=a.op('viewing/first_person');n.cook(force=True);data=n.numpyArray();h,w=data.shape[:2]
    expected=((np.floor((np.arange(w)+.5)/w*16)[None,:]+np.floor((np.arange(h)+.5)/h*9)[:,None])%2)>0
    results[label+'_pixel_agreement']=float(((data[:,:,:3].mean(axis=2)>.4)==expected).mean())
    n.save(project.folder+'/assets/alignment_'+label+'.png')
    return data.copy()
def step(frame):
    global count,initial,depth,saved
    count+=1
    if count==1:
        saved={n:getattr(a.par,n).eval() for n in names}
        a.par.Pattern='checker';a.par.View='compare';m.pulse('Resetperson');m.pulse('Reanchor');m.cameras()
    if count==12:
        initial=imagecheck('sweet');depth=a.op('projection/reference_depth').numpyArray().copy()
        a.op('viewing/third_person').save(project.folder+'/assets/alignment_third.png')
        a.par.Personx=-.65;a.par.Personz=.65;a.par.Heading=-8
    if count==24:
        moved=imagecheck('off_axis')
        results['off_axis_image_difference']=float(np.mean(np.abs(moved-initial)))
        results['fixed_depth_unchanged']=bool(np.array_equal(depth,a.op('projection/reference_depth').numpyArray()))
        tm=m.sim_time;m.pulse('Reanchor');results['reanchor_does_not_reset_fluid']=m.sim_time==tm
    if count==36:
        imagecheck('reanchored')
        for name,value in saved.items():getattr(a.par,name).val=value
        m.cameras();a.op('alignment_execute').par.active=False
        Path(project.folder+'/assets/alignment_validation.json').write_text(json.dumps(results,indent=2))
'''
e=a.create(executeDAT,'alignment_execute');e.par.frameend=True;e.text="def onFrameEnd(frame):\n    parent().op('alignment_test').module.step(frame)\n"
print('PHASED_ALIGNMENT_CHECK_STARTED')
