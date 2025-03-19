# A sudoku solver that is actually helpful

I occasionally enjoy playing [sudoku puzzles](https://en.wikipedia.org/wiki/Sudoku). I particularly like the harder ones that pose a real challenge. Play them and you will get stuck inevitable. I often wonder if I missed something, or if I need to apply a more advanced strategy to solve this puzzle, one that I have not yet learned.

What if I could write a sudoku solver that gives me the easiest possible strategy required to find the next move?
Cheating? Sudoku's are already a complete waste of time because they are easily solvable by computers. A sudoku solver that makes playing challenging sudoku puzzles more fun is not cheating but a great hack!

## Strategies for writing sudoku solvers

Writing a sudoku solver? Dead simple.

Ask ChatGPT _"Write me a sudoku solver in python_" and you will get a solver in just 25 lines of code. Sudoku's are easy to solve by computers using an efficient tree search. There are many implementations out there that are also very fast.

What we need however is a solver that tries each strategy that a human would try. Starting from easiest to hardest.
Humans can have many different strategies, so the question is which strategies do we need to include? There are approaches like Crook's algorithm ([A Pencil-and-Paper
Algorithm for Solving
Sudoku Puzzles, Crook, 2009](http://www.ams.org/notices/200904/rtx090400460p.pdf)) that involves writing up the entire markup (also known as _pencilmarks_) of a puzzle to solve even the hardest sudoku's. Here's an example:

<img src="https://www.sudokuoftheday.com/image.svg?sg=!43**51**36!62**948!65**7*59!562*8**2!6491**8!624**23**8!4" width="350" />

Instead of working with pencilmarks exclusively, I will use the most common techniques applied by puzzlers, as taken from https://www.sudokuoftheday.com/techniques. For example, the easiest strategy is the [Single Position](https://www.sudokuoftheday.com/techniques/single-position), where you choose a row, column or box, and then go through each of the numbers that hasn’t already been placed. If you're lucky, there will a number that has only one place it could go and you can fill it in: 

<img src="https://www.sudokuoftheday.com/image.svg?sg=,6030E70803_4K,12_5K6,K1M0M0K3K5M0M0G06K0E7K9K0K4K0K150K5K0K0K0K1E7K,4,2.K,76_5K080407060K2," width="350" />

These are the strategies I will implement:

- Easy techniques:
    - [Single Position](https://www.sudokuoftheday.com/techniques/single-position)
    - [Single Candidate](https://www.sudokuoftheday.com/techniques/single-candidate)
- Medium techniques:
    - [Candidate Lines](https://www.sudokuoftheday.com/techniques/candidate-lines)
    - [Double Pairs](https://www.sudokuoftheday.com/techniques/double-pairs)
    - [Multiple Lines](https://www.sudokuoftheday.com/techniques/multiple-lines)
- Advanced techniques:
    - [Naked Pairs/Triples](https://www.sudokuoftheday.com/techniques/naked-pairs-triples)
    - [Hidden Pairs/Triples](https://www.sudokuoftheday.com/techniques/hidden-pairs-triples)
- Master techniques:
    - [X-Wing](https://www.sudokuoftheday.com/techniques/x-wings)
    - [Swordfish](https://www.sudokuoftheday.com/techniques/swordfish)
    - [Forcing Chains](https://www.sudokuoftheday.com/techniques/forcing-chains)
- When all else fails:
    - [Nishio](https://www.sudokuoftheday.com/techniques/nishio) (aka guessing or brute force)

## The implementation in python

Our goal is not speed but interpretability. And we will have to implement many different strategies. This is why we choose an _object oriented programming_ (OOP) approach: each `Puzzle` has `Cell`, which is one of the 9 members of a `Row`, `Column` and `Block` respectively. A sudoku puzzle is represented as a list of lists with 9 integers, where `0` means no value is assigned yet.

Here is how it works:

```python
# Very easy puzzle that can be solved
# with single candidates
grid = [
[2, 5, 0, 0, 3, 0, 9, 0, 1],
[0, 1, 0, 0, 0, 4, 0, 0, 0],
[4, 0, 7, 0, 0, 0, 2, 0, 8],
[0, 0, 5, 2, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 9, 8, 1, 0, 0],
[0, 4, 0, 0, 0, 3, 0, 0, 0],
[0, 0, 0, 3, 6, 0, 0, 7, 2],
[0, 7, 0, 0, 0, 0, 0, 0, 3],
[9, 0, 3, 0, 0, 0, 6, 0, 4]]
p = Puzzle(grid)
p
# ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ 
# ┃ 2 │ 5 │   ┃ ┃   │ 3 │   ┃ ┃ 9 │   │ 1 ┃ 
# ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
# ┃   │ 1 │   ┃ ┃   │   │ 4 ┃ ┃   │   │   ┃ 
# ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
# ┃ 4 │   │ 7 ┃ ┃   │   │   ┃ ┃ 2 │   │ 8 ┃ 
# ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ 
# ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ 
# ┃   │   │ 5 ┃ ┃ 2 │   │   ┃ ┃   │   │   ┃ 
# ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
# ┃   │   │   ┃ ┃   │ 9 │ 8 ┃ ┃ 1 │   │   ┃ 
# ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
# ┃   │ 4 │   ┃ ┃   │   │ 3 ┃ ┃   │   │   ┃ 
# ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ 
# ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ ┏━━━┯━━━┯━━━┓ 
# ┃   │   │   ┃ ┃ 3 │ 6 │   ┃ ┃   │ 7 │ 2 ┃ 
# ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
# ┃   │ 7 │   ┃ ┃   │   │   ┃ ┃   │   │ 3 ┃ 
# ┠───┼───┼───┨ ┠───┼───┼───┨ ┠───┼───┼───┨ 
# ┃ 9 │   │ 3 ┃ ┃   │   │   ┃ ┃ 6 │   │ 4 ┃ 
# ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ ┗━━━┷━━━┷━━━┛ 
p.solve()
assert p.is_solved()
assert p.strategies_used == {'single candidates','single position'}
```

## Double pairs vs multiple pairs

Interestingly, while multiple pairs is harder to spot for humans, it was harder to implement the easier double pairs. 
That because we then need to keep track of how many rows for each value.

## Other stuff to discuss:

- Debugging is hard. You don't want to be making sudoku's by hand now, do we ? :) 
   - I needed to make a `Puzzle` class that can be printed in a nice way, but that could also highlight the cells that were in scope for a certain strategy.


reflect on using LLMs for code:
https://simonwillison.net/2025/Mar/11/using-llms-for-code/

Example prompt to `Claude 3.7 Sonnet Thinking`:

```
I am writing a sudoku puzzle solver, see `@puzzle.py` .

I've already implemented the double pairs strategy in `@double_pairs.py` , which implements the technique described in `@https://www.sudokuoftheday.com/techniques/double-pairs` .

Now write the implementation for `@multiple_lines.py` , as described in `@https://www.sudokuoftheday.com/techniques/multiple-lines` .
```

- it's actually much faster than the basic brute force solver. (show some tests)

- git scraper https://simonwillison.net/2020/Oct/9/git-scraping/

- having lots of tests cases is important, as there are a lot of edge cases.

next steps: - deploy webapp with optical camera recognition, and solver in Python via PyScript