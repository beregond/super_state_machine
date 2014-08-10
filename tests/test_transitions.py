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
