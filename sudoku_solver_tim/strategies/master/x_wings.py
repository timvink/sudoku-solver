from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle

from itertools import combinations
import logging


def x_wings(p: "Puzzle", digits: list[int] | None = None) -> bool:
    """
    Applies X-Wings strategy.

    See: https://www.sudokuoftheday.com/techniques/x-wings

    An X-Wing occurs when there are two lines (rows or columns) that have the same two positions
    for a number, forming an X pattern. This allows us to eliminate that number from other cells
    in the columns/rows that form the X.

    The key insight is that whichever position the number occupies in one line, it must occupy
    the opposite position in the other line, forming an X. This means we can eliminate that
    number from all other cells in the columns/rows that form the X.

    Returns:
        bool: Whether 1 or more cells have been updated.
    """
    updates_found = False

    # Check both rows and columns for X-Wings
    update_found = 1
    while update_found > 0:
        row_xwing_found = _find_x_wing_in_lines(p, digits, "rows")
        col_xwing_found = _find_x_wing_in_lines(p, digits, "columns")
        update_found = (row_xwing_found + col_xwing_found) > 0
        if update_found > 0:
            updates_found = True

    if updates_found:
        p.strategies_used.add("X-Wings")
        return True

    return False


def _find_x_wing_in_lines(
    p: "Puzzle",
    digits: list[int] | None = None,
    line_type: Literal["rows", "columns", "blocks"] = "rows",
) -> int:
    """
    Find X-Wings in lines and eliminate candidates from other lines.

    Args:
        p: The puzzle to solve
        digits: The digits to check for X-Wings
        line_type: The type of lines to check for X-Wings

    Returns:
        int: Number of cells updated
    """
    updates_found = 0

    # For each candidate number
    for num in digits or range(1, 10):
        lines_with_two_cells_with_digit = []
        for line in p.get_lines(line_type):
            cells = [cell for cell in line.cells if num in cell.markup]
            if len(cells) == 2:
                lines_with_two_cells_with_digit.append(line)

        # Check each pair of lines
        for line1, line2 in combinations(lines_with_two_cells_with_digit, 2):
            # Find cells in each line that contain this number
            cells1 = [cell for cell in line1.cells if num in cell.markup]
            cells2 = [cell for cell in line2.cells if num in cell.markup]

            # both lines should have exactly two cells with this number
            assert len(cells1) == 2 and len(cells2) == 2

            # If rows, get the column indices
            if line_type == "rows":
                x_line_1 = {cell.col_id for cell in cells1}
                x_line_2 = {cell.col_id for cell in cells2}
            # If columns, get the row indices
            elif line_type == "columns":
                x_line_1 = {cell.row_id for cell in cells1}
                x_line_2 = {cell.row_id for cell in cells2}
            else:
                raise ValueError(f"Invalid line type: {line_type}")

            # If the cross columns/rows match, we found an X-Wing
            if x_line_1 == x_line_2:
                # Get the cells that form the X-Wing
                x_wing_cells = cells1 + cells2

                # Remove this number from other cells in these columns
                for cell in cells1:
                    if line_type == "rows":
                        other_line = cell.column
                    elif line_type == "columns":
                        other_line = cell.row
                    else:
                        raise ValueError(f"Invalid line type: {line_type}")

                    for other_cell in [
                        c
                        for c in other_line.cells
                        if c not in x_wing_cells and not c.is_solved
                    ]:
                        if other_cell.remove_markup(num):
                            updates_found += 1
                            logging.debug(
                                f"X-Wing in rows: removed {num} from cell ({other_cell.row_id}, {other_cell.col_id})"
                            )

                # If we made any updates, we need to re-run the strategy from the start
                if updates_found > 0:
                    return updates_found

    return updates_found
