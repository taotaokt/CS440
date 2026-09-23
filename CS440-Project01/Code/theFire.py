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

#put the start fire in a random cell
def place_fire(grid, seed = None):
    range1 = random.Random(seed)

    open_cells = get_open_cells(grid)

    if not open_cells:
        raise ValueError("No open cell is available for the fire.")

    return range1.choice(open_cells)

#count for the burning neighbor for the cell
def count_burning_neighbors(grid, row, col, burning_cells):
    D = len(grid)

    directions = [
        #up, down, left, right
        (-1, 0), (1, 0), (0, -1), (0, 1) 
    ]

    count = 0

    for drow, dcol in directions:
        new_row = row + drow
        new_col = col + dcol

        if (
            0 <= new_row<D
            and 0 <= new_col<D
            and (new_row, new_col) in burning_cells
        ):
            count += 1

    return count

def spread_fire(grid, burning_cells, q, rng):
    if not 0 <= q <= 1:
        raise ValueError("q value error.")

    new_fires = set()

    for row in range(len(grid)):
        for col in range(len(grid)):

            #only not burning cells can catch fire
            if (
                grid[row][col] == OPEN
                and (row, col) not in burning_cells
            ):

                K = count_burning_neighbors(
                    grid,
                    row,
                    col,
                    burning_cells
                )

                if K > 0:
                    probability = 1 - (1 - q) ** K

                    if rng.random() < probability:
                        new_fires.add((row, col))

    #all new cells catch fire at the end of this time step
    return burning_cells | new_fires
