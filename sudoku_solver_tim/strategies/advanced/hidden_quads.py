from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle

from itertools import combinations, chain
import logging


def hidden_quads(p: "Puzzle") -> bool:
    """
    Applies hidden subset strategies.

    See: https://www.sudokuoftheday.com/techniques/hidden-pairs-triples

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    groups = list(chain(p.rows, p.columns, p.blocks))

    for group in groups:
        updates_found += len(_find_hidden_quads(group))

    if updates_found > 0:
        logging.debug(f"Hidden quads iteration updated {updates_found} cells.")
        p.strategies_used.add("Hidden Quads")
        return True

    return False


def _find_hidden_quads(group):
    """
    Find hidden quads in a group and remove other candidates from those cells.

    A hidden quad occurs when four values only appear in four cells in a group.
    We can then remove all other candidates from those four cells.

    Args:
        group: List of cells in a row, column, or block

    Returns:
        list: List of cells that were updated
    """
    updated_cells = []

    # Get all unsolved cells
    unsolved_cells = [cell for cell in group if not cell.is_solved]

    # Get all candidates from unsolved cells
    all_candidates = set().union(*(cell.markup for cell in unsolved_cells))

    # Check all possible quadruples of candidates
    for quad in combinations(all_candidates, 4):
        # Find cells that contain any of these candidates
        cells_with_quad = [
            cell for cell in unsolved_cells if any(c in cell.markup for c in quad)
        ]

        # If exactly four cells contain these candidates, check if they are the only cells
        if len(cells_with_quad) == 4:
            # Check if any other cells contain these values
            other_cells = [
                cell for cell in unsolved_cells if cell not in cells_with_quad
            ]
            other_values = set(range(1, 10)) - set(quad)
            if not any(any(c in cell.markup for c in quad) for cell in other_cells):
                # We found a hidden quad - remove all other candidates from these cells
                for cell in cells_with_quad:
                    if cell.remove_markup(other_values):
                        updated_cells.append(cell)

    return updated_cells
