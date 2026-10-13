void main(){
    vec2 uv=vUV.st,h=px();
    float w=.5*uDynamics.w*(texture(sTD2DInputs[0],clampUV(uv+vec2(h.x,0))).y-texture(sTD2DInputs[0],clampUV(uv-vec2(h.x,0))).y-texture(sTD2DInputs[0],clampUV(uv+vec2(0,h.y))).x+texture(sTD2DInputs[0],clampUV(uv-vec2(0,h.y))).x);
    fragColor=TDOutputSwizzle(vec4(w,0,0,1));
}
