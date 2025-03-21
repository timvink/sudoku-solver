import os
import logging

# Configure logging based on environment variable
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from sudoku_solver_tim.puzzle import Puzzle

__all__ = ["Puzzle"]