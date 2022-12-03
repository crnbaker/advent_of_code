from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple


class Tool(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


TOOL_SCORES = {Tool.ROCK: 1, Tool.PAPER: 2, Tool.SCISSORS: 3}


class Outcome(Enum):
    DRAW = 0
    LOSE = 1
    WIN = 2


OUTCOME_SCORES = {Outcome.LOSE: 0, Outcome.DRAW: 3, Outcome.WIN: 6}

OPPONENT_PLAY_CODE = {"A": Tool.ROCK, "B": Tool.PAPER, "C": Tool.SCISSORS}

MY_PLAY_CODE_PART_1 = {"X": Tool.ROCK, "Y": Tool.PAPER, "Z": Tool.SCISSORS}

MY_PLAY_CODE_PART_2 = {"X": Outcome.LOSE, "Y": Outcome.DRAW, "Z": Outcome.WIN}


@dataclass
class Round:
    opponent_play: Tool
    my_play: Tool

    def __str__(self) -> str:
        return f"{self.opponent_play} vs {self.my_play} ({self.play()})"

    def play(self) -> int:
        outcome = Outcome((self.opponent_play.value - self.my_play.value) % 3)
        return OUTCOME_SCORES[outcome] + TOOL_SCORES[self.my_play]


class Game(ABC):
    def __init__(self) -> None:
        self.rounds = self._load_rounds()

    def _load_rounds(self) -> List[Round]:
        rounds = []
        with open("../inputs/day_2.txt", "r") as f:
            for line in f.readlines():
                if line != "\n":
                    coded_round = (line.split()[0], line.split()[1])
                    rounds.append(self._decode_round(coded_round))
        return rounds

    @staticmethod
    @abstractmethod
    def _decode_round(coded_round: Tuple[str, str]) -> Round:
        raise NotImplementedError()

    def play(self) -> int:
        score = 0
        for round in self.rounds:
            score += round.play()
        return score


class Part1Game(Game):
    @staticmethod
    def _decode_round(coded_round: Tuple[str, str]) -> Round:
        return Round(
            opponent_play=OPPONENT_PLAY_CODE[coded_round[0]],
            my_play=MY_PLAY_CODE_PART_1[coded_round[1]],
        )


class Part2Game(Game):
    @staticmethod
    def _decode_round(coded_round: Tuple[str, str]) -> Round:
        opponent_play = OPPONENT_PLAY_CODE[coded_round[0]]
        desired_outcome = MY_PLAY_CODE_PART_2[coded_round[1]]
        my_play = Tool((opponent_play.value - desired_outcome.value) % 3)
        return Round(opponent_play=opponent_play, my_play=my_play)


def main() -> None:

    game1 = Part1Game()
    game2 = Part2Game()
    print(f"My total score in game 1 would be {game1.play()} points")
    print(f"My total score in game 2 would be {game2.play()} points")


if __name__ == "__main__":
    main()
