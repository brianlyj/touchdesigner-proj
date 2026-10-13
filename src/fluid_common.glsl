uniform vec4 uControl; // simulation seconds, fixed dt, force, injection
uniform vec4 uDynamics; // viscosity, pitch, onset, resolution
uniform vec4 uEmitter1;
uniform vec4 uEmitter2;
uniform vec4 uEmitter3;
uniform vec4 uStyle; // vorticity, filament detail, surface sheen, unused
out vec4 fragColor;
vec2 px(){ return vec2(1.0/uDynamics.w); }
vec2 clampUV(vec2 uv){ return clamp(uv,px()*0.5,1.0-px()*0.5); }
vec4 emitter(int i){return i==0?uEmitter1:(i==1?uEmitter2:uEmitter3);}
vec2 center(int i){vec4 e=emitter(i);float t=uControl.x;return clamp(e.xy+0.13*vec2(sin(t*.16+float(i)*2.1),cos(t*.13+float(i)*3.7)),vec2(.05),vec2(.95));}
vec2 boundedVelocity(vec2 v,vec2 uv){
    if(uv.x<px().x*1.5||uv.x>1.0-px().x*1.5)v.x=0.0;
    if(uv.y<px().y*1.5||uv.y>1.0-px().y*1.5)v.y=0.0;
    return clamp(v,vec2(-.6),vec2(.6));
}
float hash21(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float noise2(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash21(i),hash21(i+vec2(1,0)),f.x),mix(hash21(i+vec2(0,1)),hash21(i+1.),f.x),f.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*noise2(p);p=mat2(.8,.6,-.6,.8)*p*2.03+13.7;a*=.5;}return v;}
