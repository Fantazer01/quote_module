from __future__ import annotations


def calculate_piercing_cost(*, pierce_count: int, price_rub_per_pierce: float) -> float:
    if pierce_count <= 0:
        return 0.0
    return float(pierce_count) * price_rub_per_pierce
