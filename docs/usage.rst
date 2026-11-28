=====
Usage
=====

A state machine is a class that inherits from
:class:`~super_state_machine.machines.StateMachine` and holds a ``States``
enum. Every value of that enum is a valid state.

.. code-block:: python

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

The rules for the enum:

* State values **must** be strings. They are used to build method names, so
  ``"draft"`` gives ``is_draft``, ``set_draft`` and ``can_be_draft``.
* Values **must** be unique.
* The enum is looked up under the name ``States``. Use the
  :ref:`option_states_enum_name` option to pick another name.

Initial state
-------------

Every machine needs an initial state. Give it as the ``state`` class attribute
(like above) or as the :ref:`option_initial_state` option in ``Meta``. Without
one, the class definition fails:

.. code-block:: python

    >>> class Broken(machines.StateMachine):
    ...
    ...     class States(Enum):
    ...         ON = "on"
    ...         OFF = "off"
    Traceback (most recent call last):
      ...
    ValueError: Empty state is disallowed, yet no initial state is given!

Reading the state
-----------------

``state`` holds the value as a string, ``actual_state`` (or its alias
``as_enum``) holds the enum member:

.. code-block:: python

    >>> task = Task()
    >>> task.state
    'draft'
    >>> task.actual_state
    <States.DRAFT: 'draft'>
    >>> task.as_enum
    <States.DRAFT: 'draft'>

Each state has an ``is_*`` property. ``is_(state)`` does the same for a state
given as an argument, which is handy in templates and loops:

.. code-block:: python

    >>> task.is_draft
    True
    >>> task.is_sent
    False
    >>> task.is_("draft")
    True

Changing the state
------------------

There are three equivalent ways to change the state. Each one checks that the
transition is allowed (see :doc:`transitions`):

.. code-block:: python

    >>> task.set_scheduled()
    >>> task.state = "processing"
    >>> task.set_(Task.States.SENT)
    >>> task.state
    'sent'

``can_be_*`` properties (and ``can_be_(state)``) tell whether a transition is
allowed from the current state. This machine defines no transitions, so all of
them are allowed:

.. code-block:: python

    >>> task.can_be_draft
    True

States given by value
---------------------

Wherever a state is expected (in ``Meta``, in ``state = ...`` or in the
``is_``, ``set_`` and ``can_be_`` methods) you can pass either the enum member
or its **full** string value. Unknown values raise :exc:`ValueError`:

.. code-block:: python

    >>> task.state = "wrong"
    Traceback (most recent call last):
      ...
    ValueError: Value wrong doesn't match any state.

Short forms such as ``"sched"`` were accepted before version 2.0 and are
rejected now.

An enum member from another enum is rejected too:

.. code-block:: python

    >>> class Other(Enum):
    ...     DRAFT = "draft"

    >>> task.set_(Other.DRAFT)
    Traceback (most recent call last):
      ...
    ValueError: Given value ('Other.DRAFT') doesn't belong to states enum.

Forced set
----------

``force_set`` moves the machine to any valid state and skips the transition
check. Think of it as a hard reset:

.. code-block:: python

    >>> task.force_set("draft")
    >>> task.force_set(Task.States.FAILED)
    >>> task.state
    'failed'

.. versionadded:: 2.0

Name collisions
---------------

Generated members must not clash with anything defined in the class, and named
transitions and checkers must not clash with generated members. A clash raises
:exc:`ValueError` when the class is created:

.. code-block:: python

    >>> class Lamp(machines.StateMachine):  # doctest: +ELLIPSIS
    ...
    ...     state = "on"
    ...
    ...     class States(Enum):
    ...         ON = "on"
    ...         OFF = "off"
    ...
    ...     def is_on(self):
    ...         return True
    Traceback (most recent call last):
      ...
    ValueError: Name collision in state machine class - ...
