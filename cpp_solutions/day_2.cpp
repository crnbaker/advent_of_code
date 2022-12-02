#include "day_2.hpp"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cmath>

std::vector<Round> Game::loadRounds()
{
	std::ifstream file("../inputs/day_2.txt");
	std::string line;
	std::vector<Round> rounds;
	while (std::getline(file, line)) {
		if (isalpha(line[0])) {
			std::vector<std::string> coded_round;
			std::stringstream coded_line(line);
			std::string coded_play;
			while (std::getline(coded_line, coded_play, ' '))
			{
				coded_round.push_back(coded_play);
			};
			rounds.push_back(decodeRound(coded_round));
		}
	}
	return rounds;
};

int Game::play()
{
	std::vector<Round> rounds = loadRounds();
	int score = 0;
	for (Round & round : rounds) {
    	score += round.play();
	}
	return score;
}

Round Part1Game::decodeRound(std::vector<std::string> codedRound)
{
	Tool opponentPlay = opponentPlayCode[codedRound[0]];
	Tool myPlay = myPlayCode[codedRound[1]];
	Round round(opponentPlay, myPlay);
	return round;
};

Round Part2Game::decodeRound(std::vector<std::string> codedRound)
{
	Tool opponentPlay = opponentPlayCode[codedRound[0]];
	Outcome desiredOutcome = desiredOutcomeCode[codedRound[1]];
	int toolValue = (((opponentPlay - desiredOutcome) % 3) + 3) % 3;
	Tool myPlay = Tool(toolValue);
	Round round(opponentPlay, myPlay);
	return round;
};

int Round::play()
{
	int outcomeValue = (((opponentPlay - myPlay) % 3) + 3) % 3;
	Outcome outcome = Outcome(outcomeValue);
	return OUTCOME_SCORES[outcome] + TOOL_SCORES[myPlay];
}

int main()
{
	Part1Game game1;
	Part2Game game2;
	std::cout << "Game 1 result is " << game1.play() << std::endl;
	std::cout << "Game 2 result is " << game2.play() << std::endl;
}