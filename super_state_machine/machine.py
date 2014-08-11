"""State machine core."""

from enum import Enum, unique
from functools import partial

import six

from . import utils

def _get_config(meta, attr, default=[]):
    for m in [meta, DefaultMeta]:
        try:
            return getattr(m, attr)
        except AttributeError:
            pass

    if isinstance(default, list):
        raise

    return default


class DefaultMeta(object):

    states_enum_name = 'States'
    allow_empty = True


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

        try:
            states_enum = getattr(new_class, states_enum_name)
        except AttributeError:
            raise ValueError('No states enum given!')

        proper = True
        try:
            if not issubclass(states_enum, Enum):
                proper = False
        except TypeError:
            proper = False

        if not proper:
            raise ValueError(
                'Please provide enum instance for available states.')

        states_enum = unique(states_enum)

        new_meta['states_enum'] = states_enum
        new_meta['reversed_states_map'] = {s.value: s for s in states_enum}

        state_name = 'state'
        new_state_name = '_' + state_name
        new_meta['state_attribute_name'] = new_state_name
        state_value = get_config('initial_state', None)
        if not state_value:
            try:
                state_value = getattr(new_class, state_name)
            except AttributeError:
                pass

        if state_value:
            if isinstance(state_value, Enum):
                if not state_value in states_enum:
                    raise ValueError(
                        "Initial state does not belong to states enum!")
            else:
                raise ValueError(
                    "Initial value cannot be scalar, use Enum instance!")

        if not get_config('allow_empty') and not state_value:
            raise ValueError(
                "Empty state is disallowed, yet no initial state is given!")

        setattr(new_class, new_state_name, state_value)
        setattr(new_class, state_name, utils.state_property)

        setattr(new_class, 'is_', utils.is_)
        setattr(new_class, 'set_', utils.set_)

        new_methods = {}
        for s in states_enum:
            getter_name = 'is_{}'.format(s.value)
            new_methods[getter_name] = utils.generate_getter(s.value)

            setter_name = 'set_{}'.format(s.value)
            new_methods[setter_name] = utils.generate_setter(s.value)

        for name, method in new_methods.items():
            if hasattr(new_class, name):
                raise ValueError(
                    "Name collision in generated class - '{}'.".format(name))

            setattr(new_class, name, method)

        allowed_transitions = get_config('transitions', {})
        new_trans = {}
        translator = utils.EnumValueTranslator(states_enum)
        for key, transitions in allowed_transitions.items():
            if not isinstance(key, Enum):
                key = translator.translate(key)

            new_transitions = set()
            for trans in transitions:
                if not isinstance(trans, Enum):
                    trans = translator.translate(trans)
                new_transitions.add(trans)

            new_trans[key] = new_transitions

        new_meta['transitions'] = new_trans

        complete = get_config('complete', None)
        if complete is None:
            complete = not bool(allowed_transitions)

        new_meta['complete'] = complete

        new_meta['config_getter'] = get_config
        setattr(new_class, '_meta', new_meta)

        return new_class


class StateMachine(six.with_metaclass(StateMachineMetaclass)):

    pass
