"""Clean-room rolling-origin splits for a fabricated time series."""


def rolling_origins(length: int, minimum_history: int, horizon: int = 1):
    """Yield training and test index ranges without allowing future leakage."""
    if minimum_history < 1 or horizon < 1:
        raise ValueError("minimum_history and horizon must be positive")
    for origin in range(minimum_history, length - horizon + 1):
        yield range(0, origin), range(origin, origin + horizon)


def evaluate_last_value(values: list[float], minimum_history: int) -> list[tuple[float, float]]:
    """Return prediction/actual pairs using only history available at each origin."""
    results = []
    for train, test in rolling_origins(len(values), minimum_history):
        results.append((values[train.stop - 1], values[test.start]))
    return results


if __name__ == "__main__":
    print(evaluate_last_value([10.0, 12.0, 13.0, 15.0, 14.0], minimum_history=2))
