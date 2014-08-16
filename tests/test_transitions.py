import unittest
from enum import Enum

from super_state_machine import machine, errors


class StatesEnum(Enum):

    ONE = 'one'
    TWO = 'two'
    THREE = 'three'
    FOUR = 'four'


class TestSuperStateMachineTransitions(unittest.TestCase):

    def test_transitions(self):

        class Machine(machine.StateMachine):

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
            raise RuntimeError('TransitionError should be raised.')

        self.assertIs(sm.is_three, True)

        sm.set_two()
        sm.set_one()
        self.assertIs(sm.is_one, True)

    def test_reduced_transition_graph(self):

        class Machine(machine.StateMachine):

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

        class Machine(machine.StateMachine):

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

        class Machine(machine.StateMachine):

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

        class Machine(machine.StateMachine):

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

            class Machine(machine.StateMachine):

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
            raise RuntimeError('ValueError should be raised.')

    def test_named_checkers_cant_overwrite_generated_methods(self):
        try:

            class Machine(machine.StateMachine):

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
            raise RuntimeError('ValueError should be raised.')

    def test_named_checkers_dont_accept_wrong_values(self):
        try:

            class Machine(machine.StateMachine):

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
            raise RuntimeError('ValueError should be raised.')

    def test_named_checkers_dont_accept_wrong_enums(self):

        class OtherEnum(Enum):

            ONE = 'one'

        try:

            class Machine(machine.StateMachine):

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
            raise RuntimeError('ValueError should be raised.')
