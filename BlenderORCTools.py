from bpy.utils import register_class, unregister_class
from bpy.types import (Operator, Panel, Menu, PropertyGroup)
from bpy.props import (StringProperty,BoolProperty,IntProperty,FloatProperty,FloatVectorProperty, EnumProperty,PointerProperty,)
import math
import bpy
import mathutils
from mathutils import Vector
import os
import bmesh
import json
import enum


bl_info = {
    "name": "ORC Tools",
    "author": "Winderson Soares Matos",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N",
    "description": "Ferramentas para orçamento",
    "warning": "",
    "doc_url": "",
    "category": "",
}


class MyProperties(PropertyGroup):
    dimensionProperty: FloatProperty(name="Valor:",description="O valor da dimensão", default=100)

# region BOTÕES

class ButtonOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "potato.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        print('Potato')
        return {'FINISHED'}

# region BOTÕES LEVANTAMENTO
    
class BOCalcularAreaPorMaterial(bpy.types.Operator):
    """Calcula a área total dos materiais aplicados nos objetos"""
    bl_idname = "calcarea.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOCalcularAreaPorMaterial ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Dicionário para armazenar as áreas de cada material
        materialArea = {}


        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                
                # Matriz de transformações do objeto
                matrix = obj.matrix_world
                
                # Obtém o Mesh do objeto levando em consideração a escala
                mesh = obj.data

                # Para pegar o mesh após modificadores
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm = bmesh.new()
                bm.from_object(obj, depsgraph)
                bm.verts.ensure_lookup_table()
                
                # Aplica a matriz de transformação
                bm.transform(matrix)        

                materials = obj.data.materials

                for f in bm.faces:
                    matIndex = f.material_index
                    if matIndex < len(materials):
                        slot = obj.material_slots[f.material_index]
                        mat = slot.material
                        if mat is not None:
                            # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                            if mat.name not in materialArea:
                                materialArea[mat.name] = 0.0
                            
                            # Calcula a área da face e adiciona ao material correspondente
                            materialArea[mat.name] += f.calc_area()
                        else:
                            # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                            if "Sem material" not in materialArea:
                                materialArea["Sem material"] = 0.0
                            
                            # Calcula a área da face e adiciona ao material correspondente
                            materialArea["Sem material"] += f.calc_area()
                            print("Detectada face sem material aplicado")
                    else:
                        # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                        if "Sem material" not in materialArea:
                            materialArea["Sem material"] = 0.0
                        
                        # Calcula a área da face e adiciona ao material correspondente
                        materialArea["Sem material"] += f.calc_area()
                        print("Detectada face sem material aplicado")

        exportString = "Material\tÁrea"

        for mat, area in materialArea.items():
            areaString = str(round(area,3)).replace(".",",")
            exportString += f"\n{mat}\t{areaString}"
                
        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = exportString
        return {'FINISHED'}

class BOCalcularAreaPorObjetoEMaterial(bpy.types.Operator):
    """Calcula a área dos materiais aplicados aplicados nos objetos dividindo por objeto"""
    bl_idname = "calcarea.20"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOCalcularAreaPorObjetoEMaterial ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Dicionário para armazenar as áreas de cada material e objeto
        objetoMaterial = {}
        


        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':

                materialArea = {}

                # Matriz de transformações do objeto
                matrix = obj.matrix_world
                
                # Obtém o Mesh do objeto levando em consideração a escala
                mesh = obj.data

                # Para pegar o mesh após modificadores
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm = bmesh.new()
                bm.from_object(obj, depsgraph)
                bm.verts.ensure_lookup_table()
                
                # Aplica a matriz de transformação
                bm.transform(matrix)        

                materials = obj.data.materials

                for f in bm.faces:
                    matIndex = f.material_index
                    if matIndex < len(materials):
                        slot = obj.material_slots[f.material_index]
                        mat = slot.material
                        if mat is not None:
                            # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                            if mat.name not in materialArea:
                                materialArea[mat.name] = 0.0
                            
                            # Calcula a área da face e adiciona ao material correspondente
                            materialArea[mat.name] += f.calc_area()
                        else:
                            # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                            if "Sem material" not in materialArea:
                                materialArea["Sem material"] = 0.0
                            
                            # Calcula a área da face e adiciona ao material correspondente
                            materialArea["Sem material"] += f.calc_area()
                            print("Detectada face sem material aplicado")
                    else:
                        # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                        if "Sem material" not in materialArea:
                            materialArea["Sem material"] = 0.0
                        
                        # Calcula a área da face e adiciona ao material correspondente
                        materialArea["Sem material"] += f.calc_area()
                        print("Detectada face sem material aplicado")
                
                objetoMaterial[obj.name] = materialArea

        exportString = "Objeto\tMaterial\tÁrea"

        for objeto, areamat in objetoMaterial.items():
            for mat, area in areamat.items():
                areaString = str(round(area,3)).replace(".",",")
                exportString += f"\n{objeto}\t{mat}\t{areaString}"
                
        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = exportString
        return {'FINISHED'}

class BOCalcularAreaPorObjeto(bpy.types.Operator):
    """Calcula a área dos objetos selecionados"""
    bl_idname = "calcarea.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOCalcularAreaPorObjeto ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Dicionário para armazenar as áreas de cada material
        areaObjeto = {}

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                
                # Matriz de transformações do objeto
                matrix = obj.matrix_world
                
                # Obtém o Mesh do objeto levando em consideração a escala
                mesh = obj.data

                # Para pegar o mesh após modificadores
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm = bmesh.new()
                bm.from_object(obj, depsgraph)
                bm.verts.ensure_lookup_table()
                
                # Aplica a matriz de transformação
                bm.transform(matrix)        

                materials = obj.data.materials

                for f in bm.faces:
                    # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                    if obj.name not in areaObjeto:
                        areaObjeto[obj.name] = 0.0
                    
                    # Calcula a área da face e adiciona ao material correspondente
                    areaObjeto[obj.name] += f.calc_area()

        exportString = "Objeto\tÁrea"

        for objeto, area in areaObjeto.items():
            areaString = str(round(area,3)).replace(".",",")
            exportString += f"\n{objeto}\t{areaString}"
                
        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = exportString
        return {'FINISHED'}

class BOCalcularAreaDasFacesSelecionadas(bpy.types.Operator):
    """Calcula a área dos objetos selecionados"""
    bl_idname = "calcareafaces.1"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOCalcularAreaDasFacesSelecionadas ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Ativa o modo de edição, ambos métodos funcionam
        bpy.ops.object.mode_set(mode='EDIT')

        # Dicionário para armazenar as áreas de cada material
        areaFaces = 0.0

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                
                # Matriz de transformações do objeto
                matrix = obj.matrix_world
                
                # Obtém o Mesh do objeto levando em consideração a escala
                mesh = obj.data

                # Para pegar o mesh após modificadores
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm = bmesh.new()
                bm.from_mesh(obj, depsgraph)
                bm.faces.ensure_lookup_table()

                # Pega as faces selecionadas
                selectedFaces = [x for x in bm.faces if x.select]

                print(len(selectedFaces))
                
                # Aplica a matriz de transformação
                bm.transform(matrix)        

                materials = obj.data.materials

                for f in bm.faces:
                    if f.select == True:
                        print("Face selecionada")
                        areaFaces += f.cal_area()

        exportString = f"Área\t{areaFaces}"

        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = exportString
        return {'FINISHED'}

class BOCalcularVolumePorObjeto(bpy.types.Operator):
    """Calcula o volume dos objetos selecionados"""
    bl_idname = "calcolume.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOCalcularVolumePorObjeto ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Dicionário para armazenar as áreas de cada material
        volumes = {}

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                
                # Matriz de transformações do objeto
                matrix = obj.matrix_world
                
                # Obtém o Mesh do objeto levando em consideração a escala
                mesh = obj.data

                # Para pegar o mesh após modificadores
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm = bmesh.new()
                bm.from_object(obj, depsgraph)
                bm.verts.ensure_lookup_table()
                
                # Aplica a matriz de transformação
                bm.transform(matrix)    

                # Triangula o bmesh
                bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')

                # Calcula o volume usando o padrão do Blender
                volume = bm.calc_volume()
                print(f"Volume do objeto: {obj.name} | {volume}")

                # Calcula o volume usando o algoritmo SignedVolumeOfTriangle
                bm.faces.ensure_lookup_table() # Necessário antes de usar índices para faces, vértices, etc
                signedVolume = 0.0
                for face in bm.faces:
                    signedVolume += SignedVolumeOfTriangle(face)
                print(f"Signed Volume do objeto: {obj.name} | {signedVolume}")

                # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                if obj.name not in volumes:
                    volumes[obj.name] = 0.0
                
                # Calcula a área da face e adiciona ao material correspondente
                volumes[obj.name] += volume

        exportString = "Objeto\tVolume"

        for objeto, area in volumes.items():
            areaString = str(round(area,3)).replace(".",",")
            exportString += f"\n{objeto}\t{areaString}"
                
        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = exportString
        return {'FINISHED'}

class BOCalcularGeometria(bpy.types.Operator):
    """Calcula a geometria dos objetos selecionados, dimensões, boundingBox, áreas e volumes"""
    bl_idname = "calcgeometria.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOCalcularGeometria ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Dicionário para armazenar as áreas de cada material
        objetosCalculados = []

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':

                # Matriz de transformações do objeto
                matrix = obj.matrix_world
                
                # Obtém o Mesh do objeto levando em consideração a escala
                mesh = obj.data

                # Para pegar o mesh após modificadores
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm = bmesh.new()
                bm.from_object(obj, depsgraph)
                bm.verts.ensure_lookup_table()
                
                # Aplica a matriz de transformação
                bm.transform(matrix)    

                # Triangula o bmesh
                bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')

                # Calcula o volume usando o padrão do Blender
                volume = bm.calc_volume()
                print(f"Volume do objeto: {obj.name} | {volume}")

                # Calcula o volume usando o algoritmo SignedVolumeOfTriangle e também a área das faces
                signedVolume = 0.0
                facesArea = 0.0
                facesInfArea = 0.0
                facesVertiArea = 0.0
                facesSupArea = 0.0
                facesIncInfArea = 0.0
                facesIncSupArea = 0.0

                bm.faces.ensure_lookup_table() # Necessário antes de usar índices para faces, vértices, etc
                
                for face in bm.faces:
                    signedVolume += SignedVolumeOfTriangle(face)
                    fArea = face.calc_area()
                    facesArea += fArea

                    # Verifica a normal da Area
                    faceNormal = face.normal
                    print(faceNormal)

                    if math.isclose(faceNormal.z, -1):
                        facesInfArea += fArea
                    elif math.isclose(faceNormal.z, 1):
                        facesSupArea += fArea
                    elif math.isclose(faceNormal.z, 0):
                        facesVertiArea += fArea
                    elif faceNormal.z < 0 and not math.isclose(faceNormal.z, -1):
                        facesIncInfArea += fArea
                    elif faceNormal.z > 0 and not math.isclose(faceNormal.z, 1):
                        facesIncSupArea += fArea


                print(f"Signed Volume do objeto: {obj.name} | {signedVolume}")

                # Calcula a BoundingBox
                bbX = obj.dimensions.x
                bbY = obj.dimensions.y
                bbZ = obj.dimensions.z
                bbVolume = bbX*bbY*bbZ

                # Cria um objetoCalculado
                calcObj = GeometryObj(obj.name, bbX, bbY, bbZ, bbVolume, facesArea, 
                                      facesInfArea, facesVertiArea, facesSupArea, facesIncInfArea,
                                      facesIncSupArea, volume, signedVolume)
                
                print(f"Area Inferior{facesInfArea}")
                objetosCalculados.append(calcObj)

        exportString = "Objeto\tBoundingBox X\tBoundingBox Y\tBoundingBox Z\tBoundingBox Volume\tArea total das faces\tArea das faces inferiores"
        exportString += "\tArea das faces verticais\tArea das faces superiores\tArea das faces inclinadas inferiores"
        exportString += "\tArea das faces inclinadas superiores\tVolume\tSigned Volume"

        for objeto in objetosCalculados:
            strBBX = str(round(objeto.boundingBoxX,3)).replace(".",",")
            strBBY = str(round(objeto.boundingBoxY,3)).replace(".",",")
            strBBZ = str(round(objeto.boundingBoxZ,3)).replace(".",",")
            strBBVolume = str(round(objeto.boundingBoxVolume,3)).replace(".",",")
            strAreaTotal = str(round(objeto.facesArea,3)).replace(".",",")
            strAreaInferior = str(round(objeto.facesInfArea,3)).replace(".",",")
            strAreaVertical = str(round(objeto.facesVertiArea,3)).replace(".",",")
            strAreaSuperior = str(round(objeto.facesSupArea,3)).replace(".",",")
            strAreaIncInferior = str(round(objeto.facesIncInfArea,3)).replace(".",",")
            strAreaIncSuperior = str(round(objeto.facesIncSupArea,3)).replace(".",",")
            strVolume = str(round(objeto.Volume,3)).replace(".",",")
            strSignedVolume = str(round(objeto.SignedVolume,3)).replace(".",",")

            exportString += f"\n{objeto.name}\t{strBBX}\t{strBBY}\t{strBBZ}\t{strBBVolume}\t{strAreaTotal}\t{strAreaInferior}"
            exportString += f"\t{strAreaVertical}\t{strAreaSuperior}\t{strAreaIncInferior}\t{strAreaIncSuperior}\t{strVolume}\t{strSignedVolume}"
                
        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = exportString
        return {'FINISHED'}    

class BOCalcularQuantidade(bpy.types.Operator):
    """Calcula a quantidade dos objetos selecionados considerando também o modificador Array"""
    bl_idname = "calcularquantidade.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        
        print('---------- CÓDIGO INICIA AQUI - BOCalcularQuantidade ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Quantidade de elementos selecionados
        quantidade = 0

        # Para cada objeto selecionado
        for obj in selection:
            
            # Verifica se tem o modificador Aray aplicado
            temArray = False

            for modifier in obj.modifiers:
                if modifier.type == "ARRAY":
                    temArray = True
            
            if temArray:
                for modifier in obj.modifiers:
                    if modifier.type == "ARRAY":
                        quantidade += modifier.count
            else:
                quantidade += 1
        
        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = str(quantidade)
                
        return {'FINISHED'}

class BOCalcularComprimentoDasArestas(bpy.types.Operator):
    """Calcula o comprimento total das arestas dos objetos selecionados"""
    bl_idname = "calcularcomprimento.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOCalcularComprimentoDasArestas ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Dicionário para armazenar as áreas de cada material
        comprimentoObjeto = {}

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                
                # Matriz de transformações do objeto
                matrix = obj.matrix_world
                
                # Obtém o Mesh do objeto levando em consideração a escala
                mesh = obj.data

                # Para pegar o mesh após modificadores
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm = bmesh.new()
                bm.from_object(obj, depsgraph)
                bm.edges.ensure_lookup_table()
                
                # Aplica a matriz de transformação
                bm.transform(matrix)        

                for e in bm.edges:
                    if obj.name not in comprimentoObjeto:
                        comprimentoObjeto[obj.name] = 0.0
                    
                    # Calcula a área da face e adiciona ao material correspondente
                    comprimentoObjeto[obj.name] += e.calc_length()

        exportString = "Objeto\tComprimento"

        for objeto, comprimento in comprimentoObjeto.items():
            comprimentoStrign = str(round(comprimento,3)).replace(".",",")
            exportString += f"\n{objeto}\t{comprimentoStrign}"
                
        # Copia para a área de transferência e imprime a string final
        bpy.context.window_manager.clipboard = exportString
        return {'FINISHED'}

        return {'FINISHED'}

# endregion 

# region BOTÕES UTILIDADES

class BOSelecionarMateriaisLinkados(bpy.types.Operator):
    """Seleciona os objetos que compartilham o mesmo material"""
    bl_idname = "selecionarmateriais.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BOSelecionarMateriaisLinkados ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Desseleciona todos os objetos
        bpy.ops.object.select_all(action='DESELECT')

        # Lista para guardar os objetos selecionados
        allselected = []

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.select_linked(type='MATERIAL')
                newselection = bpy.context.selected_objects
                allselected.extend(newselection)

        # Restora a seleção
        for obj in allselected:
            obj.select_set(True)
                
        return {'FINISHED'}    

class BODividirMeshPorNormal(bpy.types.Operator):
    """Divide as faces do objeto selecionado de acordo com a direção da mesma"""
    bl_idname = "dividir.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BODividirMeshPorNormal ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Define a tolerância do vetor
        tolerancia = 0.1

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                
                # Obtenha o objeto da malha atual e entre no modo de seleção de face        
                #bpy.ops.mesh.select_mode(type='FACE')

                facesVerticais = []
                facesInferiores = []
                facesSuperiores = []
                facesInclinadasInferiores = []
                facesInclinadasSuperiores = []

                for face in obj.data.polygons:
                    normal = face.normal
                    if abs(normal.z) <= tolerancia:
                        facesVerticais.append(face.index)
                    elif abs(normal.z - -1) <= tolerancia:
                        facesInferiores.append(face.index)
                    elif abs(normal.z - 1) <= tolerancia:
                        facesSuperiores.append(face.index)
                    elif normal.z < 0:
                        facesInclinadasInferiores.append(face.index)
                    elif normal.z > 0:
                        facesInclinadasSuperiores.append(face.index)
                    
                if len(facesVerticais) > 0:
                    SepararFacesPeloIndice(obj,facesVerticais,"_FacesVerticais")
                if len(facesInferiores) > 0:
                    SepararFacesPeloIndice(obj,facesInferiores,"_FacesInferiores")
                if len(facesSuperiores) > 0:        
                    SepararFacesPeloIndice(obj,facesSuperiores,"_FacesSuperiores")
                if len(facesInclinadasInferiores) > 0:        
                    SepararFacesPeloIndice(obj,facesInclinadasInferiores,"_FacesInclinadasInferiores")        
                if len(facesInclinadasSuperiores) > 0:        
                    SepararFacesPeloIndice(obj,facesInclinadasSuperiores,"_FacesInclinadasSuperiores")
        

        # Verifique se está no modo de objeto (Object Mode)
        if bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            
        # Atualiza a cena
        bpy.context.view_layer.update()

        return {'FINISHED'}

class BODividirPorMaterial(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "dividirpormaterial.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):

        print('---------- CÓDIGO INICIA AQUI - BODividirMeshPorNormal ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Separa os elementos pelo material
        facesEMateriais = {}
        novosObj = []

        # Verifique se está no modo de objeto (Object Mode)
        if bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')        

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':

                # Matriz de transformações do objeto
                matrix = obj.matrix_world

                # Para pegar o mesh após modificadores
                depsgraph = bpy.context.evaluated_depsgraph_get()
                bm = bmesh.new()
                bm.from_object(obj, depsgraph)
                bm.verts.ensure_lookup_table()
                
                # Aplica a matriz de transformação
                bm.transform(matrix)        

            # Filtra as faces de acordo com o material
            materials = obj.data.materials

            for f in bm.faces:
                matIndex = f.material_index
                if matIndex < len(materials):
                    slot = obj.material_slots[f.material_index]
                    mat = slot.material
                    if mat is not None:
                        # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                        if mat.name not in facesEMateriais:
                            facesEMateriais[mat.name] = [f.index]
                        
                        # Calcula a área da face e adiciona ao material correspondente
                        facesEMateriais[mat.name] += [f.index]
                    else:
                        # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                        if "Sem material" not in facesEMateriais:
                            facesEMateriais["Sem material"] = [f.index]
                        
                        # Calcula a área da face e adiciona ao material correspondente
                        facesEMateriais["Sem material"] += [f.index]
                        print("Detectada face sem material aplicado")
                else:
                    # Verifica se o material já está no dicionário se não adiciona uma nova chave com o nome do mesmo
                    if "Sem material" not in facesEMateriais:
                        facesEMateriais["Sem material"] = [f.index]
                    
                    # Calcula a área da face e adiciona ao material correspondente
                    facesEMateriais["Sem material"] += [f.index]
                    print("Detectada face sem material aplicado")   

            # Para cada face dividir criando novos objetos
            for material, faces in facesEMateriais.items():
                print(f"{material} com {len(faces)} faces")
                novoObj = SepararFacesPeloIndice(obj, faces, material)
                novosObj.append(novoObj)             
                
        # Verifique se está no modo de objeto (Object Mode)
        if bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            
        # Atualiza a cena
        bpy.context.view_layer.update()

        return {'FINISHED'}

class BOCopiarCores(bpy.types.Operator):
    """Copia a cor da viewport do objeto ativo para os objetos selecionados"""
    bl_idname = "copiarcores.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        
        print('---------- CÓDIGO INICIA AQUI - BOCalcularAreaPorMaterial ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Pega a cor do objeto ativo
        cor = active_object.color

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':
                obj.color = cor
                
        return {'FINISHED'}

# endregion 

# region BOTÕES INTEROPERABILIDADE

# endregion 

class BOExportarCAD(bpy.types.Operator):
    """Exporta as arestas dos para o CAD"""
    bl_idname = "exportarcad.0"
    bl_label = "Simple potato Operator"

    def execute(self, context):
        
        print('---------- CÓDIGO INICIA AQUI - BOExportarCAD ----------')

        # Pega todos os objetos na seleção
        selection = bpy.context.selected_objects

        # Pega o objeto ativo
        active_object = bpy.context.active_object

        # Pega a cor do objeto ativo
        cor = active_object.color

        # Para cada objeto selecionado
        for obj in selection:
            if obj.type == 'MESH':

                # Pega o mesh
                mesh = obj.data

                for edge in mesh.edges:
                    vert1 = mesh.vertices[edge.vertices[0]]
                    vert2 = mesh.vertices[edge.vertices[1]]



        return {'FINISHED'}

# endregion

# region FUNÇÕES

def SignedVolumeOfTriangle(face):

    v1 = mathutils.Vector(face.verts[0].co)
    v2 = mathutils.Vector(face.verts[1].co)
    v3 = mathutils.Vector(face.verts[2].co)

    volume = volume = v1.dot(v2.cross(v3)) / 6

    return volume

def SepararFacesPeloIndice(obj, facesIndex, sufix):
    # Cria uma cópia do objeto atual
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate(linked=False)
    novoObj = bpy.context.active_object
    novoObj.name = obj.name + sufix   
    
    # Seleciona as faces de acordo com as listas fornecidas
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = novoObj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    mesh = novoObj.data
    
    # Cria um bmesh a partir do novoObj para poder selecionar as faces
    bm = bmesh.from_edit_mesh(novoObj.data)
    bm.faces.ensure_lookup_table()
    
    for face in bm.faces:
        if face.index not in facesIndex:
           bm.faces[face.index].select = True
    
    bmesh.update_edit_mesh(novoObj.data)        
    
    # Deleta as faces não selecionadas
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Atualiza o objeto
    novoObj.update_from_editmode()
    novoObj.select_set(True)
    
    return novoObj

class GeometryObj:
    def __init__(self, name, boundingBoxX, boundingBoxY, boundingBoxZ, boundingBoxVolume, 
                 facesArea, facesInfArea, facesVertiArea, facesSupArea, facesIncInfArea, facesIncSupArea, Volume, SignedVolume):
        self.name = name
        self.boundingBoxX = boundingBoxX
        self.boundingBoxY = boundingBoxY
        self.boundingBoxZ = boundingBoxZ
        self.boundingBoxVolume = boundingBoxVolume
        self.facesArea = facesArea
        self.facesInfArea = facesInfArea
        self.facesVertiArea = facesVertiArea
        self.facesSupArea = facesSupArea
        self.facesIncInfArea = facesIncInfArea
        self.facesIncSupArea = facesIncSupArea
        self.Volume = Volume
        self.SignedVolume = SignedVolume

class CadType(enum.Enum):
    Line = 0
    Arc = 1
    Circle = 2
    Polyline = 3
    Point = 4
    Block = 5
    Hatch = 6

class CadObject:
    def __init__(self):
        self.CadType = None
        self.LineGeometry = None
        self.ArcGeometry = None
        self.CircleGeometry = None
        self.PolylineGeometry = None
        self.PointGeometry = None
        self.LoopsGeometry = None
        self.BlockGeometry = None
        self.CadProperties = {}
    
    def CadObject(self, lineGeometry, cadProperties):
        self.CadType = CadType.Line
        self.LineGeometry = lineGeometry
        self.CadProperties = cadProperties

class CurveType(enum.Enum):
    Line = 0
    Arc = 1
    Circle = 2

class CadPoint3D:
    def __init__(self, xCoord, yCoord, zCoord):
        self.XCoord = xCoord
        self.YCoord = yCoord
        self.ZCoord = zCoord

    def Normalize(self):
        length = math.sqrt(self.XCoord * self.XCoord + self.YCoord * self.YCoord + self.ZCoord * self.ZCoord)
        self.XCoord /= length
        self.YCoord /= length
        self.ZCoord /= length

class CadCurve:
    def __init__(self):
        self.CurveType = None
        self.StartPoint = None
        self.EndPoint = None
        self.Center = None
        self.Middle = None
        self.Normal = None
        self.Radius = None

# endregion

# region PAINEL E CLASSES

class CustomPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "ORC Panel"
    bl_idname = "OBJECT_PT_ORCTOOLS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ORC Tools"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        myTool = scene.my_tool

        box = layout.box()
        box.label(text="Levantamento")
        row = box.row()
        row.operator(BOCalcularAreaPorMaterial.bl_idname,
                     text="Área dos materiais", icon='FACESEL')
        row = box.row()
        row.operator(BOCalcularAreaPorObjetoEMaterial.bl_idname,
                     text="Área dos materiais por objeto", icon='FACESEL')
        row = box.row()
        row.operator(BOCalcularAreaPorObjeto.bl_idname,
                     text="Área dos objetos", icon='FACESEL')
        row = box.row()
        row.operator(BOCalcularVolumePorObjeto.bl_idname,
                     text="Volume dos objetos", icon='SNAP_VOLUME')
        row = box.row()
        row.operator(BOCalcularGeometria.bl_idname,
                     text="Calcular geometria", icon='SNAP_VOLUME')
        row = box.row()
        row.operator(BOCalcularComprimentoDasArestas.bl_idname,
                     text="Calcular comprimento", icon='MOD_LENGTH')
        row = box.row()
        row.operator(BOCalcularQuantidade.bl_idname,
                     text="Calcular quantidade", icon='OUTLINER_OB_POINTCLOUD')        
        
        box = layout.box()
        box.label(text="Utilidades")
        row = box.row()
        row.operator(BOSelecionarMateriaisLinkados.bl_idname,
                     text="Selecionar por material", icon='MATERIAL')
        row = box.row()
        row.operator(BODividirMeshPorNormal.bl_idname,
                     text="Dividir por normal", icon='ORIENTATION_NORMAL')
        row = box.row()
        row.operator(BODividirPorMaterial.bl_idname,
                     text="Dividir por material", icon='MATERIAL')        
        row = box.row()
        row.operator(BOCopiarCores.bl_idname,
                     text="Copiar cor", icon='COLOR')        
        
        box = layout.box()
        box.label(text="Interoperabilidade")

_classes = [
    BOCalcularAreaPorMaterial,
    BOCalcularAreaPorObjeto,
    BOCalcularVolumePorObjeto,
    BOCalcularGeometria,
    BOSelecionarMateriaisLinkados,
    BOCalcularComprimentoDasArestas,
    BODividirMeshPorNormal,
    BOCalcularAreaPorObjetoEMaterial,
    BOCalcularQuantidade,
    BODividirPorMaterial,
    BOCopiarCores,
    MyProperties,
    CustomPanel]

# endregion

def register():
    for cls in _classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)


def unregister():
    for cls in _classes:
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
