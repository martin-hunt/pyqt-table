from PySide import QtGui, QtCore
import numpy as np
from mod_col_ui import Ui_tableModColDialog

class AddDialog(QtGui.QDialog,  Ui_tableModColDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

    def getValue(self):
        return self.tableAddLine.text()

class BTable(QtGui.QTableWidget):
    def __init__(self, parent = None):
        super(BTable, self).__init__(parent)

        # connect cell change callback
        self.cellChanged.connect(self.cell_changed)

        # connect table popup
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.table_popup)

        # connect header popup
        headers = self.horizontalHeader()
        headers.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        headers.customContextMenuRequested.connect(self.col_table_popup)

    def table_popup(self, pos):
        menu = QtGui.QMenu()
        dumpAction = menu.addAction("Write out contents of table")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == dumpAction:
            print self.read_array()

    def col_table_popup(self, pos):
        try:
            pop_col = self.selectionModel().selection().indexes()[0].column()
        except:
            return
        menu = QtGui.QMenu()
        modAction = menu.addAction("Change the Name for this Column")
        menu.addSeparator()
        delAction = menu.addAction("Delete This Column")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == delAction:
            print 'remove column', pop_col
            arr = self.read_array()
            arr = np.delete(arr, pop_col, axis=1)
            header = self.read_header()
            del header[pop_col]
            self.write_array(arr, header)
        elif action == modAction:
            print 'change name of column', pop_col
            dia = AddDialog()
            if dia.exec_():
                name = dia.getValue()
                header = self.read_header()
                header[pop_col] =  name
                self.write_header(header)

    def cell_changed(self, r, c):
        if r >= self.rows:
            self.rows = r+1
            self.setRowCount(self.rows+1)
        elif c >= self.cols:
            self.cols = c+1
            self.setColumnCount(self.cols+1)
            header = self.read_header()
            if len(header) < self.cols:
                header.append('Col%s' % self.cols)
                self.write_header(header)

    ##############################################
    # read/write parameters. These must be the only way
    # to read or write the contents of the table.
    # We could use properties to do this.
    ##############################################

    def write_header(self, header):
        self.setHorizontalHeaderLabels(header)
        self._header = header

    def read_header(self):
        return self._header

    def write_array(self, num, header = None):
        self.rows, self.cols = num.shape
        self.clear()
        # always have the table bigger than
        # the data so more can be added
        self.setColumnCount(self.cols+1)
        self.setRowCount(self.rows+1)
        for r in range(self.rows):
            for c in range(self.cols):
                item = QtGui.QTableWidgetItem(str(num[r,c]))
                self.setItem(r, c, item)
        if header is not None:
            self.write_header(header)

    def read_array(self):
        arr = np.zeros((self.rows, self.cols))
        for r in range(self.rows):
            for c in range(self.cols):
                item = self.item(r,c)
                if item is None:
                    print 'Error: incomplete array at row %s, col %s' % (r,c)
                    return None
                else:
                    try:
                        arr[r,c] = float(item.text())
                    except:
                        arr[r,c] = np.nan
        return arr

