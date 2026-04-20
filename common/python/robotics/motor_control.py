from __future__ import annotations

from dataclasses import dataclass


class SpeedOutOfRangeError(ValueError):
    """Raised when a commanded speed is outside 0..100%."""


@dataclass
class MotorSpeedController:
    """Map speed percent commands to PWM pulse widths with simple safety shaping.

    - Accepts user speed commands in range 0..100 (%).
    - Applies a configurable deadband near zero to avoid motor twitch.
    - Applies a slew-rate limit between successive set_speed() calls.
    - Converts final command to PWM microseconds.
    """

    min_pwm_us: int = 1000
    max_pwm_us: int = 2000
    deadband_percent: float = 2.0
    max_delta_percent: float = 20.0
    _last_speed_percent: float = 0.0

    def _validate_speed(self, speed_percent: float) -> float:
        try:
            value = float(speed_percent)
        except (TypeError, ValueError) as exc:
            raise SpeedOutOfRangeError("Speed value must be numeric and between 0 and 100.") from exc

        if not 0.0 <= value <= 100.0:
            raise SpeedOutOfRangeError("Speed value must be between 0 and 100.")
        return value

    def _apply_deadband(self, speed_percent: float) -> float:
        return 0.0 if speed_percent < self.deadband_percent else speed_percent

    def _apply_slew_rate(self, target_percent: float) -> float:
        delta = target_percent - self._last_speed_percent
        if delta > self.max_delta_percent:
            return self._last_speed_percent + self.max_delta_percent
        if delta < -self.max_delta_percent:
            return self._last_speed_percent - self.max_delta_percent
        return target_percent

    def speed_to_pwm_us(self, speed_percent: float) -> int:
        speed_percent = self._validate_speed(speed_percent)
        span = self.max_pwm_us - self.min_pwm_us
        return int(round(self.min_pwm_us + (speed_percent / 100.0) * span))

    def set_speed(self, speed_percent: float) -> dict[str, float | int | str]:
        requested = self._validate_speed(speed_percent)
        with_deadband = self._apply_deadband(requested)
        applied = self._apply_slew_rate(with_deadband)
        self._last_speed_percent = applied
        pwm_us = self.speed_to_pwm_us(applied)

        return {
            "requested_percent": requested,
            "applied_percent": applied,
            "pwm_us": pwm_us,
            "message": f"Motor speed set to {applied:.1f}% ({pwm_us}us PWM)",
        }
