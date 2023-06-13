# SPDX-License-Identifier: Apache-2.0

from pxr import Sdf, UsdShade, Gf
import omni.usd

stage = omni.usd.get_context().get_stage()

mtl_path = Sdf.Path("/World/Looks/OmniSurface")
mtl = UsdShade.Material.Define(stage, mtl_path)
shader = UsdShade.Shader.Define(stage, mtl_path.AppendPath("Shader"))
shader.CreateImplementationSourceAttr(UsdShade.Tokens.sourceAsset)
# MDL shaders should use "mdl" sourceType
shader.SetSourceAsset("OmniSurface.mdl", "mdl")
shader.SetSourceAssetSubIdentifier("OmniSurface", "mdl")
shader.CreateInput("diffuse_reflection_color", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1.0, 0.0, 0.0))
# MDL materials should use "mdl" renderContext
mtl.CreateSurfaceOutput("mdl").ConnectToSource(shader.ConnectableAPI(), "out")
mtl.CreateDisplacementOutput("mdl").ConnectToSource(shader.ConnectableAPI(), "out")
mtl.CreateVolumeOutput("mdl").ConnectToSource(shader.ConnectableAPI(), "out")

prvw_shader = UsdShade.Shader.Define(stage, mtl_path.AppendPath("prvw_shader"))
prvw_shader.CreateIdAttr("UsdPreviewSurface")
prvw_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.0, 0.0, 1.0))

# Render Context specific to Storm
# mtl.CreateSurfaceOutput("glslfx").ConnectToSource(prvw_shader.ConnectableAPI(), "out")
# mtl.CreateDisplacementOutput("glslfx").ConnectToSource(prvw_shader.ConnectableAPI(), "out")
# mtl.CreateVolumeOutput("glslfx").ConnectToSource(prvw_shader.ConnectableAPI(), "out")

# Universal outputs
mtl.CreateSurfaceOutput().ConnectToSource(prvw_shader.ConnectableAPI(), "out")
mtl.CreateDisplacementOutput().ConnectToSource(prvw_shader.ConnectableAPI(), "out")
mtl.CreateVolumeOutput().ConnectToSource(prvw_shader.ConnectableAPI(), "out")