import json
import pytest
from sudoku_solver.puzzle import Puzzle
from sudoku_solver.strategies import STRATEGY_NAMES
import os

def read_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    

def read_all_json_files_in_directory(directory):
    examples = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            examples.extend(read_from_json(filepath))
    return examples

EXAMPLES = read_all_json_files_in_directory("tests/fixtures")

levels = ['beginner','easy','medium','tricky','fiendish','diabolical']
for level in levels:
    unique_strategies = {strategy for ex in EXAMPLES if level in ex['url'] for strategy in ex['strategies']}
    print(f"{level}: {unique_strategies}")



@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'beginner' in ex['url']])
def test_beginner_examples(strategies, puzzle, url):
    p = Puzzle(puzzle)
    # Constrain strategies to only the ones in the strategies list
    p.solve(strategies=[STRATEGY_NAMES[s] for s in strategies])
    assert p.is_solved()
    assert p.strategies_used == set(strategies)

@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'easy' in ex['url']])
def test_easy_examples(strategies, puzzle, url):
    p = Puzzle(puzzle)
    p.solve(strategies=[STRATEGY_NAMES[s] for s in strategies])
    assert p.is_solved()
    assert p.strategies_used == set(strategies)

@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'medium' in ex['url']])
def test_medium_examples(strategies, puzzle, url):
    p = Puzzle(puzzle)
    p.solve(strategies=[STRATEGY_NAMES[s] for s in strategies])
    assert p.is_solved()
    assert p.strategies_used == set(strategies)

@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'tricky' in ex['url']])
def test_tricky_examples(strategies, puzzle, url):
    p = Puzzle(puzzle)
    p.solve(strategies=[STRATEGY_NAMES[s] for s in strategies])
    assert p.is_solved()
    assert set(p.strategies_used).issubset(set(strategies))


@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'fiendish' in ex['url']])
def test_fiendish_examples(strategies, puzzle, url):
    p = Puzzle(puzzle)
    p.solve(strategies=[STRATEGY_NAMES[s] for s in strategies])
    assert p.is_solved()
    assert set(p.strategies_used).issubset(set(strategies))

@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'diabolical' in ex['url']])
def test_diabolical_examples(strategies, puzzle, url):
    if any(s in strategies for s in ['Swordfish','Forcing Chains']):
        pytest.skip("Swordfish and Forcing Chains strategy is not implemented")
    p = Puzzle(puzzle)
    p.solve(strategies=[STRATEGY_NAMES[s] for s in strategies])
    assert p.is_solved()
    assert set(p.strategies_used).issubset(set(strategies))
