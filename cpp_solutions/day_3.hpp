#include <string>
#include <vector>

int getItemPriority(char item);

class Elf
{
public:
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
	ElfGroup(Elf* elves) : elves(elves) {};
	~ElfGroup() {};
	char findCommonItem() {};
	Elf* elves;
};

std::vector<ElfGroup> groupElves();
