"""
06_shade.py (Realistic Bulb & Clean Cable Routing)
1. Cable routes cleanly: arches from the top socket grommet and drops smoothly
   BETWEEN the twin struts in the center channel (no cutting through solid metal!).
2. Realistic A19 Bulb: larger, smooth-shaded, with ceramic/screw base socket.
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

cream_mat = bpy.data.materials.get("Mat_ShadeInterior")
if not cream_mat:
    cream_mat = bpy.data.materials.new(name="Mat_ShadeInterior")
    cream_mat.use_nodes = True
    c_bsdf = cream_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs["Base Color"].default_value = (0.94, 0.90, 0.82, 1.0)
        c_bsdf.inputs["Roughness"].default_value = 0.4
        c_bsdf.inputs["Emission Color"].default_value = (1.0, 0.85, 0.55, 1.0)
        c_bsdf.inputs["Emission Strength"].default_value = 0.8

bulb_mat = bpy.data.materials.get("Mat_Bulb_Glow")
if not bulb_mat:
    bulb_mat = bpy.data.materials.new(name="Mat_Bulb_Glow")
    bulb_mat.use_nodes = True
    b_bsdf = bulb_mat.node_tree.nodes.get("Principled BSDF")
    if b_bsdf:
        b_bsdf.inputs["Base Color"].default_value = (1.0, 0.98, 0.90, 1.0)
        b_bsdf.inputs["Emission Color"].default_value = (1.0, 0.92, 0.65, 1.0)
        b_bsdf.inputs["Emission Strength"].default_value = 6.0

# ------------------------------------------------------------------------------
# 2. CLEANUP EXISTING OBJECTS
# ------------------------------------------------------------------------------
for obj in list(bpy.data.objects):
    if any(obj.name.startswith(p) for p in ["Lamp_Top", "Lamp_Shade", "Lamp_Bulb", "Lamp_PowerCord", "Lamp_Cable"]):
        bpy.data.objects.remove(obj, do_unlink=True)

# ------------------------------------------------------------------------------
# 3. TOP JOINT & AXIS
# ------------------------------------------------------------------------------
top_pin_y = 0.215
top_pin_z = 2.503

tilt_deg = 38.0
rad_tilt = math.radians(tilt_deg)

dir_y = math.cos(rad_tilt)   # +0.7880 (forward)
dir_z = -math.sin(rad_tilt)  # -0.6157 (downward)
rot_shade_x = math.atan2(-dir_y, dir_z) # -128 deg

# ------------------------------------------------------------------------------
# 4. TOP SWIVEL BOLT & NECK BRACKET
# ------------------------------------------------------------------------------
bracket_x = 0.075

bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=0.024,
    depth=bracket_x * 2.6,
    location=(0.0, top_pin_y, top_pin_z),
    rotation=(0, math.radians(90), 0)
)
top_bolt = bpy.context.active_object
top_bolt.name = "Lamp_TopJoint_Bolt"
top_bolt.data.materials.append(chrome_mat)

for side in (-1, 1):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.036,
        depth=0.015,
        location=(side * (bracket_x * 1.35), top_pin_y, top_pin_z),
        rotation=(0, math.radians(90), 0)
    )
    cap = bpy.context.active_object
    cap.name = f"Lamp_TopBoltCap_{side}"
    cap.data.materials.append(chrome_mat)

# Neck collar connecting to shade cap
neck_len = 0.14
neck_pos_y = top_pin_y + dir_y * (neck_len / 2.0)
neck_pos_z = top_pin_z + dir_z * (neck_len / 2.0)

bpy.ops.mesh.primitive_cylinder_add(
    vertices=20,
    radius=0.075,
    depth=neck_len,
    location=(0.0, neck_pos_y, neck_pos_z),
    rotation=(rot_shade_x, 0, 0)
)
neck = bpy.context.active_object
neck.name = "Lamp_Top_Neck"
neck.data.materials.append(dark_mat)

# ------------------------------------------------------------------------------
# 5. STEPPED TOP CAP & TRUE HOLLOW FLARED SHADE DOME
# ------------------------------------------------------------------------------
cap_start_y = top_pin_y + dir_y * neck_len
cap_start_z = top_pin_z + dir_z * neck_len
cap_len = 0.20
cap_mid_y = cap_start_y + dir_y * (cap_len / 2.0)
cap_mid_z = cap_start_z + dir_z * (cap_len / 2.0)

# Top socket cap cylinder
bpy.ops.mesh.primitive_cylinder_add(
    vertices=24,
    radius=0.18,
    depth=cap_len,
    location=(0.0, cap_mid_y, cap_mid_z),
    rotation=(rot_shade_x, 0, 0)
)
top_cap = bpy.context.active_object
top_cap.name = "Lamp_Shade_TopCap"
top_cap.data.materials.append(dark_mat)

# Rubber cable grommet at the top peak of the cap
grommet_y = cap_start_y - dir_y * 0.02
grommet_z = cap_start_z - dir_z * 0.02
bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=0.035,
    depth=0.04,
    location=(0.0, grommet_y, grommet_z),
    rotation=(rot_shade_x, 0, 0)
)
grommet = bpy.context.active_object
grommet.name = "Lamp_Cable_Grommet"
grommet.data.materials.append(dark_mat)

# Main Bell Cone (100% Hollow opening)
bell_start_y = cap_start_y + dir_y * cap_len
bell_start_z = cap_start_z + dir_z * cap_len
bell_len = 0.44
bell_mid_y = bell_start_y + dir_y * (bell_len / 2.0)
bell_mid_z = bell_start_z + dir_z * (bell_len / 2.0)

bpy.ops.mesh.primitive_cone_add(
    vertices=32,
    radius1=0.20,             # Top junction
    radius2=0.62,             # Wide open rim
    depth=bell_len,
    end_fill_type='NOTHING',  # Hollow opening
    location=(0.0, bell_mid_y, bell_mid_z),
    rotation=(rot_shade_x, 0, 0)
)
shade_bell = bpy.context.active_object
shade_bell.name = "Lamp_Shade_Bell"
shade_bell.data.materials.append(dark_mat)
shade_bell.data.materials.append(cream_mat)

# Smooth shading with auto-smooth
for p in shade_bell.data.polygons:
    p.use_smooth = True

# Solidify modifier for realistic sheet thickness & inner cream surface
solid_mod = shade_bell.modifiers.new(name="Solidify", type='SOLIDIFY')
solid_mod.thickness = 0.022
solid_mod.material_offset_rim = 0
solid_mod.material_offset = 1

# Rolled lip rim on the outer edge
rim_pos_y = bell_start_y + dir_y * bell_len
rim_pos_z = bell_start_z + dir_z * bell_len

bpy.ops.mesh.primitive_torus_add(
    major_radius=0.62,
    minor_radius=0.016,
    major_segments=32,
    minor_segments=12,
    location=(0.0, rim_pos_y, rim_pos_z),
    rotation=(rot_shade_x, 0, 0)
)
rim = bpy.context.active_object
rim.name = "Lamp_Shade_Rim"
rim.data.materials.append(dark_mat)

# ------------------------------------------------------------------------------
# 6. REALISTIC LARGER A19 BULB & CERAMIC SOCKET (Proper Size & Smooth Shading)
# ------------------------------------------------------------------------------
# Bulb ceramic socket base inside top cap
socket_y = bell_start_y + dir_y * 0.06
socket_z = bell_start_z + dir_z * 0.06
bpy.ops.mesh.primitive_cylinder_add(
    vertices=20,
    radius=0.10,
    depth=0.10,
    location=(0.0, socket_y, socket_z),
    rotation=(rot_shade_x, 0, 0)
)
b_socket = bpy.context.active_object
b_socket.name = "Lamp_Bulb_Socket"
b_socket.data.materials.append(chrome_mat)

# Main Bulb (A19 Teardrop shape: Radius = 0.22, Smooth Shaded)
bulb_y = bell_start_y + dir_y * (bell_len * 0.48)
bulb_z = bell_start_z + dir_z * (bell_len * 0.48)

bpy.ops.mesh.primitive_uv_sphere_add(
    segments=24,
    ring_count=16,
    radius=0.22, # Generous, realistic bulb size (matches reference photo)
    location=(0.0, bulb_y, bulb_z)
)
bulb = bpy.context.active_object
bulb.name = "Lamp_Bulb"
for p in bulb.data.polygons:
    p.use_smooth = True
bulb.data.materials.append(bulb_mat)

# Warm Point Light Source
bpy.ops.object.light_add(
    type='POINT',
    radius=0.20,
    location=(0.0, bulb_y, bulb_z)
)
lamp_light = bpy.context.active_object
lamp_light.name = "Lamp_Bulb_Light"
lamp_light.data.energy = 85.0
lamp_light.data.color = (1.0, 0.88, 0.65) # Warm 2700K

# ------------------------------------------------------------------------------
# 7. REALISTIC SLACK CABLE ROUTING (Loops & feeds BETWEEN twin struts)
# ------------------------------------------------------------------------------
# Upper arm direction vector
upper_angle_rad = math.radians(36.0)
u_dir_y = math.cos(upper_angle_rad) # +0.8090
u_dir_z = math.sin(upper_angle_rad) # +0.5878

curve_data = bpy.data.curves.new(name="Lamp_PowerCord_Curve", type='CURVE')
curve_data.dimensions = '3D'
curve_data.bevel_depth = 0.013
curve_data.bevel_resolution = 4
curve_data.use_fill_caps = True

polyline = curve_data.splines.new('BEZIER')
polyline.bezier_points.add(3) # 4 control points for graceful arc

# P0: Emerges straight out of top grommet
p0 = polyline.bezier_points[0]
p0.co = (0.0, grommet_y, grommet_z)
p0.handle_left_type = 'AUTO'
p0.handle_right_type = 'AUTO'

# P1: High apex of the slack arch
p1 = polyline.bezier_points[1]
p1.co = (0.0, top_pin_y - 0.18, top_pin_z + 0.20)
p1.handle_left_type = 'AUTO'
p1.handle_right_type = 'AUTO'

# P2: Drops into the center channel BETWEEN the twin struts (X=0.0)
p2 = polyline.bezier_points[2]
p2.co = (0.0, top_pin_y - 0.25, top_pin_z - 0.12)
p2.handle_left_type = 'AUTO'
p2.handle_right_type = 'AUTO'

# P3: Tucks neatly along the inner channel of the upper arm towards middle elbow
p3 = polyline.bezier_points[3]
p3.co = (0.0, top_pin_y - 0.50, top_pin_z - 0.35)
p3.handle_left_type = 'AUTO'
p3.handle_right_type = 'AUTO'

cord_obj = bpy.data.objects.new("Lamp_PowerCord", curve_data)
bpy.context.collection.objects.link(cord_obj)
cord_obj.data.materials.append(dark_mat)

# ------------------------------------------------------------------------------
# 8. ADJUST CAMERA, SAVE & RENDER
# ------------------------------------------------------------------------------
cam = bpy.data.objects.get("Scene_Camera")
if cam:
    cam.location = (6.0, -6.6, 3.2)
    target = mathutils.Vector((0.0, 0.0, 1.35))
    direction = target - cam.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()

render_output = r"c:\AI_Studio\Blender\renders\06_shade.png"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.context.scene.render.filepath = render_output
bpy.ops.render.render(write_still=True)

print("\n" + "="*60)
print("SUCCESS: 06_shade.py (Realistic Bulb & Clean Cable Routing)")
print("="*60)
print("Bulb: Sized up (Radius=0.22), Smooth Shaded with Socket Mount")
print("Cable: Routes cleanly between twin struts in the center channel")
print("="*60 + "\n")
