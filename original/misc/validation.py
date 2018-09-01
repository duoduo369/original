#! -*- coding: utf-8 -*-
import cStringIO
import logging
import random

from django.conf import settings
from django.views.decorators.cache import cache_control
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
)

from path import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from common import constants

log = logging.getLogger(__name__)


@cache_control(no_cache=True)
def validate_image(request):
    '''
    background  #随机背景颜色
    line_color #随机干扰线颜色
    img_width = #画布宽度
    img_height = #画布高度
    font_color = #验证码字体颜色
    font_size = #验证码字体尺寸
    font = I#验证码字体
    '''
    session_key = constants.VALIDATION_SESSION_KEY
    string = {
        'number': '12345679',
        'litter': 'ACEFGHKMNPRTUVWXY',
        'chars': '12345679ACEFGHKMNPRTUVWXY'
    }
    background = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
    line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    img_width = 58
    img_height = 30
    font_color = ['black', 'darkblue', 'darkred']
    font_size = 14
    font_path = Path(settings.VALIDATION_FONT_PATH)
    font_file_list = [
        'DejaVuSans-Bold.ttf', 'DejaVuSansMono-Bold.ttf', 'DejaVuSansMono.ttf',
        'DejaVuSans.ttf', 'DejaVuSerif-Bold.ttf', 'DejaVuSerif.ttf'
    ]
    font = [ImageFont.truetype(font_path / font_file, font_size) for font_file in font_file_list]
    request.session[session_key] = ''

    # 新建画布
    im = Image.new('RGB', (img_width, img_height), background)
    draw = ImageDraw.Draw(im)
    code = random.sample(string['chars'], random.randrange(4, 6))
    # 新建画笔
    draw = ImageDraw.Draw(im)
    # 画干扰线
    for i in range(random.randrange(3, 5)):
        xy = (
            random.randrange(0, img_width), random.randrange(0, img_height),
            random.randrange(0, img_width), random.randrange(0, img_height)
        )
        draw.line(xy, fill=line_color, width=random.randrange(1, 3))

    # 写入验证码文字
    x = 2
    count = len(code)
    width_gap = (img_width - x - 2) / count
    for i in code:
        y = random.randrange(0, 10)
        draw.text((x, y), i, font=random.choice(font), fill=random.choice(font_color))
        x += width_gap
        request.session[session_key] += i
    del x
    del draw
    buf = cStringIO.StringIO()
    im.save(buf, 'gif')
    buf.seek(0)
    return HttpResponse(buf.getvalue(), 'image/gif')
