from sudoku_solver.puzzle import Row, Cell
from sudoku_solver.strategies.naked_subset import _find_naked_pairs, _find_naked_triples, _find_naked_quads

def test_find_naked_pairs():

    # Here row 3 and 4 contain a naked pair
    # Cell 5,6,7 should have updated markup
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].value = 9; row.cells[0].markup = set()
    row.cells[1].value = 8; row.cells[1].markup = set()
    row.cells[2].value = 7; row.cells[2].markup = set()
    row.cells[3].markup = {1,2}
    row.cells[4].markup = {1,2}
    row.cells[5].markup = {1,2,3,4,5,6}
    row.cells[6].markup = {1,2,3,4,5,6}
    row.cells[7].markup = {1,2,3,4,5,6}
    row.cells[8].markup = {3,4,5,6}

    assert 1 in row.cells[5].markup
    assert 2 in row.cells[5].markup
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 3
    assert 1 not in row.cells[5].markup
    assert 2 not in row.cells[5].markup

    # Example from https://www.sudokuoftheday.com/techniques/naked-pairs-triples
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].markup = {1,3,6,9}
    row.cells[1].markup = {1,5}
    row.cells[2].value = 4; row.cells[2].markup = set()
    row.cells[3].markup = {3,6,9}
    row.cells[4].value = 8; row.cells[4].markup = set()
    row.cells[5].value = 7; row.cells[5].markup = set()
    row.cells[6].markup = {1,5}
    row.cells[7].markup = {1,6}
    row.cells[8].value = 2; row.cells[8].markup = set()
    updated_cells = _find_naked_pairs(row)
    assert len(updated_cells) == 2
    assert 1 not in row.cells[0].markup
    assert 1 not in row.cells[7].markup

def test_find_naked_triple():

    # Here row 3,4,7 contain a naked triple
    # Cell 5,6,8 should have updated markup
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].value = 9; row.cells[0].markup = set()
    row.cells[1].value = 8; row.cells[1].markup = set()
    row.cells[2].value = 7; row.cells[2].markup = set()
    row.cells[3].markup = {1,2,3}
    row.cells[4].markup = {1,2,3}
    row.cells[5].markup = {1,2,3,4,5,6}
    row.cells[6].markup = {1,2,3,4,5,6}
    row.cells[7].markup = {1,2,3}
    row.cells[8].markup = {3,4,5,6}

    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 3
    assert 1 not in row.cells[5].markup
    assert 2 not in row.cells[5].markup
    assert 3 not in row.cells[5].markup

    # Here row 3,4,7 contain a naked triple
    # Cell 5,6,8 should have updated markup
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].value = 9; row.cells[0].markup = set()
    row.cells[1].value = 8; row.cells[1].markup = set()
    row.cells[2].value = 7; row.cells[2].markup = set()
    row.cells[3].markup = {1,2}
    row.cells[4].markup = {1,3}
    row.cells[5].markup = {1,2,3,4,5,6}
    row.cells[6].markup = {1,2,3,4,5,6}
    row.cells[7].markup = {2,3}
    row.cells[8].markup = {3,4,5,6}

    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 3
    assert 1 not in row.cells[5].markup
    assert 2 not in row.cells[5].markup
    assert 3 not in row.cells[5].markup

    # From the example in 
    # https://www.sudokuoftheday.com/techniques/naked-pairs-triples
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].markup = {1,4,9}
    row.cells[1].markup = {1,8}
    row.cells[2].markup = {1,5,8,9}
    row.cells[3].markup = {3,8}
    row.cells[4].markup = {4,5}
    row.cells[5].value = 7; row.cells[5].markup = set()
    row.cells[6].markup = {1,3,8}
    row.cells[7].value = 6; row.cells[7].markup = set()
    row.cells[8].value = 2; row.cells[8].markup = set()
    updated_cells = _find_naked_triples(row)
    assert len(updated_cells) == 2
    assert 1 not in row.cells[0].markup
    assert 1 not in row.cells[2].markup
    assert 8 not in row.cells[2].markup


def test_naked_quads():
    # Here row 3,4,7,8 contain a naked quad
    # Cell 5,6 should have updated markup
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].value = 9; row.cells[0].markup = set()
    row.cells[1].value = 8; row.cells[1].markup = set()
    row.cells[2].value = 7; row.cells[2].markup = set()
    row.cells[3].markup = {1,2,3,4}
    row.cells[4].markup = {1,2,3,4}
    row.cells[5].markup = {1,2,3,4,5,6}
    row.cells[6].markup = {1,2,3,4,5,6}
    row.cells[7].markup = {1,2,3,4}
    row.cells[8].markup = {1,2,3,4}
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 2
    assert 1 not in row.cells[5].markup
    assert 1 not in row.cells[6].markup

    # Here row 3,4,7,8 contain a naked quad
    # Cell 5,6 should have updated markup
    # variation: not full markup but a subset
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].value = 9; row.cells[0].markup = set()
    row.cells[1].value = 8; row.cells[1].markup = set()
    row.cells[2].value = 7; row.cells[2].markup = set()
    row.cells[3].markup = {1,2}
    row.cells[4].markup = {2,3}
    row.cells[5].markup = {1,2,3,4,5,6}
    row.cells[6].markup = {1,2,3,4,5,6}
    row.cells[7].markup = {1,4}
    row.cells[8].markup = {3,4}
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 2
    assert 1 not in row.cells[5].markup
    assert 1 not in row.cells[6].markup    

    # Another example from 
    # https://www.sudokuoftheday.com/techniques/naked-pairs-triples
    # A quad for 1,3,5,7
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].markup = {7,5} # quad
    row.cells[1].markup = {1,5,3} # quad
    row.cells[2].markup = {1,5,3,7} # quad
    row.cells[3].markup = {4,5,6}
    row.cells[4].markup = {2,4,5}
    row.cells[5].value = 8; row.cells[5].markup = set()
    row.cells[6].markup = {6,7,9}
    row.cells[7].markup = {2,3,9}
    row.cells[8].markup = {3,7} # quad
    updated_cells = _find_naked_quads(row)
    assert len(updated_cells) == 4
    assert 5 not in row.cells[3].markup
    assert 5 not in row.cells[4].markup
    assert 7 not in row.cells[6].markup
    assert 3 not in row.cells[7].markup
