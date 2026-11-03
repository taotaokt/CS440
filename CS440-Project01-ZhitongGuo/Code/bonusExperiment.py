
import random

from Code.theStrategies import (
    Bot1Strategy,
    bot2_strategy,
    bot3_strategy,
    Bot4Strategy,
)
from Code.theTask import run_task
from Code.bonusShip import optimize_ship, is_connected


#create a new strategy for each simulation
#Bot 1 initialized again for it stores its path
def create_strategy(bot_id, q):

    if bot_id == 1:
        return Bot1Strategy()

    if bot_id == 2:
        return bot2_strategy

    if bot_id == 3:
        return bot3_strategy

    if bot_id == 4:
        return Bot4Strategy(q)

    raise ValueError("Invalid bot ID.")


#evaluate the performance of all four bots on one ship
def evaluate_ship(
    grid,
    q_values=(0.3, 0.5, 0.7),
    trials=20,
    seed=42
):

    if not is_connected(grid):
        raise ValueError("The ship must be connected.")

    if trials <= 0:
        raise ValueError("Trials must be positive.")

    if not q_values:
        raise ValueError("At least one q value is required.")

    results = {}
    all_rates = []

    rng = random.Random(seed)

    trial_seeds = [
        rng.randrange(10**9)
        for _ in range(trials)
    ]

    for q in q_values:

        if not 0 <= q <= 1:
            raise ValueError("q must be between 0 and 1.")

        for bot_id in range(1, 5):

            successes = 0

            for trial_seed in trial_seeds:

                #fresh strategy for each trial
                strategy = create_strategy(bot_id, q)

                #run the  simulation
                success, timestep = run_task(
                    grid,
                    q,
                    strategy,
                    seed=trial_seed
                )

                if success:
                    successes += 1

            success_rate = successes / trials

            results[(q, bot_id)] = success_rate
            all_rates.append(success_rate)

    #average success rate across all bots and q values
    fitness = sum(all_rates) / len(all_rates)

    return fitness, results


#find a safer ship using the optimization algorithm.
def run_bonus_optimization(
    initial_grid,
    generations=10,
    candidates=20,
    q_values=(0.3, 0.5, 0.7),
    trials=20,
    seed=42
):

    if not is_connected(initial_grid):
        raise ValueError("Initial ship must be connected.")

    if generations < 0 or candidates < 0:
        raise ValueError(
            "Generations and candidates cannot be negative."
        )

    def fitness_function(grid):

        fitness, _ = evaluate_ship(
            grid,
            q_values=q_values,
            trials=trials,
            seed=seed
        )

        return fitness

    best_ship, best_score, history = optimize_ship(
        initial_grid,
        evaluate_ship=fitness_function,
        generations=generations,
        candidates_per_generation=candidates,
        seed=seed
    )

    return best_ship, best_score, history


#compare the original ship with the optimized ship
def compare_ships(
    original_grid,
    optimized_grid,
    q_values=(0.3, 0.5, 0.7),
    trials=200,
    seed=2026
):

    if not is_connected(original_grid):
        raise ValueError("Original ship must be connected.")

    if not is_connected(optimized_grid):
        raise ValueError("Optimized ship must be connected.")

    output = []

    ships = [
        ("Original", original_grid),
        ("Optimized", optimized_grid)
    ]

    for ship_name, grid in ships:

        fitness, results = evaluate_ship(
            grid,
            q_values=q_values,
            trials=trials,
            seed=seed
        )

        print(f"\n{ship_name} Ship")
        print(f"Average fitness: {fitness:.4f}")

        for (q, bot_id), rate in sorted(results.items()):

            print(
                f"q = {q:.2f}, "
                f"Bot {bot_id}, "
                f"Success rate = {rate:.3f}"
            )

            output.append({
                "ship": ship_name,
                "q": q,
                "bot": bot_id,
                "success_rate": rate
            })

    return output


#count open cells in a ship
def count_open_cells(grid):

    return sum(
        1
        for row in grid
        for cell in row
        if cell == 1
    )


#check that optimization preserved the ship constraints
def verify_optimized_ship(original_grid, optimized_grid):

    original_rows = len(original_grid)
    optimized_rows = len(optimized_grid)

    original_cols = len(original_grid[0])
    optimized_cols = len(optimized_grid[0])

    same_size = (
        original_rows == optimized_rows
        and original_cols == optimized_cols
    )

    same_open_count = (
        count_open_cells(original_grid)
        == count_open_cells(optimized_grid)
    )

    connected = is_connected(optimized_grid)

    print("\nShip Verification")
    print("Same grid size:", same_size)
    print("Same number of open cells:", same_open_count)
    print("All open cells connected:", connected)

    return same_size and same_open_count and connected
