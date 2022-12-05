from pathlib import Path
import pandas as pd

# find the files
this_script_path = Path(__file__)
aoc_path = this_script_path.parents[1]
day5_input_path = aoc_path / 'inputs' / 'day_5.txt'

# read everything in with pandas
stack_col_w = [4]*8 + [3]
stack_input = pd.read_fwf(day5_input_path, nrows=8, header=None, widths=stack_col_w)
moves_input = pd.read_csv(day5_input_path, skiprows=10, header=None, delim_whitespace=True)
moves_input.drop([0,2,4], axis=1, inplace=True)
moves_input.rename({1:'move', 3:'from', 5:'to'}, axis=1, inplace=True)


# convert stack input into list of lists
ncols = stack_input.shape[1]
nrows = stack_input.shape[0]
stack_lists = []
for m in range(ncols):
	stack_lists.append([])
	for n in range(nrows):
		rev_idx = nrows - n - 1
		crate = stack_input.iloc[rev_idx, m]
		if isinstance(crate, float): # its only a float if its actually a nan - good import technique with pd.read_fwf
			break
		else:
			stack_lists[-1].append(crate[1])

# iteratre all the moves
for n, row in moves_input.iterrows():
	how_many_to_move = row['move']
	col_to_move_from = row['from'] - 1
	col_to_move_to = row['to'] - 1
	for m in range(how_many_to_move):
		stack_lists[col_to_move_to].append(stack_lists[col_to_move_from].pop())

# they should be all sorted now
# find out the top item from each stack
top_crate_str = ''.join([x.pop() for x in stack_lists])
print(top_crate_str)