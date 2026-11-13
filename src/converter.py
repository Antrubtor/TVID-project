import numpy as np


def clamp(v):
    return np.clip(np.rint(v), 0, 255).astype(np.uint8)


def yuv_to_rgb(y, u, v):
    y = y.astype(np.float64) - 16
    u = u.astype(np.float64) - 128
    v = v.astype(np.float64) - 128

    r = 1.164 * y + 1.596 * v
    g = 1.164 * y - 0.392 * u - 0.813 * v
    b = 1.164 * y + 2.017 * u
    # stack because not anymore a tuple
    return np.stack([clamp(r), clamp(g), clamp(b)], axis=2)


def interpolate_matrix(matrix, first):
    float_matrix = matrix.astype(np.float64)
    rows = np.arange(first, len(matrix) - 1, 2)
    rgb = clamp((float_matrix[rows - 1] + float_matrix[rows + 1]) / 2)
    matrix[rows] = rgb


def vec_to_decoded_vec(matrix, f_width, f_height, ys, hs):
    xs = np.arange(f_width)
    return yuv_to_rgb(
        matrix[ys, :f_width],
        matrix[f_height + hs][:, xs // 2],
        matrix[f_height + hs][:, f_width // 2 + xs // 2],
    )


def matrix_to_decoded_matrix(matrix, to_deinterlace):
    width, height = matrix.shape[1], matrix.shape[0]
    f_width, f_height = width, height - height // 3
    ys = np.arange(f_height)

    if not to_deinterlace:
        return vec_to_decoded_vec(matrix, f_width, f_height, ys, ys // 2)

    else:
        ys_top = ys[0::2]
        ys_bot = ys[1::2]
        hs_top = (ys_top // 4) * 2  # better formula than previously lol
        hs_bot = (ys_bot // 4) * 2 + 1

        # Liste of 3 values rather than simple tuple
        top_field_matrix = np.zeros((f_height, f_width, 3), dtype=np.uint8)
        bot_field_matrix = np.zeros((f_height, f_width, 3), dtype=np.uint8)

        top_field_matrix[0::2] = vec_to_decoded_vec(
            matrix, f_width, f_height, ys_top, hs_top
        )
        bot_field_matrix[1::2] = vec_to_decoded_vec(
            matrix, f_width, f_height, ys_bot, hs_bot
        )

        bot_field_matrix[0] = bot_field_matrix[1]
        interpolate_matrix(top_field_matrix, 1)
        interpolate_matrix(bot_field_matrix, 2)
        top_field_matrix[-1] = top_field_matrix[-2]

        return top_field_matrix, bot_field_matrix
