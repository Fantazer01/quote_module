from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    """Sheet stock: density and purchase price per kg (MVP stub values)."""

    code: str
    name: str
    density_kg_per_m3: float
    price_rub_per_kg: float


MATERIALS: tuple[Material, ...] = (
    Material(
        code="steel_s235",
        name="Сталь S235",
        density_kg_per_m3=7850.0,
        price_rub_per_kg=95.0,
    ),
    Material(
        code="steel_dc01",
        name="Сталь DC01",
        density_kg_per_m3=7850.0,
        price_rub_per_kg=102.0,
    ),
    Material(
        code="aluminum_5754",
        name="Алюминий 5754",
        density_kg_per_m3=2700.0,
        price_rub_per_kg=320.0,
    ),
)


def get_material_by_code(code: str) -> Material:
    for material in MATERIALS:
        if material.code == code:
            return material
    raise ValueError(f"Unknown material code: {code!r}")
