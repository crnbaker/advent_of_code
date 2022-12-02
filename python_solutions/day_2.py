
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class Tool(Enum):
	ROCK = 0
	PAPER = 1
	SCISSORS = 2


TOOL_SCORES = {
	Tool.ROCK: 1,
	Tool.PAPER: 2,
	Tool.SCISSORS: 3
}

class Outcome(Enum):
	DRAW = 0
	WIN = 1
	LOSE = 2

OUTCOME_SCORES = {
	Outcome.LOSE: 0,
	Outcome.DRAW: 3,
	Outcome.WIN: 6
}

OPPONENT_PLAY_CODE = {
	'A': Tool.ROCK,
	'B': Tool.PAPER,
	'C': Tool.SCISSORS
}

MY_PLAY_CODE = {
	'X': Tool.ROCK,
	'Y': Tool.PAPER,
	'Z': Tool.SCISSORS
}

@dataclass
class Round:
	opponent_play: Tool
	my_play: Tool

	def __str__(self) -> str:
		return f'{self.opponent_play} vs {self.my_play}'


def load_strategy() -> List[Round]:
	strategy = []
	with open('../inputs/day_2.txt', 'r') as f:
		for line in f.readlines():
			if line != '\n':
				coded_plays = line.split()[:2]
				strategy.append(Round(
					opponent_play=OPPONENT_PLAY_CODE[coded_plays[0]],
					my_play=MY_PLAY_CODE[coded_plays[1]]
					))
	return strategy


def play_round(round: Round) -> int:
	
	outcome = Outcome((round.my_play.value - round.opponent_play.value) % 3)
	return OUTCOME_SCORES[outcome] + TOOL_SCORES[round.my_play]


def main() -> None:
	strategy = load_strategy()
	score = 0

	print(f'Playing {len(strategy)} rounds...')
	for round in strategy:
		this_score = play_round(round)
		score += this_score
	print(f'My total score would be {score} points')


if __name__ == '__main__':
	main()
