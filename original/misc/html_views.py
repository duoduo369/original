# -*- coding: utf-8 -*-
from djangomako.shortcuts import render_to_response

def mako_html(request):
    context = {
        't': 'for test',
    }
    return render_to_response('misc/mako_html.html', context)
