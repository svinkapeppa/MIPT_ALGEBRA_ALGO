def get_vertices(edges):
    vertices = {}

    for edge in edges:
        if edge[0] not in vertices:
            vertices[edge[0]] = len(vertices)
        if edge[1] not in vertices:
            vertices[edge[1]] = len(vertices)

    return vertices


def get_edges(edges):
    dictionary = {}

    for edge in edges:
        if edge[0] not in dictionary:
            dictionary[edge[0]] = [edge[1]]
        else:
            dictionary[edge[0]] += [edge[1]]

    return dictionary


def get_adjacency_matrix(vertices, edges):
    matrix = []
    num_vertices = len(vertices)

    for i in range(num_vertices):
        zeros = [0] * num_vertices
        matrix.append(zeros)

    for v_out in edges.keys():
        idx_v_out = vertices[v_out]
        count = len(edges[v_out])

        for v_in in edges[v_out]:
            idx_v_in = vertices[v_in]
            matrix[idx_v_in][idx_v_out] = 1 / count

    for vertex in vertices:
        if vertex not in edges.keys():
            for i in range(num_vertices):
                matrix[i][vertices[vertex]] = 1 / num_vertices

    return matrix


def get_teleportation_matrix(num_vertices):
    matrix = []

    for i in range(num_vertices):
        row = [1 / num_vertices] * num_vertices
        matrix.append(row)

    return matrix


def matsum(lhs, rhs):
    size = len(lhs)
    return [[lhs[i][j] + rhs[i][j] for j in range(size)] for i in range(size)]


def matmul(lhs, rhs):
    packed = list(zip(*rhs))
    return [[sum(left * right for left, right in zip(row, col))
             for col in packed] for row in lhs]


def mul(matrix, factor):
    size = len(matrix)
    return [[matrix[i][j] * factor for j in range(size)] for i in range(size)]


def get_rank(vertices, edges, p):
    num_vertices = len(vertices)

    z = []
    for _ in range(num_vertices):
        z.append([1 / num_vertices])

    a = get_adjacency_matrix(vertices, edges)
    b = get_teleportation_matrix(num_vertices)
    m = matsum(mul(a, 1 - p), mul(b, p))

    for _ in range(10000):
        z = matmul(m, z)

    return z


if __name__ == '__main__':
    p = float(input())
    num_edges = int(input())

    edges = []
    for i in range(num_edges):
        edge = input().split()
        edges.append([edge[0], edge[1]])

    vertices = get_vertices(edges)
    edges = get_edges(edges)
    rank = get_rank(vertices, edges, p)

    for vertex, idx in vertices.items():
        print(vertex, rank[idx][0])
