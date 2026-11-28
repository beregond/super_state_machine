.. _options:

=======
Options
=======

Options go in a ``Meta`` class inside the state machine. All of them are
optional, and a machine without ``Meta`` is fine as long as it has an initial
state.

.. code-block:: python

    class Task(machines.StateMachine):

        class States(Enum):
            DRAFT = "draft"
            SENT = "sent"

        class Meta:
            initial_state = "draft"
            transitions = {"draft": ["sent"]}

States may be given by enum member or by full string value in every option.

.. _option_states_enum_name:

``states_enum_name``
--------------------

Default: ``"States"``.

Name of the class attribute that holds the states enum. A missing attribute
raises ``ValueError: No states enum given!``.

.. code-block:: python

    class Task(machines.StateMachine):

        state = "draft"

        class Status(Enum):
            DRAFT = "draft"
            SENT = "sent"

        class Meta:
            states_enum_name = "Status"

.. _option_initial_state:

``initial_state``
-----------------

Default: none.

State of a new instance. It takes precedence over the ``state`` class
attribute. One of the two is required.

.. _option_complete:

``complete``
------------

Default: ``True`` if neither :ref:`option_transitions` nor
:ref:`option_named_transitions` is given, ``False`` otherwise.

With ``True`` every transition is valid. With ``False`` transitions are checked
against the graph.

.. _option_transitions:

``transitions``
---------------

Default: ``{}``.

Dict mapping each source state to the list of states it may move to. The
graph can be extended by :ref:`option_named_transitions`.

.. code-block:: python

    transitions = {
        "draft": ["scheduled", "failed"],
        "scheduled": ["failed"],
        "processing": ["sent", "failed"],
    }

.. _option_named_transitions:

``named_transitions``
---------------------

Default: ``[]``.

List of tuples, each one adds a method that moves the machine to a state:

* ``(name, target)``: allowed from every state, all states get an edge to
  ``target``.
* ``(name, target, [source, ...])``: edges from the listed states are added
  to the graph. A single state may be given without the list.
* ``(name, target, None)``: the graph does not change.

.. code-block:: python

    named_transitions = [
        ("process", "processing", ["scheduled"]),
        ("fail", "failed"),
    ]

See :ref:`transitions:named transitions` for a walkthrough.

.. _option_named_checkers:

``named_checkers``
------------------

Default: ``[]``.

List of ``(name, state)`` tuples. Each one adds a property that tells whether
the machine can move to ``state``, like the generated ``can_be_*`` ones.

.. code-block:: python

    named_checkers = [
        ("can_be_processed", "processing"),
    ]
