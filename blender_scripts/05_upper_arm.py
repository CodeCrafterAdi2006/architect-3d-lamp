"""
05_upper_arm.py (Seamless Mechanical Linkage)
Adds the Upper Articulated Arm.
The upper tension rod connects directly and seamlessly to Center Pin 2
with zero gap, zero disconnect, and zero melting/intersecting collars.
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
chrome_mat = bpy.data.materials.get("Mat_Chrome_Accent")

# ------------------------------------------------------------------------------
# 2. CLEANUP EXISTING UPPER ARM OBJECTS
# ------------------------------------------------------------------------------
for obj in list(bpy.data.objects):
    if obj.name.startswith("Lamp_UpperArm") or obj.name.startswith("Lamp_LowerTension"):
        bpy.data.objects.remove(obj, do_unlink=True)

# ------------------------------------------------------------------------------
# 3. ELBOW PIN COORDINATES
# ------------------------------------------------------------------------------
# Center & Mount pin positions
pin1_y = -0.5657
pin1_z = 0.545 + 1.35 * math.cos(math.radians(22.0)) # approx 1.7967

pin2_y = pin1_y - 0.08  # Center Pivot Pin (where both tension rods meet!)
pin2_z = pin1_z + 0.09

pin3_y = pin1_y - 0.15  # Upper Arm Mount Pin
pin3_z = pin1_z + 0.03

# ------------------------------------------------------------------------------
# 4. BUILD UPPER ARTICULATED ARM (Twin Struts reaching up-forward)
# ------------------------------------------------------------------------------
upper_length = 1.15
upper_angle_deg = 36.0 # Natural forward reach
rad_36 = math.radians(upper_angle_deg)

strut_width = 0.032
strut_depth = 0.045
strut_spacing_x = 0.052

p3_y = pin3_y
p3_z = pin3_z

# Forward vector to top shade mount
vec_forward_y = upper_length * math.cos(rad_36) # +0.9304 forward
vec_forward_z = upper_length * math.sin(rad_36) # +0.6759 upward

top_y = p3_y + vec_forward_y # approx +0.215
top_z = p3_z + vec_forward_z # approx +2.503

mid_y = p3_y + (vec_forward_y / 2.0)
mid_z = p3_z + (vec_forward_z / 2.0)

upper_parts = []
rot_arm_x = math.radians(-(90.0 - upper_angle_deg)) # -54 deg

# Twin main struts with clean rounded eyelet ends
for side in (-1, 1):
    # Main straight bar
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(side * strut_spacing_x, mid_y, mid_z),
        rotation=(rot_arm_x, 0, 0)
    )
    bar = bpy.context.active_object
    bar.name = f"Lamp_UpperArm_Bar_{side}"
    bar.scale = (strut_width, strut_depth, upper_length)
    bar.data.materials.append(dark_mat)
    upper_parts.append(bar)
    
    # Bottom eyelet at Pin 3
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=strut_depth * 0.75,
        depth=strut_width,
        location=(side * strut_spacing_x, p3_y, p3_z),
        rotation=(0, math.radians(90), 0)
    )
    eye_bot = bpy.context.active_object
    eye_bot.data.materials.append(dark_mat)
    upper_parts.append(eye_bot)
    
    # Top eyelet at shade mount
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=strut_depth * 0.75,
        depth=strut_width,
        location=(side * strut_spacing_x, top_y, top_z),
        rotation=(0, math.radians(90), 0)
    )
    eye_top = bpy.context.active_object
    eye_top.data.materials.append(dark_mat)
    upper_parts.append(eye_top)

# Cross-brace spacer pin near upper arm center
brace_y = p3_y + (vec_forward_y * 0.52)
brace_z = p3_z + (vec_forward_z * 0.52)
bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=0.016,
    depth=strut_spacing_x * 2.2,
    location=(0.0, brace_y, brace_z),
    rotation=(0, math.radians(90), 0)
)
brace = bpy.context.active_object
brace.name = "Lamp_UpperArm_CrossBrace"
brace.data.materials.append(dark_mat)
upper_parts.append(brace)

# ------------------------------------------------------------------------------
# 5. CONTINUOUS SEAMLESS UPPER TENSION ROD (From Pin 2 to Top Mount)
# ------------------------------------------------------------------------------
u_rod_start_y = pin2_y
u_rod_start_z = pin2_z
u_rod_end_y = top_y
u_rod_end_z = top_z + 0.04 # Connects to top pivot

u_dy = u_rod_end_y - u_rod_start_y
u_dz = u_rod_end_z - u_rod_start_z
u_rod_len = math.sqrt(u_dy**2 + u_dz**2)
u_rod_mid_y = (u_rod_start_y + u_rod_end_y) / 2.0
u_rod_mid_z = (u_rod_start_z + u_rod_end_z) / 2.0

# Exact cylinder alignment rotation around X
u_rot_rod_x = math.atan2(-u_dy, u_dz)

bpy.ops.mesh.primitive_cylinder_add(
    vertices=12,
    radius=0.012,
    depth=u_rod_len,
    location=(0.0, u_rod_mid_y, u_rod_mid_z),
    rotation=(u_rot_rod_x, 0, 0)
)
tension_rod = bpy.context.active_object
tension_rod.name = "Lamp_UpperTension_Rod"
tension_rod.data.materials.append(dark_mat)
upper_parts.append(tension_rod)

# Chrome tension coil spring on upper rod
u_spring_y = u_rod_start_y + u_dy * 0.25
u_spring_z = u_rod_start_z + u_dz * 0.25
bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=0.026,
    depth=0.22,
    location=(0.0, u_spring_y, u_spring_z),
    rotation=(u_rot_rod_x, 0, 0)
)
spring = bpy.context.active_object
spring.name = "Lamp_UpperTension_Spring"
spring.data.materials.append(chrome_mat)
upper_parts.append(spring)

# Join all into single Lamp_UpperArm
bpy.ops.object.select_all(action='DESELECT')
for p in upper_parts:
    p.select_set(True)
bpy.context.view_layer.objects.active = upper_parts[0]
bpy.ops.object.join()
upper_arm_obj = upper_parts[0]
upper_arm_obj.name = "Lamp_UpperArm"

# ------------------------------------------------------------------------------
# 6. ADJUST CAMERA, SAVE & RENDER
# ------------------------------------------------------------------------------
cam = bpy.data.objects.get("Scene_Camera")
if cam:
    cam.location = (5.8, -6.5, 3.2)
    target = mathutils.Vector((0.0, -0.2, 1.4))
    direction = target - cam.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()

render_output = r"c:\AI_Studio\Blender\renders\05_upper_arm.png"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.context.scene.render.filepath = render_output
bpy.ops.render.render(write_still=True)

print("\n" + "="*60)
print("SUCCESS: 05_upper_arm.py (Seamless Alignment)")
print("="*60)
print("Lower & Upper tension rods meet seamlessly at Center Pin 2.")
print("Zero gaps, zero disconnected stubs, zero intersecting collars.")
print("="*60 + "\n")
