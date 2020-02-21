"""Test for npzheader"""
# =============================================================================
# ---- Import
# =============================================================================
# Local imports
from npzheader.parser import get_headers_of_numpy, ItemInfo
from npzheader.viewer import HeaderViewer


# =============================================================================
# ---- Tests
# =============================================================================
def test_viewer(qtbot):
    widget = HeaderViewer('data1.npy')
    qtbot.addWidget(widget)

    assert widget.table_for_info.item(0, 0).text() == 'data1'
    assert widget.table_for_info.item(0, 1).text() == '(50,) float64'


def test_parse_npy_header():
    ret = get_headers_of_numpy('data1.npy')

    expect = {"data1": ItemInfo((50,), 'float64', None)}

    assert ret == expect


def test_parse_npz_header():
    ret = get_headers_of_numpy('data1.npz')

    expect = {"val1": ItemInfo((), 'int64', -5),
              "val2": ItemInfo((), 'float64', -3.0),
              "val3": ItemInfo((), 'complex128', (1 + 1j)),
              "val4": ItemInfo((), '<U7', 'dhrwodn'),
              "array1": ItemInfo((50,), 'float64', None)}

    assert ret == expect


def test_parse_mat_header():
    ret = get_headers_of_numpy('data1.mat')

    expect = {"array1": ItemInfo((3, 5), 'double', None),
              "array2": ItemInfo((1, 100), 'double', None),
              "val1": ItemInfo((1, 1), 'double', 1),
              "val2": ItemInfo((1, 1), 'double', 3.5),
              "val3": ItemInfo((1,), 'char', 'dhrwodn')}

    assert ret == expect
