"""Embedded TouchDesigner runtime; no external Python or audio playback required."""
import math
import time
import numpy as np

app = parent()
model = app.op('audio_emotion').module
geo = app.op('room_geometry').module
state = model.EmotionalState()
values = state.update(0, 0, 0, 1/60)
values.update(sim_time=0, fps=60)
keys = set()
buffer = np.zeros(8192, dtype=np.float32)
last = time.perf_counter()
last_pitch_time = -1
pitch, confidence = 0., 0.
clock = 0.
sim_time = 0.
demo_time = 0.
calibration = []
calibration_end = 0.
status = 'Starting microphone'
last_status_time = -1.
last_geometry = None
mouse = None
test_input = None
samples_log = []

def P(name): return getattr(app.par, name).eval()

def basis(yaw, pitch):
    y,p=math.radians(yaw),math.radians(pitch)
    return ((math.cos(y),0,-math.sin(y)),
            (math.sin(y)*math.sin(p),math.cos(p),math.cos(y)*math.sin(p)),
            (-math.sin(y)*math.cos(p),math.sin(p),-math.cos(y)*math.cos(p)))

def camera(name, pos, yaw, pitch, fov):
    cam=app.op('viewing/'+name)
    target=app.op('viewing/'+name+'_target')
    forward=basis(yaw,pitch)[2]
    for i,axis in enumerate('xyz'):
        getattr(cam.par,'t'+axis).val=pos[i]
        getattr(target.par,'t'+axis).val=pos[i]+forward[i]
    cam.par.fov=fov

def cameras():
    camera('first',(P('Personx'),P('Eyeheight'),P('Personz')),P('Heading'),P('Lookpitch'),P('Fov'))
    camera('sweet',(P('Anchorx'),P('Anchory'),P('Anchorz')),P('Anchoryaw'),P('Anchorpitch'),P('Anchorfov'))
    a=math.radians(P('Orbitangle'))
    cam=app.op('viewing/third')
    cam.par.tx=math.sin(a)*P('Orbitdistance')
    cam.par.ty=P('Orbith')
    cam.par.tz=math.cos(a)*P('Orbitdistance')
    human=app.op('room/person')
    human.par.tx=P('Personx');human.par.tz=P('Personz');human.par.ry=P('Heading')

def pulse(name):
    global calibration,calibration_end,sim_time,mouse,demo_time
    if name=='Reanchor':
        for dst,src in [('Anchorx','Personx'),('Anchory','Eyeheight'),('Anchorz','Personz'),('Anchoryaw','Heading'),('Anchorpitch','Lookpitch'),('Anchorfov','Fov')]:
            getattr(app.par,dst).val=P(src)
        app.par.Anchoraspect=16/9
    elif name=='Resetperson':
        app.par.Personx=0;app.par.Personz=1.25;app.par.Heading=-20;app.par.Lookpitch=-3;app.par.Eyeheight=1.65
    elif name=='Resetfluid':
        sim_time=0
        for n in ['velocity_feedback','pigment_feedback','pressure_feedback']:
            if app.op('fluid/'+n): app.op('fluid/'+n).par.resetpulse.pulse()
    elif name=='Resetdemo': demo_time=0
    elif name=='Calibrate':
        calibration=[];calibration_end=clock+2
    elif name=='Refreshmic':
        mic=app.op('audio/microphone')
        app.par.Device.menuNames=list(mic.par.device.menuNames)
        app.par.Device.menuLabels=list(mic.par.device.menuLabels)
        mic.par.active=False
        mic.par.active=True

def action(name):
    if name in ['first','third','compare']: app.par.View=name
    elif name=='pause': app.par.Pause=not P('Pause')
    elif name=='silence': app.par.Auditionsilence=not P('Auditionsilence')
    elif name=='demo': app.par.Source='demo' if P('Source')!='demo' else 'mic'
    elif name.startswith('page_'): app.par.Controls=name[5:]
    else: pulse(name)

def drag(panel, ending=False):
    global mouse
    uv=(float(panel.u),float(panel.v))
    if bool(panel.lselect) or ending:
        if mouse is not None:
            dx,dy=uv[0]-mouse[0],uv[1]-mouse[1]
            if P('View')=='third':
                app.par.Orbitangle=P('Orbitangle')-dx*160
                app.par.Orbith=max(1.5,min(10,P('Orbith')-dy*8))
            else:
                app.par.Heading=P('Heading')-dx*140
                app.par.Lookpitch=max(-75,min(75,P('Lookpitch')+dy*90))
        mouse=None if ending else uv
    else: mouse=None

def tick():
    global last,clock,sim_time,demo_time,buffer,pitch,confidence,last_pitch_time,values,status,last_status_time,last_geometry,calibration_end
    now=time.perf_counter();dt=max(.001,min(.1,now-last));last=now;clock+=dt
    values['fps']=values.get('fps',60)*.95+min(240,1/dt)*.05
    if P('Pause'):
        app.op('fluid').allowCooking=False
    else:
        app.op('fluid').allowCooking=True
        sim_time+=1/60
    # Input remains alive while the simulation is paused.
    mic=app.op('audio/microphone')
    source=P('Source');rms=0.;samples=None
    if test_input is not None:
        rms,pitch,confidence=test_input;status='Acceptance test input'
    elif P('Auditionsilence'):
        rms=10**((P('Gate')-10)/20);pitch=0;confidence=0;status='Audition silence / below gate'
    elif source=='demo':
        # Deterministic synthesised fundamental with two harmonics, periodic quiet intervals.
        demo_time+=1/60
        f=180*2**(1.1*math.sin(demo_time*.22));amp=.12*(.52+.48*math.sin(demo_time*.41))
        if demo_time%32>23: amp=10**((P('Gate')-12)/20)
        t=np.arange(4096)/48000+demo_time
        samples=amp*(np.sin(2*np.pi*f*t)+.25*np.sin(4*np.pi*f*t)+.12*np.sin(6*np.pi*f*t))
        rms=float(np.sqrt(np.mean(samples*samples)));status='Synthetic voice demo / no mic'
    else:
        try:
            raw=mic.numpyArray() if mic.par.active and len(mic.par.device.menuNames)>1 else None
            if raw is not None and raw.size and not mic.errors():
                samples=raw.mean(axis=0)*10**(P('Gain')/20)
                rms=float(np.sqrt(np.mean(samples*samples)));status='Microphone / '+str(mic.par.device.menuLabels[mic.par.device.menuIndex])
            else: status='Microphone unavailable / idle active; select Synthetic demo'
        except Exception: status='Microphone unavailable / idle active; select Synthetic demo'
    if samples is not None:
        if source=='demo': buffer[-4096:]=samples
        else:
            n=min(len(samples),len(buffer));buffer=np.roll(buffer,-n);buffer[-n:]=samples[-n:]
        if clock-last_pitch_time>=1/30:
            pitch,confidence=model.yin(buffer[-4096:][::4],12000)
            last_pitch_time=clock
    elif test_input is None and not P('Auditionsilence'):
        pitch=0;confidence=0
    if calibration_end>clock:
        calibration.append(20*math.log10(max(rms,1e-9)));status='Calibrating ambient floor / remain quiet'
    elif calibration_end:
        app.par.Gate=float(np.clip(np.percentile(calibration,90)+6,-80,-12)) if calibration else -45
        calibration_end=0
    fps=values['fps']
    values=state.update(rms,pitch,confidence,dt,P('Gate'),P('Ceiling'),P('Sensitivity'),P('Transition'),P('Pitchlow'),P('Pitchhigh'),P('Coloursensitivity'))
    values.update(sim_time=sim_time,fps=fps)
    # WASD moves horizontally in the person's heading; projection anchor is untouched.
    drag(app.op('interface/viewport').panel)
    x,z=P('Personx'),P('Personz');right,_,forward=basis(P('Heading'),0)
    move=(int('w' in keys)-int('s' in keys),int('d' in keys)-int('a' in keys))
    norm=max(1,math.hypot(*move));speed=P('Walkspeed')*dt/norm
    x+=(forward[0]*move[0]+right[0]*move[1])*speed
    z+=(forward[2]*move[0]+right[2]*move[1])*speed
    x,z=geo.clamp_person(x,z,P('Width'),P('Depth'),P('Heightcurve'),P('Protrusion'))
    app.par.Personx=x;app.par.Personz=z
    dims=(P('Width'),P('Depth'),P('Height'),P('Heightcurve'),P('Protrusion'))
    if dims!=last_geometry:
        for n in app.op('room').findChildren(type=scriptSOP): n.cook(force=True)
        last_geometry=dims
    cameras()
    app.op('emotion/channels').cook(force=True)
    # Explicit pull guarantees simulation progress even with all network viewers hidden.
    app.op('interface/view').cook(force=True)
    if clock-last_status_time>.15:
        dominant=max(['calm','wonder','joy','intensity'],key=lambda k:values[k])
        meter='|'*int(values['loudness']*26)
        app.op('interface/status_text').par.text=(f"{status}\n{values['rms_db']:.1f} dBFS  {meter:<26}  {values['pitch_hz']:.0f} Hz  / confidence {values['pitch_confidence']:.2f}\n"
            f"{dominant.upper()}   Calm {values['calm']:.0%}   Wonder {values['wonder']:.0%}   Joy {values['joy']:.0%}   Intensity {values['intensity']:.0%}\n"
            f"Idle {values['idle_mix']:.0%}    {fps:.1f} FPS    {'PAUSED' if P('Pause') else 'FLOWING'}    {'256' if P('Quality')=='performance' else '512'} x {'256' if P('Quality')=='performance' else '512'}")
        last_status_time=clock

def startup():
    global last,keys
    last=time.perf_counter();keys=set()
    app.op('audio/microphone').par.active=True
    cameras()
