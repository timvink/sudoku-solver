from typing import TYPE_CHECKING, Literal, Optional, List

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle, Cell

import logging
import copy


def is_valid(board, row, col, num):
    # Check if 'num' is not in the current row, column and 3x3 subgrid
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        if board[row // 3 * 3 + i // 3][col // 3 * 3 + i % 3] == num:
            return False
    return True


def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def brute_force(puzzle: "Puzzle") -> bool:
    grid = copy.deepcopy(puzzle.grid)
    if solve_sudoku(grid):
        for row_id, row in enumerate(grid):
            for col_id, value in enumerate(row):
                puzzle.cells[row_id * 9 + col_id].set_solution(value)
        puzzle.strategies_used.add("Brute Force")
        return True
    return False
