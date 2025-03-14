from sudoku_solver.strategies.easy.single_candidates import single_candidates
from sudoku_solver.strategies.easy.single_position import single_position
from sudoku_solver.strategies.medium.candidate_lines import candidate_lines 
from sudoku_solver.strategies.medium.double_pairs import double_pairs 
from sudoku_solver.strategies.medium.multiple_lines import multiple_lines
from sudoku_solver.strategies.advanced.naked_pairs import naked_pairs
from sudoku_solver.strategies.advanced.naked_triples import naked_triples
from sudoku_solver.strategies.advanced.naked_quads import naked_quads
from sudoku_solver.strategies.advanced.hidden_pairs import hidden_pairs
from sudoku_solver.strategies.advanced.hidden_triples import hidden_triples
from sudoku_solver.strategies.advanced.hidden_quads import hidden_quads

__all__ = ["single_candidates","single_position","candidate_lines","double_pairs","naked_pairs","naked_triples","naked_quads","hidden_pairs","multiple_lines","hidden_triples","hidden_quads"]

# List of strategies in order of complexity, from simple to advanced
STRATEGIES = [
    single_candidates,
    single_position,
    candidate_lines,
    double_pairs,
    multiple_lines,
    naked_pairs,
    naked_triples,
    naked_quads,
    hidden_pairs,
    hidden_triples,
    hidden_quads,
]