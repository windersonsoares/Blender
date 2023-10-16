from bpy.utils import register_class, unregister_class
from bpy.types import Operator
import math
import bpy
import mathutils
import os
import bmesh
import json
import enum

bl_info = {
    "name": "UE Tools",
    "author": "Winderson Soares Matos",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N",
    "description": "Ferramentas para facilitar o fluxod e trabalho para a UE",
    "warning": "",
    "doc_url": "",
    "category": "",
}


class CadType(enum.Enum):
    Line = 0
    Arc = 1
    Circle = 2
    Polyline = 3
    Hatch = 4
    Point = 5
    Block = 6


class CurveType(enum.Enum):
    Line = 0
    Arc = 1
    Circle = 2


class ButtonOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "potato.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        print('Potato')
        return {'FINISHED'}


class ButtonOperatorShadeNormal(bpy.types.Operator):
    """Altera o Shade do elemento para Shade Smooth e define as Normals das faces"""
    bl_idname = "shade.1"
    bl_label = "ShadeNormal Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - SHADE NORMAL ----------')

        # Função que aplica o Shade Smooth e configura as normals
        def SetSmoothNormal(object, angle):
            # Seleciona o objeto
            object.select_set(True)
            # Ativa o objeto
            bpy.context.view_layer.objects.active = object
            # Define o shading como Smooth
            bpy.ops.object.shade_smooth()
            # Limpa o Normal Data
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            # Define o AutoSmooth
            object.data.use_auto_smooth = True
            object.data.auto_smooth_angle = angle
            # Sai do modo de ediçao, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='OBJECT')
            # bpy.ops.object.editmode_toggle()
            # Desceleciona o objeto
            object.select_set(False)

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects
        # Pega o objeto ativo
        active_object = bpy.context.active_object
        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selection:
            if obj.type == 'MESH':
                SetSmoothNormal(obj, math.radians(30))
        # Restora a seleção
        for obj in selection:
            obj.select_set(True)
        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class ButtonOperatorSDeffineBottomOrigin(bpy.types.Operator):
    """Define a origem do elemento como sendo o centro inferior"""
    bl_idname = "origin.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - DEFFINE BOTTOM ORIGIN ----------')

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
                    type='ORIGIN_GEOMETRY', center='MEDIAN')
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


class ButtonOperatorExportToClipboard(bpy.types.Operator):
    """Copia para a área de transferência as informações dos elementos para ser cerem criados dentro da UE como referência"""
    bl_idname = "export.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - COPY TO CLIPBOARD ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # String final
        finalString = ""

        finalString += "Begin Map"
        finalString += "\n    Begin Level"

        unitInfo = GetUnits()

        for obj in selection:
            if obj.type == 'MESH':
                # Valores da posição do elemento
                name = obj.name
                locX = round(UnitToCentimeter(obj.location.x, unitInfo), 2)
                locY = -round(UnitToCentimeter(obj.location.y, unitInfo), 2)
                locZ = round(UnitToCentimeter(obj.location.z, unitInfo), 2)
                rotation = obj.rotation_euler
                rotX = round(math.degrees(rotation[0]), 2)
                rotY = round(math.degrees(rotation[1]), 2)
                rotZ = round(math.degrees(rotation[2]), 2)
                sclX = round(UnitToCentimeter(
                    obj.dimensions.x/100, unitInfo), 2)
                sclY = round(UnitToCentimeter(
                    obj.dimensions.y/100, unitInfo), 2)
                sclZ = round(UnitToCentimeter(
                    obj.dimensions.z/100, unitInfo), 2)
                # Cria a string a partir dos valores
                finalString += f"\n        Begin Actor Class=StaticMeshActor Name={name} Archetype=StaticMeshActor'/Script/Engine.Default__StaticMeshActor'"
                finalString += "\n            Begin Object Class=StaticMeshComponent Name=StaticMeshComponent0 ObjName=StaticMeshComponent0"
                finalString += "\n            Archetype=StaticMeshComponent'/Script/Engine.Default__StaticMeshActor:StaticMeshComponent0'"
                finalString += "\n            End Object"
                finalString += "\n            Begin Object Name=StaticMeshComponent0"
                finalString += f"\n                StaticMesh=StaticMesh'/Engine/BasicShapes/Cube.Cube'"
                finalString += f"\n                RelativeLocation=(X={locX},Y={locY},Z={locZ})"
                finalString += f"\n                RelativeScale3D=(X={sclX},Y={sclY},Z={sclZ})"
                finalString += f"\n                RelativeRotation=(Pitch={rotY},Yaw={rotZ},Roll={rotX})"
                finalString += "\n                CustomProperties"
                finalString += "\n            End Object"
                finalString += "\n            StaticMeshComponent=StaticMeshComponent0"
                finalString += "\n            Components(0)=StaticMeshComponent0"
                finalString += "\n            RootComponent=StaticMeshComponent0"
                finalString += f'\n            ActorLabel="{name}"'
                finalString += "\n        End Actor"

        finalString += "\n    End Level"
        finalString += "\nBegin Surface"
        finalString += "\nEnd Surface"
        finalString += "\nEnd Map"

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = finalString

        return {'FINISHED'}


class ButtonOperatorCleanUVChannels(bpy.types.Operator):
    """Limpa os canais de UV"""
    bl_idname = "uv.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - CLEANUVCHANNELS ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:
            try:
                if obj.type == 'MESH':
                    mesh = obj.data
                    polygons = mesh.polygons
                    if len(polygons) > 0:
                        obj.select_set(True)
                        # Ativa o objeto
                        bpy.context.view_layer.objects.active = obj
                        # Pega os canais UV e deleta
                        uvlayers = obj.data.uv_layers
                        for uvc in uvlayers:
                            obj.data.uv_layers.remove(uvc)
                        obj.select_set(False)
            except Exception as e:
                print(obj.name)
                print(e)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class ButtonOperatorViewUnwrapIndividual(bpy.types.Operator):
    """""SmartUnwrap os elementos selecionados preparando para a UE"""
    bl_idname = "uv.2"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - SMARTUNWRAPUV TO UE ----------')

        def UnwrapUVProjection(object, angle, margin, uvLayerName):
            # Seleciona o objetos
            object.select_set(True)
            # Ativa o objeto
            bpy.context.view_layer.objects.active = object
            # Cria um novo UV Layer caso nao exista
            newLayer = True
            uvlayers = object.data.uv_layers
            lm = ""
            for layer in uvlayers:
                if (layer.name == uvLayerName):
                    newLayer = False
                    lm = layer
            if newLayer:
                lm = object.data.uv_layers.new(name=uvLayerName)
            lm.active = True
            # Ativa o modo de edição, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='EDIT')
            # bpy.ops.object.editmode_toggle()
            # Seleciona a geometria
            bpy.ops.mesh.select_all(action='SELECT')
            # Chama o Smart UV Projection com os parãmetros passados
            bpy.ops.uv.smart_project(
                angle_limit=math.radians(angle), island_margin=margin)
            # Ajusta o UV, Pack islands
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.pack_islands(margin=margin, rotate=False)
            # Sai do modo de ediçao, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='OBJECT')
            # bpy.ops.object.editmode_toggle()
            # Desceleciona o objeto
            object.select_set(False)

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:
            try:
                if obj.type == 'MESH':
                    mesh = obj.data
                    polygons = mesh.polygons
                    if len(polygons) > 0:
                        UnwrapUVProjection(
                            obj, math.radians(66.0), 0.025, 'LightMap')
                        UnwrapUVProjection(
                            obj, math.radians(66.0), 0.0, 'UVMap')
                        # CubeUVProjection(obj, 0.0, 'UVMap')
                        # CubeUVProjection(obj, 0.025, 'LightMap')
            except Exception as e:
                print(obj.name)
                print(e)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class ButtonOperatorUnwrapElementsToUE(bpy.types.Operator):
    """Unwrap os elementos selecionados preparando para a UE"""
    bl_idname = "uv.3"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - UNWRAPUV TO UE ----------')

        def UnwrapUVProjection(object, angle, margin, uvLayerName):
            # Seleciona o objeto
            object.select_set(True)
            # Ativa o objeto
            bpy.context.view_layer.objects.active = object
            # Cria um novo UV Layer caso nao exista
            newLayer = True
            uvlayers = object.data.uv_layers
            lm = object.data.uv_layers[0]
            for layer in uvlayers:
                if (layer.name == uvLayerName):
                    newLayer = False
                    lm = layer
            if newLayer:
                lm = object.data.uv_layers.new(name=uvLayerName)
            lm.active = True
            # Ativa o modo de edição, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='EDIT')
            # bpy.ops.object.editmode_toggle()
            # Seleciona a geometria
            bpy.ops.mesh.select_all(action='SELECT')
            # Chama o Smart UV Projection com os parãmetros passados
            bpy.ops.uv.smart_project(
                angle_limit=math.radians(angle), island_margin=margin)
            # Sai do modo de ediçao, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='OBJECT')
            # bpy.ops.object.editmode_toggle()
            # Desceleciona o objeto
            object.select_set(False)

        def CubeUVProjection(object, marg, uvLayerName):
            # Seleciona o objetos
            object.select_set(True)
            # Ativa o objeto
            bpy.context.view_layer.objects.active = object
            # Cria um novo UV Layer caso nao exista
            newLayer = True
            uvlayers = object.data.uv_layers
            lm = ""
            for layer in uvlayers:
                if (layer.name == uvLayerName):
                    newLayer = False
                    lm = layer
            if newLayer:
                lm = object.data.uv_layers.new(name=uvLayerName)
            lm.active = True
            # Ativa o modo de edição, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='EDIT')
            # bpy.ops.object.editmode_toggle()
            # Seleciona a geometria
            bpy.ops.mesh.select_all(action='SELECT')
            # Chama o Smart UV Projection com os parãmetros passados
            bpy.ops.uv.cube_project()
            # Ajusta o UV, Pack islands
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.pack_islands(margin=marg, rotate=False)
            # Sai do modo de ediçao, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='OBJECT')
            # bpy.ops.object.objectmode_toggle()
            # Desceleciona o objeto
            object.select_set(False)

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:
            try:
                if obj.type == 'MESH':
                    mesh = obj.data
                    polygons = mesh.polygons
                    if len(polygons) > 0:
                        # UnwrapUVProjection(obj, math.radians(66.0), 0.025, 'LightMap')
                        # UnwrapUVProjection(obj, math.radians(66.0), 0.0, 'UVMap')
                        CubeUVProjection(obj, 0.0, 'UVMap')
                        CubeUVProjection(obj, 0.025, 'LightMap')
            except Exception as e:
                print(obj.name)
                print(e)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class ButtonOperatorCleanMaterials(bpy.types.Operator):
    """Limpa os materiais dos elementos selecionados"""
    bl_idname = "uv.4"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - CLEAN MATERIAL ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto ativo
                bpy.context.view_layer.objects.active = obj
                ms = obj.data.materials
                for i in range(len(ms) - 1, 0, -1):
                    obj.active_material_index = i
                    bpy.ops.object.material_slot_remove()

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}

class ButtonOperatorCleanObjectUnusedMaterials(bpy.types.Operator):
    """Limpa os materiais não utilizados dos elementos selecionados"""
    bl_idname = "uv.10"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - CLEAN MATERIAL ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:
            if obj.type == 'MESH':
                # Define o objeto ativo
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.material_slot_remove_unused()

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}



class ButtonOperatorSelectNonPolygon(bpy.types.Operator):
    """Seleciona elementos que não contenham polígonos"""
    bl_idname = "select.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - SELECT NON POLYGONS ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Lista de objetos sem poligonos
        newSelection = []

        for obj in selection:
            try:
                if obj.type == 'MESH':
                    mesh = obj.data
                    polygons = mesh.polygons
                    if len(polygons) == 0:
                        newSelection.append(obj)

            except Exception as e:
                print(obj.name)
                print(e)

        if len(newSelection) > 0:
            print(len(newSelection))
            for obj in newSelection:
                obj.select_set(True)
        return {'FINISHED'}


class ButtonExportEchSelectedToFBX(bpy.types.Operator):
    """Exporta cada objeto selecionado para um arquivo FBX com o mesmo nome"""
    bl_idname = "export.2"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - EXPORT EACH SELECTED ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Loop sobre cada objeto da collection
        for obj in selection:
            obj.select_set(True)

            # export to FBX
            filepath = bpy.data.filepath
            directory = os.path.dirname(filepath)

            bpy.ops.export_scene.fbx(filepath=directory
                                     + '\\'
                                     + obj.name
                                     + '.fbx',
                                     axis_forward='Y',
                                     axis_up='Z',
                                     use_selection=True,
                                     object_types={'MESH'},
                                     mesh_smooth_type='FACE',
                                     bake_anim=False,
                                     embed_textures=False,
                                     use_custom_props=True)

            # deselect objects
            bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


class ButtoNOperatorBoundingBoxCube(bpy.types.Operator):
    """Cria um cubo a partir da BoundingBox dos elementos selecionados"""
    bl_idname = "generate.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - EXPORT EACH SELECTED ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pontos das BoundingBoxes globais
        bboxesPoints = []

        # Loop sobre cada objeto da collection
        for obj in selection:

            # Pega a matriz do objeto
            matrixWorld = obj.matrix_world

            # Pega a BoundingBox do objeto selecionado nas coordenadas locais
            bbox = obj.bound_box

            # Lista de BoundingBoxes globais
            worldBoxes = []

            # Itera sobre cada canto da BoundingBox
            for corner in bbox:

                # Multiplica as coordenadas do canto pela matriz
                worldCorner = matrixWorld @ mathutils.Vector(corner)

                # Adiciona as coordenadas globais para a lista de coordenadas
                bboxesPoints.append(worldCorner)

        minX = min([p[0] for p in bboxesPoints])
        minY = min([p[1] for p in bboxesPoints])
        minZ = min([p[2] for p in bboxesPoints])

        maxX = max([p[0] for p in bboxesPoints])
        maxY = max([p[1] for p in bboxesPoints])
        maxZ = max([p[2] for p in bboxesPoints])

        # Cria um cubo com o tamanho final
        bpy.ops.mesh.primitive_cube_add()

        # Cube é o novo objeto criado
        cube = bpy.context.selected_objects[0]
        cube.location = ((minX+maxX)/2, (minY+maxY)/2, (minZ+maxZ)/2)
        bpy.context.view_layer.update()
        cube.dimensions[0] = maxX-minX
        bpy.context.view_layer.update()
        cube.dimensions[1] = maxY-minY
        bpy.context.view_layer.update()
        cube.dimensions[2] = maxZ-minZ
        bpy.context.view_layer.update()

        return {'FINISHED'}


class ButtoNOperatorBoundingBoxCubeAndDelete(bpy.types.Operator):
    """Cria um cubo a partir da BoundingBox dos elementos selecionados e exclui os mesmos ao final"""
    bl_idname = "generate.2"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - EXPORT EACH SELECTED ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pontos das BoundingBoxes globais
        bboxesPoints = []

        # Loop sobre cada objeto da collection
        for obj in selection:

            # Pega a matriz do objeto
            matrixWorld = obj.matrix_world

            # Pega a BoundingBox do objeto selecionado nas coordenadas locais
            bbox = obj.bound_box

            # Lista de BoundingBoxes globais
            worldBoxes = []

            # Itera sobre cada canto da BoundingBox
            for corner in bbox:

                # Multiplica as coordenadas do canto pela matriz
                worldCorner = matrixWorld @ mathutils.Vector(corner)

                # Adiciona as coordenadas globais para a lista de coordenadas
                bboxesPoints.append(worldCorner)

        minX = min([p[0] for p in bboxesPoints])
        minY = min([p[1] for p in bboxesPoints])
        minZ = min([p[2] for p in bboxesPoints])

        maxX = max([p[0] for p in bboxesPoints])
        maxY = max([p[1] for p in bboxesPoints])
        maxZ = max([p[2] for p in bboxesPoints])

        # Cria um cubo com o tamanho final
        bpy.ops.mesh.primitive_cube_add()

        # Cube é o novo objeto criado
        cube = bpy.context.selected_objects[0]
        cube.location = ((minX+maxX)/2, (minY+maxY)/2, (minZ+maxZ)/2)
        bpy.context.view_layer.update()
        cube.dimensions[0] = maxX-minX
        bpy.context.view_layer.update()
        cube.dimensions[1] = maxY-minY
        bpy.context.view_layer.update()
        cube.dimensions[2] = maxZ-minZ
        bpy.context.view_layer.update()

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        bpy.ops.object.delete()

        return {'FINISHED'}


class ButtoNOperatorBoundingBoxCubeAndDeleteEach(bpy.types.Operator):
    """Cria um cubo a partir da BoundingBox dos elementos selecionados e exclui os mesmos ao final"""
    bl_idname = "generate.2"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - EXPORT EACH SELECTED ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Loop sobre cada objeto da collection
        for obj in selection:

            # Pontos da BoundingBox
            bboxesPoints = []

            # Pega a matriz do objeto
            matrixWorld = obj.matrix_world

            # Pega a BoundingBox do objeto selecionado nas coordenadas locais
            bbox = obj.bound_box

            # Lista de BoundingBoxes globais
            worldBoxes = []

            # Itera sobre cada canto da BoundingBox
            for corner in bbox:

                # Multiplica as coordenadas do canto pela matriz
                worldCorner = matrixWorld @ mathutils.Vector(corner)

                # Adiciona as coordenadas globais para a lista de coordenadas
                bboxesPoints.append(worldCorner)

            minX = min([p[0] for p in bboxesPoints])
            minY = min([p[1] for p in bboxesPoints])
            minZ = min([p[2] for p in bboxesPoints])

            maxX = max([p[0] for p in bboxesPoints])
            maxY = max([p[1] for p in bboxesPoints])
            maxZ = max([p[2] for p in bboxesPoints])

            # Cria um cubo com o tamanho final
            bpy.ops.mesh.primitive_cube_add()

            # Cube é o novo objeto criado
            cube = bpy.context.selected_objects[0]
            cube.location = ((minX+maxX)/2, (minY+maxY)/2, (minZ+maxZ)/2)
            bpy.context.view_layer.update()
            cube.dimensions[0] = maxX-minX
            bpy.context.view_layer.update()
            cube.dimensions[1] = maxY-minY
            bpy.context.view_layer.update()
            cube.dimensions[2] = maxZ-minZ
            bpy.context.view_layer.update()

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        bpy.ops.object.delete()

        return {'FINISHED'}


class ButtoNOperatorBoundingBoxCylinderAndDeleteEach(bpy.types.Operator):
    """Cria um cilindro a partir da BoundingBox dos elementos selecionados e exclui os mesmos ao final"""
    bl_idname = "generate.20"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - CYLINDER BOUNDING BOX ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Loop sobre cada objeto da collection
        for obj in selection:

            # Pontos da BoundingBox
            bboxesPoints = []

            # Pega a matriz do objeto
            matrixWorld = obj.matrix_world

            # Pega a BoundingBox do objeto selecionado nas coordenadas locais
            bbox = obj.bound_box

            # Lista de BoundingBoxes globais
            worldBoxes = []

            # Itera sobre cada canto da BoundingBox
            for corner in bbox:

                # Multiplica as coordenadas do canto pela matriz
                worldCorner = matrixWorld @ mathutils.Vector(corner)

                # Adiciona as coordenadas globais para a lista de coordenadas
                bboxesPoints.append(worldCorner)

            minX = min([p[0] for p in bboxesPoints])
            minY = min([p[1] for p in bboxesPoints])
            minZ = min([p[2] for p in bboxesPoints])

            maxX = max([p[0] for p in bboxesPoints])
            maxY = max([p[1] for p in bboxesPoints])
            maxZ = max([p[2] for p in bboxesPoints])

            # Cria um cubo com o tamanho final
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=24, 
                radius=(maxX-minX)/2, 
                depth=maxZ-minZ, 
                end_fill_type='TRIFAN', 
                calc_uvs=True, 
                enter_editmode=False, 
                align='WORLD', 
                location=((minX+maxX)/2, (minY+maxY)/2, (minZ+maxZ)/2), 
                rotation=(0.0, 0.0, 0.0), 
                scale=(1.0, 1.0, 1.0))

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # bpy.ops.object.delete()

        return {'FINISHED'}


class ButtoNOperatorConnectOuterEdges(bpy.types.Operator):
    """Conecta as arestas externas dos elementos selecionados"""
    bl_idname = "generate.3"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - EXPORT EACH SELECTED ----------')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        # Pega os vértices selecionados
        for v in obj.data.vertices:
            if v.select:
                v.select = True

        # Roda o comando "Select Boundary Loop"
        bpy.ops.mesh.region_to_loop()

        # Roda o comando "Bridge Edge loops"
        bpy.ops.mesh.bridge_edge_loops()

        return {'FINISHED'}


class ButtoNOperatorConnectOuterEdgesMany(bpy.types.Operator):
    """Conecta as arestas externas dos elementos selecionados"""
    bl_idname = "generate.4"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print(
            '---------- CÓDIGO INICIA AQUI - ButtoNOperatorConnectOuterEdgesMany ----------')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        # Pega os vértices selecionados
        for v in obj.data.vertices:
            if v.select:
                v.select = True

        # Roda o comando "Select Boundary Loop"
        bpy.ops.mesh.region_to_loop()

        # Roda o comando "Bridge Edge loops"
        bpy.ops.mesh.bridge_edge_loops()

        return {'FINISHED'}


class ButtonOperatorWorldSpaceUnwrapIndividual(bpy.types.Operator):

    """""SmartUnwrap os elementos selecionados com dimensão alterada"""
    bl_idname = "uv.5"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - SMARTUNWRAPUV TO UE ----------')

        def UnwrapUVProjection(object, angle, margin, uvLayerName):
            # Seleciona o objetos
            object.select_set(True)
            # Ativa o objeto
            bpy.context.view_layer.objects.active = object
            # Cria um novo UV Layer caso nao exista
            newLayer = True
            uvlayers = object.data.uv_layers
            lm = ""
            for layer in uvlayers:
                if (layer.name == uvLayerName):
                    newLayer = False
                    lm = layer
            if newLayer:
                lm = object.data.uv_layers.new(name=uvLayerName)
            lm.active = True
            # Ativa o modo de edição, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='EDIT')
            # bpy.ops.object.editmode_toggle()
            # Seleciona a geometria
            bpy.ops.mesh.select_all(action='SELECT')
            # Chama o Smart UV Projection com os parãmetros passados
            bpy.ops.uv.smart_project(
                angle_limit=math.radians(angle), island_margin=margin)
            # Ajusta o UV, Pack islands
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.pack_islands(margin=margin, rotate=False)
            # Aplica o WorldScaleUV do addon que já vem com o Blender MagicUV
            bpy.ops.uv.muv_world_scale_uv_apply_manual()
            # Sai do modo de ediçao, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='OBJECT')
            # bpy.ops.object.editmode_toggle()
            # Desceleciona o objeto
            object.select_set(False)

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:
            try:
                if obj.type == 'MESH':
                    mesh = obj.data
                    polygons = mesh.polygons
                    if len(polygons) > 0:
                        # UnwrapUVProjection(obj, math.radians(66.0), 0.025, 'LightMap')
                        UnwrapUVProjection(
                            obj, math.radians(66.0), 0.0, 'UVMap')
                        # CubeUVProjection(obj, 0.0, 'UVMap')
                        # CubeUVProjection(obj, 0.025, 'LightMap')
            except Exception as e:
                print(obj.name)
                print(e)

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class ButtonOperatorSDeffineTopOrigin(bpy.types.Operator):
    """Define a origem do elemento como sendo o centro superior"""
    bl_idname = "origin.2"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - DEFFINE BOTTOM ORIGIN ----------')

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
                    type='ORIGIN_GEOMETRY', center='MEDIAN')
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


class ButtonOperatorExportEdges(bpy.types.Operator):
    """Exporta as arestas de um mesh para uma lista de pontos iniciais e finais"""
    bl_idname = "export.3"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - EXPORT EDGES ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Lista das arestas
        arestas = []

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                mesh = obj.data
                for edge in mesh.edges:
                    vert1 = mesh.vertices[edge.vertices[0]]
                    vert2 = mesh.vertices[edge.vertices[1]]
                    arestas.append(
                        str(vert1.co[0])
                        + "\t" + str(vert1.co[1])
                        + "\t" + str(vert1.co[2])
                        + "\t" + str(vert2.co[0])
                        + "\t" + str(vert2.co[1])
                        + "\t" + str(vert2.co[2])
                    )

        # Transforma a lista em um texto separado por novas linhas
        texto = "\n".join(arestas)

        texto = texto.replace(".", ",")

        print(texto)

        # Copia o texto para a área de transferência
        bpy.context.window_manager.clipboard = texto

        # Restora a seleção
        for obj in selection:
            obj.select_set(True)

        # Restora o objeto ativo
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class ButtonOperatorSelectVisibleSharpenEdges(bpy.types.Operator):
    """Seleciona as arestas visíveis dos elementos"""
    bl_idname = "select.2"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - SELECT VISIBLE SHARPEN EDGES ----------')

        # Lista das arestas
        arestas = []

        # Para cada objeto selecionado
        select_border(bpy.context)

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        sharpEdges = []

        for edge in selection:
            if edge.use_sharp_edges == True:
                sharpEdges.append(edge)

        # Restora a seleção
        for obj in sharpEdges:
            obj.select_set(True)

        return {'FINISHED'}


class ButtonOperatorImportCAD(bpy.types.Operator):
    """Cria linhas com base na exportação do CAD"""
    bl_idname = "import.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - IMPORT CAD ----------')

        # Acessa os dados presentes na área de transfer~ncia
        clipboard = bpy.context.window_manager.clipboard

        # Deserializa o JSON
        cadObjects = json.loads(clipboard)

        # Para cada item
        for cadObj in cadObjects:
            # Pega o tipo da linha
            cadType = CadType(cadObj["CadType"])

            # Caso seja Linha
            if cadType == CadType.Line:
                line = cadObj["LineGeometry"]["Line"]
                pontoInicial = (line["StartPoint"]["XCoord"], line["StartPoint"]
                                ["YCoord"], line["StartPoint"]["ZCoord"])
                pontoFinal = (line["EndPoint"]["XCoord"], line["EndPoint"]
                              ["YCoord"], line["EndPoint"]["ZCoord"])
                linhaObj = CreateLine(pontoInicial, pontoFinal)
                SetOriginCenter(linhaObj)

            # Caso seja Arco
            if cadType == CadType.Arc:
                arc = cadObj["ArcGeometry"]["Arc"]
                raio = arc["Radius"]
                centro = (arc["Center"]["XCoord"], arc["Center"]
                          ["YCoord"], arc["Center"]["ZCoord"])
                pontoInicial = (arc["StartPoint"]["XCoord"], arc["StartPoint"]
                                ["YCoord"], arc["StartPoint"]["ZCoord"])
                pontoFinal = (arc["EndPoint"]["XCoord"], arc["EndPoint"]
                              ["YCoord"], arc["EndPoint"]["ZCoord"])
                arcObj = CreateArc(centro, raio, pontoInicial, pontoFinal)
                # SetOriginCenter(arcObj)

            # Caso seja PolyLinha
            if cadType == cadType.Polyline:
                curves = cadObj["PolylineGeometry"]["ListCurves"]
                for curve in curves:
                    if CurveType(curve["CurveType"]) == CurveType.Line:
                        pontoInicial = (curve["StartPoint"]["XCoord"], curve["StartPoint"]
                                        ["YCoord"], curve["StartPoint"]["ZCoord"])
                        pontoFinal = (curve["EndPoint"]["XCoord"], curve["EndPoint"]
                                      ["YCoord"], curve["EndPoint"]["ZCoord"])
                        linhaObj = CreateLine(pontoInicial, pontoFinal)
                    if CurveType(curve["CurveType"]) == CurveType.Arc:
                        raio = curve["Radius"]
                        centro = (curve["Center"]["XCoord"], curve["Center"]
                                  ["YCoord"], curve["Center"]["ZCoord"])
                        pontoInicial = (curve["StartPoint"]["XCoord"], curve["StartPoint"]
                                        ["YCoord"], curve["StartPoint"]["ZCoord"])
                        pontoFinal = (curve["EndPoint"]["XCoord"], curve["EndPoint"]
                                      ["YCoord"], curve["EndPoint"]["ZCoord"])
                        arcObj = CreateArc(
                            centro, raio, pontoInicial, pontoFinal)

        return {'FINISHED'}


class ButtonOperatorClarCustomProperties(bpy.types.Operator):
    """Limpa as Custom Properties dos objetos selecionados"""
    bl_idname = "props.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - CLEAR CUSTOM PROPERTIES ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Para cada objeto selecionado
        for obj in selection:
            for custom_prop_name in list(obj.keys()):
                print(custom_prop_name)
                del obj[custom_prop_name]

        return {'FINISHED'}


class ButtonOperatorAddCronoCustomProperties(bpy.types.Operator):
    """Adiciona as Custom Properties padrões do cronograma"""
    bl_idname = "props.2"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - ADD CRONO CUSTOM PROPERTIES ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Para cada objeto selecionado
        for obj in selection:
            obj["Element_AY_Tarefa"] = "Tarefa"
            obj["Element_AY_OrdemNaTarefa"] = 0
            obj["Element_AY_QuantidadeNaTarefa"] = 0

        return {'FINISHED'}


class ButtonOperatorCleanUnusedMaterials(bpy.types.Operator):
    """Limpa os materiais não utilizados"""
    bl_idname = "uv.6"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - CLEAN UNUSED MATERIALS ----------')

        # Lista contendo os objetos e materiais
        materiais = []
        objetos = []

        # Adiciona os materiais a lista
        for mat in bpy.data.materials:
            materiais.append(mat)

        # Adiciona os objetos a lista
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                objetos.append(obj)

        # Remove da lista de materiais os materiais presentes nos objetos
        for obj in objetos:
            for mat in obj.data.materials:
                if mat in materiais:
                    materiais.remove(mat)

        # Remove os materiais restantes na lista
        for mat in materiais:
            bpy.data.materials.remove(mat)

        return {'FINISHED'}


class ButtonOperatorJoinObjectsByCoordinates(bpy.types.Operator):
    """Une os objetos pela sua coordenada"""
    bl_idname = "modify.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - JOIN OBJECTS BY COORDINATES ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Lista contendo os objetos
        objetos = []

        # Adiciona os objetos a lista
        for obj in selection:
            if obj.type == 'MESH':
                objetos.append(obj)

        # Pega as coordenadas dos objetos
        coordenadasDosObjetos = []

        for obj in objetos:

            # Pega a matriz do objeto
            matrixWorld = obj.matrix_world

            # Pega a BoundingBox do objeto selecionado nas coordenadas locais
            bbox = obj.bound_box

            # Lista de BoundingBoxes globais
            pontos = []

            # Itera sobre cada canto da BoundingBox
            for corner in bbox:

                # Multiplica as coordenadas do canto pela matriz
                worldCorner = matrixWorld @ mathutils.Vector(corner)

                pontos.append(worldCorner)

            minX = min([p[0] for p in pontos])
            minY = min([p[1] for p in pontos])
            minZ = min([p[2] for p in pontos])

            maxX = max([p[0] for p in pontos])
            maxY = max([p[1] for p in pontos])
            maxZ = max([p[2] for p in pontos])

            coordenadasDosObjetos.append(
                [(minX+maxX)/2, (minY+maxY)/2, (minZ+maxZ)/2])

        # Agrupa de acordo com as coordenadas e uma tolerância
        grupos = AgruparPontosComTolerancia(coordenadasDosObjetos, 1, 0, False)

        print(grupos)
        # Planifica a lista

        return {'FINISHED'}


class ButtonExportEchSelectedCollectionToFBX(bpy.types.Operator):
    """Exporta cada Collection selecionada para um arquivo FBX com o mesmo nome"""
    bl_idname = "export.4"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - EXPORT EACH COLECTION ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects
        objetosPorColecao = {}

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Para cada objeto na seleção adicionar ao dicionario com a coleção como chave
        for obj in selection:
            # Percorre todas as collections às quais o objeto pertence
            for colecao in obj.users_collection:
                # Verifica se a collection já existe no dicionário
                if colecao.name in objetosPorColecao:
                    # Se a collection já existe, adiciona o objeto à lista de objetos
                    objetosPorColecao[colecao.name].append(obj)
                else:
                    # Se a collection não existe, cria uma nova lista com o objeto e adiciona ao dicionário
                    objetosPorColecao[colecao.name] = [obj]

        # Loop sobre cada objeto da collection
        for colecao, objetos in objetosPorColecao.items():
            for objeto in objetos:
                objeto.select_set(True)

            # export to FBX
            filepath = bpy.data.filepath
            directory = os.path.dirname(filepath)

            bpy.ops.export_scene.fbx(filepath=directory
                                     + '\\'
                                     + colecao
                                     + '.fbx',
                                     use_selection=True,
                                     object_types={'MESH'},
                                     mesh_smooth_type='FACE',
                                     bake_anim=False,
                                     embed_textures=False,
                                     use_custom_props=True)

            # deselect objects
            bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


class ButtonOperatorExportToClipboardFaceCenter(bpy.types.Operator):
    """Copia para a área de transferência as informações das faces dos elementos para ser cerem criados dentro da UE como referência"""
    bl_idname = "export.5"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - COPY TO CLIPBOARD FACE CENTER ----------')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        # String final
        finalString = ""

        finalString += "Begin Map"
        finalString += "\n    Begin Level"

        unitInfo = GetUnits()

        if obj.type == 'MESH':
            # Valores da posição do elemento
            faces = obj.data.polygons
            for i in range(len(faces)):

                face = faces[i]
                vertices = []
                for v in face.vertices:
                    vertices.append(obj.data.vertices[v].co)
                centro = sum(vertices, mathutils.Vector()) / len(vertices)

                # rotação em torno do eixo Z
                normal = face.normal
                angulo = normal.angle(mathutils.Vector((0, 1, 0)))
                anguloGraus = angulo * 180 / math.pi

                name = obj.name + str(i)
                locX = round(UnitToCentimeter(centro.x, unitInfo), 1)
                locY = -round(UnitToCentimeter(centro.y, unitInfo), 1)
                locZ = round(UnitToCentimeter(centro.z, unitInfo), 1)
                rotation = obj.rotation_euler
                rotX = 0
                rotY = 0
                rotZ = round(anguloGraus, 1)
                sclX = 1
                sclY = 1
                sclZ = 1
                # Cria a string a partir dos valores
                finalString += f"\n        Begin Actor Class=StaticMeshActor Name={name} Archetype=StaticMeshActor'/Script/Engine.Default__StaticMeshActor'"
                finalString += "\n            Begin Object Class=StaticMeshComponent Name=StaticMeshComponent0 ObjName=StaticMeshComponent0"
                finalString += "\n            Archetype=StaticMeshComponent'/Script/Engine.Default__StaticMeshActor:StaticMeshComponent0'"
                finalString += "\n            End Object"
                finalString += "\n            Begin Object Name=StaticMeshComponent0"
                finalString += f"\n                StaticMesh=StaticMesh'/Engine/BasicShapes/Cube.Cube'"
                finalString += f"\n                RelativeLocation=(X={locX},Y={locY},Z={locZ})"
                finalString += f"\n                RelativeScale3D=(X={sclX},Y={sclY},Z={sclZ})"
                finalString += f"\n                RelativeRotation=(Pitch={rotY},Yaw={rotZ},Roll={rotX})"
                finalString += "\n                CustomProperties"
                finalString += "\n            End Object"
                finalString += "\n            StaticMeshComponent=StaticMeshComponent0"
                finalString += "\n            Components(0)=StaticMeshComponent0"
                finalString += "\n            RootComponent=StaticMeshComponent0"
                finalString += f'\n            ActorLabel="{name}"'
                finalString += "\n        End Actor"

        finalString += "\n    End Level"
        finalString += "\nBegin Surface"
        finalString += "\nEnd Surface"
        finalString += "\nEnd Map"

        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = finalString

        return {'FINISHED'}


class ButtonOperatorDivideByAreaFace(bpy.types.Operator):
    """Divide um elemento pelo tamanho das faces"""
    bl_idname = "modify.3"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - DIVIDIR FACES ----------')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        # Tolerância da área
        tolerancia = 0.0001

        # Cria um dicionário vazio para guardar as coordenadas
        grupos = {}

        if obj.type == 'MESH':

            # Pega as faces do elemento
            faces = obj.data.polygons

            # Organiza as faces de acordo com sua área
            facesordenadas = sorted(faces, key=lambda f: f.area, reverse=False)

            for face in facesordenadas:
                # Checa se a área da face esta dentro da tolerância de algum grupo existente
                for grupoArea in grupos:
                    if abs(face.area - grupoArea) <= tolerancia:
                        # Se existir um grupo então adiciona a face a ele
                        grupos[grupoArea].append(face)
                        break
                else:
                    # Se não então criar um novo grupo
                    grupos[face.area] = [face]

        print(list(grupos.values()))

        return {'FINISHED'}


class ButtonOperatorConnectOuterEdgesBB(bpy.types.Operator):
    """Conecta as areas a partir de uma bounding box"""
    bl_idname = "generate.5"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print(
            '---------- CÓDIGO INICIA AQUI - ButtonOperatorConnectOuterEdgesBB ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:

            obj.select_set(True)

            # Pontos das BoundingBoxes globais
            bboxesPoints = []

            # Pega a matriz do objeto
            matrixWorld = obj.matrix_world

            # Pega a BoundingBox do objeto selecionado nas coordenadas locais
            bbox = obj.bound_box

            # Lista de BoundingBoxes globais
            worldBoxes = []

            # Itera sobre cada canto da BoundingBox
            for corner in bbox:

                # Multiplica as coordenadas do canto pela matriz
                worldCorner = matrixWorld @ mathutils.Vector(corner)

                # Adiciona as coordenadas globais para a lista de coordenadas
                bboxesPoints.append(worldCorner)

            minX = min([p[0] for p in bboxesPoints])
            minY = min([p[1] for p in bboxesPoints])
            minZ = min([p[2] for p in bboxesPoints])

            maxX = max([p[0] for p in bboxesPoints])
            maxY = max([p[1] for p in bboxesPoints])
            maxZ = max([p[2] for p in bboxesPoints])

            dimX = maxX-minX
            dimY = maxY-minY
            dimZ = maxZ-minZ

            direcao = mathutils.Vector((1, 0, 0))
            direcaoEixo = 0

            if dimX >= dimY and dimX >= dimZ:
                direcao = mathutils.Vector((1, 0, 0))
                direcaoEixo = 0
            if dimY >= dimX and dimY >= dimZ:
                direcao = mathutils.Vector((0, 1, 0))
                direcaoEixo = 1
            if dimZ >= dimX and dimZ >= dimY:
                direcao = mathutils.Vector((0, 0, 1))
                direcaoEixo = 2

            # Cria um bmesh
            mesh = obj.data
            bm = bmesh.new()
            bm.from_mesh(mesh)

            # Seleciona as faces pela sua normal
            facesManter = []
            facesDelete = []

            for face in bm.faces:
                if face.normal == direcao or face.normal == direcao * -1:
                    facesManter.append(face)
                else:
                    facesDelete.append(face)

            # Filtra apenas as faces mais distantes
            tolerancia = 0.001
            facesAgrupadas = AgruparFacesComTolerancia(
                facesManter, tolerancia, direcaoEixo, False)

            # Remove o primeiro e último grupos
            facesAgrupadasDelete = facesAgrupadas[1:-1]

            facesDelete += facesAgrupadasDelete

            facesDelete = PlanificarLista(facesDelete)

            # Deleta as faces
            bmesh.ops.delete(bm, geom=facesDelete, context='FACES')

            # Atualiza o mesh
            bm.to_mesh(mesh)
            mesh.update()

            # Ativa o modo de edição, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='EDIT')

            # Seleciona a geometria
            bpy.ops.mesh.select_all(action='SELECT')

            # Roda o comando "Select Boundary Loop"
            bpy.ops.mesh.region_to_loop()

            # Roda o comando "Bridge Edge loops"
            bpy.ops.mesh.bridge_edge_loops()

            # Sai do modo de ediçao, ambos métodos funcionam
            bpy.ops.object.mode_set(mode='OBJECT')

            # Desseleciona todos os objetos
            bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}


class ButtonOperatorExportSelectedVertex(bpy.types.Operator):
    """Copia para a área de transferência as informações das faces dos elementos para ser cerem criados dentro da UE como referência"""
    bl_idname = "export.6"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - COPY TO CLIPBOARD FACE CENTER ----------')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        # String final
        finalString = ""

        finalString += "Begin Map"
        finalString += "\n    Begin Level"

        unitInfo = GetUnits()

        # Matriz de transformações do elemento
        matrix = obj.matrix_world

        # Sai do modo de ediçao, ambos métodos funcionam
        bpy.ops.object.mode_set(mode='OBJECT')

        if obj.type == 'MESH':
            # Para pegar o mesh após modificadores
            depsgraph = bpy.context.evaluated_depsgraph_get()
            bm = bmesh.new()
            bm.from_object(obj, depsgraph)
            bm.verts.ensure_lookup_table()

            # Pega os vértices selecionados
            for i in range(len(bm.verts)):
                v = bm.verts[i]
                if v.select:
                    name = obj.name + str(i)
                    locX = round(UnitToCentimeter(
                        (matrix @ v.co).x, unitInfo), 1)
                    locY = - \
                        round(UnitToCentimeter((matrix @ v.co).y, unitInfo), 1)
                    locZ = round(UnitToCentimeter(
                        (matrix @ v.co).z, unitInfo), 1)
                    rotX = 0
                    rotY = 0
                    rotZ = 0
                    sclX = 1
                    sclY = 1
                    sclZ = 1

                    # Cria a string a partir dos valores
                    finalString += f"\n        Begin Actor Class=StaticMeshActor Name={name} Archetype=StaticMeshActor'/Script/Engine.Default__StaticMeshActor'"
                    finalString += "\n            Begin Object Class=StaticMeshComponent Name=StaticMeshComponent0 ObjName=StaticMeshComponent0"
                    finalString += "\n            Archetype=StaticMeshComponent'/Script/Engine.Default__StaticMeshActor:StaticMeshComponent0'"
                    finalString += "\n            End Object"
                    finalString += "\n            Begin Object Name=StaticMeshComponent0"
                    finalString += f"\n                StaticMesh=StaticMesh'/Engine/BasicShapes/Cube.Cube'"
                    finalString += f"\n                RelativeLocation=(X={locX},Y={locY},Z={locZ})"
                    finalString += f"\n                RelativeScale3D=(X={sclX},Y={sclY},Z={sclZ})"
                    finalString += f"\n                RelativeRotation=(Pitch={rotY},Yaw={rotZ},Roll={rotX})"
                    finalString += "\n                CustomProperties"
                    finalString += "\n            End Object"
                    finalString += "\n            StaticMeshComponent=StaticMeshComponent0"
                    finalString += "\n            Components(0)=StaticMeshComponent0"
                    finalString += "\n            RootComponent=StaticMeshComponent0"
                    finalString += f'\n            ActorLabel="{name}"'
                    finalString += "\n        End Actor"

        finalString += "\n    End Level"
        finalString += "\nBegin Surface"
        finalString += "\nEnd Surface"
        finalString += "\nEnd Map"

        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = finalString

        # Ativa o modo de edição, ambos métodos funcionam
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


class ButtonOperatorUnwrapCylinder(bpy.types.Operator):
    """Unwrap um cilindro"""
    bl_idname = "export.6"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - UNWRAP CYLINDER ----------')

        # Ativa o modo de objeto
        bpy.ops.object.mode_set(mode='OBJECT')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Desleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Para cada objeto selecionado
        for obj in selection:

            if obj.type == 'MESH':

                # Retorna a seleção para o objeto
                obj.select_set(True)

                # Pega o mesh
                mesh = obj.data

                # Ativa o modo de edição
                bpy.ops.object.mode_set(mode='EDIT')

                # Remove a seleção
                bpy.ops.mesh.select_all(action='DESELECT')

                # Ativa o modo de objeto
                bpy.ops.object.mode_set(mode='OBJECT')

                # Seleciona as faces inferiores e superiores
                eixoZ = mathutils.Vector((0, 0, 1))
                for face in mesh.polygons:
                    print(face.normal)
                    if face.normal.z == 1 or face.normal.z == -1:
                        face.select = True

                # Roda o comando "Select Boundary Loop"
                # Ativa o modo de edição
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.region_to_loop()

                # Ativa o modo de objeto
                bpy.ops.object.mode_set(mode='OBJECT')

                # Cria a lista de EDGES a serem marcadas
                edges = []

                for edge in mesh.edges:
                    if edge.select == True:
                        edges.append(edge)

                for edge in mesh.edges:
                    vert1 = mesh.vertices[edge.vertices[0]]
                    vert2 = mesh.vertices[edge.vertices[1]]
                    direcao = (vert2.co - vert1.co).normalized()
                    # print(f'Direção= {direcao}')
                    # Caso o produto cruzado for zero então é paralelo ao eixo Z
                    if direcao.cross(eixoZ).length == 0.0:
                        edge.use_seam = True
                        edges.append(edge)
                        break

                # Marca a SEAM do UV
                for edge in mesh.edges:
                    if edge.select == True:
                        edge.use_seam = True

                # Ativa o modo de edição
                bpy.ops.object.mode_set(mode='EDIT')
                # Adiciona a seleção
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0)
                # Ativa o modo de objeto
                bpy.ops.object.mode_set(mode='OBJECT')

                # Desleciona todos os objetos
                bpy.ops.object.select_all(action='DESELECT')

        # Ativa o modo de objeto
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}


class ButtonOperatorExportObjectCenter(bpy.types.Operator):
    """Copia para a área de transferência a locação central dos elementos para ser serem criados dentro da UE como referência"""
    bl_idname = "exportobjectcenter.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - ButtonOperatorExportObjectCenter ----------')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # String final
        finalString = ""

        finalString += "Begin Map"
        finalString += "\n    Begin Level"

        unitInfo = GetUnits()

        for i in range(len(selection)):

            obj = selection[i]

            # Pontos das BoundingBoxes globais
            bboxesPoints = []

            # Pega a matriz do objeto
            matrixWorld = obj.matrix_world

            # Pega a BoundingBox do objeto selecionado nas coordenadas locais
            bbox = obj.bound_box

            # Itera sobre cada canto da BoundingBox
            for corner in bbox:

                # Multiplica as coordenadas do canto pela matriz
                worldCorner = matrixWorld @ mathutils.Vector(corner)

                # Adiciona as coordenadas globais para a lista de coordenadas
                bboxesPoints.append(worldCorner)

            minX = min([p[0] for p in bboxesPoints])
            minY = min([p[1] for p in bboxesPoints])
            minZ = min([p[2] for p in bboxesPoints])

            maxX = max([p[0] for p in bboxesPoints])
            maxY = max([p[1] for p in bboxesPoints])
            maxZ = max([p[2] for p in bboxesPoints])

            print(minX)
            print(maxX)

            centro = mathutils.Vector(
                [(minX+maxX)/2, (minY+maxY)/2, (minZ+maxZ)/2])

            name = obj.name + str(i)
            locX = round(UnitToCentimeter(centro.x, unitInfo), 1)
            locY = -round(UnitToCentimeter(centro.y, unitInfo), 1)
            locZ = round(UnitToCentimeter(centro.z, unitInfo), 1)
            rotation = obj.rotation_euler
            rotX = rotation.x * 180 / math.pi
            rotY = rotation.y * 180 / math.pi
            rotZ = rotation.z * 180 / math.pi
            sclX = 1
            sclY = 1
            sclZ = 1
            # Cria a string a partir dos valores
            finalString += f"\n        Begin Actor Class=StaticMeshActor Name={name} Archetype=StaticMeshActor'/Script/Engine.Default__StaticMeshActor'"
            finalString += "\n            Begin Object Class=StaticMeshComponent Name=StaticMeshComponent0 ObjName=StaticMeshComponent0"
            finalString += "\n            Archetype=StaticMeshComponent'/Script/Engine.Default__StaticMeshActor:StaticMeshComponent0'"
            finalString += "\n            End Object"
            finalString += "\n            Begin Object Name=StaticMeshComponent0"
            finalString += f"\n                StaticMesh=StaticMesh'/Engine/BasicShapes/Cube.Cube'"
            finalString += f"\n                RelativeLocation=(X={locX},Y={locY},Z={locZ})"
            finalString += f"\n                RelativeScale3D=(X={sclX},Y={sclY},Z={sclZ})"
            finalString += f"\n                RelativeRotation=(Pitch={rotY},Yaw={rotZ},Roll={rotX})"
            finalString += "\n                CustomProperties"
            finalString += "\n            End Object"
            finalString += "\n            StaticMeshComponent=StaticMeshComponent0"
            finalString += "\n            Components(0)=StaticMeshComponent0"
            finalString += "\n            RootComponent=StaticMeshComponent0"
            finalString += f'\n            ActorLabel="{name}"'
            finalString += "\n        End Actor"

        finalString += "\n    End Level"
        finalString += "\nBegin Surface"
        finalString += "\nEnd Surface"
        finalString += "\nEnd Map"

        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = finalString

        return {'FINISHED'}


class ButtonOperatorExportObjectOrigin(bpy.types.Operator):
    """Copia para a área de transferência a locação da origem dos elementos para ser serem criados dentro da UE como referência"""
    bl_idname = "exportobjectorigin.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - ButtonOperatorExportObjectCenter ----------')

        # Pega o objeto ativo
        obj = bpy.context.active_object

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # String final
        finalString = ""

        finalString += "Begin Map"
        finalString += "\n    Begin Level"

        unitInfo = GetUnits()

        for i in range(len(selection)):

            obj = selection[i]

            centro = obj.location

            name = obj.name + str(i)
            locX = round(UnitToCentimeter(centro.x, unitInfo), 1)
            locY = -round(UnitToCentimeter(centro.y, unitInfo), 1)
            locZ = round(UnitToCentimeter(centro.z, unitInfo), 1)
            rotation = obj.rotation_euler
            rotX = rotation.x * 180 / math.pi
            rotY = rotation.y * 180 / math.pi
            rotZ = rotation.z * 180 / math.pi
            sclX = 1
            sclY = 1
            sclZ = 1
            # Cria a string a partir dos valores
            finalString += f"\n        Begin Actor Class=StaticMeshActor Name={name} Archetype=StaticMeshActor'/Script/Engine.Default__StaticMeshActor'"
            finalString += "\n            Begin Object Class=StaticMeshComponent Name=StaticMeshComponent0 ObjName=StaticMeshComponent0"
            finalString += "\n            Archetype=StaticMeshComponent'/Script/Engine.Default__StaticMeshActor:StaticMeshComponent0'"
            finalString += "\n            End Object"
            finalString += "\n            Begin Object Name=StaticMeshComponent0"
            finalString += f"\n                StaticMesh=StaticMesh'/Engine/BasicShapes/Cube.Cube'"
            finalString += f"\n                RelativeLocation=(X={locX},Y={locY},Z={locZ})"
            finalString += f"\n                RelativeScale3D=(X={sclX},Y={sclY},Z={sclZ})"
            finalString += f"\n                RelativeRotation=(Pitch={rotY},Yaw={rotZ},Roll={rotX})"
            finalString += "\n                CustomProperties"
            finalString += "\n            End Object"
            finalString += "\n            StaticMeshComponent=StaticMeshComponent0"
            finalString += "\n            Components(0)=StaticMeshComponent0"
            finalString += "\n            RootComponent=StaticMeshComponent0"
            finalString += f'\n            ActorLabel="{name}"'
            finalString += "\n        End Actor"

        finalString += "\n    End Level"
        finalString += "\nBegin Surface"
        finalString += "\nEnd Surface"
        finalString += "\nEnd Map"

        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = finalString

        return {'FINISHED'}



class CustomPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "UETools Panel"
    bl_idname = "OBJECT_PT_UETOOLS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UE Tools"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator(ButtonOperatorShadeNormal.bl_idname,
                     text="Corrigir Shade e Normal", icon='NODE_MATERIAL')
        row = layout.row()
        row.operator(ButtonOperatorSDeffineBottomOrigin.bl_idname,
                     text="Alterar origem para centro e inferior", icon='EMPTY_AXIS')
        row = layout.row()
        row.operator(ButtonOperatorSDeffineTopOrigin.bl_idname,
                     text="Alterar origem para centro e superior", icon='EMPTY_AXIS')
        row = layout.row()
        row.operator(ButtonOperatorExportToClipboard.bl_idname,
                     text="Copiar coordenadas dos elementos", icon='WINDOW')
        row = layout.row()
        row.operator(ButtonOperatorUnwrapElementsToUE.bl_idname,
                     text="CubeUnwrapUV para cada elemento", icon='UV_DATA')
        row = layout.row()
        row.operator(ButtonOperatorViewUnwrapIndividual.bl_idname,
                     text="SmartUnwrapUV para cada objeto", icon='UV_DATA')
        row = layout.row()
        row.operator(ButtonOperatorWorldSpaceUnwrapIndividual.bl_idname,
                     text="SmartUnwrapUV e corrigir tamanho", icon='UV_DATA')
        row = layout.row()
        row.operator(ButtonOperatorCleanMaterials.bl_idname,
                     text="Limpar materiais", icon='TRASH')
        row = layout.row()
        row.operator(ButtonOperatorCleanObjectUnusedMaterials.bl_idname,
                     text="Limpar materiais não usados", icon='TRASH')
        row = layout.row()
        row.operator(ButtonOperatorCleanUVChannels.bl_idname,
                     text="Limpar UVChannels", icon='TRASH')
        row = layout.row()
        row.operator(ButtonOperatorSelectNonPolygon.bl_idname,
                     text="Selecionar não polígonos", icon='OUTLINER_DATA_CURVE')
        row = layout.row()
        row.operator(ButtonExportEchSelectedToFBX.bl_idname,
                     text="Exportar cada objeto para FBX", icon='EXPORT')
        row = layout.row()
        row.operator(ButtonExportEchSelectedCollectionToFBX.bl_idname,
                     text="Exportar cada collection para FBX", icon='EXPORT')
        row = layout.row()
        row.operator(ButtoNOperatorBoundingBoxCube.bl_idname,
                     text="Cubo a partir da BoundingBox ", icon='CUBE')
        row = layout.row()
        row.operator(ButtoNOperatorBoundingBoxCubeAndDelete.bl_idname,
                     text="Cubo a partir da BoundingBox e excluir", icon='CUBE')
        row = layout.row()
        row.operator(ButtoNOperatorBoundingBoxCubeAndDeleteEach.bl_idname,
                     text="Cubos a partir da BoundingBox e excluir", icon='CUBE')
        row = layout.row()
        row.operator(ButtoNOperatorBoundingBoxCylinderAndDeleteEach.bl_idname,
                     text="BoundingBox > Cilindros", icon='MESH_CYLINDER')
        row = layout.row()
        row.operator(ButtoNOperatorConnectOuterEdges.bl_idname,
                     text="Conectar arestas exteriores", icon='META_CAPSULE')
        row = layout.row()
        row.operator(ButtonOperatorConnectOuterEdgesBB.bl_idname,
                     text="Conectar arestas +", icon='META_CAPSULE')
        row = layout.row()
        row.operator(ButtonOperatorExportEdges.bl_idname,
                     text="Exportar arestas", icon='MESH_DATA')
        row = layout.row()
        row.operator(ButtonOperatorImportCAD.bl_idname,
                     text="Importar CAD", icon='MESH_GRID')
        row = layout.row()
        row.operator(ButtonOperatorClarCustomProperties.bl_idname,
                     text="Limpar custom properties", icon='PRESET')
        row = layout.row()
        row.operator(ButtonOperatorAddCronoCustomProperties.bl_idname,
                     text="Criar crono properties", icon='PRESET')
        row = layout.row()
        row.operator(ButtonOperatorCleanUnusedMaterials.bl_idname,
                     text="Limpar materiais não utilizados", icon='MATERIAL')
        row = layout.row()
        row.operator(ButtonOperatorExportToClipboardFaceCenter.bl_idname,
                     text="Exportar centro faces", icon='WINDOW')
        row.operator(ButtonOperatorExportSelectedVertex.bl_idname,
                     text="Exportar vértices selecionados", icon='WINDOW')
        row = layout.row()
        row.operator(ButtonOperatorExportObjectCenter.bl_idname,
                     text="Exportar centro objetos", icon='WINDOW')
        row = layout.row()
        row.operator(ButtonOperatorExportObjectOrigin.bl_idname,
                     text="Exportar origem objetos", icon='WINDOW')
        row = layout.row()
        row.operator(ButtonOperatorUnwrapCylinder.bl_idname,
                     text="Unwrap cilindro", icon='MESH_CYLINDER')


_classes = [
    ButtonOperatorShadeNormal,
    ButtonOperatorSDeffineBottomOrigin,
    ButtonOperatorSDeffineTopOrigin,
    ButtonOperatorExportToClipboard,
    ButtonOperatorViewUnwrapIndividual,
    ButtonOperatorWorldSpaceUnwrapIndividual,
    ButtonOperatorUnwrapElementsToUE,
    ButtonOperatorCleanMaterials,
    ButtonOperatorCleanObjectUnusedMaterials,
    ButtonOperatorCleanUVChannels,
    ButtonOperatorSelectNonPolygon,
    ButtonExportEchSelectedToFBX,
    ButtonExportEchSelectedCollectionToFBX,
    ButtoNOperatorBoundingBoxCube,
    ButtoNOperatorBoundingBoxCubeAndDelete,
    ButtoNOperatorBoundingBoxCubeAndDeleteEach,
    ButtoNOperatorBoundingBoxCylinderAndDeleteEach,
    ButtoNOperatorConnectOuterEdges,
    ButtonOperatorConnectOuterEdgesBB,
    ButtonOperatorExportEdges,
    ButtonOperatorImportCAD,
    ButtonOperatorClarCustomProperties,
    ButtonOperatorAddCronoCustomProperties,
    ButtonOperatorCleanUnusedMaterials,
    ButtonOperatorExportToClipboardFaceCenter,
    ButtonOperatorExportSelectedVertex,
    ButtonOperatorUnwrapCylinder,
    ButtonOperatorExportObjectCenter,
    ButtonOperatorExportObjectOrigin,
    CustomPanel]


def CreateArc(centro, raio, pontoInicial, pontoFinal):

    # Calcula o ângulos iniciais e finais do arco
    # Calcule os vetores do centro para o início e fim do arco em 3D
    vetor_inicio = (
        pontoInicial[0]-centro[0], pontoInicial[1]-centro[1], pontoInicial[2]-centro[2])
    vetor_fim = (pontoFinal[0]-centro[0], pontoFinal[1] -
                 centro[1], pontoFinal[2]-centro[2])

    # Calcule os ângulos iniciais e finais do arco em 3D usando a tangente inversa
    angulo_inicial = math.atan2(vetor_inicio[1], vetor_inicio[0])
    angulo_final = math.atan2(vetor_fim[1], vetor_fim[0])

    # Normalize os ângulos para o intervalo [0, 2*pi)
    angulo_inicial = (angulo_inicial + 2*math.pi) % (2*math.pi)
    angulo_final = (angulo_final + 2*math.pi) % (2*math.pi)

    print(angulo_inicial)
    print(angulo_final)

    # Verifique se o arco está "invertido" (ângulo inicial > ângulo final)
    if angulo_inicial > angulo_final:
        angulo_inicial -= 2*math.pi
        # angulo_final += 2*math.pi

    print(angulo_inicial)
    print(angulo_final)

    # Cria um objeto a partir da linha
    arcoObj = bpy.ops.curve.simple(
        Simple_Type='Arc',
        Simple_radius=raio,
        location=centro,
        Simple_startangle=math.degrees(angulo_inicial),
        Simple_endangle=math.degrees(angulo_final),
        Simple_sides=4,
        outputType='BEZIER',
        use_cyclic_u=False
    )

    # Sai do modo de edição se não os arcos são criados juntos
    bpy.ops.object.editmode_toggle()

    # Retorna a linha
    return arcoObj


def CreateLine(pontoInicial, pontoFinal):

    # Cria a linha
    curveData = bpy.data.curves.new(name="Line", type="CURVE")
    curveData.dimensions = '3D'
    curveData.resolution_u = 2

    polyline = curveData.splines.new('POLY')
    polyline.points.add(1)
    polyline.points[0].co = (
        pontoInicial[0], pontoInicial[1], pontoInicial[2], 1)
    polyline.points[1].co = (
        pontoFinal[0], pontoFinal[1], pontoFinal[2], 1)

    # Cria um objeto a partir da linha
    linhaObj = bpy.data.objects.new("Line", curveData)

    # Adiciona o objeto a cena
    bpy.context.collection.objects.link(linhaObj)

    # Retorna a linha
    return linhaObj


def SetOrigin(object, ponto):

    # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
    bpy.context.view_layer.objects.active = object
    object.select_set(True)

    # Define o cursor para a localização do primeiro ponto
    cursor = bpy.context.scene.cursor
    cursorLoc = mathutils.Vector(cursor.location)
    cursor.location = ponto

    # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
    bpy.context.view_layer.objects.active = object
    object.select_set(True)

    # Define a origem para o cursor
    bpy.ops.object.origin_set(
        type='ORIGIN_CURSOR', center='MEDIAN')
    # Reseta o cursor para a posição original
    cursor.location = cursorLoc

    # Desseleciona o objeto
    object.select_set(False)


def SetOriginCenter(object):

    # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
    bpy.context.view_layer.objects.active = object
    object.select_set(True)

    # Define o objeto como ativo e seleciona o mesmo para poder alterar sua origem
    bpy.context.view_layer.objects.active = object
    object.select_set(True)

    # Define a origem para o cursor
    bpy.ops.object.origin_set(
        type='ORIGIN_GEOMETRY', center='MEDIAN')

    # Desseleciona o objeto
    object.select_set(False)


""" def CreateArc(pontoInicial, pontoFinal, pontoMedio):

    # Cria o arco
    curveData = bpy.data.curves.new(name="Arc", type="CURVE")
    curveData.dimensions = '3D'

    # Cria uma spline e adiciona dois pontos
    spline = curveData.splines.new("NURBS")
    spline.points.add(2)

    # Define o ponto inicial e final da spline
    spline.points[0].co = (
        pontoInicial[0], pontoInicial[1], pontoInicial[2], 1)
    spline.points[1].co = (pontoFinal[0], pontoFinal[1], pontoFinal[2], 1)

    # Cria um bmesh para manipular os pontos de controle das curvas
    bm = bmesh.new()
    bm.verts.new(pontoMedio)

    # Define o ponto do meio como controle
    spline.points[0].handle_right = bm.verts[0].co
    spline.points[1].handle_left = bm.verts[0].co

    # Finaliza e limpa o bmesh
    bm.to_mesh(curveData.splines[0].points[0].co)
    bm.free()

    # Cria um objeto para guardar a curva e adiciona a cena
    arcObj = bpy.data.objects.new("Arc", curveData)
    bpy.context.collection.objects.link(arcObj)
 """


def CreatePolyLine(pontos):

    # Cria a Polylinha
    curveData = bpy.data.curves.new(name="PolyLine", type="CURVE")
    curveData.dimensions = '3D'
    curveData.resolution_u = 2

    polyline = curveData.splines.new('POLY')

    polyline.points.add(len(pontos)-1)

    for i in range(len(pontos)):
        ponto = pontos[i]
        polyline.points[i].co = (ponto[0], ponto[1], ponto[2], 1)

    # for point in pontos:
    #    print(point)
    #    polyline.points.add(1)
    #    polyline.points[-1].co = (point[0], point[1], point[2],1)

    # Fecha a Polylinha
    polyline.use_endpoint_u = True
    polyline.use_cyclic_u = True

    # Cria um objeto a partir da linha
    linhaObj = bpy.data.objects.new("PolyLine", curveData)

    # Adiciona o objeto a cena
    bpy.context.collection.objects.link(linhaObj)

    # Retorna a linha
    return linhaObj


def getView3dAreaAndRegion(context):
    for area in context.screen.areas:
        if area.type == "VIEW_3D":
            for region in area.regions:
                if region.type == "WINDOW":
                    print("Found WINDOW")
                    return area, region


def select_border(context, view3dAreaAndRegion=None, extend=True):
    if not view3dAreaAndRegion:
        view3dAreaAndRegion = getView3dAreaAndRegion(context)
        print(view3dAreaAndRegion)
    view3dArea, view3dRegion = view3dAreaAndRegion
    override = context.copy()
    override['area'] = view3dArea
    override['region'] = view3dRegion
    bpy.ops.view3d.select_box(
        override, xmin=0, xmax=view3dArea.width, ymin=0, ymax=view3dArea.height, mode='ADD')


def AgruparEOrdenarPontosEmDuasCoordenadasComTolerancia(pontos, toleranciaA, toleranciaB, coordenadaA=0, coordenadaB=1, inverterA=False, inverterB=False):

    print(toleranciaA)
    print(toleranciaB)
    print(coordenadaA)
    print(coordenadaB)
    print(inverterA)
    print(inverterB)

    gruposDePontos = AgruparPontosComTolerancia(
        pontos, toleranciaA, coordenadaA, inverterA)

    gruposOrdenados = []

    for grupo in gruposDePontos:
        gruposOrdenados.append(OrdenarPontos(grupo, coordenadaB, inverterB))

    return gruposOrdenados


def AgruparPontosComTolerancia(pontos, tolerancia, coordenada=0, inverter=False):
    # print("AgruparPontosComTolerancia")

    # Cria um dicionário vazio para guardar as coordenadas
    grupos = {}

    # Ordena a lista
    pontos = OrdenarPontos(pontos, coordenada, inverter)

    # Itera sobre a lista de pontos
    for ponto in pontos:
        # Checa se a coordenada do ponto esta dentro da tolerância de algum grupo existente
        for grupoCoordenada in grupos:
            if abs(ponto[coordenada] - grupoCoordenada) <= tolerancia:
                # Se existir um grupo então adiciona o ponto a ele
                grupos[grupoCoordenada].append(ponto)
                break
        else:
            # Se não então criar um novo grupo
            grupos[ponto[coordenada]] = [ponto]

    # Retorna a lista de grupos ordenados
    return list(grupos.values())


def AgruparFacesComTolerancia(faces, tolerancia, coordenada=0, inverter=False):
    # print("AgruparPontosComTolerancia")

    # Cria um dicionário vazio para guardar as coordenadas
    grupos = {}

    # Ordena a lista
    facesordenadas = OrdenarFaces(faces, coordenada, inverter)

    # Itera sobre a lista de pontos
    for face in facesordenadas:
        # Checa se a coordenada do ponto esta dentro da tolerância de algum grupo existente
        for grupoCoordenada in grupos:
            if abs(face.calc_center_median()[coordenada] - grupoCoordenada) <= tolerancia:
                # Se existir um grupo então adiciona o ponto a ele
                grupos[grupoCoordenada].append(face)
                break
        else:
            # Se não então criar um novo grupo
            grupos[face.calc_center_median()[coordenada]] = [face]

    # Retorna a lista de grupos ordenados
    return list(grupos.values())


def OrdenarPontos(pontos, coordenada, inverter=False):
    # Organiza os pontos pela coordenada escolhida em ordem crescente ou decrescente
    pontosOrdenados = sorted(
        pontos, key=lambda p: p[coordenada], reverse=inverter)

    # Retorna os pontos ordenados
    return pontosOrdenados


def OrdenarFaces(faces, coordenada, inverter=False):
    # Organiza as faces pela coordenada escolhida em ordem crescente ou decrescente
    facesOrdenadas = sorted(faces, key=lambda f: f.calc_center_median()[
                            coordenada], reverse=inverter)

    # Retorna os pontos ordenados
    return facesOrdenadas


def PlanificarLista(lista):
    resultado = []
    for elemento in lista:
        if type(elemento) == list:
            resultado.extend(PlanificarLista(elemento))
        else:
            resultado.append(elemento)
    return resultado


def PlanificarListaDePontos(pontos):

    listaPlanificada = PlanificarLista(pontos)

    subListas = []

    for i in range(0, len(listaPlanificada), 3):
        subLista = listaPlanificada[i:i+3]
        subListas.append(subLista)

    return subListas


def GetUnits():
    lengthUnits = bpy.context.scene.unit_settings.system
    if lengthUnits == 'KILOMETERS':
        return (1000)
    if lengthUnits == 'METERS':
        return (1)
    if lengthUnits == 'CENTIMETERS':
        return (1/100)
    if lengthUnits == 'MILLIMETERS':
        return (1/1000)
    if lengthUnits == 'MICROMETERS':
        return (1/1000000)
    if lengthUnits == 'MILES':
        return (1760)
    if lengthUnits == 'FEET':
        return (1/3)
    if lengthUnits == 'INCHES':
        return (1/36)
    if lengthUnits == 'THOU':
        return (1/36000)
    else:
        return (1)


def BuToUnit(value, scale):
    return value / scale


def UnitToBu(value, scale):
    return value / scale


def UnitToCentimeter(value, scale):
    return value/scale*100


def register():
    for cls in _classes:
        register_class(cls)


def unregister():
    for cls in _classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()
