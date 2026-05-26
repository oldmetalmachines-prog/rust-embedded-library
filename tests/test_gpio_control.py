import pytest

from electronics.gpio_control import GPIOControl


def test_initialization_requires_nonempty_valid_pin_list():
    with pytest.raises(ValueError):
        GPIOControl([])

    with pytest.raises(ValueError):
        GPIOControl([1, -2])


def test_set_mode_accepts_valid_modes_and_rejects_invalid_mode():
    gpio = GPIOControl([2, 4])

    gpio.set_mode(2, "output")
    gpio.write_value(2, 1)
    assert gpio.read_value(2) == 1

    with pytest.raises(ValueError):
        gpio.set_mode(2, "analog")


def test_invalid_pin_raises_for_all_operations():
    gpio = GPIOControl([1, 3])

    with pytest.raises(ValueError):
        gpio.set_mode(99, "output")

    with pytest.raises(ValueError):
        gpio.write_value(99, 1)

    with pytest.raises(ValueError):
        gpio.read_value(99)


def test_write_requires_output_mode_and_binary_value():
    gpio = GPIOControl([7])

    with pytest.raises(RuntimeError):
        gpio.write_value(7, 1)

    gpio.set_mode(7, "output")

    with pytest.raises(ValueError):
        gpio.write_value(7, 2)

    gpio.write_value(7, 0)
    assert gpio.read_value(7) == 0

    gpio.write_value(7, 1)
    assert gpio.read_value(7) == 1
