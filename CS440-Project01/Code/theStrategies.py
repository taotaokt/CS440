from collections import deque
import heapq

OPEN = 1


#return all valid open neighbors
def get_open_neighbors(grid, position):
    row, col = position
    D = len(grid)

    directions = [ (-1, 0), (1, 0), (0, -1),(0, 1)
    ]

    neighbors = []

    for drow, dcol in directions:
        new_row = row + drow
        new_col = col + dcol

        if (
            0 <= new_row < D
            and 0 <= new_col < D
            and grid[new_row][new_col] == OPEN
        ):
            neighbors.append((new_row, new_col))

    return neighbors

#shortest path BFS
def shortest_path(grid, start, goal, blocked_cells=None):

    if blocked_cells is None:
        blocked_cells = set()

    queue = deque([start])
    visited = {start}

    parent = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            path = [current]

            while current != start:
                current = parent[current]
                path.append(current)

            path.reverse()
            return path

        for neighbor in get_open_neighbors(grid, current):

            if (
                neighbor not in visited
                and neighbor not in blocked_cells
            ):
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None