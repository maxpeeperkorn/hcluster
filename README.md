# hcluster

Hierarchical clustering using quartet trees and normalised compression distance.

# Usage

```python
import hcluster

n = 6
max_k = 16
budget = 1000
best_score = -1

T = hcluster.quartet_tree(n)
D, cost_fn = hcluster.compute_distance_matrix(dataset)
operators = hcluster.default_operators


while budget > 0:
    T_prime = T
    
    k_mutation = hcluster.k_mutation_sequence(operators, max_k)
    for operator in k_mutation:
        T_prime = operator(T_prime)

    score = hcluster.evaluate(T_prime, cost_fn)

    if score > best_score:
        best_score = score
        T = T_prime
    
    budget = budget -1
    
    if best_score == 1:
        break

print(best_score)
```

# References

Cilibrasi, R. L., & Vitányi, P. M. (2005). Clustering by compression. IEEE Transactions on Information theory, 51(4), 1523-1545.

Cilibrasi, R. L., & Vitányi, P. M. (2011). A fast quartet tree heuristic for hierarchical clustering. Pattern recognition, 44(3), 662-677.
