from sudoku_solver_tim.puzzle import Puzzle

from sudoku_solver_tim.strategies.medium.double_pairs import double_pairs


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
        [9, 3, 4, 0, 6, 0, 0, 5, 0],
        [0, 0, 6, 0, 0, 4, 9, 2, 3],
        [0, 0, 8, 9, 0, 0, 0, 4, 6],
        [8, 0, 0, 5, 4, 6, 0, 0, 7],
        [6, 0, 0, 0, 1, 0, 0, 0, 5],
        [5, 0, 0, 3, 9, 0, 0, 6, 2],
        [3, 6, 0, 4, 0, 1, 2, 7, 0],
        [4, 7, 0, 6, 0, 0, 5, 0, 0],
        [0, 8, 0, 0, 0, 0, 6, 3, 4],
    ]
    puzzle = Puzzle(grid)

    # Remove alls 2s from first and third block columns
    for column in [puzzle.blockcolumns[0], puzzle.blockcolumns[2]]:
        for cell in column.cells:
            cell.markup.discard(2)

    # Remove some more 2s to reflect the example
    puzzle.rows[2].cells[4].markup.discard(2)
    puzzle.rows[2].cells[5].markup.discard(2)

    # Verify the markup is set up correctly
    assert 2 in puzzle.rows[7].cells[5].markup, "2 should be in r8c6"
    assert 2 in puzzle.rows[8].cells[3].markup, "2 should be in r9c4"
    assert 2 in puzzle.rows[8].cells[5].markup, "2 should be in r9c6"
    # Apply the double pairs strategy
    puzzle.show_markup(2)
    result = double_pairs(puzzle, [2])
    # Verify the strategy worked
    assert result == True, "Strategy should have made changes"

    # Verify 2s were removed from columns 4 and 6 in bottom-middle block
    assert 2 not in puzzle.rows[7].cells[5].markup, "2 should be removed from r8c6"
    assert 2 not in puzzle.rows[8].cells[3].markup, "2 should be removed from r9c4"
    assert 2 not in puzzle.rows[8].cells[5].markup, "2 should be removed from r9c6"
