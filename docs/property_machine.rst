============================
State machines as properties
============================

:class:`~super_state_machine.extras.PropertyMachine` turns a state machine
into an attribute of another class. Every instance of that class gets its own
machine.

.. code-block:: python

    >>> from enum import Enum

    >>> from super_state_machine import extras, machines

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
    ...     lock3 = extras.PropertyMachine(Lock)
    ...
    ...     locks = ["lock1", "lock2", "lock3"]
    ...
    ...     @property
    ...     def is_locked(self):
    ...         return any(getattr(self, lock).is_locked for lock in self.locks)
    ...
    ...     @property
    ...     def is_open(self):
    ...         return all(getattr(self, lock).is_open for lock in self.locks)

The attribute reads as the state string, and the machine's members are
reachable through it:

.. code-block:: python

    >>> safe = Safe()
    >>> safe.lock1
    'locked'
    >>> safe.lock1 == "locked"
    True
    >>> safe.is_open
    False
    >>> safe.lock1.open()
    >>> safe.lock1.is_open
    True
    >>> safe.lock1.as_enum
    <States.OPEN: 'open'>

Assigning a state (string or enum member) goes through the transition check,
like ``machine.state = ...``:

.. code-block:: python

    >>> safe.lock2.open()
    >>> safe.lock3 = "open"
    >>> safe.is_open
    True
    >>> safe.lock3 = Lock.States.LOCKED
    >>> safe.is_locked
    True

Instances do not share state:

.. code-block:: python

    >>> Safe().lock1
    'locked'

.. note::

    The value is a :class:`str` subclass that forwards attribute access to the
    machine. Use ``safe.lock1.as_enum`` or ``safe.lock1.actual_state`` when you
    need the enum member.
