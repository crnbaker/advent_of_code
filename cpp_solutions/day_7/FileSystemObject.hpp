#include <string>

#pragma once

// This is a "forward decleration".
// It tells the compiler that class Directory exists without having to
// load Directory.hpp (which would be recursive).
class Directory;

class FileSystemObject {
public:
    FileSystemObject(std::string name);
    FileSystemObject(std::string name, Directory* parent);
    virtual ~FileSystemObject() = default;
    std::string name;
    Directory* parent;
    virtual int getSize() = 0;
};
