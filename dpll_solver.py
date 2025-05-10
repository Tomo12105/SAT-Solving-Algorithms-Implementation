import random
from typing import List, Set, Tuple, Dict, Optional
import time
import psutil
import os
import matplotlib.pyplot as plt


def generate_random_cnf(num_vars: int, num_clauses: int) -> List[Set[int]]:
    cnf = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 3:
            lit = random.randint(1, num_vars)
            lit *= -1 if random.random() < 0.5 else 1
            clause.add(lit)
        cnf.append(clause)
    return cnf


def get_memory_usage_mb() -> float:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def dpll(cnf: List[Set[int]], assignment: Set[int] = None) -> Tuple[bool, Set[int]]:
    if assignment is None:
        assignment = set()

    cnf, assignment = unit_propagation(cnf, assignment)

    cnf, assignment = pure_literal_elimination(cnf, assignment)

    if not cnf:
        return True, assignment

    if any(not clause for clause in cnf):
        return False, set()

    lit = choose_literal(cnf)

    result, new_assignment = dpll(cnf, assignment | {lit})
    if result:
        return True, new_assignment

    return dpll(cnf, assignment | {-lit})


def unit_propagation(cnf: List[Set[int]], assignment: Set[int]) -> Tuple[List[Set[int]], Set[int]]:
    cnf = [clause.copy() for clause in cnf]
    assignment = assignment.copy()

    cnf = simplify(cnf, assignment)

    changed = True
    while changed:
        changed = False
        unit_clauses = [list(clause)[0] for clause in cnf if len(clause) == 1]
        if unit_clauses:
            changed = True
            for lit in unit_clauses:
                assignment.add(lit)
            cnf = simplify(cnf, set(unit_clauses))

            if any(not clause for clause in cnf):
                return [set()], assignment

    return cnf, assignment


def pure_literal_elimination(cnf: List[Set[int]], assignment: Set[int]) -> Tuple[List[Set[int]], Set[int]]:

    cnf = [clause.copy() for clause in cnf]
    assignment = assignment.copy()

    if not cnf:
        return cnf, assignment

    all_literals = set()
    for clause in cnf:
        all_literals.update(clause)

    pure_literals = set()
    for lit in all_literals:
        if -lit not in all_literals:
            pure_literals.add(lit)

    if pure_literals:
        assignment.update(pure_literals)
        new_cnf = []
        for clause in cnf:
            if not any(lit in pure_literals for lit in clause):
                new_cnf.append(clause)
        cnf = new_cnf

    return cnf, assignment


def simplify(cnf: List[Set[int]], assignment: Set[int]) -> List[Set[int]]:
    simplified = []
    for clause in cnf:
        if any(lit in assignment for lit in clause):
            continue

        new_clause = {lit for lit in clause if -lit not in assignment}
        simplified.append(new_clause)

    return simplified


def choose_literal(cnf: List[Set[int]]) -> int:
    scores = {}
    for clause in cnf:
        weight = 2 ** -len(clause)
        for lit in clause:
            scores[lit] = scores.get(lit, 0) + weight

    if not scores:
        return 0
    return max(scores, key=scores.get)


def evaluate_performance(max_vars: int = 30, step: int = 5, samples: int = 3) -> Tuple[Dict, Dict]:

    runtimes = {}
    memory_usages = {}

    for n_vars in range(10, max_vars + 1, step):
        n_clauses = int(n_vars * 4.3)

        total_time = 0
        total_memory = 0

        for _ in range(samples):
            cnf = generate_random_cnf(n_vars, n_clauses)

            start_time = time.time()
            start_memory = get_memory_usage_mb()

            dpll(cnf)

            end_time = time.time()
            end_memory = get_memory_usage_mb()

            total_time += (end_time - start_time) * 1000
            total_memory += end_memory - start_memory

        runtimes[n_vars] = total_time / samples
        memory_usages[n_vars] = total_memory / samples

    return runtimes, memory_usages


def plot_performance(runtimes: Dict[int, float], memory_usages: Dict[int, float],
                     save_path: str = "plots.png") -> None:

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    var_counts = sorted(runtimes.keys())

    ax1.plot(var_counts, [runtimes[v] for v in var_counts], 'o-', color='orange')
    ax1.set_title("DPLL Runtime vs Problem Size")
    ax1.set_xlabel("Number of Variables")
    ax1.set_ylabel("Runtime (ms)")
    ax1.grid(True)
    ax1.set_xlim(min(var_counts) - 1, max(var_counts) + 1)
    ax1.set_ylim(0, max([runtimes[v] for v in var_counts]) * 1.1)
    ax1.legend(["DPLL Runtime (ms)"])

    ax2.plot(var_counts, [memory_usages[v] for v in var_counts], 'o-', color='orange')
    ax2.set_title("DPLL Memory Usage vs Problem Size")
    ax2.set_xlabel("Number of Variables")
    ax2.set_ylabel("Memory (MB)")
    ax2.grid(True)
    ax2.set_xlim(min(var_counts) - 1, max(var_counts) + 1)
    ax2.set_ylim(0, max([memory_usages[v] for v in var_counts]) * 1.1)
    ax2.legend(["Memory Usage (MB)"])

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


if __name__ == "__main__":

    runtimes, memory_usages = evaluate_performance(max_vars=30, step=5, samples=3)
    plot_performance(runtimes, memory_usages)

    cnf = generate_random_cnf(5, 10)
    print("Random CNF:", cnf)
    result, assignment = dpll(cnf)
    print("Satisfiable:", result)
    print("Assignment:", assignment)