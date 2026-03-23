from __future__ import annotations


def calculate_cutting_cost(
    *,
    total_cut_length_mm: float,
    speed_mm_per_min: float,
    rub_per_minute: float,
) -> float:
    """Machine time cost: (cut length / cutting speed) × rate per minute."""
    if total_cut_length_mm <= 0.0:
        return 0.0
    if speed_mm_per_min <= 0.0:
        return 0.0

    minutes = total_cut_length_mm / speed_mm_per_min
    return minutes * rub_per_minute
