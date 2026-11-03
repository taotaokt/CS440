
import random
from collections import deque

OPEN = 1
BLOCKED = 0

#return all open cells in the ship
def get_open_cells(grid):
    return [
        (r, c)
        for r in range(len(grid))
        for c in range(len(grid[0]))
        if grid[r][c] == OPEN
    ]

#return valid four directional neighbor
def get_neighbors(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])

    neighbors = []

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = row + dr
        nc = col + dc

        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))

    return neighbors

#check id all open cells are reachable from each other using bfs algorithm
def is_connected(grid):
    open_cells = get_open_cells(grid)

    if not open_cells:
        return False

    start = open_cells[0]

    queue = deque([start])
    visited = {start}

    while queue:
        row, col = queue.popleft()

        for nr, nc in get_neighbors(grid, row, col):
            if grid[nr][nc] != OPEN:
                continue

            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return len(visited) == len(open_cells)

#generate a candidate by swapping an open cell with a blocked cell
def mutate_ship(grid, rng, attempts=30):

    open_cells = get_open_cells(grid)

    blocked_cells = [
        (r, c)
        for r in range(len(grid))
        for c in range(len(grid[0]))
        if grid[r][c] == BLOCKED
    ]

    if not open_cells or not blocked_cells:
        return [row[:] for row in grid]

    for _ in range(attempts):
        candidate = [row[:] for row in grid]

        opened = rng.choice(blocked_cells)
        closed = rng.choice(open_cells)

        candidate[opened[0]][opened[1]] = OPEN
        candidate[closed[0]][closed[1]] = BLOCKED

        if is_connected(candidate):
            return candidate

    return [row[:] for row in grid]

#generate one connected ship candidate by mutating an existing ship
def generate_candidate_ship(initial_grid, seed=None):
    rng = random.Random(seed)

    return mutate_ship(initial_grid, rng)

#search for a safer ship layout
def optimize_ship(
    initial_grid,
    evaluate_ship,
    generations=10,
    candidates_per_generation=20,
    seed=42
):

    if not is_connected(initial_grid):
        raise ValueError("Initial ship must be connected.")

    rng = random.Random(seed)

    best_ship = [row[:] for row in initial_grid]
    #evaluate_ship(grid) return a numerical fitness score, such as average bot success rate
    best_score = evaluate_ship(best_ship)

    history = [best_score]

    for generation in range(generations):

        generation_best_ship = best_ship
        generation_best_score = best_score

        for _ in range(candidates_per_generation):

            candidate = mutate_ship(best_ship, rng)
            candidate_score = evaluate_ship(candidate)

            if candidate_score > generation_best_score:
                generation_best_ship = candidate
                generation_best_score = candidate_score

        best_ship = generation_best_ship
        best_score = generation_best_score

        history.append(best_score)

        print(
            f"Generation {generation + 1}: "
            f"Best fitness = {best_score:.4f}"
        )

    return best_ship, best_score, history
