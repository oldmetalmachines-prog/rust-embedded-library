import math

import pytest

from Jetson.GPIO.encoder_utils import calculate_distance, convert_pulses_to_rpm


def test_calculate_distance_forward_and_reverse() -> None:
    diameter = 0.2
    ppr = 20

    forward = calculate_distance(100, diameter, ppr)
    reverse = calculate_distance(-100, diameter, ppr)

    assert math.isclose(forward, math.pi, rel_tol=1e-9)
    assert math.isclose(reverse, -math.pi, rel_tol=1e-9)


def test_convert_pulses_to_rpm() -> None:
    # 500 pulses, 10 pulses/rev -> 50 revolutions in 60 seconds -> 50 RPM.
    rpm = convert_pulses_to_rpm(500, 60.0, 10)
    assert math.isclose(rpm, 50.0, rel_tol=1e-9)


@pytest.mark.parametrize(
    "args",
    [
        (10, 0.0, 20),
        (10, -1.0, 20),
    ],
)
def test_convert_pulses_to_rpm_rejects_nonpositive_interval(args) -> None:
    with pytest.raises(ValueError):
        convert_pulses_to_rpm(*args)


@pytest.mark.parametrize(
    "args",
    [
        (10, 0.2, 0),
        (10, 0.2, -5),
    ],
)
def test_calculate_distance_rejects_nonpositive_ppr(args) -> None:
    with pytest.raises(ValueError):
        calculate_distance(*args)
