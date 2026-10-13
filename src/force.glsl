void main(){
    vec2 uv=vUV.st;
    vec2 old=texture(sTD2DInputs[0],uv).xy;
    vec2 v=texture(sTD2DInputs[0],clampUV(uv-uControl.y*old)).xy;
    v*=exp(-uControl.y*.12);
    float breathe=1.0+.15*sin(uControl.x*6.283185/20.0);
    // Multi-scale divergence-free stirring rolls the broad billows into smaller eddies.
    vec2 stirring=vec2(0);
    for(int j=0;j<3;j++){
        float k=6.283185*(j==0?2.:(j==1?5.:11.));
        float a=j==0?.035:(j==1?.018:.007);
        vec2 q=uv*k+vec2(uControl.x*.12+float(j)*1.7,-uControl.x*.09);
        stirring+=a*vec2(sin(q.x)*cos(q.y),-cos(q.x)*sin(q.y));
    }
    v+=uControl.y*stirring*uControl.z*(4.+4.*uStyle.y);
    for(int i=0;i<3;i++){
        vec4 e=emitter(i);vec2 d=uv-center(i);
        float g=exp(-dot(d,d)/(e.w*e.w*6.0));
        float signv=i==1?-1.0:1.0;
        vec2 vortex=vec2(-d.y,d.x)*signv*3.5;
        float angle=uDynamics.y*3.14159+float(i)*2.094+uControl.x*.23;
        vec2 push=vec2(cos(angle),sin(angle))*.045;
        v+=uControl.y*(vortex+push)*g*e.z*(uControl.z*2.6+uDynamics.z*.3)*breathe;
    }
    fragColor=TDOutputSwizzle(vec4(boundedVelocity(v,uv),0,1));
}
