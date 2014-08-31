"""Utilities for core."""

from enum import Enum, unique
from functools import wraps

from .errors import TransitionError, AmbiguityError


def is_(self, state):
    """Check if machine is in given state."""
    translator = self._meta['translator']
    state = translator.translate(state)
    return self.actual_state == state


def can_be_(self, state):
    """Check if machine can transit to given state."""
    translator = self._meta['translator']
    state = translator.translate(state)

    if self._meta['complete']:
        return True

    if self.actual_state is None:
        return True

    transitions = self._meta['transitions'][self.actual_state]
    return state in transitions


def set_(self, state):
    """Set new state for machine."""
    translator = self._meta['translator']
    state = translator.translate(state)

    if not self.can_be_(state):
        raise TransitionError(
            "Cannot transit from '{}' to '{}'.".format(
                self.actual_state.value, state.value))

    attr = self._meta['state_attribute_name']
    setattr(self, attr, state)


def state_getter(self):
    """Get actual state as value."""
    try:
        return self.actual_state.value
    except AttributeError:
        return None


def state_setter(self, value):
    """Set new state for machine."""
    self.set_(value)


def state_deleter(self):
    """Delete state.

    In fact just set actual state to `None`.

    """
    if not self._meta['config_getter']('allow_empty'):
        raise RuntimeError('State cannot be empty.')

    attr = self._meta['state_attribute_name']
    setattr(self, attr, None)


def generate_getter(value):
    """Generate getter for given value."""
    @property
    @wraps(is_)
    def getter(self):
        return self.is_(value)

    return getter


def generate_checker(value):
    """Generate state checker for given value."""
    @property
    @wraps(can_be_)
    def checker(self):
        return self.can_be_(value)

    return checker


def generate_setter(value):
    """Generate setter for given value."""
    @wraps(set_)
    def setter(self):
        self.set_(value)

    return setter

state_property = property(state_getter, state_setter, state_deleter)


@property
def actual_state(self):
    """Actual state as `None` or `enum` instance."""
    attr = self._meta['state_attribute_name']
    return getattr(self, attr)


@property
def as_enum(self):
    """Return actual state as enum."""
    return self.actual_state


class EnumValueTranslator(object):

    """Helps to find enum element by (part of) its value."""

    def __init__(self, base_enum):
        """Init.

        :param enum base_enum: Enum, to which elements values are translated.

        """
        base_enum = unique(base_enum)
        self.base_enum = base_enum
        self._generate_values_tree()

    def translate(self, value):
        """Translate value to enum instance.

        If value is already enum instance, check if this value belongs to base
        enum.

        """
        is_proper = self._check_if_already_proper(value)
        if is_proper:
            return value

        items = self._get_matching_items(value)
        if len(items) == 1:
            return items[0]
        else:
            raise AmbiguityError(
                "Can't decide which value is proper for value '{}', "
                "available choices are: {}.".format(
                    value,
                    ", ".join(
                        "'{} - {}'".format(e, e.value) for e in items),
                ))

    def _get_matching_items(self, value):
        root = self._values_tree
        for letter in value:
            try:
                root = root[letter]
            except KeyError:
                raise ValueError(
                    "Unrecognized value ('{}').".format(value))

        try:
            return root['hit']
        except KeyError:
            return root['items']

    def _generate_values_tree(self):
        root = {}

        for enum in self.base_enum:
            tmp_root = root
            index = 1
            length = len(enum.value)

            for letter in enum.value:
                tmp_root = tmp_root.setdefault(letter, {})
                if index == length:
                    tmp_root['hit'] = [enum]
                else:
                    enum_container = tmp_root.setdefault('items', [])
                    enum_container.append(enum)
                index += 1

        self._values_tree = root

    def _check_if_already_proper(self, value):
        if isinstance(value, Enum):
            if value not in self.base_enum:
                raise ValueError(
                    "Given value ('{}') doesn't belong to states enum."
                    .format(value))

            return True

        return False
