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


def matrix_to_ppm(path, matrix):
    with open(path, mode="w") as f:
        width, height = len(matrix[0]), len(matrix)
        f.write(f"P3\n{width} {height}\n255\n")

        for y in range(height):
            for x in range(width):
                f.writelines(f"{matrix[y][x][0]} {matrix[y][x][1]} {matrix[y][x][2]}\n")
