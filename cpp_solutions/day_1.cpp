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


int main()
{
	CalorieCounter counter;
	int max_cals = counter.calcCaloriesInTopElf();
	std::cout << "Greediest elf has " << max_cals << " calories" << std::endl;
};