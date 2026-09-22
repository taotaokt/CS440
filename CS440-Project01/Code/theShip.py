
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

    for drow, dcol in directions:
        new_row = row + drow
        new_col = col + dcol
        if 0 <= new_row <= D and 0 <= new_col <= D:
            neighbors.append(new_row, new_col)
    return neighbors