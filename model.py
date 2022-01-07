import os

from PIL import Image, ImageQt, ImageOps, ExifTags


class ModelImage():

    def __init__(self, path: str) -> None:
        self.path = path
        self.name = os.path.basename(self.path)
        self._image = Image.open(self.path)
        self._image = ImageOps.exif_transpose(self._image)
        self.has_gps = False

    def rotate(self, degree: float) -> None:
        self._image = self._image.rotate(angle=(180+degree), expand=True)

    def get_image(self) -> ImageQt.ImageQt:
        return ImageQt.ImageQt(self._image)

    def get_exif(self):
        self._exif = {}
        info = self._image.getexif()
        if info:
            for tag, value in info.items():
                decoded_tag = ExifTags.TAGS.get(tag, tag)
                if decoded_tag == 'ExifOffset':
                    self.add_extra_ifd_tags()
                elif decoded_tag == 'GPSInfo':
                    self.add_extra_gps_tags()
                    self.has_gps = True
                else:
                    self._exif[decoded_tag] = value

        if self.has_gps:
            lat, lon = self.get_gps_coordinates()
            #print(lat, lon)

    def add_extra_ifd_tags(self):
        for tag, value in ExifTags.TAGS.items():
            if value == "ExifOffset":
                break
        info = self._image.getexif().get_ifd(tag)
        self._exif.update({ExifTags.TAGS.get(tag, tag)
                          : value for tag, value in info.items()})

    def add_extra_gps_tags(self):
        for tag, value in ExifTags.TAGS.items():
            if value == "GPSInfo":
                break
        gps_info = self._image.getexif().get_ifd(tag)
        self._exif.update({ExifTags.GPSTAGS.get(tag, tag)
                          : value for tag, value in gps_info.items()})

    def get_tag_if_exist(self, tag):
        if tag in self._exif:
            return self._exif[tag]
        return None

    def to_degrees(self, value):
        return round(float(value[0]) + (float(value[1]) / 60.0) + (float(value[2]) / 3600.0), 6)

    def get_gps_coordinates(self):
        lat = None
        lon = None
        gps_lat = self.get_tag_if_exist('GPSLatitude')
        gps_lat_ref = self.get_tag_if_exist('GPSLatitudeRef')
        gps_lon = self.get_tag_if_exist('GPSLongitude')
        gps_lon_ref = self.get_tag_if_exist('GPSLongitudeRef')

        if gps_lat and gps_lat_ref and gps_lon and gps_lon:
            lat = self.to_degrees(gps_lat)
            if gps_lat_ref[0] != 'N':
                lat = 0 - lat
            lon = self.to_degrees(gps_lon)
            if gps_lon_ref[0] != 'E':
                lon = 0 - lon
        return lat, lon
