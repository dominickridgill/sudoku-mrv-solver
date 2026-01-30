# 16×16 Sudoku Solver using MRV Heuristic

This project implements a **16×16 Sudoku (Hexadoku) solver** using **backtracking with the Minimum Remaining Values (MRV) heuristic**.  
The solver models Sudoku as a **constraint satisfaction problem (CSP)** and applies MRV to significantly reduce the search space compared to naive depth-first search.

## Problem Overview

Standard 9×9 Sudoku already presents a non-trivial search problem.  
A 16×16 Sudoku increases complexity substantially:

- Larger symbol set (0–9, A–F)
- 4×4 subgrids instead of 3×3
- Much higher branching factor

Without heuristics, naive backtracking becomes impractical.

## Approach

### Constraint Satisfaction Model
Each empty cell is treated as a variable with a domain of possible symbols.  
Constraints are enforced across:

- Rows
- Columns
- 4×4 subgrids

### Minimum Remaining Values (MRV)
At each step, the solver selects the empty cell with the **fewest valid remaining candidates**.

This heuristic:
- Reduces the branching factor
- Detects dead ends early
- Improves overall efficiency and determinism

### Additional Techniques
- **Forward checking**: immediately abandons invalid branches
- **Deterministic candidate ordering** for reproducible behavior
- **Recursive call counter** to observe performance

## Results

Using MRV dramatically reduces the number of recursive calls compared to naive backtracking.  
This makes solving complex 16×16 puzzles feasible within reasonable time.

Example output includes:
- Completed Sudoku grid
- Total recursive calls used to reach the solution

## Code Structure

- `get_valid_candidates` — computes legal symbols for a cell
- `find_mrv_cell` — selects the most constrained empty cell
- `solve_sudoku` — recursive backtracking solver
- `print_board` — formatted output for readability

The implementation favors **clarity and correctness** over micro-optimizations.

## Limitations & Future Improvements

- No constraint caching (e.g., arc consistency)
- No parallel search
- Performance can be further improved with advanced CSP techniques

These trade-offs were intentional to keep the solver readable and explainable.

## Disclaimer

This repository contains **only personal and academic work**.  
No proprietary, confidential, or employer-owned code or data is included.

---

**Author:** Dominick Ridgill  
**Focus Areas:** Algorithms, Constraint Satisfaction, Heuristic Search
