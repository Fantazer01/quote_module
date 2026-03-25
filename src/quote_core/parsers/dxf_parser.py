from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

import ezdxf

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RawLine:
    start_x: float
    start_y: float
    end_x: float
    end_y: float


@dataclass(frozen=True)
class RawArc:
    center_x: float
    center_y: float
    radius: float
    start_angle_deg: float
    end_angle_deg: float


@dataclass(frozen=True)
class RawCircle:
    center_x: float
    center_y: float
    radius: float


@dataclass(frozen=True)
class RawLWPolyline:
    vertices: list[tuple[float, float]]
    is_closed: bool


RawEntity: TypeAlias = RawLine | RawArc | RawCircle | RawLWPolyline


def parse_dxf(file_path: Path) -> list:
    document = ezdxf.readfile(str(file_path))
    modelspace = document.modelspace()

    entities: list[RawEntity] = []

    for entity in modelspace:
        entity_type = entity.dxftype()

        if entity_type == "LINE":
            entities.append(
                RawLine(
                    start_x=float(entity.dxf.start.x),
                    start_y=float(entity.dxf.start.y),
                    end_x=float(entity.dxf.end.x),
                    end_y=float(entity.dxf.end.y),
                )
            )
            continue

        if entity_type == "ARC":
            entities.append(
                RawArc(
                    center_x=float(entity.dxf.center.x),
                    center_y=float(entity.dxf.center.y),
                    radius=float(entity.dxf.radius),
                    start_angle_deg=float(entity.dxf.start_angle),
                    end_angle_deg=float(entity.dxf.end_angle),
                )
            )
            continue

        if entity_type == "CIRCLE":
            entities.append(
                RawCircle(
                    center_x=float(entity.dxf.center.x),
                    center_y=float(entity.dxf.center.y),
                    radius=float(entity.dxf.radius),
                )
            )
            continue

        if entity_type == "LWPOLYLINE":
            vertices: list[tuple[float, float]] = [
                (float(point[0]), float(point[1])) for point in entity.get_points()
            ]
            entities.append(
                RawLWPolyline(
                    vertices=vertices,
                    is_closed=bool(entity.closed),
                )
            )

    logger.info(
        "Parsed DXF %s: %d supported entities",
        file_path,
        len(entities),
    )
    return entities
