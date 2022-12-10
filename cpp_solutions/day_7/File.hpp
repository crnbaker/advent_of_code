#include <string>
#include "FileSystemObject.hpp"

class File : public FileSystemObject {
public:
    File(std::string name, int size, Directory* parent);
    int getSize() override {return size;};
private:
    int size;
};