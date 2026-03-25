from __future__ import annotations

import logging

from quote_core.catalogs.cutting_speeds import get_cutting_speed_mm_per_min
from quote_core.catalogs.materials import get_material_by_code
from quote_core.catalogs.pierce_prices import get_pierce_price_rub_per_pierce
from quote_core.catalogs.settings import DEFAULT_COSTING_SETTINGS
from quote_core.costing.cutting_cost import calculate_cutting_cost
from quote_core.costing.material_cost import calculate_material_cost
from quote_core.costing.piercing_cost import calculate_piercing_cost
from quote_core.costing.total_cost import calculate_total_cost
from quote_core.domain.models import CostBreakdown, GeometryMetrics, QuoteRequest

logger = logging.getLogger(__name__)


def build_cost_breakdown(
    *,
    request: QuoteRequest,
    metrics: GeometryMetrics,
) -> CostBreakdown:
    """
    Per-part costs from metrics × quantity; setup once per quote.

    Material: area × thickness × density × price/kg.
    Cutting: (length / speed) × RUB/min.
    Piercing: pierce_count × price/pierce.
    """
    logger.info("Building cost breakdown (material=%s, qty=%d)", request.material_code, request.quantity)
    quantity = max(0, request.quantity)
    if quantity == 0:
        return CostBreakdown(
            material_cost=0.0,
            cutting_cost=0.0,
            piercing_cost=0.0,
            setup_cost=0.0,
            total_cost=0.0,
        )

    material = get_material_by_code(request.material_code)
    speed_mm_per_min = get_cutting_speed_mm_per_min(
        request.material_code, request.thickness_mm
    )
    pierce_price = get_pierce_price_rub_per_pierce(
        request.material_code, request.thickness_mm
    )
    settings = DEFAULT_COSTING_SETTINGS

    material_per_part = calculate_material_cost(
        area_mm2=metrics.total_area_mm2,
        thickness_mm=request.thickness_mm,
        density_kg_per_m3=material.density_kg_per_m3,
        price_rub_per_kg=material.price_rub_per_kg,
    )

    cutting_per_part = calculate_cutting_cost(
        total_cut_length_mm=metrics.total_cut_length_mm,
        speed_mm_per_min=speed_mm_per_min,
        rub_per_minute=settings.cutting_machine_rub_per_min,
    )

    piercing_per_part = calculate_piercing_cost(
        pierce_count=metrics.pierce_count,
        price_rub_per_pierce=pierce_price,
    )

    material_cost = material_per_part * quantity
    cutting_cost = cutting_per_part * quantity
    piercing_cost = piercing_per_part * quantity
    setup_cost = settings.setup_cost_rub

    total_cost = calculate_total_cost(
        material_cost=material_cost,
        cutting_cost=cutting_cost,
        piercing_cost=piercing_cost,
        setup_cost=setup_cost,
    )

    logger.info(
        "Cost breakdown ready: total=%.2f RUB (material=%.2f, cutting=%.2f, "
        "piercing=%.2f, setup=%.2f)",
        total_cost,
        material_cost,
        cutting_cost,
        piercing_cost,
        setup_cost,
    )
    return CostBreakdown(
        material_cost=material_cost,
        cutting_cost=cutting_cost,
        piercing_cost=piercing_cost,
        setup_cost=setup_cost,
        total_cost=total_cost,
    )
