"""Utilities for core."""


def is_(self, state):
    return self.state == state


def set_(self, state):
    attr = self._meta['state_attribute_name']
    state = self._meta['reversed_states_map'][state]
    setattr(self, attr, state)


def state_getter(self):
    attr = self._meta['state_attribute_name']
    try:
        return getattr(self, attr).value
    except AttributeError:
        return None


def state_setter(self, value):
    attr = self._meta['state_attribute_name']
    return setattr(self, attr, value)


def state_deleter(self):
    pass


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
