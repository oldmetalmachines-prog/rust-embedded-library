from common.python.robotics.motor_control import MotorSpeedController, SpeedOutOfRangeError


def test_set_speed_nominal_50_percent():
    ctl = MotorSpeedController(max_delta_percent=100.0)
    result = ctl.set_speed(50)

    assert result["applied_percent"] == 50.0
    assert result["pwm_us"] == 1500
    assert "50.0%" in result["message"]


def test_invalid_speed_above_range_raises():
    ctl = MotorSpeedController()
    try:
        ctl.set_speed(105)
        assert False, "Expected SpeedOutOfRangeError"
    except SpeedOutOfRangeError as exc:
        assert "between 0 and 100" in str(exc)


def test_invalid_speed_below_range_raises():
    ctl = MotorSpeedController()
    try:
        ctl.set_speed(-10)
        assert False, "Expected SpeedOutOfRangeError"
    except SpeedOutOfRangeError as exc:
        assert "between 0 and 100" in str(exc)


def test_deadband_snaps_small_values_to_zero():
    ctl = MotorSpeedController(deadband_percent=2.0, max_delta_percent=100.0)
    result = ctl.set_speed(1.9)
    assert result["applied_percent"] == 0.0
    assert result["pwm_us"] == 1000


def test_slew_rate_limits_large_step_commands():
    ctl = MotorSpeedController(max_delta_percent=10.0)

    r1 = ctl.set_speed(0)
    r2 = ctl.set_speed(80)

    assert r1["applied_percent"] == 0.0
    assert r2["applied_percent"] == 10.0
    assert r2["pwm_us"] == 1100
