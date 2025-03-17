

import json
import pytest
from sudoku_solver.puzzle import Puzzle
from sudoku_solver.strategies import STRATEGY_NAMES
import os

def read_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    

def read_all_json_files_in_directory(directory):
    examples = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            examples.extend(read_from_json(filepath))
    return examples

EXAMPLES = read_all_json_files_in_directory("tests/fixtures")

levels = ['beginner','easy','medium','tricky']
for level in levels:
    unique_strategies = {strategy for ex in EXAMPLES if level in ex['url'] for strategy in ex['strategies']}
    print(f"{level}: {unique_strategies}")


for level in levels:
    for example in EXAMPLES:
        if level in example['url']:
            puzzle = Puzzle(example['puzzle'])
            puzzle.solve()
            if not puzzle.is_solved():
                print(f"{level}: {puzzle.strategies_used}")
                break

# Single Position, Single Candidate, Candidate Lines, Double Pairs, Hidden Pairs
tricky_20220707 = [
    [0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 3, 0, 0],
    [3, 9, 0, 0, 0, 7, 0, 0, 6],
    [0, 0, 3, 1, 4, 0, 0, 0, 0],
    [0, 6, 0, 0, 9, 0, 0, 5, 0],
    [0, 0, 0, 0, 3, 2, 4, 0, 0],
    [1, 0, 0, 4, 0, 0, 0, 7, 8],
    [0, 0, 7, 0, 0, 0, 0, 9, 0],
    [0, 0, 0, 0, 0, 9, 0, 0, 0]
]
p = Puzzle(tricky_20220707)
# p.solve_step(strategies=[STRATEGY_NAMES['Single Candidate']])


p.solve(strategies={STRATEGY_NAMES[s] for s in STRATEGY_NAMES if s in {'Single Candidate', 'Candidate Lines', 'Single Position','Multiple Lines'}})

p.show_markup(1)

p.solve_step(strategies={STRATEGY_NAMES[s] for s in STRATEGY_NAMES if s in {'Multiple Lines'}})
p.show_markup(1)

p.solve(strategies={STRATEGY_NAMES[s] for s in STRATEGY_NAMES if s in {'Single Candidate','Single Position','Candidate Lines',}})


from sudoku_solver.strategies.medium.double_pairs import double_pairs
from copy import deepcopy
cells_before = deepcopy(p.cells)
double_pairs(p)
cells_after = p.cells

for cell_before, cell_after in zip(cells_before, cells_after):
    if cell_before.markup != cell_after.markup:
        print(f"Cell row{cell_before.row.id+1} col{cell_before.col_id+1} markup: {cell_before.markup} --> {cell_after.markup}")

p.show_markup(1)