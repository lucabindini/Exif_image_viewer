from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtGui, QtCore

from model import ModelImage


class ImageViewerWidget(QtWidgets.QWidget):

    proportion = 5

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.images: list[ModelImage] = []

        h_layout = QtWidgets.QHBoxLayout()

        images_list_widget = QtWidgets.QWidget()
        images_list_layout = QtWidgets.QVBoxLayout()
        images_list = ImagesListWidget()
        images_list.currentRowChanged.connect(self.display_image)
        images_list.itemPressed.connect(self.display_image)
        images_list_layout.addWidget(images_list)
        open_image_widget = QtWidgets.QWidget()
        open_image_layout = QtWidgets.QHBoxLayout()
        open_image_layout.addStretch()
        open_image_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}image-sunset.png'), 'Open an image')
        open_image_layout.addWidget(open_image_btn)
        open_image_layout.addStretch()
        open_image_widget.setLayout(open_image_layout)
        images_list_layout.addWidget(open_image_widget)
        images_list_widget.setLayout(images_list_layout)

        display_widget = QtWidgets.QWidget()
        display_layout = QtWidgets.QVBoxLayout()
        exif_btn_widget = QtWidgets.QWidget()
        exif_btn_layout = QtWidgets.QHBoxLayout()
        exif_btn_layout.addStretch()
        exif_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}information.png'), 'Show Exif data')
        exif_btn.released.connect(self.show_exif)
        exif_btn_layout.addWidget(exif_btn)
        exif_btn_widget.setLayout(exif_btn_layout)
        display_layout.addWidget(exif_btn_widget)
        image_widget = QtWidgets.QWidget()
        image_layout = QtWidgets.QHBoxLayout()
        image_layout.addStretch()
        self.image_label = ImageQLabel()
        image_layout.addWidget(self.image_label)
        image_layout.addStretch()
        image_widget.setLayout(image_layout)
        display_layout.addWidget(image_widget)
        rotate_btn_widget = QtWidgets.QWidget()
        rotate_btn_layout = QtWidgets.QHBoxLayout()
        rotate_btn_layout.addStretch()
        left_rot_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}arrow-circle-135-left.png'), '')
        left_rot_btn.setToolTip('Rotate 90 degrees counterclockwise')
        left_rot_btn.released.connect(
            lambda: self.rotate_image(clockwise=False))
        rotate_btn_layout.addWidget(left_rot_btn)
        right_rot_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}arrow-circle.png'), '')
        right_rot_btn.setToolTip('Rotate 90 degrees clockwise')
        right_rot_btn.released.connect(
            lambda: self.rotate_image(clockwise=True))
        rotate_btn_layout.addWidget(right_rot_btn)
        rotate_btn_layout.addStretch()
        rotate_btn_widget.setLayout(rotate_btn_layout)
        display_layout.addWidget(rotate_btn_widget)
        display_widget.setLayout(display_layout)

        h_layout.addWidget(images_list_widget, 100//self.proportion)
        h_layout.addWidget(display_widget,
                           100 * (self.proportion-1) // self.proportion)
        self.setLayout(h_layout)

        #self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        #self.shortcut.activated.connect(lambda: print('test_hotkey'))

        # display_widget.setVisible(False)

        image = QtGui.QImage('img/test.jpeg')
        if image.isNull():
            QtWidgets.QMessageBox.information(
                self, 'Loading image error', 'Cannot load the image')
            return

        self.image_label.set_image(image)

    def display_image(self) -> None:
        pass

    def show_exif(self) -> None:
        pass

    def rotate_image(self, clockwise: bool = True) -> None:
        if clockwise:
            print('Clockwise')
        else:
            print('Counterclockwise')
        pass


class ImagesListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.placeholder_text = 'Open your first image by clicking "Open an image" button'

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QtGui.QPainter(self.viewport())
            painter.save()
            fm = self.fontMetrics()
            elided_text = fm.elidedText(
                self.placeholder_text, QtCore.Qt.ElideRight, self.viewport().width()
            )
            painter.drawText(self.viewport().rect(),
                             QtCore.Qt.AlignCenter, elided_text)
            painter.restore()


class ImageQLabel(QtWidgets.QLabel):

    MAX_DIM = 512

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.setMaximumWidth(self.MAX_DIM)
        self.setMaximumHeight(self.MAX_DIM)

    def set_image(self, image: QtGui.QImage) -> None:
        self.image = image
        self.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        try:
            self.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(
                self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        except AttributeError:
            pass
        return super().resizeEvent(a0)
