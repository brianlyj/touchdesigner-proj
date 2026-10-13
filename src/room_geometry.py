"""Shared metre-scale, Y-up geometry for TouchDesigner and Blender."""
import math

def room(width=6.0, depth=5.0, height=3.0, curve=0.4, protrusion=0.55):
    w, d, h = width/2, depth/2, height
    shapes = {}
    def add(name, vertices, faces):
        shapes[name] = {'vertices': vertices, 'faces': faces}
    add('floor', [(-w,0,-d),(w,0,-d),(w,0,d),(-w,0,d)], [(0,1,2,3)])
    add('ceiling', [(-w,h,-d),(-w,h,d),(w,h,d),(w,h,-d)], [(0,1,2,3)])
    add('front_wall', [(-w,0,-d),(-w,h,-d),(w,h,-d),(w,0,-d)], [(0,1,2,3)])
    add('back_wall', [(-w,0,d),(w,0,d),(w,h,d),(-w,h,d)], [(0,1,2,3)])
    add('left_wall', [(-w,0,-d),(-w,0,d),(-w,h,d),(-w,h,-d)], [(0,1,2,3)])
    vertices, faces = [], []
    for i in range(65):
        t=i/64
        z=-d+depth*t
        x=w-curve*math.sin(math.pi*t)**2
        vertices.extend([(x,0,z),(x,h,z)])
        if i: faces.append((2*i-2,2*i-1,2*i+1,2*i))
    add('curved_wall',vertices,faces)
    x0,x1 = -0.8,0.45
    y1=min(2.15,h*0.78)
    z0,z1=-d,-d+protrusion
    v=[(x0,0,z0),(x1,0,z0),(x1,y1,z0),(x0,y1,z0),
       (x0,0,z1),(x1,0,z1),(x1,y1,z1),(x0,y1,z1)]
    add('protrusion',v,[(4,5,6,7),(0,4,7,3),(5,1,2,6),(3,7,6,2)])
    return shapes

def mannequin():
    v, f = [], []
    def ellipsoid(center, size, rows=10, cols=16):
        start=len(v)
        for i in range(rows+1):
            a=math.pi*i/rows
            for j in range(cols):
                b=math.tau*j/cols
                v.append((center[0]+size[0]*math.sin(a)*math.cos(b),
                          center[1]+size[1]*math.cos(a),
                          center[2]+size[2]*math.sin(a)*math.sin(b)))
        for i in range(rows):
            for j in range(cols):
                f.append((start+i*cols+j,start+i*cols+(j+1)%cols,
                          start+(i+1)*cols+(j+1)%cols,start+(i+1)*cols+j))
    ellipsoid((0,1.62,0),(0.105,0.14,0.11))
    ellipsoid((0,1.25,0),(0.21,0.25,0.11))
    ellipsoid((0,0.94,0),(0.16,0.15,0.105))
    for sign in (-1,1):
        ellipsoid((sign*0.24,1.22,0),(0.065,0.21,0.065))
        ellipsoid((sign*0.28,0.94,-0.025),(0.05,0.15,0.05))
        ellipsoid((sign*0.29,0.77,-0.025),(0.047,0.065,0.04))
        ellipsoid((sign*0.105,0.64,0),(0.085,0.23,0.085))
        ellipsoid((sign*0.105,0.24,0),(0.062,0.23,0.065))
        ellipsoid((sign*0.105,0.055,-0.065),(0.07,0.055,0.14))
    return {'vertices':v,'faces':f}

def clamp_person(x,z,width,depth,curve,protrusion,radius=0.23):
    d=depth/2
    z=max(-d+radius,min(d-radius,z))
    right=width/2-curve*math.sin(math.pi*(z+d)/depth)**2-radius
    x=max(-width/2+radius,min(right,x))
    if -0.8-radius<x<0.45+radius and z<-d+protrusion+radius:
        distances=[(abs(x-(-0.8-radius)),'l'),(abs(x-(0.45+radius)),'r'),(abs(z-(-d+protrusion+radius)),'f')]
        side=min(distances)[1]
        if side=='l': x=-0.8-radius
        elif side=='r': x=0.45+radius
        else: z=-d+protrusion+radius
    return x,z
