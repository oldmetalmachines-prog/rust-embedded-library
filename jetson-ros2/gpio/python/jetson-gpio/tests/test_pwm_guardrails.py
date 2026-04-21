from pwm_guardrails import (
    clamp_duty_cycle,
    normalize_pwm_command,
    validate_frequency,
)


def test_clamp_duty_cycle_bounds():
    assert clamp_duty_cycle(-7.5) == 0.0
    assert clamp_duty_cycle(0) == 0.0
    assert clamp_duty_cycle(41.25) == 41.25
    assert clamp_duty_cycle(120) == 100.0


def test_clamp_duty_cycle_rejects_non_finite():
    try:
        clamp_duty_cycle(float("nan"))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_validate_frequency_accepts_in_range_values():
    assert validate_frequency(1000) == 1000.0
    assert validate_frequency(50.5, min_hz=10, max_hz=100) == 50.5


def test_validate_frequency_rejects_out_of_range_values():
    for value in (0, -1, 1000.1):
        try:
            validate_frequency(value, min_hz=1, max_hz=1000)
            assert False, "expected ValueError"
        except ValueError:
            pass


def test_validate_frequency_rejects_invalid_range():
    try:
        validate_frequency(100, min_hz=1000, max_hz=100)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_normalize_pwm_command_combines_validation_and_clamp():
    frequency, duty = normalize_pwm_command(500, 133.3, min_hz=10, max_hz=1000)
    assert frequency == 500.0
    assert duty == 100.0
