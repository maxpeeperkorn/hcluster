import networkx as nx
import random


def chunks(xs, r):
    for i in range(0, len(xs), r):
        yield xs[i:i + r]


def get_nodes(G, node_type=None):
    return [node for node, type_ in G.nodes.data("type")  # type: ignore
            if node_type is None or type_ == node_type]


def select_nodes(G, node_label=None, min_distance=3):
    nodes = get_nodes(G, node_label)

    u, w = random.choices(nodes, k=2)
    path = nx.shortest_path(G, u, w)

    while len(path) < min_distance:
        w = random.choice(nodes)
        path = nx.shortest_path(G, u, w)

    x, y = path[1], path[-2]
    return (u, w), (x, y)


def quartet_tree(n):
    """ Create a quartet tree with `n` leaf nodes and `n - 2` internal nodes. """
    m = 2 * n - 2
    T = nx.full_rary_tree(3, 6)
    T.graph['n'] = n

    for internal, leaf in chunks(list(range(6, m)), r=2):
        u, v = random.choice(list(T.edges()))
        T.remove_edge(u, v)
        edges = [(internal, leaf), (u, internal), (internal, v)]
        T.add_edges_from(edges)

    # add internal and external labels for nodes
    for node in T.nodes():
        if nx.degree(T, node) == 1:
            nx.set_node_attributes(T, {node: {'type': 's'}})
        else:
            nx.set_node_attributes(T, {node: {'type': 'n'}})

    # relabel first leaf nodes then internal nodes, so that
    # the leaf indices map to the distance matrix.
    nodes = get_nodes(T, 's') + get_nodes(T, 'n')
    mapping = {node: i for node, i in zip(nodes, range(m))}
    T = nx.relabel_nodes(T, mapping)
    return T
