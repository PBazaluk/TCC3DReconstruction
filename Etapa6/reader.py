import os
import numpy as np
from scipy.spatial import KDTree

class ShapeLoader:
    def __init__(self, tolerance=1e-5):
        self.tolerance = tolerance
    
    def load_shape_from_obj(self, file_path):
        try:
            vertices = []
            faces = []
            with open(file_path) as f:
                for line in f:
                    if line.startswith("v "):
                        vertex = list(map(float, line[2:].strip().split()))
                        vertices.append(vertex)
                    elif line.startswith("f "):
                        face = [int(idx.split('/')[0]) - 1 for idx in line[2:].strip().split()]
                        faces.append(face)

            shape_data = {"vertices": vertices, "faces": faces}
            return shape_data

        except FileNotFoundError:
            print(f"{file_path} not found.")
        except Exception as e:
            print(f"An error occurred while loading the shape: {e}")

    def load_all_shapes_from_folder(self, folder_path):
        shape_data_list = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.obj'):
                file_path = os.path.join(folder_path, file_name)
                print(f"Loading {file_path}...")
                shape_data = self.load_shape_from_obj(file_path)
                if shape_data:
                    shape_data_list.append(shape_data)
        return shape_data_list

    def merge_shapes(self, shape_data_list):
        all_vertices = []
        all_faces = []
        
        for shape_data in shape_data_list:
            all_vertices.extend(shape_data['vertices'])
        
        all_vertices_np = np.array(all_vertices)
        all_vertices_np = self._remove_duplicates_with_tolerance(all_vertices_np)
        vertex_map = {tuple(vertex): idx for idx, vertex in enumerate(all_vertices_np)}
        
        def map_faces(faces):
            mapped_faces = []
            for face in faces:
                mapped_face = []
                for vertex_idx in face:
                    vertex = tuple(all_vertices[vertex_idx])
                    if vertex in vertex_map:
                        mapped_face.append(vertex_map[vertex])
                    else:
                        print(f"Warning: Vertex {vertex} not found in vertex_map")
                mapped_faces.append(mapped_face)
            return mapped_faces
        
        for shape_data in shape_data_list:
            all_faces.extend(map_faces(shape_data['faces']))
        
        return all_vertices_np.tolist(), all_faces
    
    def _remove_duplicates_with_tolerance(self, vertices):
        # Use a KDTree for fast spatial queries
        tree = KDTree(vertices)
        unique_indices = set()
        for idx, vertex in enumerate(vertices):
            neighbors = tree.query_ball_point(vertex, r=self.tolerance)
            unique_indices.add(min(neighbors))
        unique_indices = sorted(unique_indices)
        return np.array(vertices)[unique_indices]

    def write_merged_obj(self, vertices, faces, output_folder, output_file):
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        output_path = os.path.join(output_folder, output_file)
        
        with open(output_path, 'w') as file:
            for vertex in vertices:
                file.write(f"v {' '.join(map(str, vertex))}\n")
            for face in faces:
                file.write(f"f {' '.join(str(idx + 1) for idx in face)}\n")

if __name__ == "__main__":
    shape_loader = ShapeLoader()
    input_folder = 'C:/Users/danie/Downloads/tcc_dan/tcc_dan/obj_files'
    output_folder = 'C:/Users/danie/Downloads/tcc_dan/tcc_dan/merged_shapes'
    
    all_shapes = shape_loader.load_all_shapes_from_folder(input_folder)

    if all_shapes:
        merged_vertices, merged_faces = shape_loader.merge_shapes(all_shapes)
        
        output_file = 'combined_shapes.obj'
        shape_loader.write_merged_obj(merged_vertices, merged_faces, output_folder, output_file)
        
        print(f'Merged shape saved to {os.path.join(output_folder, output_file)}')
    else:
        print("No shapes were loaded. Exiting.")
