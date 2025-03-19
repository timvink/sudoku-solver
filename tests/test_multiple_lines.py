from sudoku_solver_tim.puzzle import Puzzle
from sudoku_solver_tim.strategies.medium.multiple_lines import multiple_lines
from sudoku_solver_tim.strategies.medium.double_pairs import double_pairs
from sudoku_solver_tim.strategies import STRATEGIES


def test_multiple_lines():
    """
    Test the multiple lines strategy using the example from:
    https://www.sudokuoftheday.com/techniques/multiple-lines

    The example shows digit 5 appearing only in the first two columns across two blocks,
    which means we can eliminate 5 from column 1 in the middle box.
    """
    # Create a puzzle with the example scenario
    grid = [
        [0, 0, 9, 0, 3, 0, 6, 0, 0],
        [0, 3, 6, 0, 1, 4, 0, 8, 9],
        [1, 0, 0, 8, 6, 9, 0, 3, 5],
        [0, 9, 0, 0, 0, 0, 8, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 9, 0],
        [0, 6, 8, 0, 9, 0, 1, 7, 0],
        [6, 0, 1, 9, 0, 3, 0, 0, 2],
        [9, 7, 2, 6, 4, 0, 3, 0, 0],
        [0, 0, 3, 0, 2, 0, 9, 0, 0],
    ]
    puzzle = Puzzle(grid)

    # Remove alls 5s from second and third block columns
    for column in puzzle.blockcolumns[1:3]:
        for cell in column.cells:
            cell.markup.discard(5)

    puzzle.show_markup(5)
    # Apply the double pairs strategy
    result = double_pairs(puzzle, [5])
    assert result == False, "Double pairs strategy should not have changed anything"

    # Apply the multiple lines strategy
    result = multiple_lines(puzzle, [5])
    puzzle.show_markup(5)

    # Verify the strategy worked
    assert result == True, "Strategy should have made changes"

    # Verify 5s were removed from column 1 in middle-left block
    for row in [3, 4, 5]:  # rows 4-6
        assert 5 not in puzzle.rows[row].cells[0].markup, (
            f"5 should be removed from r{row + 1}c3"
        )

    # There was another bug where the strategy introduced a wrong solution..
    grid = [
        [0, 0, 0, 2, 5, 0, 0, 9, 0],
        [0, 0, 7, 4, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 8, 0, 0, 0],
        [8, 0, 6, 0, 1, 0, 0, 7, 9],
        [9, 0, 0, 0, 2, 0, 0, 0, 4],
        [1, 4, 0, 0, 8, 0, 5, 0, 3],
        [0, 0, 0, 8, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 9, 0, 0],
        [0, 2, 0, 0, 6, 5, 0, 0, 0],
    ]
    puzzle = Puzzle(grid)
    # solve everything until we get to the multiple lines strategy
    strategies = []
    for strategy in STRATEGIES:
        if strategy.__name__ == "multiple_lines":
            break
        strategies.append(strategy)
    assert puzzle.solve(strategies=strategies) == False, "Puzzle should not be solved"

    status_before = []
    for cell in puzzle.cells:
        if cell.value == 0:
            status_before.append(
                f"cell r{cell.row_id + 1}c{cell.col_id + 1}: {cell.markup}"
            )

    assert puzzle.solve_step() == True, "Puzzle should make progress"

    status_after = []
    for cell in puzzle.cells:
        if cell.value == 0:
            status_after.append(
                f"cell r{cell.row_id + 1}c{cell.col_id + 1}: {cell.markup}"
            )
    # print differences
    differences = []
    for before, after in zip(status_before, status_after):
        if before != after:
            differences.append(f"{before} -> {after}")

    # It should find
    assert len(differences) == 1, "Puzzle should make one updates"
    assert differences[0] == "cell r3c3: {3, 9} -> cell r3c3: {9}"
