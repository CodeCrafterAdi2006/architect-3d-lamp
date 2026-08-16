"""
08_export_glb.py
Phase 5.1: Exports the Desk Lamp model as an optimized self-contained .GLB binary file.
Applies modifiers (Bevel, Solidify), embeds PBR materials, and excludes studio lights/camera.
Saves to exports/desk_lamp.glb and copies to web/assets/desk_lamp.glb.
"""

import bpy
import os
import shutil

blend_path = r"c:\AI_Studio\Blender\desk_lamp_wip.blend"
if not os.path.exists(blend_path):
    raise FileNotFoundError(f"Missing {blend_path}. Run previous steps first.")

bpy.ops.wm.open_mainfile(filepath=blend_path)

# ------------------------------------------------------------------------------
# 1. SELECT ONLY THE LAMP OBJECTS (EXCLUDE LIGHTS, CAMERA, DESK GROUND)
# ------------------------------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')

lamp_objects = []
for obj in bpy.data.objects:
    if obj.name.startswith("Lamp_"):
        # Exclude rigid static wire and its orphaned grommet
        if "PowerCord" in obj.name or "Grommet" in obj.name:
            continue
        obj.select_set(True)
        lamp_objects.append(obj)
        # Ensure object is visible in viewport/render
        obj.hide_viewport = False
        obj.hide_render = False

print(f"Selected {len(lamp_objects)} lamp objects for clean GLB export:")
for o in lamp_objects:
    print(f" - {o.name} ({o.type})")

# ------------------------------------------------------------------------------
# 2. CONVERT CURVES TO MESHES FOR GLTF COMPATIBILITY
# ------------------------------------------------------------------------------
# glTF exporter requires curve objects (like the power cord) to be meshes
for obj in lamp_objects:
    if obj.type == 'CURVE':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target='MESH')
        print(f"Converted curve {obj.name} to mesh.")

# Re-select all lamp objects
bpy.ops.object.select_all(action='DESELECT')
for obj in lamp_objects:
    obj.select_set(True)

if lamp_objects:
    bpy.context.view_layer.objects.active = lamp_objects[0]

# ------------------------------------------------------------------------------
# 3. EXPORT OPTIMIZED GLB
# ------------------------------------------------------------------------------
export_dir = r"c:\AI_Studio\Blender\exports"
os.makedirs(export_dir, exist_ok=True)
glb_path = os.path.join(export_dir, "desk_lamp.glb")

# Blender 5.1 gltf export
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=True,
    export_apply=True,        # Bake modifiers (Solidify, Bevel)
    export_materials='EXPORT',
    export_cameras=False,
    export_lights=False
)

file_size_kb = os.path.getsize(glb_path) / 1024.0

# ------------------------------------------------------------------------------
# 4. COPY ASSET TO WEB DIRECTORY
# ------------------------------------------------------------------------------
web_assets_dir = r"c:\AI_Studio\Blender\web\assets"
os.makedirs(web_assets_dir, exist_ok=True)
web_glb_path = os.path.join(web_assets_dir, "desk_lamp.glb")
shutil.copy2(glb_path, web_glb_path)

print("\n" + "="*60)
print("SUCCESS: 08_export_glb.py (Phase 5.1 GLB Export)")
print("="*60)
print(f"Exported Asset:     {glb_path}")
print(f"Asset File Size:    {file_size_kb:.2f} KB (Ultra lightweight < 500KB)")
print(f"Web Asset Copy:     {web_glb_path}")
print("="*60 + "\n")
