===================
Super State Machine
===================

.. image:: https://badge.fury.io/py/super_state_machine.png
    :target: http://badge.fury.io/py/super_state_machine

.. image:: https://travis-ci.org/beregond/super_state_machine.png?branch=master
        :target: https://travis-ci.org/beregond/super_state_machine

.. image:: https://pypip.in/d/super_state_machine/badge.png
        :target: https://pypi.python.org/pypi/super_state_machine


Super State Machine gives you utilities to build finite state machines.

* Free software: BSD license
* Documentation: https://super_state_machine.readthedocs.org
* Source: https://github.com/beregond/super_state_machine

Features
--------

* Fully tested with Python 2.7, 3.3, 3.4 and PyPy.

* Create finite state machines:

  .. code-block:: python

    >>> from enum import Enum

    >>> from super_state_machine import machine


    >>> class Task(machine.StateMachine):
    ...
    ...    class States(Enum):
    ...
    ...         DRAFT = 'draft'
    ...         SCHEDULED = 'scheduled'
    ...         PROCESSING = 'processing'
    ...         SENT = 'sent'
    ...         FAILED = 'failed'

    >>> task = Task()
    >>> task.is_draft
    False
    >>> task.set_draft()
    >>> task.state
    'draft'
    >>> task.state = 'scheduled'
    >>> task.is_scheduled
    True
    >>> task.state = 'p'
    >>> task.state
    'processing'
    >>> task.state = 'wrong'
    *** ValueError

* Define allowed transitions graph, define additional named transitions
  and checkers:

  .. code-block:: python

    >>> class Task(machine.StateMachine):
    ...
    ...     class States(Enum):
    ...
    ...         DRAFT = 'draft'
    ...         SCHEDULED = 'scheduled'
    ...         PROCESSING = 'processing'
    ...         SENT = 'sent'
    ...         FAILED = 'failed'
    ...
    ...     class Meta:
    ...
    ...         allow_empty = False
    ...         initial_state = 'draft'
    ...         transitions = {
    ...             'draft': ['scheduled', 'failed'],
    ...             'scheduled': ['failed'],
    ...             'processing': ['sent', 'failed']
    ...         }
    ...         named_transitions = [
    ...             ('process', 'processing', ['scheduled']),
    ...             ('fail', 'failed')
    ...         ]
    ...         named_checkers = [
    ...             ('can_be_processed', 'processing'),
    ...         ]

    >>> task = Task()
    >>> task.state
    'draft'
    >>> task.process()
    *** TransitionError: Cannot transit from 'draft' to 'processing'.
    >>> task.set_scheduled()
    >>> task.can_be_processed
    True
    >>> task.process()
    >>> task.state
    'processing'
    >>> task.fail()
    >>> task.state
    'failed'

  Note, that third argument restricts from which states transition will be
  **added** to allowed (in case of `process`, new allowed transition will be
  added, from 'scheduled' to 'processing'). No argument means all available
  states, `None` or empty list won't add anything beyond defined ones.
