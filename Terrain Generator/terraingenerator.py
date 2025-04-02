bl_info = {
    "name": "Procedural Terrain Generator",
    "author": "Ville Seppänen",
    "wiki_url": "https://github.com/villesepp/Blender",
    "version": (1, 0),
    "blender": (4, 3, 2),
    "location": "View3D > Sidebar > TerrainGen",
    "description": "Generate a simple procedural terrain with vertex colors",
    "category": "Add Mesh",
}

import bpy
import bmesh
from bpy.props import FloatProperty, IntProperty
from mathutils import noise, Vector
import math
import random

def create_subdivided_plane(name="Plane", size=2, cuts=4):
        # Create a new mesh and object
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)

        # Create bmesh and generate a plane
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=cuts + 1, y_segments=cuts + 1, size=size / 2)

        # Write the bmesh into the mesh
        bm.to_mesh(mesh)
        bm.free()

        return obj
    
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
    bl_label = "Generate"
    bl_options = {'REGISTER', 'UNDO'}

    size: FloatProperty(name="Size", default=20.0, min=1.0)
    cuts: IntProperty(name="Subdivisions", default=50, min=1, max=200)
    seed: IntProperty(name="Seed", default=0)
    low_limit: FloatProperty(name="Low Limit", default=-1.0)
    scale: FloatProperty(name="Scale | Noise", default=0.25, min=0.01, max=0.5)
    height: FloatProperty(name="Height | Noise", default=2.0, min=0.1)
    minor_scale: FloatProperty(name="Scale | Min. Noise", default=1.0, min=0.01, max=5.0)
    minor_height: FloatProperty(name="Height | Min. Noise", default=1.0, min=0.0)
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
        seed = self.seed
        low_limit = self.low_limit
        scale = self.scale
        height = self.height
        minor_scale = self.minor_scale
        minor_height = self.minor_height

        obj = create_subdivided_plane(size=size, cuts=cuts)
        mesh = obj.data

        seed = Vector((seed, seed, 0))

        # translate vertices
        for v in mesh.vertices:
            pos = Vector((
                v.co.x * scale,
                v.co.y * scale,
                0
                )) + seed
            v.co.z += noise.noise(pos) * height
        
        # minor translate
        for v in mesh.vertices:
            pos = Vector((
                v.co.x * minor_scale,
                v.co.y * minor_scale,
                0
                )) + seed
            v.co.z += noise.noise(pos) * (v.co.z * minor_height)
            
        # z low-limit
        for v in mesh.vertices:
            if v.co.z < low_limit:
                v.co.z = low_limit

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
    bpy.utils.register_class(TerrainGeneratorOperator)
    bpy.utils.register_class(TerrainGeneratorPanel)


def unregister():
    bpy.utils.unregister_class(TerrainGeneratorPanel)
    bpy.utils.unregister_class(TerrainGeneratorOperator)
    bpy.utils.unregister_class(TerrainSettings)

if __name__ == "__main__":
    register()