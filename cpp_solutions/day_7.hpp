#include <string>
#include <map>
#include <optional>

class FileSystemObject {
public:
    FileSystemObject(std::string name, std::optional<Directory&> parent);
    ~FileSystemObject() {};
    std::string name;
    Directory& parent;
    virtual int getSize() = 0;
};

class File : public FileSystemObject {
public:
    File(std::string name, int size, std::optional<Directory&> parent) : FileSystemObject(name, parent), size(size) {};
    int getSize() override {return size;};
private:
    int size;
};

class Directory : public FileSystemObject {
public:
    Directory(std::string name, std::optional<Directory&> parent) : FileSystemObject(name, parent) {};
    void addItem(FileSystemObject& item);
    Directory getSubDirectory(std::string name);
    int getSize() override {
        int totalSize = 0;
        for (auto const& [name, item] : contents) {
            totalSize += item.getSize();
        }
        return totalSize;
    };
private:
    std::map<std::string, FileSystemObject&> contents;
};

FileSystemObject& fileSystemObjectFactory(std::string line, Directory& currentDir);

struct OSCommand {};
struct ListCommand : OSCommand {};
struct ChangeDirectoryCommand : OSCommand {Directory& destination;};
OSCommand commandFactory(std::string line, std::optional<Directory&> currentDir);

class FileSystemScraper {
public:
    FileSystemScraper() {};
    ~FileSystemScraper() {};
    Directory& scrape();
private:
    void handleFileSystemObject(std::string line);
    void handleCommand(ListCommand command);
    void handleCommand(ChangeDirectoryCommand command);
    std::optional<Directory&> topDirectory;
    std::optional<Directory&> currentDirectory;
};