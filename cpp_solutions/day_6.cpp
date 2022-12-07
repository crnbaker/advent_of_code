#include <string>
#include <fstream>
#include <set>
#include <exception>
#include <iostream>

#define INPUT_FILE_PATH "../inputs/day_6.txt"

std::string getSignal() {
    std::ifstream file(INPUT_FILE_PATH);
    std::string line;
    std::getline(file, line);
    return line;
}

int searchForMarker(std::string signal, int markerSize) {
    int remainder = ((signal.length() % markerSize) + markerSize) % markerSize;
    for (int i = 0; i < (signal.length() - remainder - markerSize); i++) {
        std::set<char> chunk;
        for (int j = 0; j < markerSize; j++) {
            chunk.insert(signal.at(i + j));
        }
        if (chunk.size() == markerSize) {
            return i + (markerSize - 1);
        }
    }
    throw std::runtime_error("No marker found");
}

int main() {
    std::string signal = getSignal();
    int part1 = searchForMarker(signal, 4);
    int part2 = searchForMarker(signal, 14);
    std::cout << "Packet received at character " << part1 + 1 << std::endl;
    std::cout << "Message received at character " << part2  + 1 << std::endl;
}