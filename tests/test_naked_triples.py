from sudoku_solver_tim.puzzle import Row, Cell, Block, BlockRow, BlockColumn, Column, Row
from sudoku_solver_tim.strategies.advanced.naked_triples import _find_naked_triples
from sudoku_solver_tim.strategies.advanced.naked_pairs import _find_naked_pairs


def test_find_naked_triples():
    """
    Test cases for naked triples strategy.
    Examples from https://www.sudokuoftheday.com/techniques/naked-pairs-triples
    """

    default_cell_params = {
        "block": Block(0),
        "row": Row(0),
        "column": Column(0),
        "blockrow": BlockRow(0, []),
        "blockcolumn": BlockColumn(0, []),
    }
    # Test case 1: Perfect naked triple
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
    row.cells[3].markup = {1, 2, 3}
    row.cells[4].markup = {1, 2, 3}
    row.cells[5].markup = {1, 2, 3, 4, 5, 6}
    row.cells[6].markup = {1, 2, 3, 4, 5, 6}
    row.cells[7].markup = {1, 2, 3}
    row.cells[8].markup = {3, 4, 5, 6}

    # First verify that naked pairs doesn't find this as a pair
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, (
        "Naked pairs should not identify a triplet as a pair"
    )
    assert 1 in row.cells[5].markup
    assert 2 in row.cells[5].markup
    assert 3 in row.cells[5].markup

    # Then verify that naked triples finds it
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 3
    assert 1 not in row.cells[5].markup
    assert 2 not in row.cells[5].markup
    assert 3 not in row.cells[5].markup

    # Test case 2: Imperfect naked triple
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
    row.cells[4].markup = {1, 3}
    row.cells[5].markup = {1, 2, 3, 4, 5, 6}
    row.cells[6].markup = {1, 2, 3, 4, 5, 6}
    row.cells[7].markup = {2, 3}
    row.cells[8].markup = {3, 4, 5, 6}

    # First verify that naked pairs doesn't find this as a pair
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, (
        "Naked pairs should not identify a triplet as a pair"
    )
    assert 1 in row.cells[5].markup
    assert 2 in row.cells[5].markup
    assert 3 in row.cells[5].markup

    # Then verify that naked triples finds it
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 3
    assert 1 not in row.cells[5].markup
    assert 2 not in row.cells[5].markup
    assert 3 not in row.cells[5].markup

    # Test case 3: Example from the article: https://www.sudokuoftheday.com/techniques/naked-pairs-triples
    row = Row(1)
    row.cells = [
        Cell(value=0, row_id=i + 1, col_id=1, **default_cell_params) for i in range(9)
    ]
    row.cells[0].markup = {1, 4, 9}
    row.cells[1].markup = {1, 8}
    row.cells[2].markup = {1, 5, 8, 9}
    row.cells[3].markup = {3, 8}
    row.cells[4].markup = {4, 5}
    row.cells[5].value = 7
    row.cells[5].markup = set()
    row.cells[6].markup = {1, 3, 8}
    row.cells[7].value = 6
    row.cells[7].markup = set()
    row.cells[8].value = 2
    row.cells[8].markup = set()

    # First verify that naked pairs doesn't find this as a pair
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 0, (
        "Naked pairs should not identify a triplet as a pair"
    )
    assert 1 in row.cells[0].markup
    assert 1 in row.cells[2].markup
    assert 8 in row.cells[2].markup

    # Then verify that naked triples finds it
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 2
    assert 1 not in row.cells[0].markup
    assert 1 not in row.cells[2].markup
    assert 8 not in row.cells[2].markup
