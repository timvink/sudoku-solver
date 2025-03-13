from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sudoku_solver.puzzle import Puzzle

from itertools import combinations, groupby, chain
import logging

def naked_subset(p: 'Puzzle') -> bool:
    """
    Applies naked subset strategies.

    See:

    - https://www.sudokuoftheday.com/techniques/naked-pairs-triples

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    groups = list(chain(p.rows, p.columns, p.blocks))
    
    for group in groups:
        updates_found += len(_find_naked_pairs(group))
    if updates_found > 0:
        logging.debug(f"Naked pairs iteration updated {updates_found} cells.")
        p.strategies_used.add("naked pairs")
        return True
    
    for group in groups:
        updates_found += len(_find_naked_triples(group))
    if updates_found > 0:
        logging.debug(f"Naked triples iteration updated {updates_found} cells.")
        p.strategies_used.add("naked triples")
        return True

    for group in groups:
        updates_found += len(_find_naked_quads(group))
    if updates_found > 0:
        logging.debug(f"Naked quads iteration updated {updates_found} cells.")
        p.strategies_used.add("naked quads")
        return True

    return False



def _find_naked_triples(group):
    """
    A naked triple is just 3 values shared across 3 cells.

    Has $\binom{9}{3}=84$ combinations.
    """
    updated_cells = []

    # Unsolved cells with <= 3 options
    candidate_triples = [c for c in group.cells if not c.is_solved and len(c.markup) <= 3]
    # Combinations of max 9 cells in sets of 3 yields 84 combinations
    candidate_triples = combinations(candidate_triples, 3)

    for triple in candidate_triples:
        options = set(chain(*[c.markup for c in triple])) 
        # if between the markup of 3 cells
        # there are only 3 options
        # it's a naked triple
        if len(options) == 3:
            # Remove the options from other cells 
            for remove_value in list(options):
                updated_cells += [c for c in group.cells if c not in triple and c.remove_markup(remove_value)]
            
    return list(set(updated_cells))


def _find_naked_quads(group):
    """
    A naked quad is just 4 values shared across 4 cells.

    Has $\binom{9}{4}=126$ combinations.
    """
    updated_cells = []

    # Unsolved cells with <= 4 options
    candidate_quads = [c for c in group.cells if not c.is_solved and len(c.markup) <= 4]
    # Combinations of max 9 cells in sets of 4 yields 126 combinations
    candidate_quads = combinations(candidate_quads, 4)

    for quad in candidate_quads:
        options = set(chain(*[c.markup for c in quad])) 
        # if between the markup of 4 cells
        # there are only 4 options
        # it's a naked quad
        if len(options) == 4:
            # Remove the options from other cells 
            for remove_value in list(options):
                updated_cells += [c for c in group.cells if c not in quad and c.remove_markup(remove_value)]
            
    return list(set(updated_cells))
    


def all_equal(iterable):
    """
    credits: https://stackoverflow.com/a/3844832/5525118
    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)