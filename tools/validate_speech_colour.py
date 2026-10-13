"""Regression checks for speech pitch, perceptible colour response, and idle."""
import json,math,sys
from pathlib import Path
import numpy as np
base=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(base/'src'))
from audio_emotion import EmotionalState,yin

keys=['calm','wonder','joy','intensity']
def drive(state,db,pitch,seconds=12,confidence=.99,**kw):
    for _ in range(round(seconds*60)):
        out=state.update(10**(db/20),pitch,confidence,1/60,gate_db=-49.5,**kw)
    return out
def weights(out):return np.array([out[k] for k in keys])
report={};tones=[]
for hz in [85,110,150,165,180,220,255,440]:
    for db in [-48,-30,-12]:
        t=np.arange(1024)/12000
        f,c=yin(10**(db/20)*(np.sin(2*np.pi*hz*t)+.3*np.sin(4*np.pi*hz*t)))
        cents=1200*math.log2(f/hz) if f else 9999
        tones.append(dict(hz=hz,db=db,estimated_hz=f,confidence=c,error_cents=cents))
assert all(abs(t['error_cents'])<100 and t['confidence']>=.8 for t in tones)
report['tones']=tones
grid=[]
for db in [-44,-38,-30]:
    for hz in [85,110,150,180,220,255]:
        out=drive(EmotionalState(),db,hz)
        grid.append(dict(db=db,hz=hz,**{k:float(out[k]) for k in keys+['pitch_norm','colour_pitch_norm','loudness','colour_loudness']}))
report['speech_grid']=grid
for db in [-44,-38,-30]:
    rows=[r for r in grid if r['db']==db]
    assert all(a['wonder']+a['joy']<b['wonder']+b['joy'] for a,b in zip(rows,rows[1:]))
for hz in [85,110,150,180,220,255]:
    rows=[r for r in grid if r['hz']==hz]
    assert all(a['joy']+a['intensity']<b['joy']+b['intensity'] for a,b in zip(rows,rows[1:]))
report['monotonic_pitch_and_volume']=True
responses={}
for name,config in [('previous_saved',dict(transition=5.99,pitch_low=80,pitch_high=218,colour_sensitivity=1)),('speech_tuned',{})]:
    s=EmotionalState();before=weights(drive(s,-44,110,seconds=60,**config))
    after=weights(drive(s,-32,220,seconds=2,**config))
    target=weights(drive(s,-32,220,seconds=60,**config))
    progress=1-float(np.linalg.norm(after-target)/np.linalg.norm(before-target))
    responses[name]={'fraction_of_palette_transition_after_2_s':progress}
assert responses['speech_tuned']['fraction_of_palette_transition_after_2_s']>.8
assert responses['previous_saved']['fraction_of_palette_transition_after_2_s']<.4
report['step_response']=responses
# The separate colour gain must not increase fluid force or inject more ink.
one=drive(EmotionalState(),-38,165,colour_sensitivity=1)
boost=drive(EmotionalState(),-38,165,colour_sensitivity=2.5)
assert all(abs(one[k]-boost[k])<1e-12 for k in ['loudness','pitch_norm','force','injection','viscosity'])
assert float(np.linalg.norm(weights(one)-weights(boost)))>.1
report['colour_gain_independent_of_force']=True
s=EmotionalState();out=drive(s,-38,180,seconds=30);original=weights(out)
out=drive(s,-38,0,seconds=5,confidence=0)
assert out['pitch_hz']==180 and np.max(np.abs(original-weights(out)))<1e-7
report['unpitched_hold_without_mood_flicker']=True
out=drive(s,-59.5,0,seconds=60,confidence=0)
assert out['idle_mix']==1 and out['calm']>.999 and abs(out['force']-.12)<1e-9 and abs(out['injection']-.08)<1e-9
assert all(np.isfinite(v) for v in out.values())
report['below_gate_idle_after_60_s']={k:float(out[k]) for k in keys+['idle_mix','force','injection']}
report['all_checks_passed']=True
(base/'assets/speech_colour_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['tones','speech_grid']},indent=2))
