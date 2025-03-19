from sudoku_solver_tim.puzzle import Puzzle


def test_solving_sudokus():
    # Very easy puzzle that can be solved
    # with single candidates
    grid = [
        [2, 5, 0, 0, 3, 0, 9, 0, 1],
        [0, 1, 0, 0, 0, 4, 0, 0, 0],
        [4, 0, 7, 0, 0, 0, 2, 0, 8],
        [0, 0, 5, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 8, 1, 0, 0],
        [0, 4, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 3, 6, 0, 0, 7, 2],
        [0, 7, 0, 0, 0, 0, 0, 0, 3],
        [9, 0, 3, 0, 0, 0, 6, 0, 4],
    ]
    p = Puzzle(grid)
    p.solve()
    assert p.is_solved()
    assert p.strategies_used == {"Single Candidate"}

    # Easy puzzle.
    # https://www.sudokuoftheday.com/dailypuzzles/2022-07-08/easy
    # Required strategies: Single Candidate, Single Position
    easy_20220708 = [
        [0, 9, 0, 0, 0, 5, 0, 0, 8],
        [4, 0, 0, 0, 3, 0, 5, 0, 0],
        [3, 0, 0, 0, 0, 0, 1, 0, 6],
        [0, 0, 2, 0, 0, 9, 0, 0, 5],
        [8, 0, 5, 1, 4, 7, 9, 0, 2],
        [6, 0, 0, 5, 0, 0, 3, 0, 0],
        [1, 0, 6, 0, 0, 0, 0, 0, 9],
        [0, 0, 4, 0, 5, 0, 0, 0, 3],
        [5, 0, 0, 2, 0, 0, 0, 1, 0],
    ]
    p = Puzzle(easy_20220708)
    p.solve()
    assert p.is_solved()
    assert p.strategies_used == {"Single Candidate", "Single Position"}

    # Test adding candidate lines strategy.
    # Medium puzzle.
    # https://www.sudokuoftheday.com/dailypuzzles/2022-07-10/medium
    # Required strategies: single candidates, single position, candidate lines
    medium_20220710 = [
        [1, 0, 0, 5, 0, 3, 4, 0, 8],
        [0, 3, 0, 9, 0, 4, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 0, 3, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 9],
        [0, 2, 0, 8, 4, 1, 0, 6, 0],
        [3, 0, 0, 0, 0, 0, 0, 7, 0],
        [0, 4, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 2, 0, 6, 0, 4, 0],
        [2, 0, 3, 4, 0, 8, 0, 0, 1],
    ]
    p = Puzzle(medium_20220710)
    p.solve()
    assert p.is_solved()
    assert p.strategies_used == {
        "Single Candidate",
        "Single Position",
        "Candidate Lines",
    }

    # Test adding Naked Pairs strategy
    # Tricky puzzle
    # https://www.sudokuoftheday.com/dailypuzzles/2022-07-10/tricky
    # Required strategies: Single Position, Single Candidate, Candidate Lines, Naked Pairs
    tricky_20220710 = [
        [9, 6, 0, 0, 5, 0, 0, 0, 3],
        [0, 0, 4, 1, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 2, 0, 3, 6, 0, 0, 5],
        [0, 7, 0, 0, 0, 0, 0, 2, 0],
        [6, 0, 0, 7, 2, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 4, 7, 0, 0],
        [8, 0, 0, 0, 6, 0, 0, 5, 2],
    ]
    p = Puzzle(tricky_20220710)
    p.solve()
    # TODO: implement naked pairs
    # assert p.is_solved()
    # assert p.strategies_used == {'Single Candidate','Single Position','Candidate Lines','Naked Pairs'}

    # Test adding Hidden Pairs strategy
    # Tricky puzzle
    # https://www.sudokuoftheday.com/dailypuzzles/2022-07-12/tricky
    # Required strategies: Single Position, Single Candidate, Candidate Lines, Hidden Pairs
    tricky_20220712 = [
        [0, 8, 0, 0, 2, 0, 0, 0, 5],
        [0, 3, 6, 0, 0, 0, 8, 0, 0],
        [1, 0, 0, 8, 0, 0, 0, 3, 0],
        [0, 6, 0, 4, 0, 0, 0, 7, 8],
        [2, 0, 0, 0, 5, 0, 0, 0, 3],
        [8, 9, 0, 0, 0, 7, 0, 5, 0],
        [0, 4, 0, 0, 0, 9, 0, 0, 7],
        [0, 0, 7, 0, 0, 0, 3, 8, 0],
        [3, 0, 0, 0, 6, 0, 0, 4, 0],
    ]
    p = Puzzle(tricky_20220712)
    p.solve()
    # TODO: implement hidden pairs
    # assert p.is_solved()
    # assert p.strategies_used == {'Single Candidate','Single Position','Candidate Lines','Naked Triple'}
    # assert p.strategies_used == {'single candidates','single position','candidate lines','hidden pairs'}

    # Test adding double pairs strategy
    # Tricky puzzle
    # https://www.sudokuoftheday.com/dailypuzzles/2022-07-07/tricky
    # Single Position, Single Candidate, Candidate Lines, Double Pairs, Hidden Pairs
    tricky_20220707 = [
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 3, 0, 0],
        [3, 9, 0, 0, 0, 7, 0, 0, 6],
        [0, 0, 3, 1, 4, 0, 0, 0, 0],
        [0, 6, 0, 0, 9, 0, 0, 5, 0],
        [0, 0, 0, 0, 3, 2, 4, 0, 0],
        [1, 0, 0, 4, 0, 0, 0, 7, 8],
        [0, 0, 7, 0, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 9, 0, 0, 0],
    ]
    p = Puzzle(tricky_20220707)
    p.solve()
    # assert p.is_solved()
    # assert p.strategies_used == {'Single Candidate','Single Position','Candidate Lines','Naked Triple'}
    # assert "double pairs" in p.strategies_used

    # Finally,
    # test some of the diabolical sudoku's shown in
    # http://www.ams.org/notices/200904/rtx090400460p.pdf


# Empty grid
# [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]
