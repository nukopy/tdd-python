from typing import Any, Dict

from app.tasks import Task


def test_defaults():
    """ Using no parameters should invoke defaults. """

    defaults = Task()
    expected = Task(None, None, False, None)

    assert defaults == expected


def test_member_access():
    """ Check .field functionality of namedtuple. """

    t = Task(summary="buy milk", owner="brian")

    assert t.summary == "buy milk"
    assert t.owner == "brian"
    assert (t.done, t.id) == (False, None)


def test_asdict():
    """ _asdict() should return a dictionary. """

    t_task: Task = Task(summary="do something", owner="okken", done=True, id=21)
    t_dict: Dict[str, Any] = t_task._asdict()
    expected: Dict[str, Any] = {
        "summary": "do something",
        "owner": "okken",
        "done": True,
        "id": 21,
    }

    assert t_dict == expected


def test_replace():
    """ _replace() should change passed in fields. """

    t_before: Task = Task(summary="finish book", owner="brian", done=False)
    t_after: Task = t_before._replace(id=10, done=True)
    t_expected: Task = Task(summary="finish book", owner="brian", done=True, id=10)

    assert t_after == t_expected
