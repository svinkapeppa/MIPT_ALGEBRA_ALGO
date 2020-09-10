import numpy as np


def calculate_density(candidate, num_vertices, edges):
    density = 0
    rest = list(set(list(range(num_vertices))).difference(set(candidate)))

    for v_out in candidate:
        for v_in in edges[v_out]:
            if v_in in rest:
                density += 1

    density = density * num_vertices / (len(candidate) * (num_vertices - len(candidate)))

    return density


if __name__ == '__main__':
    num_edges = int(input())

    edges = {}
    vertex_mapping = {}
    vertex_mapping_reverse = {}

    for _ in range(num_edges):
        v_out, v_in = list(map(int, input().split()))

        if v_out not in vertex_mapping:
            vertex_mapping_reverse[len(vertex_mapping)] = v_out
            vertex_mapping[v_out] = len(vertex_mapping)

        if v_in not in vertex_mapping:
            vertex_mapping_reverse[len(vertex_mapping)] = v_in
            vertex_mapping[v_in] = len(vertex_mapping)

        v_out = vertex_mapping[v_out]
        v_in = vertex_mapping[v_in]

        if v_out not in edges:
            edges[v_out] = {v_in}
        else:
            edges[v_out].add(v_in)

        if v_in not in edges:
            edges[v_in] = {v_out}
        else:
            edges[v_in].add(v_out)

    laplacian = [[0 for _ in range(len(vertex_mapping))] for _ in range(len(vertex_mapping))]

    for i in range(len(vertex_mapping)):
        laplacian[i][i] = len(edges[i])

    for v_out, vertices in edges.items():
        for vertex in vertices:
            laplacian[v_out][vertex] = -1

    vector = [(idx, value) for idx, value in enumerate(np.linalg.eigh(laplacian)[1][:, 1])]
    permutation = [idx for idx, _ in sorted(vector, key=lambda x: -x[1])]

    candidates = []
    min_density = np.inf
    for i in range(1, len(permutation) // 2):
        candidate = permutation[:i]

        density = calculate_density(candidate, len(vertex_mapping), edges)
        if density == min_density:
            candidates.append(candidate)
        elif density < min_density:
            candidates = [candidate]
            min_density = density

    answers = []
    for candidate in candidates:
        vertices = sorted([vertex_mapping_reverse[vertex] for vertex in candidate])
        answers.append(vertices)

    print(*min(answers))
