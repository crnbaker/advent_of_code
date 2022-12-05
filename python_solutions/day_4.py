

if __name__ == '__main__':

	overlap_counter = 0
	with open("../inputs/day_4.txt", "r") as f:
		for line in f.readlines():
			elf_codes = line.split(',')[:2]

			first_elf_start_stop = [int(s) for s in elf_codes[0].split('-')]
			first_elf_start = first_elf_start_stop[0]
			first_elf_stop = first_elf_start_stop[1]

			second_elf_start_stop = [int(s) for s in elf_codes[1].split('-')]
			second_elf_start = second_elf_start_stop[0]
			second_elf_stop = second_elf_start_stop[1]

			first_elf_zones = set(range(first_elf_start, first_elf_stop + 1))
			second_elf_zones = set(range(second_elf_start, second_elf_stop + 1))

			max_zone_length = max([len(first_elf_zones), len(second_elf_zones)])

			if len(first_elf_zones | second_elf_zones) == max_zone_length:
				overlap_counter += 1

	print(f'There are {overlap_counter} overlaps')
			