# -*- coding: utf-8 -*-
import pyqrcode

from .data_structure import ObjectDict


def qrcode(text):
    scale = 6
    q = pyqrcode.create(text)
    return 'data:image/png;base64,{}'.format(q.png_as_base64_str(scale))


def iter_items(items, interval, total=None):
  """
  :param items: 要遍历的集合
  :param interval: 每次遍历的元素的数量
  :return:
  """
  if interval < 1:
      return

  start = 0
  if total is None:
      total = len(items)
  while True:
      if start >= total:
          break
      yield items[start:start + interval]
      start += interval


def format_api_object(obj, attrs):
    result = ObjectDict()
    for attr in attrs:
        result[attr] = getattr(obj, attr)
    return result


def get_result_in_query_order(query_set, query_ids, query_key='id'):
    mapper = {getattr(each, query_key):each for each in query_set}
    result = []
    for _id in query_ids:
        if _id in mapper:
            result.append(mapper[_id])
    return result
