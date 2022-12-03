from itertools import islice
from typing import List, Tuple


def get_item_priority(item: str) -> int:
    item_ascii_code = ord(item)
    if item.upper() == item:
        return item_ascii_code - ord("A") + 27
    else:
        return item_ascii_code - ord("a") + 1


class Elf:
    def __init__(self, coded_line: str) -> None:
        self._first_compartment_contents = coded_line[: len(coded_line) // 2]
        self._second_compartment_contents = coded_line[len(coded_line) // 2 :]

    @property
    def held_items(self) -> str:
        return self._first_compartment_contents + self._second_compartment_contents

    def has(self, item: str) -> bool:
        return item in self.held_items

    def find_duplicated_item(self) -> str:
        for item in self._first_compartment_contents:
            if item in self._second_compartment_contents:
                return item
        raise IOError("No dubplicated item found")


class ElfGroup:
    def __init__(self, elves: Tuple[Elf, Elf, Elf]) -> None:
        self._elves = elves

    @property
    def elves(self) -> Tuple[Elf, Elf, Elf]:
        return self._elves

    def find_common_item(self) -> str:
        for item in self._elves[0].held_items:
            if self._elves[1].has(item) and self._elves[2].has(item):
                return item
        raise IOError("No common item found")


def group_elves() -> List[ElfGroup]:
    with open("../inputs/day_3.txt", "r") as f:
        elf_groups = []
        next_3_lines = list(islice(f, 3))
        while next_3_lines:
            elf_groups.append(
                ElfGroup(
                    (Elf(next_3_lines[0]), Elf(next_3_lines[1]), Elf(next_3_lines[2]))
                )
            )
            next_3_lines = list(islice(f, 3))
        return elf_groups


if __name__ == "__main__":

    duplicated_items_total = 0
    common_items_total = 0

    elf_groups = group_elves()
    for elf_group in elf_groups:
        common_items_total += get_item_priority(elf_group.find_common_item())
        for elf in elf_group.elves:
            duplicated_items_total += get_item_priority(elf.find_duplicated_item())

    print(f"Total priorities of duplicated items: {duplicated_items_total}")
    print(f"Total priorities of common items: {common_items_total}")
