import unittest
from enum import Enum

from super_state_machine import machines, errors


class StatesEnum(Enum):

    ONE = 'one'
    TWO = 'two'
    THREE = 'three'


class OtherEnum(Enum):

    ONE = 'one'


class TestSuperStateMachine(unittest.TestCase):

    def test_state_machine_state_is_none(self):

        class Machine(machines.StateMachine):

            class States(Enum):

                ONE = 'one'
                TWO = 'two'
                THREE = 'three'

        sm = Machine()
        self.assertIsNone(sm.state)

    def test_state_machine_is_always_scalar(self):

        class Machine(machines.StateMachine):

            class States(Enum):

                ONE = 'one'
                TWO = 'two'
                THREE = 'three'

            state = States.ONE

        sm = Machine()
        self.assertEqual(sm.state, 'one')

    def test_state_machine_allow_scalars_on_init(self):

        class Machine(machines.StateMachine):

            class States(Enum):

                ONE = 'one'
                TWO = 'two'
                THREE = 'three'

            state = 'tw'

        sm = Machine()
        self.assertIs(sm.is_two, True)

    def test_state_machine_init_value_ambiguity(self):
        try:

            class Machine(machines.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                state = 't'

        except errors.AmbiguityError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_state_machine_accepts_enums_only_from_proper_source(self):

        class OtherEnum(Enum):

            FOUR = 'four'

        try:

            class Machine(machines.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                state = OtherEnum.FOUR

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_state_machine_doesnt_allow_wrong_scalars(self):
        try:

            class Machine(machines.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                state = 'four'

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_state_machine_accepts_only_unique_enums(self):
        try:

            class Machine(machines.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'one'
                    THREE = 'three'

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_state_machine_allows_to_change_and_check_state(self):

        class Machine(machines.StateMachine):

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

        class Machine(machines.StateMachine):

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

            class Machine(machines.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                def is_one(self):
                    pass

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_name_collistion_for_setter_raises_exception(self):
        try:

            class Machine(machines.StateMachine):

                class States(Enum):

                    ONE = 'one'
                    TWO = 'two'
                    THREE = 'three'

                def set_one(self):
                    pass

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_states_enum_can_be_predefined(self):

        class Machine(machines.StateMachine):

            States = StatesEnum
            state = StatesEnum.ONE

        sm = Machine()
        self.assertIs(sm.is_one, True)

    def test_state_deleter(self):

        class Machine(machines.StateMachine):

            States = StatesEnum
            state = StatesEnum.ONE

        sm = Machine()
        self.assertIs(sm.is_one, True)
        del sm.state
        self.assertIsNone(sm.state)

    def test_disallow_empty(self):

        class Machine(machines.StateMachine):

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
            pass
        else:
            raise AssertionError('RuntimeError should be raised.')

    def test_states_enum_is_always_given(self):
        try:

            class Machine(machines.StateMachine):

                pass

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_states_enum_is_always_enum(self):
        try:

            class Machine(machines.StateMachine):

                States = 'something'

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_disallow_empty_without_initial_value(self):
        try:

            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    allow_empty = False

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_initial_value(self):

        class Machine(machines.StateMachine):

            States = StatesEnum
            state = StatesEnum.ONE

            class Meta:

                initial_state = StatesEnum.TWO

        sm = Machine()
        self.assertEqual(sm.state, 'two')
        self.assertIs(sm.is_two, True)

    def test_wrong_initial_value_from_class_is_ignored(self):

        class Machine(machines.StateMachine):

            States = StatesEnum
            state = 'wrong'

            class Meta:

                initial_state = StatesEnum.TWO

        sm = Machine()
        self.assertEqual(sm.state, 'two')
        self.assertIs(sm.is_two, True)

    def test_initial_value_from_meta_and_disallowed_empty(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

            class Meta:

                allow_empty = False
                initial_state = StatesEnum.TWO

        sm = Machine()
        self.assertEqual(sm.state, 'two')
        self.assertIs(sm.is_two, True)

    def test_disallow_assignation_of_wrong_value(self):

        class Machine(machines.StateMachine):

            class States(Enum):

                ONE = 'one'
                TWO = 'two'
                THREE = 'three'

        sm = Machine()
        sm.set_one()
        self.assertIs(sm.is_one, True)
        sm.set_(Machine.States.TWO)
        self.assertIs(sm.is_two, True)
        self.assertRaises(ValueError, sm.set_, StatesEnum.TWO)
        self.assertRaises(ValueError, sm.set_, 'four')

    def test_checker_getter_and_setter_wrong_values_and_enums(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

        sm = Machine()

        sm.is_('one')
        sm.can_be_('one')
        sm.set_('one')

        self.assertRaises(ValueError, sm.is_, 'five')
        self.assertRaises(ValueError, sm.is_, OtherEnum.ONE)
        self.assertRaises(ValueError, sm.can_be_, 'five')
        self.assertRaises(ValueError, sm.can_be_, OtherEnum.ONE)
        self.assertRaises(ValueError, sm.set_, 'five')
        self.assertRaises(ValueError, sm.set_, OtherEnum.ONE)

    def test_get_actual_state_as_enum(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

        sm = Machine()
        self.assertIsNone(sm.actual_state)
        sm.set_one()
        self.assertIs(sm.actual_state, StatesEnum.ONE)
        sm.set_two()
        self.assertIs(sm.actual_state, StatesEnum.TWO)
        del sm.state
        self.assertIsNone(sm.actual_state)

    def test_actual_state_name_collision(self):
        try:
            class Machine(machines.StateMachine):

                States = StatesEnum

                def actual_state(self):
                    pass

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_actual_state_name_collision_with_generated_methods(self):
        try:
            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_transitions = [
                        ('actual_state', 'one'),
                    ]

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_as_enum(self):

        class Machine(machines.StateMachine):

            States = StatesEnum

        sm = Machine()
        self.assertIsNone(sm.as_enum)
        sm.set_one()
        self.assertIs(sm.as_enum, StatesEnum.ONE)
        sm.set_two()
        self.assertIs(sm.as_enum, StatesEnum.TWO)
        del sm.state
        self.assertIsNone(sm.as_enum)

    def test_as_enum_name_collision(self):
        try:
            class Machine(machines.StateMachine):

                States = StatesEnum

                def as_enum(self):
                    pass

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_as_enum_name_collision_with_generated_methods(self):
        try:
            class Machine(machines.StateMachine):

                States = StatesEnum

                class Meta:

                    named_transitions = [
                        ('as_enum', 'one'),
                    ]

        except ValueError:
            pass
        else:
            raise AssertionError('ValueError should be raised.')

    def test_custom_states_enum(self):

        class Machine(machines.StateMachine):

            trololo = StatesEnum

            class Meta:

                states_enum_name = 'trololo'

        machine = Machine()
        self.assertIs(machine.is_one, False)
