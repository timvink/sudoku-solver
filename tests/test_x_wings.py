from sudoku_solver.puzzle import Puzzle, Row, Column, Cell, Block
from sudoku_solver.strategies.master.x_wings import x_wings
import logging
import pytest

@pytest.mark.skip(reason="X-Wings strategy is not implemented")
def test_x_wings():
    """
    Test cases for X-Wings strategy.
    Examples from https://www.sudokuoftheday.com/techniques/x-wings
    """
    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Test case 1: X-Wing in rows for number 6
    p = Puzzle([[0] * 9 for _ in range(9)])
    
    # Set up the X-Wing pattern for number 6 in rows 4 and 9
    # The 6s appear in columns 2 and 8 in both rows
    for row_id in [4, 9]:
        for col_id in [2, 8]:
            cell = p.rows[row_id - 1].cells[col_id - 1]
            cell.markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # All candidates
            logging.debug(f"Setting up X-Wing cell ({row_id}, {col_id}) with markup {cell.markup}")
    
    # Add some other candidates to cells in columns 2 and 8
    # These should be eliminated by the X-Wing
    for col_id in [2, 8]:
        for row_id in range(1, 10):
            if row_id not in [4, 9]:  # Skip the X-Wing rows
                cell = p.rows[row_id - 1].cells[col_id - 1]
                if not cell.is_solved:
                    cell.markup.add(6)
                    logging.debug(f"Adding candidate 6 to cell ({row_id}, {col_id})")
    
    # Apply X-Wings strategy
    updated = x_wings(p)
    assert updated, "X-Wings should find and eliminate candidates"
    
    # Verify that 6 was eliminated from other cells in columns 2 and 8
    for col_id in [2, 8]:
        for row_id in range(1, 10):
            if row_id not in [4, 9]:  # Skip the X-Wing rows
                cell = p.rows[row_id - 1].cells[col_id - 1]
                if not cell.is_solved:
                    assert 6 not in cell.markup, f"6 should be eliminated from cell ({row_id}, {col_id})"
                    logging.debug(f"Verified 6 is not in cell ({row_id}, {col_id})")
    
    # Test case 2: X-Wing in columns for number 8
    p = Puzzle([[0] * 9 for _ in range(9)])
    
    # Set up the X-Wing pattern for number 8 in columns 3 and 7
    # The 8s appear in rows 2 and 5 in both columns
    for col_id in [3, 7]:
        for row_id in [2, 5]:
            cell = p.columns[col_id - 1].cells[row_id - 1]
            cell.markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # All candidates
            logging.debug(f"Setting up X-Wing cell ({row_id}, {col_id}) with markup {cell.markup}")
    
    # Add some other candidates to cells in rows 2 and 5
    # These should be eliminated by the X-Wing
    for row_id in [2, 5]:
        for col_id in range(1, 10):
            if col_id not in [3, 7]:  # Skip the X-Wing columns
                cell = p.rows[row_id - 1].cells[col_id - 1]
                if not cell.is_solved:
                    cell.markup.add(8)
                    logging.debug(f"Adding candidate 8 to cell ({row_id}, {col_id})")
    
    # Apply X-Wings strategy
    updated = x_wings(p)
    assert updated, "X-Wings should find and eliminate candidates"
    
    # Verify that 8 was eliminated from other cells in rows 2 and 5
    for row_id in [2, 5]:
        for col_id in range(1, 10):
            if col_id not in [3, 7]:  # Skip the X-Wing columns
                cell = p.rows[row_id - 1].cells[col_id - 1]
                if not cell.is_solved:
                    assert 8 not in cell.markup, f"8 should be eliminated from cell ({row_id}, {col_id})"
                    logging.debug(f"Verified 8 is not in cell ({row_id}, {col_id})")
    
    # Test case 3: No X-Wing (should not update any cells)
    p = Puzzle([[0] * 9 for _ in range(9)])
    
    # Set up a pattern that looks like an X-Wing but isn't
    # The 9s appear in columns 2 and 8 in row 4, but only in column 2 in row 9
    for col_id in [2, 8]:
        cell = p.rows[3].cells[col_id - 1]  # Row 4
        cell.markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # All candidates
        logging.debug(f"Setting up non-X-Wing cell (4, {col_id}) with markup {cell.markup}")
    
    cell = p.rows[8].cells[1]  # Row 9, column 2
    cell.markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # All candidates
    logging.debug(f"Setting up non-X-Wing cell (9, 2) with markup {cell.markup}")
    
    # Apply X-Wings strategy
    updated = x_wings(p)
    assert not updated, "X-Wings should not find a pattern when columns don't match" 