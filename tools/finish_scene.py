from pathlib import Path
scene = op('/anamorphic/scene')
demo = op('/anamorphic')
s = scene.op('geo_ring/script_anamorphosis')
cb = s.par.callbacks.eval()
cb.text = cb.text.replace("scriptOp.pointAttribs.create('Cd', (1.0, 1.0, 1.0, 1.0))", "scriptOp.pointAttribs.create('Cd')")
s.parent().render = True
s.parent().display = True
s.viewer = True

for n in scene.children:
    if n.family == 'TOP':
        n.par.outputaspect = 'resolution'
    if n.type == 'text':
        n.par.keepfontratio = True
    n.viewer = True

# Exact pixel placement preserves unequal header/image/footer sizes.
compositor = scene.create(glslmultiTOP, 'glsl_presentation')
compositor.nodeX, compositor.nodeY = 1175, 100
compositor.par.outputresolution = 'custom'
compositor.par.resolutionw = 1024
compositor.par.resolutionh = 688
compositor.par.outputaspect = 'resolution'
names = ['null_render_sweet_spot','null_render_observer','text_title',
         'text_sweet_spot','text_observer','text_front_note','text_side_note','text_footer']
for i,name in enumerate(names):
    compositor.inputConnectors[i].connect(scene.op(name))
pixel = compositor.par.pixeldat.eval()
pixel.par.language = 'glsl'
pixel.text = '''out vec4 fragColor;
void main() {
    vec2 p = vUV.st * vec2(1024.0, 688.0);
    vec4 c = vec4(0.018,0.025,0.04,1.0);
    bool left = p.x < 512.0;
    float x = left ? p.x : p.x-512.0;
    if (p.y < 68.0) c = texture(sTD2DInputs[7],vec2(p.x/1024.0,p.y/68.0));
    else if (p.y < 108.0) {
        vec2 uv=vec2(x/512.0,(p.y-68.0)/40.0);
        c = left ? texture(sTD2DInputs[5],uv) : texture(sTD2DInputs[6],uv);
    } else if (p.y < 556.0) {
        vec2 uv=vec2(x/512.0,(p.y-108.0)/448.0);
        c = left ? texture(sTD2DInputs[0],uv) : texture(sTD2DInputs[1],uv);
    } else if (p.y < 604.0) {
        vec2 uv=vec2(x/512.0,(p.y-556.0)/48.0);
        c = left ? texture(sTD2DInputs[3],uv) : texture(sTD2DInputs[4],uv);
    } else c=texture(sTD2DInputs[2],vec2(p.x/1024.0,(p.y-604.0)/84.0));
    if(abs(p.x-512.0)<0.5 && p.y>90.0 && p.y<584.0) c=vec4(0.10,0.14,0.19,1.0);
    if(abs(p.y-604.0)<0.5 || abs(p.y-68.0)<0.5) c=vec4(0.10,0.14,0.19,1.0);
    fragColor=TDOutputSwizzle(c);
}
'''
scene.op('null_output').inputConnectors[0].connect(compositor)
for name in ['layout_front','layout_side','layout_two_views','layout_presentation']:
    scene.op(name).destroy()
demo.par.opviewer = ''
demo.viewer = True
scene.viewer = True
demo.op('preview').viewer = True
demo.op('controls').viewer = True
# Needed once to initialize the newly edited Script SOP callback immediately.
s.cook(force=True)
print('mesh',s.numPoints,s.numPrims,s.errors())
print('errors',demo.errors(recurse=True))
