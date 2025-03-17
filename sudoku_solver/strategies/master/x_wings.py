from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sudoku_solver.puzzle import Puzzle

from itertools import combinations
import logging

def x_wings(p: 'Puzzle') -> bool:
    """
    Applies X-Wings strategy.

    See: https://www.sudokuoftheday.com/techniques/x-wings

    An X-Wing occurs when there are two lines (rows or columns) that have the same two positions
    for a number, forming an X pattern. This allows us to eliminate that number from other cells
    in the columns/rows that form the X.

    The key insight is that whichever position the number occupies in one line, it must occupy
    the opposite position in the other line, forming an X. This means we can eliminate that
    number from all other cells in the columns/rows that form the X.

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = 0

    # Check both rows and columns for X-Wings
    updates_found += _find_x_wings_in_rows(p)
    updates_found += _find_x_wings_in_columns(p)

    if updates_found > 0:
        logging.debug(f"X-Wings iteration updated {updates_found} cells.")
        p.strategies_used.add("X-Wings")
        return True
    
    return False

def _find_x_wings_in_rows(p: 'Puzzle') -> int:
    """
    Find X-Wings in rows and eliminate candidates from columns.
    
    Args:
        p: The puzzle to solve
    
    Returns:
        int: Number of cells updated
    """
    updates_found = 0
    
    # Check each pair of rows
    for row1, row2 in combinations(p.rows, 2):
        # For each candidate number
        for num in range(1, 10):
            # Find cells in each row that contain this number
            cells1 = [cell for cell in row1.cells if not cell.is_solved and num in cell.markup]
            cells2 = [cell for cell in row2.cells if not cell.is_solved and num in cell.markup]
            
            # If both rows have exactly two cells with this number
            if len(cells1) == 2 and len(cells2) == 2:
                # Get the column indices
                cols1 = {cell.col_id for cell in cells1}
                cols2 = {cell.col_id for cell in cells2}
                
                # If the columns match, we found an X-Wing
                if cols1 == cols2:
                    # Get the cells that form the X-Wing
                    x_wing_cells = cells1 + cells2
                    
                    # Remove this number from other cells in these columns
                    for col_id in cols1:
                        col = p.columns[col_id - 1]
                        for cell in col.cells:
                            # Only eliminate from cells that are not part of the X-Wing
                            if cell not in x_wing_cells and not cell.is_solved:
                                if num in cell.markup:
                                    cell.markup.remove(num)
                                    updates_found += 1
                                    logging.debug(f"X-Wing in rows: removed {num} from cell ({cell.row_id}, {cell.col_id})")
    
    return updates_found

def _find_x_wings_in_columns(p: 'Puzzle') -> int:
    """
    Find X-Wings in columns and eliminate candidates from rows.
    
    Args:
        p: The puzzle to solve
    
    Returns:
        int: Number of cells updated
    """
    updates_found = 0
    
    # Check each pair of columns
    for col1, col2 in combinations(p.columns, 2):
        # For each candidate number
        for num in range(1, 10):
            # Find cells in each column that contain this number
            cells1 = [cell for cell in col1.cells if not cell.is_solved and num in cell.markup]
            cells2 = [cell for cell in col2.cells if not cell.is_solved and num in cell.markup]
            
            # If both columns have exactly two cells with this number
            if len(cells1) == 2 and len(cells2) == 2:
                # Get the row indices
                rows1 = {cell.row_id for cell in cells1}
                rows2 = {cell.row_id for cell in cells2}
                
                # If the rows match, we found an X-Wing
                if rows1 == rows2:
                    # Get the cells that form the X-Wing
                    x_wing_cells = cells1 + cells2
                    
                    # Remove this number from other cells in these rows
                    for row_id in rows1:
                        row = p.rows[row_id - 1]
                        for cell in row.cells:
                            # Only eliminate from cells that are not part of the X-Wing
                            if cell not in x_wing_cells and not cell.is_solved:
                                if num in cell.markup:
                                    cell.markup.remove(num)
                                    updates_found += 1
                                    logging.debug(f"X-Wing in columns: removed {num} from cell ({cell.row_id}, {cell.col_id})")
    
    return updates_found 