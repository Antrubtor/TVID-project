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


def matrix_to_decoded_matrix(matrix):
    width, height = len(matrix[0]), len(matrix)
    f_width, f_height = width, height - height // 3
    f_matrix = [[(-1, -1, -1)] * f_width for _ in range(f_height)]
    for y in range(f_height):
        for x in range(f_width):
            f_matrix[y][x] = yuv_to_rgb(
                matrix[y][x],
                matrix[f_height + y // 2][x // 2],
                matrix[f_height + y // 2][f_width // 2 + x // 2],
            )
    return f_matrix


def matrix_to_decoded_multiple_matrices(matrix):
    width, height = len(matrix[0]), len(matrix)
    f_width, f_height = width, height - height // 3
    top_field_matrix = [[(-1, -1, -1)] * f_width for _ in range(f_height)]
    bot_field_matrix = [[(-1, -1, -1)] * f_width for _ in range(f_height)]

    for y in range(f_height):
        if y % 2 == 0:
            for x in range(f_width):
                # top field
                mid_height = y // 2
                h = mid_height if (mid_height) % 2 == 0 else mid_height - 1
                top_field_matrix[y][x] = yuv_to_rgb(
                    matrix[y][x],
                    matrix[f_height + h][x // 2],
                    matrix[f_height + h][f_width // 2 + x // 2],
                )
        else:
            for x in range(f_width):
                # bottom field
                mid_height = y // 2
                h = mid_height + 1 if (mid_height % 2) == 0 else mid_height
                bot_field_matrix[y][x] = yuv_to_rgb(
                    matrix[y][x],
                    matrix[f_height + h][x // 2],  # TODO
                    matrix[f_height + h][f_width // 2 + x // 2],  # TODO
                )

    bot_field_matrix[0] = bot_field_matrix[1]

    # To try:
    # NewColor = sqrt((R1^2+R2^2)/2),sqrt((G1^2+G2^2)/2),sqrt((B1^2+B2^2)/2)

    for y in range(1, f_height - 1):
        if y % 2 == 0:
            for x in range(f_width):
                # bottom field
                r = (bot_field_matrix[y - 1][x][0] + bot_field_matrix[y + 1][x][0]) / 2
                g = (bot_field_matrix[y - 1][x][1] + bot_field_matrix[y + 1][x][1]) / 2
                b = (bot_field_matrix[y - 1][x][2] + bot_field_matrix[y + 1][x][2]) / 2
                bot_field_matrix[y][x] = (clamp(r), clamp(g), clamp(b))
        else:
            for x in range(f_width):
                # top field
                r = (top_field_matrix[y - 1][x][0] + top_field_matrix[y + 1][x][0]) / 2
                g = (top_field_matrix[y - 1][x][1] + top_field_matrix[y + 1][x][1]) / 2
                b = (top_field_matrix[y - 1][x][2] + top_field_matrix[y + 1][x][2]) / 2
                top_field_matrix[y][x] = clamp(r), clamp(g), clamp(b)

    top_field_matrix[-1] = top_field_matrix[-2]

    return top_field_matrix, bot_field_matrix
