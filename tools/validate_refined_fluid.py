from pathlib import Path
a=op('/fluid_room')
for name in ['refined_validation','refined_validation_execute']:
    if a.op(name):a.op(name).destroy()
d=a.create(textDAT,'refined_validation')
d.text='''import time,json,numpy as np
from pathlib import Path
start=None;last=0.;rows=[];saved={};initial=None
def step(frame):
    global start,last,saved,initial
    a=parent();m=a.op('runtime').module;now=time.perf_counter()
    if start is None:
        start=now;last=now;saved={'view':a.par.View.eval(),'palette':a.par.Palette.eval()}
        m.test_input=(10**((a.par.Gate.eval()-10)/20),0,0)
        a.par.View='compare';a.par.Palette='audio'
    if now-last<1:return
    last=now;elapsed=now-start
    d=a.op('fluid/pigment').numpyArray()[:,:,:3];v=a.op('fluid/velocity').numpyArray()[:,:,:2]
    col=a.op('fluid/OUT').numpyArray()[:,:,:3]
    before=a.op('fluid/divergence_before').numpyArray()[:,:,0];after=a.op('fluid/divergence_after').numpyArray()[:,:,0]
    if initial is None:initial=d.copy()
    rows.append(dict(seconds=elapsed,view=a.par.View.eval(),fps=m.values['fps'],rms_db=m.values['rms_db'],gate=a.par.Gate.eval(),idle_mix=m.values['idle_mix'],density_mean=float(d[:,:,0].mean()),density_max=float(d[:,:,0].max()),velocity_rms=float(np.sqrt(np.mean(v*v))),divergence_before=float(np.sqrt(np.mean(before*before))),divergence_after=float(np.sqrt(np.mean(after*after))),mean_brightness=float(col.mean()),brightness_std=float(col.std()),image_change=float(np.mean(np.abs(d-initial))),finite=bool(np.isfinite(d).all() and np.isfinite(v).all() and np.isfinite(col).all())))
    if elapsed>33:a.par.View='first'
    if elapsed>=65:
        Path(project.folder+'/assets/refined_fluid_validation.json').write_text(json.dumps(rows,indent=2))
        a.op('fluid/OUT').save(project.folder+'/assets/refined_idle.png')
        a.op('viewing/third_person').save(project.folder+'/assets/refined_idle_room.png')
        m.test_input=None;a.par.View=saved['view'];a.par.Palette=saved['palette']
        a.op('refined_validation_execute').par.active=False
'''
e=a.create(executeDAT,'refined_validation_execute');e.par.frameend=True;e.text="def onFrameEnd(frame):\n    parent().op('refined_validation').module.step(frame)\n"
print('REFINED_65_SECOND_IDLE_TEST_STARTED')
