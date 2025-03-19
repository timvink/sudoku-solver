from sudoku_solver_tim.puzzle import Row, Cell, Block, BlockRow, BlockColumn, Column, Row
from sudoku_solver_tim.strategies.advanced.naked_pairs import _find_naked_pairs


def test_find_naked_pairs():
    """
    Test cases for naked pairs strategy.
    Examples from https://www.sudokuoftheday.com/techniques/naked-pairs-triples
    """

    default_cell_params = {
        "block": Block(0),
        "row": Row(0),
        "column": Column(0),
        "blockrow": BlockRow(0, []),
        "blockcolumn": BlockColumn(0, []),
    }
    # Test case 1: Perfect naked pair
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
    row.cells[3].markup = {1, 2}
    row.cells[4].markup = {1, 2}
    row.cells[5].markup = {1, 2, 3, 4, 5, 6}
    row.cells[6].markup = {1, 2, 3, 4, 5, 6}
    row.cells[7].markup = {1, 2, 3, 4, 5, 6}
    row.cells[8].markup = {3, 4, 5, 6}

    assert 1 in row.cells[5].markup
    assert 2 in row.cells[5].markup
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 3
    assert 1 not in row.cells[5].markup
    assert 2 not in row.cells[5].markup

    # Test case 2: Example from the article
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {1, 3, 6, 9}
    row.cells[1].markup = {1, 5}
    row.cells[2].value = 4
    row.cells[2].markup = set()
    row.cells[3].markup = {3, 6, 9}
    row.cells[4].value = 8
    row.cells[4].markup = set()
    row.cells[5].value = 7
    row.cells[5].markup = set()
    row.cells[6].markup = {1, 5}
    row.cells[7].markup = {1, 6}
    row.cells[8].value = 2
    row.cells[8].markup = set()

    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 2
    assert 1 not in row.cells[0].markup
    assert 1 not in row.cells[7].markup

    # Test case 3: Another example with different markup combinations
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
    row.cells[3].markup = {2, 3}
    row.cells[4].markup = {2, 3}
    row.cells[5].markup = {1, 2, 3, 4, 5, 6}
    row.cells[6].markup = {1, 2, 3, 4, 5, 6}
    row.cells[7].markup = {1, 2, 3, 4, 5, 6}
    row.cells[8].markup = {1, 4, 5, 6}

    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 3
    assert 2 not in row.cells[5].markup
    assert 3 not in row.cells[5].markup
