import math

from angle_conversion import (
    degrees_to_radians,
    normalize_degrees,
    radians_to_degrees,
    shortest_angular_distance_deg,
)


def test_degrees_to_radians_cardinal_points() -> None:
    assert degrees_to_radians(0.0) == 0.0
    assert math.isclose(degrees_to_radians(90.0), math.pi / 2, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(degrees_to_radians(180.0), math.pi, rel_tol=0, abs_tol=1e-12)


def test_radians_to_degrees_cardinal_points() -> None:
    assert radians_to_degrees(0.0) == 0.0
    assert math.isclose(radians_to_degrees(math.pi / 2), 90.0, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(radians_to_degrees(math.pi), 180.0, rel_tol=0, abs_tol=1e-12)


def test_round_trip_conversion_stability() -> None:
    for value in (-720.0, -45.5, 0.0, 13.37, 359.99, 1080.0):
        back = radians_to_degrees(degrees_to_radians(value))
        assert math.isclose(back, value, rel_tol=0, abs_tol=1e-10)


def test_normalize_degrees_basic_ranges() -> None:
    assert normalize_degrees(0.0) == 0.0
    assert normalize_degrees(360.0) == 0.0
    assert normalize_degrees(-360.0) == 0.0
    assert normalize_degrees(181.0) == -179.0
    assert normalize_degrees(-181.0) == 179.0


def test_normalize_degrees_upper_boundary_maps_to_minus_180() -> None:
    assert normalize_degrees(180.0) == -180.0
    assert normalize_degrees(540.0) == -180.0


def test_shortest_angular_distance_simple_turns() -> None:
    assert shortest_angular_distance_deg(10.0, 20.0) == 10.0
    assert shortest_angular_distance_deg(20.0, 10.0) == -10.0


def test_shortest_angular_distance_wraparound() -> None:
    assert shortest_angular_distance_deg(350.0, 10.0) == 20.0
    assert shortest_angular_distance_deg(10.0, 350.0) == -20.0


def test_shortest_angular_distance_half_turn() -> None:
    # Convention from normalize_degrees is [-180, 180), so 180 maps to -180.
    assert shortest_angular_distance_deg(0.0, 180.0) == -180.0
