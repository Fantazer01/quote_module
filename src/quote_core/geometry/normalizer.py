from __future__ import annotations

import math
from typing import Sequence

from quote_core.parsers.dxf_parser import (
    RawArc,
    RawCircle,
    RawEntity,
    RawLine,
    RawLWPolyline,
)

from quote_core.geometry.primitives import Point, Segment


def _arc_ccw_sweep_deg(start_deg: float, end_deg: float) -> float:
    """CCW angular distance in degrees from start to end (DXF ARC convention)."""
    delta = (end_deg - start_deg) % 360.0
    if delta < 1e-12:
        return 360.0
    return delta


def _arc_to_segments(raw: RawArc) -> list[Segment]:
    cx = raw.center_x
    cy = raw.center_y
    radius = raw.radius
    if radius <= 0.0:
        return []

    sweep_deg = _arc_ccw_sweep_deg(raw.start_angle_deg, raw.end_angle_deg)
    if sweep_deg >= 359.999:
        # Degenerate full circle as ARC — approximate like a circle.
        return _circle_to_segments(
            RawCircle(center_x=cx, center_y=cy, radius=radius)
        )

    start_rad = math.radians(raw.start_angle_deg)
    sweep_rad = math.radians(sweep_deg)

    segment_count = max(8, min(64, int(sweep_deg / 5.0) + 1))
    segments: list[Segment] = []

    for index in range(segment_count):
        t0 = start_rad + sweep_rad * (index / segment_count)
        t1 = start_rad + sweep_rad * ((index + 1) / segment_count)
        x0 = cx + radius * math.cos(t0)
        y0 = cy + radius * math.sin(t0)
        x1 = cx + radius * math.cos(t1)
        y1 = cy + radius * math.sin(t1)
        segments.append(
            Segment(start=Point(x=x0, y=y0), end=Point(x=x1, y=y1))
        )

    return segments


def _circle_to_segments(raw: RawCircle) -> list[Segment]:
    if raw.radius <= 0.0:
        return []

    segment_count = 36
    cx = raw.center_x
    cy = raw.center_y
    r = raw.radius
    segments: list[Segment] = []

    for index in range(segment_count):
        t0 = (2.0 * math.pi * index) / segment_count
        t1 = (2.0 * math.pi * (index + 1)) / segment_count
        x0 = cx + r * math.cos(t0)
        y0 = cy + r * math.sin(t0)
        x1 = cx + r * math.cos(t1)
        y1 = cy + r * math.sin(t1)
        segments.append(
            Segment(start=Point(x=x0, y=y0), end=Point(x=x1, y=y1))
        )

    return segments


def _lwpolyline_to_segments(raw: RawLWPolyline) -> list[Segment]:
    vertices = raw.vertices
    if len(vertices) < 2:
        return []

    segments: list[Segment] = []
    last_index = len(vertices) - 1

    for index in range(last_index):
        x0, y0 = vertices[index]
        x1, y1 = vertices[index + 1]
        segments.append(
            Segment(
                start=Point(x=float(x0), y=float(y0)),
                end=Point(x=float(x1), y=float(y1)),
            )
        )

    if raw.is_closed:
        x0, y0 = vertices[last_index]
        x1, y1 = vertices[0]
        segments.append(
            Segment(
                start=Point(x=float(x0), y=float(y0)),
                end=Point(x=float(x1), y=float(y1)),
            )
        )

    return segments


def normalize_entities(entities: Sequence[RawEntity]) -> list[Segment]:
    """Convert raw DXF entities into directed segments in WCS (mm)."""
    result: list[Segment] = []

    for entity in entities:
        if isinstance(entity, RawLine):
            result.append(
                Segment(
                    start=Point(x=entity.start_x, y=entity.start_y),
                    end=Point(x=entity.end_x, y=entity.end_y),
                )
            )
        elif isinstance(entity, RawArc):
            result.extend(_arc_to_segments(entity))
        elif isinstance(entity, RawCircle):
            result.extend(_circle_to_segments(entity))
        elif isinstance(entity, RawLWPolyline):
            result.extend(_lwpolyline_to_segments(entity))

    return result
