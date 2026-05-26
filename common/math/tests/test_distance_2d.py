import math

import pytest

from common.math.distance_2d import euclidean_distance_2d


@pytest.mark.parametrize(
    ("point1", "point2", "expected"),
    [
        ((0, 0), (3, 4), 5.0),
        ((1, 1), (4, 5), 5.0),
        ((0, 0), (0, 0), 0.0),
        ((-1, -1), (2, 3), 5.0),
        ((2.5, -0.5), (2.5, -0.5), 0.0),
    ],
)
def test_euclidean_distance_2d_nominal(point1, point2, expected):
    assert math.isclose(euclidean_distance_2d(point1, point2), expected, rel_tol=1e-12)


def test_euclidean_distance_2d_rejects_wrong_arity():
    with pytest.raises(ValueError):
        euclidean_distance_2d((0, 1, 2), (0, 1))


def test_euclidean_distance_2d_rejects_non_numeric_values():
    with pytest.raises(TypeError):
        euclidean_distance_2d((0, "x"), (1, 1))


def test_euclidean_distance_2d_rejects_non_finite_values():
    with pytest.raises(ValueError):
        euclidean_distance_2d((0.0, float("nan")), (1.0, 2.0))
