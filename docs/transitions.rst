===========
Transitions
===========

By default any state can follow any other. To restrict that, describe the
state graph in ``Meta``.

Transitions graph
-----------------

The :ref:`option_transitions` option maps each **source** state to the list of
states it may move to:

.. code-block:: python

    >>> from enum import Enum

    >>> from super_state_machine import errors, machines

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

From ``draft`` the task can go to ``scheduled`` or ``failed``, and nowhere
else. A state missing from the dict (``sent`` and ``failed`` here) is a dead
end. A forbidden change raises
:exc:`~super_state_machine.errors.TransitionError`:

.. code-block:: python

    >>> task = Task()
    >>> task.can_be_scheduled
    True
    >>> task.can_be_sent
    False
    >>> task.set_sent()
    Traceback (most recent call last):
      ...
    super_state_machine.errors.TransitionError: Cannot transit from 'draft' to 'sent'.

:exc:`~super_state_machine.errors.TransitionError` is a subclass of
:exc:`RuntimeError`. See :doc:`errors` for all exceptions.

``force_set`` skips the graph, see :ref:`usage:forced set`.

Named transitions
-----------------

:ref:`option_named_transitions` adds methods with domain names, such as
``task.process()`` instead of ``task.set_processing()``. Each entry is a tuple:

``(name, target)``
    The method is allowed from **every** state. All states get an edge to
    ``target``.

``(name, target, [source, ...])``
    The method is allowed from the listed states. Those edges are **added**
    to the graph.

``(name, target, None)``
    Only a method is added, the graph does not change.

.. code-block:: python

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

    >>> task = Task()
    >>> task.process()
    Traceback (most recent call last):
      ...
    super_state_machine.errors.TransitionError: Cannot transit from 'draft' to 'processing'.
    >>> task.set_scheduled()
    >>> task.process()
    >>> task.state
    'processing'
    >>> task.fail()
    >>> task.state
    'failed'

``("process", "processing", ["scheduled"])`` adds the ``scheduled ->
processing`` edge, and ``("fail", "failed")`` lets every state, ``failed``
included, move to ``failed``.

.. warning::

    A 2-tuple opens the target to **all** states. To add only the method,
    pass ``None`` as the third item:

    .. code-block:: python

        named_transitions = [
            ("process", "processing", None),
        ]

Named checkers
--------------

Every state already has a ``can_be_*`` property. :ref:`option_named_checkers`
adds aliases with nicer names:

.. code-block:: python

    >>> class Task(machines.StateMachine):
    ...
    ...     class States(Enum):
    ...         DRAFT = "draft"
    ...         PROCESSING = "processing"
    ...
    ...     class Meta:
    ...         initial_state = "draft"
    ...         transitions = {"draft": ["processing"]}
    ...         named_checkers = [
    ...             ("can_be_processed", "processing"),
    ...         ]

    >>> task = Task()
    >>> task.can_be_processed
    True
    >>> task.can_be_processing
    True

Complete graphs
---------------

The :ref:`option_complete` option switches the graph off: with
``complete = True`` every transition is allowed, even if ``transitions`` is
set. When you leave it out, it is ``True`` for machines without
``transitions`` and ``named_transitions``, and ``False`` otherwise.

.. code-block:: python

    >>> class Task(machines.StateMachine):
    ...
    ...     class States(Enum):
    ...         DRAFT = "draft"
    ...         SENT = "sent"
    ...
    ...     class Meta:
    ...         initial_state = "draft"
    ...         complete = True
    ...         named_transitions = [("send", "sent", None)]

    >>> task = Task()
    >>> task.send()
    >>> task.set_draft()
    >>> task.state
    'draft'
