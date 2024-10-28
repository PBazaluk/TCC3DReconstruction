import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay
from PIL import Image
import vtk
import cv2
from scipy.spatial import Delaunay


malha1 = [[93, 181, 156], [93, 181, 156], [115, 355, 184], [117, 329, 190], [117, 329, 190], [117, 407, 34], [120, 105, 35], [120, 105, 35], [121, 321, 194], [121, 101, 35], [125, 315, 196], [125, 338, 193], [126, 337, 193], [126, 143, 163], [126, 143, 163], [127, 322, 196], [130, 340, 194], [130, 340, 194], [130, 378, 187], [130, 378, 187], [132, 338, 196], [133, 343, 195], [133, 343, 195], [133, 109, 39], [133, 109, 39], [134, 329, 198], [147, 374, 198], [147, 374, 198], [149, 367, 200], [149, 367, 200], [154, 357, 203], [176, 351, 213], [179, 302, 220], [188, 293, 225], [188, 293, 225], [189, 299, 225], [189, 229, 232], [189, 229, 232], [189, 376, 175], [190, 367, 178], [190, 231, 232], [191, 248, 231], [191, 237, 232], [192, 376, 173], [198, 236, 235], [204, 266, 234], [204, 266, 234], [206, 261, 235], [207, 368, 173], [208, 397, 123], [209, 254, 237], [211, 55, 63], [212, 273, 205], [212, 273, 205], [213, 410, 99], [215, 58, 65], [215, 58, 65], [216, 254, 229], [217, 253, 222], [222, 31, 68], [222, 31, 68], [222, 31, 68], [224, 335, 181], [229, 43, 71], [229, 43, 71], [232, 57, 72], [232, 29, 72], [232, 29, 72], [237, 395, 133], [237, 185, 217], [239, 225, 214], [239, 41, 75], [240, 244, 208], [241, 221, 214], [241, 36, 76], [242, 36, 76], [244, 353, 169], [244, 44, 76], [244, 44, 76], [246, 245, 206], [246, 50, 77], [246, 50, 77], [250, 45, 79], [250, 45, 79], [254, 398, 61], [254, 54, 80], [257, 48, 81], [260, 40, 82], [260, 40, 82], [263, 213, 214], [263, 213, 214], [265, 52, 83], [265, 215, 212], [266, 244, 200], [267, 280, 199], [268, 242, 200], [275, 306, 192], [276, 406, 120], [277, 412, 85], [277, 402, 104], [277, 402, 104], [278, 318, 194], [279, 265, 196], [279, 43, 88], [280, 273, 208], [284, 391, 93], [286, 49, 91], [286, 322, 195], [288, 206, 209], [290, 261, 191], [291, 231, 198], [293, 314, 197], [298, 244, 191], [298, 244, 191], [303, 368, 144], [309, 199, 187], [310, 261, 183], [312, 259, 182], [312, 259, 182], [313, 277, 204], [313, 270, 191], [315, 260, 181], [324, 219, 186], [325, 194, 163], [327, 246, 179], [327, 219, 183], [327, 269, 182], [329, 254, 177], [332, 234, 177], [332, 306, 175], [333, 228, 178], [333, 228, 178], [335, 245, 176], [337, 384, 113], [339, 252, 174], [341, 294, 175], [346, 244, 172], [347, 277, 181], [347, 277, 181], [347, 244, 172], [349, 223, 174], [368, 342, 138], [378, 338, 147], [381, 187, 135], [385, 246, 156], [385, 212, 168], [385, 212, 168], [385, 192, 131], [385, 199, 138], [386, 203, 157], [386, 203, 157], [388, 178, 132], [388, 192, 132], [391, 203, 154], [395, 199, 136], [395, 309, 148], [397, 204, 149], [398, 211, 160], [400, 240, 147], [400, 240, 147], [401, 204, 140], [404, 215, 155], [406, 292, 150], [407, 211, 153], [407, 211, 153], [410, 216, 149], [410, 231, 145], [411, 224, 146], [412, 286, 148], [412, 286, 148], [415, 240, 147], [415, 240, 147], [415, 158, 142], [415, 158, 142], [416, 235, 147], [416, 235, 147], [420, 231, 149], [421, 224, 149], [421, 224, 149], [421, 159, 145]]
malha2 = [[44, 353, 33], [44, 353, 33], [57, 461, 27], [57, 461, 27], [64, 454, 30], [64, 454, 30], [70, 370, 75], [76, 179, 447], [76, 345, 429], [77, 180, 456], [77, 180, 456], [78, 434, 39], [78, 434, 39], [79, 181, 471], [79, 181, 471], [84, 298, 513], [86, 239, 525], [89, 231, 531], [95, 104, 81], [95, 105, 81], [103, 423, 51], [103, 423, 51], [127, 235, 573], [129, 325, 570], [129, 337, 570], [132, 323, 573], [135, 372, 573], [136, 288, 579], [138, 404, 567], [140, 274, 585], [142, 423, 69], [142, 422, 72], [145, 446, 75], [146, 421, 66], [146, 270, 594], [147, 420, 147], [147, 362, 594], [147, 362, 594], [148, 414, 603], [148, 413, 603], [154, 422, 186], [165, 297, 621], [166, 469, 90], [174, 369, 513], [184, 357, 507], [188, 218, 660], [190, 378, 492], [191, 215, 666], [191, 215, 666], [191, 215, 666], [195, 217, 669], [196, 217, 672], [198, 393, 267], [204, 265, 531], [204, 265, 531], [205, 31, 135], [210, 33, 138], [211, 34, 138], [213, 268, 525], [215, 444, 126], [215, 262, 528], [216, 444, 126], [216, 444, 126], [216, 256, 528], [217, 306, 513], [217, 311, 510], [217, 311, 510], [218, 23, 141], [218, 23, 141], [218, 459, 129], [219, 282, 504], [219, 334, 498], [219, 334, 498], [219, 207, 573], [219, 304, 513], [219, 325, 501], [219, 325, 501], [220, 293, 498], [222, 326, 501], [222, 326, 501], [222, 22, 144], [222, 443, 126], [224, 351, 489], [224, 351, 489], [225, 457, 132], [225, 457, 132], [227, 458, 135], [228, 445, 270], [228, 451, 135], [229, 299, 507], [231, 315, 504], [235, 287, 492], [235, 25, 156], [235, 25, 156], [235, 25, 156], [236, 6, 156], [237, 460, 147], [238, 459, 147], [238, 22, 156], [239, 357, 477], [240, 473, 150], [248, 430, 384], [249, 247, 513], [252, 21, 168], [253, 327, 486], [257, 18, 171], [258, 234, 504], [262, 280, 486], [263, 441, 387], [263, 286, 483], [264, 291, 480], [265, 300, 519], [265, 300, 519], [266, 309, 510], [266, 309, 510], [266, 283, 483], [266, 287, 492], [266, 287, 492], [267, 292, 522], [267, 292, 522], [269, 285, 528], [269, 285, 528], [269, 278, 528], [269, 197, 552], [269, 294, 516], [270, 241, 498], [270, 303, 504], [270, 303, 504], [271, 312, 504], [271, 312, 504], [281, 284, 492], [281, 300, 498], [283, 205, 543], [287, 272, 510], [287, 272, 510], [293, 190, 543], [302, 230, 519], [303, 238, 516], [305, 257, 519], [307, 338, 453], [307, 267, 525], [307, 267, 525], [310, 270, 522], [311, 275, 519], [312, 261, 519], [316, 324, 462], [316, 324, 462], [319, 303, 489], [322, 119, 480], [325, 445, 342], [325, 429, 291], [326, 430, 294], [326, 430, 294], [330, 225, 534], [332, 436, 306], [338, 425, 315], [354, 256, 462], [370, 203, 480], [378, 210, 474], [381, 187, 444], [382, 201, 471], [385, 210, 471], [390, 282, 423], [390, 282, 423], [392, 386, 357], [393, 387, 354], [395, 395, 321], [400, 202, 462], [401, 216, 459], [402, 188, 468], [403, 261, 429], [405, 184, 468], [407, 218, 453], [407, 188, 462], [407, 291, 408], [408, 251, 423], [409, 211, 453], [409, 211, 453], [409, 228, 450], [409, 199, 459], [410, 276, 411], [410, 259, 423], [410, 259, 423], [411, 178, 465], [412, 217, 450], [412, 217, 450], [412, 185, 459], [412, 185, 459], [413, 279, 411], [414, 250, 423], [414, 181, 462], [415, 151, 486], [415, 151, 486], [415, 274, 411], [415, 274, 411], [416, 212, 447], [417, 228, 444], [419, 197, 450], [419, 269, 411], [419, 190, 453], [421, 213, 444], [421, 193, 450], [424, 353, 354], [425, 265, 414], [426, 202, 444], [426, 221, 438], [426, 209, 441], [427, 204, 441], [432, 244, 417], [433, 215, 432], [433, 215, 432], [434, 235, 435], [434, 223, 429], [434, 318, 399], [434, 318, 399], [437, 242, 420], [439, 261, 411], [439, 261, 411], [439, 338, 369], [439, 338, 369], [441, 229, 417], [443, 237, 426], [446, 336, 378], [446, 336, 378], [448, 254, 414], [448, 254, 414], [450, 244, 420], [450, 244, 420], [450, 329, 384], [450, 329, 384], [452, 337, 384]]

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
    points = malha2
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
img = cv2.imread('imgs/202.jpg')
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