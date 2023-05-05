For Task1:

This program to solve the Sudoku matrix in the internal modification of the matrix to be solved, input after the execution of the script can be obtained. Run the python HaonanZhou_task01.py command. HaonanZhou_task01.py for task1 run separately, if you want to go to run task1 and task2 integration, please run ChenzhengxiongZhang/Haonanzhou_task1.py
This file is two people cooperation after the integration of the program.



For Task2:

I write code to parse the following flags:
-explain, which provides a set of instructions for solving the puzzle.
-file INPUT OUTPUT, which reads a grid from the input file, solves it, and then saves the solution to the output file.
-hint N, which rather than giving the full solution, instead returns a grid with N values filled in.
-profile, which measures the performance of the solution for grids of different size and difficulties.
I also write the main function that acts as an entry point to parse these flags and select the appropriate behavior.



For Task3:

This code contains a Python implementation of the Wavefront propagation program to solve Sudoku puzzles. The program is implemented in the function ‘solve_sudoku’, which takes as input a nested list representing a grid of Sudoku, where empty locations are represented as [1, 2, …, 9].

The program works by iteratively propagating known values in each row, column, and box to eliminate possible values in neighboring cells. This reduces the number of possible values for each cell and allows the algorithm to fill in more cells. If this process does not solve the puzzle entirely, the program searches for the unfilled location with the fewest possible values and tries each value recursively until it finds a solution or exhausts all possibilities.

The program includes three helper functions:
1. The ‘get_possible_values’ is to get the possible values for an empty location in the Sudoku grid.
2. The ‘propagate_wavefront’ is to iterate over the Sudoku grid, eliminating possible values based on the know values in each row, column, and box.
3. The ‘search’ is to choose the unfilled location with the fewest possible values and try each value recursively.

The function ‘test_solve_sudoku’ includes an example Sudoku grid and its expected solution. The function tests the ‘solve_sudoku’ function by solving the example Sudoku grid and comparing the result to the expected solution.
