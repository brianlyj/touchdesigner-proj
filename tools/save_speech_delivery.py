"""Save the speech tuning into the single canonical delivery filename."""
import json,time,shutil,hashlib
import numpy as np
from pathlib import Path
base=Path('C:/Users/ASUS/Downloads/TD-proj').resolve()
a=op('/fluid_room');m=a.op('runtime').module
errors=[(n.path,n.errors()) for n in a.findChildren() if n.errors()]
assert not errors,errors
assert hasattr(a.par,'Coloursensitivity')
assert 'colour_sensitivity' in a.op('audio_emotion').text
assert np.isfinite(a.op('fluid/pigment').numpyArray()).all()
settings={p.name:p.eval() for p in a.customPars if p.style!='Pulse'}
assert settings['Pitchlow']==85 and settings['Pitchhigh']==255
stamp=time.strftime('%Y%m%d_%H%M%S')
target=base/'Anamorphic_Fluid_Room.toe'
backup=base/'checkpoints'/('Before_speech_colour_'+stamp+'.toe')
# Existing paths cause an interactive overwrite prompt in this TD build.
# Move only the two explicitly named native saves into this workspace's checkpoints.
moved=[]
for source,destination in [(target,backup),(base/'Anamorphic_Fluid_Room.1.toe',base/'checkpoints'/('Before_speech_colour_'+stamp+'.1.toe'))]:
    assert source.resolve().parent==base and destination.resolve().parent==base/'checkpoints'
    if source.exists():shutil.move(str(source),str(destination));moved.append((source,destination))
try:
    success=project.save(str(target).replace('\\','/'))
    assert success and target.exists() and target.stat().st_size>200000,'Native save failed'
except Exception:
    for source,destination in moved:
        if not source.exists():shutil.copy2(destination,source)
    raise
(base/'assets/saved_controls.json').write_text(json.dumps(settings,indent=2))
report={'native_save_succeeded':bool(success),'file':target.name,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'errors':errors,'finite_pigment':True,'microphone_status':m.status,'settings':{k:settings[k] for k in ['Pitchlow','Pitchhigh','Coloursensitivity','Transition','Palette','Source','Auditionsilence']},'channels':{k:float(m.values[k]) for k in ['loudness','pitch_hz','pitch_norm','colour_loudness','colour_pitch_norm','idle_mix','calm','wonder','joy','intensity','fps']}}
(base/'assets/speech_colour_delivery.json').write_text(json.dumps(report,indent=2))
manifest={}
for name in ['Anamorphic_Fluid_Room.toe','Anamorphic_Fluid_Room.blend','assets/room_and_person.glb','README.md']:
    data=(base/name).read_bytes();manifest[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(base/'assets/delivery_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(report,indent=2))
