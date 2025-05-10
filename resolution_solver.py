from typing import List, Set, FrozenSet

def resolution(cnf: List[Set[int]]) -> bool:

    clauses = set(frozenset(clause) for clause in cnf)

    if not clauses:
        return True

    if frozenset() in clauses:
        return False

    new_resolvents = set()

    iterations = 0
    max_iterations = 1000

    while iterations < max_iterations:
        iterations += 1

        additions = set()

        clauses_list = list(clauses)
        for i, ci in enumerate(clauses_list):
            for j in range(i + 1, len(clauses_list)):
                cj = clauses_list[j]

                resolvents = resolve(ci, cj)

                if frozenset() in resolvents:
                    return False

                additions.update(r for r in resolvents if r not in clauses)

        if not additions:
            return True

        clauses.update(additions)

        if not (additions - new_resolvents):
            return True

        new_resolvents.update(additions)

    return True


def resolve(c1: FrozenSet[int], c2: FrozenSet[int]) -> Set[FrozenSet[int]]:
    result = set()

    for lit in c1:
        if -lit in c2:
            resolvent = (c1 | c2) - {lit, -lit}
            result.add(frozenset(resolvent))

    return result