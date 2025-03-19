from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Cell, Puzzle

from itertools import chain
import logging


def single_position(p: "Puzzle") -> bool:
    """
    Applies the single position strategy on all cells.

    For every row, column and block, if a value is only found in one cell, then that cell must be that value.
    See:

    - https://www.sudokuoftheday.com/techniques/single-position

    Returns:
        bool: Whether 1 or more cells have been solved.
    """
    solutions_found = False

    # Check each group (rows, columns, blocks) for values that only appear in one cell's markup
    for group in chain(p.rows, p.columns, p.blocks):
        for value in range(1, 10):
            # Find cells in this group that could contain this value
            possible_cells = [
                c for c in group.cells if not c.is_solved and value in c.markup
            ]

            # If only one cell could contain this value, that must be the solution
            if len(possible_cells) == 1:
                possible_cells[0].set_solution(value)
                solutions_found = True
                logging.debug(
                    f"Single Position found solution: value {value} in {group.__class__.__name__} {group.id}"
                )
                p.strategies_used.add("Single Position")

    return solutions_found
