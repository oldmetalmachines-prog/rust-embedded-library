import math

import pytest

from encoder_math import calculate_distance, calculate_position


def test_calculate_position_zero_ticks_is_zero_position() -> None:
    assert calculate_position(0, gear_ratio=1.0) == 0.0


def test_calculate_position_one_output_revolution() -> None:
    # 4096 ticks at 2048 ticks/rev = 2 motor revs; with 2:1 ratio => 1 output rev.
    assert calculate_position(4096, gear_ratio=2.0) == pytest.approx(1.0)


def test_calculate_position_preserves_sign() -> None:
    assert calculate_position(-2048, gear_ratio=1.0) == pytest.approx(-1.0)


def test_calculate_position_supports_custom_encoder_resolution() -> None:
    assert calculate_position(1024, gear_ratio=1.0, ticks_per_motor_rev=1024) == pytest.approx(1.0)


def test_calculate_position_rejects_non_positive_gear_ratio() -> None:
    with pytest.raises(ValueError, match="gear_ratio"):
        calculate_position(100, gear_ratio=0)


def test_calculate_position_rejects_non_positive_ticks_per_rev() -> None:
    with pytest.raises(ValueError, match="ticks_per_motor_rev"):
        calculate_position(100, gear_ratio=1, ticks_per_motor_rev=0)


def test_calculate_distance_basic() -> None:
    assert calculate_distance(2.5, wheel_circumference_m=0.4) == pytest.approx(1.0)


def test_calculate_distance_rejects_negative_circumference() -> None:
    with pytest.raises(ValueError, match="wheel_circumference_m"):
        calculate_distance(1.0, wheel_circumference_m=-0.1)


def test_calculate_distance_signed_output() -> None:
    assert math.isclose(calculate_distance(-3.0, wheel_circumference_m=0.2), -0.6)
