import random

BLOCKED = 0
OPEN = 1

#return valid neighbors of the cell
def getneighbors(grid, row, col):
    D = len(grid)
    direction = [
        #up, down, left, right
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]
    neighbors = []

    for drow, dcol in direction:
        new_row = row + drow
        new_col = col + dcol
        if 0 <= new_row <= D and 0 <= new_col <= D:
            neighbors.append((new_row, new_col))
    return neighbors

#count how many neighbor cells opening
def count_open_neighbors(grid, row, col):
    count = 0
    for r, c in getneighbors(grid, row, col):
        if grid[r][c] == OPEN:
            count+=1
    return count

#return all block neighbors cells
def get_block_neighbors(grid, row, col):
    block_neighbors = []
    for r, c in getneighbors(grid, row, col):
        if grid[r][c] == BLOCKED:
            block_neighbors.append((r, c))
    return block_neighbors

#find the blocked cells with one open neighbor
#the target cell ready to open
def find_ready_to_open(grid):
    D = len(grid)
    ready_to_open = []
    for row in range(D):
        for col in range(D):
            if grid[row][col] == BLOCKED:
                if count_open_neighbors(grid, row, col) == 1:
                    ready_to_open.append((row, col))
    return ready_to_open

#find all open cells with only one open neighbor/three dead ends
def find_dead_ends(grid):
    D = len(grid)
    dead_ends = []

    for row in range(D):
        for col in range(D):

            if grid[row][col] == OPEN:
                if count_open_neighbors(grid, row, col) == 1:
                    dead_ends.append((row, col))

    return dead_ends
def generate_ship(D, seed=None):
#generate a D*D ship
    if D<3:
        raise ValueError("D must larger or equal than 3")

    range1 = random.Random(seed)

    #start with a D*D grid with all blocked cells
    grid = [
        [BLOCKED for _ in range(D)]
        for _ in range(D)
    ]
    #randomly choose a cell and open it
    start_row = range1.randrange(1, D-1)
    start_col = range1.randrange(1, D-1)
    grid[start_row][start_col] = OPEN

    #open a blocked cell that already has one open neighbor(ready to open)
    while True:
        ready_to_open = find_ready_to_open(grid)
        if not ready_to_open:
            break

        row, col = range1.choice(ready_to_open)
        grid[row][col] = OPEN

        #find the initial dead end
        initial_dead_ends = find_dead_ends(grid)
        initial_count = len(initial_dead_ends)

        target_count = initial_count // 2
        current_dead_ends = initial_dead_ends

        #open the neighbor of the dead end randomly
        while len(current_dead_ends) > target_count:
            usable_dead_ends = [] #some of the dead end maynot have a blocked neighbor
            for row, col in current_dead_ends:
                if get_block_neighbors(grid, row, col):
                    usable_dead_ends.append((row, col))
            if not usable_dead_ends:
                break

            row, col = range1.choice(usable_dead_ends)

            blocked_neighbors = get_block_neighbors(
                grid, row, col
            )
            new_row, new_col = range1.choice(blocked_neighbors)

            grid[new_row][new_col] = OPEN  #open the cell
            #recompute the dead end because the dead end has changed
            current_dead_ends = find_dead_ends(grid)
    return grid