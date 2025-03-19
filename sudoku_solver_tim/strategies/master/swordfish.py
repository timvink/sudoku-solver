from typing import TYPE_CHECKING, Literal, Optional

if TYPE_CHECKING:
    from sudoku_solver_tim.puzzle import Puzzle, Cell

import logging


def swordfish(p: "Puzzle", digits: list[int] | None = None) -> bool:
    """
    Applies Swordfish strategy.

    See: https://www.sudokuoftheday.com/techniques/swordfish
    """
    updates_found = False

    # Check both rows and columns for Swordfish
    update_found = 1
    while update_found > 0:
        update_found_rows = _find_swordfish_in_lines(p, line_type="rows", digits=digits)
        update_found_columns = _find_swordfish_in_lines(
            p, line_type="columns", digits=digits
        )
        update_found = (update_found_rows + update_found_columns) > 0
        if update_found > 0:
            updates_found = True

    if updates_found:
        p.strategies_used.add("Swordfish")
        return True

    return updates_found


def _find_swordfish_in_lines(
    p: "Puzzle",
    digits: list[int] | None = None,
    line_type: Literal["rows", "columns", "blocks"] = "rows",
) -> bool:
    """
    Find Swordfish in lines and eliminate candidates from other lines.

    Note, we did not implement this strategy in blocks.

    Args:
        p: The puzzle to solve
        digits: The digits to check for Swordfish
        line_type: The type of lines to check for Swordfish
    """
    if line_type == "rows":
        lines = p.rows
    elif line_type == "columns":
        lines = p.columns
    else:
        raise ValueError(f"Invalid line type: {line_type}")

    # For each candidate number
    for num in digits or range(1, 10):
        # We need to find lines with two cells with the candidate number.
        cell_pairs = []
        for line in p.get_lines(line_type):
            cells = [cell for cell in line.cells if num in cell.markup]
            # We need to have two cells, so one 'forces' the other.
            if len(cells) == 2:
                cell_pairs.append(cells)

        # We need at least 3 lines to have a swordfish. Because 2 would be an X-wing.
        if len(cell_pairs) < 3:
            continue

        # We need to cell to be linked to another pair cell via the cross line (column or row)
        candidate_cells = flatten_list_of_lists(cell_pairs)
        valid_candidate_cells = []
        for cell in candidate_cells:
            other_cell = _find_linked_cell(cell, cell_pairs, line_type)
            if other_cell:
                valid_candidate_cells.append(cell)
        cell_pairs = [
            cell_pair
            for cell_pair in cell_pairs
            if all(c in valid_candidate_cells for c in cell_pair)
        ]

        # We need at least 3 lines to have a swordfish. Because 2 would be an X-wing.
        if len(cell_pairs) < 3:
            continue

        logging.debug(
            f"Looking for swordfish in {len(cell_pairs)} lines of type {line_type}. Considering pairs of '{num}'"
        )

        assert all(len(cell_pair) == 2 for cell_pair in cell_pairs)

        # We need to check if there is a closed loop.
        # We start with the first line and the first cell.
        first_cell = cell_pairs[0][0]
        current_cell = first_cell
        linked = False
        cells_in_chain = [first_cell]

        while True:
            current_cell = _find_linked_cell(
                current_cell, cell_pairs, line_type=line_type
            )

            if current_cell is None:
                break
            cells_in_chain.append(current_cell)
            # find the pair of the current cell
            for cell_pair in cell_pairs:
                if current_cell in cell_pair:
                    current_cell = (
                        cell_pair[0] if cell_pair[1] == current_cell else cell_pair[1]
                    )
            # if we have returned to the first cell, we have a closed loop cycle
            if current_cell == first_cell:
                linked = True
                break
            cells_in_chain.append(current_cell)

        if linked:
            # We have found a swordfish!
            logging.debug(f"Swordfish in {line_type}: found a swordfish with {num}")
            # Remove candidates
            for cell in cells_in_chain:
                # If we were looking at rows, we need to eliminate from columns, and vice versa
                line = cell.column if line_type == "rows" else cell.row
                update_cells = [c for c in line.cells if c not in cells_in_chain]
                for update_cell in update_cells:
                    if update_cell.remove_markup(num):
                        logging.debug(
                            f"Swordfish in {line_type}: removed {num} from cell ({update_cell.row_id}, {update_cell.col_id})"
                        )
                        return True

    return False


def _find_linked_cell(
    cell: "Cell", cell_pairs: list[list["Cell"]], line_type: Literal["rows", "columns"]
) -> Optional["Cell"]:
    """
    Find a cell that is linked to the given cell and is not in the list of other cells.

    When we are looking at the row lines, the links should be across columns.
    When we are looking at the column lines, the links should be across rows.
    """
    # Flatten the list of cell pairs

    other_cells = flatten_list_of_lists(cell_pairs)
    other_cells = [c for c in other_cells if c != cell]

    if line_type == "rows":
        other_cell = [c for c in other_cells if c.column.id == cell.column.id]
    elif line_type == "columns":
        other_cell = [c for c in other_cells if c.row.id == cell.row.id]
    else:
        raise ValueError(f"Invalid line type: {line_type}")

    return other_cell[0] if other_cell else None


def flatten_list_of_lists(xss):
    return [x for xs in xss for x in xs]
