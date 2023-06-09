import random
import copy
import time
import sys
import matplotlib.pyplot as plt

explain_flag = False
file_flag = False
hint_flag = False
profile_flag = False
hint_n = 0
input_file = ""
output_file = ""
solution_hint = []
fout = open(sys.argv[0],'r')

#Grids 1-4 are 2x2
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

grid6 = [
		[0, 0, 6, 0, 0, 3],
		[5, 0, 0, 0, 0, 0],
		[0, 1, 3, 4, 0, 0],
		[0, 0, 0, 0, 0, 6],
		[0, 0, 1, 0, 0, 0],
		[0, 5, 0, 0, 6, 4]]

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

grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), (grid5, 2, 2), (grid6,2,3), (grid7,3,3)]
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

#To complete the first assignment, please write the code for the following function
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

	for i in range(n_rows**2):
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


def find_empty(grid):
	'''
	This function returns the index (i, j) to the first zero element in a sudoku grid
	If no such element is found, it returns None

	args: grid
	return: A tuple (i,j) where i and j are both integers, or None
	'''

	for i in range(len(grid)):
		row = grid[i]
		for j in range(len(row)):
			if grid[i][j] == 0:
				return (i, j)

	return None

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
		global hint_n
		global solution_hint
		for i in range(len(grid)):
			for j in range(len(grid)):
				if grid[i][j] != 0: continue
				for k in range(1, len(grid)+1):
					if is_valid(grid, n_rows, n_cols, i, j, k):
						grid[i][j] = k
						if backtracking(grid, n_rows, n_cols):
							if explain_flag:
								if hint_flag == True:
									if hint_n > 0:
										my_print("Put %d in location(%d, %d)" % (k,i+1,j+1))
										solution_hint[i][j] = k
										hint_n -= 1
								else:
									my_print("Put %d in location(%d, %d)" % (k,i+1,j+1))
							return True
						grid[i][j] = 0
				return False
		return True
	backtracking(grid, n_rows, n_cols)
	return grid

def random_solve(grid, n_rows, n_cols, max_tries=50000):
	'''
	This function uses random trial and error to solve a Sudoku grid

	args: grid, n_rows, n_cols, max_tries
	return: A solved grid (as a nested list), or the original grid if no solution is found
	'''

	for i in range(max_tries):
		possible_solution = fill_board_randomly(grid, n_rows, n_cols)
		if check_solution(possible_solution, n_rows, n_cols):
			return possible_solution

	return grid

def fill_board_randomly(grid, n_rows, n_cols):
	'''
	This function will fill an unsolved Sudoku grid with random numbers

	args: grid, n_rows, n_cols
	return: A grid with all empty values filled in
	'''
	n = n_rows*n_cols
	#Make a copy of the original grid
	filled_grid = copy.deepcopy(grid)

	#Loop through the rows
	for i in range(len(grid)):
		#Loop through the columns
		for j in range(len(grid[0])):
			#If we find a zero, fill it in with a random integer
			if grid[i][j] == 0:
				filled_grid[i][j] = random.randint(1, n)

	return filled_grid 

def solve(grid, n_rows, n_cols):

	'''
	Solve function for Sudoku coursework.
	Comment out one of the lines below to either use the random or recursive solver
	'''
	
	#return random_solve(grid, n_rows, n_cols)
	return recursive_solve(grid, n_rows, n_cols)

def my_print(msg):
	global fout
	print(msg)
	if file_flag:
		if isinstance(msg, list):
			for x in msg:
				for y in x:
					fout.write(str(y))
					fout.write(',')
				fout.write('\n')
		else:
			fout.write(msg + '\n')

'''
===================================
DO NOT CHANGE CODE BELOW THIS LINE
===================================
'''
def main():
	global explain_flag
	global file_flag
	global hint_flag
	global profile_flag
	global hint_n
	global input_file
	global output_file
	global solution_hint
	global fout
	global grids
	
	performance_2x2 = {}
	performance_3x2 = {}
	performance_3x3 = {}
	
	points = 0  
	for i in range(len(sys.argv)):
		if sys.argv[i] == '-explain':
			explain_flag = True
		if sys.argv[i] == '-file':
			file_flag = True
			input_file = sys.argv[i+1]
			output_file = sys.argv[i+2]
		if sys.argv[i] == '-hint':
			hint_flag = True
			hint_n = int(sys.argv[i+1])
		if sys.argv[i] == '-profile':
			profile_flag = True
	
	#if explain_flag == True:
	#	my_print("explain....")
	if file_flag == True:
		grid = []
		with open(input_file, 'r') as fin:
			line = fin.readline()
			while line:
				#print(line)
				grid.append(list(map(int, line.strip().split(','))))
				line = fin.readline()
		#print(grid)
		grids = []
		if len(grid) == 6:
			grids.append((grid,2,3))
		if len(grid) == 9:
			grids.append((grid,3,3))
			
		fout = open(output_file, 'w')
		
	#if profile_flag == True:
	#	print("profile.........")	

	my_print("Running test script for coursework 3")
	my_print("====================================")
	
	for (i, (grid, n_rows, n_cols)) in enumerate(grids):
		difficulties = 0
		for x in grid:
			for y in x:
				if y==0:
					difficulties += 1
		#print("difficulties: %d" % difficulties)
		
		solution_hint = copy.deepcopy(grid)
		#print(solution_hint)
		my_print("Solving grid: %d" % (i+1))
		start_time = time.time()
		#my_print(grid)
		solution = solve(grid, n_rows, n_cols)
		elapsed_time = time.time() - start_time
		my_print("Solved in: %f seconds" % elapsed_time)
		
		performance = {}	
		if len(grid) == 4:
			performance = performance_2x2
		elif len(grid) == 6:
			performance = performance_3x2
		elif len(grid) == 9:
			performance = performance_3x3
			
		if difficulties in performance:
			performance[difficulties].append(elapsed_time)
		else:
			performance[difficulties] = []
			performance[difficulties].append(elapsed_time)	
			
		if explain_flag and hint_flag:
			my_print(solution_hint)	
		else:
			my_print(solution)
			if check_solution(solution, n_rows, n_cols):
				my_print("grid %d correct" % (i+1))
				points = points + 10
			else:
				my_print("grid %d incorrect" % (i+1))

	my_print("====================================")
	
	if hint_flag:
		my_print("Test script complete")
	else:
		my_print("Test script complete, Total points: %d" % points)
	
	if file_flag:
		my_print("\nsuccessfully saved the output file\n")
		fout.close()
		
	if profile_flag:	
		plt.xlabel('difficulties')
		plt.ylabel('performance')
	
		x1 = []
		y1 = []
		for key in performance_2x2:
			x1.append(key)
			y1.append(sum(performance_2x2[key])/len(performance_2x2[key]))
		#plt.subplot(131)
		plt.plot(x1,y1,label='grid size 2x2')
			
		x2 = []
		y2 = []
		for key in performance_3x2:
			x2.append(key)
			y2.append(sum(performance_3x2[key])/len(performance_3x2[key]))
		plt.plot(x2,y2,label='grid size 3x2')
		
		x3 = []
		y3 = []
		for key in performance_3x3:
			x3.append(key)
			y3.append(sum(performance_3x3[key])/len(performance_3x3[key]))	
		plt.plot(x3,y3,label='grid size 3x3')
		plt.legend()
		plt.show()
	

if __name__ == "__main__":
	main()
