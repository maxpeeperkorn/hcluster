import random


def permutation(xs):
    xs = xs[:]
    random.shuffle(xs)
    return xs


def chunks(xs, r):
    for i in range(0, len(xs), r):
        yield xs[i:i + r]
