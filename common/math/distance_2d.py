"""2D distance helpers for robotics coordinate math."""

from __future__ import annotations

import math
from collections.abc import Sequence


Number = int | float


def _validate_point(point: Sequence[Number], name: str) -> tuple[float, float]:
    if not isinstance(point, Sequence) or isinstance(point, (str, bytes)):
        raise TypeError(f"{name} must be a sequence of two numeric values")
    if len(point) != 2:
        raise ValueError(f"{name} must contain exactly two values")

    x, y = point
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError(f"{name} values must be numeric")

    x_f, y_f = float(x), float(y)
    if not math.isfinite(x_f) or not math.isfinite(y_f):
        raise ValueError(f"{name} values must be finite")

    return x_f, y_f


def euclidean_distance_2d(point1: Sequence[Number], point2: Sequence[Number]) -> float:
    """Return Euclidean distance between two 2D points.

    Args:
        point1: Sequence with two finite numeric values (x1, y1).
        point2: Sequence with two finite numeric values (x2, y2).

    Returns:
        Non-negative Euclidean distance as float.
    """

    x1, y1 = _validate_point(point1, "point1")
    x2, y2 = _validate_point(point2, "point2")
    return math.hypot(x2 - x1, y2 - y1)
