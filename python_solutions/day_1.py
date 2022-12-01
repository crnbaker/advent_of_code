from typing import List


def load_calorie_file() -> str:
	with open('../inputs/day_1.txt', 'r') as f:
		return f.read()


def parse_calories(raw_string: str) -> List[List[int]]:
	elf_strings = [s for s in raw_string.strip().split('\n\n')]
	return [[int(v) for v in s.split('\n')] for s in elf_strings]


def calc_total_calories_per_elf(calories: List[List[int]]) -> List[int]:
	return [sum(elf) for elf in calories]


def find_top_three(values: List[int]) -> List[int]:
	return sorted(values)[-3:]


def main():
	calories_string = load_calorie_file()
	calories_each_elf = parse_calories(calories_string)
	total_calories_each_elf = calc_total_calories_per_elf(calories_each_elf)
	top_three_elves = find_top_three(total_calories_each_elf)
	print(f'The elf with the most calories has {max(total_calories_each_elf)} calories')
	print(f'The top three elves have {sum(top_three_elves)} calories altogether')


if __name__ == '__main__':
	main()
