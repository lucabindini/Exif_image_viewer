import os

from PIL import Image, ImageQt


class ModelImage():

    def __init__(self, path: str) -> None:
        self.name = os.path.basename(path)
        self._image = Image.open(path)

    def rotate(self, degree: float) -> None:
        self._image = self._image.rotate(angle=(180+degree), expand=True)

    def get_image(self) -> ImageQt.ImageQt:
        return ImageQt.ImageQt(self._image)
