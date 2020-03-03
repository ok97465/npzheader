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
    widget = HeaderViewer('data2.npz')
    qtbot.addWidget(widget)

    assert widget.table_for_info.item(0, 0).text() == 'val1'
    assert widget.table_for_info.item(0, 1).text() == '1'
    assert widget.table_for_info.item(1, 0).text() == 'val2'
    assert widget.table_for_info.item(1, 1).text() == 'False'
    assert widget.table_for_info.item(2, 0).text() == 'val3'
    assert widget.table_for_info.item(2, 1).text() == '0'
    assert widget.table_for_info.item(3, 0).text() == 'val4'
    assert widget.table_for_info.item(3, 1).text() == '5.5'
    assert widget.table_for_info.item(4, 0).text() == 'utf'
    assert widget.table_for_info.item(4, 1).text() == 'dhrwodn'
    assert widget.table_for_info.item(5, 0).text() == 'arr'
    assert widget.table_for_info.item(5, 1).text() == '(3,) int64'


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
              "array1": ItemInfo((50,), 'float64', None),
              "structured_type": ItemInfo((1,), "[('val1', 'i1'), ('val2', '<u2'), ('valf', '<f8'), ('array1', '<f4', (3, 2)), ('array2', '<c16', (5,))]", None)}

    assert ret == expect


def test_parse_mat_header():
    ret = get_headers_of_numpy('data1.mat')

    expect = {"array1": ItemInfo((3, 5), 'double', None),
              "array2": ItemInfo((1, 100), 'double', None),
              "val1": ItemInfo((1, 1), 'double', 1),
              "val2": ItemInfo((1, 1), 'double', 3.5),
              "val3": ItemInfo((1,), 'char', 'dhrwodn'),
              "st": ItemInfo((1, 1), 'struct', None)}

    assert ret == expect
