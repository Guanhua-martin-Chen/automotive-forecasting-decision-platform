"""Clean-room conceptual Brand × Model × PLC matrix reconciliation.

This fabricated RAS-style demonstration is not private production code.
"""

from math import isclose


def reconcile_matrix(
    seed_matrix: list[list[float]],
    model_totals: list[float],
    plc_totals: list[float],
    *,
    tolerance: float = 1e-9,
    max_iterations: int = 1_000,
) -> list[list[float]]:
    """Reconcile a positive seed matrix to synthetic Model rows and PLC columns."""
    if not seed_matrix or len(seed_matrix) != len(model_totals):
        raise ValueError("seed rows must match model totals")
    if any(len(row) != len(plc_totals) for row in seed_matrix):
        raise ValueError("seed columns must match PLC totals")
    if any(value <= 0 for row in seed_matrix for value in row):
        raise ValueError("this simple demonstration requires a positive seed matrix")
    if any(value < 0 for value in model_totals + plc_totals):
        raise ValueError("control totals must be non-negative")
    if not isclose(sum(model_totals), sum(plc_totals), abs_tol=tolerance):
        raise ValueError("Model and PLC control totals must share the Brand total")

    matrix = [row[:] for row in seed_matrix]
    for _ in range(max_iterations):
        for row, target in zip(matrix, model_totals):
            factor = target / sum(row)
            for column in range(len(row)):
                row[column] *= factor
        for column, target in enumerate(plc_totals):
            factor = target / sum(row[column] for row in matrix)
            for row in matrix:
                row[column] *= factor
        row_error = max(abs(sum(row) - target) for row, target in zip(matrix, model_totals))
        column_error = max(
            abs(sum(row[column] for row in matrix) - target)
            for column, target in enumerate(plc_totals)
        )
        if max(row_error, column_error) <= tolerance:
            return matrix
    raise RuntimeError("synthetic matrix did not converge within max_iterations")


if __name__ == "__main__":
    result = reconcile_matrix([[3.0, 2.0], [1.0, 4.0]], [50.0, 50.0], [45.0, 55.0])
    print(result)
