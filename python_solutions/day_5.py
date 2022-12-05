from dataclasses import dataclass
import re
from typing import List, Tuple

NUM_STACKS = 9
INITIAL_MAX_HEIGHT = 8
PROCEDURE_START_LINE = 10
CHARS_PER_CRATE = 4

NUM_CRATES_KEYWORD = 'move'
SOURCE_STACK_KEYWORD = 'from'
DEST_STACK_KEYWORD = 'to'

@dataclass
class CraneCommand:
	num_crates_to_move: int
	source_stack: int
	destination_stack: int

	def __str__(self) -> str:
		return (
			f"Moving {self.num_crates_to_move} crates "
			f"from stack {self.source_stack + 1} "
			f"to stack {self.destination_stack + 1}."
		)


@dataclass
class Crane:
	stacks: Tuple[List[str], ...]

	def execute_command(self, command: CraneCommand) -> None:

		picked_up_crates = [
			self.stacks[command.source_stack].pop()
			for _ in range(command.num_crates_to_move)
		]

		dest_stack = self.stacks[command.destination_stack]
		dest_stack += picked_up_crates
	
	@property
	def top_crates(self) -> List[str]:
		_top_crates = []
		for stack in self.stacks:
			_top_crates.append(stack[-1])
		return _top_crates

	def __str__(self) -> str:
		tallest_stack_height = max([len(stack) for stack in self.stacks])
		output = ''
		for n in range(tallest_stack_height):
			row = ''
			for stack in self.stacks:
				try:
					row += f'[{stack[tallest_stack_height - n - 1]}] '
				except IndexError:
					row += ' ' * CHARS_PER_CRATE
			row += '\n'
			output += row
		output += ''.join([f' {n + 1}  ' for n in range(NUM_STACKS)]) + '\n'
		output += ('_' * (CHARS_PER_CRATE * NUM_STACKS) + '\n')
		return output


def decode_stacks() -> Tuple[List[str], ...]:

	stacks: Tuple[List[str], ...] = tuple([[] for _ in range(NUM_STACKS)])

	with open("../inputs/day_5.txt", "r") as f:
		for line in f.readlines()[:INITIAL_MAX_HEIGHT]:
			for n, stack in enumerate(stacks):
				crate = line[n * CHARS_PER_CRATE + 1]
				if crate.isalpha():
					stack.append(crate)

		return stacks


def get_crane_commands() -> List[CraneCommand]:
	command_list = []
	with open("../inputs/day_5.txt", "r") as f:
		for line in f.readlines()[PROCEDURE_START_LINE:]:
			command_list.append(parse_crane_command(line))
	return command_list


def extract_integer_after_keyword(command_string: str, keyword: str) -> int:
	regex = re.compile(keyword + ' \d+')
	return int(regex.findall(command_string)[0][len(keyword):])


def parse_crane_command(command_string: str) -> CraneCommand:

	num_crates = extract_integer_after_keyword(command_string, NUM_CRATES_KEYWORD)
	source = extract_integer_after_keyword(command_string, SOURCE_STACK_KEYWORD)
	dest = extract_integer_after_keyword(command_string, DEST_STACK_KEYWORD)

	return CraneCommand(
		num_crates_to_move=num_crates,
		source_stack=source - 1,
		destination_stack=dest - 1
	)

def main() -> None:
	crane = Crane(decode_stacks())

	print(crane)

	commands = get_crane_commands()

	for command in commands:
		print(command)
		crane.execute_command(command)
		print(crane)

	print(f"{len(commands)} commands executed:")
	print(f"Top crates are {''.join(crane.top_crates)}")


if __name__ == '__main__':
	main()
