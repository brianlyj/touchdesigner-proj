import json,math,numpy as np
from pathlib import Path
from types import SimpleNamespace
a=op('/fluid_room');m=a.op('runtime').module
names=['Personx','Personz','Eyeheight','Heading','Lookpitch','Fov','Anchorx','Anchory','Anchorz','Anchoryaw','Anchorpitch','Anchorfov','Anchoraspect','View','Pattern','Quality']
saved={n:getattr(a.par,n).eval() for n in names};result={}
try:
    a.par.Pattern='checker'
    m.pulse('Resetperson');m.pulse('Reanchor');m.cameras()
    sweet=a.op('viewing/first_person').numpyArray()
    h,w=sweet.shape[:2]
    expected=((np.floor((np.arange(w)+.5)/w*16)[None,:]+np.floor((np.arange(h)+.5)/h*9)[:,None])%2)>0
    observed=sweet[:,:,:3].mean(axis=2)>.4
    result['sweet_checker_pixel_agreement']=float((observed==expected).mean())
    a.op('viewing/first_person').save(project.folder+'/assets/alignment_sweet.png')
    a.op('viewing/third_person').save(project.folder+'/assets/alignment_third.png')
    depth=a.op('projection/reference_depth').numpyArray().copy()
    anchor=[getattr(a.par,n).eval() for n in names[6:13]]
    a.par.Personx=-.65;a.par.Personz=.65;a.par.Heading=-8;m.cameras();a.par.View='third'
    moved_depth=a.op('projection/reference_depth').numpyArray()
    result['movement_keeps_depth_reference']=bool(np.array_equal(depth,moved_depth))
    result['movement_keeps_anchor']=anchor==[getattr(a.par,n).eval() for n in names[6:13]]
    moved=a.op('viewing/first_person').numpyArray()
    result['off_axis_image_changes']=float(np.mean(np.abs(moved-sweet)))
    a.op('viewing/first_person').save(project.folder+'/assets/alignment_off_axis.png')
    oldtime=m.sim_time;m.pulse('Reanchor');m.cameras()
    result['reanchor_keeps_fluid_time']=oldtime==m.sim_time
    reanchored=a.op('viewing/first_person').numpyArray()
    result['reanchored_checker_pixel_agreement']=float(((reanchored[:,:,:3].mean(axis=2)>.4)==expected).mean())
    a.op('viewing/first_person').save(project.folder+'/assets/alignment_reanchored.png')
    before=(a.par.Personx.eval(),a.par.Personz.eval())
    cb=a.op('viewing/keyboard_callbacks').module
    cb.onKey(None,SimpleNamespace(key='w',state=True));m.last-=.05;m.tick();cb.onKey(None,SimpleNamespace(key='w',state=False))
    after=(a.par.Personx.eval(),a.par.Personz.eval())
    result['keyboard_callback_moves_person']=math.dist(before,after)>0
    m.mouse=(.5,.5);heading=a.par.Heading.eval();a.par.View='first'
    m.drag(SimpleNamespace(u=.6,v=.55,lselect=True));m.mouse=None
    result['mouse_callback_rotates_person']=a.par.Heading.eval()!=heading
    for view,button in [('first','first1'),('third','third1'),('compare','compare1')]:
        a.op('interface/'+view+'_action').module.onOffToOn(SimpleNamespace(owner=a.op('interface/'+button)))
        result['button_'+view]=a.par.View.eval()==view
    a.par.Quality='performance'
    data=a.op('fluid/OUT').numpyArray()
    result['performance_preset_shape']=list(data.shape)
    result['performance_preset_finite']=bool(np.isfinite(data).all())
finally:
    for name,value in saved.items(): getattr(a.par,name).val=value
    m.keys.clear();m.mouse=None;m.cameras()
# Rendered optical measurements need separate frames after changing camera parameters.
# validate_alignment.py supplies those measurements; same-call pixel reads can be stale.
for key in ['sweet_checker_pixel_agreement','reanchored_checker_pixel_agreement','off_axis_image_changes']:
    result.pop(key,None)
result['optical_measurements']='alignment_validation.json (staged across rendered frames)'
result['errors']=[(n.path,n.errors()) for n in a.findChildren() if n.errors()]
Path(project.folder+'/assets/interaction_validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
