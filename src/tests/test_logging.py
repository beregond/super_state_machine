import logging
from enum import Enum

import pytest

from super_state_machine import machines
from super_state_machine.errors import TransitionError


class Task(machines.StateMachine):
    class States(Enum):
        DRAFT = "draft"
        SCHEDULED = "scheduled"
        DONE = "done"

    state = "draft"

    class Meta:
        allow_empty = False
        transitions = {"draft": ["scheduled"], "scheduled": ["done"]}


class Other(machines.StateMachine):
    class States(Enum):
        A = "a"
        B = "b"

    state = "a"

    class Meta:
        complete = True


def records(caplog):
    return [r for r in caplog.records if r.name.startswith("super_state_machine")]


def test_set_logs_transition(caplog):
    task = Task()
    with caplog.at_level(logging.DEBUG, logger="super_state_machine"):
        task.set_scheduled()
    recs = records(caplog)
    assert len(recs) == 1
    msg = recs[0].getMessage()
    assert recs[0].levelno == logging.DEBUG
    assert "Task" in msg
    assert "draft -> scheduled" in msg


def test_force_set_logs(caplog):
    task = Task()
    with caplog.at_level(logging.DEBUG, logger="super_state_machine"):
        task.force_set("done")
    recs = records(caplog)
    assert len(recs) == 1
    assert "draft -> done" in recs[0].getMessage()


def test_set_goes_through_patched_force_set(monkeypatch):
    calls = []
    original = Task.force_set

    def tracking_force_set(self, state):
        calls.append(state)
        original(self, state)

    monkeypatch.setattr(Task, "force_set", tracking_force_set)
    task = Task()
    task.set_scheduled()
    task.state = "done"
    assert calls == [Task.States.SCHEDULED, "done"]
    assert task.is_done


def test_state_assignment_logs(caplog):
    task = Task()
    with caplog.at_level(logging.DEBUG, logger="super_state_machine"):
        task.state = "scheduled"
    recs = records(caplog)
    assert len(recs) == 1
    assert "draft -> scheduled" in recs[0].getMessage()


def test_rejected_transition_does_not_log(caplog):
    task = Task()
    with (
        caplog.at_level(logging.DEBUG, logger="super_state_machine"),
        pytest.raises(TransitionError),
    ):
        task.set_done()
    assert records(caplog) == []


def test_classes_can_be_told_apart(caplog):
    with caplog.at_level(logging.DEBUG, logger="super_state_machine"):
        Task().set_scheduled()
        Other().set_b()
    msgs = [r.getMessage() for r in records(caplog)]
    assert len(msgs) == 2
    assert msgs[0].startswith("Task ")
    assert msgs[1].startswith("Other ")


def test_silent_by_default(capsys):
    package_logger = logging.getLogger("super_state_machine")
    assert any(isinstance(h, logging.NullHandler) for h in package_logger.handlers)
    assert package_logger.propagate is True
    Task().set_scheduled()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
