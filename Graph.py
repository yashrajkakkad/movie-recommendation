from Movies import load_movies_data, Movie
import pickle


def create_graph():
    graph = {}
    movies = load_movies_data()
    for movie in movies:
        nodes = [movie.title]
        nodes.extend(movie.people)
        nodes.extend(movie.genres)
        for node in nodes:
            for i in range(len(nodes)):
                if node != nodes[i]:
                    try:
                        graph[node].append(nodes[i])
                    except KeyError:
                        graph[node] = [nodes[i]]
    with open('Graph.pickle', 'wb') as f:
        pickle.dump(graph, f)
    return graph


def load_graph():
    with open('Graph.pickle', 'rb') as f:
        graph = pickle.load(f)
    return graph


# def find_parent(node, graph, parent):
#     if parent[node]:
#         return find_parent(parent[node], graph, parent)
#     else:
#         return node


# def disjoint_set_union(node_1, node_2, graph, parent, size):
#     node_1 = find_parent(node_1, graph, parent)
#     node_2 = find_parent(node_2, graph, parent)
#     if node_1 != node_2:
#         if size[node_1] < size[node_2]:
#             temp = node_1
#             node_1 = node_2
#             node_2 = temp
#         parent[node_2] = node_1
#         size[node_2] += size[node_1]


def union_colors(graph, nodes):
    # Initialize required variables
    colors = {}
    visited = {}
    queue = []
    parent = {}
    # size = {}
    # Mark each initial node with a different color
    n_colors = len(nodes)
    for i, node in enumerate(nodes):
        colors[node] = i
        queue.append(node)  # Enqueue all initial nodes
        # visited[node] = True
        parent[node] = node
        # size[node] = 1
    # Keep merging until only one color remains
    while n_colors != 1:
        print(queue)
        node = queue.pop(0)  # Dequeue a node and visit it
        visited[node] = True
        color = None
        try:
            color = colors[node]
        except KeyError:
            colors[node] = colors[parent[node]]  # If it is yet to be colored
        if color:  # If it is already colored, merge two colors to one
            parent_color = colors[parent[node]]
            while parent[node] != node:
                colors[node] = parent_color
                node = parent[node]
            n_colors -= 1
        # Add the neighbours of the visited queue which are yet to be visited to the queue
        for neighbour in graph[node]:
            try:
                did_visit = visited[neighbour]
            except KeyError:
                queue.append(neighbour)
                parent[neighbour] = node
    new_queue = queue
    for node in queue:  # Return the current and next required number of nodes as a result
        for neighbour in graph[node]:
            try:
                did_visit = visited[neighbour]
            except KeyError:
                new_queue.append(neighbour)
                parent[neighbour] = node
    queue = new_queue
    print(queue)
    print(colors)


if __name__ == "__main__":
    graph = create_graph()
    nodes = ['Comedy', 'Bajirao Mastani', 'Sanjay Leela Bhansali', 'Badlapur', 'Dozakh in Search of Heaven']
    union_colors(graph, nodes)
