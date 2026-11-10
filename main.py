import argparse
import os

import cv2
import numpy as np

from src.converter import matrix_to_decoded_matrix
from src.image import matrix_to_ppm, pgm_to_matrix


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path of the file to execute the pipeline")
    parser.add_argument(
        "--out", help="path of the output file, if None, then result is only displayed"
    )
    args = parser.parse_args()

    pgm_path = args.input

    matrix = pgm_to_matrix(pgm_path)
    decoded_matrix = matrix_to_decoded_matrix(matrix)

    if args.out:
        ppm_path = args.out
        if not "/" in ppm_path:
            ppm_path = "./" + ppm_path
        os.makedirs(os.path.dirname(ppm_path), exist_ok=True)
        matrix_to_ppm(ppm_path, decoded_matrix)
    else:
        img = np.array(decoded_matrix, np.uint8)
        cv2.imshow("ppm", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
