class Sudoku:
    def __init__(self, grid, size=9, block=3):
        self.initial_state = grid
        self.size = size
        self.block = block 

    def get_actions(self, state):
        actions = []
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:  # empty cell
                    for num in range(1, self.size + 1):
                        if self.is_valid(state, i, j, num):
                            actions.append((i, j, num)) # get possible actions
                    return actions  # return after finding first empty cell
        return actions

    def apply_action(self, state, action):
        # action is a tuple (i, j, num)
        i, j, num = action
        new_state = [row[:] for row in state]
        new_state[i][j] = num
        return new_state

    def is_goal(self, state):
        for row in state: # must contain no zeroes
            if 0 in row:
                return False
    
        for i in range(self.size):
            if not self.is_unique(state[i]):  # rows
                return False
        for j in range(self.size):
            if not self.is_unique([state[i][j] for i in range(self.size)]):  # cols
                return False
        # blocks 3x3
        for bi in range(0, self.size, self.block):
            for bj in range(0, self.size, self.block):
                block = [state[i][j] for i in range(bi, bi+self.block) for j in range(bj, bj+self.block)]
                if not self.is_unique(block):
                    return False
        return True

    def is_unique(self, nums):
        # count non-zero numbers and check uniqueness
        nums = [n for n in nums if n != 0]
        return len(nums) == len(set(nums))

    def is_valid(self, state, row, col, num):
        # check row
        if num in state[row]:
            return False
        # check column
        if num in [state[i][col] for i in range(self.size)]:
            return False
        # check block
        start_row, start_col = row - row % self.block, col - col % self.block
        for i in range(start_row, start_row + self.block):
            for j in range(start_col, start_col + self.block):
                if state[i][j] == num:
                    return False
        return True

    def state_to_hashable(self, state):
        return tuple(tuple(row) for row in state)
    

def generate_random_sudoku_grid(size=9, block=3, num_clues=30):
    import random
    def fill_grid(grid):
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 0:
                    nums = list(range(1, size + 1))
                    random.shuffle(nums)
                    for num in nums:
                        if Sudoku(grid).is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    grid = [[0]*size for _ in range(size)]
    fill_grid(grid)

    # Remove numbers to create clues
    cells = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(cells)
    for i, j in cells[:size*size - num_clues]:
        grid[i][j] = 0

    return grid


def pretty_print(grid):
    for k in range(len(grid)):
        row = grid[k]
        if k % 3 == 0 and k != 0:
            print("- - - + - - - + - - -")
        for i in range(len(row)):
            if i % 3 == 0 and i != 0 and i != len(row):
                print("|", end=" ")
            if i == len(row) - 1:
                if row[i]!= 0: print(row[i]) 
                else: print(".")
            else:
                if row[i]!= 0: print(row[i], end=" ") 
                else: print(".", end=" ")


def check_solution(grid):
    sudoku = Sudoku(grid)
    return sudoku.is_goal(grid)

import requests

def sudoku_parser(line):
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            char = line[i*9 + j]
            if char == '.':
                row.append(0)
            else:
                row.append(int(char))
        grid.append(row)
    return grid

def get_sudokus_from_web(url):
    sudokus = []
    resp = requests.get(url)
    text = resp.text
    print('Parsing web page...')
    for line in text.splitlines():
        line = line.strip()
        if len(line) == 81 and all(c.isdigit() or c == '.' for c in line):
            grid = sudoku_parser(line)
            sudokus.append(grid)
    return sudokus

if __name__ == "__main__":
    url = "http://magictour.free.fr/top2365"
    sudokus = get_sudokus_from_web(url)
    print(f"Trovati {len(sudokus)} sudoku")

