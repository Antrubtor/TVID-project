import argparse
import os
from pathlib import Path

import cv2
import numpy as np

from src.converter import matrix_to_decoded_matrix
from src.image import matrix_to_ppm, pgm_to_matrix

FRAME_DELAY_MS = 40  # for 25 fps but isn't that fast for know


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path of the directory to execute the pipeline")
    parser.add_argument(
        "--out",
        help="path of the output directory, if None, then result is only displayed",
    )
    args = parser.parse_args()

    pgm_path_dir = Path(args.input)
    ppm_path_dir = args.out

    if ppm_path_dir:
        os.makedirs(ppm_path_dir, exist_ok=True)

    for pgm_path in sorted(pgm_path_dir.glob("*.pgm"), key=lambda p: int(p.stem)):
        print(f"Processing {pgm_path}...")
        matrix = pgm_to_matrix(pgm_path)
        decoded_matrix = matrix_to_decoded_matrix(matrix)

        if ppm_path_dir:
            ppm_path = os.path.join(ppm_path_dir, f"{pgm_path.stem}.ppm")
            matrix_to_ppm(ppm_path, decoded_matrix)
        else:
            img = np.array(decoded_matrix, np.uint8)
            cv2.imshow("ppm", img)
            key = cv2.waitKey(FRAME_DELAY_MS)
            if key == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
