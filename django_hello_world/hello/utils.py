
import os


def rel(*x):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.sep.join(os.path.split(current_dir)[:-1])
    return os.path.join(parent_dir, *x)
