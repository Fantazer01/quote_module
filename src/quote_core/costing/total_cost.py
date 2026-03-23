from __future__ import annotations


def calculate_total_cost(
    *,
    material_cost: float,
    cutting_cost: float,
    piercing_cost: float,
    setup_cost: float,
) -> float:
    return material_cost + cutting_cost + piercing_cost + setup_cost
