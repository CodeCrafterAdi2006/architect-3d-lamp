"""
07_materials.py
Phase 4.1: Final Material & Shader Pass.
Creates polished PBR materials (Gunmetal Dark Metal, Polished Chrome Pins & Springs,
Cream Reflector, Glowing Tungsten Bulb, and Matte Rubber Cable).
Also adds the base trailing power cord and renders the final textured preview.
Saves to desk_lamp_wip.blend.
"""

import bpy
import os
import math
import mathutils

blend_path = r"c:\AI_Studio\Blender\desk_lamp_wip.blend"
if not os.path.exists(blend_path):
    raise FileNotFoundError(f"Missing {blend_path}. Run previous steps first.")

bpy.ops.wm.open_mainfile(filepath=blend_path)

# ------------------------------------------------------------------------------
# 1. CREATE MASTER PBR MATERIALS
# ------------------------------------------------------------------------------
def create_or_get_mat(name, color, metallic=0.0, roughness=0.5, emission=None, emission_strength=1.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if emission:
            # Handle emission input
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = emission
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

mat_dark_metal = create_or_get_mat(
    "Mat_DarkMetal",
    color=(0.045, 0.045, 0.05, 1.0),
    metallic=0.88,
    roughness=0.35
)

mat_chrome = create_or_get_mat(
    "Mat_Chrome_Accent",
    color=(0.90, 0.90, 0.92, 1.0),
    metallic=0.98,
    roughness=0.12
)

mat_cream = create_or_get_mat(
    "Mat_ShadeInterior",
    color=(0.95, 0.92, 0.86, 1.0),
    metallic=0.0,
    roughness=0.45,
    emission=(0.0, 0.0, 0.0, 1.0),
    emission_strength=0.0
)

mat_bulb = create_or_get_mat(
    "Mat_Bulb_Glow",
    color=(1.0, 0.98, 0.92, 1.0),
    metallic=0.0,
    roughness=0.1,
    emission=(1.0, 0.88, 0.62, 1.0),
    emission_strength=2.0
)

mat_rubber = create_or_get_mat(
    "Mat_Cable_Rubber",
    color=(0.02, 0.02, 0.022, 1.0),
    metallic=0.0,
    roughness=0.75
)

# ------------------------------------------------------------------------------
# 2. ASSIGN MATERIALS ACROSS ALL OBJECTS
# ------------------------------------------------------------------------------
for obj in bpy.data.objects:
    if obj.type == 'MESH' or obj.type == 'CURVE':
        name = obj.name
        
        if "Bulb" in name and "Socket" not in name:
            obj.data.materials.clear()
            obj.data.materials.append(mat_bulb)
            
        elif "Shade_Bell" in name:
            obj.data.materials.clear()
            obj.data.materials.append(mat_dark_metal) # Slot 0: Exterior
            obj.data.materials.append(mat_cream)      # Slot 1: Interior
            # Ensure solidify modifier uses slot 1 for inner surface
            for mod in obj.modifiers:
                if mod.type == 'SOLIDIFY':
                    mod.material_offset = 1
                    mod.material_offset_rim = 0
                    
        elif any(k in name for k in ["Bolt", "Cap", "Spring", "Socket"]):
            obj.data.materials.clear()
            obj.data.materials.append(mat_chrome)
            
        elif "PowerCord" in name or "Cable" in name:
            obj.data.materials.clear()
            obj.data.materials.append(mat_rubber)
            
        elif any(k in name for k in ["Base", "Stem", "Arm", "Elbow", "Neck", "TopCap", "Rim"]):
            obj.data.materials.clear()
            obj.data.materials.append(mat_dark_metal)

# ------------------------------------------------------------------------------
# 3. CLEAN BASE FOR 3D WEB ASSET (No awkward protruding cords)
# ------------------------------------------------------------------------------
for obj in list(bpy.data.objects):
    if "Base_PowerCord" in obj.name:
        bpy.data.objects.remove(obj, do_unlink=True)

# ------------------------------------------------------------------------------
# 4. STUDIO LIGHTING WITH WARM DESK BOUNCE
# ------------------------------------------------------------------------------
# Warm key light
key_light = bpy.data.objects.get("Key_Light")
if key_light:
    key_light.location = (3.5, -2.5, 4.0)
    key_light.data.energy = 180.0
    key_light.data.color = (1.0, 0.95, 0.88)

# Subtle fill
fill_light = bpy.data.objects.get("Fill_Light")
if fill_light:
    fill_light.location = (-4.0, -2.0, 2.5)
    fill_light.data.energy = 50.0
    fill_light.data.color = (0.75, 0.82, 0.95)

# Desk material polish (Warm rich walnut wooden tone)
desk_mat = bpy.data.materials.get("Mat_Desk_Ground")
if desk_mat and desk_mat.use_nodes:
    d_bsdf = desk_mat.node_tree.nodes.get("Principled BSDF")
    if d_bsdf:
        d_bsdf.inputs["Base Color"].default_value = (0.10, 0.06, 0.035, 1.0)
        d_bsdf.inputs["Roughness"].default_value = 0.55

# Camera position
cam = bpy.data.objects.get("Scene_Camera")
if cam:
    cam.location = (6.0, -6.6, 3.2)
    target = mathutils.Vector((0.0, 0.0, 1.35))
    direction = target - cam.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()

# ------------------------------------------------------------------------------
# 5. SAVE & RENDER
# ------------------------------------------------------------------------------
render_output = r"c:\AI_Studio\Blender\renders\07_materials.png"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.context.scene.render.filepath = render_output
bpy.ops.render.render(write_still=True)

print("\n" + "="*60)
print("SUCCESS: 07_materials.py (Phase 4.1 Master Materials Pass)")
print("="*60)
print("Mat_DarkMetal:       Gunmetal Matte Black applied across body")
print("Mat_Chrome_Accent:   Polished Chrome applied to all bolts & springs")
print("Mat_ShadeInterior:   Cream Reflector with warm glow bounce")
print("Mat_Bulb_Glow:       Warm 2700K Tungsten Emissive Bulb")
print("Mat_Cable_Rubber:    Matte Black Flexible Power Cable")
print("Base Power Cord:     Trailing cable added across desk")
print(f"Saved:               {blend_path}")
print(f"Rendered:            {render_output}")
print("="*60 + "\n")
