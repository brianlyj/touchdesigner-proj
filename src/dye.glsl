void main(){
    vec2 uv=vUV.st;
    // Transport is handled by the bounded MacCormack stages before this pass.
    vec3 dye=texture(sTD2DInputs[0],uv).rgb;
    dye*=exp(-uControl.y*(.028+.055*dye.x));
    for(int i=0;i<3;i++){
        vec4 e=emitter(i);vec2 d=uv-center(i);
        float g=exp(-dot(d,d)/(e.w*e.w));
        float strata=.5+.5*sin(dot(d,vec2(153.,221.))*(.5+.5*uStyle.y)+uControl.x*.42+fbm(uv*28.)*9.);
        float ribbon=mix(.45,1.,pow(strata,3.));
        float amount=uControl.y*4.5*uControl.w*g*e.z*ribbon;
        float pigment=clamp(.5+.38*sin(uControl.x*.48+float(i)*2.1)+.16*(strata-.5),0.,1.);
        float pearl=smoothstep(.30,.74,strata)*(.65+.35*(.5+.5*sin(uControl.x*.31+float(i)*2.)));
        dye+=vec3(amount,amount*pigment,amount*pearl);
    }
    dye=clamp(dye,vec3(0),vec3(3));dye.yz=min(dye.yz,vec2(dye.x));
    fragColor=TDOutputSwizzle(vec4(dye,1));
}
