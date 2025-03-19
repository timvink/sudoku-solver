from sudoku_solver_tim.puzzle import Puzzle, Row, Column, Cell, Block
from sudoku_solver_tim.strategies.master.x_wings import x_wings
import logging


def test_x_wings():
    """
    Test cases for X-Wings strategy.
    Examples from https://www.sudokuoftheday.com/techniques/x-wings
    """
    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)

    # Example from https://www.sudokuoftheday.com/techniques/x-wings
    grid = [
        [9, 0, 0, 0, 5, 1, 7, 3, 0],
        [1, 0, 7, 3, 9, 8, 2, 0, 5],
        [5, 0, 0, 0, 7, 6, 0, 9, 1],
        [8, 1, 0, 7, 2, 4, 3, 5, 0],
        [2, 0, 0, 1, 6, 5, 0, 0, 7],
        [0, 7, 5, 9, 8, 3, 0, 1, 2],
        [0, 2, 1, 5, 3, 7, 0, 0, 0],
        [7, 5, 8, 6, 4, 9, 1, 2, 3],
        [3, 9, 0, 8, 1, 2, 5, 7, 0],
    ]
    p = Puzzle(grid)
    p.show_markup(6)

    # Apply X-Wings strategy
    assert 6 in p.rows[6].cells[8].markup, "6 should be eliminated from cell (6, 8)"
    updated = x_wings(p)
    assert updated, "X-Wings should find and eliminate candidates"
    assert 6 not in p.rows[6].cells[8].markup, "6 should be eliminated from cell (6, 8)"
