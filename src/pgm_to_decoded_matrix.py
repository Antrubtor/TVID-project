def pgm_to_matrix(path):
    with open(path, mode="rb") as f:
        f.readline()
        line = f.readline().split()
        width, height = int(line[0]), int(line[1])
        lines = f.read()

    matrix = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            matrix[y][x] = int(lines[y * width + x])
    return matrix


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
