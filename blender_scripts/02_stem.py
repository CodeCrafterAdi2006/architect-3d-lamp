"""
02_stem.py
Phase 3.2: Loads desk_lamp_wip.blend and adds the vertical stem post
with swivel base hinge bracket.
Saves updated scene and renders preview for verification.
"""

import bpy
import sys
import os
import math
import importlib.util
import mathutils

# ------------------------------------------------------------------------------
# 1. LOAD WORK-IN-PROGRESS SCENE
# ------------------------------------------------------------------------------
blend_path = r"c:\AI_Studio\Blender\desk_lamp_wip.blend"
if not os.path.exists(blend_path):
    raise FileNotFoundError(f"Missing {blend_path}. Please run 01_base.py first.")

bpy.ops.wm.open_mainfile(filepath=blend_path)

base_obj = bpy.data.objects.get("Lamp_Base")
if not base_obj:
    raise ValueError("Lamp_Base not found in scene!")

# Clean up any previous stem objects if re-running
for obj in list(bpy.data.objects):
    if obj.name.startswith("Lamp_Stem"):
        bpy.data.objects.remove(obj, do_unlink=True)

base_top_z = base_obj.location.z + (base_obj.dimensions.z / 2.0) # approx 0.22

# ------------------------------------------------------------------------------
# 2. CREATE STEM CYLINDER & SWIVEL BRACKET
# ------------------------------------------------------------------------------
stem_radius = 0.14
stem_height = 0.32
stem_center_z = base_top_z + (stem_height / 2.0)

# Create the vertical post
bpy.ops.mesh.primitive_cylinder_add(
    vertices=24,
    radius=stem_radius,
    depth=stem_height,
    location=(0.0, 0.0, stem_center_z)
)
stem_obj = bpy.context.active_object
stem_obj.name = "Lamp_Stem"

# Add bevel modifier for crisp machined edges
bevel_mod = stem_obj.modifiers.new(name="Bevel", type='BEVEL')
bevel_mod.width = 0.015
bevel_mod.segments = 2
bevel_mod.limit_method = 'ANGLE'
bevel_mod.angle_limit = math.radians(35.0)

for poly in stem_obj.data.polygons:
    poly.use_smooth = True

# Assign dark metal material
dark_mat = bpy.data.materials.get("Mat_DarkMetal_Preview")
if dark_mat:
    stem_obj.data.materials.append(dark_mat)

# Create the lower hinge collar/bracket on top of stem
bracket_z = base_top_z + stem_height + 0.08
bpy.ops.mesh.primitive_cube_add(
    size=1.0,
    location=(0.0, 0.0, bracket_z)
)
bracket_obj = bpy.context.active_object
bracket_obj.name = "Lamp_Stem_Bracket"
bracket_obj.scale = (0.16, 0.12, 0.16)

# Assign dark metal material to bracket
if dark_mat:
    bracket_obj.data.materials.append(dark_mat)

# Join bracket into Lamp_Stem so it's a single clean object
bpy.ops.object.select_all(action='DESELECT')
bracket_obj.select_set(True)
stem_obj.select_set(True)
bpy.context.view_layer.objects.active = stem_obj
bpy.ops.object.join()

# ------------------------------------------------------------------------------
# 3. SAVE WORK-IN-PROGRESS FILE & RENDER
# ------------------------------------------------------------------------------
render_output = r"c:\AI_Studio\Blender\renders\02_stem.png"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.context.scene.render.filepath = render_output
bpy.ops.render.render(write_still=True)

# ------------------------------------------------------------------------------
# 4. AUTOMATED GEOMETRY AUDIT
# ------------------------------------------------------------------------------
stem_dim_x = stem_obj.dimensions.x
stem_dim_y = stem_obj.dimensions.y
stem_dim_z = stem_obj.dimensions.z
bottom_contact_z = stem_obj.location.z - (stem_height / 2.0)

print("\n" + "="*60)
print("AUTOMATED AUDIT: 02_stem.py")
print("="*60)
print(f"Object Name:       {stem_obj.name}")
print(f"Stem Dimensions:   X={stem_dim_x:.2f}, Y={stem_dim_y:.2f}, Z={stem_dim_z:.2f}")
print(f"Center Alignment:  X={stem_obj.location.x:.3f}, Y={stem_obj.location.y:.3f} (Target: 0,0)")
print(f"Base Contact Z:    Z={bottom_contact_z:.3f} vs Base Top Z={base_top_z:.3f}")
print(f"Saved .blend:      {blend_path}")
print(f"Render output:     {render_output}")
print("="*60 + "\n")
