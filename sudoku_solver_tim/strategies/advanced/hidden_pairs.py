from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle

from itertools import combinations, chain
import logging


def hidden_pairs(p: "Puzzle") -> bool:
    """
    Applies hidden subset strategies.

    See: https://www.sudokuoftheday.com/techniques/hidden-pairs-triples

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    groups = list(chain(p.rows, p.columns, p.blocks))

    for group in groups:
        updates_found += len(_find_hidden_pairs(group))

    if updates_found > 0:
        logging.debug(f"Hidden pairs iteration updated {updates_found} cells.")
        p.strategies_used.add("Hidden Pairs")
        return True

    return False


def _find_hidden_pairs(group):
    """
    Find hidden pairs in a group and remove other candidates from those cells.

    A hidden pair occurs when two values only appear in two cells in a group.
    We can then remove all other candidates from those two cells.

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

    # Check all possible pairs of candidates, f.e. {1,2}
    for pair in combinations(all_candidates, 2):
        # Find cells that contain any of these candidates
        cells_with_pair = [
            cell for cell in unsolved_cells if any(c in cell.markup for c in pair)
        ]

        # If exactly two cells contain these candidates, check if they are the only cells
        if len(cells_with_pair) == 2:
            # Check if any other cells contain these values
            other_cells = [
                cell for cell in unsolved_cells if cell not in cells_with_pair
            ]
            other_values = set(range(1, 10)) - set(pair)
            if not any(any(c in cell.markup for c in pair) for cell in other_cells):
                # We found a hidden pair - remove all other candidates from these cells
                for cell in cells_with_pair:
                    if cell.remove_markup(other_values):
                        updated_cells.append(cell)

    return updated_cells
