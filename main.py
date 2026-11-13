import argparse
import os
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from src.converter import (
    matrix_to_decoded_matrix,
)
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
    parser.add_argument(
        "--progressive_frame",
        type=int,
        choices=[0, 1],
        help="give the wanted progressive_frame",
    )
    parser.add_argument(
        "--top_field_first",
        type=int,
        choices=[0, 1],
        help="give the wanted top_field_first",
    )
    parser.add_argument(
        "--repeat_first_field",
        type=int,
        choices=[0, 1],
        help="give the wanted repeat_first_field",
    )
    return parser.parse_args()


# J'ai update de ms -> s car j'utilise time.perf_coutner qui est en s.
def frame_duration_s(pace, frame_period):
    if pace and pace > 0:
        return 1 / pace
    if frame_period is not None and frame_period > 0:
        return frame_period / 27e6
    return 1 / DEFAULT_PACE


def save_or_display_ppm(ppm_path_dir, name, matrix, chrono):
    if ppm_path_dir:
        ppm_path = os.path.join(ppm_path_dir, f"{name}.ppm")
        matrix_to_ppm(ppm_path, matrix)
        return False

    img = np.array(matrix, np.uint8)
    cv2.imshow("ppm", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    remaining_ms = round((chrono - time.perf_counter()) * 1000)
    key = cv2.waitKey(max(1, remaining_ms))
    return key == ord("q")


def main():

    args = get_arguments()

    pgm_path_dir = Path(args.input)
    ppm_path_dir = Path(args.out) if args.out else None
    logs_file = Path.joinpath(pgm_path_dir, "logs.csv")
    pace = args.pace

    progressive_frame_input = args.progressive_frame
    top_field_first_input = args.top_field_first
    repeat_first_field_input = args.repeat_first_field

    if ppm_path_dir:
        os.makedirs(ppm_path_dir, exist_ok=True)

    df = pd.read_csv(logs_file, sep=";") if logs_file.exists() else None

    # https://www.geeksforgeeks.org/python/time-perf_counter-function-in-python/
    chrono = time.perf_counter()

    for pgm_path in sorted(pgm_path_dir.glob("*.pgm"), key=lambda p: int(p.stem)):
        print(f"Processing {pgm_path}...")
        i = int(pgm_path.stem)

        progressive_frame = (
            progressive_frame_input
            if progressive_frame_input is not None
            else df.iloc[i]["progressive_frame"]
            if df is not None and i < len(df)
            else 1
        )
        top_field_first = (
            top_field_first_input
            if top_field_first_input is not None
            else df.iloc[i]["top_field_first"]
            if df is not None and i < len(df)
            else 1
        )
        repeat_first_field = (
            repeat_first_field_input
            if repeat_first_field_input is not None
            else df.iloc[i]["repeat_first_field"]
            if df is not None and i < len(df)
            else 0
        )
        frame_period = (
            df.iloc[i]["frame_period"] if df is not None and i < len(df) else None
        )

        matrix = pgm_to_matrix(pgm_path)

        if progressive_frame == 1:
            decoded_matrix = matrix_to_decoded_matrix(matrix, False)
            images = [("", decoded_matrix)]
            duration = frame_duration_s(pace, frame_period)
        else:
            top_field_matrix, bot_field_matrix = matrix_to_decoded_matrix(matrix, True)
            if top_field_first:
                first, second = top_field_matrix, bot_field_matrix
            else:
                first, second = bot_field_matrix, top_field_matrix

            images = [("_first", first), ("_second", second)]
            if repeat_first_field:
                images.append(("_third", first))
            duration = frame_duration_s(pace, frame_period) / 2

        stop = False
        for suffix, image in images:
            chrono += duration
            if save_or_display_ppm(
                ppm_path_dir, f"{pgm_path.stem}{suffix}", image, chrono
            ):
                stop = True
                break
        if stop:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
