import os

from PIL import Image


class ModelImage():

    def __init__(self, path: str) -> None:
        self.path = path
        self.name = os.path.basename(self.path)
        self.image = Image.open(path)

    def rotate(self, degree: float) -> None:
        self.image.rotate(degree)

    

    