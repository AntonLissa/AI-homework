
from pysat.solvers import Glucose3



def print_clauses(all_clauses):
        for rule, clauses in all_clauses.items():
            print(f"\n{rule} clauses:")
            for clause in clauses[:10]:
                print(clause)


def solve_sudoku_sat(grid):
    clauses = {'rule 1': [], 'rule 2': [], 'rule 3': [], 'rule 4': [], 'rule 5': [], 'rule 6': []}
    # solves a Sudoku puzzle using SAT solver
    size = len(grid)  
    solver = Glucose3()

    # Helper: map (i,j,n) -> variable number
    def var(i, j, n):
        return i*size*size + j*size + n

    # rule 1: each cell has at least one number 
    for i in range(size):
        for j in range(size):
            clause = [var(i, j, n+1) for n in range(size)] # makes clause [X001, X002, ..., X009]
            solver.add_clause(clause)
            clauses['rule 1'].append(clause)

    # rule 2: each cell has at most one number
    for i in range(size):
        for j in range(size):
            for n1 in range(size):
                for n2 in range(n1+1, size):
                    solver.add_clause([-var(i,j,n1+1), -var(i,j,n2+1)]) # makes clauses: [¬X001, ¬X002], [¬X001, ¬X003], ...
                    clauses['rule 2'].append([-var(i,j,n1+1), -var(i,j,n2+1)])

    # rule 3: Row unique
    for i in range(size):
        for n in range(size):
            for j1 in range(size):
                for j2 in range(j1+1, size):
                    solver.add_clause([-var(i,j1,n+1), -var(i,j2,n+1)]) # makes clauses: [¬X001, -X011], [¬X001, -X021], ...
                    clauses['rule 3'].append([-var(i,j1,n+1), -var(i,j2,n+1)])
    # rule 4: Column unique
    for j in range(size):
        for n in range(size):
            for i1 in range(size):
                for i2 in range(i1+1, size):
                    solver.add_clause([-var(i1,j,n+1), -var(i2,j,n+1)]) # makes clauses: [¬X001, -X101], [¬X001, -X201], ...
                    clauses['rule 4'].append([-var(i1,j,n+1), -var(i2,j,n+1)])

    # rule 5: Pre-filled cells must retain their numbers
    for i in range(size):
        for j in range(size):
            if grid[i][j] != 0:
                solver.add_clause([var(i,j,grid[i][j])]) # makes clause: [X005] for a cell pre-filled with 5
                clauses['rule 5'].append([var(i,j,grid[i][j])])


    block_size = int(size**0.5)  # es. 2 per 4x4, 3 per 9x9

    # rule 6: Block unique
    for bi in range(0, size, block_size):
        for bj in range(0, size, block_size):
            for n in range(size):
                cells_in_block = []
                # collect all cells in the block
                for i in range(bi, bi + block_size):
                    for j in range(bj, bj + block_size):
                        cells_in_block.append((i, j))
                # add clauses to ensure uniqueness in the block
                for idx1 in range(len(cells_in_block)):
                    for idx2 in range(idx1 + 1, len(cells_in_block)):
                        i1, j1 = cells_in_block[idx1]
                        i2, j2 = cells_in_block[idx2]
                        solver.add_clause([-var(i1, j1, n+1), -var(i2, j2, n+1)]) # makes clauses: [¬X001, -X011], [¬X001, -X021], ...
                        clauses['rule 6'].append([-var(i1, j1, n+1), -var(i2, j2, n+1)])


    # solve the SAT problem
    if solver.solve():
        model = solver.get_model()
        solution = [[0]*size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                for n in range(size):
                    if var(i,j,n+1) in model:
                        solution[i][j] = n+1
        return solution, clauses
    else:
        return None



from sudoku import Sudoku, generate_random_sudoku_grid, pretty_print

if __name__ == "__main__":
    puzzle = generate_random_sudoku_grid(num_clues=80)
    print("Generated Sudoku Puzzle:")
    pretty_print(puzzle)

    solution, clauses = solve_sudoku_sat(puzzle)
    if solution:
        print("\nSudoku solved with SAT:")
        pretty_print(solution)

        for sub_clauses in clauses.values():
            print('Number of clauses for rule:', len(sub_clauses))
        

    else:
        print("No SAT solution.")
