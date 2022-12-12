from dataclasses import dataclass
from typing import List

INPUT_FILE_PATH = "../inputs/day_10.txt"


@dataclass
class Command:
    duration: int
    value: int


def parse_command(line: str) -> Command:
    match line.split()[0]:
        case "noop":
            return Command(duration=1, value=0)
        case "addx":
            return Command(duration=2, value=int(line.split()[1]))
        case _:
            raise ValueError("Unrecognised command.")


class SignalStrengthLogger:
    def __init__(self, start_cycle: int, log_period: int) -> None:
        self._start_cycle = start_cycle
        self._log_period = log_period
        self._strength_log: List[int] = []

    def log(self, clock_cycle: int, register_value: int) -> None:
        if ((clock_cycle - self._start_cycle) % self._log_period) == 0:
            self._strength_log.append(clock_cycle * register_value)

    @property
    def strength_log(self) -> List[int]:
        return self._strength_log


class CRT:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._draw_pos = 0
        self._pixels: List[str] = ["."] * (width * height)

    def draw(self, sprite_pos: int) -> None:
        if (self._draw_pos % self._width) in [
            sprite_pos - 1,
            sprite_pos,
            sprite_pos + 1,
        ]:
            self._pixels[self._draw_pos] = "#"
        self._draw_pos += 1

    def render(self) -> str:
        image = ""
        for row in range(self._height):
            image += (
                "".join(self._pixels[row * self._width : (row + 1) * self._width])
                + "\n"
            )
        return image


class CPU:
    def __init__(self, crt: CRT, logger: SignalStrengthLogger) -> None:
        self._clock = 0
        self._register = 1
        self._crt = crt
        self._logger = logger

    def handle_command(self, command: Command) -> None:
        for _ in range(command.duration):
            self._tick()
        self._register += command.value

    def _tick(self) -> None:
        self._clock += 1
        self._logger.log(self._clock, self._register)
        self._crt.draw(self._register)

    @property
    def clock(self) -> int:
        return self._clock

    @property
    def register(self) -> int:
        return self._register

    def render_crt(self) -> str:
        return self._crt.render()


def main() -> None:

    crt = CRT(40, 6)
    logger = SignalStrengthLogger(start_cycle=20, log_period=40)
    cpu = CPU(crt, logger)

    with open(INPUT_FILE_PATH, "r") as f:
        for line in f.readlines():
            command = parse_command(line)
            cpu.handle_command(command)

    print(logger.strength_log)
    print(f"Sum of strengths: {sum(logger.strength_log)}")

    print(cpu.render_crt())


if __name__ == "__main__":
    main()
