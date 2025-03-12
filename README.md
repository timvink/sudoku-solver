# Sudoku solver

This is a sudoku solver that helps you solve sudoku puzzles by showing you the easiest possible strategy required to solve the puzzle.

## Ideas

- scrape sudokuoftheday.com with gitscraper
- deploy webapp with optical camera recognition, and solver in Python via PyScript

## TODO

- Download more sudoku puzzles from sudokuoftheday.com for testing
- implement more strategies
- fix typing issues
- clear git history.

- for unit testing, limit the strategies allowed by solver to ensure other techniques are not used
- update the solver loop, because you use a technique as soon as you use it to remove a pencil mark, not only when you solve a cell!
