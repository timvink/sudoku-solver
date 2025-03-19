from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle

from itertools import combinations, chain
import logging


def naked_triples(p: "Puzzle") -> bool:
    """
    Applies naked subset strategies.

    See: https://www.sudokuoftheday.com/techniques/naked-pairs-triples

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    groups = list(chain(p.rows, p.columns, p.blocks))

    for group in groups:
        updates_found += len(_find_naked_triples(group))

    if updates_found > 0:
        logging.debug(f"Naked triples iteration updated {updates_found} cells.")
        p.strategies_used.add("Naked Triples")
        return True

    return False


def _find_naked_triples(group):
    """
    Find naked triples in a group and remove their candidates from other cells.

    A naked triple occurs when three cells in a group contain exactly three candidates.
    We can then remove these candidates from all other cells in the group.

    Args:
        group: List of cells in a row, column, or block

    Returns:
        list: List of cells that were updated
    """
    updated_cells = []

    # Get all unsolved cells
    unsolved_cells = [cell for cell in group if not cell.is_solved]

    # Check all possible triples of cells
    for cells in combinations(unsolved_cells, 3):
        # Get all candidates from these cells
        candidates = set().union(*(cell.markup for cell in cells))

        # If exactly three candidates, we found a naked triple
        if len(candidates) == 3:
            # Remove these candidates from all other cells
            other_cells = [cell for cell in unsolved_cells if cell not in cells]
            for cell in other_cells:
                if cell.remove_markup(candidates):
                    updated_cells.append(cell)

    return updated_cells
