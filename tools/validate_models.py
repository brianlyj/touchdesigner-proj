import sys,json,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from audio_emotion import yin,EmotionalState
from room_geometry import room,clamp_person
report={}
tones=[]
for freq in [80,110,220,440,880,1000]:
    for db in [-48,-30,-12]:
        t=np.arange(1024)/12000
        x=10**(db/20)*(np.sin(2*np.pi*freq*t)+.3*np.sin(4*np.pi*freq*t))
        pitch,confidence=yin(x)
        cents=1200*math.log2(pitch/freq) if pitch else 9999
        tones.append(dict(hz=freq,db=db,estimated=pitch,confidence=confidence,error_cents=cents))
report['tones']=tones
report['tones_pass']=all(abs(x['error_cents'])<100 for x in tones)
rng=np.random.default_rng(771)
report['noise_pitch']=yin(rng.normal(0,.05,1024))
moods={}
for name,db,pitch in [('calm',-42,110),('wonder',-42,800),('joy',-14,800),('intensity',-14,110)]:
    state=EmotionalState()
    for i in range(1200): values=state.update(10**(db/20),pitch,.99,1/60)
    moods[name]={k:float(values[k]) for k in ['calm','wonder','joy','intensity']}
report['moods']=moods
report['moods_pass']=all(max(w,key=w.get)==n for n,w in moods.items())
state=EmotionalState()
for i in range(1200): state.update(.2,440,.99,1/60)
held=state.last_pitch
for i in range(120): unpitched=state.update(.1,0,0,1/60)
report['unpitched_retains_pitch']=unpitched['pitch_hz']==held
for i in range(3600): idle=state.update(10**(-55/20),0,0,1/60)
report['idle_after_60_s']={k:float(v) for k,v in idle.items()}
report['idle_pass']=idle['idle_mix']==1 and idle['calm']>.999 and abs(idle['force']-.12)<1e-6 and abs(idle['injection']-.08)<1e-6
report['collision_samples']=[clamp_person(*pos,6,5,.4,.55) for pos in [(0,-2.4),(4,0),(-4,0),(0,3)]]
report['bounds_m']=np.ptp(np.array([v for part in room().values() for v in part['vertices']]),axis=0).tolist()
Path('assets/model_validation.json').write_text(json.dumps(report,indent=2))
assert report['tones_pass'] and report['moods_pass'] and report['idle_pass']
assert report['unpitched_retains_pitch']
print(json.dumps(report,indent=2))
