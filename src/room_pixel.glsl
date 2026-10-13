uniform sampler2D sFluid;
uniform sampler2D sReference;
uniform vec4 uSurface; // pattern: 0 ink, 1 checkerboard, 2 circle; projection strength, surface index
void main(){
    TDCheckDiscard();
    vec3 n=normalize(cross(dFdx(worldPosition),dFdy(worldPosition)));
    float shade=.65+.35*abs(dot(n,normalize(vec3(.4,.85,.2))));
    vec3 base=vec3(.065,.081,.103)*shade;
    float floorGrid=0.0;
    if(abs(n.y)>.8){
        vec2 grid=abs(fract(worldPosition.xz+.5)-.5)/max(fwidth(worldPosition.xz),vec2(.0001));
        floorGrid=1.0-min(min(grid.x,grid.y),1.0);
        base+=floorGrid*vec3(.035,.047,.06);
    }
    vec3 c=cameraPoint(worldPosition);
    if(c.z>.05){
        vec2 uv=vec2(c.x/(c.z*uEye.w),c.y/(c.z*uEye.w/uRight.w))*.5+.5;
        if(all(greaterThanEqual(uv,vec2(0)))&&all(lessThanEqual(uv,vec2(1)))){
            ivec2 sz=textureSize(sReference,0);
            float d=texelFetch(sReference,clamp(ivec2(uv*vec2(sz)),ivec2(0),sz-1),0).r;
            if(abs(c.z-d)<max(.025,c.z*.006)){
                vec3 ink=texture(sFluid,uv).rgb;
                if(uSurface.x>.5&&uSurface.x<1.5){
                    vec2 cell=floor(uv*vec2(16,9));float checker=mod(cell.x+cell.y,2.);
                    ink=mix(vec3(.035,.12,.18),vec3(.5,.95,.88),checker);
                }else if(uSurface.x>1.5){
                    vec2 q=(uv-.5)*vec2(uRight.w,1);
                    float radius=length(q);
                    float line=1.-smoothstep(.006,.014,abs(radius-.31));
                    float crosshair=(1.-smoothstep(.002,.005,abs(q.x)))*(1.-smoothstep(.025,.05,abs(q.y)))+
                                    (1.-smoothstep(.002,.005,abs(q.y)))*(1.-smoothstep(.025,.05,abs(q.x)));
                    ink=vec3(.1,.9,.75)*clamp(line+crosshair,0.,1.);
                }
                base+=ink*uSurface.y;
            }
        }
    }
    fragColor=TDOutputSwizzle(vec4(base,1));
}
