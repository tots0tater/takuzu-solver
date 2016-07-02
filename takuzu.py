import re, itertools, copy

def rotate_right(puzzle):
	"""
	Rotates the puzzle right thus making
	our columns into our rows and vice versa
	"""
	return [''.join(t) for t in zip(*puzzle[::-1])]

def rotate_left(puzzle):
	"""
	Rotates the puzzle left thus making
	our rows back into our columns
	"""
	return [''.join(t) for t in list(zip(*puzzle))[::-1]]

def replace_twos(line):
	"""
	An easy placement of alternating numbers. 
	Helps fill out the initial board
	"""
	line = line.replace('.00.', '1001')
	line = line.replace('00.', '001')
	line = line.replace('.00', '100')
	
	line = line.replace('.11.', '0110')
	line = line.replace('11.', '110')
	line = line.replace('.11', '011')

	line = line.replace('1.1', '101')
	line = line.replace('0.0', '010')

	return line

def half_filled(line):
	"""
	Fills all .s with the opposite number
	if the board has half already filled
	"""
	if line.count('1') == (len(line) // 2):
		line = line.replace('.', '0')
	elif line.count('0') == (len(line) // 2):
		line = line.replace('.', '1')

	return line

def solve_partial(puzzle):
	"""
	Finds rows and columns that match a 
	criteria and replaces them 
	"""
	for i in range(len(puzzle)):
		puzzle[i] = replace_twos(puzzle[i])
		puzzle[i] = half_filled(puzzle[i])

	rot_puzzle = rotate_right(puzzle)
	for i in range(len(rot_puzzle)):
		rot_puzzle[i] = replace_twos(rot_puzzle[i])
		rot_puzzle[i] = half_filled(rot_puzzle[i])

	puzzle = rotate_left(rot_puzzle)

	return puzzle

def fill_rest(puzzle, valid_lines):
	"""
	Brute force solves the rest of the
	puzzle by populating potential 
	solutions for each line and validating
	whether the entire puzzle is valid
	"""
	# In the unlikely scenario where we've already solved it
	if satisfy_constraints(puzzle):
		return puzzle

	line_solutions = []
	for i in range(len(puzzle)):
		sol = set()
		for line in valid_lines:
			if like_original(puzzle[i], line):
				sol.add(line)
		line_solutions.append(list(sol))

	filled_puzzles = list(itertools.product(*line_solutions))

	for p in filled_puzzles:
		if satisfy_constraints(p):
			return p

	print("UH OH")

def satisfy_constraints(puzzle):
	"""
	Checks a bunch of criteria the puzzle must
	match before it satisfies the constraints.
	"""
	rot_puzzle = rotate_right(puzzle)

	contain_dot = not any(['.' in line for line in puzzle])
	reg_eq = all([equal_num(line) for line in puzzle])
	rot_eq = all([equal_num(line) for line in rot_puzzle])

	# Make sure all of the rows/columns are unique
	reg_diff = [puzzle.count(line) for line in puzzle] == [1]*len(puzzle)
	rot_diff = [rot_puzzle.count(line) for line in rot_puzzle] == [1]*len(puzzle)

	# If any of them have three consecutive
	reg_consecutive = not any([three_consecutive(line) for line in puzzle])
	rot_consecutive = not any([three_consecutive(line) for line in rot_puzzle])

	return all([contain_dot, reg_eq, rot_eq, reg_diff, rot_diff, reg_consecutive, rot_consecutive])

def like_original(line, potential_solution):
	# Our line is already in the form of a regular
	# expression. '.' is a wildcard 
	return True if re.match(line, potential_solution) else False

def three_consecutive(line):
	"""
	Returns a bool whether or not there are three
	consecutive numbers in a row on our line
	"""
	return True if re.search('[0]{3,}|[1]{3,}', line) else False

def equal_num(line):
	"""
	Returns a bool determining if there are more
	1s than half the length of our line
	"""
	if line.count('1') > len(line) // 2 or line.count('0') > len(line) // 2:
		return False
	return True

def flatten(deep_list):
	while type(deep_list[0]) == type([]):
		deep_list = list(itertools.chain.from_iterable(deep_list))

	return deep_list

def build_perms(s, match, left):
	"""
	A recursive function that takes an original 
	prefix, a dictionary that matches with the
	prefix, and the number of iterations we have
	left. Returns all the permutations for a prefix.
	"""
	if left == 0:
		return s[:-2] # Cut off our last two appended 
	prefix = s[-2:]
	return [build_perms(s + postfix, match, left - 2) for postfix in match[prefix]]

def get_permutations(size):
	# A dictionary to match all of our valid 
	# prefixes with all valid postfixes
	match = {
		'00': ['10', '11'],
		'01': ['01', '10', '00'],
		'10': ['01', '10', '11'],
		'11': ['00', '01']
	}

	perms = [build_perms(key, match, size) for key in match]
	perms = list(set(flatten(perms)))
	return list(filter(equal_num, perms))

def print_puzzle(puzzle):
	for line in puzzle:
		print(line)
	print()

if __name__ == '__main__':
	puzzle = open('puzzle.txt', 'r').readlines()
	puzzle = [line.replace('\n', '') for line in puzzle]

	print("ORIGINAL")
	print_puzzle(puzzle)
	
	puzzle_copy = []
	# Go until our solve partial returns the
	# same puzzle as before; this means we
	# can't get any more easy placements
	while puzzle != puzzle_copy:
		puzzle_copy = copy.deepcopy(puzzle)
		puzzle = solve_partial(puzzle)

	print("AFTER PARTIAL")
	print_puzzle(puzzle)

	valid_lines = get_permutations(len(puzzle))
	puzzle = fill_rest(puzzle, valid_lines)
	
	print("AFTER FILL")
	print_puzzle(puzzle)
