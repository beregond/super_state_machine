"""Utilities for core."""

from enum import Enum

from .errors import TransitionError, AmbiguityError


def is_(self, state):
    return self.state == state


def set_(self, state):
    attr = self._meta['state_attribute_name']
    if not isinstance(state, Enum):
        try:
            state = self._meta['reversed_states_map'][state]
        except KeyError:
            raise ValueError("Tried to assign wrong value ('{}').".format(
                state))

    states_enum = self._meta['states_enum']
    if state not in states_enum:
        raise ValueError(
            "Given value ('{}') does not belongs to defined states enum."\
            .format(state))

    actual_state = getattr(self, attr)
    complete = self._meta['complete']
    if not complete and actual_state is not None:
        transitions = self._meta['transitions'][actual_state]
        if state not in transitions:
            raise TransitionError(
                "Cannot transit from '{}' to '{}'.".format(
                    actual_state.value, state.value))

    setattr(self, attr, state)


def state_getter(self):
    attr = self._meta['state_attribute_name']
    try:
        return getattr(self, attr).value
    except AttributeError:
        return None


def state_setter(self, value):
    self.set_(value)


def state_deleter(self):
    if not self._meta['config_getter']('allow_empty'):
        raise RuntimeError('State cannot be empty.')

    attr = self._meta['state_attribute_name']
    setattr(self, attr, None)


def generate_checker(value):

    @property
    def checker(self):
        return self.is_(value)

    return checker


def generate_setter(value):

    def setter(self):
        self.set_(value)

    return setter

state_property = property(state_getter, state_setter, state_deleter)


class EnumValueTranslator(object):

    def __init__(self, base_enum):
        root = {}
        for enum in base_enum:
            tmp_root = root
            for letter in enum.value:
                tmp_root = tmp_root.setdefault(letter, {})
                enum_container = tmp_root.setdefault('items', [])
                enum_container.append(enum)

        self.tree = root

    def translate(self, value):
        root = self.tree
        for letter in value:
            try:
                root = root[letter]
            except KeyError:
                raise ValueError(
                    "Wrong value given to translate ('{}')".format(value))

        if len(root['items']) == 1:
            return root['items'][0]

        raise AmbiguityError(
            "Can't decide which value is proper for value '{}', "
            "available choices are: {}.".format(
                value,
                ", ".join(
                    "'{} - {}'".format(e, e.value) for e in root['items']),
            ))
