bl_info = {
    "name": "JSON exporter  ",
    "author": "Ville Seppänen",
    "wiki_url": "https://github.com/villesepp/Blender",
    "version": (1, 0),
    "blender": (4, 3, 2),
    #"location": "View3D > Sidebar > JSONexport",
    "description": "Export a JSON file with some object properties",
    "category": "Add Mesh",
}

import bpy
import json
import os

# Export JSON as before
selected_collection = bpy.context.view_layer.active_layer_collection.collection

# Save in same folder as the .blend file
blend_dir = os.path.dirname(bpy.data.filepath)
output_path = os.path.join(blend_dir, f"{selected_collection.name}.json")

# Ensure a collection is selected
if not selected_collection:
    raise ValueError("No collection selected.")

# Prepare data structure
export_data = {
    "collection": selected_collection.name,
    "objects": []
}

# Function to convert Blender custom property values to JSON-safe values
def convert_value(value):
    if isinstance(value, (int, float, str, bool)):
        return value
    elif hasattr(value, "to_list"):  # e.g., Vector, Color
        return list(value)
    else:
        return str(value)  # fallback for unsupported types

# Collect all object data first
collected_objects = []

# Properties to be ignored
ignoreproperties = ['cycles', 'booleans'] 

# Decimal precision
precision = 1

# Gather object data
for obj in selected_collection.objects:
    if obj.type == 'MESH':
        obj_data = {
            "name": obj.name,
            "position": {
                "x": round(obj.location.x, precision),
                "y": round(obj.location.y, precision),
                "z": round(obj.location.z, precision
                )
            },
            "custom_properties": {}
        }
        # Collect custom properties
        for key in obj.keys():
            if key not in ignoreproperties:  # Skip Blender internal metadata
                obj_data["custom_properties"][key] = convert_value(obj[key])
        collected_objects.append(obj_data)
        
# Sort objects by name
collected_objects.sort(key=lambda o: o["name"].lower())

# Assign to export data
export_data["objects"] = collected_objects

# Write to JSON
with open(output_path, 'w') as f:
    json.dump(export_data, f, indent=4)

print(f"Exported {len(export_data['objects'])} objects to {output_path}")