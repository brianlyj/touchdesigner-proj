uniform vec4 uAdvection;
void main(){
    vec2 uv=vUV.st;float dt=uControl.y*uAdvection.x;
    vec2 v=texture(sTD2DInputs[1],uv).xy;
    vec2 mid=texture(sTD2DInputs[1],clampUV(uv-.5*dt*v)).xy;
    fragColor=TDOutputSwizzle(texture(sTD2DInputs[0],clampUV(uv-dt*mid)));
}
