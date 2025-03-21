"""
Run a benchmark on 2000 puzzles.

Run using:

```
uv run python scripts/benchmark_2k.py
```
"""
from sudoku_solver_tim.puzzle import Puzzle
import time
import numpy as np
from sudoku_solver_tim.strategies.master.brute_force import brute_force
import json


def read_grids():
    with open("tests/fixtures/grids.txt", "r") as f:
        grids = f.readlines()

    return [grid.strip() for grid in grids]





def calculate_stats(timings):
    if not timings:
        return None
    
    np_timings = np.array(timings)
    return {
        "lower": float(np.percentile(np_timings, 0)),  # min
        "q1": float(np.percentile(np_timings, 25)),
        "median": float(np.percentile(np_timings, 50)),
        "q3": float(np.percentile(np_timings, 75)),
        "upper": float(np.percentile(np_timings, 100)),  # max
        "n": len(timings)
    }



def benchmark_puzzles(grids, strategies=None):
    timings = []
    for grid in grids:
        puzzle = Puzzle.from_string(grid)
        start_time = time.time()
        puzzle.solve()
        end_time = time.time()
        
        timings.append(end_time - start_time)

    # total time
    total_time = sum(timings)
    print(f"Total time: {total_time} seconds")
    return calculate_stats(timings), total_time


def save_results(results, output_file):
    # Write results to JSON file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    


def main():
    grids = read_grids()
    stats = benchmark_puzzles(grids)
    print("Completed full benchmark")
    # save_results(stats, "benchmark_results_2k.json")

    # stats_brute = benchmark_puzzles(grids, strategies=[brute_force])
    # print("Completed brute force benchmark")
    # save_results(stats_brute, "benchmark_results_2k_brute.json")


if __name__ == "__main__":
    main()

