void main(){
    vec2 uv=vUV.st,h=px();
    float div=.5*uDynamics.w*(texture(sTD2DInputs[0],clampUV(uv+vec2(h.x,0))).x-texture(sTD2DInputs[0],clampUV(uv-vec2(h.x,0))).x+
                texture(sTD2DInputs[0],clampUV(uv+vec2(0,h.y))).y-texture(sTD2DInputs[0],clampUV(uv-vec2(0,h.y))).y);
    fragColor=TDOutputSwizzle(vec4(div,0,0,1));
}
