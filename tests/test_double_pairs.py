from sudoku_solver.puzzle import Puzzle

from sudoku_solver.strategies.double_pairs import double_pairs

def test_double_pairs():
    """
    Test the double pairs strategy using the example from:
    https://www.sudokuoftheday.com/techniques/double-pairs
    
    The example shows digit 2 appearing only in columns 4 and 6 in both
    top-middle and middle-middle blocks, which means we can eliminate 2
    from those columns in the bottom-middle block.
    """
    # Create a puzzle with the example scenario
    grid = [
        [1, 0, 0,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        
        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        
        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  0, 0, 0]
    ]
    puzzle = Puzzle(grid)
    
    # Set up the markup for digit 2 according to the example
    # Clear all 2s from markup except in specific positions
    for cell in puzzle.cells:
        cell.markup.discard(2)
    
    # Add 2 to markup in top-middle block (only in columns 4 and 6)
    puzzle.rows[0].cells[3].markup.add(2)  # row 1, column 4
    puzzle.rows[0].cells[5].markup.add(2)  # row 1, column 6
    puzzle.rows[1].cells[3].markup.add(2)  # row 2, column 4
    puzzle.rows[1].cells[5].markup.add(2)  # row 2, column 6
    
    # Add 2 to markup in middle-middle block (only in columns 4 and 6)
    puzzle.rows[3].cells[3].markup.add(2)  # row 4, column 4
    puzzle.rows[3].cells[5].markup.add(2)  # row 4, column 6
    puzzle.rows[4].cells[3].markup.add(2)  # row 5, column 4
    puzzle.rows[4].cells[5].markup.add(2)  # row 5, column 6
    
    # Add 2 to markup in bottom-middle block (in all columns)
    puzzle.rows[6].cells[3].markup.add(2)  # row 7, column 4
    puzzle.rows[6].cells[4].markup.add(2)  # row 7, column 5
    puzzle.rows[6].cells[5].markup.add(2)  # row 7, column 6
    puzzle.rows[7].cells[3].markup.add(2)  # row 8, column 4
    puzzle.rows[7].cells[4].markup.add(2)  # row 8, column 5
    puzzle.rows[7].cells[5].markup.add(2)  # row 8, column 6
    puzzle.rows[8].cells[3].markup.add(2)  # row 9, column 4
    puzzle.rows[8].cells[4].markup.add(2)  # row 9, column 5
    puzzle.rows[8].cells[5].markup.add(2)  # row 9, column 6
    
    # Apply the double pairs strategy
    result = double_pairs(puzzle)
    puzzle.show_markup(2)
    
    # Verify the strategy worked
    assert result == True, "Strategy should have made changes"
    
    # Verify 2s were removed from columns 4 and 6 in bottom-middle block
    for row in [6, 7, 8]:  # rows 7-9
        assert 2 not in puzzle.rows[row].cells[3].markup, f"2 should be removed from r{row+1}c4"
        assert 2 not in puzzle.rows[row].cells[5].markup, f"2 should be removed from r{row+1}c6"
        # But 2 should remain in column 5
        assert 2 in puzzle.rows[row].cells[4].markup, f"2 should remain in r{row+1}c5"