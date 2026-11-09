def pgm_to_matrix(path):
    f = open(path, mode="rb")
    type = f.readline().split()[0] # P5, mais inutile
    line = f.readline().split()
    width, height = int(line[0]), int(line[1])
    max_value = int(f.readline().split()[0])

    lines = f.read()
    f.close()

    matrix = [[0] * width for i in range(height)]
    for y in range(height):
        for x in range(width):
            matrix[y][x] = int(lines[y * width + x])
    return matrix, max_value

def clamp(v, max_value):
    return max(0, min(max_value, round(v)))

def matrix_to_decoded_matrix(matrix, max_value):
    width, height = len(matrix[0]), len(matrix)
    f_width, f_height = width, height - height // 3
    f_matrix = [[(-1, -1, -1)] * f_width for i in range(f_height)]
    for y in range(f_height):
        for x in range(f_width):
            Y = matrix[y][x] - 16
            U = matrix[f_height + y // 2][x // 2] - 128
            V = matrix[f_height + y // 2][f_width // 2 + x // 2] - 128
            R = 1.164 * Y + 1.596 * V
            G = 1.164 * Y - 0.392 * U - 0.813 * V
            B = 1.164 * Y + 2.017 * U
            f_matrix[y][x] = (clamp(R, max_value), clamp(G, max_value), clamp(B, max_value))
    return f_matrix
