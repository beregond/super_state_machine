========
Cookbook
========

Short recipes for common tasks. They use this machine:

.. code-block:: python

    >>> from enum import Enum

    >>> from super_state_machine import machines

    >>> class Task(machines.StateMachine):
    ...
    ...     class States(Enum):
    ...         DRAFT = "draft"
    ...         SCHEDULED = "scheduled"
    ...         SENT = "sent"
    ...         FAILED = "failed"
    ...
    ...     class Meta:
    ...         initial_state = "draft"
    ...         transitions = {
    ...             "draft": ["scheduled"],
    ...             "scheduled": ["sent", "failed", "draft"],
    ...             "failed": ["scheduled"],
    ...         }

Listing the next possible states
--------------------------------

.. code-block:: python

    >>> task = Task()
    >>> task.set_scheduled()
    >>> [state.value for state in Task.States if task.can_be_(state)]
    ['draft', 'sent', 'failed']

Saving and restoring the state
------------------------------

Store ``state`` (a plain string) and bring it back with ``force_set``, since
the stored state does not have to be reachable from the initial one:

.. code-block:: python

    >>> saved = task.state
    >>> restored = Task()
    >>> restored.force_set(saved)
    >>> restored.state
    'scheduled'

Running code on a transition
----------------------------

Wrap the generated setter in a method with its own name. The setter still
checks the graph, so the side effect runs only after a valid change:

.. code-block:: python

    >>> class Mail(machines.StateMachine):
    ...
    ...     class States(Enum):
    ...         DRAFT = "draft"
    ...         SENT = "sent"
    ...
    ...     class Meta:
    ...         initial_state = "draft"
    ...         transitions = {"draft": ["sent"]}
    ...
    ...     def send(self):
    ...         self.set_sent()
    ...         print("mail sent")

    >>> mail = Mail()
    >>> mail.send()
    mail sent
    >>> mail.send()
    Traceback (most recent call last):
      ...
    super_state_machine.errors.TransitionError: Cannot transit from 'sent' to 'sent'.

Choosing the state by name in templates
---------------------------------------

``is_(state)`` and ``can_be_(state)`` take the state as an argument, which
helps when the state comes from a variable:

.. code-block:: python

    >>> wanted = "sent"
    >>> task.can_be_(wanted)
    True
    >>> task.is_(wanted)
    False
