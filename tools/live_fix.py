a=op('/fluid_room');ui=a.op('interface');switch=ui.op('view')
for i,name in enumerate(['first_person','third_person','comparison']):
    sel=ui.create(selectTOP,'source_'+str(i));sel.par.top=a.op('viewing/'+name);switch.inputConnectors[i].connect(sel)
a.par.Auditionsilence=True
a.par.Pattern='checker'
print('FIXED',switch.inputs)
