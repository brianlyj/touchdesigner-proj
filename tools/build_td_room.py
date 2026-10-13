"""Run inside TD through the installed official TDMCP execute_code endpoint."""
from pathlib import Path
import math
SRC=Path(project.folder)/'src'
if op('/fluid_room'): op('/fluid_room').destroy()
A=op('/').create(containerCOMP,'fluid_room')
A.par.parentshortcut='App';A.par.w=1360;A.par.h=840
A.par.bgcolorr=.025;A.par.bgcolorg=.035;A.par.bgcolorb=.055
def val(o,n,v):
    p=getattr(o.par,n,None)
    if p is not None: p.val=v
def expr(o,n,v): getattr(o.par,n).expr=v
def dat(parent,name,text):
    n=parent.create(textDAT,name);n.text=text;n.par.language='python';return n
def source(parent,name,file): return dat(parent,name,(SRC/file).read_text(encoding='utf-8'))
def custom(page,name,label,kind='Float',default=0,min=0,max=1,menu=None):
    p=getattr(page,'append'+kind)(name,label=label)[0]
    if menu:
        p.menuNames=[x[0] for x in menu];p.menuLabels=[x[1] for x in menu]
    if kind not in ['Pulse']:
        p.default=default;p.val=default
    if kind in ['Float','Int']:
        p.min=min;p.max=max;p.normMin=min;p.normMax=max;p.clampMin=True;p.clampMax=True
    return p
pages={x:A.appendCustomPage(x) for x in ['Experience','Voice','Fluid','Room','Person','Anchor','Emitters']}
custom(pages['Experience'],'View','View','Menu','compare',menu=[('first','First person'),('third','Third person / orbit'),('compare','Side by side')])
custom(pages['Experience'],'Pattern','Alignment overlay','Menu','ink',menu=[('ink','Fluid ink'),('checker','Checkerboard'),('circles','Circle and crosshair')])
custom(pages['Experience'],'Source','Audio source','Menu','mic',menu=[('mic','Microphone'),('demo','Synthetic voice demo')])
custom(pages['Experience'],'Auditionsilence','Audition silence','Toggle',False)
custom(pages['Experience'],'Pause','Pause fluid','Toggle',False)
custom(pages['Experience'],'Reanchor','Set sweet spot here','Pulse')
custom(pages['Experience'],'Resetfluid','Reset fluid','Pulse')
custom(pages['Experience'],'Cutaway','Inspection cutaway','Toggle',True)
custom(pages['Experience'],'Controls','Controls page','Menu','Experience',menu=[(x,x) for x in pages])
custom(pages['Voice'],'Device','Microphone device','Menu','default',menu=[('default','System default')])
for args in [('Gain','Input gain dB',0,-24,36),('Gate','Noise gate dBFS',-45,-80,-6),('Ceiling','Full response dBFS',-12,-40,0),('Sensitivity','Overall audio sensitivity',1,.1,3),('Coloursensitivity','Colour sensitivity',1.8,.25,4),('Transition','Palette smoothing / seconds',1,.1,10)]: custom(pages['Voice'],*args[:2],default=args[2],min=args[3],max=args[4])
custom(pages['Voice'],'Calibrate','Calibrate noise floor (2 s)','Pulse')
custom(pages['Voice'],'Refreshmic','Refresh microphone devices','Pulse')
custom(pages['Voice'],'Pitchlow','Low mapping pitch / Hz',default=85,min=80,max=800)
custom(pages['Voice'],'Pitchhigh','High mapping pitch / Hz',default=255,min=110,max=1000)
custom(pages['Voice'],'Resetdemo','Restart synthetic voice','Pulse')
custom(pages['Fluid'],'Quality','Simulation quality','Menu','default',menu=[('default','512 / default'),('performance','256 / performance')])
for args in [('Saturation','Colour saturation',1,0,2),('Brightness','Ink brightness',1.6,.1,3),('Viscosity','Viscosity multiplier',1,0,3),('Force','Force multiplier',1,0,3),('Injection','Injection multiplier',1,0,3)]: custom(pages['Fluid'],*args[:2],default=args[2],min=args[3],max=args[4])
for args in [('Width','Width / metres',6,4,10),('Depth','Depth / metres',5,4,10),('Height','Height / metres',3,2.4,5),('Heightcurve','Inward curve / metres',.4,0,1.2),('Protrusion','Protrusion / metres',.55,.1,1.4)]: custom(pages['Room'],*args[:2],default=args[2],min=args[3],max=args[4])
for args in [('Personx','Person X / metres',0,-5,5),('Personz','Person Z / metres',1.25,-5,5),('Eyeheight','Eye height / metres',1.65,.8,2.2),('Heading','Heading / degrees',-20,-3600,3600),('Lookpitch','Look pitch / degrees',-3,-75,75),('Fov','Eye horizontal FOV',90,45,120),('Walkspeed','Walk speed / m per second',1.5,.1,4),('Orbitangle','Orbit angle',-42,-3600,3600),('Orbitdistance','Orbit distance',8,4,15),('Orbith','Orbit height',5,1.5,10)]: custom(pages['Person'],*args[:2],default=args[2],min=args[3],max=args[4])
custom(pages['Person'],'Resetperson','Reset person','Pulse')
for args in [('Anchorx','Sweet spot X',0,-10,10),('Anchory','Sweet spot Y',1.65,.1,5),('Anchorz','Sweet spot Z',1.25,-10,10),('Anchoryaw','Sweet spot heading',-20,-3600,3600),('Anchorpitch','Sweet spot pitch',-3,-80,80),('Anchorfov','Sweet spot horizontal FOV',90,45,120),('Anchoraspect','Sweet spot aspect',16/9,.5,3)]: custom(pages['Anchor'],*args[:2],default=args[2],min=args[3],max=args[4])
for i,(x,y) in enumerate([(.25,.35),(.7,.55),(.46,.74)],1):
    for suffix,label,default,lo,hi in [('x','X',x,.05,.95),('y','Y',y,.05,.95),('strength','Strength',1,0,3),('radius','Radius',.075,.025,.2)]: custom(pages['Emitters'],f'Emitter{i}{suffix}',f'Emitter {i} {label}',default=default,min=lo,max=hi)
for name,file in [('room_geometry','room_geometry.py'),('audio_emotion','audio_emotion.py'),('runtime','runtime.py')]: source(A,name,file)
B={x:A.create(baseCOMP,x) for x in ['audio','emotion','fluid','room','projection','viewing']}
B['interface']=A.create(containerCOMP,'interface');UI=B['interface'];UI.par.w=1360;UI.par.h=840;UI.par.bgcolorr=.025;UI.par.bgcolorg=.035;UI.par.bgcolorb=.055

mic=B['audio'].create(audiodeviceinCHOP,'microphone');mic.par.rate=48000;mic.par.format='mono';mic.par.active=True
expr(mic,'device','parent.App.par.Device')
A.par.Device.menuNames=list(mic.par.device.menuNames);A.par.Device.menuLabels=list(mic.par.device.menuLabels)
audioNote=dat(B['audio'],'READ_ME','Microphone analysis is performed by ../runtime using 30 ms attack / 250 ms release and NumPy YIN. No Audio Device Out exists. The source is never played back.')
ch=B['emotion'].create(scriptCHOP,'channels')
chcb=dat(B['emotion'],'channels_callbacks',"def onCook(scriptOp):\n    scriptOp.clear()\n    scriptOp.numSamples=1\n    for name,value in parent.App.op('runtime').module.values.items():\n        scriptOp.appendChan(name)[0]=float(value)\n")
ch.par.callbacks=chcb
out=B['emotion'].create(nullCHOP,'OUT');out.inputConnectors[0].connect(ch)

def size(o,w=512,h=512,fmt='rgba32float'):
    val(o,'outputresolution','custom');val(o,'resolutionw',w);val(o,'resolutionh',h);val(o,'outputaspect','resolution');val(o,'format',fmt)
def uniform(o,name,values):
    # Multiple GLSL vectors are an expandable built-in sequence.
    index=o.fetch('uniform_count',0);o.seq.vec.numBlocks=max(index+1,1)
    getattr(o.par,f'vec{index}name').val=name
    for c,v in zip('xyzw',values):
        p=getattr(o.par,f'vec{index}value{c}')
        if isinstance(v,str): p.expr=v
        else: p.val=v
    o.store('uniform_count',index+1)
def C(n): return f"parent.App.op('emotion/OUT')['{n}'][0]"
def P(n): return f'parent.App.par.{n}'
N="(256 if parent.App.par.Quality == 'performance' else 512)"
def fluiduniforms(n):
    uniform(n,'uControl',[C('sim_time'),1/60,C('force')+'*'+P('Force'),C('injection')+'*'+P('Injection')])
    uniform(n,'uDynamics',[C('viscosity')+'*'+P('Viscosity'),C('pitch_norm'),C('onset'),N])
    for i in range(1,4): uniform(n,'uEmitter'+str(i),[P(f'Emitter{i}{s}') for s in ['x','y','strength','radius']])
F=B['fluid'];common=(SRC/'fluid_common.glsl').read_text()
shaders={}
for name in ['force','diffuse','divergence','pressure','project_velocity','dye','dye_seed']:
    shaders[name]=dat(F,name+'_shader',common+(SRC/(name+'.glsl')).read_text())
def gpu(name,shader,inputs=(),uniforms=True):
    n=F.create(glslmultiTOP,name);n.par.pixeldat=shaders[shader];size(n)
    expr(n,'resolutionw',N);expr(n,'resolutionh',N)
    n.par.inputextenduv='hold'
    for index,sourceop in enumerate(inputs): n.inputConnectors[index].connect(sourceop)
    if uniforms: fluiduniforms(n)
    n.viewer=False;return n
zero=F.create(constantTOP,'zero');size(zero);expr(zero,'resolutionw',N);expr(zero,'resolutionh',N);zero.par.colorr=0;zero.par.colorg=0;zero.par.colorb=0
seed=gpu('pigment_seed','dye_seed')
vf=F.create(feedbackTOP,'velocity_feedback');vf.inputConnectors[0].connect(zero)
force=gpu('advect_and_force','force',[vf])
v=force
for i in range(12): v=gpu('viscosity_%02d'%i,'diffuse',[v,force])
div=gpu('divergence_before','divergence',[v]);pressure=zero
for i in range(24): pressure=gpu('pressure_%02d'%i,'pressure',[pressure,div])
projected=gpu('pressure_projection','project_velocity',[v,pressure])
velocity=F.create(nullTOP,'velocity');velocity.inputConnectors[0].connect(projected);vf.par.top=velocity
after=gpu('divergence_after','divergence',[velocity])
df=F.create(feedbackTOP,'pigment_feedback');df.inputConnectors[0].connect(seed)
dye=gpu('advect_and_inject_pigment','dye',[df,velocity])
dyeout=F.create(nullTOP,'pigment');dyeout.inputConnectors[0].connect(dye);df.par.top=dyeout
palette=F.create(glslTOP,'emotional_palette');palette.par.pixeldat=source(F,'palette_shader','palette.glsl');palette.inputConnectors[0].connect(dyeout);size(palette);expr(palette,'resolutionw',N);expr(palette,'resolutionh',N)
uniform(palette,'uMood',[C(x) for x in ['calm','wonder','joy','intensity']]);uniform(palette,'uLook',[P('Saturation'),P('Brightness'),C('sim_time'),0])
col=F.create(nullTOP,'OUT');col.inputConnectors[0].connect(palette)

R=B['room'];V=B['viewing'];PROJ=B['projection']
vertex=source(PROJ,'world_vertex','room_vertex.glsl');mapcommon=(SRC/'mapping_common.glsl').read_text()
pixel=dat(PROJ,'projective_pixel',mapcommon+(SRC/'room_pixel.glsl').read_text())
depthpixel=dat(PROJ,'reference_depth_pixel',mapcommon+(SRC/'reference_depth.glsl').read_text())
def material(name,pixel):
    mat=PROJ.create(glslMAT,name);mat.par.vdat=vertex;mat.par.pdat=pixel;val(mat,'cullface','neither');return mat
def anchoruniforms(mat):
    uniform(mat,'uEye',[P('Anchorx'),P('Anchory'),P('Anchorz'),f'math.tan(math.radians({P("Anchorfov")})/2)'])
    for name,index in [('uRight',0),('uUp',1),('uForward',2)]:
        uniform(mat,name,[f"parent.App.op('runtime').module.basis({P('Anchoryaw')}, {P('Anchorpitch')})[{index}][{j}]" for j in range(3)]+[P('Anchoraspect') if index==0 else 0])
depthmat=material('reference_depth_material',depthpixel);anchoruniforms(depthmat)
roommat=material('projected_ink_material',pixel);anchoruniforms(roommat)
uniform(roommat,'uSurface',["parent.App.par.Pattern.menuIndex",1,0,0])
humanmat=material('mannequin_material',source(PROJ,'human_pixel','human_pixel.glsl'))

geomcb=dat(R,'mesh_callbacks',"""def onCook(scriptOp):
    scriptOp.clear()
    a=parent.App
    g=a.op('room_geometry').module
    name=scriptOp.parent().name
    data=g.mannequin() if name=='person' else g.room(a.par.Width.eval(),a.par.Depth.eval(),a.par.Height.eval(),a.par.Heightcurve.eval(),a.par.Protrusion.eval())[name]
    for v in data['vertices']:
        p=scriptOp.appendPoint();p.P=v
    for face in data['faces']:
        poly=scriptOp.appendPoly(len(face),closed=True,addPoints=False)
        for i,idx in enumerate(face): poly[i].point=scriptOp.points[idx]
""")
names=['floor','ceiling','front_wall','back_wall','left_wall','curved_wall','protrusion','person']
for name in names:
    g=R.create(geometryCOMP,name)
    for child in list(g.children): child.destroy()
    mesh=g.create(scriptSOP,'mesh');mesh.par.callbacks=geomcb;mesh.display=True;mesh.render=True
    g.par.material=humanmat if name=='person' else roommat;g.render=True;g.display=True
    mesh.cook(force=True)
for name in ['first','third','sweet']:
    target=V.create(geometryCOMP,name+'_target')
    for child in list(target.children): child.destroy()
    target.render=False;target.display=False
    cam=V.create(cameraCOMP,name);cam.par.lookat=target;cam.par.fov=90;cam.par.near=.05;cam.par.far=40;cam.par.viewanglemethod='horzfov'
V.op('third_target').par.ty=1.1;V.op('third').par.fov=58
def render(parent,name,cam,geometry,w=960,h=540):
    r=parent.create(renderTOP,name);size(r,w,h,'rgba16float');r.par.camera=cam;r.par.geometry=geometry;r.par.antialias='aa2';r.par.bgcolorr=.014;r.par.bgcolorg=.019;r.par.bgcolorb=.030;return r
roompaths=' '.join(R.op(n).path for n in names if n!='person')
reference=render(PROJ,'reference_depth',V.op('sweet'),roompaths,960,540);reference.par.overridemat=depthmat;reference.par.antialias='aa1';reference.par.format='rgba32float'
expr(reference,'resolutionh','round(960/parent.App.par.Anchoraspect)')
roommat.seq.sampler.numBlocks=2;roommat.par.sampler0name='sFluid';roommat.par.sampler0top=col;roommat.par.sampler1name='sReference';roommat.par.sampler1top=reference
first=render(V,'first_person',V.op('first'),roompaths)
first.par.antialias='aa1'
third=render(V,'third_person',V.op('third'),roompaths+' '+R.op('person').path)
cut=' '.join(R.op(n).path for n in names if n not in ['ceiling','left_wall','back_wall'])
expr(third,'geometry',repr(cut)+" if parent.App.par.Cutaway else "+repr(roompaths+' '+R.op('person').path))
split=V.create(glslTOP,'comparison');size(split,960,540,'rgba16float')
split.inputConnectors[0].connect(first);split.inputConnectors[1].connect(third)
split.par.pixeldat=dat(V,'comparison_shader',"""out vec4 fragColor;
void main(){vec2 uv=vUV.st;vec3 col=vec3(.014,.019,.03);float y=(uv.y-.25)*2.;
if(y>=0.&&y<=1.){vec2 p=vec2(fract(uv.x*2.),y);col=uv.x<.5?texture(sTD2DInputs[0],p).rgb:texture(sTD2DInputs[1],p).rgb;}
if(abs(uv.x-.5)<.0015)col=vec3(.12,.22,.25);fragColor=TDOutputSwizzle(vec4(col,1));}""")
switch=UI.create(switchTOP,'view')
for i,sourceop in enumerate([first,third,split]):
    sel=UI.create(selectTOP,'source_'+str(i));sel.par.top=sourceop;switch.inputConnectors[i].connect(sel)
expr(switch,'index','parent.App.par.View.menuIndex')
def panel(name,x,y,w,h,top=None):
    p=UI.create(containerCOMP,name);p.par.x=x;p.par.y=y;p.par.w=w;p.par.h=h
    if top: p.par.top=top;p.par.topfill='best'
    return p
preview=panel('viewport',20,235,960,540,switch)
def textpanel(name,text,x,y,w,h,fontsize=20):
    t=UI.create(textTOP,name+'_text');size(t,w,h,'rgba8fixed');t.par.text=text;t.par.fontsizex=fontsize;t.par.fontsizey=fontsize;t.par.alignx='left';t.par.bgalpha=0;val(t,'fontcolorb',.9);val(t,'fontcolorg',.9);val(t,'fontcolorr',.9)
    p=panel(name,x,y,w,h,t);return t
textpanel('title','ANAMORPHIC / FLUID ROOM',20,785,960,40,28)
textpanel('caption','FIRST PERSON                                               THIRD PERSON / CUTAWAY',20,690,960,26,12)
UI.op('caption').par.layer=10;expr(UI.op('caption'),'display',"parent.App.par.View == 'compare'")
textpanel('status','Initialising...',20,91,960,100,17)
textpanel('instructions','WASD to walk  /  drag image to look or orbit\nSweet spot stays fixed until you press Set sweet spot here',20,8,960,55,16)
textpanel('control_title','EXPERIENCE CONTROLS',1000,785,340,40,21)
controls=UI.create(parameterCOMP,'controls');controls.par.x=1000;controls.par.y=20;controls.par.w=340;controls.par.h=710;controls.par.op=A;expr(controls,'pagescope','parent.App.par.Controls.eval()');controls.par.header=False;val(controls,'allowexpand',False)
buttoncb=dat(UI,'buttons_callbacks',"def onOffToOn(panelValue):\n    parent.App.op('runtime').module.action(panelValue.owner.fetch('action'))\n    return\n")
def button(name,label,x,y,w=130,h=32):
    b=UI.create(buttonCOMP,name);b.par.label=label;b.par.x=x;b.par.y=y;b.par.w=w;b.par.h=h
    b.store('action',name)
    e=UI.create(panelexecuteDAT,name+'_action');e.par.panels=b;e.par.panelvalue='state';e.par.offtoon=True;e.text=buttoncb.text
    return b
for i,(name,label) in enumerate([('first','First person'),('third','Third person'),('compare','Compare'),('Reanchor','Set sweet spot here'),('silence','Audition silence'),('demo','Synthetic demo')]): button(name,label,20+i*160,198,150,32)
for i,name in enumerate(['Experience','Voice','Fluid','Room','Person','Anchor','Emitters']): button('page_'+name,name,1000+(i%4)*84,751-(i//4)*29,80,25)
pe=A.create(parameterexecuteDAT,'parameter_events');pe.par.op=A;pe.par.pars='Reanchor Resetperson Resetfluid Calibrate Refreshmic Resetdemo';pe.par.onpulse=True;pe.text="def onPulse(par):\n    parent().op('runtime').module.pulse(par.name)\n"
kb=B['viewing'].create(keyboardinDAT,'movement_keys');kb.par.keys='w a s d';kb.par.perform=False;kb.par.panels=preview
kcb=dat(B['viewing'],'keyboard_callbacks',"""def onKey(dat,keyInfo):
    keys=parent.App.op('runtime').module.keys
    k=keyInfo.key.lower()
    if keyInfo.state: keys.add(k)
    else: keys.discard(k)
    return
def onShortcut(dat,shortcutName,time): return
""");kb.par.callbacks=kcb
mouse=UI.create(panelexecuteDAT,'mouse_look');mouse.par.panels=preview;mouse.par.panelvalue='lselect';mouse.par.offtoon=True;mouse.par.ontooff=True;mouse.text="def onOffToOn(panelValue):\n    parent.App.op('runtime').module.drag(panelValue.owner.panel)\ndef onOnToOff(panelValue):\n    parent.App.op('runtime').module.drag(panelValue.owner.panel, True)\n"
ex=A.create(executeDAT,'frame');ex.par.framestart=True;ex.par.start=True;ex.text="def onFrameStart(frame):\n    parent().op('runtime').module.tick()\ndef onStart():\n    parent().op('runtime').module.startup()\n"
for b in B.values():
    for i,n in enumerate(b.children): n.nodeX=(i%8)*190;n.nodeY=-(i//8)*120
for i,b in enumerate(B.values()): b.nodeX=(i%4)*350;b.nodeY=-(i//4)*250
for old in ['/anamorphic','/project1','/fluid_probe']:
    if op(old): op(old).allowCooking=False
project.cookRate=60
A.op('runtime').module.startup()
print('BUILD_COMPLETE',A.path,len(A.findChildren()))
exec((Path(project.folder)/'tools/refine_fluid.py').read_text(encoding='utf-8'),globals())
