#Bot、Button、初始 Fire 随机放在三个不同的 open cells
#t = 0
#随机放置 Bot / Button / Fire（三个不同 open cells）
#每个 timestep：Bot 决定下一步 -> Bot 移动 -> 如果到达 Button → 成功，结束 -> 否则 Fire 扩散一次 -> 如果 Bot 和 Fire 在同一格 → 失败

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