#include "day_4.hpp"
#include <algorithm>
#include <fstream>
#include <iostream>


std::set<int> decodeAssignment(std::string coded)
{
    std::string delimiter = "-";
    std::string start = coded.substr(0, coded.find(delimiter));
    std::string stop = coded.substr(coded.find(delimiter) + 1, coded.length());

    std::set<int> assignment;
    for (int i = stoi(start); i <= stoi(stop); i++) {
        assignment.insert(i);
    };

    return assignment;
}

bool doesOneContainOther(std::set<int> assignment1, std::set<int> assignment2)
{
    int max_length = std::max(assignment1.size(), assignment2.size());

    std::set<int> result;
    std::set_union(
        assignment1.begin(), assignment1.end(),
        assignment2.begin(), assignment2.end(),
        std::inserter(result, result.begin())
        );

    return (result.size() == max_length);
}

bool doOverlap(std::set<int> assignment1, std::set<int> assignment2) {
    std::set<int> result;
    std::set_intersection(
        assignment1.begin(), assignment1.end(),
        assignment2.begin(), assignment2.end(),
        std::inserter(result, result.begin())
        );
    return (result.size() > 0);
}

int main()
{
    std::ifstream file("../inputs/day_4.txt");
    std::string line;

    int fully_contained_counter = 0;
    int overlap_counter = 0;

    while (std::getline(file, line)) {
        std::string delimiter = ",";
        std::set<int> firstAssignment = decodeAssignment(
            line.substr(0, line.find(delimiter))
            );
        std::set<int> secondAssignment = decodeAssignment(
            line.substr(line.find(delimiter) + 1, line.length())
            );

        if (doesOneContainOther(firstAssignment, secondAssignment)
            ) {
            fully_contained_counter++;
        }

        if (doOverlap(firstAssignment, secondAssignment)
            ) {
            overlap_counter++;
        }
    }

    std::cout << "There are " << fully_contained_counter << " fully contained assignments." << std::endl;
    std::cout << "There are " << overlap_counter << " overlapping assignments." << std::endl;

}
