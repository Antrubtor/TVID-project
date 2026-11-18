def clamp(v):
    return max(0, min(255, round(v)))


def yuv_to_rgb(y, u, v):
    y -= 16
    u -= 128
    v -= 128

    r = 1.164 * y + 1.596 * v
    g = 1.164 * y - 0.392 * u - 0.813 * v
    b = 1.164 * y + 2.017 * u
    return clamp(r), clamp(g), clamp(b)


def interpolate_matrix(matrix, f_width, y):
    for x in range(f_width):
        r = (matrix[y - 1][x][0] + matrix[y + 1][x][0]) / 2
        g = (matrix[y - 1][x][1] + matrix[y + 1][x][1]) / 2
        b = (matrix[y - 1][x][2] + matrix[y + 1][x][2]) / 2
        matrix[y][x] = (clamp(r), clamp(g), clamp(b))


def vec_to_decoded_vec(final_matrix, matrix, f_width, f_height, y, h):
    for x in range(f_width):
        final_matrix[y][x] = yuv_to_rgb(
            matrix[y][x],
            matrix[f_height + h][x // 2],
            matrix[f_height + h][f_width // 2 + x // 2],
        )


def matrix_to_decoded_matrix(matrix, to_deinterlace):
    width, height = len(matrix[0]), len(matrix)
    f_width, f_height = width, height - height // 3

    if not to_deinterlace:
        final_matrix = [[(-1, -1, -1)] * f_width for _ in range(f_height)]
        for y in range(f_height):
            vec_to_decoded_vec(final_matrix, matrix, f_width, f_height, y, y // 2)
        return final_matrix

    else:
        top_field_matrix = [[(-1, -1, -1)] * f_width for _ in range(f_height)]
        bot_field_matrix = [[(-1, -1, -1)] * f_width for _ in range(f_height)]

        for y in range(f_height):
            if y % 2 == 0:
                mid_height = y // 2
                h = mid_height if (mid_height) % 2 == 0 else mid_height - 1
                vec_to_decoded_vec(top_field_matrix, matrix, f_width, f_height, y, h)
            else:
                mid_height = y // 2
                h = mid_height + 1 if (mid_height % 2) == 0 else mid_height
                vec_to_decoded_vec(bot_field_matrix, matrix, f_width, f_height, y, h)

        # To try:
        # NewColor = sqrt((R1^2+R2^2)/2),sqrt((G1^2+G2^2)/2),sqrt((B1^2+B2^2)/2)

        bot_field_matrix[0] = bot_field_matrix[1]

        for y in range(1, f_height - 1):
            if y % 2 == 0:
                interpolate_matrix(bot_field_matrix, f_width, y)
            else:
                interpolate_matrix(top_field_matrix, f_width, y)

        top_field_matrix[-1] = top_field_matrix[-2]

        return top_field_matrix, bot_field_matrix
