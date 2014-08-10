"""Utilities for core."""

from enum import Enum

from .errors import TransitionError


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
