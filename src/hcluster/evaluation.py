import itertools
import networkx as nx
import functools
import zlib


def C(x):
    """ Approximates Kolmogorov Complexity. `K(x) ≃ C(x)` """
    obj = zlib.compressobj(level=9, wbits=-15)
    C_x = obj.compress(x if isinstance(x, bytes) else x.encode()) + obj.flush()
    return len(C_x)


def NCD(x, y):
    """ Returns the Normalised Compressed Distance of x and y"""
    C_x, C_y = C(x), C(y)
    return (C(x + y) - min(C_x, C_y)) / max(C_x, C_y)


def tree_benefit_score(cost_fn, quartets):
    return sum([cost_fn(quartet) for quartet in quartets])


def normalised_tree_benefit_score(tree_benefit_score, min, max):
    return 1 - (tree_benefit_score - min) / (max - min)


@functools.cache
def __all_quartets(n):
    """ Returns all quartet combinations for `n` leaf nodes. """
    return itertools.combinations(range(n), r=4)


@functools.cache
def __all_pairs(quartet):
    """ Returns all possible pairings for a quartet. """
    u, v, w, x = quartet
    return [(u, v, w, x), (u, w, v, x), (u, x, v, w)]


def is_consistent(G, quartet):
    u, v, w, x = quartet
    uv_path = set(nx.shortest_path(G, u, v))
    wx_path = set(nx.shortest_path(G, w, x))
    return len(uv_path.intersection(wx_path)) == 0


def compute_cost_bounds(cost_function, quartets):
    min_cost, max_cost = 0, 0
    for quartet in quartets:
        scores = [cost_function(quartet) for quartet in __all_pairs(quartet)]
        min_cost += min(scores)
        max_cost += max(scores)
    return min_cost, max_cost


def compute_cost(cost_function, quartets):
    min_cost, max_cost = compute_cost_bounds(cost_function, quartets)
    S = tree_benefit_score(cost_function, quartets)
    return normalised_tree_benefit_score(S, min_cost, max_cost)


def compute_distance_matrix(dataset, key="obj"):
    n = len(dataset)
    D = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(NCD(dataset[i][key], dataset[j][key]))
        D.append(row)

    def cost_function(quartet):
        u, v, w, x = quartet
        return D[u][v] + D[w][x]

    return D, cost_function


def evaluate(T, cost_function):
    quartets = [list(quartet) for quartet in __all_quartets(T.graph['n'])
                if is_consistent(T, quartet)]
    return compute_cost(cost_function, quartets)
