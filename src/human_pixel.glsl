in vec3 worldPosition;
out vec4 fragColor;
void main(){
    TDCheckDiscard();
    vec3 n=normalize(cross(dFdx(worldPosition),dFdy(worldPosition)));
    float shade=.25+.75*abs(dot(n,normalize(vec3(.2,.8,.5))));
    fragColor=TDOutputSwizzle(vec4(vec3(.55,.59,.60)*shade,1));
}
