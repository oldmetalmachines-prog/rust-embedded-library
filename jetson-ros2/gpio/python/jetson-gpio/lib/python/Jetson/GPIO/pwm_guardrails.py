"""Utilities for safer PWM command handling in robotics control loops."""

from __future__ import annotations

import math

DEFAULT_MIN_FREQUENCY_HZ = 1.0
DEFAULT_MAX_FREQUENCY_HZ = 1_000_000.0


def clamp_duty_cycle(duty_cycle: float) -> float:
    """Clamp PWM duty cycle to the safe [0.0, 100.0] range.

    Raises:
        ValueError: If duty_cycle is NaN or not finite.
    """
    value = float(duty_cycle)
    if not math.isfinite(value):
        raise ValueError("duty_cycle must be a finite number")
    if value < 0.0:
        return 0.0
    if value > 100.0:
        return 100.0
    return value


def validate_frequency(
    frequency_hz: float,
    *,
    min_hz: float = DEFAULT_MIN_FREQUENCY_HZ,
    max_hz: float = DEFAULT_MAX_FREQUENCY_HZ,
) -> float:
    """Validate PWM frequency bounds and return the normalized float value."""
    freq = float(frequency_hz)
    low = float(min_hz)
    high = float(max_hz)

    if not math.isfinite(freq):
        raise ValueError("frequency_hz must be a finite number")
    if not math.isfinite(low) or not math.isfinite(high):
        raise ValueError("min_hz and max_hz must be finite numbers")
    if low <= 0:
        raise ValueError("min_hz must be > 0")
    if high < low:
        raise ValueError("max_hz must be >= min_hz")
    if freq < low or freq > high:
        raise ValueError(
            f"frequency_hz must be between {low:g} and {high:g} (got {freq:g})"
        )
    return freq


def normalize_pwm_command(
    frequency_hz: float,
    duty_cycle: float,
    *,
    min_hz: float = DEFAULT_MIN_FREQUENCY_HZ,
    max_hz: float = DEFAULT_MAX_FREQUENCY_HZ,
) -> tuple[float, float]:
    """Return a validated (frequency_hz, duty_cycle) tuple for PWM APIs."""
    return (
        validate_frequency(frequency_hz, min_hz=min_hz, max_hz=max_hz),
        clamp_duty_cycle(duty_cycle),
    )
