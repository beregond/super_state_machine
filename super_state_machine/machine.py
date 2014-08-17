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

        translator = utils.EnumValueTranslator(states_enum)
        new_meta['translator'] = translator

        state_name = 'state'
        new_state_name = '_' + state_name
        new_meta['state_attribute_name'] = new_state_name

        state_value = get_config('initial_state', None)
        state_value = state_value or getattr(new_class, state_name, None)

        if state_value:
            state_value = translator.translate(state_value)

        if not get_config('allow_empty') and not state_value:
            raise ValueError(
                "Empty state is disallowed, yet no initial state is given!")

        setattr(new_class, new_state_name, state_value)
        setattr(new_class, state_name, utils.state_property)

        setattr(new_class, 'is_', utils.is_)
        setattr(new_class, 'can_be_', utils.can_be_)
        setattr(new_class, 'set_', utils.set_)

        allowed_transitions = get_config('transitions', {})
        new_trans = {}
        for key, transitions in allowed_transitions.items():
            key = translator.translate(key)

            new_transitions = set()
            for trans in transitions:
                if not isinstance(trans, Enum):
                    trans = translator.translate(trans)
                new_transitions.add(trans)

            new_trans[key] = new_transitions

        for state in states_enum:
            if state not in new_trans:
                new_trans[state] = set()

        new_methods = {}
        for state in states_enum:
            getter_name = 'is_{}'.format(state.value)
            new_methods[getter_name] = utils.generate_getter(state)

            setter_name = 'set_{}'.format(state.value)
            new_methods[setter_name] = utils.generate_setter(state)

            checker_name = 'can_be_{}'.format(state.value)
            new_methods[checker_name] = utils.generate_checker(state)

        new_methods['actual_state'] = utils.actual_state

        named_checkers = get_config('named_checkers', None) or []
        for method, key in named_checkers:
            if method in new_methods:
                raise ValueError(
                    "Name collision for named checker '{}' - this name is "
                    "reserved for other auto generated method.".format(method))

            key = translator.translate(key)
            new_methods[method] = utils.generate_checker(key.value)

        named_transitions = get_config('named_transitions', None) or []
        for item in named_transitions:
            try:
                method, key = item
                from_values = states_enum
            except ValueError:
                method, key, from_values = item
                if from_values is None:
                    from_values = []
                if not isinstance(from_values, list):
                    from_values = list((from_values,))

            if method in new_methods:
                raise ValueError(
                    "Name collision for transition '{}' - this name is "
                    "reserved for other auto generated method.".format(method))

            key = translator.translate(key)
            new_methods[method] = utils.generate_setter(key)

            if from_values:
                from_values = [translator.translate(k) for k in from_values]
                for s in states_enum:
                    if s in from_values:
                        new_trans[s].add(key)

        for name, method in new_methods.items():
            if hasattr(new_class, name):
                raise ValueError(
                    "Name collision in state machine class - '{}'."
                    .format(name))

            setattr(new_class, name, method)

        new_meta['transitions'] = new_trans

        complete = get_config('complete', None)
        if complete is None:
            complete = not (allowed_transitions or named_transitions)

        new_meta['complete'] = complete

        new_meta['config_getter'] = get_config
        setattr(new_class, '_meta', new_meta)

        return new_class


class StateMachine(six.with_metaclass(StateMachineMetaclass)):

    pass
