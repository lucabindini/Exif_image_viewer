from PyQt5 import QtWidgets
import qdarkgraystyle

import image_viewer_widget


class MainWindow(QtWidgets.QMainWindow):

    ICONS_PATH = 'img/icons/fugue-icons-3.5.6/icons/'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
        self.setWindowTitle('Exif Image Viewer')
        self.resize(800, 600)
        self.setMinimumSize(self.size()/2)

        self.setCentralWidget(
            image_viewer_widget.ImageViewerWidget(parent=self))
