"""State machine core."""

from enum import Enum, unique
from functools import partial

import six

from . import utils

def _get_config(meta, attr):
    try:
        return getattr(meta, attr)
    except AttributeError:
        return getattr(DefaultMeta, attr)


class DefaultMeta(object):

    states_enum_name = 'States'


class StateMachineMetaclass(type):

    def __new__(cls, name, bases, attrs):
        new_class =  super(cls, cls).__new__(cls, name, bases, attrs)

        parents = [b for b in bases if isinstance(b, cls)]
        if not parents:
            return new_class

        meta = getattr(new_class, 'Meta', DefaultMeta)
        get_config = partial(_get_config, meta)
        new_meta = {}

        states_enum_name = get_config('states_enum_name')
        states_enum = getattr(new_class, states_enum_name)
        states_enum = unique(states_enum)

        new_meta['states_enum'] = states_enum
        new_meta['reversed_states_map'] = {s.value: s for s in states_enum}

        state_name = 'state'
        new_state_name = '_' + state_name
        new_meta['state_attribute_name'] = new_state_name
        state_value = None

        try:
            state_value = getattr(new_class, state_name)
            if isinstance(state_value, Enum):
                if not state_value in states_enum:
                    raise ValueError(
                        'Initial state does not belong to states enum!')
            else:
                raise ValueError(
                    'Initial value cannot be scalar, use Enum instance!')

        except AttributeError:
            pass

        setattr(new_class, new_state_name, state_value)
        setattr(new_class, state_name, utils.state_property)

        new_methods = {}
        for s in states_enum:
            checker_name = 'is_{}'.format(s.value)
            new_methods[checker_name] = utils.generate_checker(s.value)

            setter_name = 'set_{}'.format(s.value)
            new_methods[setter_name] = utils.generate_setter(s.value)

        for name, method in new_methods.items():
            if hasattr(new_class, name):
                raise ValueError(
                    "Name collision in generated class - '{}'.".format(name))

            setattr(new_class, name, method)

        setattr(new_class, '_meta', new_meta)
        setattr(new_class, 'is_', utils.is_)
        setattr(new_class, 'set_', utils.set_)

        return new_class


class StateMachine(six.with_metaclass(StateMachineMetaclass)):

    pass
