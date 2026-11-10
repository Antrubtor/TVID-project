import argparse
import os
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from src.converter import matrix_to_decoded_matrix
from src.image import matrix_to_ppm, pgm_to_matrix


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input", type=str, help="path of the directory to execute the pipeline"
    )
    parser.add_argument(
        "--out",
        type=str,
        help="path of the output directory, if None, then result is only displayed",
    )
    parser.add_argument("--pace", type=int, help="give the wanted pace")
    args = parser.parse_args()

    pgm_path_dir = Path(args.input)
    ppm_path_dir = args.out
    logs_file = Path.joinpath(pgm_path_dir, "logs.csv")

    frame_delay_ms = 1000 // args.pace if args.pace else -1

    if ppm_path_dir:
        os.makedirs(ppm_path_dir, exist_ok=True)

    df = pd.read_csv(logs_file, sep=";")
    for pgm_path in sorted(pgm_path_dir.glob("*.pgm"), key=lambda p: int(p.stem)):
        print(f"Processing {pgm_path}...")
        i = int(pgm_path.stem)

        matrix = pgm_to_matrix(pgm_path)
        decoded_matrix = matrix_to_decoded_matrix(matrix)

        if ppm_path_dir:
            ppm_path = os.path.join(ppm_path_dir, f"{pgm_path.stem}.ppm")
            matrix_to_ppm(ppm_path, decoded_matrix)
        else:
            img = np.array(decoded_matrix, np.uint8)
            cv2.imshow("ppm", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            frame_delay_ms = int(
                frame_delay_ms
                if frame_delay_ms != -1
                else 27e6 / df.iloc[i]["frame_period"]
            )
            print(f"Frame delay: {frame_delay_ms} ms")
            key = cv2.waitKey(frame_delay_ms)
            if key == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
