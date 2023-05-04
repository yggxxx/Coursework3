import sys

import numpy as np


sys.setrecursionlimit(200000)   # Found that python's default recursion depth is limited (1000 by default), 
                                # so when the recursion depth exceeds 999, 
                                # an exception will be raised.


def get_coordinates_of_blank(matrix, x, y):     # m:" Sudoku Matrix ", 
                                                # x:" Number of blank Spaces ", 
                                                # y:" number of blank Spaces"
    """ Function: Get the coordinates of the next blank space in Sudoku.
    """

    for blank_y in range(y+1, len(matrix)):  # The next blank cell and the current cell are in a row
        if matrix[x][blank_y] == 0:
            return x, blank_y
    for blank_x in range(x+1, len(matrix)):  # When the next blank cell and the current cell are not on the same row
        for blank_y in range(0, len(matrix)):
            if matrix[blank_x][blank_y] == 0:
                return blank_x, blank_y
    return -1, -1               # If there is no next blank space, -1, -1 is returned



def get_pre_satisfied_value(matrix, x, y):
    """ 
    Function: Returns valid values that meet the condition 
        No identical number exists in every horizontal and vertical row and in every nine-cell.
    """
    i, j = x // int(len(matrix) / 3), y // 3
    grid = [matrix[i * int(len(matrix)/3) + r][j * 3 + c] for r in range(int(len(matrix)/3)) for c in range(3)]
    # print('grid:{}'.format(grid))
    v = set([x for x in range(1,int(len(matrix)+1))]) - set(grid) - set(matrix[x]) - \
        set(list(zip(*matrix))[y])
    # print('v:{}'.format(v))
    # print('lst_v:{}'.format(list(v)))
    return list(v)


def get_position_of_first_blank(matrix):
    """Function: Returns the position coordinates of the first blank space"""
    for x in range(len(matrix)):
        for y in range(len(matrix)):
            if matrix[x][y] == 0:
                return x, y
    return False, False  # If the Sudoku is complete, return False, False


def step_forward_sudoku(matrix, x, y):
    """ Function: Try filling out Sudoku """
    for v in get_pre_satisfied_value(matrix, x, y):
        matrix[x][y] = v
        next_x, next_y = get_coordinates_of_blank(matrix, x, y)
        if next_y == -1: # If there is no next blank space
            return True
        else:
            end = step_forward_sudoku(matrix, next_x, next_y) # recursion
            if end:
                return True
            matrix[x][y] = 0 # In the process of recursion, 
                        # if the Sudoku is not solved, go back to the previous blank space


def result_of_sudoku(matrix):
    x, y = get_position_of_first_blank(matrix)
    step_forward_sudoku(matrix, x, y)

    print(np.array(matrix))


if __name__ == "__main__":


    m2_3 = [[0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
    m3_3 = [
        [6, 0, 0, 1, 0, 0, 7, 0, 8],
        [0, 0, 0, 8, 0, 0, 2, 0, 0],
        [2, 3, 8, 0, 5, 0, 1, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 9, 2],
        [0, 0, 4, 3, 0, 8, 6, 0, 0],
        [3, 7, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 3, 0, 7, 0, 5, 2, 6],
        [0, 0, 2, 0, 0, 4, 0, 0, 0],
        [9, 0, 7, 0, 0, 6, 0, 0, 4]
    ]
    result_of_sudoku(m2_3)
    result_of_sudoku(m3_3)

'''
2*3 output
[[2 3 1 4 5 6]
 [4 5 6 1 2 3]
 [1 2 3 5 6 4]
 [5 6 4 2 3 1]
 [3 1 2 6 4 5]
 [6 4 5 3 1 2]]

3*3 output
[
[6, 9, 5, 1, 2, 3, 7, 4, 8], 
[7, 4, 1, 8, 6, 9, 2, 5, 3], 
[2, 3, 8, 4, 5, 7, 1, 6, 9], 
[8, 1, 6, 7, 4, 5, 3, 9, 2], 
[5, 2, 4, 3, 9, 8, 6, 7, 1], 
[3, 7, 9, 6, 1, 2, 4, 8, 5], 
[4, 8, 3, 9, 7, 1, 5, 2, 6], 
[1, 6, 2, 5, 8, 4, 9, 3, 7], 
[9, 5, 7, 2, 3, 6, 8, 1, 4]]
'''
