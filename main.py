import argparse
import os
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from src.converter import matrix_to_decoded_matrix
from src.image import matrix_to_ppm, pgm_to_matrix

DEFAULT_PACE = 25


def get_arguments():
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
    return parser.parse_args()


def frame_delay_ms(pace, df, i):
    if pace and pace > 0:
        return int(1000 / pace)
    elif df is not None and df.iloc[i]["frame_period"] > 0:
        return int(df.iloc[i]["frame_period"] * 1000 / 27e6)
    else:
        return int(1000 / DEFAULT_PACE)


def main():

    args = get_arguments()

    pgm_path_dir = Path(args.input)
    ppm_path_dir = Path(args.out) if args.out else None
    logs_file = Path.joinpath(pgm_path_dir, "logs.csv")
    pace = args.pace

    if ppm_path_dir:
        os.makedirs(ppm_path_dir, exist_ok=True)

    df = pd.read_csv(logs_file, sep=";") if logs_file.exists() else None
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
            key = cv2.waitKey(frame_delay_ms(pace, df, i))
            if key == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
