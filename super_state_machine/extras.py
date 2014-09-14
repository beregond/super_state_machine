"""Extra utilities for state machines, to make them more usable."""

import six


class ProxyString(str):

    """String that proxies every call to nested machine."""

    def __new__(cls, value, machine):
        """Create new string instance with reference to given machine."""
        string = super(cls, cls).__new__(cls, value)
        string.state_machine = machine
        return string

    def __getattr__(self, name):
        """Proxy call to machine."""
        return getattr(self.state_machine, name)


class PropertyMachine(object):

    """Descriptor to help using machines as properties."""

    def __init__(self, machine_type):
        """Create descriptor."""
        self._memory = {}
        self._machine_type = machine_type

    def _check_machine(self, obj):
        try:
            machine = self._memory[obj]
        except KeyError:
            machine = self._machine_type()
            self._memory[obj] = machine

    def __set__(self, obj, value):
        """Set state to machine."""
        self._check_machine(obj)
        self._memory[obj].set_(value)

    def __get__(self, obj, _type=None):
        """Get machine state."""
        if obj is None:
            return self

        self._check_machine(obj)

        machine = self._memory[obj]
        try:
            actual_state = machine.actual_state.value
        except AttributeError:
            actual_state = ''

        return ProxyString(actual_state, machine)


class FieldMachine(object):

    """Field machine.

    This class is designed for cases when you define field in model, which
    metaclass does some 'magic' with that - so it is required that this field
    is present during construction of it in its metaclass. ``FieldMachine``
    wraps that model and hides its own instances during that construction, so
    magic can happen, and later replaces properties with instances of
    :class:`PropertyMachine` with declared machine type.

    Field machine usage is similar to :class:`PropertyMachine` but you must
    remember that class that contains ``FieldMachine`` properties MUST inherit
    from ``FieldMachine.wrap(original_model)``.

    Example:

        >>> class SomeModel(FieldMachine.wrap(OriginalBaseModel)):
        ...
        ...     field1 = SomeField('field1')
        ...     field2 = SomeField('field2')
        ...     field3 = FieldMachine(SomeField('field1'), Machine)

    In case above all magic done by ``OriginalBaseModel`` metaclass will
    happen, but in instance of ``SomeModel`` property ``field3`` will behave as
    it was initialized with :class:`PropertyMachine`.

    """

    def __init__(self, field, machine_type):
        """Init field with replaced field and desired machine type.

        :param field: Some arbitrary field, that must be present for original
            metaclass.
        :param machine_type: Machine type that is to be used as property.

        """
        self.field = field
        self.machine_type = machine_type

    @classmethod
    def wrap(cls, wrapped_type):
        """Wrap type metaclass, to hide field machine for initialization.

        Generated temporary class will hide instances of ``FieldMachine``,
        execute metaclass of ``wrapped_type`` and replace properties with
        :class:`PropertyMachine` initialized with ``machine_type`` in
        ``__init__``.

        :param wrapped_type: Some arbitrary type to wrap.

        """
        wrapped_type = type(wrapped_type)
        field_cls = cls

        class TemporaryMetaclass(type):

            def __new__(cls, name, bases, attrs):
                tmp = {}
                for name, value in attrs.items():
                    if isinstance(value, field_cls):
                        tmp[name] = value
                        attrs[name] = value.field

                new_class = wrapped_type.__new__(
                    wrapped_type, name, bases, attrs)

                for name, value in tmp.items():
                    setattr(
                        new_class, name, PropertyMachine(value.machine_type))

                return new_class

        return six.with_metaclass(TemporaryMetaclass)
