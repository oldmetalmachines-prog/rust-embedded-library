from encoder_wrap_delta import compute_wrap_delta


def test_no_wrap_positive():
    assert compute_wrap_delta(120, 100, 1024) == 20


def test_no_wrap_negative():
    assert compute_wrap_delta(100, 120, 1024) == -20


def test_forward_wrap():
    assert compute_wrap_delta(3, 1022, 1024) == 5


def test_reverse_wrap():
    assert compute_wrap_delta(1021, 2, 1024) == -5


def test_zero_delta():
    assert compute_wrap_delta(512, 512, 1024) == 0


def test_invalid_range_raises():
    try:
        compute_wrap_delta(1024, 0, 1024)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_invalid_type_raises():
    try:
        compute_wrap_delta(1.5, 0, 1024)
        assert False, "expected TypeError"
    except TypeError:
        pass
