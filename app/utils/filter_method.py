# -*- coding: utf-8 -*-

from typing import List


def filter_obj_fields(obj_list: List, values_list: List) -> List:
    return [obj.values(values_list) for obj in obj_list]
