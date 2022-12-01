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
			line.erase(line.length() - 1);
			// std::cout << line;
			temp_total += stoi(line);
		} else {
			caloriesPerElf.push_back(temp_total);
			temp_total = 0;
		}
    }
	return caloriesPerElf;
};


int main()
{
	CalorieCounter counter;
	std::vector<int> values = counter.getCaloriesPerElf();
	std::cout << "Counting calories...." << std::endl;
	for (int value : values)
	{
		std::cout << value << std::endl;
	}
	std::cout << "... Finished!.";
};