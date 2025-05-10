import time
import random
from dpll_solver import generate_random_cnf, dpll, evaluate_performance, plot_performance
from dp_solver import dp
from resolution_solver import resolution


def test_all_solvers(num_tests=10, min_vars=5, max_vars=20):

    print("Testing all SAT solvers on random instances...")
    print(f"Running {num_tests} tests with {min_vars}-{max_vars} variables")
    print("-" * 50)

    dpll_times = []
    dp_times = []
    resolution_times = []

    agreements = 0

    for i in range(num_tests):
        n_vars = random.randint(min_vars, max_vars)
        n_clauses = random.randint(n_vars, n_vars * 4)

        print(f"Test {i + 1}: {n_vars} variables, {n_clauses} clauses")

        cnf = generate_random_cnf(n_vars, n_clauses)

        start_time = time.time()
        dpll_result, assignment = dpll(cnf)
        dpll_time = (time.time() - start_time) * 1000  # ms
        dpll_times.append(dpll_time)

        if dpll_result and not verify_assignment(cnf, assignment):
            print("  WARNING: DPLL returned invalid assignment!")

        start_time = time.time()
        dp_result = dp(cnf)
        dp_time = (time.time() - start_time) * 1000  # ms
        dp_times.append(dp_time)

        start_time = time.time()
        resolution_result = resolution(cnf)
        resolution_time = (time.time() - start_time) * 1000  # ms
        resolution_times.append(resolution_time)

        agreement = (dpll_result == dp_result == resolution_result)
        agreements += int(agreement)

        print(f"  DPLL: {'SAT' if dpll_result else 'UNSAT'} in {dpll_time:.2f}ms")
        print(f"  DP: {'SAT' if dp_result else 'UNSAT'} in {dp_time:.2f}ms")
        print(f"  Resolution: {'SAT' if resolution_result else 'UNSAT'} in {resolution_time:.2f}ms")
        print(f"  Agreement: {'Yes' if agreement else 'No'}")
        print()

    print("Test Summary:")
    print(f"  Agreement rate: {agreements}/{num_tests} ({agreements / num_tests * 100:.1f}%)")
    print(
        f"  Average times: DPLL={sum(dpll_times) / len(dpll_times):.2f}ms, DP={sum(dp_times) / len(dp_times):.2f}ms, Resolution={sum(resolution_times) / len(resolution_times):.2f}ms")


def verify_assignment(cnf, assignment):

    for clause in cnf:
        if not any(lit in assignment for lit in clause):
            return False
    return True


def create_performance_plots():

    print("Creating performance plots for DPLL algorithm...")

    runtimes, memory_usages = evaluate_performance(max_vars=30, step=5, samples=3)

    plot_performance(runtimes, memory_usages, "plots.png")

    print("Performance plots created and saved as 'plots.png'")


if __name__ == "__main__":
    test_all_solvers(num_tests=5)

    create_performance_plots()