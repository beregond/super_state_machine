import unittest
from enum import Enum

from super_state_machine import machine


class StatesEnum(Enum):

    ONE = 'one'
    TWO = 'two'
    THREE = 'three'


class TestSuperStateMachineTransitions(unittest.TestCase):

    pass
