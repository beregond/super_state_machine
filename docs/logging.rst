=======
Logging
=======

Every successful state change is logged with the standard :mod:`logging`
module at ``DEBUG`` level. Records go to loggers under the
``super_state_machine`` name (the changes themselves are logged by
``super_state_machine.utils``).

Logging is silent by default: the package adds a
:class:`~logging.NullHandler`, as the :ref:`library logging howto
<python:library-config>` recommends.

Enabling it
-----------

Turn on ``DEBUG`` for the whole application:

.. code-block:: python

    import logging

    logging.basicConfig(level=logging.DEBUG)

Or only for this library:

.. code-block:: python

    import logging

    logger = logging.getLogger("super_state_machine")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

What is logged
--------------

One record per change, with the class name, the instance id, the old state and
the new state:

.. code-block:: text

    DEBUG:super_state_machine.utils:Task (id=140245581263376): draft -> scheduled

Changes made with ``set_*`` methods, named transitions, ``state = ...``,
property machines and ``force_set`` are all logged. Rejected transitions are
not logged, they raise :exc:`~super_state_machine.errors.TransitionError`.

To tell machines apart, filter on the class name or id in the message. All
records come from one logger.
