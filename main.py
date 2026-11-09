import os

from src.converter import matrix_to_decoded_matrix
from src.image import matrix_to_ppm, pgm_to_matrix

ENCODED_IMAGES_DIR = "encoded_images"
DECODED_IMAGES_DIR = "decoded_images"

DIRECTORIES = ["bw_numbers", "Jaggies1", "lci", "pendulum"]


def main():

    for directory in DIRECTORIES:
        dir = os.fsencode(f"{ENCODED_IMAGES_DIR}/{directory}")
        for file in os.listdir(dir):
            filename = os.fsdecode(file)
            if not filename.endswith(".pgm"):
                continue
            path = f"{ENCODED_IMAGES_DIR}/{directory}/{filename}"
            f_path = f"{DECODED_IMAGES_DIR}/{directory}/{filename}"
            os.makedirs(os.path.dirname(f_path), exist_ok=True)

            matrix = pgm_to_matrix(path)
            decoded_matrix = matrix_to_decoded_matrix(matrix)
            matrix_to_ppm(f_path, decoded_matrix)
            print(path)


if __name__ == "__main__":
    main()
