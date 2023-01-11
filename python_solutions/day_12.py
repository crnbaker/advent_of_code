from dataclasses import dataclass
import sys
from typing import Optional, cast, Dict, List, Tuple
from matplotlib.pyplot import subplots
from numpy import (
    argwhere,
    array,
    diff,
    int_,
    ndarray,
    ravel_multi_index,
    unravel_index,
    zeros,
)
from numpy.typing import NDArray
from tqdm import tqdm


@dataclass(frozen=True)
class GridPoint:
    grid_size: Tuple[int, int]
    row: int
    col: int

    @property
    def ravelled_index(self) -> int:
        index = cast(int, ravel_multi_index((self.row, self.col), self.grid_size))
        if isinstance(index, ndarray):
            print(self.row)
            print(self.col)
            print(self.grid_size)
            print(index)
            print(type(index))
        return index

    @classmethod
    def from_ravelled_index(cls, grid_size: Tuple[int, int], index: int) -> "GridPoint":
        (x, y) = unravel_index(index, grid_size)
        row = cast(int, x)
        col = cast(int, y)
        return GridPoint(grid_size=grid_size, row=row, col=col)


class Graph:
    def __init__(self, grid_size: Tuple[int, int]) -> None:
        num_nodes = grid_size[0] * grid_size[1]
        self._adjacency_matrix = zeros([num_nodes, num_nodes], dtype=int_)
        self._grid_size = grid_size

    def add_edge(self, from_point: GridPoint, to_point: GridPoint):
        self._adjacency_matrix[from_point.ravelled_index, to_point.ravelled_index] = 1

    @property
    def nodes(self) -> List[GridPoint]:
        nodes = []
        for n in range(self._grid_size[0]):
            for m in range(self._grid_size[1]):
                nodes.append(GridPoint(self._grid_size, n, m))
        return nodes

    def get_node_neighbours(self, node: GridPoint) -> List[GridPoint]:
        node_row = self._adjacency_matrix[node.ravelled_index, :]
        neighbours_ravelled_indices = argwhere(node_row == 1)[:, 0]
        neighbours: List[GridPoint] = []
        for ravelled_index in neighbours_ravelled_indices:
            neighbours.append(
                GridPoint.from_ravelled_index(self._grid_size, ravelled_index)
            )
        return neighbours

    def plot(self) -> None:
        _, ax = subplots(1, 1)
        for node in self.nodes:
            ax.plot(node.col, node.row, "rx")
            for neighbor in self.get_node_neighbours(node):
                ax.arrow(
                    node.col,
                    node.row,
                    neighbor.col - node.col,
                    neighbor.row - node.row,
                    length_includes_head=True,
                    head_width=0.15,
                    head_length=0.15,
                )
        ax.invert_yaxis()
        ax.axis("equal")

    def transpose(self) -> None:
        self._adjacency_matrix = self._adjacency_matrix.T


class AltitudeMap:
    def __init__(self) -> None:
        map = []

        with open("../inputs/day_12.txt", "r") as f:
            for line in f.readlines():
                row = [int(ord(c) - ord("a")) for c in line.strip()]
                map.append(row)

        self._map: NDArray[int_] = array(map, dtype=int)
        self._start = tuple(argwhere(self._map == (ord("S") - ord("a")))[0])
        self._stop = tuple(argwhere(self._map == (ord("E") - ord("a")))[0])

        self._map[self._start[0], self._start[1]] = 0
        self._map[self._stop[0], self._stop[1]] = 25

    @property
    def start(self) -> GridPoint:
        return GridPoint(
            grid_size=self.grid_dimensions, row=self._start[0], col=self._start[1]
        )

    @property
    def stop(self) -> GridPoint:
        return GridPoint(
            grid_size=self.grid_dimensions, row=self._stop[0], col=self._stop[1]
        )

    @property
    def minima(self) -> List[GridPoint]:
        zero_alt_points = argwhere(self._map == 0)

        zero_alt = [
            GridPoint(grid_size=self.grid_dimensions, row=p[0], col=p[1])
            for p in zero_alt_points
        ] + [self.start]

        return zero_alt

    @property
    def grid_dimensions(self) -> Tuple[int, int]:
        return cast(Tuple[int, int], self._map.shape)

    @property
    def num_grid_points(self) -> int:
        return self._map.shape[0] * self._map.shape[1]

    def get_hor_gradients(self) -> NDArray[int_]:
        grad_x = zeros((self._map.shape[0], self._map.shape[1] - 1), dtype=int_)
        for (x, row) in zip(grad_x, self._map):
            x[:] = diff(row).astype(int_)
        return grad_x

    def get_ver_gradients(self) -> NDArray[int_]:
        grad_y = zeros((self._map.shape[0] - 1, self._map.shape[1]), dtype=int_)
        for (y, col) in zip(grad_y.T, self._map.T):
            y[:] = diff(col).astype(int_)
        return grad_y


def dijkstra_algorithm(
    graph: Graph, start: GridPoint, end: Optional[GridPoint] = None
) -> Dict[int, int]:
    unvisited_nodes = graph.nodes
    shortest_paths: Dict[int, int] = {}
    previous_nodes: Dict[int, int] = {}

    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_paths[node.ravelled_index] = max_value
    shortest_paths[start.ravelled_index] = 0

    def should_continue(_unvisited_nodes: List[GridPoint]) -> bool:
        if end is not None:
            return end in _unvisited_nodes
        else:
            return len(_unvisited_nodes) > 0

    with tqdm(total=len(unvisited_nodes)) as pbar:
        while should_continue(unvisited_nodes):
            num_nodes_left_to_visit = len(unvisited_nodes)
            current_min_node = None
            for node in unvisited_nodes:
                if current_min_node is None:
                    current_min_node = node
                elif (
                    shortest_paths[node.ravelled_index]
                    < shortest_paths[current_min_node.ravelled_index]
                ):
                    current_min_node = node

            # The code block below retrieves the current node's neighbors and updates their distances
            if current_min_node is not None:
                neighbors = graph.get_node_neighbours(current_min_node)
                for neighbor in neighbors:
                    tentative_value = (
                        shortest_paths[current_min_node.ravelled_index] + 1
                    )
                    if tentative_value < shortest_paths[neighbor.ravelled_index]:
                        shortest_paths[neighbor.ravelled_index] = tentative_value
                        # We also update the best path to the current node
                        previous_nodes[
                            neighbor.ravelled_index
                        ] = current_min_node.ravelled_index

                # After visiting its neighbors, we mark the node as "visited"
                unvisited_nodes.remove(current_min_node)
            else:
                raise RuntimeError("Pathfinding failed")
            pbar.update(num_nodes_left_to_visit - len(unvisited_nodes))

    # Return the length of the shortest paths from start to each node
    return shortest_paths


def graph_factory(altitude_map: AltitudeMap) -> Graph:

    graph = Graph(altitude_map.grid_dimensions)
    for n, grad_row in enumerate(altitude_map.get_hor_gradients()):
        for m, edge in enumerate(grad_row):
            left_node = GridPoint(grid_size=altitude_map.grid_dimensions, row=n, col=m)
            right_node = GridPoint(
                grid_size=altitude_map.grid_dimensions, row=n, col=m + 1
            )
            if edge <= 1:
                graph.add_edge(from_point=left_node, to_point=right_node)
            if edge >= -1:
                graph.add_edge(from_point=right_node, to_point=left_node)

    for n, grad_col in enumerate(altitude_map.get_ver_gradients()):
        for m, edge in enumerate(grad_col):
            upper_node = GridPoint(grid_size=altitude_map.grid_dimensions, row=n, col=m)
            lower_node = GridPoint(
                grid_size=altitude_map.grid_dimensions, row=n + 1, col=m
            )
            if edge <= 1:
                graph.add_edge(from_point=upper_node, to_point=lower_node)
            if edge >= -1:
                graph.add_edge(from_point=lower_node, to_point=upper_node)
    return graph


def main():

    map = AltitudeMap()

    graph = graph_factory(map)
    graph.plot()

    shortest_path = dijkstra_algorithm(graph, map.start, map.stop)[
        map.stop.ravelled_index
    ]
    print(f"Shortest path from S to E has {shortest_path} steps")

    graph.transpose()
    shortest_paths = dijkstra_algorithm(graph, map.stop)
    paths_to_minima = [shortest_paths[p.ravelled_index] for p in map.minima]
    print(
        f"Shortest path from any zero-altitude point to end is {min(paths_to_minima)}"
    )


if __name__ == "__main__":
    main()
