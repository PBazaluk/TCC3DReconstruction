import vtk
import numpy as np
import cv2
from scipy.spatial import Delaunay

NUM_VERTICES = 20
SPACE_SIZE = 500
IMG_PATH = "Entrada/imagem_composta.jpg"  # Substitua pelo caminho da sua imagem


# Função para criar uma linha a partir de pontos
def create_line(start_point, end_point, color):
    points = vtk.vtkPoints()
    points.InsertNextPoint(start_point)
    points.InsertNextPoint(end_point)

    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, 0)
    line.GetPointIds().SetId(1, 1)

    lines = vtk.vtkCellArray()
    lines.InsertNextCell(line)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetLineWidth(2)

    return actor

# Função para filtrar pontos com base na profundidade mínima de cada linha
def filtrar_pontos_por_profundidade_minima(points):
    
    # Filtrar pontos com base na profundidade
    pontos_filtrados = []
    for p in points:
        pontos = []
        # Encontrar o menor item do array
        menor_item = min(p)
        for i in p:
            if i >= menor_item + 20:
                pontos.append(i)
            else:
                pontos.append(i)
        pontos_filtrados.append(pontos)
    return np.array(pontos_filtrados)


def gerar_malha_delaunay_2d(depht, space_size):
    # Definir os quatro pontos fixos nos cantos da área 2D
    corner_points = np.array([[1, 1], [space_size-1, 1], 
                              [1, space_size-1], [space_size-1, space_size-1]], np.float32)
                    
    # Adicionar uma coluna de zeros para z
    corner_points = np.hstack((corner_points, np.zeros((corner_points.shape[0], 1))))

    points = []
    for i,a in enumerate(depht):
        for j,b in enumerate(a):
            # if depht[i][j] != 0:
            p = [i,j,depht[i][j]]
            points.append(p)
    
    points = np.array(points)
    terc_col = points[:, 2]
    points_2d = points[:, -2:]
    terc_col = points[:, 2]
    points_2d = points[:, :2]

    # Combinar os pontos fixos com os pontos aleatórios
    # points = np.vstack((corner_points, random_points))
    points = np.vstack((corner_points, points))

    # Fazer a triangulação de Delaunay
    delaunay = Delaunay(points_2d)

    return delaunay, points_2d, terc_col


# Função para calcular o centro de massa
def calcular_centro_de_massa(points):
    return np.mean(points, axis=0)


def aplicar_textura_vtk(img, delaunay, points, terc_col):
    # Redimensionar a imagem para SPACE_SIZE
    img_resized = cv2.resize(img, (SPACE_SIZE, SPACE_SIZE))

    # Converter imagem de BGR para RGB
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    
    img_rgb = cv2.flip(img_rgb, 0)
    img_rgb = cv2.rotate(img_rgb, cv2.ROTATE_90_CLOCKWISE)

    # Converter imagem para o formato de textura do VTK
    vtk_image = vtk.vtkImageData()
    height, width, channels = img_rgb.shape
    vtk_image.SetDimensions(width, height, 1)
    vtk_image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, channels)

    for y in range(height):
        for x in range(width):
            vtk_image.SetScalarComponentFromFloat(x, y, 0, 0, img_rgb[y, x, 0])
            vtk_image.SetScalarComponentFromFloat(x, y, 0, 1, img_rgb[y, x, 1])
            vtk_image.SetScalarComponentFromFloat(x, y, 0, 2, img_rgb[y, x, 2])



    # Criar o objeto VTK para a malha
    points_vtk = vtk.vtkPoints()
    triangles = vtk.vtkCellArray()
    texture_coords = vtk.vtkFloatArray()
    texture_coords.SetNumberOfComponents(2)
    texture_coords.SetName("Texture Coordinates")

    # Calcular o centro de massa
    centro_de_massa = calcular_centro_de_massa(points)
    for i, p in enumerate(points):
        # Ajustar as coordenadas para serem relativas ao centro de massa
        adjusted_p = p - centro_de_massa
        points_vtk.InsertNextPoint(adjusted_p[0], adjusted_p[1], terc_col[i])
        # Normalizar as coordenadas UV
        texture_coords.InsertNextTuple2((adjusted_p[0] + width / 2) / width, (adjusted_p[1] + height / 2) / height)

    for tri in delaunay.simplices:
        triangle = vtk.vtkTriangle()
        triangle.GetPointIds().SetId(0, tri[0])
        triangle.GetPointIds().SetId(1, tri[1])
        triangle.GetPointIds().SetId(2, tri[2])
        triangles.InsertNextCell(triangle)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points_vtk)
    polydata.SetPolys(triangles)
    polydata.GetPointData().SetTCoords(texture_coords)

    # Mapper para o mapeamento de textura
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    # Criar ator para a malha
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Aplicar textura
    texture = vtk.vtkTexture()
    texture.SetInputData(vtk_image)
    actor.SetTexture(texture)
    
    # Renderizador
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    renderer.AddActor(actor)
    # renderer.AddActor(x_axis)
    # renderer.AddActor(y_axis)
    # renderer.AddActor(z_axis)
    renderer.SetBackground(1, 1, 1)

    render_window.Render()
    render_interactor.Start()

# Abre o arquivo em modo de leitura
with open('Entrada/resultado_depth.txt', 'r') as file:
    conteudo_depth = file.read()  # Lê o conteúdo do arquivo

# Converte a string lida para uma lista
depth = eval(conteudo_depth)

d = np.array(depth)

# Ler e redimensionar a imagem
img = cv2.imread(IMG_PATH)

# Obter as dimensões da imagem
height, width, _ = img.shape

# Calcular a proporção
proportion = width / height

# Exibir as dimensões e a proporção
print(f'Largura: {width}, Altura: {height}, Proporção: {proportion}')

# Gerar a malha de Delaunay 2D
delaunay, points, terc_col = gerar_malha_delaunay_2d(d, SPACE_SIZE)

# Aplicar a textura e exibir a malha 3D com VTK
aplicar_textura_vtk(img, delaunay, points, terc_col)