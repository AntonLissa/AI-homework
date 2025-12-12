# tester.py
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from sudoku import Sudoku, generate_random_sudoku_grid, get_sudokus_from_web
from a_star import a_star, heuristic
from sat_solver import solve_sudoku_sat  # supponiamo ritorni anche clausole

# Assicuriamoci che la cartella results esista
os.makedirs("results", exist_ok=True)

NUM_TESTS = 50
CLUES_LIST = [20, 45, 70]

# Funzione helper per misurare tempo e metriche A*
def run_a_star(puzzle):
    env = Sudoku(puzzle)
    metrics = {}
    start = time.time()
    solution, metrics = a_star(env, heuristic, verbose=False)
    end = time.time()
    metrics['time'] = end - start
    if solution:
        metrics['steps'] = len(solution)-1
        metrics['solution'] = solution[-1]
        metrics['nodes_generated'] = metrics['nodes_generated']
        metrics['nodes_expanded'] = metrics['nodes_expanded']
        metrics['max_frontier_size'] = metrics['max_frontier_size']
    else:
        metrics['steps'] = None
        metrics['nodes_generated'] = None
        metrics['nodes_expanded'] = None
        metrics['max_frontier_size'] = None
    return metrics

# SAT runner
def run_sat(puzzle):
    metrics = {}
    start = time.time()
    solution, clauses = solve_sudoku_sat(puzzle)
    end = time.time()
    metrics['time'] = end - start
    if solution:
        # clauses vars
        num_clauses = sum(len(sub_clauses) for sub_clauses in clauses.values())
        metrics['clauses'] = num_clauses
        
        # variables
        all_vars = set()
        for sub_clauses in clauses.values():
            for clause in sub_clauses:
                all_vars.update(abs(lit) for lit in clause)
        num_vars = len(all_vars)
        metrics['variables'] = num_vars

        # clause to var ratio
        metrics['clause_to_var_ratio'] = num_clauses / num_vars if num_vars > 0 else None

        metrics['solution'] = solution
    else:
        metrics['clauses'] = None
        metrics['variables'] = None
        metrics['clause_to_var_ratio'] = None
        metrics['solution'] = None
    return metrics

# Main loop

def my_test(num_test=50):
    results = {}
    for num_clues in CLUES_LIST:
        results[num_clues] = {'a_star':[], 'sat':[]}
        print(f"Running tests for num_clues={num_clues}...")
        for _ in range(num_test):
            puzzle = generate_random_sudoku_grid(num_clues=num_clues)
            
            # A*
            a_star_metrics = run_a_star(puzzle)
            results[num_clues]['a_star'].append(a_star_metrics)
            
            # SAT
            sat_metrics = run_sat(puzzle)
            results[num_clues]['sat'].append(sat_metrics)
            print(f"Test completed for iteration {_}: A* time: {a_star_metrics['time']:.4f}s; SAT time: {sat_metrics['time']:.4f}s")
    return results



def test_on_benchmark_web(url, num = None):
    sudokus = get_sudokus_from_web(url)
    results = {'a_star':[], 'sat':[]}
    num_clues_list = []
    if num is not None:
        sudokus = sudokus[:num]

    for idx, puzzle in enumerate(sudokus):
        print(f"Testing puzzle {idx+1}/{len(sudokus)} from benchmark...")
        # get clues number
        num_clues = sum(1 for row in puzzle for cell in row if cell != 0)
        num_clues_list.append(num_clues)

        # A*
        a_star_metrics = run_a_star(puzzle)
        a_star_metrics['num_clues'] = num_clues
        results['a_star'].append(a_star_metrics)

        # SAT
        sat_metrics = run_sat(puzzle)
        sat_metrics['num_clues'] = num_clues
        results['sat'].append(sat_metrics)

    return results, num_clues_list


def plot_metric(metric_name, title, filename, results, folder):
    plt.figure(figsize=(8,6))
    means_a = []
    stds_a = []
    means_s = []
    stds_s = []
    
    for num_clues in CLUES_LIST:
        a_values = [r[metric_name] for r in results[num_clues]['a_star'] if r.get(metric_name) is not None]
        s_values = [r[metric_name] for r in results[num_clues]['sat'] if r.get(metric_name) is not None]
        means_a.append(np.mean(a_values))
        stds_a.append(np.std(a_values))
        means_s.append(np.mean(s_values))
        stds_s.append(np.std(s_values))

    if any(~np.isnan(means_a)):
        plt.errorbar(CLUES_LIST, means_a, yerr=stds_a, label='A*', marker='o', capsize=5, color='blue')
    if any(~np.isnan(means_s)):
        plt.errorbar(CLUES_LIST, means_s, yerr=stds_s, label='SAT', marker='s', capsize=5, color='orange')

    plt.xlabel("Number of clues")
    plt.ylabel(metric_name)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(folder, filename))
    plt.close()

def plot_unsolved_counts(results, filename="unsolved.png", folder="results"):
    unsolved_astar = []
    unsolved_sat = []

    
    for num_clues in CLUES_LIST:
        # A* non risolti
        count_astar = sum(1 for r in results[num_clues]['a_star'] if r.get('solution') is None)
        unsolved_astar.append(count_astar)

        # SAT non risolti
        count_sat = sum(1 for r in results[num_clues]['sat'] if r.get('solution') is None)
        unsolved_sat.append(count_sat)

    x = np.arange(len(CLUES_LIST))
    width = 0.35

    plt.figure(figsize=(8, 6))
    plt.bar(x - width/2, unsolved_astar, width, label='A*')
    plt.bar(x + width/2, unsolved_sat, width, label='SAT')

    plt.xticks(x, CLUES_LIST)
    plt.xlabel("Number of clues")
    plt.ylabel("Unsolved puzzles (out of {})".format(NUM_TESTS))
    plt.title("Unsolved puzzles vs number of clues")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, filename))
    plt.close()

import csv
import numpy as np

def save_summary_table(results, filename="summary_table.csv", folder="results"):
    """
    Save a summary table of metrics to a CSV file.
      - mean
      - std
      - solved puzzles
      - unsolved puzzles
    """
    metrics_astar = ['time', 'steps', 'nodes_generated', 'max_frontier_size']
    metrics_sat = ['time', 'clauses', 'variables', 'clause_to_var_ratio']

    with open(os.path.join(folder, filename), mode='w', newline='') as f:
        writer = csv.writer(f)
        # Header
        header = ['Algorithm', 'Num_clues', 'Metric', 'Mean', 'Std', 'Solved', 'Unsolved']
        writer.writerow(header)

        for num_clues, algos in results.items():
            # A* metrics
            for metric in metrics_astar:
                values = [r[metric] for r in algos['a_star'] if r.get(metric) is not None]
                solved = sum(1 for r in algos['a_star'] if r.get('solution') is not None)
                unsolved = sum(1 for r in algos['a_star'] if r.get('solution') is None)
                mean_val = np.mean(values) if values else None
                std_val = np.std(values) if values else None
                writer.writerow(['A*', num_clues, metric, mean_val, std_val, solved, unsolved])

            # SAT metrics
            for metric in metrics_sat:
                values = [r[metric] for r in algos['sat'] if r.get(metric) is not None]
                solved = sum(1 for r in algos['sat'] if r.get('solution') is not None)
                unsolved = sum(1 for r in algos['sat'] if r.get('solution') is None)
                mean_val = np.mean(values) if values else None
                std_val = np.std(values) if values else None
                writer.writerow(['SAT', num_clues, metric, mean_val, std_val, solved, unsolved])

    print(f"Summary table saved to {filename}")


results = my_test(num_test=50)
folder="my_results"

#results = test_on_benchmark_web("http://magictour.free.fr/top2365", 100)
#folder="results_benchmark"

os.makedirs(folder, exist_ok=True)
# Metriche da plottare
plot_metric('time', 'Execution time vs number of clues', 'time.png', results, folder)
plot_metric('steps', 'A* steps vs number of clues', 'steps.png', results, folder)
plot_metric('nodes_generated', 'A* nodes generated vs number of clues', 'nodes_generated.png', results, folder)
plot_metric('max_frontier_size', 'A* max frontier size vs number of clues', 'max_frontier_size.png', results, folder)

# Metriche SAT
plot_metric('clauses', 'SAT clauses vs number of clues', 'sat_clauses.png', results, folder)
plot_metric('variables', 'SAT number of variables vs number of clues', 'sat_variables.png', results, folder)
plot_metric('clause_to_var_ratio', 'SAT clause-to-variable ratio vs number of clues', 'sat_clause_to_var_ratio.png', results, folder)

plot_unsolved_counts(results, "unsolved.png", folder)

save_summary_table(results, "summary_table.csv", folder)

print("All tests done. Plots saved in 'results/' folder.")


print(results)
