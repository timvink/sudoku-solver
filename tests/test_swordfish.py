from sudoku_solver_tim.puzzle import Puzzle, Row, Column, Cell, Block
from sudoku_solver_tim.strategies.master.x_wings import x_wings
from sudoku_solver_tim.strategies.master.swordfish import swordfish
import logging


def test_swordfish():
    """
    Test cases for Swordfish strategy.
    Examples from https://www.sudokuoftheday.com/techniques/swordfish
    """
    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)

    # Example from https://www.sudokuoftheday.com/techniques/swordfish
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
    p.show_markup(4)

    # Apply Swordfish strategy
    assert 4 in p.rows[1].cells[3].markup, "4 should be eliminated from cell (2, 4)"
    updated = swordfish(p)
    assert updated, "Swordfish should find and eliminate candidates"
    assert 4 not in p.rows[1].cells[3].markup, "4 should be eliminated from cell (2, 4)"
