from __future__ import annotations

import logging

from quote_core.domain.models import GeometryMetrics

logger = logging.getLogger(__name__)
from quote_core.geometry.primitives import Contour


def calculate_metrics(contours: list[Contour]) -> GeometryMetrics:
    contour_count = len(contours)

    total_cut_length_mm = sum(
        segment.length
        for contour in contours
        for segment in contour.segments
    )

    pierce_count = sum(1 for contour in contours if contour.segments)

    all_x: list[float] = []
    all_y: list[float] = []
    for contour in contours:
        for segment in contour.segments:
            all_x.append(segment.start.x)
            all_x.append(segment.end.x)
            all_y.append(segment.start.y)
            all_y.append(segment.end.y)

    if all_x and all_y:
        min_x = min(all_x)
        max_x = max(all_x)
        min_y = min(all_y)
        max_y = max(all_y)
        bounding_box_width_mm = max_x - min_x
        bounding_box_height_mm = max_y - min_y
    else:
        bounding_box_width_mm = 0.0
        bounding_box_height_mm = 0.0

    # MVP approximation: area as bounding box area.
    total_area_mm2 = bounding_box_width_mm * bounding_box_height_mm

    logger.info(
        "Computed geometry metrics: contours=%d, cut_length_mm=%.2f, pierces=%d",
        contour_count,
        total_cut_length_mm,
        pierce_count,
    )
    return GeometryMetrics(
        contour_count=contour_count,
        total_cut_length_mm=total_cut_length_mm,
        total_area_mm2=total_area_mm2,
        pierce_count=pierce_count,
        bounding_box_width_mm=bounding_box_width_mm,
        bounding_box_height_mm=bounding_box_height_mm,
    )
