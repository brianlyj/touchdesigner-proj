"""Apply speech-focused palette response without resetting fluid or camera state."""
import json
from pathlib import Path
a=op('/fluid_room');base=Path(project.folder);src=base/'src'
old=a.op('runtime').module
before={'sim_time':old.sim_time,'controls':{p.name:p.eval() for p in a.customPars if p.style!='Pulse'}}
(base/'assets/colour_tuning_before.json').write_text(json.dumps(before,indent=2))
# Retain buffers, pitch history, smoothed weights, counters, and interaction state.
keep={k:v for k,v in vars(old).items() if k in ['values','keys','buffer','last','last_pitch_time','pitch','confidence','clock','sim_time','demo_time','calibration','calibration_end','status','last_status_time','last_geometry','mouse','test_input','samples_log']}
state_data=dict(vars(old.state))
voice=next(p for p in a.customPages if p.name=='Voice')
if not hasattr(a.par,'Coloursensitivity'):
    p=voice.appendFloat('Coloursensitivity',label='Colour sensitivity')[0]
    p.min=.25;p.max=4;p.normMin=.25;p.normMax=4;p.clampMin=True;p.clampMax=True
for name,value in [('Coloursensitivity',1.8),('Transition',1),('Pitchlow',85),('Pitchhigh',255)]:
    p=getattr(a.par,name);p.default=value;p.val=value
a.par.Transition.label='Palette smoothing / seconds'
a.par.Sensitivity.label='Overall audio sensitivity'
a.op('audio_emotion').text=(src/'audio_emotion.py').read_text()
a.op('runtime').text=(src/'runtime.py').read_text()
m=a.op('runtime').module
vars(m).update(keep)
m.state=m.model.EmotionalState();vars(m.state).update(state_data)
a.par.Palette='audio'
errors=[(n.path,n.errors()) for n in a.findChildren() if n.errors()]
result={'settings':{n:getattr(a.par,n).eval() for n in ['Pitchlow','Pitchhigh','Coloursensitivity','Transition','Sensitivity','Gate','Ceiling']},'simulation_time_preserved':m.sim_time==before['sim_time'],'weights_preserved':bool((m.state.weights==state_data['weights']).all()),'errors':errors}
(base/'assets/colour_tuning_applied.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
