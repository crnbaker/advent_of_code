#include "day_3.hpp"
#include <cctype>
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <functional>

int getItemPriority(char item)
{
    int asciiCode = (int)item;
    int firstLowerCode = (int)'a';
    int firstCapitalCode = (int)'A';

    if (isupper(item)) {
        return asciiCode - firstCapitalCode + 27;
    } else {
        return asciiCode - firstLowerCode + 1;
    };
}

std::string Elf::getHeldItems()
{
    return firstCompartment + secondCompartment;
}

bool Elf::has(char item)
{
    return (getHeldItems().find(item) != std::string::npos);
}

char Elf::findDuplicatedItem()
{
    for (int i = 0; i < firstCompartment.length(); i++) {
        char item = firstCompartment.at(i);
        if (secondCompartment.find(item) != std::string::npos) {
                return item;
            }
      }
    throw std::runtime_error("Cannot find duplicated item");
}

std::string Elf::decodeFirstCompartment(std::string codedItems)
{
    return codedItems.substr(0, codedItems.length() / 2);
}

std::string Elf::decodeSecondCompartment(std::string codedItems)
{
    return codedItems.substr(codedItems.length() / 2, codedItems.length() / 2);
}

char ElfGroup::findCommonItem()
{
    int numHeldItems = elves[0].getHeldItems().length();
    if (numHeldItems == 0) {throw std::runtime_error("All elves should have some items.");};
    try {
        for (int i = 0; i < elves[0].getHeldItems().length(); i++) {
            char item = elves[0].getHeldItems().at(i);
            if (elves[1].has(item) and elves[2].has(item)) {
                return item;
            }
        }
    } catch (const std::out_of_range&) {
        std::cout << "OUT OF RANGE ERROR!!!!!!!!!" << std::endl;
        std::cout << elves[0].getHeldItems() << std::endl;
    };
    throw std::runtime_error("Cannot find common item");

}

std::vector<ElfGroup> groupElves()
{
    std::ifstream file("../inputs/day_3.txt");
    std::vector<ElfGroup> elfGroups;

    while (true) {
        std::string lines[3];
        std::getline(file, lines[0]);
        std::getline(file, lines[1]);
        if (std::getline(file, lines[2])) {
            Elf elves[3] = {
                {std::ref(lines[0])},
                {std::ref(lines[1])},
                {std::ref(lines[2])}
            };
            ElfGroup elfGroup(elves);
            elfGroups.push_back(elfGroup);
        } else {
            break;
        }
    }

    return elfGroups;
}

int main()
{
    int duplicatedItemsTotal = 0;
    int commonItemsTotal = 0;

    std::vector<ElfGroup> elfGroups = groupElves();
    
    for (ElfGroup & elfGroup : elfGroups) {
        commonItemsTotal += getItemPriority(elfGroup.findCommonItem());
        for (int i = 0; i < 3; i++) {
            duplicatedItemsTotal += getItemPriority(
                elfGroup.elves[i].findDuplicatedItem()
                );
        }
    }

    std::cout << "Total priorities of duplicated items: " << duplicatedItemsTotal << std::endl;
    std::cout << "Total priorities of common items: " << commonItemsTotal << std::endl;
}