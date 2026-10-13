"""Run inside TouchDesigner through TDMCP execute_code.

Creates an independent scene; no pre-existing project operators are removed.
The saved project embeds every callback and uses no external media.
"""
from pathlib import Path
import json

DEST = Path('C:/Users/ASUS/Downloads/TD-proj')
if op('/anamorphic'):
    raise RuntimeError('The anamorphic component already exists; refusing to overwrite it.')

demo = op('/').create(containerCOMP, 'anamorphic')
demo.par.parentshortcut = 'Demo'
demo.par.w = 1344
demo.par.h = 760
demo.par.bgcolorr = 0.035
demo.par.bgcolorg = 0.043
demo.par.bgcolorb = 0.065
demo.par.bgalpha = 1
page = demo.appendCustomPage('Illusion')
def control(name, label, value, lo, hi, kind='Float'):
    p = getattr(page, 'append'+kind)(name, label=label)[0]
    p.default = value
    p.val = value
    p.min = lo
    p.max = hi
    p.normMin = lo
    p.normMax = hi
    p.clampMin = True
    p.clampMax = True
    return p
control('Depth', 'Depth spread', 2.6, 0, 3.6)
control('Orbit', 'Observer angle', 52, -85, 85)
control('Elevation', 'Observer elevation', 12, -30, 30)
control('Segments', 'Ring segments', 36, 8, 72, 'Int')
control('Thickness', 'Ring width', 0.28, 0.08, 0.6)
control('Gap', 'Segment gaps', 0.025, 0, 0.3)
control('Animate', 'Animate depth', True, 0, 1, 'Toggle')
control('Speed', 'Animation speed', 0.035, 0.005, 0.15)

scene = demo.create(baseCOMP, 'scene')
scene.par.parentshortcut = 'Scene'
scene.nodeX, scene.nodeY = -600, 200

def make(kind, name, nx, ny, parent=scene, **pars):
    n = parent.create(kind, name)
    n.nodeX, n.nodeY = nx, ny
    for k, v in pars.items():
        getattr(n.par, k).val = v
    return n

lfo = make(lfoCHOP, 'lfo_motion', -700, 375, wavetype='ramp')
lfo.par.frequency.expr = 'parent.Demo.par.Speed'
motion = make(nullCHOP, 'null_motion', -525, 375)
motion.inputConnectors[0].connect(lfo)

geo = make(geometryCOMP, 'geo_ring', -350, 100)
for child in list(geo.children):
    child.destroy()
geo.par.parentshortcut = 'Ring'
mat = make(constantMAT, 'mat_colour', -350, 300, colorr=1, colorg=1, colorb=1, cullface='neither')
geo.par.material = 'mat_colour'
mesh = make(scriptSOP, 'script_anamorphosis', 0, 0, parent=geo)
callbacks = mesh.par.callbacks.eval()
callbacks.par.language = 'python'
callbacks.text = '''import math
import colorsys

def onCook(scriptOp):
    scriptOp.clear()
    demo = parent.Demo
    depth = demo.par.Depth.eval()
    count = demo.par.Segments.eval()
    width = demo.par.Thickness.eval()
    gap = demo.par.Gap.eval()
    phase = float(parent.Scene.op('null_motion')[0]) * math.tau if demo.par.Animate else 0.0
    scriptOp.pointAttribs.create('Cd', (1.0, 1.0, 1.0, 1.0))
    eye_z = 8.0
    radius = 1.55

    def point_on_ray(radius, angle, z):
        # Scale x and y by the distance from the fixed eye.
        # x/(eye_z-z) and y/(eye_z-z) stay invariant.
        scale = (eye_z-z) / eye_z
        return (radius*math.cos(angle)*scale, radius*math.sin(angle)*scale, z)

    def face(coords, color):
        poly = scriptOp.appendPoly(len(coords), closed=True, addPoints=True)
        for vertex, pos in zip(poly, coords):
            vertex.point.P = pos
            vertex.point.Cd = color

    for i in range(count):
        center = (i+0.5) * math.tau/count
        z = depth * (0.72*math.sin(center*3+phase) + 0.28*math.cos(center*7-phase*0.7))
        a0 = (i+gap/2)*math.tau/count
        a1 = (i+1-gap/2)*math.tau/count
        rgb = colorsys.hsv_to_rgb(0.45 + 0.13*(0.5+0.5*math.sin(center)), 0.68, 1.0)
        color = (*rgb, 1.0)
        side = tuple(c*0.43 for c in rgb)+(1.0,)
        ri, ro = radius-width/2, radius+width/2
        za, zb = z-0.065, z+0.065
        steps = 5
        for j in range(steps):
            a = a0+(a1-a0)*j/steps
            b = a0+(a1-a0)*(j+1)/steps
            for zz, col in [(zb, color), (za, side)]:
                face([point_on_ray(ri,a,zz), point_on_ray(ro,a,zz), point_on_ray(ro,b,zz), point_on_ray(ri,b,zz)], col)
            for rr in (ri, ro):
                face([point_on_ray(rr,a,za), point_on_ray(rr,b,za), point_on_ray(rr,b,zb), point_on_ray(rr,a,zb)], side)
        for a in (a0,a1):
            face([point_on_ray(ri,a,za),point_on_ray(ro,a,za),point_on_ray(ro,a,zb),point_on_ray(ri,a,zb)],side)

def onGetCookLevel(scriptOp):
    return CookLevel.WHEN_USED
'''
outmesh = make(nullSOP, 'null_ring', 200, 0, parent=geo)
outmesh.inputConnectors[0].connect(mesh)
outmesh.display = True
outmesh.render = True
mesh.display = False
mesh.render = False

front = make(cameraCOMP, 'cam_sweet_spot', -125, 375, tz=8, fov=42)
observer = make(cameraCOMP, 'cam_observer', -125, -175, fov=48)
observer.par.tx.expr = '8 * math.sin(math.radians(parent.Demo.par.Orbit)) * math.cos(math.radians(parent.Demo.par.Elevation))'
observer.par.ty.expr = '8 * math.sin(math.radians(parent.Demo.par.Elevation))'
observer.par.tz.expr = '8 * math.cos(math.radians(parent.Demo.par.Orbit)) * math.cos(math.radians(parent.Demo.par.Elevation))'
observer.par.ry.expr = 'parent.Demo.par.Orbit'
observer.par.rx.expr = '-parent.Demo.par.Elevation'

def render(name, camera, y):
    n = make(renderTOP, name, 100, y, camera=camera, geometry='geo_ring', lights='',
             outputresolution='custom', resolutionw=512, resolutionh=448, antialias='aa4',
             bgcolorr=0.018, bgcolorg=0.025, bgcolorb=0.04, bgcolora=1)
    out = make(nullTOP, 'null_'+name, 300, y)
    out.inputConnectors[0].connect(n)
    return out
view_a = render('render_sweet_spot', 'cam_sweet_spot', 125)
view_b = render('render_observer', 'cam_observer', -125)

def texttop(name, text, w, h, size, color=(0.7,0.76,0.84), x=500, y=0):
    t = make(textTOP, name, x, y, text=text, outputresolution='custom',
             resolutionw=w, resolutionh=h, font='Segoe UI', fontautosize='nofit',
             fontsizexunit='pixels', fontsizeyunit='pixels', fontsizex=size, fontsizey=size,
             alignx='center', aligny='center', bgalpha=1,
             bgcolorr=0.018, bgcolorg=0.025, bgcolorb=0.04,
             fontcolorr=color[0], fontcolorg=color[1], fontcolorb=color[2])
    return t

def layout(name, inputs, direction, w, h, x, y):
    n = make(layoutTOP, name, x, y, align=direction, outputresolution='custom', resolutionw=w, resolutionh=h)
    for idx, source in enumerate(inputs):
        n.inputConnectors[idx].connect(source)
    return n

ta = texttop('text_sweet_spot','01  /  THE SWEET SPOT',512,48,17,(0.35,0.95,0.84),500,400)
tb = texttop('text_observer','02  /  ANOTHER VIEWPOINT',512,48,17,(0.57,0.69,1.0),500,-325)
sa = texttop('text_front_note','A circle, from precisely one position.',512,40,15,x=500,y=275)
sb = texttop('text_side_note','The same pieces, scattered in depth.',512,40,15,x=500,y=-450)
cola = layout('layout_front',[ta,view_a,sa],'verttb',512,536,725,200)
colb = layout('layout_side',[tb,view_b,sb],'verttb',512,536,725,-100)
pair = layout('layout_two_views',[cola,colb],'horizlr',1024,536,950,100)
title = texttop('text_title','ANAMORPHIC / 01',1024,84,32,(0.91,0.95,1.0),950,300)
footer = texttop('text_footer','One object. Two cameras.   |   Set depth to 0 to reveal the construction.',1024,68,16,x=950,y=-175)
final = layout('layout_presentation',[title,pair,footer],'verttb',1024,688,1175,100)
out = make(nullTOP, 'null_output', 1400, 100)
out.inputConnectors[0].connect(final)
export = make(outTOP, 'out1', 1600, 100)
export.inputConnectors[0].connect(out)

screen = make(containerCOMP, 'preview', 0, 200, parent=demo, w=1024,h=688,x=16,y=48)
screen.par.top.expr = "parent.Demo.op('scene/null_output')"
screen.par.topfill = 'best'
controls = make(parameterCOMP, 'controls', 250, 200, parent=demo, w=288,h=520,x=1048,y=170)
controls.par.op.expr = 'parent.Demo'
controls.par.pagescope = 'Illusion'

readme = make(textDAT, 'README', -600, -100, parent=demo)
readme.text = '''ANAMORPHIC / 01 - A perspective illusion

Open /anamorphic as a viewer, or press F1 for the presentation.
The panel on the right contains the live Illusion parameters.

Try:
1. Set Depth spread to 0. Every wedge lies on one ring.
2. Raise Depth spread to 2.6. The left view remains a circle.
3. Set Observer angle and Observer elevation to 0. Both cameras align.
4. Toggle Animate depth to move the wedges along the fixed camera rays.

This is spatial perspective anamorphosis, not an anamorphic lens effect.
Every vertex follows P = Eye + scale * (Original - Eye).
Perspective division cancels scale, preserving the sweet-spot image.

Inside scene: one Script SOP mesh -> Null SOP -> Geometry COMP,
two Camera COMPs -> two Render TOPs -> Layout TOPs -> null_output.
The Python callback is embedded, commented, and editable.
No external media or third-party Python packages are needed.

The official TDMCP component is at /TDMCP, localhost:13316/mcp.
'''
demo.par.opviewer = 'preview'
demo.nodeX, demo.nodeY = 500, 0
demo.nodeWidth, demo.nodeHeight = 360, 260
demo.color = (0.12,0.5,0.45)
op('/TDMCP').par.Followactive = False
op('/TDMCP').par.Animatenodes = False
op('/TDMCP').par.Installfor = 'codex'
op('/TDMCP').nodeX, op('/TDMCP').nodeY = 0, -400

# Preserve the initial project but stop its unrelated rendering.
op('/project1').allowCooking = False
for pane in ui.panes:
    if pane.type == PaneType.NETWORKEDITOR:
        pane.owner = demo
        pane.home()

op('/perform').par.winop = demo
mesh.cook(force=True)
out.cook(force=True)
print(json.dumps({'created':demo.path,'points':mesh.numPoints,'primitives':mesh.numPrims,'output':[out.width,out.height],'errors':demo.errors(recurse=True)}))
