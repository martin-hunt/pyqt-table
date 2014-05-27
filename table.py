#!/usr/bin/env python

from PySide import QtGui
from table_ui import Ui_Form
import numpy as np

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    n = np.array([[1,2,3],[4,5,6],[7,8,9], [10,11,12]])
    header = ['Col1', 'Col2', 'Col3']
    ui.dataTable.write_array(n, header)
    print ui.dataTable.read_header()
    print ui.dataTable.read_array()
    sys.exit(app.exec_())

