# AI-homework: Sudoku Solver: A* Search and SAT Approach

This project implements two different methods to solve 9×9 Sudoku puzzles:

1. **A\*** search with a simple admissible heuristic (count of empty cells).
2. **SAT-based solving**, using a CNF encoding of Sudoku and a PySAT solver.

The project also includes:
- a random Sudoku generator with a customizable number of clues,
- a full experimental pipeline,
- automatic plotting of performance metrics for both algorithms.

Check the homework_AI.pdf for the methods description and comments on the results obtained

---

## How to Run
To run a simple test with A* search and SAT run the file main.py, the result will look like this:
```
Generated Sudoku Puzzle:
. 1 . | . . . | . . .
. . . | . . 8 | 5 6 .
9 . . | 3 . . | . . 1
- - - + - - - + - - -
. . . | 6 . . | . . .
. . . | . . . | . . .
. 9 5 | . . . | . . .
- - - + - - - + - - -
. . 9 | 8 . 6 | . . .
. 7 . | 4 . 3 | . . .
. 6 8 | 7 . . | 4 . .

Sudoku solved with SAT:
8 1 6 | 5 7 9 | 3 2 4
2 3 7 | 1 4 8 | 5 6 9
9 5 4 | 3 6 2 | 8 7 1
- - - + - - - + - - -
1 8 2 | 6 3 4 | 9 5 7
7 4 3 | 9 5 1 | 2 8 6
6 9 5 | 2 8 7 | 1 4 3
- - - + - - - + - - -
4 2 9 | 8 1 6 | 7 3 5
5 7 1 | 4 2 3 | 6 9 8
3 6 8 | 7 9 5 | 4 1 2

Sudoku solved with A* in 61 steps.
8 1 7 | 9 6 5 | 3 4 2
4 3 2 | 1 7 8 | 5 6 9
9 5 6 | 3 4 2 | 8 7 1
- - - + - - - + - - -
7 8 4 | 6 9 1 | 2 5 3
6 2 3 | 5 8 7 | 9 1 4
1 9 5 | 2 3 4 | 7 8 6
- - - + - - - + - - -
5 4 9 | 8 2 6 | 1 3 7
2 7 1 | 4 5 3 | 6 9 8
3 6 8 | 7 1 9 | 4 2 5
```
To run the experiments where A* and SAT are tested 50 times on different sudokus run tester.py

## Dependencies
```
pip install numpy matplotlib python-sat
