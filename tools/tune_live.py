from pathlib import Path
a=op('/fluid_room');s=Path(project.folder)/'src'
a.op('validation_execute').par.active=False
a.op('fluid/zero').par.colorr=0;a.op('fluid/zero').par.colorg=0;a.op('fluid/zero').par.colorb=0
a.op('fluid/dye_shader').text=(s/'fluid_common.glsl').read_text()+(s/'dye.glsl').read_text()
a.op('audio_emotion').text=(s/'audio_emotion.py').read_text()
a.op('runtime').text=(s/'runtime.py').read_text()
a.op('runtime').module.pulse('Resetfluid')
for name,size in [('title',24),('caption',12),('status',13),('instructions',14),('control_title',17)]:
    t=a.op('interface/'+name+'_text');t.par.fontsizex=size;t.par.fontsizey=size;t.par.alignx='left';t.par.bgalpha=0
a.op('interface/caption').par.y=754
capture=a.create(opviewerTOP,'interface_capture');capture.par.opviewer=a.op('interface');capture.par.outputresolution='custom';capture.par.resolutionw=1360;capture.par.resolutionh=840
a.par.Auditionsilence=False;a.op('runtime').module.pulse('Calibrate')
print('TUNED_AND_CALIBRATING')
