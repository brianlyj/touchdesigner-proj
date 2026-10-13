void main(){TDCheckDiscard();float depth=dot(worldPosition-uEye.xyz,uForward.xyz);fragColor=TDOutputSwizzle(vec4(depth,depth,depth,1));}
