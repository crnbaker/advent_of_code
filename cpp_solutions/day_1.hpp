#include <stdio.h>
#include <vector>

class CalorieCounter
{
public:
	CalorieCounter();
	~CalorieCounter() {};
	int calcCaloriesInTopElf();
	int calcCaloriesInTopThreeElves();
private:
	std::vector<int> getCaloriesPerElf();
	std::vector<int> caloriesPerElf = getCaloriesPerElf();

};