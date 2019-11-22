from .Movies import load_movies_data, load_movie_titles, Movie
import pickle
from operator import itemgetter
from collections import OrderedDict


def create_graph():
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
    parent[node] = find_parent(parent[node], parent)
    return parent[node]


def union_sets(node1, node2, parent, size):
    node1 = find_parent(node1, parent)
    node2 = find_parent(node2, parent)
    parent_node = None
    if node1 != node2:
        if size[node1] <= size[node2]:
            temp = node1
            node1 = node2
            node2 = temp
            parent_node = node2
        else:
            parent_node = node1
        parent[node2] = node1
        size[node2] += size[node1]
    return parent_node


def union_colors(graph, nodes):
    # Initialize required variables
    colors = {}
    visited = {}
    queue = []
    parent = {}
    size = {}
    color_parent = {}

    last_united_color = 1  # The last united color being the first color by default
    n_colors = len(nodes)

    color_ord = []  # List of lists containing nodes of different colors
    for i in range(n_colors + 1):
        color_ord.append([])

    # Mark each initial node with a different color
    for i, node in enumerate(nodes):
        colors[node] = i + 1
        color_ord[colors[node]].append(node)
        parent[node] = None
        # Initialize the set of that particular color
        make_set(i + 1, color_parent, size)

    # Enqueue neighbours of initial nodes in the queue
    for node in nodes:
        for neighbour in graph[node]:
            if neighbour not in nodes:
                parent[neighbour] = node
                queue.append((neighbour, node))

    if n_colors == 1:
        i = 3
        new_queue = []
        while i != 0:
            while len(queue) != 0:
                node, parent_node = queue.pop(0)
                visited[node] = True
                for neighbour in graph[node]:
                    try:
                        _ = visited[neighbour]
                    except KeyError:
                        new_queue.append((neighbour, node))
                        parent[neighbour] = node
            i -= 1
            for node, parent_node in new_queue:
                queue.append((node, parent_node))
        for node, parent_node in queue:
            if node == nodes[0]:
                pass
            else:
                color_ord[last_united_color].append(node)
        results = list(dict.fromkeys(color_ord[last_united_color][1:]))
        return results

    while n_colors != 1:
        node, parent_node = queue.pop(0)  # Dequeue a node and visit it
        visited[node] = True
        color = None
        try:
            color = find_parent(colors[node], color_parent)
        except KeyError:
            # If it is yet to be colored
            colors[node] = find_parent(colors[parent_node], color_parent)
            color_ord[colors[node]].append(node)
            size[colors[node]] += 1
        # If it is already colored (and has a parent), merge two colors to one
        if color:
            if color != find_parent(colors[parent_node], color_parent):
                # print(node, color, parent_node, colors[parent_node])
                color_parent_node = union_sets(
                    color, colors[parent_node], color_parent, size)
                if color_parent_node:
                    last_united_color = color_parent_node
                    if color_parent_node == colors[node]:
                        other_node = parent_node
                    else:
                        other_node = node
                    color_ord[color_parent_node].append(other_node)
                n_colors -= 1
        # Add the neighbours of the visited queue which are yet to be visited to the queue
        for neighbour in graph[node]:
            try:
                _ = visited[neighbour]
            except KeyError:
                # if neighbour not in queue:
                queue.append((neighbour, node))
                parent[neighbour] = node
    for node in queue:
        try:
            _ = visited[node]
        except KeyError:
            try:
                color = find_parent(parent[node], color_parent)
                color_ord[color].append(node)
            except KeyError:
                pass
            # color_ord[find_parent(parent[node], color_parent)].append(node)
    return color_ord[last_united_color]


def energy_spread(graph, nodes):
    # Init variables
    energy_values = {}  # Energies of initial nodes
    neighbor_energy_values = {}  # Energies of neighbors of initial nodes
    visited = {}
    queue = []
    parent = {}
    movie_titles = load_movie_titles()
    for node in nodes:
        # Assign arbitrary energy values
        energy_values[node] = 5000 * len(nodes)
        queue.append(node)  # Enqueue initial nodes
        parent[node] = node
    for i in range(len(nodes)):
        # print(queue)
        node = queue.pop(0)
        visited[node] = True
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
                        (energy_values[parent[node]] / len(graph[node]))
                except KeyError:
                    neighbor_energy_values[neighbor] = (
                        energy_values[parent[node]] / len(graph[node]))
    final_energy_values = {}  # Energy values of neighbor movies
    for node in queue:
        for neighbor in graph[node]:
            energy_value = None
            if neighbor in movie_titles:
                try:  # Add new energy value if already exists
                    energy_value = final_energy_values[neighbor]
                    final_energy_values[neighbor] = energy_value + \
                        (neighbor_energy_values[node] / len(graph[node]))
                except KeyError:
                    final_energy_values[neighbor] = neighbor_energy_values[node] / \
                        len(graph[node])
    sorted_values = OrderedDict(sorted(final_energy_values.items(),  # Sort using OrderedDict to maintain order
                                       key=itemgetter(1)))
    for node in nodes:
        deleted_pair = sorted_values.pop(node, None)
    return sorted_values


def gen_recommendations(nodes):
    graph = load_graph()
    movies = load_movie_titles()

    count = 0
    union_colors_results = []
    energy_spread_results = []

    color_ord = union_colors(graph, nodes)
    print("Results using union colors: ")
    for node in color_ord:
        if node in movies:
            print(node)
            union_colors_results.append(node)
            count += 1
            if count >= 5:
                break

    results = energy_spread(graph, nodes)
    print("\n\nResults using energy spreading: ")
    count = 0
    for node, energy in reversed(results.items()):
        print(node)
        energy_spread_results.append(node)
        count += 1
        if count >= 5:
            break

    return union_colors_results, energy_spread_results
