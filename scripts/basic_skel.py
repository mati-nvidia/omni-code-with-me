# SPDX-License-Identifier: Apache-2.0

from pxr import Usd, UsdGeom, UsdSkel, Gf, Vt

stage = Usd.Stage.CreateNew("test_arm.usda")

xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(xform.GetPrim())
skel_root = UsdSkel.Root.Define(stage, "/World/Arm")

# Create Mesh
mesh = UsdGeom.Mesh.Define(stage, "/World/Arm/Mesh")

points = Vt.Vec3fArray([
    # Hand
    (0.5, -0.5, 4), (-0.5, -0.5, 4), (0.5, 0.5, 4), (-0.5, 0.5, 4),
    # Shoulder
    (-0.5, -0.5, 0), (0.5, -0.5, 0), (-0.5, 0.5, 0), (0.5, 0.5, 0),
    # Elbow
    (-0.5, 0.5, 2), (0.5, 0.5, 2), (0.5, -0.5, 2), (-0.5, -0.5, 2)
])
face_vert_indices = [
    2, 3, 1, 0,
    6, 7, 5, 4,
    8, 9, 7, 6,
    3, 2, 9, 8,
    10, 11, 4, 5,
    0, 1, 11, 10,
    7, 9, 10, 5,
    9, 2, 0, 10,
    3, 8, 11, 1,
    8, 6, 4, 11
]
face_vert_counts = [4] * 10
mesh.CreatePointsAttr(points)
mesh.CreateFaceVertexIndicesAttr(face_vert_indices)
mesh.CreateFaceVertexCountsAttr(face_vert_counts)


skeleton = UsdSkel.Skeleton.Define(stage, "/World/Arm/Rig")
joints = ["Shoulder", "Shoulder/Elbow", "Shoulder/Elbow/Hand"]
skeleton.CreateJointsAttr(joints)
# World space xforms. Who cares about my parents?
bind_xforms = Vt.Matrix4dArray([
    Gf.Matrix4d((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)),
    Gf.Matrix4d((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,2,1)),
    Gf.Matrix4d((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,4,1))
])
skeleton.CreateBindTransformsAttr(bind_xforms)
# Local space xforms. What's my offset from my parent joint?
rest_xforms = Vt.Matrix4dArray([
    Gf.Matrix4d((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)),
    Gf.Matrix4d((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,2,1)),
    Gf.Matrix4d((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,2,1))
])
skeleton.CreateRestTransformsAttr(rest_xforms)

# TODO: Do I need to apply BindingAPI to skel root?
binding_api1 = UsdSkel.BindingAPI.Apply(skel_root.GetPrim())
binding_api2 = UsdSkel.BindingAPI.Apply(mesh.GetPrim())
binding_api2.CreateSkeletonRel().AddTarget(skel_root.GetPath())
# This is index in joints property for each vertex.
joint_indices = binding_api2.CreateJointIndicesPrimvar(False, 1)
joint_indices.Set([2,2,2,2, 0,0,0,0, 1,1,1,1])
joint_weights = binding_api2.CreateJointWeightsPrimvar(False, 1)
joint_weights.Set([1,1,1,1, 1,1,1,1, 1,1,1,1])


stage.Save()