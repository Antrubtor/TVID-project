import argparse
import os
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from src.converter import matrix_to_decoded_matrix, matrix_to_decoded_multiple_matrices
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
        "--progressive_frame", type=int, help="give the wanted progressive_frame"
    )
    parser.add_argument(
        "--top_field_first", type=int, help="give the wanted top_field_first"
    )
    parser.add_argument(
        "--repeat_first_field", type=int, help="give the wanted repeat_first_field"
    )
    return parser.parse_args()


def frame_delay_ms(pace, frame_period):
    if pace and pace > 0:
        return int(1000 / pace)
    elif frame_period is not None and frame_period > 0:
        return int(frame_period * 1000 / 27e6)
    else:
        return int(1000 / DEFAULT_PACE)


def save_or_display_ppm(ppm_path_dir, pgm_path, position, matrix, pace, frame_period):
    if ppm_path_dir:
        ppm_path = os.path.join(ppm_path_dir, f"{pgm_path.stem}_{position}.ppm")
        matrix_to_ppm(ppm_path, matrix)
    else:
        img = np.array(matrix, np.uint8)
        cv2.imshow("ppm", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        key = cv2.waitKey(frame_delay_ms(pace, frame_period))
        if key == ord("q"):
            return True
    return False


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

    for pgm_path in sorted(pgm_path_dir.glob("*.pgm"), key=lambda p: int(p.stem)):
        print(f"Processing {pgm_path}...")
        i = int(pgm_path.stem)

        progressive_frame = (
            progressive_frame_input
            if progressive_frame_input
            else df.iloc[i]["progressive_frame"]  # type: ignore
        )
        top_field_first = (
            top_field_first_input
            if top_field_first_input
            else df.iloc[i]["top_field_first"]  # type: ignore
        )
        repeat_first_field = (
            repeat_first_field_input
            if repeat_first_field_input
            else df.iloc[i]["repeat_first_field"]  # type: ignore
        )
        frame_period = df.iloc[i]["frame_period"]  # type: ignore

        matrix = pgm_to_matrix(pgm_path)

        if progressive_frame == 1:
            decoded_matrix = matrix_to_decoded_matrix(matrix)

            if ppm_path_dir:
                ppm_path = os.path.join(ppm_path_dir, f"{pgm_path.stem}.ppm")
                matrix_to_ppm(ppm_path, decoded_matrix)
            else:
                img = np.array(decoded_matrix, np.uint8)
                cv2.imshow("ppm", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                key = cv2.waitKey(frame_delay_ms(pace, frame_period))
                if key == ord("q"):
                    break
        else:
            top_field_matrix, bot_field_matrix = matrix_to_decoded_multiple_matrices(
                matrix
            )

            if top_field_first:
                save_or_display_ppm(
                    ppm_path_dir,
                    pgm_path,
                    "first",
                    top_field_matrix,
                    pace,
                    frame_period,
                )
                save_or_display_ppm(
                    ppm_path_dir,
                    pgm_path,
                    "second",
                    bot_field_matrix,
                    pace,
                    frame_period,
                )
                if repeat_first_field:
                    save_or_display_ppm(
                        ppm_path_dir,
                        pgm_path,
                        "third",
                        top_field_matrix,
                        pace,
                        frame_period,
                    )
            else:
                save_or_display_ppm(
                    ppm_path_dir,
                    pgm_path,
                    "first",
                    bot_field_matrix,
                    pace,
                    frame_period,
                )
                save_or_display_ppm(
                    ppm_path_dir,
                    pgm_path,
                    "second",
                    top_field_matrix,
                    pace,
                    frame_period,
                )
                if repeat_first_field:
                    save_or_display_ppm(
                        ppm_path_dir,
                        pgm_path,
                        "third",
                        bot_field_matrix,
                        pace,
                        frame_period,
                    )

            # TODO

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
