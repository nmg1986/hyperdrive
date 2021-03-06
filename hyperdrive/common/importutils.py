import sys


def import_class(import_str):
    """Returns a class from a string including module and class"""
    mod_str, _sep, class_str = import_str.rpartition('.')
    try:
        __import__(mod_str)
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise


def import_module(mod_str):
    """Import a module"""
    try:
        __import__(mod_str)
        return sys.modules[mod_str]
    except ImportError:
        raise
