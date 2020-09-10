from math import log2, ceil


def calculate_degree(size):
    return 2 ** int(ceil(log2(size)))


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
    return [[sum((left * right) % 9 for left, right in zip(row, col)) % 9
             for col in packed] for row in lhs]


def matsum(lhs, rhs):
    size = len(lhs[0])
    return [[(lhs[i][j] + rhs[i][j]) % 9 for j in range(size)]
            for i in range(size)]


def matsub(lhs, rhs):
    size = len(lhs[0])
    return [[(lhs[i][j] - rhs[i][j]) % 9 for j in range(size)]
            for i in range(size)]


def strassen(lhs, rhs):
    if len(lhs[0]) <= 8:
        return matmul(lhs, rhs)

    lhs11, lhs12, lhs21, lhs22 = split_matrix(lhs)
    rhs11, rhs12, rhs21, rhs22 = split_matrix(rhs)

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

    return merge_matrix(res11, res12, res21, res22)


def power(matrix, n):
    if n == 1:
        return matrix
    if n % 2 == 1:
        return strassen(power(matrix, n - 1), matrix)
    return strassen(power(matrix, int(n / 2)), power(matrix, int(n / 2)))


def pprint(matrix, size):
    for row in matrix[:size]:
        print(*row[:size])


if __name__ == '__main__':
    row = list(map(int, input().split()))
    size = len(row)

    degree = calculate_degree(size)
    matrix = get_matrix(degree)

    for idx, element in enumerate(row):
        matrix[0][idx] = element

    for i in range(size - 1):
        row = list(map(int, input().split()))

        for idx, element in enumerate(row):
            matrix[i + 1][idx] = element

    result = power(matrix, size)
    pprint(result, size)
