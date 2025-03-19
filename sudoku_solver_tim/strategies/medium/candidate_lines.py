from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle

import logging


def candidate_lines(p: "Puzzle", digits: list[int] | None = None) -> bool:
    """
    Applies candidate lines strategy.

    See:

    - https://www.sudokuoftheday.com/techniques/candidate-lines

    Returns:
        bool: Whether 1 or more cells have been updated.
    """

    updates_found = _candidate_lines_iteration(p.blocks, digits)

    solutions_found = updates_found > 0
    while updates_found > 0:
        p.strategies_used.add("Candidate Lines")
        updates_found = _candidate_lines_iteration(p.blocks, digits)

    return solutions_found


def _candidate_lines_iteration(blocks, digits: list[int] | None = None):
    updates_found = 0

    for block in blocks:
        for value in digits or range(1, 10):
            possible_rows = list(set([c.row for c in block.cells if value in c.markup]))
            if len(possible_rows) == 1:
                other_block_cells_in_row = [
                    c
                    for c in possible_rows[0].cells
                    if not c.is_solved and c not in block.cells
                ]
                updated_cells = [
                    c for c in other_block_cells_in_row if c.remove_markup(value)
                ]

                if len(updated_cells) > 0:
                    updates_found += 1

            possible_columns = list(
                set(
                    [
                        c.column
                        for c in block.cells
                        if not c.is_solved and value in c.markup
                    ]
                )
            )
            if len(possible_columns) == 1:
                other_block_cells_in_column = [
                    c
                    for c in possible_columns[0].cells
                    if not c.is_solved and c not in block.cells
                ]
                updated_cells = [
                    c for c in other_block_cells_in_column if c.remove_markup(value)
                ]

                if len(updated_cells) > 0:
                    updates_found += 1

    if updates_found > 0:
        logging.debug(f"Candidate Lines iteration updated {updates_found} cells.")

    return updates_found > 0
