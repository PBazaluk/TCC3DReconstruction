import numpy as np
import cv2 as cv
import glob
import os
import matplotlib.pyplot as plt

# Obter o diretório atual do script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Diretórios das imagens e de saída
image_dir = os.path.join(current_dir, 'Entrada')
image_out = os.path.join(current_dir, 'Saida')

# Listar todos os arquivos de imagem no diretório
image_files = glob.glob(os.path.join(image_dir, '*.jpg'))
print("image files:", image_files)

# Carregar as imagens para combinar
img1 = cv.imread(image_files[0])
img2 = cv.imread(image_files[1])

# Converter as imagens para escala de cinza
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

# Converter a imagem resultante para escala de cinza
gray_warped = cv.cvtColor(img1_warped, cv.COLOR_BGR2GRAY)

# Encontrar a região não preta
_, thresh = cv.threshold(gray_warped, 1, 255, cv.THRESH_BINARY)
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
x, y, w, h = cv.boundingRect(contours[0])

# Recortar a imagem para remover as áreas pretas
img_final = img1_warped[y:y+h, x:x+w]

# Redimensionar a imagem para 500x500 pixels
img_final_resized = cv.resize(img_final, (500, 500))

# Exibir a imagem final
cv.imshow('Imagem Final', img_final_resized)
cv.waitKey(0)
cv.destroyAllWindows()

# Salvar a imagem composta em um arquivo
output_path = os.path.join(image_out, 'imagem_composta.jpg')
cv.imwrite(output_path, img_final)
print(f'Imagem composta salva em: {output_path}')