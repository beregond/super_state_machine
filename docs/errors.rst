======
Errors
======

When a machine is used
----------------------

:exc:`~super_state_machine.errors.TransitionError`
    The transition is not allowed by the graph. Subclass of
    :exc:`RuntimeError`.

:exc:`ValueError`
    The state is not part of the states enum: an unknown string, or a member
    of another enum.

.. code-block:: python

    from super_state_machine import errors

    try:
        task.state = requested
    except errors.TransitionError:
        ...  # valid state, wrong moment
    except ValueError:
        ...  # not a state at all

When a class is defined
-----------------------

These raise :exc:`ValueError` while the class body is evaluated, so they show
up at import time:

* no states enum (``No states enum given!``) or the attribute is not an enum,
* a state value that is not a string,
* duplicate state values,
* no initial state (``Empty state is disallowed, yet no initial state is
  given!``),
* a generated, named or user-defined member with a clashing name (see
  :ref:`usage:name collisions`).
