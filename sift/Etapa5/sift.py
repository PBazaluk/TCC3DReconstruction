import numpy as np
import cv2 as cv
import glob
import os
import matplotlib.pyplot as plt

# Diretórios das imagens e de saída
image_dir = '/home/pedro/Documents/TCC/GitHub/TCC3DReconstruction/sift/Etapa5/imgs/'
image_out = '/home/pedro/Documents/TCC/GitHub/TCC3DReconstruction/sift/Etapa5/'

# Listar todos os arquivos de imagem no diretório
image_files = glob.glob(os.path.join(image_dir, '*.jpg'))
print("image files:", image_files)

# Carregar as imagens para combinar
img1 = cv.imread(image_files[0])
img2 = cv.imread(image_files[1])

# Converter para escala de cinza
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

# Criar o detector SIFT
sift = cv.SIFT_create()

# Detectar keypoints e calcular descritores para as duas imagens
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

# Criar o objeto BFMatcher para encontrar correspondências entre os descritores
bf = cv.BFMatcher(cv.NORM_L2, crossCheck=True)

# Encontra as correspondências entre os descritores das duas imagens
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)

# Controle o número de correspondências a serem usadas para a matriz homográfica
numero_de_matches = 50  # Altere este valor para controlar quantas correspondências deseja usar

# Obter os pontos correspondentes das correspondências
src_pts = np.float32([kp1[m.queryIdx].pt for m in matches[:numero_de_matches]]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches[:numero_de_matches]]).reshape(-1, 1, 2)

# Calcular a matriz homográfica
H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

# Usar a homografia para transformar a primeira imagem e compô-la com a segunda
altura, largura = img2.shape[:2]
img1_warped = cv.warpPerspective(img1, H, (largura * 2, altura))

# Colocar a segunda imagem na composição ao lado da primeira imagem transformada
img1_warped[0:altura, 0:largura] = img2

# Exibir a imagem composta
plt.figure(figsize=(15, 10))
plt.imshow(cv.cvtColor(img1_warped, cv.COLOR_BGR2RGB))
plt.title('Composição das duas imagens com alinhamento baseado em SIFT')
plt.axis('off')
plt.show()

# Salvar a imagem composta em um arquivo
output_path = os.path.join(image_out, 'imagem_composta.jpg')
cv.imwrite(output_path, img1_warped)
print(f'Imagem composta salva em: {output_path}')