from sudoku_solver.strategies.easy.single_candidates import single_candidates
from sudoku_solver.strategies.easy.single_position import single_position
from sudoku_solver.strategies.medium.candidate_lines import candidate_lines
from sudoku_solver.strategies.medium.double_pairs import double_pairs
from sudoku_solver.strategies.medium.multiple_lines import multiple_lines
from sudoku_solver.strategies.advanced.naked_pairs import naked_pairs
from sudoku_solver.strategies.advanced.hidden_pairs import hidden_pairs
from sudoku_solver.strategies.advanced.naked_triples import naked_triples
from sudoku_solver.strategies.advanced.hidden_triples import hidden_triples
from sudoku_solver.strategies.advanced.naked_quads import naked_quads
from sudoku_solver.strategies.advanced.hidden_quads import hidden_quads
from sudoku_solver.strategies.master.x_wings import x_wings

__all__ = [
    'single_candidates',
    'single_position',
    'candidate_lines',
    'double_pairs',
    'multiple_lines',
    'naked_pairs',
    'hidden_pairs',
    'naked_triples',
    'hidden_triples',
    'naked_quads',
    'hidden_quads',
    'x_wings',
]

# Strategies in order of complexity
STRATEGIES = [
    single_candidates,
    single_position,
    candidate_lines,
    double_pairs,
    multiple_lines,
    naked_pairs,
    hidden_pairs,
    naked_triples,
    hidden_triples,
    naked_quads,
    hidden_quads,
    x_wings,
]

STRATEGY_NAMES = {
    'Single Candidate': single_candidates,
    'Single Position': single_position,
    'Candidate Lines': candidate_lines,
    'Double Pairs': double_pairs,
    'Multiple Lines': multiple_lines,
    'Naked Pairs': naked_pairs,
    'Hidden Pairs': hidden_pairs,
    'Naked Triples': naked_triples,
    'Hidden Triples': hidden_triples,
    'Naked Quads': naked_quads,
    'Hidden Quads': hidden_quads,
    'X-Wings': x_wings,
}