#include <string>
#include <vector>

int getItemPriority(char item);

class Elf
{
public:
	Elf() : firstCompartment(""), secondCompartment("") {};
	Elf(std::string codedItems) :
		firstCompartment(decodeFirstCompartment(codedItems)),
		secondCompartment(decodeSecondCompartment(codedItems))
		{};
	~Elf() {};
	std::string getHeldItems();
	bool has(char item);
	char findDuplicatedItem();
private:
	std::string decodeFirstCompartment(std::string codedItems);
	std::string decodeSecondCompartment(std::string codedItems);
	std::string firstCompartment;
	std::string secondCompartment;
};

class ElfGroup
{
public:
	ElfGroup(Elf elves[3]) {
		for (int i = 0; i < 3; i++) {
    		this->elves[i] = elves[i];
    }
	};
	~ElfGroup() {};
	char findCommonItem();
	Elf elves[3];
};

std::vector<ElfGroup> groupElves();
