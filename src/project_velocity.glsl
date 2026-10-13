void main(){
    vec2 uv=vUV.st,h=px();
    vec2 grad=.5*uDynamics.w*vec2(texture(sTD2DInputs[1],clampUV(uv+vec2(h.x,0))).r-texture(sTD2DInputs[1],clampUV(uv-vec2(h.x,0))).r,
            texture(sTD2DInputs[1],clampUV(uv+vec2(0,h.y))).r-texture(sTD2DInputs[1],clampUV(uv-vec2(0,h.y))).r);
    vec2 v=texture(sTD2DInputs[0],uv).xy-grad;
    fragColor=TDOutputSwizzle(vec4(boundedVelocity(v,uv),0,1));
}
