uniform vec4 uMood;
uniform vec4 uLook; // saturation, brightness, time, unused
uniform vec4 uStyle;
out vec4 fragColor;
vec3 toLab(vec3 c){
    vec3 lms=mat3(.41222147,.21190350,.08830246,.53633254,.68069955,.28171884,.05144599,.10739696,.62997870)*c;
    lms=pow(max(lms,vec3(0)),vec3(1.0/3.0));
    return mat3(.21045426,1.9779985,.02590404,.79361779,-2.4285922,.78277177,-.00407205,.4505937,-.80867577)*lms;
}
vec3 fromLab(vec3 c){
    vec3 lms=vec3(c.x+.39633778*c.y+.21580376*c.z,c.x-.10556135*c.y-.06385417*c.z,c.x-.08948418*c.y-1.29148555*c.z);
    lms=lms*lms*lms;
    return mat3(4.07674166,-1.268438,-.00419609,-3.30771159,2.6097574,-.70341861,.23096993,-.3413194,1.7076147)*lms;
}
vec3 gradient(vec3 a,vec3 b,vec3 c,float t){return t<.5?mix(toLab(a),toLab(b),t*2.):mix(toLab(b),toLab(c),(t-.5)*2.);}
void main(){
    vec3 dye=texture(sTD2DInputs[0],vUV.st).rgb;
    float t=clamp(dye.y/max(dye.x,.001),0.,1.);
    float milk=clamp(dye.z/max(dye.x,.001),0.,1.);
    vec3 calm=gradient(vec3(.001,.005,.028),vec3(.004,.13,.18),vec3(.12,.6,.65),t);
    vec3 wonder=gradient(vec3(.016,.003,.055),vec3(.19,.045,.40),vec3(.66,.30,.50),t);
    vec3 joy=gradient(vec3(.18,.003,.018),vec3(.82,.10,.055),vec3(.92,.48,.07),t);
    vec3 intense=gradient(vec3(.035,.001,.009),vec3(.64,.012,.008),vec3(.22,.015,.10),t);
    vec3 lab=calm*uMood.x+wonder*uMood.y+joy*uMood.z+intense*uMood.w;
    lab.yz*=uLook.x;
    vec3 pearl=toLab(vec3(.58,.63,.62));
    // A narrow concentration band leaves coloured ink and pale folds distinct.
    lab=mix(lab,pearl,smoothstep(.46,.70,milk)*.91);
    vec3 col=max(fromLab(lab),vec3(0));
    vec2 texel=1./vec2(textureSize(sTD2DInputs[0],0));
    vec3 dx=texture(sTD2DInputs[0],vUV.st+vec2(texel.x,0)).rgb-texture(sTD2DInputs[0],vUV.st-vec2(texel.x,0)).rgb;
    vec3 dy=texture(sTD2DInputs[0],vUV.st+vec2(0,texel.y)).rgb-texture(sTD2DInputs[0],vUV.st-vec2(0,texel.y)).rgb;
    vec2 slope=vec2(dot(dx,vec3(.25,.20,.55)),dot(dy,vec3(.25,.20,.55)))/texel* .016;
    vec3 normal=normalize(vec3(-slope*uStyle.z,1.));
    vec3 light=normalize(vec3(-.45,.65,1.));
    float diffuse=.32+.68*max(dot(normal,light),0.);
    float spec=pow(max(dot(reflect(-light,normal),vec3(0,0,1)),0.),28.)*.16*uStyle.z;
    float density=1.0-exp(-dye.x*2.8);
    col=(col*diffuse+spec*mix(vec3(.18),vec3(.7),milk))*density*uLook.y;
    col=col/(1.+col*.25);
    fragColor=TDOutputSwizzle(vec4(clamp(col,0.,1.),1));
}
