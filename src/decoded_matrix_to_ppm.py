import os


def decoded_matrix_to_ppm(path, decoded_matrix):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode="w") as f:
        width, height = len(decoded_matrix[0]), len(decoded_matrix)
        f.write(f"P3\n{width} {height}\n255\n")

        for y in range(height):
            for x in range(width):
                f.writelines(
                    f"{decoded_matrix[y][x][0]} {decoded_matrix[y][x][1]} {decoded_matrix[y][x][2]}\n"
                )
