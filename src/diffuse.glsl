void main(){
    vec2 uv=vUV.st,h=px();
    vec2 rhs=texture(sTD2DInputs[1],uv).xy;
    vec2 sum=texture(sTD2DInputs[0],clampUV(uv+vec2(h.x,0))).xy+texture(sTD2DInputs[0],clampUV(uv-vec2(h.x,0))).xy+
             texture(sTD2DInputs[0],clampUV(uv+vec2(0,h.y))).xy+texture(sTD2DInputs[0],clampUV(uv-vec2(0,h.y))).xy;
    float nu=.000002+.0006*uDynamics.x*uDynamics.x;
    float a=uControl.y*nu*uDynamics.w*uDynamics.w;
    fragColor=TDOutputSwizzle(vec4(boundedVelocity((rhs+a*sum)/(1.0+4.0*a),uv),0,1));
}
