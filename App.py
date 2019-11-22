from utils.Graph import gen_recommendations


# Get nodes from form
def gen_results(nodes):
    union_colors_results, energy_spread_results = gen_recommendations(nodes)
    return union_colors_results, energy_spread_results
