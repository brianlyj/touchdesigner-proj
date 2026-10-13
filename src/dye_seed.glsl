void main(){
    vec2 uv=vUV.st;
    vec2 warp=vec2(fbm(uv*4.),fbm(uv*4.+7.3));
    float layer=.5+.5*sin(uv.y*32.+uv.x*9.+warp.x*19.);
    float fine=fbm(uv*65.+warp*8.);
    float density=.20+.65*smoothstep(.18,.82,fbm(uv*5.+warp*3.));
    float identity=clamp(.12+.76*layer+.13*(fine-.5),0.,1.);
    float pearl=smoothstep(.42,.62,fbm(uv*8.+warp*5.)+.18*sin(uv.y*110.+warp.y*26.));
    fragColor=TDOutputSwizzle(vec4(density,density*identity,density*pearl,1));
}
