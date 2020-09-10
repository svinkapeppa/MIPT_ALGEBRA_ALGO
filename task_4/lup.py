from math import ceil, log2


def calculate_degree(size):
    return 2 ** int(ceil(log2(size)))


def get_padded_matrix(size):
    matrix = []

    for _ in range(size):
        zeros = [0] * size
        matrix.append(zeros)

    for i in range(size):
        matrix[i][i] = 1

    return matrix


def get_matrix(size):
    matrix = []

    for _ in range(size):
        zeros = [0] * size
        matrix.append(zeros)

    return matrix


def split_matrix(matrix):
    size = len(matrix[0])
    new_size = size // 2

    matrix11 = []
    matrix12 = []
    matrix21 = []
    matrix22 = []

    for row in matrix[:new_size]:
        matrix11.append(row[:new_size])
        matrix12.append(row[new_size:])

    for row in matrix[new_size:]:
        matrix21.append(row[:new_size])
        matrix22.append(row[new_size:])

    return matrix11, matrix12, matrix21, matrix22


def merge_matrix(res11, res12, res21, res22):
    size = len(res11[0])
    res = get_matrix(2 * size)

    for i in range(size):
        res[i][:size] = res11[i]
        res[i][size:] = res12[i]

    for i in range(size):
        res[i + size][:size] = res21[i]
        res[i + size][size:] = res22[i]

    return res


def matmul(lhs, rhs):
    packed = list(zip(*rhs))
    return [[sum((left * right) % 2 for left, right in zip(row, col)) % 2
             for col in packed] for row in lhs]


def matsub(lhs, rhs):
    height = len(lhs)
    width = len(lhs[0])
    return [[(lhs[i][j] - rhs[i][j]) % 2 for j in range(width)]
            for i in range(height)]


def matsum(lhs, rhs):
    height = len(lhs)
    width = len(lhs[0])
    return [[(lhs[i][j] + rhs[i][j]) % 2 for j in range(width)]
            for i in range(height)]


def split(matrix):
    size = len(matrix) // 2

    up = []
    down = []

    for i in range(size):
        up.append(matrix[i])
        down.append(matrix[i + size])

    return up, down


def crop_left(matrix, size):
    height = len(matrix)

    cropped = []

    for i in range(height):
        cropped += [matrix[i][:size]]

    return cropped


def crop_right(matrix, size):
    height = len(matrix)

    cropped = []

    for i in range(height):
        cropped += [matrix[i][-size:]]

    return cropped


def invert_permutation(matrix):
    inverted = []

    for i in range(len(matrix)):
        tmp = []

        for j in range(len(matrix[0])):
            tmp += [matrix[i][j]]

        inverted.append(tmp)

    for i in range(len(inverted)):
        for j in range(i, len(inverted[0])):
            inverted[i][j], inverted[j][i] = inverted[j][i], inverted[i][j]

    return inverted


def invert(matrix):
    if len(matrix) == 1:
        return [[1]]

    degree = calculate_degree(len(matrix))
    matrix_pad = get_padded_matrix(degree)

    for idx, row in enumerate(matrix):
        matrix_pad[idx][:len(row)] = row

    b, c, zero, d = split_matrix(matrix_pad)

    b_invert = invert(b)
    d_invert = invert(d)
    delta = strassen(strassen(b_invert, c), d_invert)

    inverted = merge_matrix(b_invert, delta, zero, d_invert)

    tmp = []
    for _ in range(len(matrix)):
        zeros = [0] * len(matrix)
        tmp.append(zeros)

    for idx, row in enumerate(inverted[:len(matrix)]):
        tmp[idx] = row[:len(matrix)]

    return tmp


def get_permutation_matrix(size, column):
    matrix = []

    for _ in range(size):
        zeros = [0] * size
        matrix.append(zeros)

    for i in range(size):
        matrix[i][i] = 1

    matrix[0][0] = 0
    matrix[column][column] = 0
    matrix[0][column] = 1
    matrix[column][0] = 1

    return matrix


def construct_permutation(size, down):
    p = size + len(down[0])

    matrix = []

    for _ in range(p):
        zeros = [0] * p
        matrix.append(zeros)

    for i in range(size):
        matrix[i][i] = 1

    for i in range(len(down)):
        for j in range(len(down[0])):
            matrix[i + size][j + size] = down[i][j]

    return matrix


def construct_l(left_up, left_down, right_down):
    size = len(left_up[0])

    matrix = []

    for _ in range(size * 2):
        zeros = [0] * (size * 2)
        matrix.append(zeros)

    for i in range(size):
        for j in range(size):
            matrix[i][j] = left_up[i][j]
            matrix[i + size][j] = left_down[i][j]
            matrix[i + size][j + size] = right_down[i][j]

    return matrix


def construct_u(up, down):
    height = len(up)
    width = len(up[0])

    matrix = []

    for _ in range(height * 2):
        zeros = [0] * width
        matrix.append(zeros)

    for i in range(height):
        for j in range(width):
            matrix[i][j] = up[i][j]

    for i in range(height):
        for j in range(len(down[0])):
            matrix[i + height][j + height] = down[i][j]

    return matrix


def strassen(lhs, rhs):
    lhs_degree = calculate_degree(max(len(lhs), len(lhs[0])))
    rhs_degree = calculate_degree(max(len(rhs), len(rhs[0])))
    degree = max(lhs_degree, rhs_degree)

    lhs_pad = get_matrix(degree)
    rhs_pad = get_matrix(degree)

    for idx, row in enumerate(lhs):
        lhs_pad[idx][:len(row)] = row

    for idx, row in enumerate(rhs):
        rhs_pad[idx][:len(row)] = row

    if len(lhs_pad[0]) <= 8:
        tmp = matmul(lhs_pad, rhs_pad)

        matrix = []
        for _ in range(len(lhs)):
            zeros = [0] * len(rhs[0])
            matrix.append(zeros)

        for idx, row in enumerate(tmp[:len(lhs)]):
            matrix[idx] = row[:len(rhs[0])]

        return matrix

    lhs11, lhs12, lhs21, lhs22 = split_matrix(lhs_pad)
    rhs11, rhs12, rhs21, rhs22 = split_matrix(rhs_pad)

    p1 = strassen(matsum(lhs11, lhs22), matsum(rhs11, rhs22))
    p2 = strassen(matsum(lhs21, lhs22), rhs11)
    p3 = strassen(lhs11, matsub(rhs12, rhs22))
    p4 = strassen(lhs22, matsub(rhs21, rhs11))
    p5 = strassen(matsum(lhs11, lhs12), rhs22)
    p6 = strassen(matsub(lhs21, lhs11), matsum(rhs11, rhs12))
    p7 = strassen(matsub(lhs12, lhs22), matsum(rhs21, rhs22))

    res11 = matsum(matsum(p1, p4), matsub(p7, p5))
    res12 = matsum(p3, p5)
    res21 = matsum(p2, p4)
    res22 = matsum(matsub(p1, p2), matsum(p3, p6))

    tmp = merge_matrix(res11, res12, res21, res22)

    matrix = []
    for _ in range(len(lhs)):
        zeros = [0] * len(rhs[0])
        matrix.append(zeros)

    for idx, row in enumerate(tmp[:len(lhs)]):
        matrix[idx] = row[:len(rhs[0])]

    return matrix


def decompose(matrix, height, width):
    if height == 1:
        column = matrix[0].index(1)
        permutation = get_permutation_matrix(width, column)
        return [[1]], strassen(matrix, permutation), permutation

    b, c = split(matrix)
    l_1, u_1, p_1 = decompose(b, height // 2, width)
    d = strassen(c, invert_permutation(p_1))
    e = crop_left(u_1, height // 2)
    f = crop_left(d, height // 2)
    g = matsub(d, strassen(strassen(f, invert(e)), u_1))
    gg = crop_right(g, width - height // 2)
    l_2, u_2, p_2 = decompose(gg, height // 2, width - height // 2)
    p_3 = construct_permutation(height // 2, p_2)
    h = strassen(u_1, invert_permutation(p_3))

    l = construct_l(l_1, strassen(f, invert(e)), l_2)
    u = construct_u(h, u_2)
    p = strassen(p_3, p_1)

    return l, u, p


def pprint(matrix, size):
    for row in matrix[:size]:
        print(*row[:size])


if __name__ == '__main__':
    row = list(map(int, input().split()))
    size = len(row)

    degree = calculate_degree(size)
    matrix = get_padded_matrix(degree)

    for idx, element in enumerate(row):
        matrix[0][idx] = element

    for i in range(1, size):
        row = list(map(int, input().split()))

        for idx, element in enumerate(row):
            matrix[i][idx] = element

    l, u, p = decompose(matrix, degree, degree)

    pprint(l, size)
    pprint(u, size)
    pprint(p, size)
