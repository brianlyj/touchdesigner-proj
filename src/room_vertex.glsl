out vec3 worldPosition;
void main(){
    vec4 world=TDDeform(TDPos());
    worldPosition=world.xyz;
    gl_Position=TDWorldToProj(world);
#ifdef TD_PICKING_ACTIVE
    TDWritePickingValues();
#endif
}
