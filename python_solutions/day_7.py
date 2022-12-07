from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatchmethod
from pathlib import Path
import re
from typing import Dict, List, Optional

INPUT_FILE_PATH = Path("../inputs/day_7.txt")
CHANGE_DIR_COMMAND = "$ cd"
LIST_CONTENTS_COMMAND = "$ ls"

DISK_SIZE = 70000000
REQUIRED_SPACE = 30000000


class FileSystemObject(ABC):
    def __init__(self, name: str, parent: Optional["Directory"] = None) -> None:
        self._name = name
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Optional["Directory"]:
        return self._parent

    @property
    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError()


class File(FileSystemObject):
    def __init__(
        self, name: str, size: int, parent: Optional["Directory"] = None
    ) -> None:
        super().__init__(name, parent)
        self._size = size

    @property
    def size(self) -> int:
        return self._size


class Directory(FileSystemObject):
    def __init__(self, name: str, parent: Optional["Directory"] = None) -> None:
        super().__init__(name, parent)
        self._contents: Dict[str, FileSystemObject] = {}

    def add_item(self, item: FileSystemObject) -> None:
        self._contents[item.name] = item

    @property
    def contents(self) -> Dict[str, FileSystemObject]:
        return self._contents

    def get_subdirectory(self, name: str) -> "Directory":
        item = self._contents[name]
        if isinstance(item, Directory):
            return item
        else:
            raise ValueError(f"No directory names {name} exists in this directory.")

    @property
    def size(self) -> int:
        return sum([obj.size for obj in self._contents.values()])


def file_system_object_factory(line: str, current_dir: Directory) -> FileSystemObject:
    dir_regex = re.compile(r"dir \w+")
    file_regex = re.compile(r"\d+ \w+")
    if dir_regex.match(line):
        return Directory(name=line[4:], parent=current_dir)
    elif file_regex.match(line):
        return File(name=line.split()[1], size=int(line.split()[0]), parent=current_dir)
    else:
        raise ValueError("Line does not describe a file system object.")


@dataclass
class OSCommand:
    pass


@dataclass
class ListCommand(OSCommand):
    pass


@dataclass
class ChangeDirectoryCommand(OSCommand):
    destination: Directory


class UnrecognisedCommandError(ValueError):
    pass


class CurrentDirectoryNotSetError(RuntimeError):
    pass


class DirectoryHasNoParentError(RuntimeError):
    pass


class ScapingFailedError(RuntimeError):
    pass


def command_factory(line: str, current_dir: Optional[Directory] = None) -> OSCommand:
    if line[: len(CHANGE_DIR_COMMAND)] == CHANGE_DIR_COMMAND:
        dir_name = line[len(CHANGE_DIR_COMMAND) + 1 :]
        if current_dir is None:
            destination = Directory(name=dir_name)
        elif dir_name == "..":
            if current_dir.parent is not None:
                destination = current_dir.parent
            else:
                raise DirectoryHasNoParentError()
        else:
            destination = current_dir.get_subdirectory(dir_name)
        return ChangeDirectoryCommand(destination=destination)
    elif line == LIST_CONTENTS_COMMAND:
        return ListCommand()
    else:
        raise UnrecognisedCommandError()


class FileSystemScraper:
    def __init__(self) -> None:
        self._top_dir: Optional[Directory] = None
        self._current_dir: Optional[Directory] = None

    def scrape(self) -> Directory:
        with open(INPUT_FILE_PATH, "r") as f:
            for line in f.readlines():
                line = line.strip()
                try:
                    command = command_factory(line, self._current_dir)
                    self._handle_command(command)
                except UnrecognisedCommandError:
                    self._handle_file_system_object(line)
        if self._top_dir is not None:
            return self._top_dir
        else:
            raise ScapingFailedError()

    def _handle_file_system_object(self, line: str):
        if self._current_dir is not None:
            self._current_dir.add_item(
                file_system_object_factory(line, self._current_dir)
            )
        else:
            raise CurrentDirectoryNotSetError()

    @singledispatchmethod
    def _handle_command(self, command: OSCommand) -> None:
        raise NotImplementedError()

    @_handle_command.register
    def _(self, command: ChangeDirectoryCommand) -> None:
        if self._top_dir is None:
            self._top_dir = command.destination
        self._current_dir = command.destination

    @_handle_command.register
    def _(self, command: ListCommand) -> None:
        pass


def find_subdirectories(dir: Directory) -> List[Directory]:
    dirs = [dir]
    for item in dir.contents.values():
        if isinstance(item, Directory):
            dirs += find_subdirectories(item)
    return dirs


if __name__ == "__main__":

    scraper = FileSystemScraper()
    top_dir = scraper.scrape()
    print(f"Total file system size: {top_dir.size}")

    dirs = find_subdirectories(top_dir)
    print(f"There are {len(dirs)} directories")

    dir_sizes = [dir.size for dir in dirs]
    small_dirs = [s for s in dir_sizes if s <= 100000]
    print(f"Total size of directories with size <= 100000 is {sum(small_dirs)}")

    current_free_disk_space = DISK_SIZE - top_dir.size
    extra_space_required = REQUIRED_SPACE - current_free_disk_space

    sorted_dir_sizes = sorted(dir_sizes)
    for dir_size in sorted_dir_sizes:
        if dir_size >= extra_space_required:
            break

    print(f"We need {extra_space_required} of extra space.")
    print(f"We can delete a directory that wil provide {dir_size} of extra space.")
