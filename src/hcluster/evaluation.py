import itertools
import networkx as nx

from hcluster.tree import get_nodes
from hcluster.metrics import NCD, tree_benefit_score, normalised_tree_benefit_score


def is_consistent(G, quartet):
    u, v, w, x = quartet
    uv_path = set(nx.shortest_path(G, u, v))
    wx_path = set(nx.shortest_path(G, w, x))
    return len(uv_path.intersection(wx_path)) == 0


def all_possible_pairs(quartet):
    u, v, w, x = quartet
    return [(u, v, w, x), (u, w, v, x), (u, x, v, w)]


def compute_cost_bounds(quartets, cost_fn):
    min_cost, max_cost = 0, 0
    for quartet in quartets:
        scores = [cost_fn(quartet) for quartet in all_possible_pairs(quartet)]
        min_cost += min(scores)
        max_cost += max(scores)
    return min_cost, max_cost


def compute_cost(cost_fn, quartets):
    min_cost, max_cost = compute_cost_bounds(cost_fn, quartets)
    S = tree_benefit_score(cost_fn, quartets)
    return normalised_tree_benefit_score(S, min_cost, max_cost)


def compute_distance_matrix(dataset, key="obj"):
    n = len(dataset)
    D = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(NCD(dataset[i][key], dataset[j][key]))
        D.append(row)
    return D


def create_cost_fn(D):
    def __pair_distance(quartet):
        u, v, w, x = quartet
        return D[u][v] + D[w][x]
    return __pair_distance


def evaluate(T, cost_fn):
    nodes = get_nodes(T, 's')
    quartets = [list(quartet) for quartet in itertools.combinations(nodes, r=4)
                if is_consistent(T, quartet)]
    return compute_cost(cost_fn, quartets)
