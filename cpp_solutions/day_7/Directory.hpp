#include <string>
#include <map>
#include "FileSystemObject.hpp"

class Directory : public FileSystemObject {
public:
    Directory(std::string name);
    Directory(std::string name, Directory* parent);
    void addItem(std::unique_ptr<FileSystemObject> item);
    Directory* getSubDirectory(std::string name);
    int getSize() override;
    std::vector<Directory*> recursivelyFindSubdirectories();
private:
    std::map<std::string, std::unique_ptr<FileSystemObject>> contents;
};