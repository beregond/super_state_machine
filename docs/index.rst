Super State Machine
===================

Finite state machines built on :class:`enum.Enum`. Declare the states and the
allowed transitions, and the class gets ``is_*``, ``set_*`` and ``can_be_*``
members for every state.

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
    ...         SENT = "sent"
    ...
    ...     class Meta:
    ...         transitions = {
    ...             "draft": ["scheduled"],
    ...             "scheduled": ["sent", "draft"],
    ...         }

    >>> task = Task()
    >>> task.is_draft
    True
    >>> task.can_be_sent
    False
    >>> task.set_sent()
    Traceback (most recent call last):
      ...
    super_state_machine.errors.TransitionError: Cannot transit from 'draft' to 'sent'.
    >>> task.set_scheduled()
    >>> task.state = "sent"
    >>> task.state
    'sent'

New to the library? Start with :doc:`usage`, then :doc:`transitions`.

.. toctree::
   :maxdepth: 2
   :caption: User guide

   installation
   usage
   transitions
   options
   property_machine
   logging
   errors
   cookbook

.. toctree::
   :maxdepth: 2
   :caption: Reference

   api
   readme

.. toctree::
   :maxdepth: 1
   :caption: Project

   contributing
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
