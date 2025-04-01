bl_info = {
    "name": "Procedural Terrain Generator",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 3, 2),
    "location": "View3D > Sidebar > TerrainGen",
    "description": "Generate a simple procedural terrain with vertex colors",
    "category": "Add Mesh",
}

import bpy
from bpy.props import FloatProperty, IntProperty
from mathutils import noise, Vector
import math
import random

class TerrainSettings(bpy.types.PropertyGroup):
    size: FloatProperty(name="Plane Size", default=20.0, min=1.0)
    cuts: IntProperty(name="Subdivisions", default=20, min=1, max=300)
    scale: FloatProperty(name="Noise Scale", default=0.3, min=0.01, max=0.5)
    height: FloatProperty(name="Height Multiplier", default=2.0, min=0.1)
    seed: IntProperty(name="Seed Offset", default=0)

class TerrainGeneratorPanel(bpy.types.Panel):
    bl_label = "Terrain Generator"
    bl_idname = "VIEW3D_PT_terrain_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TerrainGen'

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.generate_terrain")


class TerrainGeneratorOperator(bpy.types.Operator):
    bl_idname = "mesh.generate_terrain"
    bl_label = "Generate Procedural Terrain"
    bl_options = {'REGISTER', 'UNDO'}

    size: FloatProperty(name="Plane Size", default=20.0, min=1.0)
    cuts: IntProperty(name="Subdivisions", default=20, min=1, max=200)
    scale: FloatProperty(name="Noise Scale", default=0.3, min=0.01, max=0.5)
    height: FloatProperty(name="Height Multiplier", default=2.0, min=0.1)
    seed: IntProperty(name="Seed Offset", default=0)
    use_vertex_colors: bpy.props.BoolProperty(
        name="Use Vertex Colors",
        description="Apply grayscale vertex colors based on terrain height",
        default=True
    )
    use_smooth_shading: bpy.props.BoolProperty(
        name="Smooth Shading",
        description="Use smooth shading",
        default=True
    )

    def execute(self, context):
        # Use operator properties directly for redo panel
        size = self.size
        cuts = self.cuts
        scale = self.scale
        height = self.height
        seed = self.seed

        # Terrain generation logic
        bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=True)
        bpy.ops.mesh.subdivide(number_cuts=cuts)
        bpy.ops.object.editmode_toggle()

        obj = bpy.context.active_object
        mesh = obj.data

        seed = Vector((seed, seed, 0))

        for v in mesh.vertices:
            pos = Vector((v.co.x * scale, v.co.y * scale, 0)) + seed
            v.co.z = noise.noise(pos) * height

        # Set smooth shading
        if self.use_smooth_shading:
            for poly in mesh.polygons:
                poly.use_smooth = True
        else:
            for poly in mesh.polygons:
                poly.use_smooth = False


        # Apply vertex colors
        if self.use_vertex_colors:
            if not mesh.color_attributes:
                mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')

            color_layer = mesh.color_attributes["Col"].data

            z_min = min(v.co.z for v in mesh.vertices)
            z_max = max(v.co.z for v in mesh.vertices)
            z_range = z_max - z_min if z_max != z_min else 1

            for poly in mesh.polygons:
                for i in poly.loop_indices:
                    loop_vert_index = mesh.loops[i].vertex_index
                    z = mesh.vertices[loop_vert_index].co.z
                    normalized_z = (z - z_min) / z_range
                    color_layer[i].color = (normalized_z, normalized_z, normalized_z, 1)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(TerrainSettings)
    bpy.types.Scene.terrain_settings = bpy.props.PointerProperty(type=TerrainSettings)

    bpy.utils.register_class(TerrainGeneratorOperator)
    bpy.utils.register_class(TerrainGeneratorPanel)


def unregister():
    del bpy.types.Scene.terrain_settings

    bpy.utils.unregister_class(TerrainGeneratorPanel)
    bpy.utils.unregister_class(TerrainGeneratorOperator)
    bpy.utils.unregister_class(TerrainSettings)

if __name__ == "__main__":
    register()