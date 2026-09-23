# P(catch fire) = 1 - (1 - q)^K

import random

OPEN = 1

#find all the open cells
def get_open_cells(grid):
    open_cells = []

    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == OPEN:
                open_cells.append((row, col))

    return open_cells

