[![Actions Status](https://github.com/timvink/sudoku-solver/actions/workflows/unit_test.yml/badge.svg)](https://github.com/timvink/sudoku-solver/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sudoku-solver-tim)
![PyPI](https://img.shields.io/pypi/v/sudoku-solver-tim)
![PyPI - License](https://img.shields.io/pypi/l/sudoku-solver-tim)

# Sudoku solver

This is a sudoku solver that helps you solve sudoku puzzles by showing you the easiest possible strategy required to solve the puzzle.

If you're stuck on a sudoku puzzle, you can use this library to find out if you missed something obvious, or need to apply a more complex strategy to make progress.

See also my blogpost [Introducing an actually helpful sudoku solver](https://timvink.nl/blog/introducing-sudoku-solver/).

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

You can also create a puzzle from a string:

```python
string = "2.48........7.5....13.....9..7.......26....3.3...26.4...9..845.87.....16....6.2.."
puzzle = Puzzle.from_string(string)
puzzle.solve()
```

## Techniques implemented

The following techniques are implemented, in order of complexity:

Easy:
- [Single Candidates](https://www.sudokuoftheday.com/techniques/single-candidate)
- [Single Position](https://www.sudokuoftheday.com/techniques/single-position)

Medium:
- [Candidate Lines](https://www.sudokuoftheday.com/techniques/candidate-lines)
- [Double Pairs](https://www.sudokuoftheday.com/techniques/double-pairs)
- [Multiple Lines](https://www.sudokuoftheday.com/techniques/multiple-lines)

Advanced:
- [Naked Pairs](https://www.sudokuoftheday.com/techniques/naked-pairs-triples)
- [Naked Triples](https://www.sudokuoftheday.com/techniques/naked-pairs-triples)
- [Naked Quads](https://www.sudokuoftheday.com/techniques/naked-pairs-triples)
- [Hidden Pairs](https://www.sudokuoftheday.com/techniques/hidden-pairs-triples)
- [Hidden Triples](https://www.sudokuoftheday.com/techniques/hidden-pairs-triples)
- [Hidden Quads](https://www.sudokuoftheday.com/techniques/hidden-pairs-triples)

Master:
- [X-Wings](https://www.sudokuoftheday.com/techniques/x-wings)
- [Swordfish](https://www.sudokuoftheday.com/techniques/swordfish)
- `brute_force` (also known as "backtracking"). It will try all possible combinations and backtrack if there is a mistake. You could see this as a variant on the techniques [Forcing Chains](https://www.sudokuoftheday.com/techniques/forcing-chains), [Nishio](https://www.sudokuoftheday.com/techniques/nishio) and [Guessing](https://www.sudokuoftheday.com/techniques/guesswork).

Some remarks:

- We have not implemented [Y-wings](https://sudoku.com/sudoku-rules/y-wing/), although you do not need them given the other strategies.
- The implementation of `swordfish` included both Swordfish-3 and Swordfish-4. Swordfish-4 is sometimes called "Jellyfish", and could be a separate strategy.
- [Forcing Chains](https://www.sudokuoftheday.com/techniques/forcing-chains) is not guesswork/brute force, but it's a lot of hard work if you had to do it by hand.
