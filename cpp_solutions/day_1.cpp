#include "day_1.hpp"
#include <iostream>
#include <fstream>
#include <ctype.h>

CalorieCounter::CalorieCounter() {}

std::vector<int> CalorieCounter::getCaloriesPerElf()
{
	int temp_total = 0;
	std::ifstream file("../inputs/day_1.txt");
	std::string line;
	std::vector<int> caloriesPerElf;
    while (std::getline(file, line))
    {
		if (isdigit(line[0])) {
			temp_total += stoi(line);
		} else {
			caloriesPerElf.push_back(temp_total);
			temp_total = 0;
		}
    }
	return caloriesPerElf;
};

int CalorieCounter::calcCaloriesInTopElf()
{
	return *std::max_element(caloriesPerElf.begin(), caloriesPerElf.end());
}

int CalorieCounter::calcCaloriesInTopThreeElves()
{
	std::sort(caloriesPerElf.begin(), caloriesPerElf.end());
	int numElves = caloriesPerElf.size();
	return caloriesPerElf[numElves - 3] + caloriesPerElf[numElves - 2] + caloriesPerElf[numElves - 1];
}

int main()
{
	CalorieCounter counter;
	int maxCals = counter.calcCaloriesInTopElf();
	std::cout << "Greediest elf has " << maxCals << " calories" << std::endl;
	int calsInTopThree = counter.calcCaloriesInTopThreeElves();
	std::cout << "Top 3 elves have " << calsInTopThree << " calories" << std::endl;
};