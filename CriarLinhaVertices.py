import bpy
import math
import mathutils

# Funções
def VerticeParaVetor(vertice):
    vector = mathutils.Vector((vertice.x, vertice.y, vertice.z))
    return vector

def ProjetarPontoNaLinha(ponto, origem, direcao):
    # Acha a projeção escalar do ponto na linha
    scalarProj = (ponto-origem).dot(direcao)

    pontoProjecao = origem + direcao * scalarProj

    return pontoProjecao

def PontoInicialEFinalDalinha(pontos, iterations,):
    pontoInicial = mathutils.Vector((0,0,0))
    pontoFinal = mathutils.Vector((0,0,0))
    direcao = mathutils.Vector((0,0,0))

    # Pega a direção da linha
    #result = DirecaoDaLinhaPorPontos(pontos, direcao, iterations)
    result = DirecaoDaLinhaPorPontos(pontos)
    origem = result[0]
    direcao = result[1]

    # Projeta os pontos sobre a direção
    pontosProjecao = []

    for ponto in pontos:
        pontoProjecao = ProjetarPontoNaLinha(ponto,origem, direcao)
        pontosProjecao.append(pontoProjecao)
    
    # Pega o ponto inicial e final da linha, que estão mais distantes do ponto de origem
    
    # Calcula a distância dos pontos até o ponto de origem que é o centro de todos
    # Pega o ponto inicial da linha, sendo o ponto mais distante do ponto de origem
    pontoInicial = max(pontosProjecao, key=lambda p: (p-origem).length)
    # Pega o ponto final da linha, sendo o ponto mais distante do ponto inicial
    pontoFinal = max(pontosProjecao, key=lambda p: (p-pontoInicial).length)

    return pontoInicial, pontoFinal

def DirecaoDaLinhaPorPontosB(pontos, direcao, iterations):
    
    if direcao.length == 0 or math.isnan(direcao.x) or math.isinf(direcao.x):
        direcao = mathutils.Vector((0,0,1))    
        
    # Calcula a origem sendo a média dos pontos
    origem = mathutils.Vector((0,0,0))
    
    for ponto in pontos:
        origem += ponto

    origem /= len(pontos)

    
    # Itera para a aproximação da linha
    for i in range(iterations):

        nDirection = mathutils.Vector((0,0,0))

        for item in pontos:
            point = item - origem
            nDirection += point * direcao.dot(point)

        direcao = nDirection.normalized()
    
    print('Origem: ' + str(origem))
    print('Direção: ' + str(direcao))
    return origem, direcao

def DirecaoDaLinhaPorPontos(pontos):
    
    # Utiliza o método de SVD Singular Value Decomposition

    # Cria uma matriz com os dados dos pontos
    matrixPontos = [[v.x, v.y, v.z] for v in pontos] #Transforma os vetores em uma lista contendo os valores
    dataMatrix = mathutils.Matrix()
    for ponto in pontos:
        dataMatrix.cols.append(ponto)

    # Utiliza SVD na matriz
    u, s, v = dataMatrix.svd()

    # A ultima coluna de V contém a direção da linha
    direcao = v[2].to_3d()

    # O centro dos pontos é seu meio
    origem = sum(pontos, mathutils.Vector((0,0,0))) / len(pontos)

    
    print('Origem: ' + str(origem))
    print('Direção: ' + str(direcao))

    return origem, direcao

print('---------- CÓDIGO INICIA AQUI ----------')

# Pega todos os objetos na seleção
selection = bpy.context.selected_objects

# Pega o objeto ativo
active_object = bpy.context.active_object

# Desseleciona todos os objetos
bpy.ops.object.select_all(action='DESELECT')

# Itera sobre os objetos selecionados
linhas = []

for obj in selection:

    if obj.type == 'MESH':

        # Pega os dados do Msh
        mesh = obj.data

        # Itera sobre os vértices e pega sua posição
        pontos = []

        for vertex in mesh.vertices:
            vertexTransformed = obj.matrix_world @ vertex.co
            vector = VerticeParaVetor(vertexTransformed)
            pontos.append(vector)

        # Calcula o ponto inicial e final da linha
        direcao = mathutils.Vector((0,0,0))
        resultado = PontoInicialEFinalDalinha(pontos, 100)
        pontoInicial = resultado[0]
        pontoFinal = resultado[1]

        print(pontoInicial)
        print(pontoFinal)

        # Cria a linha
        curveData = bpy.data.curves.new(name="Line", type="CURVE")
        curveData.dimensions = '3D'
        curveData.resolution_u = 2

        polyline = curveData.splines.new('POLY')
        polyline.points.add(1)
        polyline.points[0].co = (pontoInicial.x, pontoInicial.y, pontoInicial.z,1)
        polyline.points[1].co = (pontoFinal.x, pontoFinal.y, pontoFinal.z,1)

        # Cria um objeto a partir da linha
        linhaObj = bpy.data.objects.new("Line", curveData)

        # Adiciona o objeto a cena
        bpy.context.collection.objects.link(linhaObj)

        # Adiciona a linha gerada a lista de linhas
        linhas.append(linhaObj)

# Restora a seleção para todas as linhas geradas
for obj in linhas:
    obj.select_set(True)

# Restora o objeto ativo como a primeira linha gerada
bpy.context.view_layer.objects.active = linhas[0]
