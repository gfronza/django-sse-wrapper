# -*- coding: utf-8 -*-
import importlib


def class_from_str(class_str):
    module_name, class_name = class_str.rsplit(".", 1)
    somemodule = importlib.import_module(module_name)
    return getattr(somemodule, class_name)
