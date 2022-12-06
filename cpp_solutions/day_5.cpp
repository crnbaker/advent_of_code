#include "day_5.hpp"
#include <fstream>
#include <regex>
#include <iostream>

#define INPUT_FILE_PATH "../inputs/day_5.txt"

#define CHARS_PER_CRATE 4
#define PROCEDURE_START_LINE 10

#define NUM_CRATES_KEYWORD "move"
#define SOURCE_STACK_KEYWORD "from"
#define DEST_STACK_KEYWORD "to"


std::vector<std::stack<char>> decodeStacks()
{
    std::ifstream file(INPUT_FILE_PATH);
    std::string line;
    std::stack<char> stack;
    std::vector<std::string> lines;
    std::vector<std::stack<char>> stacks(NUM_STACKS, stack);

    int lineIndex = 0;
    while (std::getline(file, line) && (lineIndex < (PROCEDURE_START_LINE - 1))) {
        lines.push_back(line);
        lineIndex++;
    }
    for (int j = lines.size() - 1; j >= 0; j--) {
        for (int i = 0; i < NUM_STACKS; i++) {
            char crate = lines[j].at(i * CHARS_PER_CRATE + 1);
            if (isalpha(crate)) {
                stacks[i].push(crate);
            };
        };
    };
    return stacks;
};

std::vector<CraneCommand> getCraneCommands()
{
    std::ifstream file(INPUT_FILE_PATH);
    std::string line;
    int lineIndex = 0;

    std::vector<CraneCommand> commands;

    while (std::getline(file, line)) {
        if (lineIndex >= PROCEDURE_START_LINE) {
            commands.push_back(parseCraneCommand(line));
        };
        lineIndex++;
    };
    return commands;
};

CraneCommand parseCraneCommand(std::string command) {
    int numCrates = extractIntAfterKeyword(command, NUM_CRATES_KEYWORD);
    int source = extractIntAfterKeyword(command, SOURCE_STACK_KEYWORD);
    int dest = extractIntAfterKeyword(command, DEST_STACK_KEYWORD);
    return CraneCommand{numCrates, source - 1, dest - 1};
};

int extractIntAfterKeyword(std::string commandString, std::string keyword) {
    std::regex keywordRegex(keyword + " \\d+");
    std::smatch regexResult;
    std::regex_search(commandString, regexResult, keywordRegex);
    std::string match = regexResult[0].str();
    return stoi(match.substr(keyword.size() + 1, match.size()));
};

std::string Crane::getTopCrates()
{
    std::string topCrates;
    for (int i = 0; i < NUM_STACKS; i++) {
        topCrates += stacks[i].top();
    }
    return topCrates;
}

void CrateMover9000::executeCommand(CraneCommand command)
{
    int moveCount = 0;
    while (moveCount < command.numCratesToMove) {
        stacks[command.destinationStack].push(stacks[command.sourceStack].top());
        stacks[command.sourceStack].pop();
        moveCount++;
    }
}

void CrateMover9001::executeCommand(CraneCommand command)
{
    std::stack<char> pickedUpCrates;
    for (int i = 0; i < command.numCratesToMove; i++) {
        pickedUpCrates.push(stacks[command.sourceStack].top());
        stacks[command.sourceStack].pop();
    }
    for (int i = 0; i < command.numCratesToMove; i++) {
        stacks[command.destinationStack].push(pickedUpCrates.top());
        pickedUpCrates.pop();
    }
}

int main()
{
    std::vector<std::stack<char>> stacksPart1 = decodeStacks();
    std::vector<std::stack<char>> stacksPart2 = decodeStacks();

    CrateMover9000 cranePart1(stacksPart1);
    CrateMover9001 cranePart2(stacksPart2);

    std::vector<CraneCommand> commands = getCraneCommands();

    for (CraneCommand command : commands) {
        cranePart1.executeCommand(command);
        cranePart2.executeCommand(command);

    }
    std::cout << "CrateMover9000 top crates: " << cranePart1.getTopCrates() << std::endl;
    std::cout << "CrateMover9001 top crates: " << cranePart2.getTopCrates() << std::endl;
};