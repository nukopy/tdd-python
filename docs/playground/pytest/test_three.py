""" Test the "Task" data type. """

from app.tasks import Task


def test_defaults():
    """ Using no parameters should invoke defaults. """

    defaults = Task()
    expected = Task(None, None, False, None)

    assert defaults == expected
