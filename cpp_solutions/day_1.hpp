#include <stdio.h>
#include <vector>

class CalorieCounter
{
public:
	CalorieCounter();
	~CalorieCounter() {};
	std::vector<int> getCaloriesPerElf();
	int calcCaloriesInTopElf();
	int calcCaloriesInTopThreeElves();
private:
	int calcSum(std::vector<int>);
	int findMax(std::vector<int>);
};