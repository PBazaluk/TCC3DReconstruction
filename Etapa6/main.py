import vedo
import random
import os

# Nome da pasta onde os arquivos .obj serão salvos
output_folder = 'obj_files'

# Cria a pasta se não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Função para criar uma forma aleatória
def create_random_shape():
    shape_type = random.choice(['sphere', 'cone', 'cube'])
    if shape_type == 'sphere':
        return vedo.Sphere(r=0.5)
    elif shape_type == 'cone':
        return vedo.Cone(r=0.5, height=1)
    elif shape_type == 'cube':
        return vedo.Cube(side=1)
    else:
        raise ValueError("Shape type not recognized")

# Função principal para criar e salvar arquivos .obj
def create_random_obj_files(num_files=5):
    for i in range(num_files):
        shape = create_random_shape()
        # Gerar um nome de arquivo baseado no índice e pasta
        filename = os.path.join(output_folder, f'random_shape_{i}.obj')
        # Salvar a forma como um arquivo .obj
        shape.write(filename)
        print(f'Salvo: {filename}')

if __name__ == "__main__":
    create_random_obj_files()
