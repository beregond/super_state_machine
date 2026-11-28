# Super State Machine

[![PyPI version](https://badge.fury.io/py/super-state-machine.svg)](https://badge.fury.io/py/super-state-machine) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/beregond/super_state_machine/test.yml) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/super-state-machine?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/super-state-machine)

Super State Machine gives you utilities to build finite state machines on top
of `enum.Enum`.

* Free software: BSD license
* Documentation: <https://super-state-machine.readthedocs.io>
* Source: <https://github.com/beregond/super_state_machine>

## Installation

```console
pip install super-state-machine
```

Supports Python 3.10 to 3.14, no runtime dependencies.

## Features

* Create finite state machines:

  ```python
  >>> from enum import Enum
  >>> from super_state_machine import machines

  >>> class Task(machines.StateMachine):
  ...
  ...     state = "draft"
  ...
  ...     class States(Enum):
  ...         DRAFT = "draft"
  ...         SCHEDULED = "scheduled"
  ...         PROCESSING = "processing"
  ...         SENT = "sent"
  ...         FAILED = "failed"

  >>> task = Task()
  >>> task.is_draft
  True
  >>> task.set_scheduled()
  >>> task.state
  'scheduled'
  >>> task.state = "processing"
  >>> task.is_processing
  True
  >>> task.state = "wrong"
  Traceback (most recent call last):
    ...
  ValueError: Value wrong doesn't match any state.

  ```

* Define the allowed transitions graph, named transitions and checkers:

  ```python
  >>> class Task(machines.StateMachine):
  ...
  ...     class States(Enum):
  ...         DRAFT = "draft"
  ...         SCHEDULED = "scheduled"
  ...         PROCESSING = "processing"
  ...         SENT = "sent"
  ...         FAILED = "failed"
  ...
  ...     class Meta:
  ...         initial_state = "draft"
  ...         transitions = {
  ...             "draft": ["scheduled", "failed"],
  ...             "scheduled": ["failed"],
  ...             "processing": ["sent", "failed"],
  ...         }
  ...         named_transitions = [
  ...             ("process", "processing", ["scheduled"]),
  ...             ("fail", "failed"),
  ...         ]
  ...         named_checkers = [
  ...             ("can_be_processed", "processing"),
  ...         ]

  >>> task = Task()
  >>> task.state
  'draft'
  >>> task.process()
  Traceback (most recent call last):
    ...
  super_state_machine.errors.TransitionError: Cannot transit from 'draft' to 'processing'.
  >>> task.set_scheduled()
  >>> task.can_be_processed
  True
  >>> task.process()
  >>> task.state
  'processing'
  >>> task.fail()
  >>> task.state
  'failed'

  ```

  `transitions` maps each source state to the states it may move to. The third
  item of a named transition **adds** edges from the listed states (here
  `scheduled -> processing`). Without it the transition is allowed from every
  state, and `None` adds the method without touching the graph.

* Use state machines as properties:

  ```python
  >>> from super_state_machine import extras

  >>> class Lock(machines.StateMachine):
  ...
  ...     class States(Enum):
  ...         OPEN = "open"
  ...         LOCKED = "locked"
  ...
  ...     class Meta:
  ...         initial_state = "locked"
  ...         named_transitions = [
  ...             ("open", "open"),
  ...             ("lock", "locked"),
  ...         ]

  >>> class Safe:
  ...
  ...     lock1 = extras.PropertyMachine(Lock)
  ...     lock2 = extras.PropertyMachine(Lock)
  ...
  ...     @property
  ...     def is_open(self):
  ...         return self.lock1.is_open and self.lock2.is_open

  >>> safe = Safe()
  >>> safe.lock1
  'locked'
  >>> safe.lock1.open()
  >>> safe.lock1
  'open'
  >>> safe.is_open
  False
  >>> safe.lock2 = "open"
  >>> safe.is_open
  True

  ```

## Logging

State changes are logged with the standard library `logging` module at
`DEBUG` level, using loggers under the `super_state_machine` name. Logging is
off by default (the package installs a `NullHandler`). To enable it:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
# or enable it for this library only:
logger = logging.getLogger("super_state_machine")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
```

Each record contains the class name, instance id and the old and new state,
for example `Task (id=140...): draft -> scheduled`.
