"""
03_lower_arm.py (Seamless Mechanical Alignment)
Builds the stem, dual-pin bracket, lower arm twin struts, and a single CONTINUOUS
lower tension rod running seamlessly from the bottom bracket pin all the way to the top elbow pin.
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
# 1. SETUP MATERIALS
# ------------------------------------------------------------------------------
dark_mat = bpy.data.materials.get("Mat_DarkMetal_Preview")
if not dark_mat:
    dark_mat = bpy.data.materials.new(name="Mat_DarkMetal_Preview")
    dark_mat.use_nodes = True
    bsdf = dark_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.04, 0.04, 0.045, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.38
        bsdf.inputs["Metallic"].default_value = 0.85

chrome_mat = bpy.data.materials.get("Mat_Chrome_Accent")
if not chrome_mat:
    chrome_mat = bpy.data.materials.new(name="Mat_Chrome_Accent")
    chrome_mat.use_nodes = True
    c_bsdf = chrome_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs["Base Color"].default_value = (0.85, 0.85, 0.88, 1.0)
        c_bsdf.inputs["Roughness"].default_value = 0.15
        c_bsdf.inputs["Metallic"].default_value = 0.95

# ------------------------------------------------------------------------------
# 2. CLEANUP EXISTING OBJECTS
# ------------------------------------------------------------------------------
for obj in list(bpy.data.objects):
    if obj.name.startswith("Lamp_Stem") or obj.name.startswith("Lamp_LowerArm") or obj.name.startswith("Lamp_Joint") or obj.name.startswith("Lamp_Tension") or obj.name.startswith("Lamp_LowerTension"):
        bpy.data.objects.remove(obj, do_unlink=True)

base_top_z = 0.22

# ------------------------------------------------------------------------------
# 3. REFINED STEM & STEPPED SWIVEL COLLAR
# ------------------------------------------------------------------------------
stem_radius = 0.12
stem_height = 0.16
stem_center_z = base_top_z + (stem_height / 2.0)

bpy.ops.mesh.primitive_cylinder_add(
    vertices=24,
    radius=stem_radius,
    depth=stem_height,
    location=(0.0, 0.0, stem_center_z)
)
stem_post = bpy.context.active_object
stem_post.name = "Lamp_Stem_Post"
stem_post.data.materials.append(dark_mat)

collar_radius = 0.145
collar_height = 0.05
collar_z = base_top_z + stem_height + (collar_height / 2.0)
bpy.ops.mesh.primitive_cylinder_add(
    vertices=24,
    radius=collar_radius,
    depth=collar_height,
    location=(0.0, 0.0, collar_z)
)
stem_collar = bpy.context.active_object
stem_collar.name = "Lamp_Stem_Collar"
stem_collar.data.materials.append(dark_mat)

# ------------------------------------------------------------------------------
# 4. SCULPTED DUAL-PIN BRACKET
# ------------------------------------------------------------------------------
bracket_thickness = 0.028
bracket_x_offset = 0.075
pin_bottom_y = 0.0
pin_bottom_z = collar_z + 0.06 # Z = 0.385
pin_top_y = -0.06
pin_top_z = pin_bottom_z + 0.16 # Z = 0.545

bracket_parts = []
for side in (-1, 1):
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(side * bracket_x_offset, pin_top_y / 2.0, (pin_bottom_z + pin_top_z) / 2.0),
        rotation=(math.radians(20), 0, 0)
    )
    b_plate = bpy.context.active_object
    b_plate.name = f"Lamp_BracketPlate_{side}"
    b_plate.scale = (bracket_thickness, 0.14, 0.22)
    b_plate.data.materials.append(dark_mat)
    bracket_parts.append(b_plate)

bpy.ops.object.select_all(action='DESELECT')
stem_post.select_set(True)
stem_collar.select_set(True)
for bp in bracket_parts:
    bp.select_set(True)
bpy.context.view_layer.objects.active = stem_post
bpy.ops.object.join()
stem_post.name = "Lamp_Stem"

# 2 Silver Pivot Bolt Pins on Stem Bracket
for p_idx, (py, pz) in enumerate([(pin_bottom_y, pin_bottom_z), (pin_top_y, pin_top_z)]):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.024,
        depth=bracket_x_offset * 2.6,
        location=(0.0, py, pz),
        rotation=(0, math.radians(90), 0)
    )
    bolt = bpy.context.active_object
    bolt.name = f"Lamp_JointBolt_Bottom_{p_idx}"
    bolt.data.materials.append(chrome_mat)
    
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.036,
            depth=0.015,
            location=(side * (bracket_x_offset * 1.35), py, pz),
            rotation=(0, math.radians(90), 0)
        )
        cap = bpy.context.active_object
        cap.name = f"Lamp_BoltCap_{p_idx}_{side}"
        cap.data.materials.append(chrome_mat)

# ------------------------------------------------------------------------------
# 5. TWIN STRUT LOWER ARM WITH ROUNDED EYELETS
# ------------------------------------------------------------------------------
arm_length = 1.35
arm_angle_deg = 68.0
rot_x_deg = 90.0 - arm_angle_deg # 22 deg
rot_x_rad = math.radians(rot_x_deg)

strut_width = 0.032
strut_depth = 0.045
strut_spacing_x = 0.052

p0_y = pin_top_y
p0_z = pin_top_z

vec_y = -arm_length * math.sin(rot_x_rad)
vec_z = arm_length * math.cos(rot_x_rad)
elbow_y = p0_y + vec_y # -0.5657
elbow_z = p0_z + vec_z # 1.7967

arm_mid_y = p0_y + (vec_y / 2.0)
arm_mid_z = p0_z + (vec_z / 2.0)

arm_parts = []
for side in (-1, 1):
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(side * strut_spacing_x, arm_mid_y, arm_mid_z),
        rotation=(rot_x_rad, 0, 0)
    )
    bar = bpy.context.active_object
    bar.name = f"Lamp_LowerArm_Bar_{side}"
    bar.scale = (strut_width, strut_depth, arm_length)
    bar.data.materials.append(dark_mat)
    arm_parts.append(bar)
    
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=strut_depth * 0.75,
        depth=strut_width,
        location=(side * strut_spacing_x, p0_y, p0_z),
        rotation=(0, math.radians(90), 0)
    )
    eye_bot = bpy.context.active_object
    eye_bot.data.materials.append(dark_mat)
    arm_parts.append(eye_bot)
    
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=strut_depth * 0.75,
        depth=strut_width,
        location=(side * strut_spacing_x, elbow_y, elbow_z),
        rotation=(0, math.radians(90), 0)
    )
    eye_top = bpy.context.active_object
    eye_top.data.materials.append(dark_mat)
    arm_parts.append(eye_top)

# Cross-brace spacer pin
brace_y = p0_y + (vec_y * 0.82)
brace_z = p0_z + (vec_z * 0.82)
bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=0.016,
    depth=strut_spacing_x * 2.2,
    location=(0.0, brace_y, brace_z),
    rotation=(0, math.radians(90), 0)
)
brace = bpy.context.active_object
brace.name = "Lamp_LowerArm_CrossBrace"
brace.data.materials.append(dark_mat)
arm_parts.append(brace)

# ------------------------------------------------------------------------------
# 6. CONTINUOUS SEAMLESS LOWER TENSION ROD (From Bottom Pin to Elbow Pin 2)
# ------------------------------------------------------------------------------
# Pin 2 of the elbow joint is at (elbow_y - 0.08, elbow_z + 0.09)
t_start_y = pin_bottom_y
t_start_z = pin_bottom_z
t_end_y = elbow_y - 0.08
t_end_z = elbow_z + 0.09

dy = t_end_y - t_start_y
dz = t_end_z - t_start_z
t_len = math.sqrt(dy**2 + dz**2)
t_mid_y = (t_start_y + t_end_y) / 2.0
t_mid_z = (t_start_z + t_end_z) / 2.0

# Exact cylinder alignment rotation around X
t_rot_x = math.atan2(-dy, dz)

bpy.ops.mesh.primitive_cylinder_add(
    vertices=12,
    radius=0.012,
    depth=t_len,
    location=(0.0, t_mid_y, t_mid_z),
    rotation=(t_rot_x, 0, 0)
)
tension_rod = bpy.context.active_object
tension_rod.name = "Lamp_TensionRod_Lower"
tension_rod.data.materials.append(dark_mat)
arm_parts.append(tension_rod)

# Coil spring on lower rod near base
spring_y = t_start_y + dy * 0.18
spring_z = t_start_z + dz * 0.18
bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=0.026,
    depth=0.22,
    location=(0.0, spring_y, spring_z),
    rotation=(t_rot_x, 0, 0)
)
spring_coil = bpy.context.active_object
spring_coil.name = "Lamp_TensionSpring_Lower"
spring_coil.data.materials.append(chrome_mat)
arm_parts.append(spring_coil)

# Join all into Lamp_LowerArm
bpy.ops.object.select_all(action='DESELECT')
for p in arm_parts:
    p.select_set(True)
bpy.context.view_layer.objects.active = arm_parts[0]
bpy.ops.object.join()
arm_parts[0].name = "Lamp_LowerArm"

bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("03_lower_arm.py updated cleanly!")
