from sudoku import Sudoku, generate_random_sudoku_grid, pretty_print, check_solution
from a_star import a_star, heuristic
from sat_solver import solve_sudoku_sat, print_clauses

if __name__ == "__main__":
    puzzle = generate_random_sudoku_grid(num_clues=20)
    print("Generated Sudoku Puzzle:")
    pretty_print(puzzle)

    solution, clauses = solve_sudoku_sat(puzzle)
    if solution:
        if check_solution(solution):
            print("\nSudoku solved with SAT:")
            pretty_print(solution)
        else:
            print("SAT solution is incorrect.")
    else:
        print("No SAT solution.")
    
    #print_clauses(clauses)


    env = Sudoku(puzzle)
    solution, metrics = a_star(env, heuristic, verbose=False)

    if solution:   
        if check_solution(solution[-1]):     
            print(f"\nSudoku solved with A* in {len(solution)-1} steps.")
            pretty_print(solution[-1])
        else:
            print("A* solution is incorrect.")
    else:
        print("No A* solution found")
    
