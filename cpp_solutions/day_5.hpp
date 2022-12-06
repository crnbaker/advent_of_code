#include<stack>
#include<string>
#include<vector>

#define NUM_STACKS 9

struct CraneCommand {
    int numCratesToMove;
    int sourceStack;
    int destinationStack;
};

class Crane {
public:
    Crane(std::vector<std::stack<char>> stacks) {
        for (int i = 0; i < NUM_STACKS; i++) {
            this->stacks[i] = stacks[i];
        };
    };
    ~Crane() {};
    virtual void executeCommand(CraneCommand command) = 0;
    std::string getTopCrates();
protected:
    std::stack<char> stacks[NUM_STACKS];
};

class CrateMover9000 : public Crane {
public:
    CrateMover9000(std::vector<std::stack<char>> stacks) : Crane(stacks) {};
    void executeCommand(CraneCommand command) override;
};

class CrateMover9001 : public Crane {
public:
    CrateMover9001(std::vector<std::stack<char>> stacks) : Crane(stacks) {};
    void executeCommand(CraneCommand command) override;
};

std::vector<std::stack<char>> decodeStacks();
std::vector<CraneCommand> getCraneCommands();

int extractIntAfterKeyword(std::string commandString, std::string keyword);

CraneCommand parseCraneCommand(std::string commandString);
