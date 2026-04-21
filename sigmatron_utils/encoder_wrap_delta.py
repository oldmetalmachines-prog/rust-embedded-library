"""Utilities for modular encoder position arithmetic."""


def compute_wrap_delta(current_count: int, previous_count: int, max_count: int) -> int:
    """Return shortest signed delta from previous_count to current_count.

    Args:
        current_count: Current encoder tick count in [0, max_count-1].
        previous_count: Previous encoder tick count in [0, max_count-1].
        max_count: Modulus of encoder counter (ticks per revolution).

    Returns:
        Signed delta in ticks, constrained to [-max_count//2, max_count//2].

    Raises:
        ValueError: If max_count < 2 or either count is outside range.
        TypeError: If inputs are not integers.
    """
    for name, value in (
        ("current_count", current_count),
        ("previous_count", previous_count),
        ("max_count", max_count),
    ):
        if not isinstance(value, int):
            raise TypeError(f"{name} must be int")

    if max_count < 2:
        raise ValueError("max_count must be >= 2")

    if not (0 <= current_count < max_count):
        raise ValueError("current_count out of range")
    if not (0 <= previous_count < max_count):
        raise ValueError("previous_count out of range")

    delta = current_count - previous_count
    half = max_count // 2

    if delta > half:
        delta -= max_count
    elif delta < -half:
        delta += max_count

    return delta
