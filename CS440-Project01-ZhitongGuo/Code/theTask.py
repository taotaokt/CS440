# At t = 0, place the bot, button, and initial fire on three distinct open cells.
# At each time step, the bot chooses and makes a move. Reaching the button
# succeeds immediately; otherwise, the fire spreads and may cause failure.

# Bot, Button, and initial Fire are placed on three distinct open cells

OPEN = 1
import random
from Code.theFire import spread_fire

def initialize_task(grid, seed=None):
    rng = random.Random(seed)

    open_cells = []

    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == OPEN:
                open_cells.append((row, col))

    if len(open_cells) < 3:
        raise ValueError("Not enough open cells.")

    #randomly choose three open cells
    bot_position, button_position, fire_position = rng.sample(
        open_cells,
        3
    )

    burning_cells = {fire_position}

    return bot_position, button_position, burning_cells


#check whether the bot's next move is valid
def is_valid_move(grid, current_position, next_position):
    row, col = current_position
    next_row, next_col = next_position

    D = len(grid)

    #next position must be inside the grid
    if not (
        0 <= next_row < D
        and 0 <= next_col < D
    ):
        return False

    #next position must be an open cell
    if grid[next_row][next_col] != OPEN:
        return False

    #the bot can stay in place
    if next_position == current_position:
        return True

    #otherwise the bot can only move one cell
    distance = abs(next_row - row) + abs(next_col - col)

    return distance == 1


def run_task(grid, q, strategy, seed=None):
    rng = random.Random(seed)

    #t = 0
    bot_position, button_position, burning_cells = initialize_task(
        grid,
        seed=seed
    )

    timestep = 0

    while True:
        timestep += 1

        #decides which neighbor cell to move to
        next_position = strategy(
            grid,
            bot_position,
            button_position,
            burning_cells
        )
        #check if the block is valid
        if not is_valid_move(grid, bot_position, next_position):
            raise ValueError(
                f"Invalid move: {bot_position} -> {next_position}"
            )

        #moves
        bot_position = next_position

        #Bot enters fire -> failure
        if bot_position in burning_cells:
            return False, timestep

        #Bot reaches button -> success
        if bot_position == button_position:
            return True, timestep

        #fire advances
        burning_cells = spread_fire(
            grid,
            burning_cells,
            q,
            rng
        )

        #fire reaches bot -> failure
        if bot_position in burning_cells:
            return False, timestep
