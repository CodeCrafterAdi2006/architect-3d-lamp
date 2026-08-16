import bpy

# Clear existing objects in the default startup scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Add a test UV Sphere
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1.5,
    location=(0, 0, 1.5)
)

sphere = bpy.context.active_object
sphere.name = "Test_Sphere"

# Save the blend file
output_path = r"c:\AI_Studio\Blender\test_output.blend"
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("\n" + "="*50)
print(f"SUCCESS: Connected to Blender {bpy.app.version_string}!")
print(f"Created: {sphere.name} at location {sphere.location}")
print(f"Saved blend file to: {output_path}")
print("="*50 + "\n")
