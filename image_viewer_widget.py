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
        open_image_btn.setToolTip('[Ctrl+O]')
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
        toggle_btn.setToolTip('Toggle image list [Ctrl+T]')
        toggle_btn.released.connect(self.toggle_list)
        top_btn_layout.addWidget(toggle_btn)
        top_btn_layout.addStretch()
        exif_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}information.png'), 'Show Exif data')
        exif_btn.setToolTip('[Ctrl+E]')
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
        left_rot_btn.setToolTip(
            'Rotate 90 degrees counterclockwise [Ctrl+Shift+R]')
        left_rot_btn.released.connect(
            lambda: self.rotate_image(clockwise=False))
        rotate_btn_layout.addWidget(left_rot_btn)
        right_rot_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{self.window().ICONS_PATH}arrow-circle.png'), '')
        right_rot_btn.setToolTip('Rotate 90 degrees clockwise [Ctrl+R]')
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

        self.configure_hotkeys()

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
                self.configure_hotkeys()
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
        if self.images[self.images_list.currentRow()].get_exif():
            exif_box = ExifBox(
                self.images[self.images_list.currentRow()], parent=self)
            if not exif_box.exec():
                return
        else:
            msg = QtWidgets.QMessageBox(parent=self)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText('No Exif tags')
            msg.setInformativeText(
                'No available Exif tags for the selected image')
            msg.exec()

    # Method that rotates the selected image
    def rotate_image(self, clockwise: bool = True) -> None:
        if clockwise:
            self.images[self.images_list.currentRow()].rotate(degree=90)
        else:
            self.images[self.images_list.currentRow()].rotate(degree=-90)
        self.image_label.set_image(
            self.images[self.images_list.currentRow()].get_image())

    def configure_hotkeys(self) -> None:
        if self.display_widget.isVisible():
            right_rot_shrt = QtWidgets.QShortcut(
                QtGui.QKeySequence('Ctrl+R'), self)
            right_rot_shrt.activated.connect(
                lambda: self.rotate_image(clockwise=True))
            left_rot_shrt = QtWidgets.QShortcut(
                QtGui.QKeySequence('Ctrl+Shift+R'), self)
            left_rot_shrt.activated.connect(
                lambda: self.rotate_image(clockwise=False))
            exif_shrt = QtWidgets.QShortcut(
                QtGui.QKeySequence('Ctrl+E'), self)
            exif_shrt.activated.connect(self.show_exif)
            toggle_list_shrt = QtWidgets.QShortcut(
                QtGui.QKeySequence('Ctrl+T'), self)
            toggle_list_shrt.activated.connect(self.toggle_list)
        else:
            open_img_shrt = QtWidgets.QShortcut(
                QtGui.QKeySequence('Ctrl+O'), self)
            open_img_shrt.activated.connect(self.open_image)


# Subclass that extends QList and adds the possibility to have a placeholder text
class ImagesListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.placeholder_text = 'Open your first image by clicking "Open an image" button\
             \nor Ctrl+O (cmd+O on macOS)'

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
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        try:
            self.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(
                self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
        except AttributeError:
            pass
        return super().resizeEvent(a0)


# Subclass that extends QLabel and adds the possibility to handle and correctly resize (w.r.t aspect ratio) an image
class ExifBox(QtWidgets.QDialog):

    def __init__(self, image: ModelImage, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle(f'Exif data of {image.name} image')
        self.resize(400, 600)

        v_layout = QtWidgets.QVBoxLayout()
        table_widget = QtWidgets.QTableWidget()
        table_widget.setRowCount(len(image.get_exif().keys()))
        table_widget.setColumnCount(2)
        columns = ['tag', 'value']
        table_widget.setHorizontalHeaderLabels(columns)
        index = 0

        for k, v in image.get_exif().items():
            table_widget.setItem(index, 0, QtWidgets.QTableWidgetItem(k))
            table_widget.setItem(index, 1, QtWidgets.QTableWidgetItem(str(v)))
            index += 1

        table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table_widget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        v_layout.addWidget(table_widget)

        gps_btn_widget = QtWidgets.QWidget()
        gps_btn_layout = QtWidgets.QHBoxLayout()
        gps_btn_layout.addStretch()
        gps_btn = QtWidgets.QPushButton(QtGui.QIcon(
            f'{parent.window().ICONS_PATH}marker.png'), 'Show photo location in Google maps')
        gps_btn.released.connect(image.open_maps)
        gps_btn_layout.addWidget(gps_btn)
        gps_btn_layout.addStretch()
        gps_btn_widget.setLayout(gps_btn_layout)
        if image.has_gps:
            v_layout.addWidget(gps_btn_widget)

        self.setLayout(v_layout)
