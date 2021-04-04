""" Test the "Task" data type. """

from collections import namedtuple


Task = namedtuple("Task", ["summary", "owner", "done", "id"])
Task.__new__.__defaults__ = (None, None, False, None)

def hello():
    print("Hello world!")
