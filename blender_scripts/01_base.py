"""
01_base.py
Phase 3.1: Creates the weighted circular base of the desk lamp.
Sets up the scene camera, lighting, and renders a preview for verification.
Saves to desk_lamp_wip.blend.
"""

import bpy
import sys
import os
import math

# Ensure blender_scripts folder is in sys.path to import proportions
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

import importlib.util
import mathutils

# Dynamically import 00_proportions
prop_path = os.path.join(scripts_dir, "00_proportions.py")
spec = importlib.util.spec_from_file_location("proportions", prop_path)
prop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prop)

# Setup clean file
bpy.ops.wm.read_factory_settings(use_empty=True)

# ------------------------------------------------------------------------------
# 1. CREATE BASE GEOMETRY
# ------------------------------------------------------------------------------
# Dimensions: Radius = 1.0 (Diameter = 2.0), Height = 0.22
base_radius = 1.0
base_height = 0.22

# Add main cylinder for the base
bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,
    radius=base_radius,
    depth=base_height,
    location=(0.0, 0.0, base_height / 2.0)
)

base_obj = bpy.context.active_object
base_obj.name = "Lamp_Base"

# Add a subtle bevel modifier for the smooth rounded top rim seen in reference
bevel_mod = base_obj.modifiers.new(name="Bevel", type='BEVEL')
bevel_mod.width = 0.03
bevel_mod.segments = 2
bevel_mod.limit_method = 'ANGLE'
bevel_mod.angle_limit = math.radians(30.0)

# Shade smooth with auto-smooth angle for crisp industrial cylinder look
for poly in base_obj.data.polygons:
    poly.use_smooth = True

# Add a default preview dark metal material
mat = bpy.data.materials.new(name="Mat_DarkMetal_Preview")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    # Set dark charcoal / gunmetal base color
    bsdf.inputs["Base Color"].default_value = (0.04, 0.04, 0.045, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.4
    bsdf.inputs["Metallic"].default_value = 0.8
base_obj.data.materials.append(mat)

# ------------------------------------------------------------------------------
# 2. SETUP CAMERA & STUDIO LIGHTING FOR PREVIEW RENDERS
# ------------------------------------------------------------------------------
# Ground Desk Plane for shadow/context
bpy.ops.mesh.primitive_plane_add(size=10.0, location=(0.0, 0.0, 0.0))
desk = bpy.context.active_object
desk.name = "Desk_Ground"
desk_mat = bpy.data.materials.new(name="Mat_Desk_Ground")
desk_mat.use_nodes = True
d_bsdf = desk_mat.node_tree.nodes.get("Principled BSDF")
if d_bsdf:
    d_bsdf.inputs["Base Color"].default_value = (0.08, 0.05, 0.03, 1.0) # warm wood tone
    d_bsdf.inputs["Roughness"].default_value = 0.6
desk.data.materials.append(desk_mat)

# Camera positioned at a 3/4 perspective matching reference photo
bpy.ops.object.camera_add(location=(3.2, -3.8, 2.2), rotation=(math.radians(65), 0, math.radians(40)))
cam = bpy.context.active_object
cam.name = "Scene_Camera"
bpy.context.scene.camera = cam

# Key Light
bpy.ops.object.light_add(type='AREA', location=(2.5, -2.0, 3.5), rotation=(math.radians(45), 0, math.radians(35)))
key_light = bpy.context.active_object
key_light.name = "Key_Light"
key_light.data.energy = 150.0
key_light.data.size = 2.0
key_light.data.color = (1.0, 0.95, 0.85)

# Soft Fill Light
bpy.ops.object.light_add(type='POINT', location=(-3.0, -1.0, 2.0))
fill_light = bpy.context.active_object
fill_light.name = "Fill_Light"
fill_light.data.energy = 40.0
fill_light.data.color = (0.8, 0.85, 1.0)

# Configure Render Settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 960
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.image_settings.file_format = 'PNG'

# ------------------------------------------------------------------------------
# 3. SAVE WORK-IN-PROGRESS FILE & RENDER
# ------------------------------------------------------------------------------
blend_output = r"c:\AI_Studio\Blender\desk_lamp_wip.blend"
render_output = r"c:\AI_Studio\Blender\renders\01_base.png"

bpy.ops.wm.save_as_mainfile(filepath=blend_output)

bpy.context.scene.render.filepath = render_output
bpy.ops.render.render(write_still=True)

# ------------------------------------------------------------------------------
# 4. AUTOMATED GEOMETRY AUDIT
# ------------------------------------------------------------------------------
bb = [base_obj.matrix_world @ mathutils.Vector(corner) for corner in base_obj.bound_box] if 'mathutils' in globals() else None
# Calculate bounds
dim_x = base_obj.dimensions.x
dim_y = base_obj.dimensions.y
dim_z = base_obj.dimensions.z
bottom_z = base_obj.location.z - (dim_z / 2.0)

print("\n" + "="*60)
print("AUTOMATED AUDIT: 01_base.py")
print("="*60)
print(f"Object Name:       {base_obj.name}")
print(f"Dimensions:        X={dim_x:.2f}, Y={dim_y:.2f}, Z={dim_z:.2f}")
print(f"Diameter-to-Height: {dim_x / dim_z:.2f}:1 (Target: ~9:1 flat disc)")
print(f"Bottom Z Contact:  Z={bottom_z:.3f} (Target: Z=0.0 on ground)")
print(f"Polygons / Faces:  {len(base_obj.data.polygons)}")
print(f"Saved .blend:      {blend_output}")
print(f"Render output:     {render_output}")
print("="*60 + "\n")
