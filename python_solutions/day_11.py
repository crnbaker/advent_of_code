from functools import partial
from math import lcm
from operator import add, mul
from pathlib import Path
import re
from typing import Callable, List

INPUT_FILE_PATH = Path("../inputs/day_11.txt")
NUM_ROUNDS_PART_1 = 20
NUM_ROUNDS_PART_2 = 10000


class Monkey:
    def __init__(
        self,
        initial_items: List[int],
        operation: Callable[[int], int],
        worry_divisor: int,
        worry_modulus: int,
    ) -> None:

        self._items = initial_items
        self._operation: Callable[[int], int] = operation
        self._worry_divisor = worry_divisor
        self._worry_modulus = worry_modulus
        self._get_target_monkey: Callable[[int], "Monkey"] = lambda _: self

        self._num_items_inspected = 0

    def set_target_monkey_function(self, func: Callable[[int], "Monkey"]) -> None:
        self._get_target_monkey = func

    def throw(self):
        while self._items:
            item_worry = self._items.pop(0)
            item_worry = (
                self._operation(item_worry) // self._worry_divisor
            ) % self._worry_modulus
            self._get_target_monkey(item_worry).catch(item_worry)
            self._num_items_inspected += 1

    def catch(self, item: int):
        self._items.append(item)

    @property
    def num_items_inspected(self) -> int:
        return self._num_items_inspected


def extract_integer_after_keyword(command_string: str, keyword: str) -> int:
    regex = re.compile(keyword + r" \d+")
    return int(regex.findall(command_string)[0][len(keyword) :])


def monkey_factory(spec: str, worry_divisor: int, worry_modulus: int) -> Monkey:
    items = spec.splitlines()[1].split(":")[1].strip().split(", ")

    mult_matches = re.compile(r"\* \d+").findall(spec.splitlines()[2])
    add_matches = re.compile(r"\+ \d+").findall(spec.splitlines()[2])
    square_matches = re.compile(r"\* old").findall(spec.splitlines()[2])

    def square(value: int) -> int:
        return value**2

    if len(mult_matches) == 1:
        operation: Callable[[int], int] = partial(mul, int(mult_matches[0].split()[1]))
    elif len(add_matches) == 1:
        operation = partial(add, int(add_matches[0].split()[1]))
    elif len(square_matches) == 1:
        operation = square
    else:
        raise ValueError("Monkey's operation not recognised")

    return Monkey(
        initial_items=[int(i) for i in items],
        operation=operation,
        worry_divisor=worry_divisor,
        worry_modulus=worry_modulus,
    )


def target_monkey_function(
    if_divisible_by: int, then_monkey: Monkey, else_monkey: Monkey, worry_level: int
) -> Monkey:
    if (worry_level % if_divisible_by) == 0:
        return then_monkey
    else:
        return else_monkey


def extract_integer_after_keyphrase(spec: str, keyword: str) -> int:
    regex = re.compile(keyword + r" \d+")
    return int(regex.findall(spec)[0][len(keyword) :])


def target_monkey_function_factory(
    spec: str, monkeys: List[Monkey]
) -> Callable[[int], "Monkey"]:

    if_divisible_by = extract_integer_after_keyphrase(spec, "Test: divisible by")
    then_monkey_index = extract_integer_after_keyphrase(
        spec, "If true: throw to monkey"
    )
    else_monkey_index = extract_integer_after_keyphrase(
        spec, "If false: throw to monkey"
    )

    return partial(
        target_monkey_function,
        if_divisible_by,
        monkeys[then_monkey_index],
        monkeys[else_monkey_index],
    )


def load_monkeys(worry_divisor: int):
    with open(INPUT_FILE_PATH, "r") as f:
        monkey_specs = f.read().split("\n\n")

    divisor_tests = []
    for monkey_spec in monkey_specs:
        divisor_tests.append(
            extract_integer_after_keyphrase(monkey_spec, "Test: divisible by")
        )
    worry_modulus = lcm(*divisor_tests)

    monkeys = []
    for monkey_spec in monkey_specs:
        monkeys.append(
            monkey_factory(monkey_spec.strip(), worry_divisor, worry_modulus)
        )

    for monkey, spec in zip(monkeys, monkey_specs):
        monkey.set_target_monkey_function(
            target_monkey_function_factory(spec.strip(), monkeys)
        )

    return monkeys


if __name__ == "__main__":

    part_1_monkeys = load_monkeys(worry_divisor=3)
    part_2_monkeys = load_monkeys(worry_divisor=1)

    for n in range(NUM_ROUNDS_PART_1):
        for p1_monkey in part_1_monkeys:
            p1_monkey.throw()

    for n in range(NUM_ROUNDS_PART_2):
        for p2_monkey in part_2_monkeys:
            p2_monkey.throw()

    p1_num_inspections_per_monkey = []
    p2_num_inspections_per_monkey = []

    for (p1_monkey, p2_monkey) in zip(part_1_monkeys, part_2_monkeys):
        p1_num_inspections_per_monkey.append(p1_monkey.num_items_inspected)
        p2_num_inspections_per_monkey.append(p2_monkey.num_items_inspected)

    print(
        f"Part 1 monkey business: {sorted(p1_num_inspections_per_monkey)[-2] * sorted(p1_num_inspections_per_monkey)[-1]}"
    )
    print(
        f"Part 2 monkey business: {sorted(p2_num_inspections_per_monkey)[-2] * sorted(p2_num_inspections_per_monkey)[-1]}"
    )
