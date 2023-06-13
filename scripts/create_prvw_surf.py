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
pbr_shader.CreateInput("occlusion", Sdf.ValueTypeNames.Float)
pbr_shader.CreateInput("displacement", Sdf.ValueTypeNames.Float)
pbr_shader.CreateInput("normal", Sdf.ValueTypeNames.Normal3f)
pbr_shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
pbr_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.0, 0.0))
material.CreateSurfaceOutput().ConnectToSource(pbr_shader.ConnectableAPI(), "surface")
material.CreateDisplacementOutput().ConnectToSource(pbr_shader.ConnectableAPI(), "displacement")

st_reader = UsdShade.Shader.Define(stage, '/World/PreviewMtl/st_reader')
st_reader.CreateIdAttr('UsdPrimvarReader_float2')


transform2d = UsdShade.Shader.Define(stage, '/World/PreviewMtl/transform2d')
transform2d.CreateIdAttr("UsdTransform2d")
transform2d.CreateInput("in", Sdf.ValueTypeNames.Float2).ConnectToSource(st_reader.ConnectableAPI(), 'result')
transform2d.CreateInput("rotation", Sdf.ValueTypeNames.Float)
transform2d.CreateInput("scale", Sdf.ValueTypeNames.Float2).Set((1.0, 1.0))
transform2d.CreateInput("translation", Sdf.ValueTypeNames.Float2)

# Diffuse 
diffuseTextureSampler = UsdShade.Shader.Define(stage,'/World/PreviewMtl/diffuseTexture')
diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("C:/Users/mcodesal/Downloads/Ground062S_1K-PNG/Ground062S_1K_Color.png")
diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(transform2d.ConnectableAPI(), 'result')
diffuseTextureSampler.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
diffuseTextureSampler.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
pbr_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')

# Roughness
roughTextureSampler = UsdShade.Shader.Define(stage,'/World/PreviewMtl/roughnessTexture')
roughTextureSampler.CreateIdAttr('UsdUVTexture')
roughTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("C:/Users/mcodesal/Downloads/Ground062S_1K-PNG/Ground062S_1K_Roughness.png")
roughTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(transform2d.ConnectableAPI(), 'result')
roughTextureSampler.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
roughTextureSampler.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
roughTextureSampler.CreateOutput('r', Sdf.ValueTypeNames.Float)
pbr_shader.CreateInput("roughness", Sdf.ValueTypeNames.Color3f).ConnectToSource(roughTextureSampler.ConnectableAPI(), 'r')

# AO
ao = UsdShade.Shader.Define(stage,'/World/PreviewMtl/aoTexture')
ao.CreateIdAttr('UsdUVTexture')
ao.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("C:/Users/mcodesal/Downloads/Ground062S_1K-PNG/Ground062S_1K_AmbientOcclusion.png")
ao.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(transform2d.ConnectableAPI(), 'result')
ao.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
ao.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
ao.CreateOutput('r', Sdf.ValueTypeNames.Float)
pbr_shader.CreateInput("occlusion", Sdf.ValueTypeNames.Color3f).ConnectToSource(ao.ConnectableAPI(), 'r')


# Displacement
displace = UsdShade.Shader.Define(stage,'/World/PreviewMtl/displaceTexture')
displace.CreateIdAttr('UsdUVTexture')
displace.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("C:/Users/mcodesal/Downloads/Ground062S_1K-PNG/Ground062S_1K_Displacement.png")
displace.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(transform2d.ConnectableAPI(), 'result')
displace.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
displace.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
displace.CreateOutput('r', Sdf.ValueTypeNames.Float)
pbr_shader.CreateInput("displacement", Sdf.ValueTypeNames.Color3f).ConnectToSource(displace.ConnectableAPI(), 'r')

# Normal
normal = UsdShade.Shader.Define(stage,'/World/PreviewMtl/normalTexture')
normal.CreateIdAttr('UsdUVTexture')
normal.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("C:/Users/mcodesal/Downloads/Ground062S_1K-PNG/Ground062S_1K_NormalGL.png")
normal.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(transform2d.ConnectableAPI(), 'result')
normal.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
normal.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
normal.CreateInput("bias", Sdf.ValueTypeNames.Float4).Set((-1, -1, -1, 0))
normal.CreateInput("scale", Sdf.ValueTypeNames.Float4).Set((2.0, 2.0, 2.0, 1.0))
normal.CreateInput("sourceColorSpace", Sdf.ValueTypeNames.Token).Set("raw")
normal.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
pbr_shader.CreateInput("normal", Sdf.ValueTypeNames.Color3f).ConnectToSource(normal.ConnectableAPI(), 'rgb')


st_input = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
st_input.Set('st')
st_reader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(st_input)

billboard.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
UsdShade.MaterialBindingAPI(billboard).Bind(material)