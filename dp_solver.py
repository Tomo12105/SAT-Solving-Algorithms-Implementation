from typing import List, Set, Dict


def dp(cnf: List[Set[int]]) -> bool:

    cnf = [clause.copy() for clause in cnf]

    if not cnf:
        return True

    if any(not clause for clause in cnf):
        return False

    variables = {abs(lit) for clause in cnf for lit in clause}

    while variables:
        var = choose_variable(cnf, variables)
        variables.remove(var)

        pos_clauses = [clause for clause in cnf if var in clause]
        neg_clauses = [clause for clause in cnf if -var in clause]

        if not pos_clauses or not neg_clauses:
            cnf = [clause for clause in cnf if var not in clause and -var not in clause]
            continue

        resolvents = []
        for p_clause in pos_clauses:
            for n_clause in neg_clauses:
                resolvent = p_clause.union(n_clause) - {var, -var}
                if not resolvent:
                    return False
                resolvents.append(resolvent)

        cnf = [clause for clause in cnf if var not in clause and -var not in clause]

        cnf.extend(resolvents)

        if any(not clause for clause in cnf):
            return False

    return True


def choose_variable(cnf: List[Set[int]], variables: Set[int]) -> int:

    counts = {var: 0 for var in variables}
    for var in variables:
        for clause in cnf:
            if var in clause or -var in clause:
                counts[var] += 1

    return min(counts, key=counts.get)