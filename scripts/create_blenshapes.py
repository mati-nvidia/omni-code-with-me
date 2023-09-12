# SPDX-License-Identifier: Apache-2.0

import math

from pxr import Usd, UsdGeom, UsdSkel, Gf, Vt

stage = Usd.Stage.CreateNew("blendshapes.usda")

xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(xform.GetPrim())
stage.SetStartTimeCode(1.0)
stage.SetEndTimeCode(17.0)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

eq_tri_height = math.sqrt(3) * 1/2

skel_root = UsdSkel.Root.Define(stage, "/World/MorphingTri")
extents_anim = {
    1: [(-0.5, 0, 0), (0.5, eq_tri_height, 0)],
    5: [(-0.5, 0, 0), (0.5, 2* eq_tri_height, 0)],
    9: [(-0.5, 0, 0), (0.5, eq_tri_height, 0)],
    13: [(-0.5, 0, 0), (0.5, eq_tri_height + (1-eq_tri_height), 0)],
    17: [(-0.5, 0, 0), (0.5, 2*eq_tri_height + (1-eq_tri_height), 0)],
}
extents_attr = skel_root.CreateExtentAttr()
for timesample, value in extents_anim.items():
    extents_attr.Set(value, timesample)


# Skeleton is required even if it's empty
skel = UsdSkel.Skeleton.Define(stage, skel_root.GetPath().AppendChild("Skel"))

mesh = UsdGeom.Mesh.Define(stage, "/World/MorphingTri/Mesh")
mesh_binding = UsdSkel.BindingAPI.Apply(mesh.GetPrim())
# This binding could go on SkelRoot too. It will inherit down to the mesh.
mesh_binding.CreateSkeletonRel().SetTargets([skel.GetPath()])


points = Vt.Vec3fArray([
    (0.5, 0, 0), (0, eq_tri_height, 0), (-0.5, 0, 0)
])
face_vert_indices = [
    0, 1, 2
]
face_vert_counts = [3]
mesh.CreatePointsAttr(points)
mesh.CreateFaceVertexIndicesAttr(face_vert_indices)
mesh.CreateFaceVertexCountsAttr(face_vert_counts)

iso = UsdSkel.BlendShape.Define(stage, mesh.GetPath().AppendChild("iso"))
iso.CreateOffsetsAttr().Set([(0, eq_tri_height, 0)])
iso.CreatePointIndicesAttr().Set([1])

right = UsdSkel.BlendShape.Define(stage, mesh.GetPath().AppendChild("right"))
right.CreateOffsetsAttr().Set([(-0.5, 1-eq_tri_height, 0)])
right.CreatePointIndicesAttr().Set([1])

mesh_binding = UsdSkel.BindingAPI.Apply(mesh.GetPrim())
mesh_binding.CreateBlendShapesAttr().Set(["iso", "right"])
mesh_binding.CreateBlendShapeTargetsRel().SetTargets([iso.GetPath(), right.GetPath()])

# anim = UsdSkel.Animation.Define(stage, skel_root.GetPath().AppendChild("Anim"))
# anim.CreateBlendShapesAttr().Set(["right", "iso"])
# anim.CreateBlendShapeWeightsAttr().Set([1.0, 2.0])

anim = UsdSkel.Animation.Define(stage, skel_root.GetPath().AppendChild("Anim"))
anim.CreateBlendShapesAttr().Set(["right", "iso"])

# Frame 1
anim.CreateBlendShapeWeightsAttr().Set([0.0, 0.0], 1.0)

# Frame 5
anim.CreateBlendShapeWeightsAttr().Set([0.0, 1.0], 5.0)

# Frame 9
anim.CreateBlendShapeWeightsAttr().Set([0.0, 0.0], 9.0)

# Frame 13
anim.CreateBlendShapeWeightsAttr().Set([1.0, 0.0], 13.0)

# Frame 17
anim.CreateBlendShapeWeightsAttr().Set([1.0, 1.0], 17.0)

root_binding = UsdSkel.BindingAPI.Apply(skel_root.GetPrim())
root_binding.CreateAnimationSourceRel().AddTarget(anim.GetPath())

stage.Save()