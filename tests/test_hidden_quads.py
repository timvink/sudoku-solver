from sudoku_solver_tim.puzzle import Row, Cell, Block, BlockRow, BlockColumn, Column, Row
from sudoku_solver_tim.strategies.advanced.hidden_quads import _find_hidden_quads
from sudoku_solver_tim.strategies.advanced.hidden_triples import _find_hidden_triples
from sudoku_solver_tim.strategies.advanced.hidden_pairs import _find_hidden_pairs
from sudoku_solver_tim.strategies.advanced.naked_quads import _find_naked_quads


def test_find_hidden_quads():
    """
    Test cases for hidden quads strategy.
    Examples from https://www.sudokuoftheday.com/techniques/hidden-pairs-triples
    """

    default_cell_params = {
        "block": Block(0),
        "row": Row(0),
        "column": Column(0),
        "blockrow": BlockRow(0, []),
        "blockcolumn": BlockColumn(0, []),
    }
    # Test case 1: Hidden quad for 1,2,3,4
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {5, 6, 7, 8, 9}
    row.cells[1].markup = {5, 6, 7, 8, 9}
    row.cells[2].markup = {5, 6, 7, 8, 9}
    row.cells[3].markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # first cell in hidden quad
    row.cells[4].markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # second cell in hidden quad
    row.cells[5].markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # third cell in hidden quad
    row.cells[6].markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # fourth cell in hidden quad
    row.cells[7].markup = {5, 6, 7, 8, 9}
    row.cells[8].markup = {5, 6, 7, 8, 9}

    # First verify that other strategies don't find this
    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 0, "Hidden pairs should not identify a quad as a pair"
    updated_cells = _find_hidden_triples(row)
    assert len(updated_cells) == 0, (
        "Hidden triples should not identify a quad as a triple"
    )
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 0, "Naked quads should not identify a hidden quad"

    # Then verify that hidden quads finds it
    updated_cells = _find_hidden_quads(row)
    assert len(updated_cells) == 4  # All four cells should be updated
    assert row.cells[3].markup == {1, 2, 3, 4}
    assert row.cells[4].markup == {1, 2, 3, 4}
    assert row.cells[5].markup == {1, 2, 3, 4}
    assert row.cells[6].markup == {1, 2, 3, 4}

    # Test case 2: Hidden quad for 5,6,7,8
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {1, 2, 3, 4, 9}
    row.cells[1].markup = {1, 2, 3, 4, 9}
    row.cells[2].markup = {1, 2, 3, 4, 9}
    row.cells[3].markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    row.cells[4].markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    row.cells[5].markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    row.cells[6].markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    row.cells[7].markup = {1, 2, 3, 4, 9}
    row.cells[8].markup = {1, 2, 3, 4, 9}

    # First verify that other strategies don't find this
    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 0, "Hidden pairs should not identify a quad as a pair"
    updated_cells = _find_hidden_triples(row)
    assert len(updated_cells) == 0, (
        "Hidden triples should not identify a quad as a triple"
    )
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 0, "Naked quads should not identify a hidden quad"

    # Then verify that hidden quads finds it
    updated_cells = _find_hidden_quads(row)
    assert len(updated_cells) == 4  # All four cells should be updated
    assert row.cells[3].markup == {5, 6, 7, 8}
    assert row.cells[4].markup == {5, 6, 7, 8}
    assert row.cells[5].markup == {5, 6, 7, 8}
    assert row.cells[6].markup == {5, 6, 7, 8}

    # Test case 3: Another example with hidden quad
    # From https://www.sudokuoftheday.com/techniques/hidden-pairs-triples
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {5, 8, 9}  # first cell in hidden quad 1, 2, 8, 9
    row.cells[1].markup = {1, 4, 5, 8}  # second cell in hidden quad 1, 2, 8, 9
    row.cells[2].markup = {4, 5}
    row.cells[3].markup = {1, 2}  # third cell in hidden quad 1, 2, 8, 9
    row.cells[4].markup = {2, 5, 9}  # fourth cell in hidden quad 1, 2, 8, 9
    row.cells[5].markup = {5, 6, 7}
    row.cells[6].markup = {4, 5, 7}
    row.cells[7].markup = {3, 4, 5, 6}
    row.cells[8].markup = {3, 4, 5, 7}

    # First verify that other strategies don't find this
    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 0, "Hidden pairs should not identify a quad as a pair"
    updated_cells = _find_hidden_triples(row)
    assert len(updated_cells) == 0, (
        "Hidden triples should not identify a quad as a triple"
    )
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 0, "Naked quads should not identify a hidden quad"

    # Then verify that hidden quads finds it
    updated_cells = _find_hidden_quads(row)

    for cell in row:
        print(cell.markup)

    assert row.cells[0].markup == {8, 9}
    assert row.cells[1].markup == {1, 8}
    assert row.cells[3].markup == {1, 2}
    assert row.cells[4].markup == {2, 9}
    assert len(updated_cells) == 3
