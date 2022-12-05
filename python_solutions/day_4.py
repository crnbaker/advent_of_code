from typing import Set


def decode_elf_set(coded_set: str) -> Set[int]:
    start_stop = [int(s) for s in coded_set.split("-")]
    return set(range(start_stop[0], start_stop[1] + 1))


if __name__ == "__main__":

    fully_contained_counter = 0
    overlap_counter = 0

    with open("../inputs/day_4.txt", "r") as f:
        for line in f.readlines():
            elf_codes = line.split(",")[:2]

            first_elf_zones = decode_elf_set(elf_codes[0])
            second_elf_zones = decode_elf_set(elf_codes[1])

            max_zone_length = max([len(first_elf_zones), len(second_elf_zones)])

            if len(first_elf_zones | second_elf_zones) == max_zone_length:
                fully_contained_counter += 1

            if len(first_elf_zones & second_elf_zones):
                overlap_counter += 1

    print(f"There are {fully_contained_counter} fully contained section assignments.")
    print(f"There are {overlap_counter} overlapping section assignments")
