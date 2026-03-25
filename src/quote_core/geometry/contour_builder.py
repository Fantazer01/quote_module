from __future__ import annotations

import logging

import math
from typing import List

from quote_core.geometry.primitives import Contour, Point, Segment

logger = logging.getLogger(__name__)


def _points_close(a: Point, b: Point, eps: float) -> bool:
    return math.hypot(a.x - b.x, a.y - b.y) <= eps


def _flip_segment(segment: Segment) -> Segment:
    return Segment(start=segment.end, end=segment.start)


def build_contours(segments: list[Segment], eps: float = 1e-4) -> list[Contour]:
    """
    Group segments into chains; mark closed when endpoints meet within eps.

    Simple greedy connection: extend forward from the chain end, then backward
    from the chain start. Remaining segments start new chains.
    """
    if not segments:
        return []

    remaining: List[Segment] = list(segments)
    contours: list[Contour] = []

    while remaining:
        chain: list[Segment] = [remaining.pop(0)]

        def grow_forward() -> bool:
            current_end = chain[-1].end
            index = 0
            while index < len(remaining):
                candidate = remaining[index]
                if _points_close(candidate.start, current_end, eps):
                    chain.append(candidate)
                    remaining.pop(index)
                    return True
                if _points_close(candidate.end, current_end, eps):
                    chain.append(_flip_segment(candidate))
                    remaining.pop(index)
                    return True
                index += 1
            return False

        def grow_backward() -> bool:
            current_start = chain[0].start
            index = 0
            while index < len(remaining):
                candidate = remaining[index]
                if _points_close(candidate.end, current_start, eps):
                    chain.insert(0, candidate)
                    remaining.pop(index)
                    return True
                if _points_close(candidate.start, current_start, eps):
                    chain.insert(0, _flip_segment(candidate))
                    remaining.pop(index)
                    return True
                index += 1
            return False

        growing = True
        while growing:
            growing = grow_forward() or grow_backward()

        is_closed = _points_close(chain[0].start, chain[-1].end, eps)
        logger.debug("Contour №%d, length: %s", len(contours) + 1, sum(segment.length for segment in chain))
        contours.append(Contour(segments=chain, is_closed=is_closed))

    return contours
