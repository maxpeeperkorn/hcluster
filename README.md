# hcluster

Hierarchical clustering using quartet trees and normalised compression distance.

# Usage

```python
n = 6
max_k = 16

T = hcluster.tree.quartet_tree(n)
D, cost_fn = hcluster.evaluation.compute_distance_matrix(dataset)
operators = [hcluster.operators.leaf_swap,
             hcluster.operators.subtree_swap,
             hcluster.operators.subtree_transfer]

budget = 1000
best_score = -1

while budget > 0:
    T_prime = T
    k_mutation = hcluster.operators.k_mutation_sequence(operators, max_k)

    for operator in k_mutation:
        T_prime = operator(T_prime)

    score = hcluster.evaluation.evaluate(T_prime, cost_fn)

    if score > best_score:
        best_score = score
        T = T_

    if budget == 0 or best_score == 1:
        break
```