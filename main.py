from src.decoded_matrix_to_ppm import decoded_matrix_to_ppm, os
from src.pgm_to_decoded_matrix import matrix_to_decoded_matrix, pgm_to_matrix


def main():
    directories = ["bw_numbers", "Jaggies1", "lci", "pendulum"]
    for directory in directories:
        dir = os.fsencode(f"encoded_images/{directory}")
        for file in os.listdir(dir):
            filename = os.fsdecode(file)
            path = f"encoded_images/{directory}/{filename}"
            f_path = f"decoded_images/{directory}/{filename}"
            matrix = pgm_to_matrix(path)
            decoded_matrix = matrix_to_decoded_matrix(matrix)
            decoded_matrix_to_ppm(f_path, decoded_matrix)
            print(path)


if __name__ == "__main__":
    main()
