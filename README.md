# AI-homework: Sudoku Solver: A* Search and SAT Approach

This project implements two different methods to solve 9×9 Sudoku puzzles:

1. **A\*** search with a simple admissible heuristic (count of empty cells).
2. **SAT-based solving**, using a CNF encoding of Sudoku and a PySAT solver.

The project also includes:
- a random Sudoku generator with a customizable number of clues,
- a full experimental pipeline,
- automatic plotting of performance metrics for both algorithms.

---

## How to Run
To run a simple test with A* search and SAT run the file main.py

To run the experiments where A* and SAT are tested 50 times on different sudokus run tester.py

## Dependencies
```
pip install numpy matplotlib python-sat
