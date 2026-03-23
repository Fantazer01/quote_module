from __future__ import annotations


def calculate_material_cost(
    *,
    area_mm2: float,
    thickness_mm: float,
    density_kg_per_m3: float,
    price_rub_per_kg: float,
) -> float:
    """
    Sheet blank mass from footprint area × thickness × density, price per kg.

    area_mm2: approximate part footprint (same convention as GeometryMetrics.total_area_mm2).
    """
    if area_mm2 <= 0.0 or thickness_mm <= 0.0:
        return 0.0

    volume_mm3 = area_mm2 * thickness_mm
    volume_m3 = volume_mm3 / 1_000_000_000.0
    mass_kg = volume_m3 * density_kg_per_m3
    return mass_kg * price_rub_per_kg
