import numpy as np
import cv2 as cv
import glob
import os
import matplotlib.pyplot as plt

# Diretórios das imagens e de saída
image_dir = 'P:/Vscodigos/sift/Etapa2/imgs'
image_out = 'P:/Vscodigos/sift/Etapa2/imgswd'

# Listar todos os arquivos de imagem no diretório
image_files = glob.glob(os.path.join(image_dir, '*.jpg'))

print("image files:", image_files)

# Inicializar dicionários e lista
vector = {}
imgs_des = {}
imgs_kp = {}
sift_kp = []
lista = []
lista_images =[]
img = 0


img_shadow = 0
path_img = "P:/Vscodigos/sift/Etapa2/imgsombra/202_img_depth.png"
img_shadow = cv.imread(path_img)
img_draw = 0
# Processar cada imagem
for file in image_files:
    img = cv.imread(file)
    
    largura = int(500)
    altura = int(500)
    dimensoes = (largura, altura)

    # Redimensionar a imagem
    img = cv.resize(img, dimensoes, interpolation=cv.INTER_AREA)
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Criar o detector SIFT
    sift = cv.SIFT_create(
        nfeatures=0,               # Define o número máximo de pontos a ser detectado (0 para ilimitado)
        contrastThreshold=0.01,    # Reduzir para detectar mais pontos em áreas de baixo contraste
        edgeThreshold=3            # Reduzir para detectar mais pontos nas bordas
    )
    
    # Detectar keypoints e calcular descritores
    kp, des = sift.detectAndCompute(gray, None)

    ##print("cord" , kp)
    # print(kp[0].pt)
    
    
    # Ordenar keypoints com base na resposta e selecionar os melhores
    #keypoints = sorted(kp, key=lambda x: x.response, reverse=True)
    #num_best_keypoints = 4000
    #keypoints = keypoints[:num_best_keypoints]
    lista_images.append(gray)
    # Desenhar os keypoints na imagem

    img_with_keypoints = cv.drawKeypoints(gray, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    output_file = os.path.splitext(file)[0] + '_keypoints.jpg'
    novo_path = output_file.replace("imgs", "imgswd")
    cv.imwrite(novo_path, img_with_keypoints)
    lista.append(novo_path)
    vector[kp]  = des
    imgs_des[novo_path] = des
    imgs_kp[novo_path] = kp
    sift_kp.append(kp)

# Cria o objeto BFMatcher para encontrar correspondências entre os descritores
bf = cv.BFMatcher(cv.NORM_L2, crossCheck=True)

# Encontra as correspondências entre os descritores das duas imagens
matches = bf.match(imgs_des[lista[0]], imgs_des[lista[1]])

# Ordena as correspondências pela distância (quanto menor, melhor)
matches = sorted(matches, key=lambda x: x.distance)


#print("metches" , matches)

# Controle o número de correspondências a serem desenhadas
numero_de_matches = 5000  # Altere este valor para controlar quantas correspondências deseja exibir


# Função para verificar se duas linhas se cruzam
def linhas_se_cruzam(p1, p2, q1, q2):
    def orientacao(a, b, c):
        return (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    
    o1 = orientacao(p1, p2, q1)
    o2 = orientacao(p1, p2, q2)
    o3 = orientacao(q1, q2, p1)
    o4 = orientacao(q1, q2, p2)
    
    return o1 * o2 < 0 and o3 * o4 < 0

# Filtrar correspondências que não cruzam outras linhas
matches_filtrados = []

for i in range(len(matches)):

    pt1_1 = imgs_kp[lista[0]][matches[i].queryIdx].pt
    pt2_1 = (imgs_kp[lista[1]][matches[i].trainIdx].pt[0] + lista_images[0].shape[1], imgs_kp[lista[1]][matches[i].trainIdx].pt[1])
    
    cruza = False
    for j in range(len(matches_filtrados)):
        pt1_2 = imgs_kp[lista[0]][matches_filtrados[j].queryIdx].pt
        pt2_2 = (imgs_kp[lista[1]][matches_filtrados[j].trainIdx].pt[0] + lista_images[0].shape[1], imgs_kp[lista[1]][matches_filtrados[j].trainIdx].pt[1])
        
        if linhas_se_cruzam(pt1_1, pt2_1, pt1_2, pt2_2):
            cruza = True
            break
    
    if not cruza:
        matches_filtrados.append(matches[i])
    
    if len(matches_filtrados) >= numero_de_matches:
        break



# Cria uma imagem para exibir as correspondências lado a lado
imagem_matches = cv.hconcat([lista_images[0], lista_images[1]])



# Desenha manualmente as correspondências com linhas mais grossas
for match in matches_filtrados:

    pt1 = tuple(map(int, imgs_kp[lista[0]][match.queryIdx].pt))
    pt2 = (int(imgs_kp[lista[1]][match.trainIdx].pt[0] + lista_images[0].shape[1]), int(imgs_kp[lista[1]][match.trainIdx].pt[1]))
    cv.line(imagem_matches, pt1, pt2, (0, 0, 255), 5)  # Cor verde e espessura 3

#print(matches_filtrados)

# Lista para armazenar os keypoints e descritores correspondentes
kp_matches_img1 = []
des_matches_img1 = []
kp_matches_img2 = []
des_matches_img2 = []

# Iterar sobre os matches filtrados
cont = 0
matriz = [[0 for _ in range(4)] for _ in range(100)]
for match in matches_filtrados:
    
    #print(cont)
    idx_img1 = match.queryIdx
    idx_img2 = match.trainIdx
    kp_img1 = imgs_kp[lista[0]][idx_img1]
    des_img1 = imgs_des[lista[0]][idx_img1]
    kp_img2 = imgs_kp[lista[1]][idx_img2]
    des_img2 = imgs_des[lista[1]][idx_img2]
    
    kp_matches_img1.append(kp_img1)
    des_matches_img1.append(des_img1)
    kp_matches_img2.append(kp_img2)
    des_matches_img2.append(des_img2)
    matriz[cont][0] = kp_img1
    matriz[cont][1] = des_img1
    matriz[cont][2] = kp_img2
    matriz[cont][3] = des_img2
    cont+=1



# Nome do arquivo de saída
output_file = 'resultado_sift.txt'



# Abre o arquivo para escrita
with open(output_file, 'w') as f:
    f.write("[")
    f.write("[")
    for i in range(cont):
        kp_img1 = matriz[i][0]
        #print(f'Imagem 1 - Keypoint {i}: Localização (x, y): {kp_img1.pt}')
        f.write(f'[{i},{int(kp_img1.pt[0])},{int(kp_img1.pt[1])}],\n')
        
        # Imprime e grava no arquivo a localização dos keypoints da segunda imagem
        kp_img2 = matriz[i][2]
        #print(f'Imagem 2 - Keypoint {i}: Localização (x, y): {kp_img2.pt}')
        f.write(f'[{i},{int(kp_img2.pt[0])},{int(kp_img2.pt[1])}],\n')
    f.write("],\n")
    f.write("[")
    for ig in sift_kp:
        f.write("[")
        for i in ig:
            f.write(f'[{int(i.pt[0])},{int(i.pt[1])}],\n')
        f.write("],\n")
    f.write("],\n")
            
    f.write("]")


    
    #for i in range(cont):  # Só itera até o número de correspondências processadas
        #for j in range(4):
            #f.write(str(matriz[i][j]) )  # Espaço entre os valores
            
            #f.write('\n')
        #f.write('\n')  # Nova linha após cada linha da matriz
        
for item in imgs_kp[lista[1]]:
    cv.circle(img_shadow,(int(item.pt[0]),int(item.pt[1])),2,(0,0,255),2)
    
#Exibe a imagem com as correspondências
largura1 = int(500)
altura1 = int(500)
dimensoes1 = (largura1, altura1)
largura2 = int(500)
altura2 = int(500)
dimensoes2 = (largura2, altura2)

# Redimensionar a imagem
img_redimensionada1 = cv.resize(img_shadow, dimensoes1, interpolation=cv.INTER_AREA)
img_redimensionada2 = cv.resize(img, dimensoes2, interpolation=cv.INTER_AREA)

i = cv.hconcat([img_redimensionada1, img_redimensionada2])
# cv.imshow('Imagem', i)
# cv.waitKey(0)
plt.figure(figsize=(15, 10))
plt.imshow(cv.cvtColor(imagem_matches, cv.COLOR_BGR2RGB))
plt.title(f'Correspondências entre as duas perspectivas usando SIFT ({len(matches_filtrados)} matches)')
plt.axis('off')
plt.show()

# Iteramos sobre o dicionário para encontrar a chave correspondente ao valor





















# FLANN parameters
# FLANN_INDEX_KDTREE = 1
# index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
# search_params = dict(checks=50)   # or pass empty dictionary
# flann = cv.FlannBasedMatcher(index_params,search_params)
# matches = flann.knnMatch(imgs_des[lista[0]],imgs_des[lista[1]],k=2)
# # Need to draw only good matches, so create a mask
# matchesMask = [[0,0] for i in range(len(matches))]
# # ratio test as per Lowe's paper
# for i,(m,n) in enumerate(matches):
#     if m.distance < 0.7*n.distance:
#         matchesMask[i]=[1,0]
# draw_params = dict(matchColor = (0,255,0),
#                    singlePointColor = (255,0,0),
#                    matchesMask = matchesMask,
#                    flags = cv.DrawMatchesFlags_DEFAULT)

# img3 = cv.drawMatchesKnn(lista_images[0],imgs_kp[lista[0]],lista_images[1],imgs_kp[lista[1]],matches,None,**draw_params)
# plt.imshow(img3,),plt.show()