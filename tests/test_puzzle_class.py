from sudoku_solver_tim.puzzle import Puzzle


def test_puzzle_class():
    # Example from https://www.sudokuoftheday.com/techniques/swordfish
    grid = [
        [1, 9, 5, 3, 6, 7, 2, 4, 8],
        [0, 7, 8, 0, 5, 0, 3, 6, 9],
        [3, 0, 6, 0, 9, 8, 1, 5, 7],
        [0, 0, 3, 7, 8, 0, 5, 9, 0],
        [7, 0, 9, 0, 0, 5, 0, 0, 6],
        [5, 8, 4, 9, 0, 6, 7, 1, 0],
        [8, 3, 2, 5, 4, 9, 6, 7, 1],
        [9, 0, 7, 0, 1, 3, 0, 2, 5],
        [0, 5, 1, 0, 7, 2, 9, 0, 0],
    ]
    p = Puzzle(grid)

    assert len(p.cells) == 9 * 9
    assert len(p.rows) == 9
    assert len(p.columns) == 9
    assert len(p.blocks) == 9
    assert len(p.blockrows) == 3
    assert len(p.blockcolumns) == 3
    for row in p.rows:
        assert len(row.cells) == 9
    for column in p.columns:
        assert len(column.cells) == 9

    assert p.grid == grid

def test_puzzle_from_string():
    string = "2.48........7.5....13.....9..7.......26....3.3...26.4...9..845.87.....16....6.2.."
    grid = [
        [2, 0, 4, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 5, 0, 0, 0],
        [0, 1, 3, 0, 0, 0, 0, 0, 9],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 2, 6, 0, 0, 0, 0, 3, 0],
        [3, 0, 0, 0, 2, 6, 0, 4, 0],
        [0, 0, 9, 0, 0, 8, 4, 5, 0],
        [8, 7, 0, 0, 0, 0, 0, 1, 6],
        [0, 0, 0, 0, 6, 0, 2, 0, 0],
    ]
    puzzle = Puzzle.from_string(string)
    assert puzzle.grid == grid
