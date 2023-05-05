import copy
import time
import random
 
#Grids 1-5 are 2x2
grid1 = [
        [1, 0, 4, 2],
        [4, 2, 1, 3],
        [2, 1, 3, 4],
        [3, 4, 2, 1]]

grid2 = [
        [1, 0, 4, 2],
        [4, 2, 1, 3],
        [2, 1, 0, 4],
        [3, 4, 2, 1]]

grid3 = [
        [1, 0, 4, 2],
        [4, 2, 1, 0],
        [2, 1, 0, 4],
        [0, 4, 2, 1]]

grid4 = [
        [1, 0, 4, 2],
        [0, 2, 1, 0],
        [2, 1, 0, 4],
        [0, 4, 2, 1]]

grid5 = [
        [1, 0, 0, 2],
        [0, 0, 1, 0],
        [0, 1, 0, 4],
        [0, 0, 0, 1]]

#3x2
grid6 = [
        [0, 0, 6, 0, 0, 3],
        [5, 0, 0, 0, 0, 0],
        [0, 1, 3, 4, 0, 0],
        [0, 0, 0, 0, 0, 6],
        [0, 0, 1, 0, 0, 0],
        [0, 5, 0, 0, 6, 4]]

#3x3
grid7 = [
        [9,4,1,0,6,0,8,5,0], 
        [5,8,3,0,1,9,7,0,6],
        [0,0,7,5,0,0,0,4,0],
        [2,0,0,0,5,8,1,7,4],
        [0,7,0,0,0,0,0,0,0],
        [0,0,0,9,7,0,5,0,0],
        [0,0,9,1,4,6,0,0,0],
        [8,0,0,7,9,0,0,0,5],
        [7,0,2,8,3,5,0,1,0]]

grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), (grid5, 2, 2), (grid6,2,3),(grid7,3,3)]
'''
===================================
DO NOT CHANGE CODE ABOVE THIS LINE
===================================
'''
def check_section(section, n):

    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n+1)]):
        return True
    return False


def get_squares(grid, n_rows, n_cols):

    squares = []
    for i in range(n_cols):
        rows = (i*n_rows, (i+1)*n_rows)
        for j in range(n_rows):
            cols = (j*n_cols, (j+1)*n_cols)
            square = []
            for k in range(rows[0], rows[1]):
                line = grid[k][cols[0]:cols[1]]
                square +=line
            squares.append(square)


    return(squares)


def check_solution(grid, n_rows, n_cols):
    '''
    This function is used to check whether a sudoku board has been correctly solved

    args: grid - representation of a suduko board as a nested list.
    returns: True (correct solution) or False (incorrect solution)
    '''
    n = n_rows*n_cols

    for row in grid:
        if check_section(row, n) == False:
            return False

    for i in range(n_rows):
        column = []
        for row in grid:
            column.append(row[i])
        if check_section(column, n) == False:
            return False

    squares = get_squares(grid, n_rows, n_cols)
    for square in squares:
        if check_section(square, n) == False:
            return False

    return True

def is_valid(grid, n_rows, n_cols, r, c, k):
    for i in range(len(grid)):
        if grid[r][i] == k:
            return False
    for j in range(len(grid)):
        if grid[j][c] == k:
            return False
    start_row = (r//n_rows)*n_rows
    start_col = (c//n_cols)*n_cols
    for i in range(start_row, start_row + n_rows):
        for j in range(start_col, start_col + n_cols):
            if grid[i][j] == k:
                return False
    return True
    

def recursive_solve(grid, n_rows, n_cols):
    #n = n_rows*n_cols
    def backtracking(grid, n_rows, n_cols):
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0: continue
                for k in range(1, len(grid)+1):
                    if is_valid(grid, n_rows, n_cols, i, j, k):
                        grid[i][j] = k
                        if backtracking(grid, n_rows, n_cols):
                            return True
                        grid[i][j] = 0
                return False
        return True
    backtracking(grid, n_rows, n_cols)
    return grid


def random_solve(grid, n_rows, n_cols, max_tries=500):
    nums = list(range(1,len(grid)+1))

    for i in range(max_tries):
        try_grid = copy.deepcopy(grid)
        for x in range(len(grid)):
            for y in range(len(grid)):
                if try_grid[x][y] == 0:
                    random.shuffle(nums)
                    try_grid[x][y] = nums[0]
        if check_solution(try_grid, n_rows, n_cols):
            break
        
    return try_grid

def solve(grid, n_rows, n_cols):

    '''
    Solve function for Sudoku coursework.
    Comment out one of the lines below to either use the random or recursive solver
    '''
    
    #return random_solve(grid, n_rows, n_cols,10000)
    return recursive_solve(grid, n_rows, n_cols)


'''
===================================
DO NOT CHANGE CODE BELOW THIS LINE
===================================
'''
def main():

    points = 0

    print("Running test script for coursework 3 task1")
    print("====================================")
    
    for (i, (grid, n_rows, n_cols)) in enumerate(grids):
        print("Solving grid: %d" % (i+1))
        start_time = time.time()
        solution = solve(grid, n_rows, n_cols)
        elapsed_time = time.time() - start_time
        print("Solved in: %f seconds" % elapsed_time)
        print(solution)
        if check_solution(solution, n_rows, n_cols):
            print("grid %d correct" % (i+1))
            points = points + 10
        else:
            print("grid %d incorrect" % (i+1))

    print("====================================")
    print("Test script complete, Total points: %d" % points)


if __name__ == "__main__":
    main()
