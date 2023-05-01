#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  24 11:37:30 2023

@author: yaogongxi
"""

import time
def solve_sudoku(sudoku):
    """
    Solve a Sudoku puzzle using the Wavefront propagation algorithm.

    Args:
        sudoku (list): A nested list representing a Sudoku grid.

    Returns:
        The solved Sudoku grid, or None if no solution could be found.
    """
    if len(sudoku) == 9:
        box_size_x = 3
        box_size_y = 3
    if len(sudoku) == 6:
        box_size_x = 2
        box_size_y = 3
        
    # Define a function to get the possible values for an empty location
    def get_possible_values(i, j):
        """
        Get the possible values for an empty location in the Sudoku grid.
        """
        # Get the existing numbers in the current row, column, and box
        row_vals = set(sudoku[i])
        col_vals = set(row[j] for row in sudoku)
        box_i, box_j = (i // box_size_x) * box_size_x, (j // box_size_y) * box_size_y
        box_vals = set(
            sudoku[m][n]
            for m in range(box_i, box_i + box_size_x)
            for n in range(box_j, box_j + box_size_y)
        )
        # Get the possible numbers for the current location
        return set(range(1, len(sudoku)+1)) - row_vals - col_vals - box_vals

    # Define a function to iterate over the entire Sudoku grid, eliminating possible values based on known values in each row, column, and box, and update the current Sudoku state
    def propagate_wavefront():
        """
        Iterate over the Sudoku grid, eliminating possible values based on known values in each row, column, and box.
        """
        while True:
            updated = False
            for i in range(len(sudoku)):
                for j in range(len(sudoku)):
                    if sudoku[i][j] != 0:
                        # If there is already a number at this location, skip it
                        continue
                    poss_vals = get_possible_values(i, j)
                    if len(poss_vals) == 0:
                        # No possible values, return False for unsolvable
                        return False
                    elif len(poss_vals) == 1:
                        # Only one possible value, fill it in and update the state
                        sudoku[i][j] = next(iter(poss_vals))
                        updated = True
                    else:
                        # Multiple possible values, remove known numbers from the current row, column, and box to get the remaining possible values, and update the state
                        row_vals = set(sudoku[i][k] for k in range(len(sudoku[0])) if sudoku[i][k] != 0)
                        col_vals = set(sudoku[k][j] for k in range(len(sudoku)) if sudoku[k][j] != 0)
                        box_i, box_j = (i // box_size_x) * box_size_x, (j // box_size_y) * box_size_y
                        box_vals = set(
                            sudoku[m][n]
                            for m in range(box_i, box_i + box_size_x)
                            for n in range(box_j, box_j + box_size_y)
                            if (sudoku[m][n] != 0)
                        )
                        poss_vals -= row_vals | col_vals | box_vals

                        if len(poss_vals) == 0:
                            # No possible values, return False for unsolvable
                            return False
                        elif len(poss_vals) == 1:
                            # Only one possible value, fill it in and update the state
                            sudoku[i][j] = next(iter(poss_vals))
                            updated = True
            if not updated:
                # If there are no more updates, we can't solve any further with wavefront propagation
                break
        return True

    # Define a function to choose the unfilled location with the fewest possible values and try each value recursively
    def search():
        """
        Choose the unfilled location with the fewest possible values and try each value recursively.
        """
        min_poss_vals = len(sudoku) + 1
        min_i, min_j = None, None
        for i in range(len(sudoku)):
            for j in range(len(sudoku[0])):
                if sudoku[i][j] != 0:
                    # If there is already a number at this location, skip it
                    continue
                poss_vals = get_possible_values(i, j)
                if len(poss_vals) < min_poss_vals:
                    # Keep track of the location with the minimum possible values
                    min_poss_vals = len(poss_vals)
                    min_i, min_j = i, j
        if min_i is None:
            # No more empty locations, return True for solved
            return True
        poss_vals = get_possible_values(min_i, min_j)
        for val in poss_vals:
            new_sudoku = [row[:] for row in sudoku]
            # Try each possible value and update the state
            new_sudoku[min_i][min_j] = val
            if solve_sudoku(new_sudoku):
                # Found a solution
                # Update the state and return True
                for i in range(len(sudoku)):
                    for j in range(len(sudoku[0])):
                        sudoku[i][j] = new_sudoku[i][j]
                return True
        # Tried all possible values and didn't find a solution
        return False

    if propagate_wavefront():
        if all(val != 0 for row in sudoku for val in row):
            # Sudoku is filled, return the solution
            return sudoku
        elif search():
            # Found a solution through backtracking, update the Sudoku state and return the solution
            return sudoku
    # Could not find a solution, return None
    return None


# The example of 3*3 grid (hard1)
grid = [
    [0, 2, 0, 0, 0, 0, 0, 1, 0],    # [7, 2, 3, 8, 5, 6, 4, 1, 9]
    [0, 0, 6, 0, 4, 0, 0, 0, 0],    # [1, 9, 6, 3, 4, 7, 5, 2, 8]
    [5, 8, 0, 0, 9, 0, 0, 0, 3],    # [5, 8, 4, 2, 9, 1, 7, 6, 3]
    [0, 0, 0, 0, 0, 3, 0, 0, 4],    # [8, 5, 9, 6, 2, 3, 1, 7, 4]
    [4, 1, 0, 0, 8, 0, 6, 0, 0],    # [4, 1, 7, 9, 8, 5, 6, 3, 2]
    [0, 0, 0, 0, 0, 0, 0, 9, 5],    # [3, 6, 2, 1, 7, 4, 8, 9, 5]
    [2, 0, 0, 0, 1, 0, 0, 8, 0],    # [2, 4, 5, 7, 1, 9, 3, 8, 6]
    [0, 0, 0, 0, 0, 0, 0, 0, 0],    # [6, 7, 8, 5, 3, 2, 9, 4, 1]
    [0, 3, 1, 0, 0, 8, 0, 5, 7]     # [9, 3, 1, 4, 6, 8, 2, 5, 7]
]


'''
# The example of 3*2 grid (easy3)
grid = [
    [0, 3, 0, 4, 0, 0],    # [1, 3, 6, 4, 5, 2]
    [0, 0, 5, 6, 0, 3],    # [2, 4, 5, 6, 1, 3]
    [0, 0, 0, 1, 0, 0],    # [6, 5, 3, 1, 2, 4]
    [0, 1, 0, 3, 0, 5],    # [4, 1, 2, 3, 6, 5]
    [0, 6, 4, 0, 3, 1],    # [5, 6, 4, 2, 3, 1]
    [0, 0, 1, 0, 4, 6],    # [3, 2, 1, 5, 4, 6]
]
'''

'''
# The example of 3*3 grid (easy1)
grid = [
    [9, 0, 6, 0, 0, 1, 0, 4, 0],    # [9, 8, 6, 3, 5, 1, 2, 4, 7]
    [7, 0, 1, 2, 9, 0, 0, 6, 0],    # [7, 3, 1, 2, 9, 4, 8, 6, 5]
    [4, 0, 2, 8, 0, 6, 3, 0, 0],    # [4, 5, 2, 8, 7, 6, 3, 9, 1]
    [0, 0, 0, 0, 2, 0, 9, 8, 0],    # [3, 1, 5, 6, 2, 7, 9, 8, 4]
    [6, 0, 0, 0, 0, 0, 0, 0, 2],    # [6, 7, 8, 4, 3, 9, 5, 1, 2]
    [0, 9, 4, 0, 8, 0, 0, 0, 0],    # [2, 9, 4, 1, 8, 5, 6, 7, 3]
    [0, 0, 3, 7, 0, 8, 4, 0, 9],    # [1, 2, 3, 7, 6, 8, 4, 5, 9]
    [0, 4, 0, 0, 1, 3, 7, 0, 6],    # [8, 4, 9, 5, 1, 3, 7, 2, 6]
    [0, 6, 0, 9, 0, 0, 1, 0, 8]     # [5, 6, 7, 9, 4, 2, 1, 3, 8]
]
'''

'''
# The example of 3*3 grid (easy2)
grid = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],    # [4, 3, 5, 2, 6, 9, 7, 8, 1]
    [6, 8, 0, 0, 7, 0, 0, 9, 0],    # [6, 8, 2, 5, 7, 1, 4, 9, 3]
    [1, 9, 0, 0, 0, 4, 5, 0, 0],    # [1, 9, 7, 8, 3, 4, 5, 6, 2]
    [8, 2, 0, 1, 0, 0, 0, 4, 0],    # [8, 2, 6, 1, 9, 5, 3, 4, 7]
    [0, 0, 4, 6, 0, 2, 9, 0, 0],    # [3, 7, 4, 6, 8, 2, 9, 1, 5]
    [0, 5, 0, 0, 0, 3, 0, 2, 8],    # [9, 5, 1, 7, 4, 3, 6, 2, 8]
    [0, 0, 9, 3, 0, 0, 0, 7, 4],    # [5, 1, 9, 3, 2, 6, 8, 7, 4]
    [0, 4, 0, 0, 5, 0, 0, 3, 6],    # [2, 4, 8, 9, 5, 7, 1, 3, 6]
    [7, 0, 3, 0, 1, 8, 0, 0, 0]     # [7, 6, 3, 4, 1, 8, 2, 5, 9]
]
'''

'''
# The example of 3*3 grid (med1)
grid = [
    [0, 0, 0, 6, 0, 0, 0, 0, 0],    # [5, 4, 1, 6, 7, 2, 9, 8, 3]
    [0, 0, 0, 0, 0, 0, 5, 0, 1],    # [2, 8, 7, 4, 9, 3, 5, 6, 1]
    [3, 6, 9, 0, 8, 0, 4, 0, 0],    # [3, 6, 9, 5, 8, 1, 4, 7, 2]
    [0, 0, 0, 0, 0, 6, 8, 0, 0],    # [9, 1, 3, 7, 5, 6, 8, 2, 4]
    [0, 0, 0, 1, 3, 0, 0, 0, 9],    # [6, 2, 8, 1, 3, 4, 7, 5, 9]
    [4, 0, 5, 0, 0, 9, 0, 0, 0],    # [4, 7, 5, 8, 2, 9, 1, 3, 6]
    [0, 0, 0, 0, 0, 0, 3, 0, 0],    # [7, 9, 4, 2, 6, 5, 3, 1, 8]
    [0, 0, 6, 0, 0, 7, 0, 0, 0],    # [8, 3, 6, 9, 1, 7, 2, 4, 5]
    [1, 0, 0, 3, 4, 0, 0, 0, 0]     # [1, 5, 2, 3, 4, 8, 6, 9, 7]
]
'''

'''
# The example of 3*3 grid (med2)
grid = [
    [8, 0, 9, 0, 2, 0, 3, 0, 0],    # [8, 6, 9, 5, 2, 7, 3, 4, 1]
    [0, 3, 7, 0, 6, 0, 5, 0, 0],    # [4, 3, 7, 1, 6, 8, 5, 2, 9]
    [0, 0, 0, 4, 0, 9, 7, 0, 0],    # [2, 5, 1, 4, 3, 9, 7, 8, 6]
    [0, 0, 2, 9, 0, 1, 0, 6, 0],    # [3, 4, 2, 9, 5, 1, 8, 6, 7]
    [1, 0, 0, 3, 0, 6, 0, 0, 0],    # [1, 9, 8, 3, 7, 6, 4, 5, 2]
    [0, 0, 0, 0, 0, 0, 1, 0, 3],    # [6, 7, 5, 8, 4, 2, 1, 9, 3]
    [7, 0, 0, 0, 0, 0, 0, 0, 8],    # [7, 2, 4, 6, 1, 5, 9, 3, 8]
    [5, 0, 0, 0, 0, 0, 0, 1, 4],    # [5, 8, 6, 7, 9, 3, 2, 1, 4]
    [0, 0, 0, 2, 8, 4, 6, 0, 5]     # [9, 1, 3, 2, 8, 4, 6, 7, 5]
]
'''

def test_solve_sudoku(grid):
    for row in grid:
        print(row)
    # Solve the example Sudoku grid using the solve_sudoku function
    solution = solve_sudoku(grid)

    if solution is not None:
        print("Solution found:")
        for row in solution:
            print(row)
    else:
        print("No solution found.")

if __name__ == "__main__":
    # Record the program start time
    start_time = time.time()
    test_solve_sudoku(grid)
    # Record the program end time
    end_time = time.time()
    # Computing solution time
    solve_time = end_time - start_time

    print("Wavefront propagation solve time: {:.5f} s".format(solve_time))

    
    
    
    
    
    
    
    