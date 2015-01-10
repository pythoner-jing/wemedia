# -*- coding: utf-8 -*-

from PIL import Image
from IPython import embed

FILENAME = 'wemedia/static/image/01.jpg'


def zoom(filename, size):
    img = Image.open(filename)
    target_img = img.resize(size, Image.ANTIALIAS)
    target_img.show()


zoom(FILENAME, (400, 270))