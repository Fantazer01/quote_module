from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuoteRequest:
    dxf_path: str
    material_code: str
    thickness_mm: float
    quantity: int


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Segment:
    start: Point
    end: Point
    length_mm: float


@dataclass(frozen=True)
class Contour:
    segments: list[Segment]
    is_closed: bool


@dataclass(frozen=True)
class GeometryMetrics:
    contour_count: int
    total_cut_length_mm: float
    total_area_mm2: float
    pierce_count: int


@dataclass(frozen=True)
class DFMResult:
    is_valid: bool
    message: str | None


@dataclass(frozen=True)
class CostBreakdown:
    material_cost: float
    cutting_cost: float
    setup_cost: float
    total_cost: float


@dataclass(frozen=True)
class QuoteResult:
    geometry: GeometryMetrics
    dfm: DFMResult
    costs: CostBreakdown
