# SPDX-License-Identifier: Apache-2.0

import omni.usd
from pxr import UsdShade, UsdGeom, Sdf

stage = omni.usd.get_context().get_stage()
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
billboard = UsdGeom.Mesh.Define(stage, "/World/billboard")
billboard.CreatePointsAttr([(-100, -100, 0), (100, -100, 0), (100, 100, 0), (-100, 100,0)])
billboard.CreateFaceVertexCountsAttr([4])
billboard.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
billboard.CreateExtentAttr([(-100, -100, 0), (100, 100, 0)])
tex_coords = UsdGeom.PrimvarsAPI(billboard).CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.varying)
tex_coords.Set([(0, 0), (1, 0), (1, 1), (0, 1)])

material = UsdShade.Material.Define(stage, "/World/PreviewMtl")
pbr_shader = UsdShade.Shader.Define(stage, "/World/PreviewMtl/PBRShader")
pbr_shader.CreateIdAttr("UsdPreviewSurface")
pbr_shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
pbr_shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
pbr_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.0, 0.0))
material.CreateSurfaceOutput().ConnectToSource(pbr_shader.ConnectableAPI(), "surface")

st_reader = UsdShade.Shader.Define(stage, '/World/PreviewMtl/st_reader')
st_reader.CreateIdAttr('UsdPrimvarReader_float2')


transform2d = UsdShade.Shader.Define(stage, '/World/PreviewMtl/transform2d')
transform2d.CreateIdAttr("UsdTransform2d")
transform2d.CreateInput("in", Sdf.ValueTypeNames.Float2).ConnectToSource(st_reader.ConnectableAPI(), 'result')
transform2d.CreateInput("rotation", Sdf.ValueTypeNames.Float)
transform2d.CreateInput("scale", Sdf.ValueTypeNames.Float2)
transform2d.CreateInput("translation", Sdf.ValueTypeNames.Float2)

diffuseTextureSampler = UsdShade.Shader.Define(stage,'/World/PreviewMtl/diffuseTexture')
diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("C:/Users/mcodesal/Downloads/Ground062S_1K-PNG/Ground062S_1K_Color.png")
diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(transform2d.ConnectableAPI(), 'result')
diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
pbr_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')


st_input = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
st_input.Set('st')
st_reader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(st_input)

billboard.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
UsdShade.MaterialBindingAPI(billboard).Bind(material)