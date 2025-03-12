from sudoku_solver.puzzle import Row, Cell
from sudoku_solver.strategies.hidden_subset import _find_hidden_pairs, _find_hidden_triple, _find_hidden_quad

def test_find_hidden_pairs():
    """
    Example from
    https://www.sudokuoftheday.com/techniques/hidden-pairs-triples
    Hidden pair for 1 and 3
    """
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].value = 9; row.cells[0].markup = []
    row.cells[1].value = 7; row.cells[1].markup = []
    row.cells[2].markup = [4,6]
    row.cells[3].markup = [4,2]
    row.cells[4].value = 8; row.cells[4].markup = []
    row.cells[5].markup = [1,3]
    row.cells[6].value = 5; row.cells[6].markup = []
    row.cells[7].markup = [2,6]
    row.cells[8].markup = [1,2,3]

    updated_cells = _find_hidden_pairs(row)
    assert len(updated_cells) == 1
    assert 8 not in row.cells[8].markup

def test_hidden_triple():
    """
    Example from 
    https://www.sudokuoftheday.com/techniques/hidden-pairs-triples
    """
    # hidden triple for 3,4,7
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].markup = [1,3,7]
    row.cells[1].value = 9; row.cells[1].markup = []
    row.cells[2].markup = [1,8]
    row.cells[3].markup = [3,4,7]
    row.cells[4].value = 2; row.cells[4].markup = []
    row.cells[5].markup = [3,4,7]
    row.cells[6].markup = [1,5,8]
    row.cells[7].markup = [5,6]
    row.cells[8].markup = [1,6]

    updated_cells = _find_hidden_triple(row)
    assert len(updated_cells) == 1
    assert 1 not in row.cells[0].markup

    # Hidden triple for 1,3,9
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].markup = [2,5,6]
    row.cells[1].markup = [2,5,6]
    row.cells[2].markup = [2,5,6,7]
    row.cells[3].markup = [1,3,6,7,8,9] # hidden triple
    row.cells[4].markup = [2,8]
    row.cells[5].markup = [1,2,3,7,9] # hidden triple
    row.cells[6].value = 4; row.cells[6].markup = []
    row.cells[7].markup = [1,3,7,8] # hidden triple
    row.cells[8].markup = [5,7,8]

    updated_cells = _find_hidden_triple(row)
    assert len(updated_cells) == 3
    assert 6 not in row.cells[3].markup

def test_hidden_quad():
    """
    Example from 
    https://www.sudokuoftheday.com/techniques/hidden-pairs-triples
    """
    # Hidden quad for 1,2,8,9
    row = Row(1)
    row.cells = [Cell(value=0, row_id=i+1, col_id=1) for i in range(9)]
    row.cells[0].markup = [5,8,9] # hidden quad
    row.cells[1].markup = [1,4,5,8] # hidden quad  
    row.cells[2].markup = [4,5] 
    row.cells[3].markup = [1,2] # hidden quad
    row.cells[4].markup = [2,5,9] # hidden quad
    row.cells[5].markup = [5,6,7] 
    row.cells[6].markup = [4,5,7] 
    row.cells[7].markup = [3,4,5,6] 
    row.cells[8].markup = [3,4,5,7]
    
    updated_cells = _find_hidden_quad(row)
    assert len(updated_cells) == 3
    assert 5 not in row.cells[0].markup
    assert 4 not in row.cells[1].markup
    assert 5 not in row.cells[1].markup
    assert [1,2] == row.cells[3].markup