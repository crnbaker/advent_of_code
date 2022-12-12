from dataclasses import dataclass
from enum import Enum
from math import atan2, cos, degrees, floor, radians, sin
from typing import List, Set, Tuple


INPUT_FILE_PATH = "../inputs/day_9.txt"
ROPE_LENGTH = 1


class Direction(Enum):
    NORTH = 0
    NORTH_EAST = 45
    EAST = 90
    SOUTH_EAST = 135
    SOUTH = 180
    SOUTH_WEST = -45
    WEST = -90
    NORTH_WEST = -135


COMMAND_DIRECTIONS = {
    "U": Direction.NORTH,
    "R": Direction.EAST,
    "D": Direction.SOUTH,
    "L": Direction.WEST,
}


@dataclass
class Command:
    direction: Direction
    distance: int

    def __str__(self) -> str:
        return f"Move {self.direction.name} {self.distance}"


@dataclass
class Displacement:
    hor: int
    ver: int

    @property
    def distance(self) -> float:
        return (self.hor**2 + self.ver**2) ** 0.5

    @property
    def angle(self) -> float:
        return degrees(atan2(self.hor, self.ver))


@dataclass
class Position:
    hor: int
    ver: int

    def unit_move(self, direction: Direction):
        self.hor += round(sin(radians(direction.value)))
        self.ver += round(cos(radians(direction.value)))

    def __sub__(self, other: "Position") -> Displacement:
        return Displacement(hor=self.hor - other.hor, ver=self.ver - other.ver)

    def __str__(self) -> str:
        return f"({self.hor}, {self.ver})"


class Rope:
    def __init__(self, length: int = ROPE_LENGTH) -> None:
        self._length = length
        self._head = Position(0, 0)
        self._tail = Position(0, 0)
        self._head_log: Set[Tuple[int, int]] = set()
        self._tail_log: Set[Tuple[int, int]] = set()

    def move(self, command: Command) -> None:
        for _ in range(command.distance):
            self._head.unit_move(command.direction)
            self._update_tail()
            self._head_log.add((self._head.hor, self._head.ver))

    def _update_tail(self) -> None:
        displacement = self._head - self._tail
        if round(displacement.distance) > self._length:
            if (displacement.angle % 90) == 0:
                self._tail.unit_move(Direction(displacement.angle))
            else:
                self._tail.unit_move(
                    Direction(round_angle_to_nearest_diagonal(displacement.angle))
                )

        self._tail_log.add((self._tail.hor, self._tail.ver))

    @property
    def num_positions_tail_visited(self) -> int:
        return len(self._tail_log)

    def __str__(self) -> str:
        return f"Head: {self._head}, Tail: {self._tail}."


def round_angle_to_nearest_diagonal(angle: float) -> int:
    wrapped = (angle + 180) % 360
    rounded = floor(wrapped / 90) * 90 + 45
    return rounded - 180


def load_commands() -> List[Command]:
    commands = []
    with open(INPUT_FILE_PATH, "r") as f:
        for line in f.readlines():
            commands.append(
                Command(
                    direction=COMMAND_DIRECTIONS[line.split()[0]],
                    distance=int(line.split()[1]),
                )
            )
    return commands


if __name__ == "__main__":

    commands = load_commands()
    rope = Rope()

    for command in commands:
        rope.move(command)

    print(f"The tail visited {rope.num_positions_tail_visited} positions")
