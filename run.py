import os
import logging

# Configure logging based on environment variable
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from sudoku_solver_tim.puzzle import Puzzle

tricky_20220707 = [
    [0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 3, 0, 0],
    [3, 9, 0, 0, 0, 7, 0, 0, 6],
    [0, 0, 3, 1, 4, 0, 0, 0, 0],
    [0, 6, 0, 0, 9, 0, 0, 5, 0],
    [0, 0, 0, 0, 3, 2, 4, 0, 0],
    [1, 0, 0, 4, 0, 0, 0, 7, 8],
    [0, 0, 7, 0, 0, 0, 0, 9, 0],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
]
p = Puzzle(tricky_20220707)
p.blocks[0]

p.solve()
# print(p)
p.show_markup()
