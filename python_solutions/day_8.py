from enum import Enum
from pathlib import Path
from typing import List


INPUT_FILE_PATH = Path("../inputs/day_8.txt")


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Forest:
    def __init__(self) -> None:
        self._tree_grid: List[List[int]] = load_tree_grid()

    def get_row(self, row: int) -> List[int]:
        return self._tree_grid[row]

    def get_col(self, col: int) -> List[int]:
        return [r[col] for r in self._tree_grid]

    def line_of_sight_length(
        self, start_row: int, start_col: int, direction: Direction
    ) -> int:
        if (direction == Direction.DOWN) or (direction == Direction.UP):
            trees = self.get_col(start_col)
            home_tree_index = start_row
        else:
            trees = self.get_row(start_row)
            home_tree_index = start_col

        if (direction == Direction.UP) or (direction == Direction.LEFT):
            trees = trees[::-1]
            home_tree_index = len(trees) - (home_tree_index + 1)

        i = -1
        home_tree = trees[home_tree_index]

        for i, other_tree in enumerate(trees[home_tree_index + 1 :]):
            if other_tree >= home_tree:
                break

        return i + 1

    def calc_tree_view_score(self, tree_row: int, tree_col: int) -> int:
        view_length_up = self.line_of_sight_length(tree_row, tree_col, Direction.UP)
        view_length_down = self.line_of_sight_length(tree_row, tree_col, Direction.DOWN)
        view_length_left = self.line_of_sight_length(tree_row, tree_col, Direction.LEFT)
        view_length_right = self.line_of_sight_length(
            tree_row, tree_col, Direction.RIGHT
        )
        return view_length_up * view_length_down * view_length_left * view_length_right

    def get_view_score_map(self) -> List[List[int]]:
        view_map: List[List[int]] = []
        for row_index, row in enumerate(self._tree_grid):
            view_map_row = []
            for col_index in range(len(row)):
                view_map_row.append(self.calc_tree_view_score(row_index, col_index))
            view_map.append(view_map_row)
        return view_map

    def is_tree_visible(self, row_index: int, col_index: int) -> bool:
        tree = self._tree_grid[row_index][col_index]
        tree_row = self.get_row(row_index)
        tree_col = self.get_col(col_index)
        hidden_lhs = any([t >= tree for t in tree_row[:col_index]])
        hidden_rhs = any([t >= tree for t in tree_row[col_index + 1 :]])
        hidden_top = any([t >= tree for t in tree_col[:row_index]])
        hidden_bottom = any([t >= tree for t in tree_col[row_index + 1 :]])
        hidden = hidden_lhs and hidden_rhs and hidden_top and hidden_bottom
        return not hidden

    def get_visibility_map(self) -> List[List[bool]]:
        visibility_map: List[List[bool]] = []
        for row_index, row in enumerate(self._tree_grid):
            visibility_map_row = []
            for col_index in range(len(row)):
                visibility_map_row.append(self.is_tree_visible(row_index, col_index))
            visibility_map.append(visibility_map_row)
        return visibility_map


def load_tree_grid() -> List[List[int]]:
    tree_grid: List[List[int]] = []
    with open(INPUT_FILE_PATH, "r") as f:
        for line in f.readlines():
            tree_grid.append([int(i) for i in list(line.strip())])
    return tree_grid


def main() -> None:
    forest = Forest()
    visibility_map = forest.get_visibility_map()
    num_visible = sum([len([tree for tree in row if tree]) for row in visibility_map])
    print(f"There are {num_visible} trees visible")

    view_map = forest.get_view_score_map()
    max_score = max([max([score for score in row]) for row in view_map])
    print(f"Max score is {max_score}")


if __name__ == "__main__":
    main()
