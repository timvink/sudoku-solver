from rich.panel import Panel
from rich.console import Console
from rich.layout import Layout
from rich.table import Table
from rich.align import Align
from rich import box

from typing import List, Callable, Literal

from functools import lru_cache
from itertools import chain

from sudoku_solver_tim.strategies import STRATEGIES

console = Console()
layout = Layout()
from rich.text import Text


class Cell:
    def __init__(
            self,
            value,
            row_id,
            col_id,
            block,
            row,
            column,
            blockrow,
            blockcolumn,
            puzzle = None, # for debugging
        ) -> None:
        self.value = value
        self.row_id = row_id
        self.col_id = col_id

        self.block = block or Block(0)
        self.row = row or Row(0)
        self.column = column or Column(0)
        self.blockrow = blockrow or BlockRow(0, [])
        self.blockcolumn = blockcolumn or BlockColumn(0, [])
        self.puzzle = puzzle or None # for debugging
        
        self.markup: set = set(range(1,10)) if value == 0 else set()

    def __repr__(self) -> str:
        return f"Cell(value={self.value}, row_id={self.row_id}, col_id={self.col_id})"

    @property
    def is_solved(self):
        return self.value != 0

    def set_solution(self, value):

        # Validate that value is not the solution of any other cell in the same row, column and block.
        cells_to_update = chain(self.row.cells, self.column.cells, self.block.cells)
        cells_to_update = [c for c in cells_to_update if c != self]
        for o in cells_to_update:
            assert o.value != value
        
        # Update the value and markup
        self.value = value
        self.markup = set()

        # Remove the value from the markup of all other cells in the same row, column and block.
        for o in cells_to_update:
            o.remove_markup(self.value)

        return self

    def remove_markup(self, value: set[int] | list[int] | int):
        if isinstance(value, int):
            value = [value]
        updates = False
        for v in value:
            if v not in self.markup:
                continue
            if len(self.markup) == 1:
                raise Exception(f"Removing last markup value {v} from cell row {self.row_id+1}, column {self.col_id+1}")
            updates = True
            self.markup.remove(v)
        return updates
    
    
    def show_markup(self, highlight: int | None = None):
        """
        Return printable markup status.
        """
        if self.value != 0:
            return Panel(Align(Text(str(self.value), justify="center", style="bold"), align="center", vertical="middle"), height=5, width=9)
        cell = Table(show_header=False, box=None, collapse_padding=True, pad_edge=False, show_edge=False)

        def v(value):
            return str(value) if value in self.markup else ""
        
        cell.add_row(v(1), v(2), v(3))
        cell.add_row(v(4), v(5), v(6))
        cell.add_row(v(7), v(8), v(9))
        color = "#b76e79" if highlight not in self.markup else "#FFD700"
        return Panel(cell, style=color)

    
    def show_value(self):
        text = Text(str(self.value) if self.value != 0 else " ", justify="center", style="on green")
        return text

class Group:
    """
    BaseClass for a container holding 9 cells.
    """
    def __init__(self, id) -> None:
        self.id = id
        self.cells = []

    @property
    def unsolved_values(self):
        """
        Return set of unsolved values across the 9 cells.
        """
        unsolved_values = set()
        for cell in self.cells:
            unsolved_values.update(cell.markup)
        return unsolved_values
    
    def __iter__(self):
        """
        Return an iterator over the cells.

        So you can do `for cell in group`.
        """
        return iter(self.cells)

    @property
    @lru_cache
    def rows(self):
        assert len(self.cells) > 0
        return sorted(list(set([c.row for c in self.cells])), key=lambda row: row.id)
    
    @property
    @lru_cache
    def columns(self):
        assert len(self.cells) > 0
        return sorted(list(set([c.column for c in self.cells])), key=lambda column: column.id)

    @property
    @lru_cache
    def blocks(self):
        assert len(self.cells) > 0
        return sorted(list(set([c.block for c in self.cells])), key=lambda block: block.id)


class Block(Group):
    id: int

    @property
    @lru_cache
    def blockrow(self):
        # Which blockrow is this block part of?
        assert len(set([c.blockrow for c in self.cells])) == 1
        return [c.blockrow for c in self.cells][0]
    
    @property
    @lru_cache
    def blockcolumn(self):
        # Which blockcolumn is this block part of?
        assert len(set([c.blockcolumn for c in self.cells])) == 1
        return [c.blockcolumn for c in self.cells][0]

    @property
    @lru_cache
    def other_blocks_in_row(self):
        other_blocks_in_row = [b for b in self.blockrow.blocks if b != self]
        assert len(other_blocks_in_row) == 2
        return other_blocks_in_row
    
    @property
    @lru_cache
    def other_blocks_in_column(self):
        other_blocks_in_column = [b for b in self.blockcolumn.blocks if b != self]
        assert len(other_blocks_in_column) == 2
        return other_blocks_in_column

    def show_values(self):
        # block = Table(show_header=False, width=18, box=box.HEAVY_EDGE, collapse_padding=False, pad_edge=False, padding=False, show_edge=True, show_lines=True)
        block = Table.grid(padding=0)
        block.box = box.HEAVY_EDGE
        block.show_lines=True
        block.show_edge=True
        block.add_row(self.cells[0].show_value(), self.cells[1].show_value(), self.cells[2].show_value())
        block.add_row(self.cells[3].show_value(), self.cells[4].show_value(), self.cells[5].show_value())
        block.add_row(self.cells[6].show_value(), self.cells[7].show_value(), self.cells[8].show_value())
        
        for c in block.columns:
            c.justify = 'center'
            c.width = 3

        return block

    def show_markup(self, highlight: int | None = None):
        # block = Table(show_header=False, box=None, collapse_padding=True, pad_edge=False, show_edge=False)
        block = Table.grid(expand=True, collapse_padding=False)
        block.add_row(self.cells[0].show_markup(highlight), self.cells[1].show_markup(highlight), self.cells[2].show_markup(highlight))
        block.add_row(self.cells[3].show_markup(highlight), self.cells[4].show_markup(highlight), self.cells[5].show_markup(highlight))
        block.add_row(self.cells[6].show_markup(highlight), self.cells[7].show_markup(highlight), self.cells[8].show_markup(highlight))
        for c in block.columns:
            c.width = 9
            c.no_wrap = True
        from rich import box
        return Panel(block, box=box.MINIMAL)
    
    def __repr__(self):
        table = Table(show_header=False, box=None, padding=0, show_edge=False, leading=0)
        # v = 

        def v(value):
            if value == self.id:
                return Panel(Align(Text(str(self.id), justify="center", style="bold"), align="center", vertical="middle"), height=5, width=9, style="#FFD700")
            else:
                return Panel(Align(Text(str(value), justify="center", style="gray"), align="center", vertical="middle"), height=5, width=9)
        
        table.add_row(v(0), v(1), v(2))
        table.add_row(v(3), v(4), v(5))
        table.add_row(v(6), v(7), v(8))
        table.padding = (0, 1, 0, 0)
        console.print(table)
        return f"Block(id={self.id})"


class Row(Group):

    @property
    @lru_cache
    def blockrows(self):
        assert len(self.blocks) == 3
        blockrows = sorted(list(set([c.blockrow for c in self.cells])), key=lambda blockrow: blockrow.id)
        assert len(blockrows) == 1
        return blockrows

class Column(Group):

    @property
    @lru_cache
    def blockrows(self):
        assert len(self.blocks) == 3
        blockcolumns = sorted(list(set([c.blockcolumn for c in self.cells])), key=lambda blockcolumn: blockcolumn.id)
        assert len(blockcolumns) == 1
        return blockcolumns


class BlockRow:
    def __init__(self, id, blocks) -> None:
        self.id = id
        self.cells = []
        self.blocks = blocks

    @property
    def rows(self):
        # Rows that are part of this blockrow
        return self.blocks[0].rows
    

class BlockColumn:
    def __init__(self, id, blocks) -> None:
        self.id = id
        self.cells = []
        self.blocks = blocks

    @property
    def columns(self):
        # Columns that are part of this blockcolumn
        return self.blocks[0].columns


class Puzzle:
    """
    Sudoku Puzzle.

    example usage:

    ```python
    from sudoku_solver.puzzle import Puzzle
    puzzle = Puzzle()
    puzzle
    ```
    """

    @classmethod
    def from_string(cls, string: str) -> "Puzzle":
        """
        Often sukodu's come in the form of a string with . or 0 to indicate an empty cell.

        Example:

        ```
        string = "2.48........7.5....13.....9..7.......26....3.3...26.4...9..845.87.....16....6.2.."
        puzzle = Puzzle.from_string(string)
        ```

        Args:
            string: A string of 81 characters representing a sudoku puzzle.

        Returns:
            A Puzzle object.
        """
        grid = [int(c) if c != "." else 0 for c in string]
        grid = [grid[i:i+9] for i in range(0, len(grid), 9)]
        return cls(grid)
    
    def __init__(self, grid: List[List[int]]) -> None:
        self._grid = grid

        self.strategies_used = set()
        self.cells = []
        self.blocks = [Block(id) for id in range(9)]
        self.rows = [Row(id) for id in range(9)]
        self.columns = [Column(id) for id in range(9)]
       
        # Add BlockRows and BlockColumns
        # Basically a 3x3 grid of blocks
        self.blockrows = [
            BlockRow(0, [self.blocks[0],self.blocks[1],self.blocks[2]]),
            BlockRow(1, [self.blocks[3],self.blocks[4],self.blocks[5]]),
            BlockRow(2, [self.blocks[6],self.blocks[7],self.blocks[8]])
        ]
        self.blockcolumns = [
            BlockColumn(0, [self.blocks[0],self.blocks[3],self.blocks[6]]),
            BlockColumn(1, [self.blocks[1],self.blocks[4],self.blocks[7]]),
            BlockColumn(2, [self.blocks[2],self.blocks[5],self.blocks[8]])
        ]

        # Create the cells
        for row_id, row in enumerate(self._grid):
            for col_id, value in enumerate(row):

                # Calculate the block_id (blocks 0-8 from top left to bottom right)
                block_id = (row_id // 3) * 3 + (col_id // 3)
                blockrow_id = row_id // 3
                blockcolumn_id = col_id // 3

                cell = Cell(
                    value=value,
                    row_id=row_id,
                    col_id=col_id,
                    block=self.blocks[block_id],
                    row=self.rows[row_id],
                    column=self.columns[col_id],
                    blockrow=self.blockrows[blockrow_id],
                    blockcolumn=self.blockcolumns[blockcolumn_id],
                    puzzle=self
                )
                self.cells.append(cell)

                self.blocks[block_id].cells.append(cell)
                self.rows[row_id].cells.append(cell)
                self.columns[col_id].cells.append(cell)
                self.blockrows[blockrow_id].cells.append(cell)
                self.blockcolumns[blockcolumn_id].cells.append(cell)

        # Update the cells
        for cell in self.cells:
            # for debugging
            cell.puzzle = self
            # Update the solved cells
            if cell.value != 0:
                cell.set_solution(cell.value)

    @property
    def grid(self):
        return [[c.value or 0 for c in row.cells] for row in self.rows]
    
    def solve(self, strategies: List[Callable] | None = None):
        """
        Solve the puzzle using the given strategies.

        Strategies are functions that take a Puzzle as input and return a boolean.

        Args:
            strategies: List of strategies to use. If no strategies are given, all strategies will be used.

        Returns:
            True if the puzzle is solved, False otherwise.
        """
        if strategies is None:
            strategies = STRATEGIES
        # Ensure the right order of strategies
        strategies = [s for s in STRATEGIES if s in strategies]

        # Keep trying strategies until the puzzle is solved
        # Note each strategy will repeat itself until no more cells are solved
        # If a strategy solves at least one cell, and it done with repeating, we move back to the first strategy
        while not self.is_solved():
            # Try each strategy in order of complexity
            for strategy in strategies:
                if strategy(self):
                    break  # If strategy made progress, break out of for loop to restart from first strategy
            else:  # If no strategy made any progress
                break  # Break out of while loop as no progress can be made

        if self.is_solved():
            self.validate()
            return True
        else:
            return False

    def solve_step(self, strategies: List[Callable] | None = None):
        """
        Solve the puzzle using the first strategy that makes progress.
        """
        if strategies is None:
            strategies = STRATEGIES
        # Ensure the right order of strategies
        strategies = [s for s in STRATEGIES if s in strategies]

        for strategy in strategies:
            if solved_cells := strategy(self):
                console.print(f"Made progress using {strategy.__name__}")
                return solved_cells
        return False

    def is_solved(self):
        if not all([c.value != 0 for c in self.cells]):
            return False
        self.validate()
        return True

    def validate(self):
        """
        The solution of a Sudoku puzzle requires that every row, column, and box contain all the numbers in the set
        [1, 2, . . . , 9] and that every cell be occupied by one
        and only one number.
        """
        for group in chain(self.blocks, self.rows, self.columns):
            solutions = [c.value for c in group.cells]
            if not sorted(solutions) == list(range(1,10)):
                raise Exception("Invalid puzzle solution.")

    def get_lines(self, type: Literal["rows", "columns", "blocks"]):
        if type == "rows":
            return self.rows
        elif type == "columns":
            return self.columns
        elif type == "blocks":
            return self.blocks
        else:
            raise ValueError(f"Invalid type: {type}")
    
    def _get_cell(self, row_id, col_id):
        """for debugging"""
        return [c for c in self.cells if c.row_id == row_id and c.col_id == col_id][0]

    def show_markup(self, highlight: int | None = None):
        from rich import box
        table = Table(show_header=False, show_lines=True, box=box.MINIMAL, collapse_padding=False, pad_edge=False, show_edge=True)
        table.add_row(self.blocks[0].show_markup(highlight), self.blocks[1].show_markup(highlight), self.blocks[2].show_markup(highlight))
        table.add_row(self.blocks[3].show_markup(highlight), self.blocks[4].show_markup(highlight), self.blocks[5].show_markup(highlight))
        table.add_row(self.blocks[6].show_markup(highlight), self.blocks[7].show_markup(highlight), self.blocks[8].show_markup(highlight))
    
        console.print(table)


    def __repr__(self):
        table = Table(show_header=False, box=None, padding=0, show_edge=False, leading=0)
        table.add_row(self.blocks[0].show_values(), self.blocks[1].show_values(), self.blocks[2].show_values())
        table.add_row(self.blocks[3].show_values(), self.blocks[4].show_values(), self.blocks[5].show_values())
        table.add_row(self.blocks[6].show_values(), self.blocks[7].show_values(), self.blocks[8].show_values())

        table.padding = (0, 1, 0, 0)
        console.print(table)
        return ""
