import json
import time
import numpy as np
from sudoku_solver_tim.puzzle import Puzzle
from sudoku_solver_tim.strategies.master.brute_force import brute_force
import os


def read_from_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def read_all_json_files_in_directory(directory):
    examples = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            examples.extend(read_from_json(filepath))
    return examples


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


def benchmark_puzzles(examples, levels, strategies=None):
    # Dictionary to store timings per level
    level_timings = {level: [] for level in levels}
    
    # Measure solve time for each puzzle
    for example in examples:
        for level in levels:
            if level in example["url"]:
                puzzle = Puzzle(example["puzzle"])
                start_time = time.time()
                if strategies:
                    puzzle.solve(strategies=strategies)
                else:
                    puzzle.solve()
                end_time = time.time()
                level_timings[level].append(end_time - start_time)
                break  # Found the level, no need to check others
    
    # Calculate statistics for each level
    results = []
    for level in levels:
        stats = calculate_stats(level_timings[level])
        if stats:
            stats["level"] = level
            results.append(stats)
    
    return results


def save_and_print_results(results, output_file, title):
    # Write results to JSON file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    


def main():
    EXAMPLES = read_all_json_files_in_directory("tests/fixtures")
    levels = ["beginner", "easy", "medium", "tricky", "fiendish", "diabolical"]
    
    # Benchmark full solver
    results_full = benchmark_puzzles(EXAMPLES, levels)
    save_and_print_results(results_full, "benchmark_results_full.json", "Full Solver Results")
    
    # Benchmark brute force solver
    results_brute = benchmark_puzzles(EXAMPLES, levels, strategies=[brute_force])
    save_and_print_results(results_brute, "benchmark_results_brute.json", "Brute Force Solver Results")


if __name__ == "__main__":
    main()



