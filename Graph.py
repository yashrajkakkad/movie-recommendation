from Movies import load_movies_data, Movie
import pickle
from operator import itemgetter
from collections import OrderedDict


def create_graph(mode):
    graph = {}
    movie_titles = []
    movies = load_movies_data()
    for movie in movies:
        nodes = [movie.title]
        movie_titles.append(movie.title)
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
    if mode is 1:
        return graph
    else:
        return movie_titles


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
        # Initialize the set of that particular color
        make_set(i + 1, color_parent, size)
    for node in nodes:
        for neighbour in graph[node]:
            parent[neighbour] = node
            if neighbour not in queue:
                queue.append(neighbour)
    # Keep merging until only one color remains
    # print(n_colors)
    while n_colors != 1 and count:
        count -= 1
        # print(n_colors)
        # print(len(queue))
        # print(queue)
        node = queue.pop(0)  # Dequeue a node and visit it
        visited[node] = True
        color = None
        try:
            color = find_parent(colors[node], color_parent)
        except KeyError:
            # print("Node:", node)
            # print(" parent:", parent[node])
            # If it is yet to be colored
            colors[node] = find_parent(colors[parent[node]], color_parent)
        print(node, parent[node])
        # If it is already colored (and has a parent), merge two colors to one
        if color and parent[node]:
            # print("In")
            # print(color, colors[parent[node]])
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
                if neighbour not in queue:
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
    # print(queue)
    # print(colors)
    return queue


def energy_spread(graph, nodes):
    # Init variables
    energy_values = {}  # Energies of initial nodes
    neighbor_energy_values = {}  # Energies of neighbors of initial nodes
    visited = {}
    queue = []
    parent = {}
    movie_titles = create_graph(0)
    for node in nodes:
        energy_values[node] = 5000*len(nodes)  # Assign arbitrary energy values
        queue.append(node)  # Enqueue initial nodes
        parent[node] = node
    for i in range(len(nodes)):
        # print(queue)
        node = queue.pop(0)
        visited[node] = True
        if node is 'Comedy':
            print(graph[node])
        for neighbor in graph[node]:
            energy_value = None
            try:
                did_visit = visited[neighbor]
            except KeyError:
                if neighbor not in queue:
                    queue.append(neighbor)
                parent[neighbor] = node
                try:  # Add new energy value if already exists
                    energy_value = neighbor_energy_values[neighbor]
                    neighbor_energy_values[neighbor] = energy_value + \
                        (energy_values[parent[node]]/len(graph[node]))
                except KeyError:
                    neighbor_energy_values[neighbor] = (
                        energy_values[parent[node]]/len(graph[node]))
    final_energy_values = {}  # Energy values of neighbor movies
    # print(queue)
    for node in queue:
        for neighbor in graph[node]:
            energy_value = None
            if neighbor in movie_titles:
                try:  # Add new energy value if already exists
                    energy_value = final_energy_values[neighbor]
                    final_energy_values[neighbor] = energy_value + \
                        (neighbor_energy_values[node]/len(graph[node]))
                except KeyError:
                    final_energy_values[neighbor] = neighbor_energy_values[node] / \
                        len(graph[node])
    sorted_values = OrderedDict(sorted(final_energy_values.items(),  # Sort using OrderedDict to maintain order
                                       key=itemgetter(1)))
    for node in nodes:
        deleted_pair = sorted_values.pop(node, None)
    return sorted_values


if __name__ == "__main__":
    graph = create_graph(1)
    nodes = ['Grand Masti', 'Dhoom 3',
             'Chennai Express']
    # nodes = ['Bajirao Mastani', 'Padmaavat']
    print("Final answer: ")
    queue = union_colors(graph, nodes)
    # print(len(queue))
    print(queue)
    # results = energy_spread(graph, nodes)
    # print(results)
    # movies_queue = []
    # for key in results.keys():
    #     for neighbor in graph[key]:
    #         if neighbor is 'Drama':
    #             movies_queue.append(key)
    # print(movies_queue)
