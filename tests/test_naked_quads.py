from sudoku_solver_tim.puzzle import Row, Cell, Block, BlockRow, BlockColumn, Column, Row
from sudoku_solver_tim.strategies.advanced.naked_quads import _find_naked_quads
from sudoku_solver_tim.strategies.advanced.naked_triples import _find_naked_triples
from sudoku_solver_tim.strategies.advanced.naked_pairs import _find_naked_pairs


def test_find_naked_quads():
    """
    Test cases for naked quads strategy.
    Examples from https://www.sudokuoftheday.com/techniques/naked-pairs-triples
    """

    default_cell_params = {
        "block": Block(0),
        "row": Row(0),
        "column": Column(0),
        "blockrow": BlockRow(0, []),
        "blockcolumn": BlockColumn(0, []),
    }

    # Test case 1: Perfect naked quad
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

    # First verify that naked pairs and triples don't find this
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, "Naked pairs should not identify a quad as a pair"
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 0, (
        "Naked triples should not identify a quad as a triplet"
    )

    # Then verify that naked quads finds it
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 2
    assert 1 not in row.cells[5].markup
    assert 2 not in row.cells[5].markup
    assert 3 not in row.cells[5].markup
    assert 4 not in row.cells[5].markup

    # Test case 2: Imperfect naked quad
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
    row.cells[4].markup = {2, 3}
    row.cells[5].markup = {1, 2, 3, 4, 5, 6}
    row.cells[6].markup = {1, 2, 3, 4, 5, 6}
    row.cells[7].markup = {1, 4}
    row.cells[8].markup = {3, 4}

    # First verify that naked pairs and triples don't find this
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, "Naked pairs should not identify a quad as a pair"
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 0, (
        "Naked triples should not identify a quad as a triplet"
    )

    # Then verify that naked quads finds it
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 2
    assert 1 not in row.cells[5].markup
    assert 2 not in row.cells[5].markup
    assert 3 not in row.cells[5].markup
    assert 4 not in row.cells[5].markup

    # Test case 3: Example from the article
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {7, 5}  # quad
    row.cells[1].markup = {1, 5, 3}  # quad
    row.cells[2].markup = {1, 5, 3, 7}  # quad
    row.cells[3].markup = {4, 5, 6}
    row.cells[4].markup = {2, 4, 5}
    row.cells[5].value = 8
    row.cells[5].markup = set()
    row.cells[6].markup = {6, 7, 9}
    row.cells[7].markup = {2, 3, 9}
    row.cells[8].markup = {3, 7}  # quad

    # First verify that naked pairs and triples don't find this
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, "Naked pairs should not identify a quad as a pair"
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 0, (
        "Naked triples should not identify a quad as a triplet"
    )

    # Then verify that naked quads finds it
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 4
    assert 5 not in row.cells[3].markup
    assert 5 not in row.cells[4].markup
    assert 7 not in row.cells[6].markup
    assert 3 not in row.cells[7].markup
