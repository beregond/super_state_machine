Usage
=====

State machine
~~~~~~~~~~~~~

State machine allows to operate on state, where allowed states are defined by
states enum.

Remember that states enum **must be** unique.

Meta
----

All options for state machine are passed through ``Meta`` class, like below:

.. code-block:: python

  >>> class Task(machines.StateMachine):
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
  ...         named_checkers = [
  ...             ('can_be_processed', 'processing'),
  ...         ]

You can see that about only option ``named_checkers`` is provided. In fact it
is not necessary to provide any option at all.  For full reference see
:ref:`options`.

Word about value translation
----------------------------

Whenever you will be passing enum value or string to represent state (in meta,
in options, in methods ``is_*``, ``set_*`` or ``can_be_*``) remember that these
values must **clearly** describe enum value.

For example in following case:

.. code-block:: python

  >>> class Lock(machine.StateMachine):
  ...
  ...     class States(Enum):
  ...
  ...         OPEN = 'open'
  ...         OPENING = 'opening'
  ...         LOCKED = 'locked'
  ...         LOCKING = 'locking'

values that clear state ``open`` are string ``'open'`` and
``Lock.States.OPEN``, but for ``opening`` state these are strings ``'openi'``,
``'opening'`` and ``Lock.States.OPENING``. In other words you must provide as
much information to make it not necessary to guess end value. Otherwise
``AmbiguityError`` will be raised.

Simple case
-----------

In simplest case you just have to define ``States`` enum to definen what valid
states are and start using it.

.. code-block:: python

  >>> from enum import Enum

  >>> from super_state_machine import machines


  >>> class Task(machines.StateMachine):
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
  *** ValueError: Unrecognized value ('wrong').

Actual state as enum
--------------------

You can also get actual state in enum form by property ``actual_state``, or
``as_enum``:

.. code-block:: python

  >>> task.actual_state
  <States.DRAFT: 'draft'>
  >>> task.as_enum
  <States.DRAFT: 'draft'>

Transitions
-----------

In case when you want to define what proper transitions are, you need to define
``transitions`` option.

.. code-block:: python

  >>> class Task(machines.StateMachine):
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
  ...         transitions = {
  ...             'draft': ['scheduled', 'failed'],
  ...             'scheduled': ['failed'],
  ...             'processing': ['sent', 'failed'],
  ...         }
  ...         named_transitions = [
  ...             ('process', 'processing', ['scheduled']),
  ...             ('fail', 'failed'),
  ...         ]

In example above ``transitions`` option defines which transitions are valid -
for example from that option we can read that state can be switched to
``draft`` but only from ``scheduled`` or ``failed``.

You can change state to desired one by generated methods like ``set_*``, so if
you want to change state of ``Task`` to ``draft`` it is enough to call
``set_draft`` on instance of ``Task``.

There is also ``named_transitions`` option. This is list of 3-tuples with name,
desired state optional "from" states, or 2-tuples with name and desired states.
First line means that instance of task will have method called ``process``
which will trigger change of state to ``process``. It is like you would call
method ``set_processing`` but sounds better. Also all "from" states are
**added** to list of valid transitions of ``Task``.

.. warning::

    In case you won't provide third argument in tuple, it is considered that
    transition to that case is allowed from ANY other state (like ``('fail',
    'failed')`` case). If you want just to add named transition without
    modifying actual transitions table, pass as ``None`` as third argument.

    .. code-block:: python

      ...      named_transitions = [
      ...          ('process', 'processing', None),
      ...      }

.. seealso::

    :ref:`option_complete`

Forced set (forced transition)
------------------------------

You can also use ``force_set`` which will change current state to any other
**proper** state without checkint if such transition is allowed. It may be seen
as 'hard reset' to some state.

.. code-block:: python

  >>> task.force_set('draft')
  >>> task.force_set(Task.States.SCHEDULED)

.. versionadded:: 2.0

Checkers
--------

.. code-block:: python

  >>> class Task(machines.StateMachine):
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
  ...         named_checkers = [
  ...             ('can_be_processed', 'processing'),
  ...         ]

Each instance of state machine has auto generated set of checkers (which are
properties) like ``can_be_*``. In this case checkers will be like
``can_be_draft``, ``can_be_sent`` etc. If you want to have custom checkers
defined, you can either define them by yourself or pass as 2-tuple in
``named_checkers`` option. Tuple must have name of checker and state to check,
so in this case instance of ``Task`` will have property ``can_be_processed``
which will work like ``can_be_processing`` (yet sounds better).

Getters
-------

.. code-block:: python

  >>> class Task(machines.StateMachine):
  ...
  ...     class States(Enum):
  ...
  ...         DRAFT = 'draft'
  ...         SCHEDULED = 'scheduled'
  ...         PROCESSING = 'processing'
  ...         SENT = 'sent'
  ...         FAILED = 'failed'


Getters checks state, but checks one particular state. All of getters are
properties and are named like ``is_*``. If you want to check if instance of
``Task`` is currently draft, just call ``instance.is_draft``. This work just
like calling ``instance.is_('draft')``. This comes handy especially in
templates.

Name collisions
---------------

In case any auto generated method would collide with already defined one, or if
named transitions or checkers would cause collision with already defined one or
with other auto generated method, ``ValueError`` will be raised. In particular
name collisions (intentional or not) are prohibited and will raise an
exception.

.. _options:

Options
~~~~~~~

``states_enum_name``
--------------------

Default value: ``'States'``.

Define name of states enum. States enum must be present in class definition
under such name.

``allow_empty``
---------------

Default value: ``True``.

Determine if empty state is allowed. If this option is set to ``False`` option
:ref:`option_initial_state` **must** be provided.

.. _option_initial_state:

``initial_state``
-----------------

Default value: ``None``.

Defines initial state the instance will start it's life cycle.

.. _option_complete:

``complete``
------------

This option defines if states **graph** is complete. It this option is set to
``True`` then any transition is **always** valid. If this option is set to
``False`` then state machine looks to states graph to determine if this
transition should succeeed.

This option in fact doesn't have default value. If isn't provided and
``transitions`` neither ``named_transitions`` options are not provided then it
is set to ``True``. If one or both options are provided this option is set to
``False`` (still, only if it wasn't provided in ``Meta`` of state machine).

.. _option_transitions:

``transitions``
---------------

Dict that defines basic state graph (which can be later filled up with data
comming from :ref:`option_named_transitions`).

Each key defines target of transition, and value (which **must** be a list)
defines initial states for transition.

.. code-block:: python

  ...     class Meta:
  ...
  ...         transitions = {
  ...             'draft': ['scheduled', 'failed'],
  ...             'scheduled': ['failed'],
  ...             'processing': ['sent', 'failed'],
  ...         }

.. _option_named_transitions:

``named_transitions``
---------------------

List of 3-tuples or 2-tuples (or mixed) which defines named transitions. These
definitions affect states graph:

  * If there is no third argument (2-tuple was passed) then desired transition
    is valid from **all** states.

  * If there is ``None`` passed as third argument - the states **will not** be
    affected.

  * Otherwise third argument must be list of allowed initial states for this
    transition. Remember that these transitions will be **added** to state
    graph. Also other transitions defined in :ref:`option_transitions` option
    will still be valid for given transition name.

.. code-block:: python

  ...     class Meta:
  ...
  ...         transitions = {
  ...             'draft': ['scheduled', 'failed'],
  ...             'scheduled': ['failed'],
  ...             'processing': ['sent', 'failed'],
  ...         }
  ...         named_transitions = [
  ...             ('process', 'processing', ['scheduled']),
  ...             ('fail', 'failed'),
  ...         ]

In this case method ``process`` will change state to ``processing`` but
transition is valid from three initial states: ``scheduled``, ``sent`` and
``failed``.

``named_checkers``
------------------

List of 2-tuple which defines named transition checkers. Tuple consist of
checker name and desired state. When called, checher will check if state
machine can transit to desired state.

.. code-block:: python

  ...     class Meta:
  ...
  ...         named_checkers = [
  ...             ('can_be_processed', 'processing'),
  ...         ]

In example above property ``can_be_processed`` on instance will determine if
state can be changed to state ``processing``.

State machine as property
~~~~~~~~~~~~~~~~~~~~~~~~~

Thanks to ``extras`` module you can use state machines as properties!

.. code-block:: python

  >>> from enum import Enum

  >>> from super_state_machine import machines, extras


  >>> class Lock(machine.StateMachine):

  ...     class States(Enum):
  ...
  ...         OPEN = 'open'
  ...         LOCKED = 'locked'
  ...
  ...     class Meta:
  ...
  ...         allow_empty = False
  ...         initial_state = 'locked'
  ...         named_transitions = [
  ...             ('open', 'o'),
  ...             ('lock', 'l'),
  ...         ]


  >>> class Safe(object):
  ...
  ...     lock1 = extras.PropertyMachine(Lock)
  ...     lock2 = extras.PropertyMachine(Lock)
  ...     lock3 = extras.PropertyMachine(Lock)
  ...
  ...     _locks = ['lock1', 'lock2', 'lock3']
  ...
  ...     def is_locked(self):
  ...          locks = [getattr(self, lock).is_locked for lock in self._locks]
  ...          return any(locks)
  ...
  ...     def is_open(self):
  ...         locks = [getattr(self, lock).is_open for lock in self._locks]
  ...         return all(locks)

  >>> safe = Safe()
  >>> safe.lock1
  'locked'
  >>> safe.is_open
  False
  >>> safe.lock1.open()
  >>> safe.lock1.is_open
  True
  >>> safe.lock1
  'open'
  >>> safe.is_open
  False
  >>> safe.lock2.open()
  >>> safe.lock3 = 'open'
  >>> safe.is_open
  True

In this case method ``as_enum`` is really handy:

.. code-block:: python

  >>> safe.lock1.as_enum
  <States.OPEN: 'open'>

Although you could also use ``actual_state`` here (yet ``as_enum`` sounds more
familiar).

.. warning::

  In this case value is always visible as string, so there is **no** ``None``
  value returned. Instead of this ``None`` is transformed into ``''`` (empty
  string).

.. note::

  Remember that change of state can be made by calling method
  ``safe.lock1.lock``, assignation of string (or its part) like ``safe.lock1 =
  'open'`` or ``safe.lock1 = 'o'`` or assignation of enum like ``safe.lock1 =
  Lock.States.OPEN``.

``utils``
~~~~~~~~~

``EnumValueTranslator``
-----------------------

This class is part of inner API (see
:class:`super_state_machine.utils.Enumvaluetranslator`) but is really handy -
it is used by state machine to translate all (short) string representations to
enum values.

It also can ensure that given enum belongs to proper states enum.

.. code-block:: python

  >>> import enum

  >>> from super_state_machine import utils


  >>> class Choices(enum.Enum):
  ...
  ...     ONE = 'one'
  ...     TWO = 'two'
  ...     THREE = 'three'


  >>> class OtherChoices(enum.Enum):
  ...
  ...    ONE = 'one'

  >>> trans = utils.Enumvaluetranslator(Choices)
  >>> trans.translate('o')
  <Choices.ONE: 'one'>
  >>> trans.translate('one')
  <Choices.ONE: 'one'>
  >>> trans.translate(Choices.ONE)
  <Choices.ONE: 'one'>

  >>> trans.translate('t')
  *** AmbiguityError: Can't decide which value is proper for value 't' (...)

  >>> trans.translate(OtherChoices.ONE)
  *** ValueError: Given value ('OtherChoices.ONE') doesn't belong (...)
