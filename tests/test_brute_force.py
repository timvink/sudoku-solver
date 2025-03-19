from sudoku_solver_tim.puzzle import Puzzle, Row, Column, Cell, Block
from sudoku_solver_tim.strategies.master.brute_force import brute_force

import json
from sudoku_solver_tim.puzzle import Puzzle
from sudoku_solver_tim.strategies import STRATEGY_NAMES
import os
import pytest


def read_from_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def read_all_json_files_in_directory(directory):
    examples = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            examples.extend(read_from_json(filepath))
    return examples


EXAMPLES = read_all_json_files_in_directory("tests/fixtures")


def test_one_brute_force_example():
    """
    Test that we can solve one example using brute force only.
    """
    grid = [
        [1, 9, 5, 3, 6, 7, 2, 4, 8],
        [0, 7, 8, 0, 5, 0, 3, 6, 9],
        [3, 0, 6, 0, 9, 8, 1, 5, 7],
        [0, 0, 3, 7, 8, 0, 5, 9, 0],
        [7, 0, 9, 0, 0, 5, 0, 0, 6],
        [5, 8, 4, 9, 0, 6, 7, 1, 0],
        [8, 3, 2, 5, 4, 9, 6, 7, 1],
        [9, 0, 7, 0, 1, 3, 0, 2, 5],
        [0, 5, 1, 0, 7, 2, 9, 0, 0],
    ]
    p = Puzzle(grid)
    assert brute_force(p)
    assert p.is_solved()
    assert "Brute Force" in p.strategies_used

    p = Puzzle(grid)
    p.solve(strategies=[brute_force])
    assert "Brute Force" in p.strategies_used
    assert p.is_solved()


N_PUZZLE_TO_TEST = 10


@pytest.mark.parametrize(
    "strategies, puzzle, url",
    [(ex["strategies"], ex["puzzle"], ex["url"]) for ex in EXAMPLES[:N_PUZZLE_TO_TEST]],
)
def test_brute_force(strategies, puzzle, url):
    """
    Test cases for brute force strategy.
    """
    # We should be able to solve all the examples using brute force only.
    p = Puzzle(puzzle)
    # Constrain strategies to only the ones in the strategies list
    p.solve(strategies=[brute_force])
    assert "Brute Force" in p.strategies_used
    assert p.is_solved()
