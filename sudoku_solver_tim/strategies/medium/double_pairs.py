from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle
import logging
from itertools import combinations


def double_pairs(p: "Puzzle", digits: list[int] | None = None) -> bool:
    """
    Applies the double pairs strategy.

    Strategy explanation:
    When a digit can only appear in the same two lines (rows or columns) in two blocks
    of a row or column of blocks, then that digit cannot appear in those same lines
    in the third block of that row/column.

    Example:
    If digit 2 can only appear in columns 4 and 6 in both the top-middle and middle-middle blocks,
    then any 2s in the bottom-middle block that are in columns 4 and 6 can be eliminated.

    See:
    - https://www.sudokuoftheday.com/techniques/double-pairs

    Args:
        p (Puzzle): The puzzle to solve.
        digits (list[int] | None): The digits to check. If None, all digits will be checked.

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_count = 0

    # Process each candidate digit
    for digit in digits or range(1, 10):
        # Check all block rows
        for block_row in p.blockrows:
            updates_count += _check_block_group(block_row.blocks, digit, is_row=True)

        # Check all block columns
        for block_col in p.blockcolumns:
            updates_count += _check_block_group(block_col.blocks, digit, is_row=False)

    # Update puzzle metadata if changes were made
    if updates_count > 0:
        logging.debug(f"Double pairs strategy removed {updates_count} candidates")
        p.strategies_used.add("Double Pairs")

    return updates_count > 0


def _check_block_group(blocks, digit, is_row=True):
    """
    Check a group of 3 blocks (in a row or column) for the double pairs pattern.

    Args:
        blocks: List of 3 blocks in a row or column
        digit: The digit to check
        is_row: Whether the blocks are in a row (True) or column (False)

    Returns:
        int: Number of candidates removed
    """
    updates = 0

    # For each pair of blocks in the group
    # Get all unique pairs of blocks using combinations
    for block1, block2 in combinations(blocks, 2):
        # Get cells that can contain the digit in each block
        cells1 = [c for c in block1.cells if digit in c.markup]
        cells2 = [c for c in block2.cells if digit in c.markup]

        # Skip if either block doesn't have the digit as a candidate
        if not cells1 or not cells2:
            continue

        # Double pairs will have only two cells in each block that can contain the digit
        if len(cells1) != 2 or len(cells2) != 2:
            continue

        # Find the lines (rows or columns) the digit appears in for each block
        if is_row:
            lines1 = {c.row.id for c in cells1}
            lines2 = {c.row.id for c in cells2}
        else:
            lines1 = {c.column.id for c in cells1}
            lines2 = {c.column.id for c in cells2}

        # If both blocks restrict the digit to the same two lines
        # And their are two lines (rows or columns)
        if lines1 == lines2 and len(lines1) == 2:
            # if digit == 2 and not is_row:
            #     import pdb; pdb.set_trace()
            # Remove the digit from cells in the third block that are in those lines
            third_block = [b for b in blocks if b != block1 and b != block2][0]
            cells3 = [c for c in third_block.cells if digit in c.markup]
            for cell in cells3:
                line_id = cell.row.id if is_row else cell.column.id
                if line_id in lines1:
                    if cell.remove_markup(digit):
                        logging.debug(
                            f"Double pairs: Removed {digit} from cell at r{cell.row_id + 1}c{cell.col_id + 1}"
                        )
                        updates += 1

    return updates
