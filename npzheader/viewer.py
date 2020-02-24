"""Viewer GUI."""
# ---- Import
# Standard library imports
import sys
import os
import os.path as osp
from urllib.parse import unquote

# Third party imports
from qtpy.QtCore import Signal, QUrl, QMimeData
from qtpy.QtGui import QDrag
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
        table.file_path = path

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
        """Reimplement Qt method.
           Inform Qt about the types of data that the widget accepts"""
        source = e.mimeData()
        if source.hasUrls() and len(source.urls()) == 1:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """Drag and Drop - Move event."""
        source = e.mimeData()
        if source.hasUrls() and len(source.urls()) == 1:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """Reimplement Qt method.
           Send signal to viewer"""
        # path = e.mimeData().urls()[0].toLocalFile()
        path_url = e.mimeData().urls()[0]
        path = _process_mime_path(unquote(path_url).toString(), None)
        self.sig_view_path.emit(path)


def _process_mime_path(path, extlist):
    """Convert url of mimedata to string
    Code From spyder ide
    """
    if path.startswith(r"file://"):
        if os.name == 'nt':
            # On Windows platforms, a local path reads: file:///c:/...
            # and a UNC based path reads like: file://server/share
            if path.startswith(r"file:///"):  # this is a local path
                path = path[8:]
            else:  # this is a unc path
                path = path[5:]
        else:
            path = path[7:]
    path = path.replace('\\', os.sep)  # Transforming backslashes
    if osp.exists(path):
        if extlist is None or osp.splitext(path)[1] in extlist:
            return path


class CustomTable(QTableWidget):
    def __init__(self, col_labels, parent):
        super().__init__(parent)
        self.setup(col_labels)
        self.file_path = None

    def setup(self, col_labels):
        """Setup attribute of customtable"""
        # Set read only
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Set header name
        self.setColumnCount(len(col_labels))
        self.setHorizontalHeaderLabels(col_labels)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Select single row
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragEnabled(True)

    def startDrag(self, e):
        """Reimplement Qt Method - handle drag event"""
        if isinstance(self.file_path, str) and len(self.file_path) > 4:
            data = QMimeData()
            data.setUrls([QUrl(self.file_path)])

            ext = self.file_path[-4:]
            if ext in [".mat", ".npz"]:
                idx_rows = set(idx.row() for idx in self.selectedIndexes())
                variable_names = [self.item(i, 0).text() for i in idx_rows]
                variable_names_one_line = ",".join(variable_names)
                data.setData('text/variable-names',
                             variable_names_one_line.encode('utf-8'))

            drag = QDrag(self)
            drag.setMimeData(data)
            drag.exec_()


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
