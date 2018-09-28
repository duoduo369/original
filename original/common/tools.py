# -*- coding: utf-8 -*-
import pyqrcode


def qrcode(text):
    scale = 6
    q = pyqrcode.create(text)
    return 'data:image/png;base64,{}'.format(q.png_as_base64_str(scale))
