from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PiercePriceEntry:
    material_code: str
    thickness_mm: float
    price_rub_per_pierce: float


PIERCE_PRICES: tuple[PiercePriceEntry, ...] = (
    PiercePriceEntry(material_code="steel_s235", thickness_mm=1.0, price_rub_per_pierce=8.0),
    PiercePriceEntry(material_code="steel_s235", thickness_mm=2.0, price_rub_per_pierce=10.0),
    PiercePriceEntry(material_code="steel_s235", thickness_mm=3.0, price_rub_per_pierce=12.0),
    PiercePriceEntry(material_code="steel_dc01", thickness_mm=1.0, price_rub_per_pierce=8.0),
    PiercePriceEntry(material_code="steel_dc01", thickness_mm=2.0, price_rub_per_pierce=10.0),
    PiercePriceEntry(material_code="aluminum_5754", thickness_mm=1.0, price_rub_per_pierce=6.0),
    PiercePriceEntry(material_code="aluminum_5754", thickness_mm=2.0, price_rub_per_pierce=8.0),
)


def _thickness_matches(a: float, b: float, eps: float = 1e-3) -> bool:
    return abs(a - b) <= eps


def get_pierce_price_rub_per_pierce(material_code: str, thickness_mm: float) -> float:
    for entry in PIERCE_PRICES:
        if entry.material_code == material_code and _thickness_matches(
            entry.thickness_mm, thickness_mm
        ):
            return entry.price_rub_per_pierce
    raise ValueError(
        f"No pierce price for material={material_code!r}, thickness_mm={thickness_mm!r}"
    )
