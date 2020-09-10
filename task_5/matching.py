import random

MODULE = 2777


def get_multiplication_table(module):
    table = {}

    for i in range(1, module):
        for j in range(1, module):
            if (i * j) % module == 1:
                table[i] = j

    return table


def get_num_vertices(edges):
    vertex = 0

    for edge in edges:
        if edge[0] > vertex:
            vertex = edge[0]
        if edge[1] > vertex:
            vertex = edge[1]

    return vertex + 1


def get_index(row):
    for idx, elem in enumerate(row):
        if elem != 0:
            return idx

    return None


def swap_columns(matrix, lhs, rhs):
    for i in range(len(matrix)):
        matrix[i][lhs], matrix[i][rhs] = matrix[i][rhs], matrix[i][lhs]


def multiply_row(matrix, table, index):
    factor = table[matrix[index][index]]

    for i in range(len(matrix[0])):
        matrix[index][i] = (matrix[index][i] * factor) % MODULE


def subtract_row(matrix, lhs, rhs):
    factor = matrix[lhs][rhs]

    for i in range(len(matrix[0])):
        matrix[lhs][i] = (matrix[lhs][i] - factor * matrix[rhs][i]) % MODULE


def step(matrix, table, index):
    multiply_row(matrix, table, index)

    for i in range(len(matrix)):
        if i == index:
            continue

        subtract_row(matrix, i, index)


def is_degenerate(matrix, table):
    for i in range(len(matrix)):
        index = get_index(matrix[i])

        if index is None:
            return True

        swap_columns(matrix, i, index)
        step(matrix, table, i)

    return False


if __name__ == '__main__':
    num_edges = int(input())

    edges = []
    for i in range(num_edges):
        edge = list(map(int, input().split()))
        edges.append(edge)

    num_vertices = get_num_vertices(edges)

    matrix = []
    for i in range(num_vertices):
        zeros = [0] * num_vertices
        matrix.append(zeros)

    for edge in edges:
        matrix[edge[0]][edge[1]] = random.randint(0, MODULE - 1)

    table = get_multiplication_table(MODULE)

    if is_degenerate(matrix, table):
        print('no')
    else:
        print('yes')
