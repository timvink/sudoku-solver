[![Actions Status](https://github.com/timvink/sudoku-solver/actions/workflows/unit_test.yml/badge.svg)](https://github.com/timvink/sudoku-solver/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sudoku-solver-tim)
![PyPI](https://img.shields.io/pypi/v/sudoku-solver-tim)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sudoku-solver-tim)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/sudoku-solver-tim)
![PyPI - License](https://img.shields.io/pypi/l/sudoku-solver-tim)

# Sudoku solver

This is a sudoku solver that helps you solve sudoku puzzles by showing you the easiest possible strategy required to solve the puzzle.

## Setup

Install the package:

```bash
pip install sudoku-solver-tim
```

## Usage

```python
from sudoku_solver_tim import Puzzle

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

# Find the easiest strategy to make progress (remove a pencil mark)
puzzle.solve_step()
#> Made progress using candidate_lines

# Solve the puzzle using all strategies
puzzle.solve()
puzzle.strategies_used
# {'Candidate Lines', 'Single Candidate'}

puzzle
#> ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ 
#> ┃ 2 │ 8 │ 1 ┃ ┃ 9 │ 5 │ 7 ┃ ┃ 4 │ 6 │ 3 ┃ 
#> ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
#> ┃ 4 │ 3 │ 5 ┃ ┃ 8 │ 2 │ 6 ┃ ┃ 9 │ 7 │ 1 ┃ 
#> ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
#> ┃ 7 │ 6 │ 9 ┃ ┃ 1 │ 3 │ 4 ┃ ┃ 8 │ 2 │ 5 ┃ 
#> ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ 
#> ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ 
#> ┃ 8 │ 4 │ 7 ┃ ┃ 2 │ 6 │ 1 ┃ ┃ 3 │ 5 │ 9 ┃ 
#> ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
#> ┃ 3 │ 1 │ 2 ┃ ┃ 4 │ 9 │ 5 ┃ ┃ 7 │ 8 │ 6 ┃ 
#> ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
#> ┃ 9 │ 5 │ 6 ┃ ┃ 3 │ 7 │ 8 ┃ ┃ 2 │ 1 │ 4 ┃ 
#> ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ 
#> ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ 
#> ┃ 1 │ 2 │ 8 ┃ ┃ 6 │ 4 │ 9 ┃ ┃ 5 │ 3 │ 7 ┃ 
#> ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
#> ┃ 5 │ 9 │ 3 ┃ ┃ 7 │ 1 │ 2 ┃ ┃ 6 │ 4 │ 8 ┃ 
#> ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
#> ┃ 6 │ 7 │ 4 ┃ ┃ 5 │ 8 │ 3 ┃ ┃ 1 │ 9 │ 2 ┃ 
#> ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ 
```

## Backlog

We could add additional strategies to the solver.

- Y-wings https://sudoku.com/sudoku-rules/y-wing/
- Forcing Chains: https://www.sudokuoftheday.com/techniques/forcing-chains
- Explicit separate the Swordfish-3 and Swordfish-4 strategies, as Swordfish-4 is sometimes called "Jellyfish"