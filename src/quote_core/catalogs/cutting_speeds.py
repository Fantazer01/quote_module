from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CuttingSpeedEntry:
    material_code: str
    thickness_mm: float
    speed_mm_per_min: float


CUTTING_SPEEDS: tuple[CuttingSpeedEntry, ...] = (
    CuttingSpeedEntry(material_code="steel_s235", thickness_mm=1.0, speed_mm_per_min=3500.0),
    CuttingSpeedEntry(material_code="steel_s235", thickness_mm=2.0, speed_mm_per_min=2200.0),
    CuttingSpeedEntry(material_code="steel_s235", thickness_mm=3.0, speed_mm_per_min=1500.0),
    CuttingSpeedEntry(material_code="steel_dc01", thickness_mm=1.0, speed_mm_per_min=3400.0),
    CuttingSpeedEntry(material_code="steel_dc01", thickness_mm=2.0, speed_mm_per_min=2100.0),
    CuttingSpeedEntry(material_code="aluminum_5754", thickness_mm=1.0, speed_mm_per_min=5000.0),
    CuttingSpeedEntry(material_code="aluminum_5754", thickness_mm=2.0, speed_mm_per_min=3800.0),
)


def _thickness_matches(a: float, b: float, eps: float = 1e-3) -> bool:
    return abs(a - b) <= eps


def get_cutting_speed_mm_per_min(material_code: str, thickness_mm: float) -> float:
    for entry in CUTTING_SPEEDS:
        if entry.material_code == material_code and _thickness_matches(
            entry.thickness_mm, thickness_mm
        ):
            return entry.speed_mm_per_min
    raise ValueError(
        f"No cutting speed for material={material_code!r}, thickness_mm={thickness_mm!r}"
    )
