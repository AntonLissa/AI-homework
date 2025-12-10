# tester.py
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from sudoku import Sudoku, generate_random_sudoku_grid
from a_star import a_star, heuristic
from sat_solver import solve_sudoku_sat  # supponiamo ritorni anche clausole

# Assicuriamoci che la cartella results esista
os.makedirs("results", exist_ok=True)

NUM_TESTS = 50
CLUES_LIST = [20, 50, 70]

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
        #metrics['solution'] = solution[-1]
        metrics['nodes_generated'] = metrics['nodes_generated']
        metrics['nodes_expanded'] = metrics['nodes_expanded']
        metrics['max_frontier_size'] = metrics['max_frontier_size']
    else:
        metrics['steps'] = None
        metrics['nodes_generated'] = None
        metrics['nodes_expanded'] = None
        metrics['max_frontier_size'] = None
    return metrics

# Funzione helper per SAT
def run_sat(puzzle):
    metrics = {}
    start = time.time()
    solution, clauses = solve_sudoku_sat(puzzle)
    end = time.time()
    metrics['time'] = end - start
    if solution:
        metrics['clauses'] = sum(len(sub_clauses) for sub_clauses in clauses.values())
        metrics['variables'] = max(max(row) for row in clauses) if clauses else None
        #metrics['solution'] = solution
    else:
        metrics['clauses'] = None
        metrics['variables'] = None
        metrics['solution'] = None
    return metrics

# Main loop
results = {}

for num_clues in CLUES_LIST:
    results[num_clues] = {'a_star':[], 'sat':[]}
    print(f"Running tests for num_clues={num_clues}...")
    for _ in range(NUM_TESTS):
        puzzle = generate_random_sudoku_grid(num_clues=num_clues)
        
        # A*
        a_star_metrics = run_a_star(puzzle)
        results[num_clues]['a_star'].append(a_star_metrics)
        
        # SAT
        sat_metrics = run_sat(puzzle)
        results[num_clues]['sat'].append(sat_metrics)
        print(f"Test completed for iteration {_}: A* time: {a_star_metrics['time']:.4f}s; SAT time: {sat_metrics['time']:.4f}s")

# Analisi e plotting
def plot_metric(metric_name, title, filename):
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
    plt.savefig(os.path.join("results", filename))
    plt.close()

def plot_unsolved_counts(results, filename="unsolved.png"):
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
    plt.savefig(os.path.join("results", filename))
    plt.close()

# Metriche da plottare
plot_metric('time', 'Execution time vs number of clues', 'time.png')
plot_metric('steps', 'A* steps vs number of clues', 'steps.png')
plot_metric('nodes_generated', 'A* nodes generated vs number of clues', 'nodes_generated.png')
#plot_metric('nodes_expanded', 'A* nodes expanded vs number of clues', 'nodes_expanded.png')
plot_metric('max_frontier_size', 'A* max frontier size vs number of clues', 'max_frontier_size.png')

# Metriche SAT
plot_metric('clauses', 'SAT clauses vs number of clues', 'sat_clauses.png')
plot_unsolved_counts(results, "unsolved.png")


print("All tests done. Plots saved in 'results/' folder.")


print(results)
