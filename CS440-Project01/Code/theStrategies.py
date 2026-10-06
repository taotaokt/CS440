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

#bot1: one shortest path, avoid initial fire, 永远按照这个path走，无论fire怎么扩散
#如果Fire烧到了原来的path，不重新规划bot1
class Bot1Strategy:

    def __init__(self):
        self.path = None
        self.index = 0


    def __call__(
        self,
        grid,
        bot_position,
        button_position,
        burning_cells
    ):

        #only plan once
        if self.path is None:

            self.path = shortest_path(
                grid,
                bot_position,
                button_position,
                burning_cells
            )

            self.index = 0

        #no path exists
        if self.path is None:
            return None

        #follow the original path
        if self.index < len(self.path) - 1:
            self.index += 1
            return self.path[self.index]

        return bot_position
    
    #bot 2
    #every time step renew BFS
    def bot2_strategy(
    grid,
    bot_position,
    button_position,
    burning_cells
):

    path = shortest_path(
        grid,
        bot_position,
        button_position,
        burning_cells
    )

    if path is None:
        return None

    if len(path) < 2:
        return bot_position

    return path[1]
