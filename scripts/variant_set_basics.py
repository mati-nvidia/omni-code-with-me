# SPDX-License-Identifier: Apache-2.0

import omni.usd
from pxr import UsdGeom

stage = omni.usd.get_context().get_stage()

xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World/MyPlane")
plane: UsdGeom.Mesh = UsdGeom.Mesh.Define(stage, "/World/MyPlane/Plane")
# plane.CreatePointsAttr().Set([(-50, 0, -50), (50, 0, -50), (-50, 0, 50), (50, 0, 50)])
# plane.CreateFaceVertexCountsAttr().Set([4])
# plane.CreateFaceVertexIndicesAttr().Set([0, 2, 3, 1])
# plane.CreateExtentAttr().Set([(-50, 0, -50), (50, 0, 50)])

xform_prim = xform.GetPrim()
plane_prim = plane.GetPrim()
# prim.GetAttribute("primvars:displayColor").Set([(1.0, 1.0, 0.0)])

#################
# Shading Variant
#################

variants = {
    "default": (1.0, 1.0, 0.0),
    "red": (1.0, 0.0, 0.0),
    "blue": (0.0, 0.0, 1.0),
    "green": (0.0, 1.0, 0.0)
}
shading_varset = xform_prim.GetVariantSets().AddVariantSet("shading")
for variant_name in variants:
    shading_varset.AddVariant(variant_name)

# Author opinions in for each variant. You could do this in the previous for loop too.
for variant_name in variants:
    # You must select a variant to author opinion for it.
    shading_varset.SetVariantSelection(variant_name)
    with shading_varset.GetVariantEditContext():
        # Specs authored within this context are authored just for the variant.
        plane_prim.GetAttribute("primvars:displayColor").Set([variants[variant_name]])

# Remember to set the variant you want selected once you're done authoring.
shading_varset.SetVariantSelection(list(variants.keys())[0])

##################
# Geometry Variant
##################
variants = {
    "default": {
        "points": [(-50, 0, -50), (50, 0, -50), (-50, 0, 50), (50, 0, 50)],
        "indices": [0, 2, 3, 1],
        "counts": [4]
    },
    "sloped": {
        "points": [(-50, 0, -50), (50, 0, -50), (-50, 20, 50), (50, 20, 50)],
        "indices": [0, 2, 3, 1],
        "counts": [4]
    },
    "stacked": {
        "points": [(-50, 0, -50), (50, 0, -50), (-50, 0, 50), (50, 0, 50), (-50, 10, -50), (-50, 10, 50), (50, 10, 50)],
        "indices": [0, 2, 3, 1, 4, 5, 6],
        "counts": [4, 3]
    }
}
shading_varset = xform_prim.GetVariantSets().AddVariantSet("geometry")
for variant_name in variants:
    shading_varset.AddVariant(variant_name)

# Author opinions in for each variant. You could do this in the previous for loop too.
for variant_name in variants:
    # You must select a variant to author opinion for it.
    shading_varset.SetVariantSelection(variant_name)
    with shading_varset.GetVariantEditContext():
        # Specs authored within this context are authored just for the variant.
        plane.CreatePointsAttr().Set(variants[variant_name]["points"])
        plane.CreateFaceVertexCountsAttr().Set(variants[variant_name]["counts"])
        plane.CreateFaceVertexIndicesAttr().Set(variants[variant_name]["indices"])

# Remember to set the variant you want selected once you're done authoring.
shading_varset.SetVariantSelection(list(variants.keys())[0])


##################
# Add Spheres Variant
##################
variants = {
    "default": 1,
    "two": 2,
    "three": 3
}
shading_varset = xform_prim.GetVariantSets().AddVariantSet("spheres")
for variant_name in variants:
    shading_varset.AddVariant(variant_name)

# Author opinions in for each variant. You could do this in the previous for loop too.
for variant_name in variants:
    # You must select a variant to author opinion for it.
    shading_varset.SetVariantSelection(variant_name)
    with shading_varset.GetVariantEditContext():
        # Specs authored within this context are authored just for the variant.
        for x in range(variants[variant_name]):
            UsdGeom.Sphere.Define(stage, xform_prim.GetPath().AppendPath(f"Sphere_{x}"))


# Remember to set the variant you want selected once you're done authoring.
shading_varset.SetVariantSelection(list(variants.keys())[0])
