import os

from src.converter import matrix_to_decoded_matrix
from src.image import matrix_to_ppm, pgm_to_matrix


def main():
    directories = ["bw_numbers", "Jaggies1", "lci", "pendulum"]
    for directory in directories:
        dir = os.fsencode(f"encoded_images/{directory}")
        for file in os.listdir(dir):
            filename = os.fsdecode(file)
            if not filename.endswith(".pgm"):
                continue
            path = f"encoded_images/{directory}/{filename}"
            f_path = f"decoded_images/{directory}/{filename}"
            os.makedirs(os.path.dirname(f_path), exist_ok=True)

            matrix = pgm_to_matrix(path)
            decoded_matrix = matrix_to_decoded_matrix(matrix)
            matrix_to_ppm(f_path, decoded_matrix)
            print(path)


if __name__ == "__main__":
    main()
