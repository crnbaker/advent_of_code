#include <string>
#include <map>
#include "File.hpp"
#include "Directory.hpp"

std::unique_ptr<FileSystemObject> fileSystemObjectFactory(std::string line, Directory& currentDir);

enum OSCommand {
    LS,
    CD
};

Directory* getDirToChangeTo(std::string line, Directory* currentDir);
OSCommand parseCommand(std::string line);

bool lineIsCommand(std::string line) {
    return line.at(0) == '$';
};

class FileSystemScraper {
public:
    FileSystemScraper() {};
    ~FileSystemScraper() {};
    Directory* scrape();
private:
    void handleFileSystemObject(std::string line);
    void handleCommand(std::string line, OSCommand command);
    Directory topDirectory = Directory("/");
    Directory* currentDirectory = &topDirectory;
};