from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtGui, QtCore

from model import ModelImage


class ImageViewerWidget(QtWidgets.QWidget):

    proportion = 5

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.images: list[ModelImage] = []

        # Create entire GUI and connect events
        h_layout = QtWidgets.QHBoxLayout()

        self.images_list_widget = QtWidgets.QWidget()
        images_list_layout = QtWidgets.QVBoxLayout()
        self.images_list = ImagesListWidget()
        self.images_list.currentRowChanged.connect(self.display_image)
        self.images_list.itemPressed.connect(self.display_image)
        images_list_layout.addWidget(self.images_list)
        open_image_widget = QtWidgets.QWidget()
        open_image_layout = QtWidgets.QHBoxLayout()
        open_image_layout.addStretch()
        open_image_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}image-sunset.png'), 'Open an image')
        open_image_btn.released.connect(self.open_image)
        open_image_layout.addWidget(open_image_btn)
        open_image_layout.addStretch()
        open_image_widget.setLayout(open_image_layout)
        images_list_layout.addWidget(open_image_widget)
        self.images_list_widget.setLayout(images_list_layout)

        self.display_widget = QtWidgets.QWidget()
        display_layout = QtWidgets.QVBoxLayout()
        top_btn_widget = QtWidgets.QWidget()
        top_btn_layout = QtWidgets.QHBoxLayout()
        toggle_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}application-sidebar-list.png'), '')
        toggle_btn.setToolTip('Toggle image list')
        toggle_btn.released.connect(self.toggle_list)
        top_btn_layout.addWidget(toggle_btn)
        top_btn_layout.addStretch()
        exif_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}information.png'), 'Show Exif data')
        exif_btn.released.connect(self.show_exif)
        top_btn_layout.addWidget(exif_btn)
        top_btn_widget.setLayout(top_btn_layout)
        display_layout.addWidget(top_btn_widget)
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
        self.display_widget.setLayout(display_layout)

        h_layout.addWidget(self.images_list_widget, 100//self.proportion)
        h_layout.addWidget(self.display_widget,
                           100 * (self.proportion-1) // self.proportion)
        self.setLayout(h_layout)

        self.display_widget.setVisible(False)

    # Method that hides/shows image list
    def toggle_list(self) -> None:
        if self.images_list_widget.isVisible():
            self.images_list_widget.setVisible(False)
        else:
            self.images_list_widget.setVisible(True)

    # Method that opens a jpeg image and adds it to image list
    def open_image(self) -> None:
        image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, caption='Open an image', filter='Image files (*.jpg *.jpeg)')
        if image_path:
            if not self.display_widget.isVisible():
                self.display_widget.setVisible(True)
            self.images.append(ModelImage(path=image_path))
            self.images_list.addItem(
                self.images[self.images_list.count()].name)
            self.images_list.setCurrentRow(self.images_list.count() - 1)

    # Method that displays the selected image
    def display_image(self) -> None:
        self.image_label.set_image(
            self.images[self.images_list.currentRow()].get_image())

    # Method that opens the dialog with Exif datas
    def show_exif(self) -> None:
        pass

    # Method that rotates the selected image
    def rotate_image(self, clockwise: bool = True) -> None:
        if clockwise:
            self.images[self.images_list.currentRow()].rotate(degree=90)
        else:
            self.images[self.images_list.currentRow()].rotate(degree=-90)
        self.image_label.set_image(
            self.images[self.images_list.currentRow()].get_image())


# Subclass that extends QList and adds the possibility to have a placeholder text
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


# Subclass that extends QLabel and adds the possibility to handle and correctly resize (w.r.t aspect ratio) an image
class ImageQLabel(QtWidgets.QLabel):

    MAX_DIM = 1024

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
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        try:
            self.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(
                self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
        except AttributeError:
            pass
        return super().resizeEvent(a0)
