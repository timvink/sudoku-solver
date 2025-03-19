from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle

from itertools import combinations, groupby, chain
import logging


def naked_pairs(p: "Puzzle") -> bool:
    """
    Applies naked subset strategies.

    See: https://www.sudokuoftheday.com/techniques/naked-pairs-triples

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    groups = list(chain(p.rows, p.columns, p.blocks))

    for group in groups:
        updates_found += len(_find_naked_pairs(group))

    if updates_found > 0:
        logging.debug(f"Naked pairs iteration updated {updates_found} cells.")
        p.strategies_used.add("Naked Pairs")
        return True

    return False


def _find_naked_pairs(group):
    updated_cells = []

    # All unique pairs of unsolved cells with <= 2 options
    # max 9 cells in sets of 2 yields 36 combinations
    candidate_pairs = combinations(
        [c for c in group.cells if not c.is_solved and len(c.markup) <= 2], 2
    )
    candidate_pairs = list(candidate_pairs)  # remove after debugging
    for pair in candidate_pairs:
        # If pair is a naked double
        if _all_equal([p.markup for p in pair]):
            # Take their markup
            for remove_value in pair[0].markup:
                # And remove from other cells in the group
                updated_cells += [
                    c
                    for c in group.cells
                    if c not in pair and c.remove_markup(remove_value)
                ]

    return list(set(updated_cells))


def _all_equal(iterable):
    """
    credits: https://stackoverflow.com/a/3844832/5525118
    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)
