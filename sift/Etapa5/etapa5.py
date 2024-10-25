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
        # sift[1][i][j][2] = 0
        malha.append(sift[1][i][j])
    malhas.append(malha)
    
merge = []
output_file = "malhas.txt"
with open(output_file, 'w') as f:
    for i in malhas:
        f.write(str(i))
        # for j in i:

            # f.write(str(j))
            # f.write("\n")
        f.write("--------------------\n")
