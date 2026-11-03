import random
OPEN = 1

#get all the open cells
#for bots to be place
def get_open_cells(grid):
    open_cells = []

    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == OPEN:
                open_cells.append((row, col))

    return open_cells

#get a cell randomly to place the bot
def place_bot(grid, seed=None):
    range1 = random.Random(seed)

    open_cells = get_open_cells(grid)

    #invalid case
    if not open_cells:
        raise ValueError("No open cell available for the bot.")

    return range1.choice(open_cells)

#get next valid place for bot to move
def get_valid_moves(grid, bot_position):
    row, col = bot_position
    D = len(grid)

    #up, down, left, right
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]

    valid_moves = []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if (
            0 <= new_row < D
            and 0 <= new_col < D
            and grid[new_row][new_col] == OPEN
        ):
            valid_moves.append((new_row, new_col))

    return valid_moves
