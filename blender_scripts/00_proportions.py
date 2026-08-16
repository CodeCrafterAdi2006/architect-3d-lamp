"""
00_proportions.py
Defines the locked-in mathematical proportions, dimensions, angles, and colors 
for the Low-Poly Desk Lamp based on reference image analysis.
This module is imported by all subsequent modeling and material scripts.
"""

# ==============================================================================
# BASE MEASUREMENTS (Normalized units where Base Radius = 1.0)
# ==============================================================================
BASE = {
    "radius": 1.0,           # Wide circular disc
    "height": 0.22,          # Flat profile (approx 4.5:1 width-to-height ratio)
    "bevel_depth": 0.03,     # Subtle rounded upper rim
    "location": (0.0, 0.0, 0.11),  # Sits flat on the ground plane (Z=0)
}

# ==============================================================================
# VERTICAL STEM & SWIVEL SOCKET
# ==============================================================================
STEM = {
    "radius": 0.14,          # Narrow vertical pin
    "height": 0.35,          # Short post rising from center of base
    "location": (0.0, 0.0, 0.395),  # Base height + half stem height
    "bracket_width": 0.16,   # Base hinge bracket width
    "bracket_height": 0.25,
}

# ==============================================================================
# LOWER ARM (Dual parallel low-poly bars)
# ==============================================================================
LOWER_ARM = {
    "bar_width": 0.04,       # Slender rectangular cross-section
    "bar_depth": 0.06,
    "length": 1.35,          # Main reach of lower segment
    "spacing": 0.10,         # Distance between parallel struts
    "angle_deg": 68.0,       # Leaning upward & backward (~68 deg from horizontal)
}

# ==============================================================================
# MIDDLE ELBOW JOINT (Articulated hinge plates & pins)
# ==============================================================================
MIDDLE_ELBOW = {
    "plate_radius": 0.15,    # Hinge circular plate
    "plate_thickness": 0.03,
    "pin_radius": 0.04,      # Joint pivot bolts
    "pin_length": 0.18,
}

# ==============================================================================
# UPPER ARM (Dual parallel low-poly bars)
# ==============================================================================
UPPER_ARM = {
    "bar_width": 0.04,
    "bar_depth": 0.06,
    "length": 1.20,          # Slightly shorter than lower arm for balanced silhouette
    "spacing": 0.10,
    "angle_deg": -42.0,      # Leaning forward towards the work surface
}

# ==============================================================================
# TOP ELBOW & SHADE SOCKET
# ==============================================================================
TOP_ELBOW = {
    "plate_radius": 0.12,
    "socket_radius": 0.16,
    "socket_length": 0.30,   # Cylinder neck leading into shade
    "angle_deg": -35.0,      # Tilted down towards the desk
}

# ==============================================================================
# LAMP SHADE (Classic dome/flared cone with stepped top)
# ==============================================================================
SHADE = {
    "cap_top_radius": 0.18,  # Narrow top step
    "cap_height": 0.25,
    "bell_top_radius": 0.22, # Expanding main bell
    "bell_bottom_radius": 0.68, # Wide flared open rim
    "bell_height": 0.65,     # Depth of shade cavity
    "rim_thickness": 0.02,   # Outer lip
    "tilt_angle_deg": -38.0, # Facing downward-forward
}

# ==============================================================================
# BULB & LIGHT SOURCE
# ==============================================================================
BULB = {
    "radius": 0.14,          # Low-poly Ico-Sphere tucked inside shade
    "light_color_rgb": (1.0, 0.85, 0.55), # Warm tungsten (approx 2700K)
    "light_energy": 25.0,    # Blender light power
    "light_radius": 0.15,
}

# ==============================================================================
# MATERIAL COLORS (RGB Linear)
# ==============================================================================
COLORS = {
    "dark_metal": (0.04, 0.04, 0.045, 1.0),       # Gunmetal matte black (Base, arms, shade)
    "chrome_accents": (0.75, 0.75, 0.78, 1.0),   # Pins, bolts & springs
    "shade_interior": (0.92, 0.88, 0.82, 1.0),   # Cream/white reflective inner coating
    "bulb_glow": (1.0, 0.92, 0.70, 1.0),         # Warm glowing emissive bulb
}

if __name__ == "__main__":
    print("=" * 60)
    print("DESK LAMP PROPORTION TABLE SUMMARY:")
    print("=" * 60)
    print(f"1. BASE:        Diameter = {BASE['radius']*2:.2f}, Height = {BASE['height']:.2f}")
    print(f"2. STEM:        Diameter = {STEM['radius']*2:.2f}, Height = {STEM['height']:.2f}")
    print(f"3. LOWER ARM:   Length = {LOWER_ARM['length']:.2f}, Incline Angle = {LOWER_ARM['angle_deg']}°")
    print(f"4. MID ELBOW:   Plate Dia = {MIDDLE_ELBOW['plate_radius']*2:.2f}")
    print(f"5. UPPER ARM:   Length = {UPPER_ARM['length']:.2f}, Forward Angle = {UPPER_ARM['angle_deg']}°")
    print(f"6. TOP ELBOW:   Socket Dia = {TOP_ELBOW['socket_radius']*2:.2f}")
    print(f"7. SHADE:       Bottom Opening Dia = {SHADE['bell_bottom_radius']*2:.2f}, Length = {SHADE['bell_height']:.2f}")
    print(f"8. BULB:        Radius = {BULB['radius']:.2f}, Color = Warm Tungsten 2700K")
    print("=" * 60)
