import sys
from functools import lru_cache

sys.setrecursionlimit(2000)


def mat(name, dim):
    @lru_cache(maxsize=500000)
    def least_cal(i, j):
        if i == j:
            return 0, dim[i][0], dim[i][1], (name[i])
        cal_times = float('inf')
        min_rows, min_cols = 0, 0
        index = -1
        for k in range(i, j):
            left_times, left_rows, left_columns, left_name = least_cal(i, k)
            right_times, right_rows, right_columns, right_name = least_cal(k + 1, j)
            total = left_times + right_times + left_rows * left_columns * right_columns
            if total < cal_times:
                cal_times = total
                min_rows, min_cols = left_rows, right_columns
                index = k
        _, _, _, left = least_cal(i, index)
        _, _, _, right = least_cal(index + 1, j)
        return cal_times, min_rows, min_cols, (left, right)

    return least_cal(0, len(dim) - 1)


def parse(filename):
    name, dim = [], []
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.rstrip('\n')
        parts = line.split(',')
        name.append(parts[0])
        dim.append((int(parts[1]), int(parts[2])))
    return name, dim


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to provide one file\n")
    else:
        file_name = sys.argv[1]
        matrix, mat_dim = parse(file_name)
        min_op, _, _, expr = mat(matrix, mat_dim)
        print(min_op)
        print(expr)
