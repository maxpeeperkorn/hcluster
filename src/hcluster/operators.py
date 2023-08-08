import functools
import math
import networkx as nx
import random

from hcluster.tree import select_nodes, get_nodes


def permutation(xs):
    xs = xs[:]
    random.shuffle(xs)
    return xs


def __has_two_leafs(G, u):
    leaf_nodes = get_nodes(G, "s")
    leaf_count = sum([1 for node in G.neighbors(u) if node in leaf_nodes])
    return leaf_count > 1


def leaf_swap(G):
    (u, w), (x, y) = select_nodes(G, 's')
    G.remove_edges_from([(u, x), (w, y)])
    G.add_edges_from([(u, y), (w, x)])
    return G


def subtree_swap(G):
    (u, w), (x, y) = select_nodes(G, 'n')
    G.remove_edges_from([(u, x), (w, y)])
    G.add_edges_from([(u, y), (w, x)])
    return G


def subtree_transfer(G):
    internal_nodes = get_nodes(G, "n")

    # make sure a suitable node is found that maintains graph arity
    u = random.choice(internal_nodes)
    while __has_two_leafs(G, u):
        u = random.choice(internal_nodes)

    # -- detach node and join the two remaing subtrees
    neighbors = [node for node in G.neighbors(u)
                 if node in internal_nodes]
    a, b = permutation(neighbors)[:2]
    G.remove_edges_from([(u, a), (u, b)])
    G.add_edge(a, b)

    # -- reattach detached subtree
    subtree_edges = list(nx.bfs_edges(G, a))  # pick edge in remaing subtree
    w, v = random.choice(subtree_edges)
    G.remove_edge(w, v)
    G.add_edges_from([(u, w), (u, v)])
    return G


@functools.cache
def k_mutation_probabilities(max_k):
    return [1 / ((k + 2) * math.log(k + 2, 2) ** 2) 
            for k in range(1, max_k + 1)]


def k_mutation_sequence(operators, max_k=16):
    p_k = k_mutation_probabilities(max_k)
    k = random.choices(range(1, max_k + 1), weights=p_k, k=1)[0]
    return [random.choice(operators) for _ in range(k)]