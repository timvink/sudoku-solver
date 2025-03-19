"""
Generated by chatGPT, prompt "write a sudoku solver in python"
"""

import os
import logging

# Configure logging based on environment variable
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


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


def print_grid(grid):
    for row in grid:
        logging.info(" ".join(str(num) if num != 0 else "." for num in row))


# Example Sudoku puzzle
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

logging.info("Sudoku puzzle:")
print_grid(sudoku_board)

if solve_sudoku(sudoku_board):
    logging.info("\nSolved Sudoku:")
    print_grid(sudoku_board)
else:
    logging.info("No solution exists")
