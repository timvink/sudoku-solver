from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Cell, Puzzle

from typing import List
import logging


def single_candidates(p: "Puzzle") -> bool:
    """
    Applies single candidate strategy.

    Checks each cell's markup.

    See:

    - https://www.sudokuoftheday.com/techniques/single-candidate

    Args:
        cells (list): cells with known values to propagate.

    Returns:
        bool: Whether 1 or more cells have been solved.
    """
    solution_found = False

    # Do a first pass to see if we can solve any cells
    newly_solved_cells = _single_candidate_iteration(p.cells)
    if len(newly_solved_cells) > 0:
        logging.debug(
            f"Single Candidate iteration found {len(newly_solved_cells)} cells."
        )
        solution_found = True
        p.strategies_used.add("Single Candidate")

    # Keep solving cells until we can't solve any more
    while len(newly_solved_cells) > 0:
        newly_solved_cells = _single_candidate_iteration(p.cells)
        if len(newly_solved_cells) > 0:
            logging.debug(
                f"Single Candidate iteration found {len(newly_solved_cells)} cells."
            )

    return solution_found


def _single_candidate_iteration(cells: List["Cell"]) -> List["Cell"]:
    solved_cells = []
    for cell in cells:
        if cell.is_solved:
            continue
        if len(cell.markup) == 1:
            solution = cell.markup.pop()
            cell.set_solution(solution)
            solved_cells.append(cell)
    return solved_cells
