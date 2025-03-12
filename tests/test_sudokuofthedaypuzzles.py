import json
import pytest
from sudoku_solver.puzzle import Puzzle
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

def test_one():
    ex = EXAMPLES[0]
    p = Puzzle(ex['puzzle'])
    p.solve()
    assert p.is_solved()
    assert p.strategies_used == set(ex['strategies'])


@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'beginner' in ex['url']])
def test_beginner_examples(strategies, puzzle, url):
    p = Puzzle(puzzle)
    p.solve()
    assert p.is_solved()
    assert p.strategies_used == set(strategies)

@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'easy' in ex['url']])
def test_easy_examples(strategies, puzzle, url):
    p = Puzzle(puzzle)
    p.solve()
    assert p.is_solved()
    assert p.strategies_used == set(strategies)

@pytest.mark.parametrize("strategies, puzzle, url", [(ex['strategies'], ex['puzzle'], ex['url']) for ex in EXAMPLES if 'medium' in ex['url']])
def test_medium_examples(strategies, puzzle, url):
    p = Puzzle(puzzle)
    p.solve()
    assert p.is_solved()
    assert p.strategies_used == set(strategies)
