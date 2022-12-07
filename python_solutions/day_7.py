
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional

class FileSystemObject(ABC):

	def __init__(self, name: str, parent: Optional['Directory'] = None) -> None:
		self._name = name
		self._parent = parent

	@property
	def name(self) -> str:
		return self._name

	@property
	def parent(self) -> Optional['Directory']:
		return self._parent

	@property
	@abstractmethod
	def size(self) -> int:
		raise NotImplementedError()


class File(FileSystemObject):
	def __init__(self, name: str, size: int, parent: Optional['Directory'] = None) -> None:
		super().__init__(name, parent)
		self._size = size

	@property
	def size(self) -> int:
		return self._size


class Directory(FileSystemObject):
	def __init__(self, name: str, parent: Optional['Directory'] = None) -> None:
		super().__init__(name, parent)
		self._contents: Dict[str, FileSystemObject] = {}

	def add_item(self, item: FileSystemObject) -> None:
		self._contents[item.name] = item

	@property
	def contents(self) -> Dict[str, FileSystemObject]:
		return self._contents

	def get_subdirectory(self, name: str) -> 'Directory':
		if isinstance(self._contents[name], Directory):
			return self._contents[name]
		else:
			raise ValueError(f"No directory names {name} exists in this directory.")
	
	@property
	def size(self) -> int:
		return sum([obj.size for obj in self._contents.values()])


if __name__ == '__main__':

	top_dir = Directory("/")

	current_dir = top_dir
	current_dir.add_item(File("a", 123, parent=current_dir))
	current_dir.add_item(File("b", 456, parent=current_dir))
	current_dir.add_item(Directory("B", parent=current_dir))

	current_dir = current_dir.get_subdirectory("B")

	current_dir.add_item(File("c", 10, parent=current_dir))

	print(top_dir.size)
