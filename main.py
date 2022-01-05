import sys

from PyQt5 import QtWidgets

import main_window

app = QtWidgets.QApplication(sys.argv)
window = main_window.MainWindow()
window.show()
app.exec()
