# SPDX-License-Identifier: Apache-2.0

from pxr import Usd, UsdGeom, UsdSkel, Gf, Vt

stage = Usd.Stage.CreateNew("test_mesh.usda")

xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(xform.GetPrim())

# Create Mesh
mesh = UsdGeom.Mesh.Define(stage, "/World/Mesh")

points = Vt.Vec3fArray([
    # Top, Right, Bottom, Left
    (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (-1.0, 0.0, 0.0),
    (0.0, 1.0, 1.0), (1.0, 0.0, 1.0), (0.0, -1.0, 1.0), (-1.0, 0.0, 1.0),
])
face_vert_indices = [
    0, 1, 2, 3,

    0, 4, 5, 1,
    1, 5, 6, 2,
    6, 7, 3, 2,
    7, 4, 0, 3,

    7, 6, 5, 4
]
face_vert_counts = [4] * int(len(face_vert_indices) / 4.0) #[4] * 2
mesh.CreatePointsAttr(points)
mesh.CreateFaceVertexIndicesAttr(face_vert_indices)
mesh.CreateFaceVertexCountsAttr(face_vert_counts)
#mesh.CreateSubdivisionSchemeAttr("none")

stage.Save()