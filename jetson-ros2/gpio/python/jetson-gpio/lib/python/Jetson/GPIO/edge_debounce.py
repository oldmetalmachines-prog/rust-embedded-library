"""GPIO edge debouncing utilities.

This module provides a small stateful debouncer suitable for polling-based
GPIO readers on robots and embedded Linux systems.
"""

from __future__ import annotations


class EdgeDebouncer:
    """Debounce a raw boolean signal and detect debounced edges.

    Parameters
    ----------
    debounce_seconds:
        Minimum time (seconds) the raw state must remain unchanged before the
        stable output is updated.
    initial_state:
        Initial debounced state.
    """

    def __init__(self, debounce_seconds: float, initial_state: bool = False) -> None:
        if debounce_seconds < 0:
            raise ValueError("debounce_seconds must be non-negative")

        self.debounce_seconds = float(debounce_seconds)
        self._debounced_state = bool(initial_state)
        self._candidate_state = bool(initial_state)
        self._candidate_since = 0.0
        self._rose = False
        self._fell = False

    def update(self, raw_state: bool, timestamp: float) -> bool:
        """Ingest a raw sample and return the current debounced state."""
        raw = bool(raw_state)
        t = float(timestamp)

        # Clear one-shot edge flags at the start of each update cycle.
        self._rose = False
        self._fell = False

        # Track candidate transitions and when they began.
        if raw != self._candidate_state:
            self._candidate_state = raw
            self._candidate_since = t

        # Promote candidate to debounced state after the hold time elapses.
        if self._candidate_state != self._debounced_state:
            if (t - self._candidate_since) >= self.debounce_seconds:
                previous = self._debounced_state
                self._debounced_state = self._candidate_state
                self._rose = (not previous) and self._debounced_state
                self._fell = previous and (not self._debounced_state)

        return self._debounced_state

    def rose(self) -> bool:
        """Return True if the most recent update produced a rising edge."""
        return self._rose

    def fell(self) -> bool:
        """Return True if the most recent update produced a falling edge."""
        return self._fell
