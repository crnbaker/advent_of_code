from pathlib import Path
from typing import Set

INPUT_FILE = Path("../inputs/day_4.txt")


def decode_elf_assignment(coded_set: str) -> Set[int]:
    start_stop = [int(s) for s in coded_set.split("-")]
    return set(range(start_stop[0], start_stop[1] + 1))


def does_one_assignment_contain_other(zone1: Set[int], zone2: Set[int]) -> bool:
    max_zone_length = max([len(zone1), len(zone2)])
    return len(zone1 | zone2) == max_zone_length


def do_assignments_overlap(zone1: Set[int], zone2: Set[int]) -> bool:
    return len(zone1 & zone2) > 0


def main() -> None:
    fully_contained_counter = 0
    overlap_counter = 0
    with open(INPUT_FILE, "r") as f:
        for line in f.readlines():

            elf_codes = line.split(",")[:2]
            first_elf_assignment = decode_elf_assignment(elf_codes[0])
            second_elf_assignment = decode_elf_assignment(elf_codes[1])

            if does_one_assignment_contain_other(
                first_elf_assignment, second_elf_assignment
            ):
                fully_contained_counter += 1

            if do_assignments_overlap(first_elf_assignment, second_elf_assignment):
                overlap_counter += 1

    print(f"There are {fully_contained_counter} fully contained section assignments.")
    print(f"There are {overlap_counter} overlapping section assignments")


if __name__ == "__main__":
    main()
