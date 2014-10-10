"""Extra utilities for state machines, to make them more usable."""


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

    def __set__(self, obj, value):
        """Set state to machine."""
        object_id = _generate_object_id(obj)
        self._check_machine(obj)
        self._memory[object_id].set_(value)

    def __get__(self, obj, _type=None):
        """Get machine state."""
        if obj is None:
            return self

        object_id = _generate_object_id(obj)
        self._check_machine(obj)

        machine = self._memory[object_id]
        try:
            actual_state = machine.actual_state.value
        except AttributeError:
            actual_state = ''

        return ProxyString(actual_state, machine)

    def _check_machine(self, obj):
        object_id = _generate_object_id(obj)
        try:
            machine = self._memory[object_id]
        except KeyError:
            machine = self._machine_type()
            self._memory[object_id] = machine


def _generate_object_id(obj):
    return hex(id(obj))


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
    def wrap(cls, wrapped_type, additional_attributes={}):
        """Wrap type metaclass, to hide field machine for initialization.

        Generated temporary class will hide instances of ``FieldMachine``,
        execute metaclass of ``wrapped_type`` and replace properties with
        :class:`PropertyMachine` initialized with ``machine_type`` in
        ``__init__``.

        :param wrapped_type: Some arbitrary type to wrap.

        """
        original_metaclass = type(wrapped_type)

        class TemporaryMetaclass(original_metaclass):

            def __new__(cls, name, bases, attrs):
                exchange = {}
                for attr_name, attr in attrs.items():
                    if isinstance(attr, FieldMachine):
                        exchange[attr_name] = attr
                        attrs[attr_name] = attr.field

                new_class = (super(TemporaryMetaclass, cls)
                             .__new__(cls, name, bases, attrs))
                for attr_name, attr in exchange.items():
                    setattr(
                        new_class,
                        attr_name,
                        PropertyMachine(attr.machine_type))

                return new_class

        new_attrs = wrapped_type.__dict__.copy()
        new_attrs.pop('__dict__', None)
        new_attrs.update(additional_attributes)

        return TemporaryMetaclass(
            wrapped_type.__name__,
            (wrapped_type,),
            new_attrs
        )
