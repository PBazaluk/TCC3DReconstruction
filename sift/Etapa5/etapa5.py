from PIL import Image
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import Delaunay
import numpy as np
import open3d as o3d

# Abre o arquivo em modo de leitura
with open('resultado_depth.txt', 'r') as file:
    conteudo_depth = file.read()  # Lê o conteúdo do arquivo

# Converte a string lida para uma lista
depth = eval(conteudo_depth)

# Abre o arquivo em modo de leitura
with open('resultado_sift.txt', 'r') as file:
    conteudo_sift = file.read()  # Lê o conteúdo do arquivo

# Converte a string lida para uma lista
sift = eval(conteudo_sift)

# Coloca os respectivos z da matriz depth dentro dos pontos da matriz sift 
cont = 0
for item in sift[0]:
    imagem = 0
    if cont % 2 != 0:
        imagem = 1
    z = depth[imagem][item[1]][item[2]]
    item.append(z)
    cont+=1
    
for i, ig in enumerate(sift[1]):
    for ponto in ig:
        z = depth[i][ponto[0]][ponto[1]]
        ponto.append(z)

# Calcula a proporção média entre os z da imagem 1 em relação a imagem 2
cont1 = 0
proporcao_media = 0
z_temp = 0
id_temp = -1
item_ant = -1
for item in sift[0]:
    z = item[3]
    id = item[0]
    if id == id_temp:
        prop = item_ant[3] / item[3]
        proporcao_media += prop
        cont1+=1
    z_temp = item[3]
    id_temp = item[0]
    item_ant = item   
proporcao_media = proporcao_media / cont1

# Aplica a proporção nas outras imagens que não são a primeira e cria as malhas x y z de todas as imagens
malhas = []
for i, imagem in enumerate(sift[1]):
    malha = []
    for j, ponto in enumerate(imagem):
        if sift[1].index(imagem) != 0:
            sift[1][i][j][2] = int(sift[1][i][j][2] * proporcao_media)
        ponto = []
        sift[1][i][j][2] = 0
        malha.append(sift[1][i][j])
    malhas.append(malha)
    
p = []
def capturar_coordenadas(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Verifica se o evento é um clique do botão esquerdo do mouse
        print(f"Coordenadas: x={x}, y={y}")
        p.append([x,y,depth[1][x][y]])
im = cv2.imread('P:/Vscodigos/sift/Etapa5/imgs/202.jpg')  # Substitua 'imagem.jpg' pelo caminho da sua imagem
largura2 = int(500)
altura2 = int(500)
dimensoes2 = (largura2, altura2)
im = cv2.resize(im, dimensoes2, interpolation=cv2.INTER_AREA) 
cv2.imshow("Imagem", im)
cv2.setMouseCallback("Imagem", capturar_coordenadas)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Criar uma única janela para visualização
vis = o3d.visualization.Visualizer()
vis.create_window()

# Mostra as malhas
for m in malhas:
    x = []
    y = []
    z = []
    for ponto in p:
        x.append(ponto[0])
        y.append(ponto[1])
        z.append(ponto[2])
    # print(z)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    
    tri = Delaunay(np.array([x, y]).T)
    triangles = tri.simplices
    imagem_textura = Image.open("P:/Vscodigos/sift/Etapa5/imgs/202.jpg")  # Substitua pelo caminho da sua imagem de textura
    imagem_textura = np.asarray(imagem_textura) / 255.0  # Normalizar a imagem
    vertices = np.vstack((x, y, z)).T

    malha = o3d.geometry.TriangleMesh()
    malha.vertices = o3d.utility.Vector3dVector(vertices)
    malha.triangles = o3d.utility.Vector3iVector(triangles)

    u = (x - x.min()) / (x.max() - x.min())  # Normalizar coordenadas x para [0, 1]
    v = (y - y.min()) / (y.max() - y.min())  # Normalizar coordenadas y para [0, 1]
    uv = np.vstack((u, v)).T
    malha.triangle_uvs = o3d.utility.Vector2dVector(uv[triangles].reshape(-1, 2))

    malha.textures = [o3d.geometry.Image((imagem_textura * 255).astype(np.uint8))]

    vis.add_geometry(malha)  # Adiciona cada malha à visualização

# Após adicionar todas as malhas, inicia a visualização
vis.run()
vis.destroy_window()
    
    # np.random.seed(0)  # Para reprodutibilidade
    # # points = np.random.rand(30, 3)  # 30 pontos aleatórios em 3D
    # points = np.array(p)
    # tri = Delaunay(points[:, :2])  # Usamos somente x e y para a triangulação
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_trisurf(points[:, 0], points[:, 1], points[:, 2], triangles=tri.simplices, cmap='viridis', edgecolor='k')
    # ax.set_xlabel('Eixo X')
    # ax.set_ylabel('Eixo Y')
    # ax.set_zlabel('Eixo Z')
    # plt.show()
    
    
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(x, y, z, c='b', marker='o')
    # ax.set_xlabel('Eixo X')
    # ax.set_ylabel('Eixo Y')
    # ax.set_zlabel('Eixo Z')
    # plt.show()