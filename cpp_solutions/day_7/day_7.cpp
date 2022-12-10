#include <typeinfo>
#include <regex>
#include <iostream>
#include <memory>
#include <fstream>
#include <exception>
#include <algorithm>
#include "day_7.hpp"

#define INPUT_FILE_PATH "../../inputs/day_7.txt"

#define CHANGE_DIR_COMMAND "$ cd"
#define LIST_CONTENTS_COMMAND "$ ls"

#define DISK_SIZE 70000000
#define REQUIRED_SPACE 30000000

FileSystemObject::FileSystemObject(std::string name) : name(name) {};
FileSystemObject::FileSystemObject(
    std::string name, Directory* parent
    ) : name(name), parent(parent) {};

File::File(
    std::string name, int size, Directory* parent
    ) : FileSystemObject(name, parent), size(size) {};

Directory::Directory(std::string name) : FileSystemObject(name) {};
Directory::Directory(
    std::string name, Directory* parent
    ) : FileSystemObject(name, parent) {};

void Directory::addItem(std::unique_ptr<FileSystemObject> item) {
    contents[item->name] = std::move(item);
};

int Directory::getSize() {
    int totalSize = 0;
    for (auto const& [name, item] : contents) {
        totalSize += item->getSize();
    }
    return totalSize;
};

Directory* Directory::getSubDirectory(std::string name) {
    try {
        FileSystemObject* obj = contents.at(name).get();
        if (Directory* dir = dynamic_cast<Directory*>(obj)) {
            return dir;
        };
        throw std::runtime_error("No directory exists with that name.");
    } catch(std::out_of_range) {
        throw std::runtime_error("No item with that name exists in this directory.");
    };
}

std::unique_ptr<FileSystemObject> fileSystemObjectFactory(std::string line, Directory* currentDir) {
    std::regex dirRegex("dir \\w+"), fileRegex("\\d+ \\w+");
    std::smatch dirResult, fileResult;
    std::regex_search(line, dirResult, dirRegex);
    std::regex_search(line, fileResult, fileRegex);
    if (!dirResult.empty()) {
        std::string dirMatch = dirResult[0].str();
        std::string name = dirMatch.substr(4, dirMatch.size());
        return std::make_unique<Directory>(name, currentDir);
    } else if (!fileResult.empty()) {
        std::string dirMatch = fileResult[0].str();
        int delimiterIndex = dirMatch.find(" ");
        int size = stoi(dirMatch.substr(0, delimiterIndex));
        std::string name = dirMatch.substr(delimiterIndex + 1, dirMatch.size());
        return std::make_unique<File>(name, size, currentDir);
    } else {
        throw std::runtime_error("Line does not describe a file system object");
    };
}

Directory* getDirToChangeTo(std::string line, Directory* currentDir) {
    std::string dirCmd = CHANGE_DIR_COMMAND;
    std::string dirName = line.substr(dirCmd.size() + 1, line.size());
    if (dirName == "..") {
        if (currentDir->parent) {
            return currentDir->parent;
        };
        throw std::runtime_error("Directory has no parent");
    } else {
        return currentDir->getSubDirectory(dirName);
    };
}

OSCommand parseCommand(std::string line) {
    std::string dirCmd = CHANGE_DIR_COMMAND;
    std::string lsCmd = LIST_CONTENTS_COMMAND;
    if (line.substr(0, dirCmd.size()) == dirCmd) {
        return OSCommand::CD;
    } else if (line.substr(0, lsCmd.size()) == lsCmd) {
        return OSCommand::LS;
    } else {
        throw std::runtime_error("Provided line is not a valid command.");
    };
};

Directory* FileSystemScraper::scrape() {
    std::ifstream file(INPUT_FILE_PATH);
    std::string line;
    std::getline(file, line);
    while (std::getline(file, line)) {
        if (lineIsCommand(line)) {
            OSCommand command = parseCommand(line);
            handleCommand(line, command);
        } else {
            handleFileSystemObject(line);
        };
    };
    return &topDirectory;
};

void FileSystemScraper::handleFileSystemObject(std::string line) {
    currentDirectory->addItem(fileSystemObjectFactory(line, currentDirectory));
}

void FileSystemScraper::handleCommand(std::string line, OSCommand command) {

    if (command == OSCommand::CD) {
         currentDirectory = getDirToChangeTo(line, currentDirectory);
    } else if (command == OSCommand::LS) {
        // do nothing
    } else {
        throw std::runtime_error("Command not recognised.");
    };
}

std::vector<Directory*> Directory::recursivelyFindSubdirectories() {
    std::vector<Directory*> directories;
    directories.push_back(this);
    for (const auto & [name, item] : contents) {
        const FileSystemObject& objRef = *item;
        if (typeid(objRef) == typeid(Directory)) {
            Directory* dir = dynamic_cast<Directory*>(std::addressof(*item));
            std::vector<Directory*> subDirs = dir->recursivelyFindSubdirectories();
            directories.insert(directories.end(), subDirs.begin(), subDirs.end());
        };
    };
    return directories;
}

int main() {
    FileSystemScraper scraper;
    Directory* fileSystem = scraper.scrape();
    std::cout << "The whole file system has size " << fileSystem->getSize() << std::endl;
    std::vector<Directory*> directories = fileSystem->recursivelyFindSubdirectories();
    std::cout << "There are " << directories.size() << " directories" << std::endl;
    int totalSizeOfSmallDirs = 0;

    std::vector<int> sizes;
    for (Directory* dir : directories) {
        if (dir->getSize() <= 100000) {
            totalSizeOfSmallDirs += dir->getSize();
        }
        sizes.push_back(dir->getSize());
    }
    std::cout << "Total size of directories with size<=100000 is " << totalSizeOfSmallDirs << std::endl;

    int current_free_disk_space = DISK_SIZE - fileSystem->getSize();
    int extra_space_required = REQUIRED_SPACE - current_free_disk_space;

    std::sort(sizes.begin(), sizes.end());
    int deletableDirSize;
    for (int size : sizes) {
        if (size >= extra_space_required) {
            deletableDirSize = size;
            break;
        };
    };

    std::cout << "We need " << extra_space_required << " of extra space" << std::endl;
    std::cout << "We can delete a directory that will provide " << deletableDirSize << " of extra space" << std::endl;
}

