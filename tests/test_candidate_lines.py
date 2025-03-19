from sudoku_solver_tim.puzzle import Puzzle
from sudoku_solver_tim.strategies.medium.candidate_lines import candidate_lines


def test_candidate_lines():
    """
    Test the candidate lines strategy on a real-world puzzle.

    See https://www.sudokuoftheday.com/techniques/candidate-lines
    """
    grid = [
        [0, 0, 1, 9, 5, 7, 0, 6, 3],
        [0, 0, 0, 8, 0, 6, 0, 7, 0],
        [7, 6, 9, 1, 3, 0, 8, 0, 5],
        [0, 0, 7, 2, 6, 1, 3, 5, 0],
        [3, 1, 2, 4, 9, 5, 7, 8, 6],
        [0, 5, 6, 3, 7, 8, 0, 0, 0],
        [1, 0, 8, 6, 0, 9, 5, 0, 7],
        [0, 9, 0, 7, 1, 0, 6, 0, 8],
        [6, 7, 4, 5, 8, 3, 0, 0, 0],
    ]
    puzzle = Puzzle(grid)
    result = candidate_lines(puzzle, [4])
    assert result == True

    assert 4 not in puzzle.rows[2].cells[7].markup
    assert 4 not in puzzle.rows[5].cells[7].markup
