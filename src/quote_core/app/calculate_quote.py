from __future__ import annotations

import logging
from pathlib import Path

from quote_core.costing.pricing_rules import build_cost_breakdown
from quote_core.dfm.checks import run_dfm_checks
from quote_core.domain.models import QuoteRequest, QuoteResult
from quote_core.geometry.contour_builder import build_contours
from quote_core.geometry.metrics import calculate_metrics
from quote_core.geometry.normalizer import normalize_entities
from quote_core.parsers.dxf_parser import parse_dxf

logger = logging.getLogger(__name__)


def calculate_quote(request: QuoteRequest) -> QuoteResult:
    logger.info("Starting quote calculation for DXF: %s", request.dxf_path)
    raw_entities = parse_dxf(Path(request.dxf_path))
    segments = normalize_entities(raw_entities)
    contours = build_contours(segments)
    metrics = calculate_metrics(contours)
    dfm_result = run_dfm_checks()
    costs = build_cost_breakdown(request=request, metrics=metrics)

    logger.info(
        "Quote calculation finished (total_cost=%.2f RUB)",
        costs.total_cost,
    )
    return QuoteResult(
        geometry=metrics,
        dfm=dfm_result,
        costs=costs,
    )
