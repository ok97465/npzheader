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
    names, shapes, dtypes = get_headers_of_numpy('data1.npy')

    assert names == ['data1']
    assert shapes == [(50,)]
    assert dtypes == ['float64']


def test_parse_npz_header():
    names, shapes, dtypes = get_headers_of_numpy('data1.npz')

    assert names == ['val1', 'val2', 'val3', 'array1']
    assert shapes == [(), (), (), (50,)]
    assert dtypes == ['int64', 'int64', '<U3', 'float64']
