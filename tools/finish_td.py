from pathlib import Path
a=op('/fluid_room');src=Path(project.folder)/'src'
voice=next(p for p in a.customPages if p.name=='Voice')
for name,label,value,lo,hi in [('Pitchlow','Low mapping pitch / Hz',85,80,800),('Pitchhigh','High mapping pitch / Hz',255,110,1000),('Coloursensitivity','Colour sensitivity',1.8,.25,4)]:
    if not hasattr(a.par,name):
        p=voice.appendFloat(name,label=label)[0];p.default=value;p.val=value;p.min=lo;p.max=hi;p.normMin=lo;p.normMax=hi;p.clampMin=True;p.clampMax=True
if not hasattr(a.par,'Resetdemo'): voice.appendPulse('Resetdemo',label='Restart synthetic voice')
a.op('parameter_events').par.pars='Reanchor Resetperson Resetfluid Calibrate Refreshmic Resetdemo'
a.op('audio_emotion').text=(src/'audio_emotion.py').read_text()
a.op('runtime').text=(src/'runtime.py').read_text()
a.op('interface/caption_text').par.text='FIRST PERSON                                               THIRD PERSON / CUTAWAY'
# Keep diagnostics as files, remove temporary test operators from the delivered network.
for name in ['validation_execute','validation','interface_capture']:
    if a.op(name): a.op(name).destroy()
if op('/fluid_probe'): op('/fluid_probe').destroy()
# Embedded provenance and relative asset references travel with the TOE.
n=a.create(textDAT,'ASSET_MANIFEST')
n.text='Editable source: Anamorphic_Fluid_Room.blend\nExchange asset: assets/room_and_person.glb\nGeometry contract: assets/geometry_contract.json\nTD generates matching native SOP surfaces from the embedded room_geometry DAT to retain live dimensions. Blender and glTF use the same canonical mesh generator. All units are metres.\n'
a.par.Pattern='ink';a.par.Source='mic';a.par.Auditionsilence=False;a.par.Pause=False;a.par.View='compare';a.par.Controls='Experience'
a.op('runtime').module.pulse('Resetperson');a.op('runtime').module.pulse('Reanchor');a.op('runtime').module.pulse('Resetfluid')
op('/perform').par.winop=a
op('/perform').par.winw=1360;op('/perform').par.winh=840
print('FINAL_NETWORK_READY',[(n.path,n.errors()) for n in a.findChildren() if n.errors()])
