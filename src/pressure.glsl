void main(){
    vec2 uv=vUV.st,h=px();
    float sum=texture(sTD2DInputs[0],clampUV(uv+vec2(h.x,0))).r+texture(sTD2DInputs[0],clampUV(uv-vec2(h.x,0))).r+
              texture(sTD2DInputs[0],clampUV(uv+vec2(0,h.y))).r+texture(sTD2DInputs[0],clampUV(uv-vec2(0,h.y))).r;
    float div=texture(sTD2DInputs[1],uv).r;
    fragColor=TDOutputSwizzle(vec4((sum-div*h.x*h.y)*.25,0,0,1));
}
