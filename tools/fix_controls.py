a=op('/fluid_room');ui=a.op('interface')
for n in ui.children:
    if n.type=='button': n.store('action',n.name[:-1] if n.name.endswith('1') else n.name)
for n in ui.children:
    if n.type=='panelexecute' and n.name.endswith('_action'):
        n.text="def onOffToOn(panelValue):\n    parent.App.op('runtime').module.action(panelValue.owner.fetch('action'))\n"
a.op('viewing/first_person').par.antialias='aa1'
a.par.Pattern='checker'
print('CONTROLS_FIXED')
