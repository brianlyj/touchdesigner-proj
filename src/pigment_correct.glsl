void main(){
    vec2 uv=vUV.st;
    vec2 v=texture(sTD2DInputs[3],uv).xy;
    vec2 mid=texture(sTD2DInputs[3],clampUV(uv-.5*uControl.y*v)).xy;
    vec2 departure=clampUV(uv-uControl.y*mid);
    vec2 cell=(floor(departure*uDynamics.w-.5)+.5)*px();
    vec3 a=texture(sTD2DInputs[0],clampUV(cell)).rgb;
    vec3 b=texture(sTD2DInputs[0],clampUV(cell+vec2(px().x,0))).rgb;
    vec3 c=texture(sTD2DInputs[0],clampUV(cell+vec2(0,px().y))).rgb;
    vec3 d=texture(sTD2DInputs[0],clampUV(cell+px())).rgb;
    vec3 q=texture(sTD2DInputs[1],uv).rgb+.5*(texture(sTD2DInputs[0],uv).rgb-texture(sTD2DInputs[2],uv).rgb);
    q=clamp(q,min(min(a,b),min(c,d)),max(max(a,b),max(c,d)));
    q=max(q,vec3(0));q.yz=min(q.yz,vec2(q.x));
    fragColor=TDOutputSwizzle(vec4(q,1));
}
