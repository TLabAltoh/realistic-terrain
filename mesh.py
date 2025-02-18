import bpy
import bmesh

#
# Terrain Mesh
#   

class tlab_terrain_smooth_terrain_mesh(bpy.types.Operator):
    bl_idname = "tlab_terrain.smooth_terrain_mesh"
    bl_label = "Smooth Terrain Mesh"
    bl_description = "Smooth Terrain Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            # enter edit mode.
            bpy.ops.object.mode_set(mode='EDIT')
            
            #print("name: ", obj.name)
            #print("object.data.name: ", obj.data.name)
            
            """
            vertices = obj.data.vertices
            vertices_num = len(vertices)
            print("vertices num: ", vertices_num)
            """
            
            mesh_data = bmesh.from_edit_mesh(obj.data)
            #print("mesh_data: ", mesh_data)
            
            verts_smoothed = []
            
            # calc smooth z.
            for v in mesh_data.verts:
                connected_vert = []
                for e in v.link_edges:
                    v_other = e.other_vert(v)
                    connected_vert.append(v_other.co[2])
                    
                # print(connected_vert)
                # print(type(connected_vert[0]))
                smoothed = sum(connected_vert) / len(connected_vert)
                # print(smoothed)
                verts_smoothed.append(smoothed)
            
            # set smoothed z
            i = 0
            for v in mesh_data.verts:
                v.co[2] = verts_smoothed[i]
                i += 1
            
            # switch back to object mode.
            bpy.ops.object.mode_set(mode='OBJECT')
            
        return {"FINISHED"}

class tlab_terrain_grid_settings(bpy.types.Operator):  
    bl_idname = "tlab_terrain.grid_settings"
    bl_label = "Grid Settings"
    bl_description = "Grid Settings"
    bl_options = {'REGISTER', 'UNDO'}

    grid_size : bpy.props.FloatProperty(name = "size: ", default = 20.0)
    grid_res : bpy.props.IntProperty(name = "res: ", default = 50)

    def execute(self, context):
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=self.grid_res, y_subdivisions=self.grid_res, size=self.grid_size, calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class tlab_terrain_generate_terrain_mesh(bpy.types.Operator):
    bl_idname = "tlab_terrain.generate_terrain_mesh"
    bl_label = "Generate Terrain Mesh"
    bl_description = "Generate Terrain Mesh"
    
    def execute(self, context):
        bpy.ops.tlab_terrain.grid_settings("INVOKE_DEFAULT")
        return {"FINISHED"}
    

class TLAB_TERRAIN_MT_mesh(bpy.types.Menu):
    bl_label = "Mesh"
    
    def draw(self, context):
        self.layout.operator("tlab_terrain.generate_terrain_mesh", text="Generate Terrain Mesh")
        self.layout.operator("tlab_terrain.smooth_terrain_mesh", text="Smooth Terrain Mesh")