from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle

from itertools import combinations, chain
import logging


def naked_quads(p: "Puzzle") -> bool:
    """
    Applies naked subset strategies.

    See: https://www.sudokuoftheday.com/techniques/naked-pairs-triples

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    groups = list(chain(p.rows, p.columns, p.blocks))

    for group in groups:
        updates_found += len(_find_naked_quads(group))

    if updates_found > 0:
        logging.debug(f"Naked quads iteration updated {updates_found} cells.")
        p.strategies_used.add("Naked Quads")
        return True

    return False


def _find_naked_quads(group):
    """
    Find naked quads in a group and remove their candidates from other cells.

    Args:
        group: List of cells in a row, column, or block

    Returns:
        list: List of cells that were updated
    """
    updated_cells = []

    # Get cells with 2, 3, or 4 candidates
    potential_cells = [cell for cell in group if 2 <= len(cell.markup) <= 4]

    # Check all possible combinations of 4 cells
    for cells in combinations(potential_cells, 4):
        # Get union of all candidates in these 4 cells
        combined_candidates = set().union(*(cell.markup for cell in cells))

        # If union has exactly 4 digits, we found a naked quad
        if len(combined_candidates) == 4:
            # Remove these candidates from all other cells in group
            for cell in group:
                if cell not in cells and not cell.is_solved:
                    if cell.remove_markup(combined_candidates):
                        updated_cells.append(cell)

    return updated_cells
