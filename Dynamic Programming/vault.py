import functools
import sys
import time

sys.setrecursionlimit(2000)


def parse(filename):
    mat_map = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        mat_map.append([int(x) for x in line.split(',')])

    return mat_map


def vault(matrix: list[list[int]]):
    height = len(matrix)
    width = len(matrix[0])
    directions = [['' for _ in range(width)] for _ in range(height)]

    @functools.lru_cache(maxsize=25000)
    def find_path(i: int, j: int):
        if i == 0 and j == 0:
            return 0
        if i < 0 or j < 0:
            return -1

        north_val = find_path(i - 1, j)
        west_val = find_path(i, j - 1)
        if north_val < west_val:
            directions[i][j] = 'W'
            return west_val + matrix[i][j]
        else:
            directions[i][j] = 'N'
            return north_val + matrix[i][j]

    max_val = find_path(height - 1, width - 1)
    return max_val, directions


if __name__ == "__main__":
    file_name = sys.argv[1]
    mat = parse(file_name)
    time.perf_counter_ns()
    max_value, direction = vault(mat)
    result = []
    i, j = len(direction) - 1, len(direction[0]) - 1
    while i >= 0 and j >= 0:
        result.append(direction[i][j])
        if direction[i][j] == "W":
            j -= 1
        elif direction[i][j] == "N":
            i -= 1
        else:
            break
    print(''.join(result))
    print(max_value)
