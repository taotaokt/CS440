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