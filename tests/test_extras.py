import enum
import unittest

from super_state_machine import extras, machines


class Lock(machines.StateMachine):

    class States(enum.Enum):

        OPEN = 'open'
        LOCKED = 'locked'

    class Meta:
        allow_empty = False
        initial_state = 'open'
        named_transitions = {
            ('lock', 'locked'),
            ('open', 'open'),
        }


class TestPropertyMachine(unittest.TestCase):

    def test_property_machine(self):

        class Door(object):

            lock1 = extras.PropertyMachine(Lock)
            lock2 = extras.PropertyMachine(Lock)

        door = Door()
        self.assertEqual(door.lock1, 'open')
        self.assertEqual(door.lock2, 'open')
        door.lock1.lock()
        self.assertEqual(door.lock1, 'locked')
        self.assertEqual(door.lock2, 'open')
        door.lock2.state_machine.lock()
        self.assertEqual(door.lock1, 'locked')
        self.assertEqual(door.lock2, 'locked')
        door.lock1.open()
        door.lock2.open()
        self.assertEqual(door.lock1, 'open')
        self.assertEqual(door.lock2, 'open')
