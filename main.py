import argparse
import os

from src.converter import matrix_to_decoded_matrix
from src.image import matrix_to_ppm, pgm_to_matrix

ENCODED_IMAGES_DIR = "encoded_images"
DECODED_IMAGES_DIR = "decoded_images"

# DIRECTORIES = ["bw_numbers"]
DIRECTORIES = ["bw_numbers", "Jaggies1", "lci", "pendulum"]


def pgm_to_ppm(pgm_path: str, ppm_path: str):
    os.makedirs(os.path.dirname(ppm_path), exist_ok=True)

    matrix = pgm_to_matrix(pgm_path)
    decoded_matrix = matrix_to_decoded_matrix(matrix)
    matrix_to_ppm(ppm_path, decoded_matrix)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="path of the file to execute the pipeline")
    parser.add_argument("--out", help="path of the output file if --input is not None")
    args = parser.parse_args()

    if args.input:
        pgm_path = args.input
        if args.out:
            ppm_path = args.out
        else:
            ppm_path = pgm_path.replace("encoded_images", "decoded_images").replace(
                ".pgm", ".ppm"
            )
        os.makedirs(os.path.dirname(ppm_path), exist_ok=True)

        pgm_to_ppm(pgm_path, ppm_path)
        return

    for directory in DIRECTORIES:
        dir = os.fsencode(f"{ENCODED_IMAGES_DIR}/{directory}")

        for file in os.listdir(dir):
            filename = os.fsdecode(file)
            if not filename.endswith(".pgm"):
                continue

            pgm_path = f"{ENCODED_IMAGES_DIR}/{directory}/{filename}"
            ppm_path = f"{DECODED_IMAGES_DIR}/{directory}/{filename}".replace(
                ".pgm", ".ppm"
            )
            os.makedirs(os.path.dirname(ppm_path), exist_ok=True)
            print(f"{pgm_path} -> {ppm_path}")
            pgm_to_ppm(pgm_path, ppm_path)


if __name__ == "__main__":
    main()
