"""Angle conversion and heading helpers for robotics control loops."""

from __future__ import annotations

import math


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians."""
    return degrees * (math.pi / 180.0)


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees."""
    return radians * (180.0 / math.pi)


def normalize_degrees(degrees: float) -> float:
    """Normalize an angle to the range [-180, 180)."""
    wrapped = (degrees + 180.0) % 360.0 - 180.0
    # Avoid returning -0.0 in telemetry/control outputs.
    return 0.0 if wrapped == 0.0 else wrapped


def shortest_angular_distance_deg(from_deg: float, to_deg: float) -> float:
    """Return shortest signed turn from from_deg to to_deg in degrees.

    Positive means counter-clockwise turn, negative clockwise.
    """
    return normalize_degrees(to_deg - from_deg)
