"""Test for npzheader"""
# =============================================================================
# ---- Import
# =============================================================================
# Local imports
from npzheader.parser import get_headers_of_numpy


# =============================================================================
# ---- Tests
# =============================================================================
def test_parse_npy_header():
    names, shapes, dtypes, values = get_headers_of_numpy('data1.npy')

    assert names == ['data1']
    assert shapes == [(50,)]
    assert dtypes == ['float64']
    assert values == [None]


def test_parse_npz_header():
    names, shapes, dtypes, values = get_headers_of_numpy('data1.npz')

    assert names == ['val1', 'val2', 'val3', 'val4', 'array1']
    assert shapes == [(), (), (), (), (50,)]
    assert dtypes == ['int64', 'float64', 'complex128', '<U7', 'float64']
    assert values == [-5, -3.0, (1 + 1j), 'dhrwodn', None]


def test_parse_mat_header():
    names, shapes, dtypes, values = get_headers_of_numpy('data1.mat')

    assert names == ['array1', 'array2', 'val1', 'val2', 'val3']
    assert shapes == [(3, 5), (1, 100), (1, 1), (1, 1), (1,)]
    assert dtypes == ['double', 'double', 'double', 'double', 'char']
    assert values == [None, None, 1, 3.5, 'dhrwodn']
