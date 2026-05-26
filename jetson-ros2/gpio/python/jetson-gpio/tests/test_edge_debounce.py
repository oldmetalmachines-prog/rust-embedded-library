import pathlib
import sys

import pytest

LIB_ROOT = pathlib.Path(__file__).resolve().parents[1] / "lib" / "python"
sys.path.insert(0, str(LIB_ROOT))

from Jetson.GPIO.edge_debounce import EdgeDebouncer


def test_negative_debounce_rejected() -> None:
    with pytest.raises(ValueError):
        EdgeDebouncer(-0.001)


def test_chatter_inside_window_does_not_flip_output() -> None:
    d = EdgeDebouncer(0.05, initial_state=False)

    assert d.update(False, 0.00) is False
    assert d.rose() is False
    assert d.fell() is False

    # Rising chatter begins but does not hold long enough.
    assert d.update(True, 0.01) is False
    assert d.update(False, 0.03) is False
    assert d.update(True, 0.04) is False

    # Held high long enough now -> one rising edge.
    assert d.update(True, 0.10) is True
    assert d.rose() is True
    assert d.fell() is False


def test_rising_and_falling_edges_are_reported_on_transition_update() -> None:
    d = EdgeDebouncer(0.02, initial_state=False)

    # Rising transition.
    assert d.update(True, 1.00) is False
    assert d.update(True, 1.03) is True
    assert d.rose() is True
    assert d.fell() is False

    # Steady high: no new edges.
    assert d.update(True, 1.04) is True
    assert d.rose() is False
    assert d.fell() is False

    # Falling transition.
    assert d.update(False, 1.06) is True
    assert d.update(False, 1.09) is False
    assert d.rose() is False
    assert d.fell() is True
