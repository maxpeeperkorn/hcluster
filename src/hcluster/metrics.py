import zlib


def K(x):
    """ Approximates Kolmogorov Complexity. `K(x) ≃ C(x)` """
    obj = zlib.compressobj(level=9, wbits=-15)
    C_x = obj.compress(x if isinstance(x, bytes) else x.encode()) + obj.flush()
    return len(C_x)


def NCD(x, y):
    """ Returns the Normalised Compressed Distance of x and y"""
    K_x, K_y = K(x), K(y)
    return (K(x + y) - min(K_x, K_y)) / max(K_x, K_y)


def tree_benefit_score(cost_fn, quartets):
    return sum([cost_fn(quartet) for quartet in quartets])


def normalised_tree_benefit_score(tree_benefit_score, min, max):
    return 1 - (tree_benefit_score - min) / (max - min)

