import random
OPEN = 1

#find all available open cells
def get_available_cells(grid, occupied=None):
    if occupied is None:
        occupied = set()

    available_cells = []

    for row in range(len(grid)):
        for col in range(len(grid)):
            if (
                grid[row][col] == OPEN
                and (row, col) not in occupied
            ):
                available_cells.append((row, col))

    return available_cells


#put the button on a random empty cell
#Button != Bot
#Button != initial Fire
def place_button(grid, occupied=None, seed=None):
    rng = random.Random(seed)

    available_cells = get_available_cells(grid, occupied)

    if not available_cells:
        raise ValueError("No empty cell is available for the button.")

    return rng.choice(available_cells)

#initialization
def press_button(bot_position, button_position, burning_cells):
    if bot_position == button_position:
        return set() #no burning cells

    return burning_cells