from sudoku_solver.strategies.easy.single_candidates import single_candidates
from sudoku_solver.strategies.easy.single_position import single_position
from sudoku_solver.strategies.medium.candidate_lines import candidate_lines 
from sudoku_solver.strategies.medium.double_pairs import double_pairs 
from sudoku_solver.strategies.medium.multiple_lines import multiple_lines
from sudoku_solver.strategies.advanced.naked_pairs import naked_pairs
from sudoku_solver.strategies.advanced.naked_triplets import naked_triplets
from sudoku_solver.strategies.advanced.naked_quads import naked_quads
# from sudoku_solver.strategies.advanced.naked_subset import naked_subset
# from sudoku_solver.strategies.advanced.hidden_subset import hidden_subset

__all__ = ["single_candidates","single_position","candidate_lines","double_pairs","naked_pairs","naked_triplets","naked_quads","multiple_lines"]

# List of strategies in order of complexity, from simple to advanced
STRATEGIES = [
    single_candidates,
    single_position,
    candidate_lines,
    double_pairs,
    multiple_lines,
    naked_pairs,
    naked_triplets,
    naked_quads,
    # naked_subset,
    # hidden_subset,
]