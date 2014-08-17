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


    >>> class Mail(machine.StateMachine):
    ...
    ...    class States(Enum):
    ...
    ...        DRAFT = 'draft'
    ...        CREATED = 'created'
    ...        PROCESSING = 'processing'
    ...        SENDED = 'sended'
    ...        FAILED = 'failed'

    >>> mail = Mail()
    >>> mail.set_draft()
    >>> mail.is_draft
    True
    >>> mail.is_created
    False
    >>> mails.set_created()
    >>> mail.is_created
    True
    >>> mail.state
    'created'
