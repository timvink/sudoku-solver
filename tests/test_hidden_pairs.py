from sudoku_solver_tim.puzzle import Row, Cell, Block, BlockRow, BlockColumn, Column, Row
from sudoku_solver_tim.strategies.advanced.hidden_pairs import _find_hidden_pairs
from sudoku_solver_tim.strategies.advanced.naked_pairs import _find_naked_pairs


def test_find_hidden_pairs():
    """
    Test cases for hidden pairs strategy.
    Examples from https://www.sudokuoftheday.com/techniques/hidden-pairs-triples
    """
    default_cell_params = {
        "block": Block(0),
        "row": Row(0),
        "column": Column(0),
        "blockrow": BlockRow(0, []),
        "blockcolumn": BlockColumn(0, []),
    }
    # Test case 1: Hidden pair for 1 and 3
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].value = 9
    row.cells[0].markup = set()
    row.cells[1].value = 7
    row.cells[1].markup = set()
    row.cells[2].markup = {4, 6}
    row.cells[3].markup = {4, 2}
    row.cells[4].value = 8
    row.cells[4].markup = set()
    row.cells[5].markup = {1, 3}  # first cell in hidden pair
    row.cells[6].value = 5
    row.cells[6].markup = set()
    row.cells[7].markup = {2, 6}
    row.cells[8].markup = {
        1,
        2,
        3,
    }  # second cell in hidden pair. The '2' can be removed.

    # First verify that naked pairs doesn't find this
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, "Naked pairs should not identify a hidden pair"

    # Then verify that hidden pairs finds it
    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 1
    assert row.cells[8].markup == {1, 3}  # Only 1 and 3 should remain

    # Test case 2: Another example from the article
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {1, 3, 6, 9}
    row.cells[1].markup = {5, 7}  # Removed 1 to make it a true hidden pair
    row.cells[2].value = 4
    row.cells[2].markup = set()
    row.cells[3].markup = {6, 9}  # Removed 3 to make it a true hidden pair
    row.cells[4].value = 8
    row.cells[4].markup = set()
    row.cells[5].value = 7
    row.cells[5].markup = set()
    row.cells[6].markup = {5, 7}  # Removed 1 to make it a true hidden pair
    row.cells[7].markup = {1, 3, 6}  # This cell and cell 0 form the hidden pair
    row.cells[8].value = 2
    row.cells[8].markup = set()

    # First verify that naked pairs doesn't find this
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, "Naked pairs should not identify a hidden pair"

    # Then verify that hidden pairs finds it
    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 2
    assert row.cells[0].markup == {1, 3}  # Only 1 and 3 should remain
    assert row.cells[7].markup == {1, 3}  # Only 1 and 3 should remain

    # Test case 3: More complex example
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].value = 9
    row.cells[0].markup = set()
    row.cells[1].value = 8
    row.cells[1].markup = set()
    row.cells[2].value = 7
    row.cells[2].markup = set()
    row.cells[3].markup = {1, 2, 3, 4}
    row.cells[4].markup = {1, 2, 3, 4}
    row.cells[5].markup = {1, 2, 3, 4, 5, 6}
    row.cells[6].markup = {1, 2, 3, 4, 5, 6}
    row.cells[7].markup = {1, 2, 3, 4}
    row.cells[8].markup = {1, 2, 3, 4}

    # First verify that naked pairs doesn't find this
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, "Naked pairs should not identify a hidden pair"

    # Then verify that hidden pairs finds it
    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 2
    assert row.cells[5].markup == {5, 6}  # Only 5 and 6 should remain
    assert row.cells[6].markup == {5, 6}  # Only 5 and 6 should remain
