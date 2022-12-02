#include <map>
#include <vector>
#include <string>

enum Tool {
    ROCK,
    PAPER,
    SCISSORS
};

enum Outcome {
    DRAW,
    LOSE,
    WIN
};

std::map<Tool, int> TOOL_SCORES = {
    {Tool::ROCK, 1},
    {Tool::PAPER, 2},
    {Tool::SCISSORS, 3}
};

std::map<Outcome, int> OUTCOME_SCORES = {
    {Outcome::LOSE, 0},
    {Outcome::DRAW, 3},
    {Outcome::WIN, 6}
};

class Round
{
public:
    Round(Tool opponentPlay, Tool myPlay)
        : opponentPlay(opponentPlay), myPlay(myPlay) {};
    ~Round() {};
    int play();
    Tool opponentPlay;
    Tool myPlay;
};

class Game
{
public:
    Game() {};
    ~Game() {};
    int play();
    std::map<std::string, Tool> opponentPlayCode = {
        {"A", Tool::ROCK},
        {"B", Tool::PAPER},
        {"C", Tool::SCISSORS}
    };

private:
    std::vector<Round> loadRounds();
    virtual Round decodeRound(std::vector<std::string> codedRound) = 0;
};

class Part1Game: public Game
{
private:
    Round decodeRound(std::vector<std::string> coded_round) override;
    std::map<std::string, Tool> myPlayCode = {
        {"X", Tool::ROCK},
        {"Y", Tool::PAPER},
        {"Z", Tool::SCISSORS}
    };
};

class Part2Game: public Game
{
private:
    Round decodeRound(std::vector<std::string> coded_round) override;
    std::map<std::string, Outcome> desiredOutcomeCode = {
        {"X", Outcome::LOSE},
        {"Y", Outcome::DRAW},
        {"Z", Outcome::WIN}
    };
};