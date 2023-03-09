from bpy.utils import register_class, unregister_class
from bpy.types import Operator
import math
import bpy
import mathutils
from mathutils import Vector
import os
import bmesh
import json
import enum

bl_info = {
    "name": "Transform Tools",
    "author": "Winderson Soares Matos",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N",
    "description": "Ferramentas para transformações",
    "warning": "",
    "doc_url": "",
    "category": "",
}


#region BOTÕES

class ButtonOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "potato.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        print('Potato')
        return {'FINISHED'}
    
class BOAlinharOrigemCentro(bpy.types.Operator):
    """Alinhar origem no centro do objeto"""
    bl_idname = "potato.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        print('---------- CÓDIGO INICIA AQUI - BOAlinharOrigemCentroInferior ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Define a origem do elemento como centro da geometria
                bpy.ops.object.origin_set(
                    type='ORIGIN_GEOMETRY', center='BOUNDS')
                # Desseleciona o objeto
                obj.select_set(False)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}    

class BOAlinharOrigemCentroInferior(bpy.types.Operator):
    """Alinhar origem no centro inferior do objeto"""
    bl_idname = "potato.2"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        print('---------- CÓDIGO INICIA AQUI - BOAlinharOrigemCentroInferior ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Define a origem do elemento como centro da geometria
                bpy.ops.object.origin_set(
                    type='ORIGIN_GEOMETRY', center='BOUNDS')
                # Define o cursor para a localização do objeto
                cursor.location = obj.location
                # O valor a ser movido pelo cursor, metade da altura do objeto
                cursorZMove = cursor.location.z - (obj.dimensions.z/2)
                # Move o cursor para baixo do elemento
                cursor.location.z = cursorZMove
                # Define a origem para o cursor
                bpy.ops.object.origin_set(
                    type='ORIGIN_CURSOR', center='MEDIAN')
                # Reseta o cursor para a posição original
                cursor.location = cursorLoc
                # Desseleciona o objeto
                obj.select_set(False)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}    
        
class BOAlinharOrigemCentroSuperior(bpy.types.Operator):
    """Alinhar origem no centro superior do objeto"""
    bl_idname = "potato.3"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOAlinharOrigemCentroSuperior ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Define a origem do elemento como centro da geometria
                bpy.ops.object.origin_set(
                    type='ORIGIN_GEOMETRY', center='BOUNDS')
                # Define o cursor para a localização do objeto
                cursor.location = obj.location
                # O valor a ser movido pelo cursor, metade da altura do objeto
                cursorZMove = cursor.location.z + (obj.dimensions.z/2)
                # Move o cursor para baixo do elemento
                cursor.location.z = cursorZMove
                # Define a origem para o cursor
                bpy.ops.object.origin_set(
                    type='ORIGIN_CURSOR', center='MEDIAN')
                # Reseta o cursor para a posição original
                cursor.location = cursorLoc
                # Desseleciona o objeto
                obj.select_set(False)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}

class BOMoverOrigemEmXPos(bpy.types.Operator):
    """Alinhar origem no centro superior do objeto"""
    bl_idname = "potato.4"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOMoverOrigemEmXPos ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Define o cursor para a localização do objeto
                cursor.location = obj.location
                # O valor a ser movido pelo cursor, metade da altura do objeto
                cursorXMove = cursor.location.x + (obj.dimensions.x/2)
                # Move o cursor para baixo do elemento
                cursor.location.x = cursorXMove
                # Define a origem para o cursor
                bpy.ops.object.origin_set(
                    type='ORIGIN_CURSOR', center='MEDIAN')
                # Reseta o cursor para a posição original
                cursor.location = cursorLoc
                # Desseleciona o objeto
                obj.select_set(False)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}

class BOMoverOrigemEmXNeg(bpy.types.Operator):
    """Alinhar origem no centro superior do objeto"""
    bl_idname = "potato.5"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOMoverOrigemEmXNeg ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Define o cursor para a localização do objeto
                cursor.location = obj.location
                # O valor a ser movido pelo cursor, metade da altura do objeto
                cursorXMove = cursor.location.x - (obj.dimensions.x/2)
                # Move o cursor para baixo do elemento
                cursor.location.x = cursorXMove
                # Define a origem para o cursor
                bpy.ops.object.origin_set(
                    type='ORIGIN_CURSOR', center='MEDIAN')
                # Reseta o cursor para a posição original
                cursor.location = cursorLoc
                # Desseleciona o objeto
                obj.select_set(False)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}
    
class BOMoverOrigemEmYPos(bpy.types.Operator):
    """Alinhar origem no centro superior do objeto"""
    bl_idname = "potato.6"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOMoverOrigemEmYPos ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Define o cursor para a localização do objeto
                cursor.location = obj.location
                # O valor a ser movido pelo cursor, metade da altura do objeto
                cursorXMove = cursor.location.y + (obj.dimensions.y/2)
                # Move o cursor para baixo do elemento
                cursor.location.y = cursorXMove
                # Define a origem para o cursor
                bpy.ops.object.origin_set(
                    type='ORIGIN_CURSOR', center='MEDIAN')
                # Reseta o cursor para a posição original
                cursor.location = cursorLoc
                # Desseleciona o objeto
                obj.select_set(False)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}

class BOMoverOrigemEmYNeg(bpy.types.Operator):
    """Alinhar origem no centro superior do objeto"""
    bl_idname = "potato.7"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOMoverOrigemEmYNeg ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Define o cursor para a localização do objeto
                cursor.location = obj.location
                # O valor a ser movido pelo cursor, metade da altura do objeto
                cursorXMove = cursor.location.y - (obj.dimensions.y/2)
                # Move o cursor para baixo do elemento
                cursor.location.y = cursorXMove
                # Define a origem para o cursor
                bpy.ops.object.origin_set(
                    type='ORIGIN_CURSOR', center='MEDIAN')
                # Reseta o cursor para a posição original
                cursor.location = cursorLoc
                # Desseleciona o objeto
                obj.select_set(False)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}

class BOMoverParaOrigem(bpy.types.Operator):
    """Move o objeto para a origem 0,0,0"""
    bl_idname = "potato.8"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOMoverParaOrigem ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Define a localização do objeto
                obj.location = (0,0,0)
                # Desseleciona o objeto
                obj.select_set(False)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}

class BOAlinharADoisObjetos(bpy.types.Operator):
    """Alinha um objeto entre dois objetos"""
    bl_idname = "potato.9"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOAlinharADoisObjetos ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        if len(selection) != 3:
            return
        else:
            posA, posB = (obj.location for obj in selection if obj != active_object)
            pontoCentral = (posA + posB)/2
            active_object.location = pontoCentral
            eixo = posA - posB
            active_object.rotation_mode = 'QUATERNION'
            active_object.rotation_quaternion = eixo.to_track_quat('Z','Y')
            active_object.rotation_mode = 'XYZ'
        
        return {'FINISHED'}

class BOAlinharOrigemASeleção(bpy.types.Operator):
    """Alinha a origem do objeto a seleção"""
    bl_idname = "potato.10"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOAlinharOrigemASeleção ----------')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Ativa o modo de edição, ambos métodos funcionam
        bpy.ops.object.mode_set(mode='EDIT')

        # Move o cursor para a seleção
        bpy.ops.view3d.snap_cursor_to_selected()

        # Sai do modo de ediçao, ambos métodos funcionam
        bpy.ops.object.mode_set(mode='OBJECT')

        # Define a origem para o cursor
        bpy.ops.object.origin_set(
            type='ORIGIN_CURSOR', center='BOUNDS')
        
        # Reseta o cursor para a posição original
        cursor.location = cursorLoc

        return {'FINISHED'}

class BOALinharElementoAOutro(bpy.types.Operator):
    """Alinha a origem do objeto a origem de outro objeto"""
    bl_idname = "potato.11"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOALinharElementoAOutro ----------')

        # Posição original do cursor
        cursor = bpy.context.scene.cursor
        cursorLoc = mathutils.Vector(cursor.location)

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Reseta o cursor para a posição original
        cursor.location = cursorLoc

        if len(selection) != 2:
            return
        else:
            for obj in selection:
                if obj != active_object:
                    active_object.location = obj.location

        return {'FINISHED'}

class BOAlinharSelecaoEmX(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "potato.12"
    bl_label = "Simple potato Operator"

    

    def execute(self, context):
        
        print('BOAlinharSelecaoEmX')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        AlinharElemento(obj, 0)

        return {'FINISHED'}
    
class BOAlinharSelecaoEmY(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "potato.13"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('BOAlinharSelecaoEmY')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        AlinharElemento(obj, 1)

        return {'FINISHED'}
    
class BOAlinharSelecaoEmZ(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "potato.14"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        
        print('BOAlinharSelecaoEmZ')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        AlinharElemento(obj, 2)

        return {'FINISHED'}

#endregion



class CustomPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Transform Panel"
    bl_idname = "OBJECT_PT_TFTOOLS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TF Tools"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator(BOAlinharOrigemCentroSuperior.bl_idname,
                     text="Eixo superior", icon='EMPTY_AXIS')
        row = layout.row()
        row.operator(BOAlinharOrigemCentro.bl_idname,
                     text="Eixo centro", icon='EMPTY_AXIS')
        row = layout.row()
        row.operator(BOAlinharOrigemCentroInferior.bl_idname,
                     text="Eixo inferior", icon='EMPTY_AXIS')
        row = layout.row()
        row.operator(BOMoverOrigemEmYPos.bl_idname,
                     text="", icon='TRIA_UP')
        row = layout.row()
        row.operator(BOMoverOrigemEmXNeg.bl_idname,
                     text="", icon='TRIA_LEFT')
        row.operator(BOMoverOrigemEmXPos.bl_idname,
                     text="", icon='TRIA_RIGHT')
        row = layout.row()
        row.operator(BOMoverOrigemEmYNeg.bl_idname,
                     text="", icon='TRIA_DOWN')
        row = layout.row()
        row.operator(BOMoverParaOrigem.bl_idname,
                     text="Mover 0,0,0", icon='EMPTY_AXIS')
        row = layout.row()
        row.operator(BOAlinharADoisObjetos.bl_idname,
                     text="Alinhar entre", icon='IPO_LINEAR')
        row = layout.row()
        row.operator(BOAlinharOrigemASeleção.bl_idname,
                     text="Origem a seleção", icon='EMPTY_AXIS')
        row = layout.row()
        row.operator(BOALinharElementoAOutro.bl_idname,
                     text="Alinhar objeto", icon='EMPTY_AXIS')
        row = layout.row()
        row.operator(BOAlinharSelecaoEmX.bl_idname,
                     text="X")
        row.operator(BOAlinharSelecaoEmY.bl_idname,
                     text="Y")
        row.operator(BOAlinharSelecaoEmZ.bl_idname,
                     text="Z")
        
        

_classes = [
    BOAlinharOrigemCentro,
    BOAlinharOrigemCentroInferior,
    BOAlinharOrigemCentroSuperior,
    BOMoverOrigemEmYPos,
    BOMoverOrigemEmXNeg,
    BOMoverOrigemEmXPos,
    BOMoverOrigemEmYNeg,
    BOMoverParaOrigem,
    BOAlinharADoisObjetos,
    BOAlinharOrigemASeleção,
    BOALinharElementoAOutro,
    BOAlinharSelecaoEmX,
    BOAlinharSelecaoEmY,
    BOAlinharSelecaoEmZ,
    CustomPanel]


#region FUNÇÕES

def AlinharElemento(obj, direcao):
    # Cria um bmesh dele
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        
        # Pega o modo de edição
        editMode = 0
        edit = False

        if bpy.context.object.mode == 'EDIT':
            edit = True
            if mesh.is_editmode:
                # Verifica o modo de seleção ativo
                if bpy.context.tool_settings.mesh_select_mode[0]:
                    editMode = 0
                    print("Modo de seleção de Vértices ativo")
                elif bpy.context.tool_settings.mesh_select_mode[1]:
                    editMode = 1
                    print("Modo de seleção de Bordas ativo")
                elif bpy.context.tool_settings.mesh_select_mode[2]:
                    editMode = 2
                    print("Modo de seleção de Faces ativo")
        else:
            return {'FINISHED'}
        
        # Caso o modo de edição esteja ativo
        if editMode == 0:
            return {'FINISHED'}

        if editMode == 1:
            # Pega a face selecionada
            edges = []

            for edge in bm.edges:
                if edge.select:
                    edges.append(edge)

            edge = edges[0]

            bpy.ops.mesh.select_linked()
            AlinharArestas(bm, edge, direcao)

            # Desseleciona todos os objetos
            bpy.ops.mesh.select_all(action='DESELECT')
            # Volta a seleção para o elemento selecionado originalmente
            edge.select = True
            # Atualiza na vista o objeto
            bpy.ops.object.mode_set(mode='OBJECT') 
            bpy.ops.object.mode_set(mode='EDIT') 

        if editMode == 2:
        # Pega a face selecionada
            faces = []

            for face in bm.faces:
                if face.select:
                    faces.append(face)

            face = faces[0]

            bpy.ops.mesh.select_linked()
            AlinharFace(bm, face, direcao)

            # Desseleciona todos os objetos
            bpy.ops.mesh.select_all(action='DESELECT')
            # Volta a seleção para o elemento selecionado originalmente
            face.select = True
            # Atualiza na vista o objeto
            bpy.ops.object.mode_set(mode='OBJECT') 
            bpy.ops.object.mode_set(mode='EDIT')

def AlinharArestas(bm, source, direcao):
    if source == None:
        return    
    moveverts = []
    for v1 in bm.verts:
        if v1.select:
            moveverts.append(v1)
        
    center = Vector((0.0, 0.0, 0.0))
    for v1 in moveverts:
        center = center + v1.co    
        
    center = center / len(moveverts)    
    
    # Altera o valor dos vetores conforme a direcão
    vetorInicial = Vector((0,0,0))
    vetorFinal = Vector((0,0,0))
    vetorMedio = Vector((0,0,0))
    if direcao == 0:
        vetorFinal = Vector((1,0,0))
    elif direcao == 1:
        vetorFinal = Vector((0,1,0))
    elif direcao == 2:
        vetorFinal = Vector((0,0,1))
    
    sv = source.verts[0].co - source.verts[1].co    
    tv = vetorInicial - vetorFinal
    
    sv2 = sv * -1   
    
    ro1 = sv.rotation_difference(tv)
    ro2 = sv2.rotation_difference(tv)    
    
    c1 = vs_midpoint(source.verts[0], source.verts[1])
    c2 = (vetorInicial + vetorFinal) /2
    
    result1 = rotate_vector(c1, center, ro1) - c2
    result2 = rotate_vector(c1, center, ro2) - c2
    if result1.length < result2.length:
        ro3 = ro1
    else:
        ro3 = ro2    
    #if invert_direction:
    #    sv = sv * -1
    #ro1 = sv.rotation_difference(tv)
    
    matro = ro3.to_matrix()
    bmesh.ops.rotate(bm, cent=center, matrix=matro, verts=moveverts)

def AlinharVertices(bm, source, direcao):
    print(len(source))
    if source == None or len(source) < 2:
        return    
    moveverts = []
    for v1 in bm.verts:
        if v1.select:
            moveverts.append(v1)
        
    center = Vector((0.0, 0.0, 0.0))
    for v1 in moveverts:
        center = center + v1.co    
        
    center = center / len(moveverts)    
    
    # Altera o valor dos vetores conforme a direcão
    vetorInicial = Vector((0,0,0))
    vetorFinal = Vector((0,0,0))
    vetorMedio = Vector((0,0,0))
    if direcao == 0:
        vetorFinal = Vector((1,0,0))
    elif direcao == 1:
        vetorFinal = Vector((0,1,0))
    elif direcao == 2:
        vetorFinal = Vector((0,0,1))
    
    sv = moveverts[0].co - moveverts[1].co    
    tv = vetorInicial - vetorFinal
    
    sv2 = sv * -1   
    
    ro1 = sv.rotation_difference(tv)
    ro2 = sv2.rotation_difference(tv)    
    
    c1 = vs_midpoint(moveverts[0], moveverts[1])
    c2 = (vetorInicial + vetorFinal) /2
    
    result1 = rotate_vector(c1, center, ro1) - c2
    result2 = rotate_vector(c1, center, ro2) - c2
    if result1.length < result2.length:
        ro3 = ro1
    else:
        ro3 = ro2    
    #if invert_direction:
    #    sv = sv * -1
    #ro1 = sv.rotation_difference(tv)
    
    matro = ro3.to_matrix()
    bmesh.ops.rotate(bm, cent=center, matrix=matro, verts=moveverts)

def AlinharFace(bm, face, direcao):
    if face == None:
        return    
    
    # Guarda os vértices selecionados
    faceVerts = []
    
    for v in bm.verts:
        if v.select:
            faceVerts.append(v)
    
    # Pega o ponto central da face
    faceCenterPoint = face.calc_center_median()
    #tp = Vector((0,0,0))
    targetPoint = faceCenterPoint # Usa o mesmo centro para o alvo
    
    # Calcula as transformacões necessarias
    norm = Vector((0,0,1))
    if direcao == 0:
        norm = Vector((1,0,0))
    elif direcao == 1:
        norm = Vector((0,1,0))
    elif direcao == 2:
        norm = Vector((0,0,1))  
    rodif = face.normal.rotation_difference(norm)    
    matro = rodif.to_matrix()
    
    bmesh.ops.rotate(bm, cent=faceCenterPoint, matrix=matro, verts=faceVerts)    
    movedif = targetPoint - faceCenterPoint
    bmesh.ops.translate(bm, vec=movedif, verts=faceVerts)  
  
def vs_midpoint(v1, v2):
    return (v1.co + v2.co)/2

def rotate_vector(v, center, q):
    v2 = v.copy()
    v2 = v2 - center
    v2.rotate(q)
    v2 = v2 + center
    return v2

#endregion

def register():
    for cls in _classes:
        register_class(cls)


def unregister():
    for cls in _classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()