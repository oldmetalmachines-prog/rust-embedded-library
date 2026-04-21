"""Encoder math helpers for mobile robot odometry and drivetrain calculations."""

from __future__ import annotations


def calculate_position(
    encoder_ticks: int,
    gear_ratio: float,
    ticks_per_motor_rev: int = 2048,
) -> float:
    """Return output-shaft revolutions from raw encoder ticks.

    Args:
        encoder_ticks: Signed encoder ticks counted at motor shaft.
        gear_ratio: Motor revolutions per output-shaft revolution (must be > 0).
        ticks_per_motor_rev: Encoder ticks per one motor revolution (must be > 0).

    Returns:
        Output shaft position in revolutions. Can be negative when ticks are negative.
    """
    if gear_ratio <= 0:
        raise ValueError("gear_ratio must be > 0")
    if ticks_per_motor_rev <= 0:
        raise ValueError("ticks_per_motor_rev must be > 0")

    motor_revs = encoder_ticks / float(ticks_per_motor_rev)
    return motor_revs / gear_ratio


def calculate_distance(position_revs: float, wheel_circumference_m: float) -> float:
    """Convert output-shaft revolutions into linear travel distance.

    Args:
        position_revs: Output shaft revolutions.
        wheel_circumference_m: Wheel circumference in meters (must be >= 0).

    Returns:
        Signed linear distance in meters.
    """
    if wheel_circumference_m < 0:
        raise ValueError("wheel_circumference_m must be >= 0")

    return position_revs * wheel_circumference_m
