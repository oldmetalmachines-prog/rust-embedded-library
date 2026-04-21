"""Quadrature encoder helpers for wrap-safe velocity estimation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EncoderSample:
    """A single tick/time sample from an encoder counter."""

    ticks: int
    timestamp_s: float


class QuadratureEncoderVelocityEstimator:
    """Estimate angular velocity from encoder ticks with counter wraparound support.

    Counter values are treated as unsigned integers in range
    ``[0, counter_max]`` and converted into the shortest signed delta.
    """

    def __init__(self, ticks_per_revolution: int, counter_max: int = 65535) -> None:
        if ticks_per_revolution <= 0:
            raise ValueError("ticks_per_revolution must be > 0")
        if counter_max <= 0:
            raise ValueError("counter_max must be > 0")

        self.ticks_per_revolution = ticks_per_revolution
        self.counter_max = counter_max
        self._range = counter_max + 1
        self._half = self._range // 2

    def delta_ticks(self, previous: int, current: int) -> int:
        """Return shortest signed tick delta from previous to current."""
        raw = int(current) - int(previous)
        if raw > self._half:
            return raw - self._range
        if raw < -self._half:
            return raw + self._range
        return raw

    def velocity_rps(self, previous: EncoderSample, current: EncoderSample) -> float:
        """Return shaft velocity in revolutions per second."""
        dt = current.timestamp_s - previous.timestamp_s
        if dt <= 0:
            raise ValueError("timestamp must be strictly increasing")

        ticks = self.delta_ticks(previous.ticks, current.ticks)
        return (ticks / self.ticks_per_revolution) / dt
