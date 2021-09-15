from math import sin, cos, pi, sqrt
import cadquery as cq

def show_object(_):
    pass

# TEST_1
# example from PythonOCC core_geometry_geomplate.py, use of thickness = 0 returns 2D surface.
thickness = 0
edge_points = [[0.0, 0.0, 0.0], [0.0, 10.0, 0.0], [0.0, 10.0, 10.0], [0.0, 0.0, 10.0]]
surface_points = [[5.0, 5.0, 5.0]]
plate_0 = cq.Workplane("XY").interpPlate(edge_points, surface_points, thickness)
print("plate_0.val().Volume() = ", plate_0.val().Volume())
plate_0 = plate_0.translate((0, 6 * 12, 0))
show_object(plate_0)

# EXAMPLE 1
# Plate with 5 sides and 2 bumps, one side is not co-planar with the other sides
thickness = 0.1
edge_points = [
    [-7.0, -7.0, 0.0],
    [-3.0, -10.0, 3.0],
    [7.0, -7.0, 0.0],
    [7.0, 7.0, 0.0],
    [-7.0, 7.0, 0.0],
]
edge_wire = cq.Workplane("XY").polyline(
    [(-7.0, -7.0), (7.0, -7.0), (7.0, 7.0), (-7.0, 7.0)]
)
# edge_wire = edge_wire.add(cq.Workplane("YZ").workplane().transformed(offset=cq.Vector(0, 0, -7), rotate=cq.Vector(45, 0, 0)).polyline([(-7.,0.), (3,-3), (7.,0.)]))
# In CadQuery Sept-2019 it worked with rotate=cq.Vector(0, 45, 0). In CadQuery Dec-2019 rotate=cq.Vector(45, 0, 0) only closes the wire.
edge_wire = edge_wire.add(
    cq.Workplane("YZ")
    .workplane()
    .transformed(offset=cq.Vector(0, 0, -7), rotate=cq.Vector(45, 0, 0))
    .spline([(-7.0, 0.0), (3, -3), (7.0, 0.0)])
)
surface_points = [[-3.0, -3.0, -3.0], [3.0, 3.0, 3.0]]
plate_1 = cq.Workplane("XY").interpPlate(edge_wire, surface_points, thickness)
# plate_1 = cq.Workplane("XY").interpPlate(edge_points, surface_points, thickness) # list of (x,y,z) points instead of wires for edges
print("plate_1.val().Volume() = ", plate_1.val().Volume())
show_object(plate_1)

# EXAMPLE 2
# Embossed star, need to change optional parameters to obtain nice looking result.
r1 = 3.0
r2 = 10.0
fn = 6
thickness = 0.1
edge_points = [
    [r1 * cos(i * pi / fn), r1 * sin(i * pi / fn)]
    if i % 2 == 0
    else [r2 * cos(i * pi / fn), r2 * sin(i * pi / fn)]
    for i in range(2 * fn + 1)
]
edge_wire = cq.Workplane("XY").polyline(edge_points)
r2 = 4.5
surface_points = [
    [r2 * cos(i * pi / fn), r2 * sin(i * pi / fn), 1.0] for i in range(2 * fn)
] + [[0.0, 0.0, -2.0]]
plate_2 = cq.Workplane("XY").interpPlate(
    edge_wire,
    surface_points,
    thickness,
    combine=True,
    clean=True,
    degree=3,
    nbPtsOnCur=15,
    nbIter=2,
    anisotropy=False,
    tol2d=0.00001,
    tol3d=0.0001,
    tolAng=0.01,
    tolCurv=0.1,
    maxDeg=8,
    maxSegments=49,
)
# plate_2 = cq.Workplane("XY").interpPlate(edge_points, surface_points, thickness, combine=True, clean=True, Degree=3, NbPtsOnCur=15, NbIter=2, Anisotropie=False, Tol2d=0.00001, Tol3d=0.0001, TolAng=0.01, TolCurv=0.1, MaxDeg=8, MaxSegments=49) # list of (x,y,z) points instead of wires for edges
print("plate_2.val().Volume() = ", plate_2.val().Volume())
plate_2 = plate_2.translate((0, 2 * 12, 0))
show_object(plate_2)

# EXAMPLE 3
# Points on hexagonal pattern coordinates, use of pushpoints.
r1 = 1.0
N = 3
ca = cos(30.0 * pi / 180.0)
sa = sin(30.0 * pi / 180.0)
# EVEN ROWS
pts = [
    (-3.0, -3.0),
    (-1.267949, -3.0),
    (0.464102, -3.0),
    (2.196152, -3.0),
    (-3.0, 0.0),
    (-1.267949, 0.0),
    (0.464102, 0.0),
    (2.196152, 0.0),
    (-2.133974, -1.5),
    (-0.401923, -1.5),
    (1.330127, -1.5),
    (3.062178, -1.5),
    (-2.133975, 1.5),
    (-0.401924, 1.5),
    (1.330127, 1.5),
    (3.062178, 1.5),
]
# Spike surface
thickness = 0.1
fn = 6
edge_points = [
    [
        r1 * cos(i * 2 * pi / fn + 30 * pi / 180),
        r1 * sin(i * 2 * pi / fn + 30 * pi / 180),
    ]
    for i in range(fn + 1)
]
surface_points = [
    [
        r1 / 4 * cos(i * 2 * pi / fn + 30 * pi / 180),
        r1 / 4 * sin(i * 2 * pi / fn + 30 * pi / 180),
        0.75,
    ]
    for i in range(fn + 1)
] + [[0, 0, 2]]
edge_wire = cq.Workplane("XY").polyline(edge_points)
plate_3 = (
    cq.Workplane("XY")
    .pushPoints(pts)
    .interpPlate(
        edge_wire,
        surface_points,
        thickness,
        combine=False,
        clean=False,
        degree=2,
        nbPtsOnCur=20,
        nbIter=2,
        anisotropy=False,
        tol2d=0.00001,
        tol3d=0.0001,
        tolAng=0.01,
        tolCurv=0.1,
        maxDeg=8,
        maxSegments=9,
    )
)
print("plate_3.val().Volume() = ", plate_3.val().Volume())
plate_3 = plate_3.translate((0, 4 * 11, 0))
show_object(plate_3)

# EXAMPLE 4
# Gyroïd, all edges are splines on different workplanes.
thickness = 0.1
edge_points = [
    [[3.54, 3.54], [1.77, 0.0], [3.54, -3.54]],
    [[-3.54, -3.54], [0.0, -1.77], [3.54, -3.54]],
    [[-3.54, -3.54], [0.0, -1.77], [3.54, -3.54]],
    [[-3.54, -3.54], [-1.77, 0.0], [-3.54, 3.54]],
    [[3.54, 3.54], [0.0, 1.77], [-3.54, 3.54]],
    [[3.54, 3.54], [0.0, 1.77], [-3.54, 3.54]],
]
plane_list = ["XZ", "XY", "YZ", "XZ", "YZ", "XY"]
offset_list = [-3.54, 3.54, 3.54, 3.54, -3.54, -3.54]
edge_wire = (
    cq.Workplane(plane_list[0]).workplane(offset=-offset_list[0]).spline(edge_points[0])
)
for i in range(len(edge_points) - 1):
    edge_wire = edge_wire.add(
        cq.Workplane(plane_list[i + 1])
        .workplane(offset=-offset_list[i + 1])
        .spline(edge_points[i + 1])
    )
surface_points = [[0, 0, 0]]
plate_4 = cq.Workplane("XY").interpPlate(edge_wire, surface_points, thickness)
print("plate_4.val().Volume() = ", plate_4.val().Volume())
plate_4 = plate_4.translate((0, 5 * 12, 0))
show_object(plate_4)

# EXAMPLE 5
# Create surface with smooth (tangential) transitions towards the adjacent faces
thickness = 0.1

o = 20 # outer side length
i = 5 # inner side length
h = 20 # height

surface_1 = cq.Face.makeFromWires(cq.Wire.makePolygon([cq.Vector(-i,-i,h), cq.Vector(-i,i,h),
                                                       cq.Vector(-o,i,0), cq.Vector(-o,-i,0)]))
surface_2 = cq.Face.makeFromWires(cq.Wire.makePolygon([cq.Vector(-5, -5, h), cq.Vector(i,-i,h),
                                                       cq.Vector(i,-o,0),cq.Vector(-i,-o,0)]))
surface_3 = cq.Face.makeFromWires(cq.Wire.makePolygon([cq.Vector(5, -5, h), cq.Vector(i,i,h),
                                                       cq.Vector(o,i,0),cq.Vector(o,-i,0)]))
surface_4 = cq.Face.makeFromWires(cq.Wire.makePolygon([cq.Vector(5, 5, h), cq.Vector(-i,i,h),
                                                       cq.Vector(-i,o,0),cq.Vector(i,o,0)]))

connection_edge_surface_1 = cq.StringSyntaxSelector(">Z").filter(surface_1.Edges())[0]
connection_edge_surface_2 = cq.StringSyntaxSelector(">Z").filter(surface_2.Edges())[0]
connection_edge_surface_3 = cq.StringSyntaxSelector(">Z").filter(surface_3.Edges())[0]
connection_edge_surface_4 = cq.StringSyntaxSelector(">Z").filter(surface_4.Edges())[0]

edges_with_face_constraints = [
    (connection_edge_surface_1, surface_1),
    (connection_edge_surface_2, surface_2),
    (connection_edge_surface_3, surface_3),
    (connection_edge_surface_4, surface_4)
]
'''new_surface_nsided = cq.Face.makeNSidedSurface(
    edges=edges_with_face_constraints, points = [],
    maxSegments=120)'''
new_surface_thickness_0 = cq.Workplane().interpPlate(surf_edges=edges_with_face_constraints, thickness=0.0, combine=False,
                                         clean=False,
                                         degree=3,
                                         nbPtsOnCur=1,
                                         nbIter=1,
                                         anisotropy=False,
                                         tol2d=0.00001,
                                         tol3d=0.0001,
                                         tolAng=0.01,
                                         tolCurv=0.1,
                                         maxDeg=4,
                                         maxSegments=100
                                         )

plate_5 = cq.Workplane().add(surface_1).add(surface_2).add(surface_3).add(surface_4).add(new_surface_thickness_0)
print("plate_5.val().Volume() = ", plate_5.val().Volume())

show_object(plate_5)

# With thickness <> 0 the BRepOffset_MakeOffset call seems to take... long (terminated the example after ~30 mins)
new_surface_thickness_01 = cq.Workplane().interpPlate(surf_edges=edges_with_face_constraints, thickness=0.1, combine=False,
                                                      clean=False,
                                                      degree=3,
                                                      nbPtsOnCur=1,
                                                      nbIter=1,
                                                      anisotropy=False,
                                                      tol2d=0.00001,
                                                      tol3d=0.0001,
                                                      tolAng=0.01,
                                                      tolCurv=0.1,
                                                      maxDeg=4,
                                                      maxSegments=100
                                                      )

plate_6 = cq.Workplane().add(surface_1).add(surface_2).add(surface_3).add(surface_4).add(new_surface_thickness_01)
print("plate_6.val().Volume() = ", plate_5.val().Volume())

show_object(plate_6)