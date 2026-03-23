from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CostingSettings:
    """Global costing knobs (MVP placeholders)."""

    setup_cost_rub: float
    cutting_machine_rub_per_min: float


DEFAULT_COSTING_SETTINGS = CostingSettings(
    setup_cost_rub=500.0,
    cutting_machine_rub_per_min=120.0,
)
