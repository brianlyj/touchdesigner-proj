void main(){
    vec2 uv=vUV.st,h=px();
    float w=texture(sTD2DInputs[1],uv).r;
    vec2 g=vec2(abs(texture(sTD2DInputs[1],clampUV(uv+vec2(h.x,0))).r)-abs(texture(sTD2DInputs[1],clampUV(uv-vec2(h.x,0))).r),abs(texture(sTD2DInputs[1],clampUV(uv+vec2(0,h.y))).r)-abs(texture(sTD2DInputs[1],clampUV(uv-vec2(0,h.y))).r));
    g/=length(g)+.00001;
    vec2 f=(8.+20.*uControl.z)*uStyle.x*h*w*vec2(g.y,-g.x);
    vec2 v=texture(sTD2DInputs[0],uv).xy+uControl.y*clamp(f,vec2(-.25),vec2(.25));
    fragColor=TDOutputSwizzle(vec4(boundedVelocity(v,uv),0,1));
}
