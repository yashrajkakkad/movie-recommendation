from Movies import load_movies_data, Movie


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
    return graph


if __name__ == "__main__":
    graph = create_graph()
    print(graph)
