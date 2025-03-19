from sudoku_solver_tim.puzzle import Row, Cell, Block, BlockRow, BlockColumn, Column, Row
from sudoku_solver_tim.strategies.advanced.hidden_triples import _find_hidden_triples
from sudoku_solver_tim.strategies.advanced.hidden_pairs import _find_hidden_pairs
from sudoku_solver_tim.strategies.advanced.naked_pairs import _find_naked_pairs
from sudoku_solver_tim.strategies.advanced.naked_triples import _find_naked_triples


def test_find_hidden_triples():
    """
    Test cases for hidden triples strategy.
    Examples from https://www.sudokuoftheday.com/techniques/hidden-pairs-triples
    """

    default_cell_params = {
        "block": Block(0),
        "row": Row(0),
        "column": Column(0),
        "blockrow": BlockRow(0, []),
        "blockcolumn": BlockColumn(0, []),
    }

    # Test case 1: Hidden triple for 3,4,7
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {1, 3, 7}  # first cell in hidden triple
    row.cells[1].value = 9
    row.cells[1].markup = set()
    row.cells[2].markup = {1, 8}
    row.cells[3].markup = {3, 4, 7}  # second cell in hidden triple
    row.cells[4].value = 2
    row.cells[4].markup = set()
    row.cells[5].markup = {3, 4, 7}  # third cell in hidden triple
    row.cells[6].markup = {1, 5, 8}
    row.cells[7].markup = {5, 6}
    row.cells[8].markup = {1, 6}

    # First verify that naked pairs, hidden pairs, and naked triples don't find this
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, "Naked pairs should not identify a hidden triple"
    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 0, "Hidden pairs should not identify a hidden triple"
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 0, "Naked triples should not identify a hidden triple"

    # Then verify that hidden triples finds it
    updated_cells = _find_hidden_triples(row)
    assert len(updated_cells) == 1  # Only cell 0 needs updating
    assert row.cells[0].markup == {3, 7}  # Remove 1
    assert row.cells[3].markup == {3, 4, 7}  # Already correct
    assert row.cells[5].markup == {3, 4, 7}  # Already correct

    # Test case 2: Hidden triple for 1,3,9
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {2, 5, 6}
    row.cells[1].markup = {2, 5, 6}
    row.cells[2].markup = {2, 5, 6, 7}
    row.cells[3].markup = {1, 3, 6, 7, 8, 9}  # hidden triple
    row.cells[4].markup = {2, 8}
    row.cells[5].markup = {1, 2, 3, 7, 9}  # hidden triple
    row.cells[6].value = 4
    row.cells[6].markup = set()
    row.cells[7].markup = {1, 3, 7, 8}  # hidden triple
    row.cells[8].markup = {5, 7, 8}

    # First verify that naked pairs, hidden pairs, and naked triples don't find this
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, "Naked pairs should not identify a hidden triple"
    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 0, "Hidden pairs should not identify a hidden triple"
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 0, "Naked triples should not identify a hidden triple"

    # Then verify that hidden triples finds it
    updated_cells = _find_hidden_triples(row)
    assert len(updated_cells) == 3  # All three cells need updating
    assert row.cells[3].markup == {1, 3, 9}  # Remove 6,7,8
    assert row.cells[5].markup == {1, 3, 9}  # Remove 2,7
    assert row.cells[7].markup == {1, 3}  # Remove 7,8
