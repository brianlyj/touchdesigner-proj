from pathlib import Path
a=op('/fluid_room');a.par.Pattern='ink';a.par.Auditionsilence=True;a.par.View='compare'
for name in ['validation_execute','validation_execute1','validation','validation1']:
    if a.op(name): a.op(name).destroy()
a.op('projection/projective_pixel').text=(Path(project.folder)/'src/mapping_common.glsl').read_text()+(Path(project.folder)/'src/room_pixel.glsl').read_text()
# Gather statistics in the actual running GPU network for 65 seconds at nonzero below-gate input.
code='''import time,json,numpy as np
start=time.perf_counter()
last=start
rows=[]
initial=None
phase='comparison'
def sample(frame):
    global last,initial,phase,start
    now=time.perf_counter()
    if now-last<1: return
    last=now
    a=parent();m=a.op('runtime').module
    d=a.op('fluid/pigment').numpyArray()[:,:,:2]
    v=a.op('fluid/velocity').numpyArray()[:,:,:2]
    before=a.op('fluid/divergence_before').numpyArray()[:,:,0]
    after=a.op('fluid/divergence_after').numpyArray()[:,:,0]
    if initial is None: initial=d.copy()
    rows.append(dict(seconds=now-start,view=a.par.View.eval(),fps=m.values['fps'],rms_db=m.values['rms_db'],gate=a.par.Gate.eval(),density_mean=float(d[:,:,0].mean()),density_max=float(d[:,:,0].max()),velocity_rms=float(np.sqrt(np.mean(v*v))),divergence_before=float(np.sqrt(np.mean(before*before))),divergence_after=float(np.sqrt(np.mean(after*after))),change=float(np.mean(np.abs(d-initial))),finite=bool(np.isfinite(d).all() and np.isfinite(v).all())))
    if now-start>33: a.par.View='first'
    if now-start>=65:
        from pathlib import Path
        Path(project.folder+'/assets/live_validation.json').write_text(json.dumps(rows,indent=2))
        a.op('validation_execute').par.active=False
        a.op('viewing/first_person').save(project.folder+'/assets/fluid_first.png')
        a.op('viewing/third_person').save(project.folder+'/assets/fluid_third.png')
'''
n=a.create(textDAT,'validation');n.text=code
e=a.create(executeDAT,'validation_execute');e.par.frameend=True;e.text="def onFrameEnd(frame):\n    parent().op('validation').module.sample(frame)\n"
print('65_SECOND_LIVE_TEST_STARTED')
