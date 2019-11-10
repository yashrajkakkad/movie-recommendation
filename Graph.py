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


def make_set(node, parent, size):
    parent[node] = node
    size[node] = 1


def find_parent(node, parent):
    if node == parent[node]:
        return node
    print(node, parent[node])
    parent[node] = find_parent(parent[node], parent)
    return parent[node]


def union_sets(node1, node2, parent, size):
    node1 = find_parent(node1, parent)
    node2 = find_parent(node2, parent)
    if node1 != node2:
        if size[node1] < size[node2]:
            temp = node1
            node1 = node2
            node2 = temp
        parent[node2] = node1
        size[node2] += size[node1]


def union_colors(graph, nodes):
    # Initialize required variables
    colors = {}
    visited = {}
    queue = []
    parent = {}
    size = {}
    color_parent = {}
    # Mark each initial node with a different color
    count = 10000
    n_colors = len(nodes)
    for i, node in enumerate(nodes):
        colors[node] = i + 1
        # queue.append(node)  # Enqueue all initial nodes
        parent[node] = None
        make_set(i + 1, color_parent, size)  # Initialize the set of that particular color
    for node in nodes:
        for neighbour in graph[node]:
            parent[neighbour] = node
            queue.append(neighbour)
    # Keep merging until only one color remains
    print(n_colors)
    while n_colors != 1 and count:
        count -= 1
        print(n_colors)
        print(len(queue))
        # print(queue)
        node = queue.pop(0)  # Dequeue a node and visit it
        visited[node] = True
        color = None
        try:
            color = find_parent(colors[node], color_parent)
        except KeyError:
            print("Node:", node)
            print(" parent:", parent[node])
            colors[node] = find_parent(colors[parent[node]], color_parent)  # If it is yet to be colored
        print(node, parent[node])
        if color and parent[node]:  # If it is already colored (and has a parent), merge two colors to one
            print("In")
            print(color, colors[parent[node]])
            if find_parent(color, color_parent) != find_parent(colors[parent[node]], color_parent):
                union_sets(color, colors[parent[node]], color_parent, size)
                n_colors -= 1
        # parent_color = colors[parent[node]]
        # while parent[node] != node:
        #     colors[node] = parent_color
        #     node = parent[node]
        # Add the neighbours of the visited queue which are yet to be visited to the queue
        for neighbour in graph[node]:
            try:
                _ = visited[neighbour]
            except KeyError:
                queue.append(neighbour)
                parent[neighbour] = node
    # new_queue = queue
    # for node in queue:  # Return the current and next required number of nodes as a result
    #     for neighbour in graph[node]:
    #         try:
    #             did_visit = visited[neighbour]
    #         except KeyError:
    #             new_queue.append(neighbour)
    #             parent[neighbour] = node
    # queue = new_queue
    print(queue)
    print(colors)
    return queue


if __name__ == "__main__":
    graph = create_graph()
    nodes = ['Comedy', 'Bajirao Mastani', 'Sanjay Leela Bhansali', 'Badlapur', 'Dozakh in Search of Heaven']
    queue = union_colors(graph, nodes)
    print("Final answer: ")
    print(len(queue))
    print(queue)
