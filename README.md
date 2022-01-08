# Exif Image Viewer
A simple PyQt5 image reader with the ability to view multiple images and their Exif tags.

## Requirements
The entire project is written in Python 3.9.7.
Some external libraries have been used:
| Library | Tested version | Required |
| -------|-------|-------|
| **PyQt5** | v5.15.6 | Yes|
| **Pillow** | v9.0.0 | Yes|
| **qdarkgraystyle** | v1.0.2 | Yes|

## Usage
Once you have downloaded the project and made sure you have all the dependencies installed, simply run the following command (on terminal) inside the project directory:
```sh
python3 main.py
```
For macOS users, the application executable is available in the Releases section of this repo.

## Functionalities
The application implements the following features:

* **Visualization of multiple images**: User can open multiple images and scroll through them from the appropriate side list
* **Image rescaling**: When the user resizes the main window, the image also adapts to the new size, maintaining the original aspect ratio with a maximum dimension (height or width) of 512 pixels
* **Image rotation**: User can rotate the selected image clockwise and counterclockwise

* **Show Exif**: If the image contains Exif data the application will show it in a tag-value table

* **Show location in Google Maps**: If there is a GPS tag in the image, the user can click on the appropriate button and will be redirected to the location page on Google Maps

* **Hotkeys**: Some keyboard shortcuts are available to use the application efficiently

|Functionality | Shortcut|
| -------|-------|
|Open an image | ```Ctrl+O```|
|Rotate image clockwise | ```Ctrl+R```|
|Rotate image counterclockwise | ```Ctrl+Shift+R```|
|Toggle image list | ```Ctrl+T```|
|Show image Exif | ```Ctrl+E```|

**N.B** in macOS ```Ctrl``` is replaced by ```cmd```

<p align="center">
<img src="img/app_usage.gif" width="50%">
</p>

## License
Licensed under the term of [GNU GPL v3.0](LICENSE).