import unittest
from enum import Enum

from super_state_machine import machines, errors


class StatesEnum(Enum):

    ONE = 'one'
    TWO = 'two'
    THREE = 'three'
    FOUR = 'four'


class OtherEnum(Enum):

    ONE = 'one'


class TestSuperStateMachineTransitions(unittest.TestCase):

    def test_transitions(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                transitions = {
                    StatesEnum.ONE: [StatesEnum.TWO, StatesEnum.THREE],
                    StatesEnum.TWO: [StatesEnum.ONE, StatesEnum.THREE],
                    StatesEnum.THREE: [StatesEnum.TWO],
                }

        sm = Machine()
        self.assertIsNone(sm.state)
        sm.set_one()
        self.assertIs(sm.is_one, True)
        sm.set_two()
        sm.set_three()

        self.assertRaises(errors.TransitionError, sm.set_one)
        self.assertIs(sm.is_three, True)

        self.assertRaises(errors.TransitionError, sm.set_, 'one')
        self.assertIs(sm.is_three, True)

        try:
            sm.state = 'one'
        except errors.TransitionError:
            pass
        else:
            raise AssertionError('TransitionError should be raised.')

        self.assertIs(sm.is_three, True)

        sm.set_two()
        sm.set_one()
        self.assertIs(sm.is_one, True)

    def test_reduced_transition_graph(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                transitions = {
                    'o': ['tw', 'th'],
                    'tw': ['o', 'th'],
                    'th': ['tw'],
                }

        sm = Machine()
        self.assertIsNone(sm.state)
        sm.set_one()
        self.assertIs(sm.is_one, True)
        sm.set_two()
        sm.set_three()

        self.assertRaises(errors.TransitionError, sm.set_one)
        self.assertIs(sm.is_three, True)

        self.assertRaises(errors.TransitionError, sm.set_, 'one')
        self.assertIs(sm.is_three, True)

    def test_transitions_checkers(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                transitions = {
                    'o': ['tw', 'th'],
                    'tw': ['o', 'th'],
                    'th': ['tw', 'th'],
                }

        sm = Machine()
        self.assertIs(sm.can_be_('one'), True)
        self.assertIs(sm.can_be_('two'), True)
        self.assertIs(sm.can_be_('three'), True)
        self.assertIs(sm.can_be_('four'), True)
        self.assertIs(sm.can_be_one, True)
        self.assertIs(sm.can_be_two, True)
        self.assertIs(sm.can_be_three, True)
        self.assertIs(sm.can_be_four, True)

        sm.set_one()
        self.assertIs(sm.can_be_one, False)
        self.assertIs(sm.can_be_two, True)
        self.assertIs(sm.can_be_three, True)
        self.assertIs(sm.can_be_four, False)

        self.assertRaises(errors.TransitionError, sm.set_one)

        sm.set_two()
        self.assertIs(sm.can_be_one, True)
        self.assertIs(sm.can_be_two, False)
        self.assertIs(sm.can_be_three, True)
        self.assertIs(sm.can_be_four, False)

        sm.set_three()
        self.assertIs(sm.can_be_one, False)
        self.assertIs(sm.can_be_two, True)
        self.assertIs(sm.can_be_three, True)
        self.assertIs(sm.can_be_four, False)

        sm.set_three()

    def test_transitions_checkers_with_complete_graph(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                complete = True
                transitions = {
                    'o': ['tw', 'th'],
                    'tw': ['o', 'th'],
                    'th': ['tw', 'th'],
                }

        sm = Machine()
        sm.set_three()
        self.assertIs(sm.can_be_one, True)
        self.assertIs(sm.can_be_two, True)
        self.assertIs(sm.can_be_three, True)
        self.assertIs(sm.can_be_four, True)
        sm.set_four()
        self.assertIs(sm.is_four, True)

    def test_named_transitions_checkers(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                transitions = {
                    'o': ['tw', 'th'],
                    'tw': ['o', 'th'],
                    'th': ['tw', 'th'],
                }
                named_checkers = [
                    ('can_go_to_one', 'one'),
                    ('can_become_two', StatesEnum.TWO),
                ]

            @property
            def can_one(self):
                return self.can_be_('one')

        sm = Machine()
        sm.set_two()
        self.assertIs(sm.can_be_one, True)
        self.assertIs(sm.can_one, True)
        self.assertIs(sm.can_go_to_one, True)
        self.assertIs(sm.can_become_two, False)

    def test_named_transitions_checkers_cant_overwrite_methods(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_checkers = [
                        ('can_one', 'one'),
                    ]

                @property
                def can_one(self):
                    return self.can_be_('one')

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_named_checkers_cant_overwrite_generated_methods(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_checkers = [
                        ('can_be_one', 'one'),
                    ]

                @property
                def can_one(self):
                    return self.can_be_('one')

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_named_checkers_dont_accept_wrong_values(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_checkers = [
                        ('can_become_five', 'five'),
                    ]

                @property
                def can_one(self):
                    return self.can_be_('one')

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_named_checkers_dont_accept_wrong_enums(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_checkers = [
                        ('can_be_other_one', OtherEnum.ONE),
                    ]

                @property
                def can_one(self):
                    return self.can_be_('one')

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_transitions_with_wrong_enum(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    transitions = {
                        OtherEnum.ONE: [StatesEnum.TWO, StatesEnum.THREE],
                        StatesEnum.TWO: [StatesEnum.ONE, StatesEnum.THREE],
                        StatesEnum.THREE: [StatesEnum.TWO],
                    }

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_transition_graph_is_complete(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                transitions = {
                    'th': ['f'],
                }

        sm = Machine()
        self.assertIs(sm.can_be_four, True)
        sm.set_four()
        self.assertIs(sm.can_be_three, False)

    def test_named_transitions(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                transitions = {
                    'o': ['tw', 'th'],
                    'tw': ['o', 'th'],
                    'th': ['tw'],
                }
                named_transitions = [
                    ('run', 'one'),
                    ('confirm', 'two'),
                    ('cancel', StatesEnum.THREE),
                ]

        sm = Machine()
        self.assertIsNone(sm.state)
        sm.run()
        self.assertIs(sm.is_one, True)
        sm.confirm()
        self.assertIs(sm.is_two, True)
        sm.cancel()
        self.assertIs(sm.is_three, True)

    def test_named_transitions_collisions(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    transitions = {
                        'o': ['tw', 'th'],
                        'tw': ['o', 'th'],
                        'th': ['tw'],
                    }
                    named_transitions = [
                        ('run', 'one'),
                        ('confirm', 'two'),
                        ('cancel', 'three'),
                    ]

                def run(self):
                    pass

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_named_transitions_collisions_with_auto_generated_methods(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_transitions = [
                        ('is_one', 'one'),
                        ('confirm', 'two'),
                        ('cancel', 'three'),
                    ]

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_named_transitions_wrong_value(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_transitions = [
                        ('run', 'five'),
                        ('confirm', 'two'),
                        ('cancel', 'three'),
                    ]

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_named_transitions_wrong_enum(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_transitions = [
                        ('run', OtherEnum.ONE),
                        ('confirm', 'two'),
                        ('cancel', 'three'),
                    ]

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_named_transitions_are_in_state_graph(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                named_transitions = [
                    ('run', 'one'),
                    ('confirm', 'two'),
                    ('cancel', 'three'),
                ]

        sm = Machine()
        sm.set_one()
        self.assertIs(sm.can_be_one, True)
        self.assertIs(sm.can_be_two, True)
        self.assertIs(sm.can_be_three, True)
        self.assertIs(sm.can_be_four, False)

    def test_named_transitions_with_restricted_source(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                named_transitions = [
                    ('run', 'o', None),
                    ('confirm', 'two', 'o'),
                    ('cancel', 'three', ['o', 'tw']),
                    ('surprise', 'four', [])
                ]

        sm = Machine()
        sm.run()
        self.assertIs(sm.can_be_one, False)
        self.assertIs(sm.can_be_two, True)
        self.assertIs(sm.can_be_three, True)
        sm.confirm()
        self.assertIs(sm.can_be_one, False)
        self.assertIs(sm.can_be_three, True)
        self.assertIs(sm.can_be_four, False)
        self.assertIs(sm.can_be_two, False)
        sm.cancel()
        self.assertIs(sm.is_three, True)

    def test_restricted_source_proper_value(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_transitions = [
                        ('run', 'o', None),
                        ('confirm', 'two', 'o'),
                        ('cancel', 'three', ['o', 'tw']),
                        ('surprise', 'four', ['five'])
                    ]

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_restricted_source_proper_enum(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_transitions = [
                        ('run', 'o', None),
                        ('confirm', 'two', 'o'),
                        ('cancel', 'three', ['o', 'tw']),
                        ('surprise', 'four', OtherEnum.ONE)
                    ]

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')
