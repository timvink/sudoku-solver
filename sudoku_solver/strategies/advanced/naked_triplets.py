from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sudoku_solver.puzzle import Puzzle

from itertools import combinations, chain
import logging

def naked_triplets(p: 'Puzzle') -> bool:
    """
    Applies naked subset strategies.

    See: https://www.sudokuoftheday.com/techniques/naked-pairs-triples

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    groups = list(chain(p.rows, p.columns, p.blocks))
    
    for group in groups:
        updates_found += len(_find_naked_triplets(group))

    if updates_found > 0:
        logging.debug(f"Naked triplets iteration updated {updates_found} cells.")
        p.strategies_used.add("Naked Triplets")
        return True
    
    return False

def _find_naked_triplets(group):
    """
    Find naked triplets in a group and remove their candidates from other cells.
    
    Args:
        group: List of cells in a row, column, or block
    
    Returns:
        list: List of cells that were updated
    """
    updated_cells = []
    
    # Get cells with 2 or 3 candidates
    potential_cells = [cell for cell in group if 2 <= len(cell.markup) <= 3]
    
    # Check all possible combinations of 3 cells
    for cells in combinations(potential_cells, 3):
        # Get union of all candidates in these 3 cells
        combined_candidates = set().union(*(cell.markup for cell in cells))
        
        # If union has exactly 3 digits, we found a naked triplet
        if len(combined_candidates) == 3:
            # Remove these candidates from all other cells in group
            for cell in group:
                if cell not in cells and cell.markup:
                    original_markup = cell.markup.copy()
                    cell.markup -= combined_candidates
                    
                    # If we removed any candidates, add to updated list
                    if cell.markup != original_markup:
                        updated_cells.append(cell)
    
    return updated_cells

