import json
s = op('/anamorphic/scene/geo_ring/script_anamorphosis')
g = s.parent()
g.render = True
g.display = True
s.cook(force=True)
print('GEO',g.render,g.display,'MESH',s.numPoints, s.errors())
print('CALLBACK',s.par.callbacks.eval().module)
print('PARS',[(p.name, str(p.eval())) for p in s.pars()])
print('LAYOUT',[(p.name,str(p.eval()),p.menuNames) for p in op('/anamorphic/scene/layout_presentation').pars() if p.page.name == 'Layout'])
op('/anamorphic/scene/render_sweet_spot').cook(force=True)
print('POST',s.numPoints,s.errors(),g.errors(recurse=True))
