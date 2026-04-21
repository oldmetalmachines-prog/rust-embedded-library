import math

import pytest

from quadrature_encoder import EncoderSample, QuadratureEncoderVelocityEstimator


def test_delta_ticks_no_wrap_positive() -> None:
    est = QuadratureEncoderVelocityEstimator(ticks_per_revolution=1024, counter_max=65535)
    assert est.delta_ticks(100, 140) == 40


def test_delta_ticks_no_wrap_negative() -> None:
    est = QuadratureEncoderVelocityEstimator(ticks_per_revolution=1024, counter_max=65535)
    assert est.delta_ticks(140, 100) == -40


def test_delta_ticks_wrap_forward() -> None:
    est = QuadratureEncoderVelocityEstimator(ticks_per_revolution=1024, counter_max=65535)
    assert est.delta_ticks(65530, 5) == 11


def test_delta_ticks_wrap_reverse() -> None:
    est = QuadratureEncoderVelocityEstimator(ticks_per_revolution=1024, counter_max=65535)
    assert est.delta_ticks(5, 65530) == -11


def test_velocity_rps_forward_wrap() -> None:
    est = QuadratureEncoderVelocityEstimator(ticks_per_revolution=2048, counter_max=65535)
    prev = EncoderSample(ticks=65520, timestamp_s=10.0)
    curr = EncoderSample(ticks=16, timestamp_s=10.2)
    expected = (32 / 2048) / 0.2
    assert math.isclose(est.velocity_rps(prev, curr), expected, rel_tol=1e-12)


def test_velocity_requires_increasing_timestamp() -> None:
    est = QuadratureEncoderVelocityEstimator(ticks_per_revolution=2048, counter_max=65535)
    prev = EncoderSample(ticks=100, timestamp_s=1.0)
    curr = EncoderSample(ticks=120, timestamp_s=1.0)
    with pytest.raises(ValueError, match="strictly increasing"):
        est.velocity_rps(prev, curr)


def test_reject_invalid_constructor_args() -> None:
    with pytest.raises(ValueError):
        QuadratureEncoderVelocityEstimator(0)
    with pytest.raises(ValueError):
        QuadratureEncoderVelocityEstimator(1024, counter_max=0)
