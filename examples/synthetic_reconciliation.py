"""Clean-room reconciliation with fabricated planning weights only."""


def reconcile(control_total: int, raw_weights: dict[str, int]) -> dict[str, int]:
    """Allocate an integer synthetic control total while preserving its exact sum."""
    if control_total < 0 or not raw_weights or any(weight < 0 for weight in raw_weights.values()):
        raise ValueError("control_total and weights must be non-negative")
    weight_total = sum(raw_weights.values())
    if weight_total == 0:
        raise ValueError("at least one weight must be positive")
    allocation = {key: control_total * weight // weight_total for key, weight in raw_weights.items()}
    remainder = control_total - sum(allocation.values())
    ranked_keys = sorted(raw_weights, key=lambda key: (control_total * raw_weights[key]) % weight_total, reverse=True)
    for key in ranked_keys[:remainder]:
        allocation[key] += 1
    return allocation


if __name__ == "__main__":
    print(reconcile(100, {"Brand A / Model": 5, "Brand A / PLC": 3, "Brand B / PLC": 2}))
