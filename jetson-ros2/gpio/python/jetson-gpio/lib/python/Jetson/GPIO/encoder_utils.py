"""Utility helpers for wheel-encoder pulse processing.

These helpers are pure functions so they can be unit-tested without hardware.
"""

from __future__ import annotations

import math


def calculate_distance(
    pulses: int,
    wheel_diameter_m: float,
    pulses_per_revolution: int,
) -> float:
    """Compute traveled distance in meters from encoder pulses.

    Args:
        pulses: Signed pulse count; negative pulses indicate reverse travel.
        wheel_diameter_m: Wheel diameter in meters. Must be > 0.
        pulses_per_revolution: Encoder pulses per one full wheel revolution. Must be > 0.

    Returns:
        Distance traveled in meters. Negative value represents reverse motion.
    """
    if wheel_diameter_m <= 0:
        raise ValueError("wheel_diameter_m must be > 0")
    if pulses_per_revolution <= 0:
        raise ValueError("pulses_per_revolution must be > 0")

    revolutions = pulses / pulses_per_revolution
    return revolutions * (math.pi * wheel_diameter_m)


def convert_pulses_to_rpm(
    pulses: int,
    interval_seconds: float,
    pulses_per_revolution: int,
) -> float:
    """Convert pulses observed over an interval into RPM.

    Args:
        pulses: Pulse count observed during the interval.
        interval_seconds: Measurement interval in seconds. Must be > 0.
        pulses_per_revolution: Encoder pulses per one full revolution. Must be > 0.

    Returns:
        Rotational speed in revolutions per minute.
    """
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be > 0")
    if pulses_per_revolution <= 0:
        raise ValueError("pulses_per_revolution must be > 0")

    revolutions = pulses / pulses_per_revolution
    return (revolutions / interval_seconds) * 60.0
