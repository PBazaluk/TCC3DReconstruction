import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay
from PIL import Image
import vtk
import cv2
from scipy.spatial import Delaunay

# Abre o arquivo em modo de leitura
with open('resultado_depth.txt', 'r') as file:
    conteudo_depth = file.read()  # Lê o conteúdo do arquivo

# Converte a string lida para uma lista
depth = eval(conteudo_depth)

malha1 = []
malha2 = []

for i,a in enumerate(depth):
    if i == 0:
        for j,b in enumerate(a):
            for k,c in enumerate(b):
                p = [j,k,depth[i][j][k]]
                malha1.append(p)
                
    elif i == 1:
        for j,b in enumerate(a):
            for k,c in enumerate(b):
                p = [j,k,depth[i][j][k]]
                malha2.append(p)
    
sift = [
[0,241,221],
[0,293,190],
[1,213,410],
[1,166,469],
[2,216,254],
[2,146,270],
[3,291,231],
[3,249,247],
[4,313,277],
[4,267,292],
[5,133,343],
[5,452,337],
[6,188,293],
[6,129,325],
[7,130,378],
[7,78,434],
[8,337,384],
[8,325,445],
[9,286,49],
[9,252,21],
[10,313,270],
[10,266,287],
[11,149,367],
[11,103,423],
[12,212,273],
[12,165,297],
[13,327,219],
[13,302,230],
[14,341,294],
[14,316,324],
[15,130,378],
[15,78,434],
[16,211,55],
[16,205,31],
[17,310,261],
[17,262,280],
[18,149,367],
[18,103,423],
[19,315,260],
[19,269,278],
[20,215,58],
[20,210,33],
[21,127,322],
[21,446,336],
[22,421,224],
[22,450,244],
[23,121,101],
[23,95,105],
[24,421,224],
[24,450,244],
[25,266,244],
[25,215,262],
[26,176,351],
[26,326,430],
[27,400,240],
[27,307,267],
]

malha2 = np.array(malha2)
# Calculando o centro de massa
center_of_mass2 = np.mean(malha2, axis=0)

# Transladando a malha para que o centro de massa fique em (0,0,0)
translated_malha2 = malha2 - center_of_mass2

# Configurando o gráfico
# fig = plt.figure(figsize=(12, 6))

# Plotando a malha original
# ax1 = fig.add_subplot(121, projection='3d')
# ax1.scatter(malha2[:, 0], malha2[:, 1], malha2[:, 2], c='blue', marker='o')
# ax1.set_title('Malha Original - 2')
# ax1.set_xlabel('X')
# ax1.set_ylabel('Y')
# ax1.set_zlabel('Z')

# # Plotando a malha transladada
# ax2 = fig.add_subplot(122, projection='3d')
# ax2.scatter(translated_malha2[:, 0], translated_malha2[:, 1], translated_malha2[:, 2], c='red', marker='o')
# ax2.set_title('Malha Transladada - 2')
# ax2.set_xlabel('X')
# ax2.set_ylabel('Y')
# ax2.set_zlabel('Z')


malha1 = np.array(malha1)
# Calculando o centro de massa
center_of_mass1 = np.mean(malha1, axis=0)

# Transladando a malha para que o centro de massa fique em (0,0,0)
translated_malha1 = malha1 - center_of_mass1

# Configurando o gráfico
# fig = plt.figure(figsize=(12, 6))

# Plotando a malha original
# ax1 = fig.add_subplot(121, projection='3d')
# ax1.scatter(malha1[:, 0], malha1[:, 1], malha1[:, 2], c='blue', marker='o')
# ax1.set_title('Malha Original - 1')
# ax1.set_xlabel('X')
# ax1.set_ylabel('Y')
# ax1.set_zlabel('Z')

# # Plotando a malha transladada
# ax2 = fig.add_subplot(122, projection='3d')
# ax2.scatter(translated_malha1[:, 0], translated_malha1[:, 1], translated_malha1[:, 2], c='red', marker='o')
# ax2.set_title('Malha Transladada - 1')
# ax2.set_xlabel('X')
# ax2.set_ylabel('Y')
# ax2.set_zlabel('Z')

# plt.show()

# Função para calcular o ângulo entre dois vetores
def angle_between_vectors(v1, v2):
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return np.arccos(cos_theta)

sift = np.array(sift)

# Criar uma nova coluna para adicionar à matriz sift
new_column = np.zeros((sift.shape[0], 1))

# Iterar sobre cada linha da matriz sift
for i in range(sift.shape[0]):
    sift_xy = sift[i, -2:]  # Duas últimas colunas de sift
    
    # Comparar com malha1
    for j in range(malha1.shape[0]):
        malha1_xy = malha1[j, :2]  # Duas primeiras colunas de malha1
        if np.array_equal(sift_xy, malha1_xy):
            new_column[i] = malha1[j, 2]  # Adicionar a terceira coluna de malha1 à nova coluna
    
    # Comparar com malha2
    for k in range(malha2.shape[0]):
        malha2_xy = malha2[k, :2]  # Duas primeiras colunas de malha2
        if np.array_equal(sift_xy, malha2_xy):
            new_column[i] = malha2[k, 2]  # Adicionar a terceira coluna de malha2 à nova coluna

# Adicionar a nova coluna à matriz sift
sift = np.hstack((sift, new_column))
sift = sift[:, 1:]

# Exibir a matriz sift atualizada
# print("Matriz sift atualizada:")
# print(sift)

theta_x = 0
theta_y = 0
theta_z = 0
p_cont = 0

for i in range(0, len(sift), 2):
    p_cont += 1
    # Definindo os pontos que você deseja alinhar
    p1 = sift[i]
    p2 = sift[i+1]

    # Calculando o vetor entre os dois pontos
    v1 = p1 - center_of_mass1
    v2 = p2 - center_of_mass2

    # Calculando os ângulos de rotação para cada eixo
    theta_x_parc = angle_between_vectors(v1[[1, 2]], v2[[1, 2]])  # Ângulo no plano yz
    theta_y_parc = angle_between_vectors(v1[[0, 2]], v2[[0, 2]])  # Ângulo no plano xz
    theta_z_parc = angle_between_vectors(v1[[0, 1]], v2[[0, 1]])  # Ângulo no plano xy
    
    theta_x += theta_x_parc
    theta_y += theta_y_parc
    theta_z += theta_z_parc

theta_x = theta_x / p_cont
theta_y = theta_y / p_cont
theta_z = theta_z / p_cont

# print(f"Theta X: {theta_x} Theta Y: {theta_y} Theta Z: {theta_z}")

# Criando as matrizes de rotação
def rotation_matrix(axis, theta):
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    return np.array([[a*a + b*b - c*c - d*d, 2*(b*c - a*d), 2*(b*d + a*c)],
                     [2*(b*c + a*d), a*a + c*c - b*b - d*d, 2*(c*d - a*b)],
                     [2*(b*d - a*c), 2*(c*d + a*b), a*a + d*d - b*b - c*c]])

# Rotação em torno dos eixos x, y e z
rotation_matrix_x = rotation_matrix(np.array([1, 0, 0]), theta_x)
rotation_matrix_y = rotation_matrix(np.array([0, 1, 0]), theta_y)
rotation_matrix_z = rotation_matrix(np.array([0, 0, 1]), theta_z)

# Aplicando as rotações à malha
rotated_malha2 = np.dot(translated_malha2, rotation_matrix_x.T)
rotated_malha2 = np.dot(rotated_malha2, rotation_matrix_y.T)
rotated_malha2 = np.dot(rotated_malha2, rotation_matrix_z.T)

# Configurando o gráfico
# fig = plt.figure(figsize=(12, 6))

# # Plotando a malha original
# ax1 = fig.add_subplot(121, projection='3d')
# ax1.scatter(malha2[:, 0], malha2[:, 1], malha2[:, 2], c='blue', marker='o')
# ax1.set_title('Malha Original')
# ax1.set_xlabel('X')
# ax1.set_ylabel('Y')
# ax1.set_zlabel('Z')

# # Plotando a malha rotacionada
# ax2 = fig.add_subplot(122, projection='3d')
# ax2.scatter(rotated_malha2[:, 0], rotated_malha2[:, 1], rotated_malha2[:, 2], c='red', marker='o')
# ax2.set_title('Malha Rotacionada')
# ax2.set_xlabel('X')
# ax2.set_ylabel('Y')
# ax2.set_zlabel('Z')

plt.show()



merge = []
equivalentes = []
for item in translated_malha1:
    merge.append(item)

for item in rotated_malha2:
    ndsift = np.array(sift)
    nditem = np.array(item)
    siftxy = ndsift[:, -2:]
    itemxy = nditem[ :2]
    inclui = 0
    igual = []
    for siftitem in siftxy:
        # print(f"{itemxy},  {siftitem}")
        if np.array_equal(itemxy,siftitem):
            inclui = -1
            igual = siftitem
            
    if inclui != -1:
        merge.append(item)
    else:
        equivalentes.append(item)
        # print(f"Igual: {igual} Equivalente: {item}")
    
output_file = "merge.txt"
with open(output_file, 'w') as f:
    f.write("[")
    for i in merge:
        f.write(str(i))
        f.write(",\n")
    f.write("]")



merge2 = []
equivalentes = []
for item in malha1:
    merge2.append(item)

for item in malha2:
    ndsift = np.array(sift)
    nditem = np.array(item)
    siftxy = ndsift[:, -2:]
    itemxy = nditem[ :2]
    inclui = 0
    igual = []
    for siftitem in siftxy:
        # print(f"{itemxy},  {siftitem}")
        if np.array_equal(itemxy,siftitem):
            inclui = -1
            igual = siftitem
            
    if inclui != -1:
        merge2.append(item)
    else:
        equivalentes.append(item)
        # print(f"Igual: {igual} Equivalente: {item}")

# # Malha 1------------------------------------
# malha1 = np.array(malha1)
# # Criação de uma grade de pontos em x e y
# x = malha1[:, 0]
# y = malha1[:, 1]
# z = malha1[:, 2]

# # Configurando o gráfico
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plotando os pontos em 3D
# ax.scatter(x, y, z, c='blue', marker='o')
# plt.title("Malha 1")

# # Malha 2------------------------------------
# malha2 = np.array(malha2)
# # Criação de uma grade de pontos em x e y
# x = malha2[:, 0]
# y = malha2[:, 1]
# z = malha2[:, 2]

# # Configurando o gráfico
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plotando os pontos em 3D
# ax.scatter(x, y, z, c='blue', marker='o')
# plt.title("Malha 2")

# Merge------------------------------------
# merge = np.array(merge)
# # Criação de uma grade de pontos em x e y
# x = merge[:, 0]
# y = merge[:, 1]
# z = merge[:, 2]

# # Configurando o gráfico
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plotando os pontos em 3D
# ax.scatter(x, y, z, c='blue', marker='o')
# plt.title("Merge")

# # Merge Velho------------------------------------
# merge2 = np.array(merge2)
# # Criação de uma grade de pontos em x e y
# x = merge2[:, 0]
# y = merge2[:, 1]
# z = merge2[:, 2]

# # Configurando o gráfico
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plotando os pontos em 3D
# ax.scatter(x, y, z, c='blue', marker='o')
# plt.title("Merge Sem Rotacionar")

# # Não plotados------------------------------------
# equivalentes = np.array(equivalentes)
# # Criação de uma grade de pontos em x e y
# # print(equivalentes)
# x = equivalentes[:, 0]
# y = equivalentes[:, 1]
# z = equivalentes[:, 2]


# # Plotando os pontos em 3D
# ax.scatter(x, y, z, c='red', marker='o')
# # plt.title("Equivalentes")

# # Exibindo o gráfico
# plt.show()

# Supondo que merge seja um array numpy de floats
# merge = np.array([
#     [-500, -500, 0],
#     [-500, 500, 0],
#     [-500, 500, 0],
#     [500, 500, 0],
#     [-500, -500, 500],
#     [500, -500, 500],
#     [-500, 500, 500],
#     [500, 500, 500]
# ])
# num_pontos = 10
# space_size = 200
# merge = np.random.rand(num_pontos, 3) * space_size

merge = np.array(merge)
merge = merge.astype(int)
# Criação de uma grade de pontos em x e y
x = merge[:, 0]
y = merge[:, 1]
z = merge[:, 2]
# print(z)

def gerar_malha_delaunay_2d(num_vertices, space_size):
    # Definir os quatro pontos fixos nos cantos da área 2D
    corner_points = np.array([[1, 1], [space_size-1, 1], 
                              [1, space_size-1], [space_size-1, space_size-1]], np.float32)

    # Gerar 'num_vertices - 4' pontos aleatórios dentro da área 2D
    # random_points = np.random.randint(0, space_size, (num_vertices - 4, 2)).astype(np.float32)
    points = merge
    terc_col = points[:, 2]
    points_2d = points[:, :2]

    # Combinar os pontos fixos com os pontos aleatórios
    # points = np.vstack((corner_points, random_points))
    # points = np.vstack((corner_points, points))

    # Fazer a triangulação de Delaunay
    delaunay = Delaunay(points_2d)

    return delaunay, points_2d, terc_col

# Função para carregar uma textura a partir de um arquivo
def load_texture(filename):
    reader = vtk.vtkPNGReader()
    reader.SetFileName(filename)
    texture = vtk.vtkTexture()
    texture.SetInputConnection(reader.GetOutputPort())
    return texture

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

# Função para calcular o centro de massa
def calcular_centro_de_massa(points):
    return np.mean(points, axis=0)

# Função para aplicar a textura e exibir a malha 3D com VTK
def aplicar_textura_vtk(img, delaunay, points, terc_col):
    # Redimensionar a imagem para SPACE_SIZE
    img_resized = cv2.resize(img, (SPACE_SIZE, SPACE_SIZE))

    # Converter imagem de BGR para RGB
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    
    img_rgb = cv2.flip(img_rgb, 0)
    img_rgb = cv2.rotate(img_rgb, cv2.ROTATE_90_CLOCKWISE)
    
    # Converter a imagem para um formato que o VTK entenda
    height, width, _ = img_rgb.shape
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(width, height, 1)
    vtk_image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 3)
    for y in range(height):
        for x in range(width):
            pixel = img_rgb[y, x]
            vtk_image.SetScalarComponentFromDouble(x, y, 0, 0, pixel[2])
            vtk_image.SetScalarComponentFromDouble(x, y, 0, 1, pixel[1])
            vtk_image.SetScalarComponentFromDouble(x, y, 0, 2, pixel[0])

    # Calcular o centro de massa
    centro_de_massa = calcular_centro_de_massa(points)
    
    # Criar a malha de Delaunay
    points_vtk = vtk.vtkPoints()
    triangles = vtk.vtkCellArray()
    texture_coords = vtk.vtkFloatArray()
    texture_coords.SetNumberOfComponents(2)
    texture_coords.SetName("Texture Coordinates")

    for i, p in enumerate(points):
        # Ajustar as coordenadas para serem relativas ao centro de massa
        adjusted_p = p - centro_de_massa
        points_vtk.InsertNextPoint(adjusted_p[0], adjusted_p[1], terc_col[i]*0.3)
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

    # Mapper para a malha
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    # Criar um ator para a malha
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Aplicar a textura
    texture = vtk.vtkTexture()
    texture.SetInputData(vtk_image)
    actor.SetTexture(texture)

    # Criar os eixos x, y, z
    x_axis = create_line([0, 0, 0], [300, 0, 0], [300, 0, 0])  # Vermelho
    y_axis = create_line([0, 0, 0], [0, 300, 0], [0, 300, 0])  # Verde
    z_axis = create_line([0, 0, 0], [0, 0, 300], [0, 0, 300])  # Azul

    # Criar os eixos x, y, z
    # x_axis = create_line([0, 0, 0], [1, 0, 0], [1, 0, 0])  # Vermelho
    # y_axis = create_line([0, 0, 0], [0, 1, 0], [0, 1, 0])  # Verde
    # z_axis = create_line([0, 0, 0], [0, 0, 1], [0, 0, 1])  # Azul

    # Renderizador
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    renderer.AddActor(actor)
    renderer.AddActor(x_axis)
    renderer.AddActor(y_axis)
    renderer.AddActor(z_axis)
    renderer.SetBackground(1, 1, 1)

    render_window.Render()
    render_interactor.Start()

# Função para exibir apenas os pontos da malha
def exibir_pontos_vtk(points):
    points_vtk = vtk.vtkPoints()
    for p in points:
        points_vtk.InsertNextPoint(p[0], p[1], 0)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points_vtk)

    # Criar glifos para os pontos
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(0.01)

    glyph3d = vtk.vtkGlyph3D()
    glyph3d.SetSourceConnection(sphere.GetOutputPort())
    glyph3d.SetInputData(polydata)
    glyph3d.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph3d.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 0, 0)  # Vermelho

    # Renderizador
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1)

    render_window.Render()
    render_interactor.Start()

# Ler e redimensionar a imagem
img = cv2.imread('imgs/200.jpg')
# Encontrar as extremidades da malha
min_x = merge[np.argmin(merge[:, 0])]
max_x = merge[np.argmax(merge[:, 0])]
min_y = merge[np.argmin(merge[:, 1])]
max_y = merge[np.argmax(merge[:, 1])]
min_z = merge[np.argmin(merge[:, 2])]
max_z = merge[np.argmax(merge[:, 2])]

extremidades = np.array([min_x, max_x, min_y, max_y, min_z, max_z])
# print(extremidades)
# for i in merge:
#     print(i)
# Gerar a malha de Delaunay 2D
NUM_VERTICES = 100
SPACE_SIZE = 500
delaunay, points, terc_col = gerar_malha_delaunay_2d(NUM_VERTICES, SPACE_SIZE)

# Exibir apenas os pontos da malha 3D com VTK
# exibir_pontos_vtk(points)
aplicar_textura_vtk(img, delaunay, points, terc_col)