import unittest
from enum import Enum

from super_state_machine import machine


class StatesEnum(Enum):

    ONE = 'one'
    TWO = 'two'
    THREE = 'three'


class TestSuperStateMachine(unittest.TestCase):

    def test_state_machine_state_is_none(self):

        class Machine(machine.StateMachine):

            class States(Enum):

                ONE = 'one'
                TWO = 'two'
                THREE = 'three'

        sm = Machine()
        self.assertIsNone(sm.state)

    def test_state_machine_is_always_scalar(self):

        class Machine(machine.StateMachine):

            class States(Enum):

                ONE = 'one'
                TWO = 'two'
                THREE = 'three'

            state = States.ONE

        sm = Machine()
        self.assertEqual(sm.state, 'one')

    def test_state_machine_doesnt_allow_scalars_on_init(self):
        try:

            class Machine(machine.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                state = 'two'

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_state_machine_accepts_enums_only_from_proper_source(self):

        class OtherEnum(Enum):

            FOUR = 'four'

        try:

            class Machine(machine.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                state = OtherEnum.FOUR

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_state_machine_doesnt_allow_wrong_scalars(self):
        try:

            class Machine(machine.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                state = 'four'

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_state_machine_accepts_only_unique_enums(self):
        try:

            class Machine(machine.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'one'
                    THREE = 'three'

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_state_machine_allows_to_change_and_check_state(self):

        class Machine(machine.StateMachine):

            class States(Enum):

                ONE = 'one'
                TWO = 'two'
                THREE = 'three'

        sm = Machine()
        self.assertIsNone(sm.state)
        self.assertIs(sm.is_('one'), False)
        sm.state = Machine.States.ONE
        self.assertIs(sm.is_('one'), True)
        self.assertEqual(sm.state, 'one')
        self.assertIs(sm.is_('two'), False)
        sm.set_('two')
        self.assertIs(sm.is_('two'), True)


    def test_state_machine_allows_to_change_and_check_state_by_methods(self):

        class Machine(machine.StateMachine):

            class States(Enum):

                ONE = 'one'
                TWO = 'two'
                THREE = 'three'

        sm = Machine()
        self.assertIsNone(sm.state)
        self.assertIs(sm.is_one, False)
        sm.state = Machine.States.ONE
        self.assertIs(sm.is_one, True)
        self.assertEqual(sm.state, 'one')
        self.assertIs(sm.is_two, False)
        sm.set_two()
        self.assertIs(sm.is_two, True)

    def test_name_collistion_for_checker_raises_exception(self):
        try:

            class Machine(machine.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                def is_one(self):
                    pass

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_name_collistion_for_setter_raises_exception(self):
        try:

            class Machine(machine.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                def set_one(self):
                    pass

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_states_enum_can_be_predefined(self):

        class Machine(machine.StateMachine):

            States = StatesEnum
            state = StatesEnum.ONE

        sm = Machine()
        self.assertIs(sm.is_one, True)

    def test_state_deleter(self):

        class Machine(machine.StateMachine):

            States = StatesEnum
            state = StatesEnum.ONE

        sm = Machine()
        self.assertIs(sm.is_one, True)
        del sm.state
        self.assertIsNone(sm.state)

    def test_disallow_empty(self):

        class Machine(machine.StateMachine):

            States = StatesEnum
            state = StatesEnum.ONE

            class Meta:

                allow_empty = False

        sm = Machine()
        self.assertEqual(sm.state, 'one')
        sm.set_two()
        self.assertTrue(sm.is_two)

        try:
            del sm.state
        except RuntimeError:
            return

        raise RuntimeError('RuntimeError should be raised.')

    def test_states_enum_is_always_given(self):
        try:

            class Machine(machine.StateMachine):

                pass

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_states_enum_is_always_enum(self):
        try:

            class Machine(machine.StateMachine):

                States = 'something'

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_disallow_empty_without_initial_value(self):
        try:

            class Machine(machine.StateMachine):

                States = StatesEnum

                class Meta:

                    allow_empty = False

        except ValueError:
            return

        raise RuntimeError('ValueError should be raised.')

    def test_initial_value(self):

        class Machine(machine.StateMachine):

            States = StatesEnum
            state = StatesEnum.ONE

            class Meta:

                initial_state = StatesEnum.TWO

        sm = Machine()
        self.assertEqual(sm.state, 'two')
        self.assertIs(sm.is_two, True)

    def test_wrong_initial_value_from_class_is_ignored(self):

        class Machine(machine.StateMachine):

            States = StatesEnum
            state = 'wrong'

            class Meta:

                initial_state = StatesEnum.TWO

        sm = Machine()
        self.assertEqual(sm.state, 'two')
        self.assertIs(sm.is_two, True)

    def test_initial_value_from_meta_and_disallowed_empty(self):

        class Machine(machine.StateMachine):

            States = StatesEnum

            class Meta:

                allow_empty = False
                initial_state = StatesEnum.TWO

        sm = Machine()
        self.assertEqual(sm.state, 'two')
        self.assertIs(sm.is_two, True)
