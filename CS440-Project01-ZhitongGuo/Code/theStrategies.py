from collections import deque
import heapq

OPEN = 1


#return all valid open neighbors
def get_open_neighbors(grid, position):
    row, col = position
    D = len(grid)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)
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

#find the shortest path using BFS
def shortest_path(grid, start, goal, blocked_cells=None):
    if blocked_cells is None:
        blocked_cells = set()

    queue = deque([start])
    visited = {start}

    #store the previous cell
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

    #no path
    return None


#Bot 1 plans the shortest path only once.
#It avoids the initial fire cell but ignores later fire spread.
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

        #only calculate the path once
        if self.path is None:
            self.path = shortest_path(
                grid,
                bot_position,
                button_position,
                burning_cells
            )

            self.index = 0

        #if there is no path, stay in place
        if self.path is None:
            return bot_position

        #move to the next cell in the original path
        if self.index < len(self.path) - 1:
            self.index += 1
            return self.path[self.index]

        return bot_position

# Bot 2
#Bot 2 recalculates the shortest path every timestep.
#avoid all current fire cells
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
        return bot_position

    #already at the button
    if len(path) < 2:
        return bot_position

    #only execute the next step
    return path[1]


# Bot 3
#find current fire cells and all open cells adjacent to them
def get_fire_adjacent_cells(grid, burning_cells):
    danger_cells = set(burning_cells)

    for fire_cell in burning_cells:
        for neighbor in get_open_neighbors(grid, fire_cell):
            danger_cells.add(neighbor)

    return danger_cells


#Bot 3 first avoids fire cells and cells adjacent to fire
#no such path exists, only avoids current fire cells
def bot3_strategy(
    grid,
    bot_position,
    button_position,
    burning_cells
):

    danger_cells = get_fire_adjacent_cells(
        grid,
        burning_cells
    )

    #first try the safer path
    path = shortest_path(
        grid,
        bot_position,
        button_position,
        danger_cells
    )

    #if there is no path, only avoid current fire cells
    if path is None:
        path = shortest_path(
            grid,
            bot_position,
            button_position,
            burning_cells
        )

    #if there is still no path, stay in place
    if path is None:
        return bot_position

    if len(path) < 2:
        return bot_position

    return path[1]


# Bot 4
#calculate the true shortest distance from every open cell to the nearest current fire cell using BFS
def fire_distance_map(grid, burning_cells):
    queue = deque()
    distances = {}

    #start BFS from all current fire cells at the same time
    for cell in burning_cells:
        queue.append(cell)
        distances[cell] = 0

    while queue:
        current = queue.popleft()

        for neighbor in get_open_neighbors(grid, current):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances


#find a path that balances path length and fire risk
#Dijkstra algorithm
def risk_aware_path(
    grid,
    start,
    goal,
    burning_cells,
    q
):

    fire_distances = fire_distance_map(
        grid,
        burning_cells
    )

    #total cost, cell
    priority_queue = [(0, start)]

    costs = {
        start: 0
    }

    parent = {}

    #larger q means fire spreads faster, safety receives a larger weight
    risk_weight = 10 * q

    while priority_queue:
        current_cost, current = heapq.heappop(
            priority_queue
        )

        #ignore an outdated queue entry
        if current_cost > costs[current]:
            continue

        #reach the button
        if current == goal:
            path = [current]

            while current != start:
                current = parent[current]
                path.append(current)

            path.reverse()
            return path

        for neighbor in get_open_neighbors(grid, current):

            #never move directly into a burning cell
            if neighbor in burning_cells:
                continue

            fire_distance = fire_distances.get(
                neighbor,
                float("inf")
            )

            #calculate the risk
            if fire_distance == float("inf"):
                risk = 0
            else:
                risk = risk_weight / (fire_distance + 1)

            #normal movement costs 1
            #dangerous cells add extra cost
            move_cost = 1 + risk

            new_cost = current_cost + move_cost

            if (
                neighbor not in costs
                or new_cost < costs[neighbor]
            ):
                costs[neighbor] = new_cost
                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor)
                )

    return None


#Bot 4 uses a risk-aware weighted path
#replan every timestep using the current fire information
class Bot4Strategy:

    def __init__(self, q):
        if not 0 <= q <= 1:
            raise ValueError("q must be between 0 and 1.")

        self.q = q

    def __call__(
        self,
        grid,
        bot_position,
        button_position,
        burning_cells
    ):

        path = risk_aware_path(
            grid,
            bot_position,
            button_position,
            burning_cells,
            self.q
        )

        #if there is no path, stay in place
        if path is None:
            return bot_position

        if len(path) < 2:
            return bot_position

        #replan every timestep and execute only one step
        return path[1]