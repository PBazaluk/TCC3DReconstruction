import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import os

class ShapeLoader:
    def load_shape_from_obj(self, file_path):
        try:
            vertices = []
            faces = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("v "):
                        vertex = list(map(float, line[2:].strip().split()))
                        vertices.append(vertex)
                    elif line.startswith("f "):
                        face = [int(part.split('/')[0]) - 1 for part in line[2:].strip().split()]
                        faces.append(face)

            shape_data = {"vertices": np.array(vertices), "faces": faces}
            return shape_data

        except FileNotFoundError:
            print(f"{file_path} not found.")
        except Exception as e:
            print(f"An error occurred while loading the shape: {e}")

    def visualize_shape(self, shape_data):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        vertices = shape_data['vertices']
        faces = shape_data['faces']

        poly3d = Poly3DCollection([vertices[face] for face in faces], facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25)
        ax.add_collection3d(poly3d)

        scale = vertices.flatten()
        ax.auto_scale_xyz(scale, scale, scale)

        plt.show()

if __name__ == "__main__":
    shape_loader = ShapeLoader()
    output_folder = r'C:\Users\danie\Downloads\tcc_dan\tcc_dan\merged_shapes'  
    file_name = 'combined_shapes.obj' 
    file_path = os.path.join(output_folder, file_name)
    
    shape_data = shape_loader.load_shape_from_obj(file_path)
    
    if shape_data:
        shape_loader.visualize_shape(shape_data)
