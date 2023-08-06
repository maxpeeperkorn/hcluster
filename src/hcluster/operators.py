import networkx as nx
import random

from hcluster.tree import select_nodes, get_nodes
from hcluster.utils import permutation


def __count_leafs(G, u):
    l_nodes = get_nodes(G, "s")
    return sum([1 for node in G.neighbors(u) if node in l_nodes])


def __has_two_leafs(G, u):
    return __count_leafs(G, u) > 1


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
    i_nodes = get_nodes(G, "n")

    # make sure a suitable node is found that maintains graph arity
    u = random.choice(i_nodes)
    while __has_two_leafs(G, u):
        u = random.choice(i_nodes)

    # -- detach node and join the two remaing subtrees
    ngbrs = [node for node in G.neighbors(u)
             if node in i_nodes]
    a, b = permutation(ngbrs)[:2]
    G.remove_edges_from([(u, a), (u, b)])
    G.add_edge(a, b)

    # -- reattach detached subtree
    subtree_edges = list(nx.bfs_edges(G, a))  # pick edge in remaing subtree
    w, v = random.choice(subtree_edges)
    G.remove_edge(w, v)
    G.add_edges_from([(u, w), (u, v)])
    return G


operators = [
    leaf_swap,
    subtree_swap,
    subtree_transfer
]
