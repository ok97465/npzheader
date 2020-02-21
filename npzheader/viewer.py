"""Viewer GUI."""
# ---- Import
# Standard library imports
import sys
import os.path as osp
from itertools import zip_longest

# Third party imports
from qtpy.QtCore import Signal
from qtpy.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                            QTableWidget, QWidget, QAbstractItemView,
                            QHeaderView, QTableWidgetItem, QLineEdit)
import qdarkstyle

# Local imports
from npzheader.parser import get_headers_of_numpy


# ---- Code
class HeaderViewer(QMainWindow):
    """Display information of science data format."""

    def __init__(self, path=None):
        super().__init__()
        self.setMinimumSize(200, 150)
        self.setWindowTitle("Npz header viewer")

        # widget factory
        self.file_path_label = CustomLabel('drag & drop', self)
        self.file_path_label.setDragEnabled(True)
        self.err_label = QLineEdit(self)
        self.err_label.setReadOnly(True)
        self.table_for_info = CustomTable(['name', 'value'], self)

        # widget layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.file_path_label)
        vbox.addWidget(self.table_for_info)
        vbox.addWidget(self.err_label)

        central_widget = QWidget(self)
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.info_update(path)
        self.file_path_label.sig_view_path.connect(self.info_update)

    def info_update(self, path: str):
        """Update table from header of file."""
        table = self.table_for_info
        table.setRowCount(0)  # Clear table

        try:
            headers = get_headers_of_numpy(path)

            table.setRowCount(len(headers))
            for idx_row, (name, info) in enumerate(headers.items()):
                table.setItem(idx_row, 0, QTableWidgetItem(name))

                if info.value:
                    table.setItem(
                        idx_row, 1, QTableWidgetItem(
                            str(info.value)))
                else:
                    table.setItem(
                        idx_row, 1, QTableWidgetItem(
                            f'{info.shape} {info.dtype}'))
            self.err_label.setText("")
        except Exception as e:
            self.err_label.setText(repr(e))

        if isinstance(path, str):
            basename = osp.split(path)[1]
            self.file_path_label.setText(basename)
        else:
            self.file_path_label.setText("File Drag & Drop")


class CustomLabel(QLineEdit):
    """Support to Drag and drop for files."""

    sig_view_path = Signal(str)

    def __init__(self, text, parent):
        super().__init__(parent)
        self.setText(text)
        self.setReadOnly(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        source = e.mimeData()
        if source.hasUrls() and len(source.urls()) == 1:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        source = e.mimeData()
        if source.hasUrls() and len(source.urls()) == 1:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile()
        self.sig_view_path.emit(path)


class CustomTable(QTableWidget):
    def __init__(self, col_labels, parent):
        super().__init__(parent)
        self.setup(col_labels)

    def setup(self, col_labels):
        # Set read only
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Set header name
        self.setColumnCount(len(col_labels))
        self.setHorizontalHeaderLabels(col_labels)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Only one row select
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.SingleSelection)


def run():
    """Start The viewer and block until the process exits."""
    app = QApplication([])

    style_sheet = qdarkstyle.load_stylesheet_from_environment()
    app.setStyleSheet(style_sheet)

    path = None
    if len(sys.argv) > 1:
        path = sys.argv[1]
    viewer = HeaderViewer(path)
    viewer.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
