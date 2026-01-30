"""
16x16 Sudoku (Hexadoku) Solver using Backtracking with
Minimum Remaining Values (MRV) Heuristic.

Symbols: 0–9, A–F
Subgrid size: 4x4

This implementation models Sudoku as a constraint satisfaction problem (CSP)
and applies MRV to reduce the branching factor during search.
"""

from typing import List, Tuple, Optional, Set

# ----------------------------
# Type aliases and constants
# ----------------------------

Board = List[List[str]]
Position = Tuple[int, int]

GRID_SIZE = 16
SUBGRID_SIZE = 4
EMPTY_CELL = "_"

SYMBOLS: Set[str] = {
    "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "A", "B", "C", "D", "E", "F"
}

# Global counter for performance analysis
recursive_calls = 0


# ----------------------------
# Utility functions
# ----------------------------

def print_board(board: Board) -> None:
    """
    Pretty-print a 16x16 Sudoku board with 4x4 subgrid separators.
    """
    for row_idx, row in enumerate(board):
        if row_idx % SUBGRID_SIZE == 0 and row_idx != 0:
            print("-" * 41)

        for col_idx, value in enumerate(row):
            if col_idx % SUBGRID_SIZE == 0 and col_idx != 0:
                print("|", end=" ")

            print(value, end=" ")

        print()
    print()


def get_valid_candidates(board: Board, row: int, col: int) -> Set[str]:
    """
    Compute the valid candidate symbols for a given empty cell
    based on row, column, and subgrid constraints.
    """
    used_symbols = set()

    # Row constraint
    used_symbols.update(board[row])

    # Column constraint
    used_symbols.update(board[r][col] for r in range(GRID_SIZE))

    # Subgrid constraint
    start_row = (row // SUBGRID_SIZE) * SUBGRID_SIZE
    start_col = (col // SUBGRID_SIZE) * SUBGRID_SIZE

    for r in range(start_row, start_row + SUBGRID_SIZE):
        for c in range(start_col, start_col + SUBGRID_SIZE):
            used_symbols.add(board[r][c])

    # Valid candidates are those not already used
    return SYMBOLS - used_symbols


# ----------------------------
# MRV heuristic
# ----------------------------

def find_mrv_cell(board: Board) -> Optional[Tuple[int, int, Set[str]]]:
    """
    Find the empty cell with the Minimum Remaining Values (MRV).

    Returns:
        (row, col, candidate_set) for the most constrained cell,
        or None if the board is complete.
    """
    best_cell = None
    smallest_domain_size = float("inf")

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == EMPTY_CELL:
                candidates = get_valid_candidates(board, row, col)

                # Forward checking: no valid assignments → dead end
                if not candidates:
                    return None

                if len(candidates) < smallest_domain_size:
                    smallest_domain_size = len(candidates)
                    best_cell = (row, col, candidates)

                    # Cannot do better than one candidate
                    if smallest_domain_size == 1:
                        return best_cell

    return best_cell


# ----------------------------
# Solver
# ----------------------------

def solve_sudoku(board: Board) -> bool:
    """
    Solve the 16x16 Sudoku using backtracking with MRV heuristic.

    Returns:
        True if solved, False otherwise.
    """
    global recursive_calls
    recursive_calls += 1

    mrv_result = find_mrv_cell(board)

    # No empty cells remain — puzzle solved
    if mrv_result is None:
        return True

    row, col, candidates = mrv_result

    # Deterministic ordering for reproducibility
    for symbol in sorted(candidates):
        board[row][col] = symbol

        if solve_sudoku(board):
            return True

        # Backtrack
        board[row][col] = EMPTY_CELL

    return False


# ----------------------------
# Entry point
# ----------------------------

if __name__ == "__main__":
    board: Board = [
        ["_", "6", "8", "_", "_", "5", "_", "_", "7", "B", "A", "D", "_", "3", "_", "_"],
        ["_", "_", "_", "F", "A", "_", "8", "B", "4", "_", "3", "0", "_", "_", "C", "_"],
        ["7", "_", "0", "_", "9", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "1"],
        ["C", "_", "_", "3", "D", "_", "_", "_", "_", "_", "_", "_", "_", "4", "_", "0"],
        ["_", "_", "_", "_", "_", "_", "6", "5", "1", "_", "_", "4", "_", "_", "E", "3"],
        ["_", "B", "_", "_", "4", "_", "A", "_", "_", "_", "8", "_", "_", "F", "_", "_"],
        ["8", "_", "_", "6", "_", "_", "_", "_", "_", "_", "_", "7", "_", "_", "_", "2"],
        ["_", "1", "F", "4", "7", "_", "_", "3", "_", "E", "_", "9", "6", "_", "_", "_"],
        ["_", "_", "_", "2", "0", "_", "_", "6", "C", "_", "_", "_", "9", "E", "A", "F"],
        ["_", "_", "3", "_", "F", "9", "D", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
        ["_", "E", "_", "A", "8", "_", "7", "2", "6", "5", "_", "_", "_", "_", "_", "_"],
        ["_", "_", "7", "C", "1", "_", "_", "_", "_", "_", "4", "3", "_", "_", "5", "_"],
        ["F", "_", "_", "_", "_", "_", "_", "_", "0", "_", "9", "8", "_", "B", "2", "D"],
        ["_", "0", "B", "E", "_", "_", "C", "1", "_", "_", "_", "_", "_", "_", "3", "A"],
        ["5", "2", "6", "9", "_", "_", "B", "_", "_", "_", "E", "1", "_", "_", "_", "_"],
        ["_", "_", "C", "_", "5", "_", "_", "9", "_", "F", "_", "_", "_", "_", "_", "6"]
    ]

    print("Original Board:")
    print_board(board)

    if solve_sudoku(board):
        print("Solved Board:")
        print_board(board)
        print(f"Recursive calls: {recursive_calls}")
    else:
        print("No solution exists.")
