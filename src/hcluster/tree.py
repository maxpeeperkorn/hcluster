import networkx as nx
import random

from hcluster.utils import chunks


def get_nodes(G, node_type=None):
    return [node for node, _type in G.nodes.data("type")  # type: ignore
            if node_type is None or _type == node_type]


def select_nodes(G, node_label=None, min_distance=3):
    nodes = get_nodes(G, node_label)

    u, w = random.choices(nodes, k=2)
    path = nx.shortest_path(G, u, w)

    while len(path) < min_distance:
        w = random.choice(nodes)
        path = nx.shortest_path(G, u, w)

    x, y = path[1], path[-2]
    return (u, w), (x, y)


def create_quartet_tree(n):
    m = 2 * n - 2
    G = nx.full_rary_tree(3, 6)

    for internal, leaf in chunks(list(range(6, m)), r=2):
        u, v = random.choice(list(G.edges()))
        G.remove_edge(u, v)
        edges = [(internal, leaf), (u, internal), (internal, v)]
        G.add_edges_from(edges)

    # add internal and external labels for nodes
    for node in G.nodes():
        if nx.degree(G, node) == 1:
            nx.set_node_attributes(G, {node: {'type': 's'}})
        else:
            nx.set_node_attributes(G, {node: {'type': 'n'}})

    # relabel first leaf nodes then internal nodes, so that
    # the leaf indices map to the distance matrix.
    all_nodes = get_nodes(G, 's') + get_nodes(G, 'n')
    mapping = {node: i for node, i in zip(all_nodes, range(m))}
    G = nx.relabel_nodes(G, mapping)
    return G
