"""GPIO pin control utility with in-memory state.

This module provides a small hardware-agnostic abstraction suitable for unit
tests and higher-level robotics control logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass(frozen=True)
class _PinState:
    mode: str
    value: int


class GPIOControl:
    """Manage digital GPIO pin mode and values.

    Parameters
    ----------
    available_pins:
        Iterable of pin numbers that this controller is allowed to access.
    """

    VALID_MODES = {"input", "output"}

    def __init__(self, available_pins: Iterable[int]):
        pins = list(available_pins)
        if not pins:
            raise ValueError("available_pins must contain at least one pin")
        if any((not isinstance(pin, int)) or pin < 0 for pin in pins):
            raise ValueError("available_pins must be non-negative integers")

        self._available_pins = set(pins)
        self._pins: Dict[int, _PinState] = {
            pin: _PinState(mode="input", value=0) for pin in self._available_pins
        }

    def set_mode(self, pin: int, mode: str) -> None:
        """Set GPIO mode for a pin.

        Raises
        ------
        ValueError
            If pin or mode is invalid.
        """

        self._validate_pin(pin)
        if mode not in self.VALID_MODES:
            raise ValueError(f"invalid mode: {mode}")

        prev = self._pins[pin]
        self._pins[pin] = _PinState(mode=mode, value=prev.value)

    def write_value(self, pin: int, value: int) -> None:
        """Write a digital value (0 or 1) to an output pin.

        Raises
        ------
        ValueError
            If pin/value is invalid.
        RuntimeError
            If the pin is not configured as output.
        """

        self._validate_pin(pin)
        if value not in (0, 1):
            raise ValueError("digital value must be 0 or 1")

        prev = self._pins[pin]
        if prev.mode != "output":
            raise RuntimeError("cannot write to a pin not set to output mode")

        self._pins[pin] = _PinState(mode=prev.mode, value=value)

    def read_value(self, pin: int) -> int:
        """Read the current digital value for a pin.

        Raises
        ------
        ValueError
            If pin is invalid.
        """

        self._validate_pin(pin)
        return self._pins[pin].value

    def _validate_pin(self, pin: int) -> None:
        if pin not in self._available_pins:
            raise ValueError(f"invalid pin: {pin}")
