import cv2 as cv
import numpy as np
import os
import glob

def load_images(image_paths):
    images = []
    for path in image_paths:
        img = cv.imread(path)
        if img is not None:
            images.append(img)
    return images

def stitch_images(images):
    # Inicializar a imagem composta com a primeira imagem
    composed_image = images[0]
    altura, largura = composed_image.shape[:2]

    for i in range(1, len(images)):
        img2 = images[i]
        altura2, largura2 = img2.shape[:2]

        # Detectar pontos chave e calcular a homografia
        sift = cv.SIFT_create()
        kp1, des1 = sift.detectAndCompute(composed_image, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        bf = cv.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Aplicar a razão de Lowe para selecionar boas correspondências
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 2)

        H, _ = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

        # Transformar a imagem composta
        altura_total = max(altura, altura2)
        largura_total = largura + largura2
        composed_image = cv.warpPerspective(composed_image, H, (largura_total, altura_total))

        # Colocar a próxima imagem na composição
        composed_image[0:altura2, 0:largura2] = img2

        # Atualizar as dimensões da imagem composta
        altura, largura = composed_image.shape[:2]

    return composed_image

def main(image_paths, output_path):
    images = load_images(image_paths)
    if len(images) < 2:
        print("É necessário pelo menos duas imagens para compor.")
        return

    composed_image = stitch_images(images)

    # Converter a imagem resultante para escala de cinza
    gray_warped = cv.cvtColor(composed_image, cv.COLOR_BGR2GRAY)

    # Encontrar a região não preta
    _, thresh = cv.threshold(gray_warped, 1, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv.boundingRect(contours[0])

    # Recortar a imagem para remover as áreas pretas
    img_final = composed_image[y:y+h, x:x+w]

    # Exibir a imagem final
    cv.imshow('Imagem Final', img_final)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Salvar a imagem composta em um arquivo
    cv.imwrite(output_path, img_final)
    print(f'Imagem composta salva em: {output_path}')

if __name__ == "__main__":
    # Obter o diretório atual do script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Diretórios das imagens e de saída
    image_dir = os.path.join(current_dir, 'Entrada')
    image_out = os.path.join(current_dir, 'Saida')

    # Listar todos os arquivos de imagem no diretório
    image_files = glob.glob(os.path.join(image_dir, '*.jpg'))
    print("image files:", image_files)

    output_path = os.path.join(image_out, 'imagem_composta.jpg')
    main(image_files, output_path)