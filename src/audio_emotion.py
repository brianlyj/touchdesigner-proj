"""Dependency-free apart from bundled NumPy. Shared by TD and verification."""
import math
import numpy as np

def yin(samples, sample_rate=12000, low=80, high=1000):
    x=np.asarray(samples,dtype=np.float64)
    if len(x)<512 or np.sqrt(np.mean(x*x))<1e-6: return 0.0,0.0
    x=x-x.mean()
    # Fixed-length difference windows avoid bias toward the large lags.
    hi=min(int(sample_rate/low)+2,len(x)//3)
    lo=max(2,int(sample_rate/high))
    n=len(x)-hi
    base=x[:n]
    differences=np.array([np.sum((base-x[t:t+n])**2) for t in range(hi+1)])
    cmnd=np.ones(hi+1)
    cumulative=np.cumsum(differences[1:])
    cmnd[1:]=differences[1:]*np.arange(1,hi+1)/np.maximum(cumulative,1e-20)
    t=lo
    while t<hi:
        if cmnd[t]<0.15:
            while t+1<=hi and cmnd[t+1]<cmnd[t]: t+=1
            break
        t+=1
    if t>=hi: return 0.0,0.0
    offset=0.0
    if 0<t<hi:
        a,b,c=cmnd[t-1:t+2]
        denom=a-2*b+c
        if abs(denom)>1e-12: offset=0.5*(a-c)/denom
    frequency=sample_rate/(t+offset)
    if frequency<low*.98 or frequency>high*1.02: return 0.0,0.0
    return float(np.clip(frequency,low,high)),float(np.clip(1-cmnd[t],0,1))

class EmotionalState:
    def __init__(self):
        self.level=0.0
        self.last_pitch=180.0
        self.pitch_norm=0.0
        self.idle=1.0
        self.silence=2.0
        self.weights=np.array([1.,0.,0.,0.])
        self.onset=0.0
    def update(self,rms,pitch,confidence,dt,gate_db=-45,ceiling_db=-12,sensitivity=1,transition=1,pitch_low=85,pitch_high=255,colour_sensitivity=1.8):
        dt=min(max(dt,1e-4),0.1)
        db=20*math.log10(max(rms,1e-9))
        active=db>gate_db
        target=float(np.clip((db-gate_db)/max(ceiling_db-gate_db,6)*sensitivity,0,1)) if active else 0.0
        old=self.level
        tau=.03 if target>old else .25
        self.level+=(target-self.level)*(1-math.exp(-dt/tau))
        self.onset=max(self.onset*math.exp(-dt/.3),max(0,self.level-old)*4)
        voiced=active and confidence>=.8 and 80<=pitch<=1000
        if voiced:
            self.last_pitch=pitch
            lo=max(80,min(pitch_low,990));hi=max(lo+10,min(pitch_high,1000))
            p=np.clip(math.log2(pitch/lo)/math.log2(hi/lo),0,1)
            self.pitch_norm+=(p-self.pitch_norm)*(1-math.exp(-dt/.15))
        self.silence=0 if active else self.silence+dt
        if active: self.idle=max(0,self.idle-dt/.4)
        elif self.silence>1: self.idle=min(1,self.idle+dt/8)
        # Shape only the palette coordinates; the measured channels and force stay honest.
        # Gain 1 is the original linear response. Higher gain brings normal speech
        # into the warm palettes sooner and makes neighbouring pitch colours clearer.
        gain=float(np.clip(colour_sensitivity,.25,4))
        a=1-(1-float(np.clip(self.level,0,1)))**gain
        raw_p=float(np.clip(self.pitch_norm,0,1))
        p=raw_p**gain/(raw_p**gain+(1-raw_p)**gain)
        target=np.array([(1-a)*(1-p),(1-a)*p,a*p,a*(1-p)])
        target=target*(1-self.idle)+np.array([1,0,0,0])*self.idle
        self.weights+=(target-self.weights)*(1-math.exp(-dt/max(transition,.05)))
        self.weights/=max(self.weights.sum(),1e-9)
        return dict(loudness=self.level,pitch_hz=self.last_pitch,pitch_norm=self.pitch_norm,
                    pitch_confidence=confidence if active else 0,voiced=float(voiced),idle_mix=self.idle,
                    colour_loudness=a,colour_pitch_norm=p,
                    calm=self.weights[0],wonder=self.weights[1],joy=self.weights[2],intensity=self.weights[3],
                    onset=self.onset,rms_db=db,
                    force=.12+self.level*.88,
                    injection=.08+self.level*.92,
                    viscosity=.7*self.idle+(1-self.idle)*(.8-.65*self.pitch_norm))
