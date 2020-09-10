def get_num_vertices(edges):
    num_vertices = 0

    for edge in edges:
        num_vertices = max(num_vertices, edge[0])
        num_vertices = max(num_vertices, edge[1])

    return num_vertices


def get_selected_edges(edges, candidate):
    selected_edges = []

    for edge in edges:
        if edge[0] < candidate and edge[1] < candidate:
            selected_edges.append(edge)

    return selected_edges


def is_face(edges, candidate):
    # Seems to be OK, as first `candidate` amount of vertices is a face
    return len(edges) == candidate


def get_num_vertices_in_face(edges, num_vertices):
    for candidate in range(3, num_vertices):
        selected_edges = get_selected_edges(edges, candidate)
        if is_face(selected_edges, candidate):
            return candidate

    # Seems to be unreachable given all the constraints
    return None


def get_links(edges):
    links = {}

    for edge in edges:
        if edge[0] not in links:
            links[edge[0]] = {edge[1]}
        else:
            links[edge[0]].add(edge[1])

        if edge[1] not in links:
            links[edge[1]] = {edge[0]}
        else:
            links[edge[1]].add(edge[0])

    for key, value in links.items():
        links[key] = list(value)

    return links


def get_face_coordinates(links, num_vertices):
    coordinates = {}

    vertex = 0
    center = (num_vertices - 1) // 2

    for i in range(num_vertices):
        x = i - center
        coordinates[vertex] = [x, x ** 2]

        if i == num_vertices - 1:
            break

        idx = 0
        while True:
            if links[vertex][idx] not in coordinates and links[vertex][idx] < num_vertices:
                vertex = links[vertex][idx]
                break
            idx += 1

    return coordinates


def get_coordinate(coordinates, axis):
    coordinate = {}

    for key, value in coordinates.items():
        coordinate[key] = value[axis]

    return coordinate


def construct_system(links, coordinates, num_vertices, num_vertices_in_face):
    size = num_vertices - num_vertices_in_face

    matrix = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        matrix[i][i] = len(links[i + num_vertices_in_face])

    for i in range(size):
        for j in range(i + 1, size):
            v_out = i + num_vertices_in_face
            v_in = j + num_vertices_in_face

            if v_in in links[v_out]:
                matrix[i][j] = -1
                matrix[j][i] = -1

    center = []

    for i in range(size):
        v_out = i + num_vertices_in_face
        tmp = 0

        for vertex in links[v_out]:
            if vertex < num_vertices_in_face:
                tmp += coordinates[vertex]

        center.append(tmp)

    return matrix, center


def solve(matrix, center):
    size = len(center)

    for i in range(size):
        if matrix[i][i] == 0:
            idx = None

            for j in range(i + 1, size):
                if matrix[j][i] != 0:
                    idx = j
                    break

            for j in range(size):
                matrix[i][j], matrix[idx][j] = matrix[idx][j], matrix[i][j]

            center[i], center[idx] = center[idx], center[i]

        factor = matrix[i][i]

        for j in range(size):
            matrix[i][j] /= factor

        center[i] /= factor

        for j in range(size):
            if j == i:
                continue

            factor = matrix[j][i]

            for k in range(size):
                matrix[j][k] -= factor * matrix[i][k]

            center[j] -= factor * center[i]

    return center


if __name__ == '__main__':
    num_edges = int(input())

    edges = []

    for _ in range(num_edges):
        edge = list(map(int, input().split()))
        edges.append(edge)

    num_vertices = get_num_vertices(edges) + 1
    num_vertices_in_face = get_num_vertices_in_face(edges, num_vertices)

    links = get_links(edges)
    coordinates = get_face_coordinates(links, num_vertices_in_face)
    coordinates_x = get_coordinate(coordinates, 0)
    coordinates_y = get_coordinate(coordinates, 1)

    matrix_x, center_x = construct_system(links, coordinates_x, num_vertices, num_vertices_in_face)
    matrix_y, center_y = construct_system(links, coordinates_y, num_vertices, num_vertices_in_face)

    x = solve(matrix_x, center_x)
    y = solve(matrix_y, center_y)

    for i in range(num_vertices - num_vertices_in_face):
        coordinates[i + num_vertices_in_face] = [x[i], y[i]]

    for key, value in coordinates.items():
        print(key, *value)
