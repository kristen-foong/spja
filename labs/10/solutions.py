import queue


def parse_graph(path):
    with open(path, "r") as f:
        graph = [[] for _ in range(int(f.readline().strip()))]

        for line in f:
            x, y = line.split("-")
            graph[int(x)].append(int(y.strip()))
        return graph


def shortest_path(graph, source, destination):
    visited = [False] * len(graph)
    q = queue.Queue()
    q.put(source)
    visited[source] = True

    predecessors = [None for _ in graph]

    while not q.empty():
        vertex = q.get()

        if vertex == destination:
            break

        for edge in graph[vertex]:
            if not visited[edge]:
                visited[edge] = True
                predecessors[edge] = vertex
                q.put(edge)

    if not visited[destination]:
        return None

    path = [destination]
    while path[-1] != source:
        path.append(predecessors[path[-1]])

    return path[::-1]


def convex_hull(points):
    # https://stackoverflow.com/a/3461533/1107768
    def on_left(point, start, end):
        a = start
        b = end
        c = point

        return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) > 0

    if not points:
        return []

    points = sorted(points, key=lambda p: p[0])
    hull = []
    onhull = points[0]

    while True:
        hull.append(onhull)
        if onhull == hull[0] and len(hull) > 1:
            break

        endpoint = points[0]
        for p in points:
            if endpoint == onhull or on_left(p, onhull, endpoint):
                endpoint = p
        onhull = endpoint

    return hull


def bonus_shortest_path_weighted(graph, source, destination):
    visited = [False] * len(graph)
    q = queue.PriorityQueue()
    q.put((0, source))

    distance = [10e10] * len(graph)
    distance[source] = 0

    while not q.empty():
        (dist, vertex) = q.get()
        if vertex == destination:
            return dist

        if visited[vertex]:
            continue
        visited[vertex] = True

        for (t, d) in graph[vertex]:
            if visited[t]:
                continue

            new_dist = d + dist
            if new_dist < distance[t]:
                distance[t] = new_dist
                q.put((new_dist, t))

    return None
