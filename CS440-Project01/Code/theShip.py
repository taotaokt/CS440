
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

#count how many neighbor cells opening
def count_open_neighbors(grid, row, col):
    count = 0
    for r, c in getneighbors(grid, row, col):
        if grid[r][c] = OPEN:
            count+=1
    return count

#return all block neighbors cells
def get_block_neighbors(grid, row, col):
    block_neighbors = []
    for r, c in getneighbors(grid, row, col):
        if grid[r][c] = BLOCKED:
            block_neighbors.append(r, c)
    return block_neighbors