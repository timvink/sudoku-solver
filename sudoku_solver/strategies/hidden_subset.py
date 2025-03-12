"""
Hidden subset strategies.


A combination of 3 values
Only possible in 3 cells.
Is a triplet (aka triple).

If a triple has markup values other than the set of 3 in its cells, 
it's a hidden triplet.
Otherwise, it's naked.

Strategy to find them:
Naked= find 3 cells that have only 3 unique markup values between them.
-- update other cells markup 

Hidden= find set of 3 values that only occur in 3 cells markup.
-- update internal markup (remove not in set)
-- update other cells (remove in set)

"""

import logging
from sudoku_solver.puzzle import Puzzle
from itertools import combinations, chain

def hidden_subset(p: Puzzle) -> bool:
    """
    Applies hidden subset strategies.

    See:

    - https://www.sudokuoftheday.com/techniques/hidden-pairs-triples

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    groups = list(chain(p.rows, p.columns, p.blocks))
    
    for group in groups:
        updates_found += len(_find_hidden_pairs(group))
    if updates_found > 0:
        logging.debug(f"Hidden pairs iteration updated {updates_found} cells.")
        p.strategies_used.add("hidden pairs")
        return True
    
    for group in groups:
        updates_found += len(_find_hidden_triple(group))
    if updates_found > 0:
        logging.debug(f"Hidden triples iteration updated {updates_found} cells.")
        p.strategies_used.add("hidden triples")
        return True

    for group in groups:
        updates_found += len(_find_hidden_quad(group))
    if updates_found > 0:
        logging.debug(f"Hidden quads iteration updated {updates_found} cells.")
        p.strategies_used.add("hidden quads")
        return True

    return False


def _find_hidden_pairs(group):
    """
    For each pair of unsolved cells,
    If they have between them a set of values,
    that are not contained in any of the other cells,
    we can remove value not in that set within the pair.
    """
    updated_cells = []

    unsolved_cells = [c for c in group.cells if not c.is_solved]

    # TODO: move this a methods of a Group class (Row, Block, Column can inherit)?
    unsolved_cells = [c for c in group.cells if not c.is_solved]
    unsolved_values = set(chain(*[c.markup for c in unsolved_cells]))

    # For every combination length 2 of unsolved values
    for value_set in combinations(unsolved_values, 2):
        
        # Cells that have at least one value in the value set
        valid_cells = [c for c in unsolved_cells if any([v in c.markup for v in value_set])]

        # value_set is present in markup of only 2 cells
        if len(valid_cells) == 2:
            # Hidden triple found. Now make the triple naked.
            invalid_values = set(unsolved_values) - set(value_set)
            for invalid_value in invalid_values:
                updated_cells += [c for c in valid_cells if c.remove_markup(invalid_value)]

    return list(set(updated_cells))

def _find_hidden_triple(group):
    """
    """
    updated_cells = []

    # TODO: move this a methods of a Group class (Row, Block, Column can inherit)?
    unsolved_cells = [c for c in group.cells if not c.is_solved]
    unsolved_values = set(chain(*[c.markup for c in unsolved_cells]))

    # For every combination length 3 of unsolved values
    for value_set in combinations(unsolved_values, 3):
        
        # Cells that have at least one value in the value set
        valid_cells = [c for c in unsolved_cells if any([v in c.markup for v in value_set])]

        # value_set is present in markup of only 3 cells
        if len(valid_cells) == 3:
            # Hidden triple found. Now make the triple naked.
            invalid_values = set(unsolved_values) - set(value_set)
            for invalid_value in invalid_values:
                updated_cells += [c for c in valid_cells if c.remove_markup(invalid_value)]

    return list(set(updated_cells))

def _find_hidden_quad(group):
    """
    """
    updated_cells = []

    # TODO: move this a methods of a Group class (Row, Block, Column can inherit)?
    unsolved_cells = [c for c in group.cells if not c.is_solved]
    unsolved_values = set(chain(*[c.markup for c in unsolved_cells]))

    # For every combination length 4 of unsolved values
    for value_set in combinations(unsolved_values, 4):
        
        # Cells that have at least one value in the value set
        valid_cells = [c for c in unsolved_cells if any([v in c.markup for v in value_set])]

        # value_set is present in markup of only 4 cells
        if len(valid_cells) == 4:
            logging.debug(f"Valid cells: {valid_cells}")
            logging.debug(f"Value set: {value_set}")
            # Hidden triple found. Now make the triple naked.
            invalid_values = set(unsolved_values) - set(value_set)
            for invalid_value in invalid_values:
                updated_cells += [c for c in valid_cells if c.remove_markup(invalid_value)]

    return list(set(updated_cells))
