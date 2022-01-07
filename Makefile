pathsep = :
UNAME := $(shell uname)
ifeq ($(UNAME),Darwin)
	options = --windowed --name 'Exif Image Viewer'
else
	options = --onefile
endif


dist/Exif_image_viewer : *.py
	pyinstaller $(options) --icon img/favicon.ico \
	  --add-data 'img/icons/fugue-icons-3.5.6/icons/*.png$(pathsep)img/icons/fugue-icons-3.5.6/icons' \
	  --add-data 'img/favicon.ico$(pathsep)img' \
	  main.py

.PHONY : clean
clean :
	rm -rf build dist ./*.spec

