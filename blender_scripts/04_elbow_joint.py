"""
04_elbow_joint.py (Refined Separation & True Oblong Hinge Bracket)
Fixes the overlapping/melted pin caps by properly spacing the 3 pivot bolts,
shapes the elbow plate to match the reference photo's curved bracket,
and adds a distinct winged thumb-screw on the side.
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
# 2. CLEANUP EXISTING ELBOW OBJECTS
# ------------------------------------------------------------------------------
for obj in list(bpy.data.objects):
    if obj.name.startswith("Lamp_MiddleElbow") or obj.name.startswith("Lamp_Elbow"):
        bpy.data.objects.remove(obj, do_unlink=True)

# ------------------------------------------------------------------------------
# 3. ELBOW JOINT PIN COORDINATES (Top of Lower Arm)
# ------------------------------------------------------------------------------
base_top_z = 0.22
stem_height = 0.16
collar_height = 0.05
collar_z = base_top_z + stem_height + (collar_height / 2.0)
pin_bottom_z = collar_z + 0.06
pin_top_y = -0.06
pin_top_z = pin_bottom_z + 0.16 # 0.65

arm_length = 1.35
rot_x_deg = 90.0 - 68.0 # 22.0 deg
rot_x_rad = math.radians(rot_x_deg)

# Pin 1: Lower arm top eyelet (Fixed base of elbow joint)
pin1_y = pin_top_y - (arm_length * math.sin(rot_x_rad)) # approx -0.5657
pin1_z = pin_top_z + (arm_length * math.cos(rot_x_rad)) # approx 1.8767

# Pin 2: Center hinge pivot (Raised and forward)
pin2_y = pin1_y - 0.08
pin2_z = pin1_z + 0.09

# Pin 3: Upper arm mount (Forward & level)
pin3_y = pin1_y - 0.15
pin3_z = pin1_z + 0.03

plate_thickness = 0.024
plate_x_offset = 0.080 # Outside twin struts

elbow_parts = []

# ------------------------------------------------------------------------------
# 4. CURVED / TRIANGULAR HINGE PLATES (Connecting all 3 widely spaced pins)
# ------------------------------------------------------------------------------
# For each side, we create a clean sculpted bracket enclosing the 3 pins
for side in (-1, 1):
    # Center plate body
    plate_mid_y = (pin1_y + pin2_y + pin3_y) / 3.0
    plate_mid_z = (pin1_z + pin2_z + pin3_z) / 3.0
    
    # Base hull around the 3 pins using 3 intersecting smooth cylinders
    for p_name, py, pz in [("P1", pin1_y, pin1_z), ("P2", pin2_y, pin2_z), ("P3", pin3_y, pin3_z)]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=20,
            radius=0.065,
            depth=plate_thickness,
            location=(side * plate_x_offset, py, pz),
            rotation=(0, math.radians(90), 0)
        )
        cyl = bpy.context.active_object
        cyl.name = f"Lamp_ElbowPlate_{side}_{p_name}"
        cyl.data.materials.append(dark_mat)
        elbow_parts.append(cyl)
    
    # Connecting central web between the 3 lobes
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(side * plate_x_offset, plate_mid_y, plate_mid_z),
        rotation=(math.radians(-15), 0, 0)
    )
    web = bpy.context.active_object
    web.name = f"Lamp_ElbowPlate_{side}_Web"
    web.scale = (plate_thickness * 0.95, 0.16, 0.14)
    web.data.materials.append(dark_mat)
    elbow_parts.append(web)

# Join all plate pieces into single Lamp_MiddleElbow
bpy.ops.object.select_all(action='DESELECT')
for p in elbow_parts:
    p.select_set(True)
bpy.context.view_layer.objects.active = elbow_parts[0]
bpy.ops.object.join()
elbow_obj = elbow_parts[0]
elbow_obj.name = "Lamp_MiddleElbow"

# ------------------------------------------------------------------------------
# 5. DISTINCT, WELL-SPACED SILVER BOLTS (Zero Overlap / Melt)
# ------------------------------------------------------------------------------
bolt_radius = 0.018
cap_radius = 0.028 # Well within the 0.08+ spacing between pins

pins_list = [
    ("LowerArmPin", pin1_y, pin1_z),
    ("CenterPivot", pin2_y, pin2_z),
    ("UpperArmPin", pin3_y, pin3_z),
]

for name, py, pz in pins_list:
    # Through-bolt
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=bolt_radius,
        depth=plate_x_offset * 2.5,
        location=(0.0, py, pz),
        rotation=(0, math.radians(90), 0)
    )
    bolt = bpy.context.active_object
    bolt.name = f"Lamp_ElbowBolt_{name}"
    bolt.data.materials.append(chrome_mat)
    
    # Silver dome rivet caps on both sides
    for side in (-1, 1):
        # Skip right-side center cap because the thumb-screw goes there!
        if name == "CenterPivot" and side == 1:
            continue
            
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=cap_radius,
            depth=0.014,
            location=(side * (plate_x_offset + plate_thickness/2.0 + 0.007), py, pz),
            rotation=(0, math.radians(90), 0)
        )
        cap = bpy.context.active_object
        cap.name = f"Lamp_ElbowCap_{name}_{side}"
        cap.data.materials.append(chrome_mat)

# ------------------------------------------------------------------------------
# 6. DISTINCT WINGED THUMB-SCREW (Option B — clearly looks like a fastener)
# ------------------------------------------------------------------------------
screw_x = plate_x_offset + plate_thickness/2.0 + 0.018

# Small central screw hub
bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=0.035,
    depth=0.022,
    location=(screw_x, pin2_y, pin2_z),
    rotation=(0, math.radians(90), 0)
)
hub = bpy.context.active_object
hub.name = "Lamp_ThumbScrew_Hub"
hub.data.materials.append(dark_mat)

# Winged cross-bar for turning
bpy.ops.mesh.primitive_cube_add(
    size=1.0,
    location=(screw_x + 0.012, pin2_y, pin2_z),
    rotation=(math.radians(25), 0, 0)
)
wing = bpy.context.active_object
wing.name = "Lamp_ThumbScrew_Wing"
wing.scale = (0.016, 0.12, 0.035)
wing.data.materials.append(dark_mat)

# Center chrome rivet on thumb screw
bpy.ops.mesh.primitive_cylinder_add(
    vertices=12,
    radius=0.014,
    depth=0.01,
    location=(screw_x + 0.022, pin2_y, pin2_z),
    rotation=(0, math.radians(90), 0)
)
screw_center = bpy.context.active_object
screw_center.name = "Lamp_ThumbScrew_ChromeCenter"
screw_center.data.materials.append(chrome_mat)

# ------------------------------------------------------------------------------
# 7. ADJUST CAMERA, SAVE & RENDER
# ------------------------------------------------------------------------------
cam = bpy.data.objects.get("Scene_Camera")
if cam:
    cam.location = (5.2, -5.6, 3.4)
    cam.rotation_euler = (math.radians(65), 0, math.radians(42))

render_output = r"c:\AI_Studio\Blender\renders\04_elbow_joint.png"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.context.scene.render.filepath = render_output
bpy.ops.render.render(write_still=True)

print("\n" + "="*60)
print("SUCCESS: 04_elbow_joint.py (Refined Clean Bracket & Spacing)")
print("="*60)
print(f"Pin 1 (Lower Arm):   Y={pin1_y:.3f}, Z={pin1_z:.3f}")
print(f"Pin 2 (Center Pivot): Y={pin2_y:.3f}, Z={pin2_z:.3f}")
print(f"Pin 3 (Upper Arm):   Y={pin3_y:.3f}, Z={pin3_z:.3f}")
print(f"Pin Spacing:         ~0.10+ units apart (Clean Separation)")
print(f"Thumb-Screw:         Winged Turn-Key on Pin 2")
print("="*60 + "\n")
