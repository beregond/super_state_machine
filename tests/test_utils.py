import unittest
from enum import Enum

from super_state_machine import utils, errors


class StatesEnum(Enum):

    ONE = 'one'
    TWO = 'two'
    THREE = 'three'
    FOUR = 'four'


class OtherEnum(Enum):

    ONE = 'one'


class NonUniqueEnum(Enum):

    ONE = 'one'
    TWO = 'two'
    THREE = 'one'


class CollidingEnum(Enum):

    OPEN = 'open'
    OPENING = 'opening'
    CLOSE = 'close'
    CLOSED = 'closed'


class TestSuperStateMachineEnumValueTranslator(unittest.TestCase):

    def test_translator(self):
        trans = utils.EnumValueTranslator(StatesEnum)
        self.assertEqual(trans.translate('one'), StatesEnum.ONE)
        self.assertEqual(trans.translate('o'), StatesEnum.ONE)
        self.assertEqual(trans.translate('two'), StatesEnum.TWO)
        self.assertEqual(trans.translate('tw'), StatesEnum.TWO)
        self.assertEqual(trans.translate('three'), StatesEnum.THREE)
        self.assertEqual(trans.translate('th'), StatesEnum.THREE)
        self.assertEqual(trans.translate('thr'), StatesEnum.THREE)
        self.assertEqual(trans.translate('thre'), StatesEnum.THREE)
        self.assertEqual(trans.translate('four'), StatesEnum.FOUR)
        self.assertEqual(trans.translate('f'), StatesEnum.FOUR)

    def test_translator_for_wrong_values(self):
        trans = utils.EnumValueTranslator(StatesEnum)
        self.assertRaises(ValueError, trans.translate, 'a')
        self.assertRaises(ValueError, trans.translate, 'x')
        self.assertRaises(ValueError, trans.translate, 'threex')
        self.assertRaises(ValueError, trans.translate, 'threx')
        self.assertRaises(ValueError, trans.translate, 'fake')

    def test_translator_for_ambiguity(self):
        trans = utils.EnumValueTranslator(StatesEnum)
        self.assertRaises(errors.AmbiguityError, trans.translate, 't')

    def test_translator_for_enum_value(self):
        trans = utils.EnumValueTranslator(StatesEnum)
        self.assertIs(trans.translate(StatesEnum.ONE), StatesEnum.ONE)
        self.assertIs(trans.translate(StatesEnum.TWO), StatesEnum.TWO)
        self.assertRaises(ValueError, trans.translate, OtherEnum.ONE)

    def test_translator_doesnt_accept_non_unique_enums(self):
        self.assertRaises(ValueError, utils.EnumValueTranslator, NonUniqueEnum)

    def test_colliding_enum(self):
        trans = utils.EnumValueTranslator(CollidingEnum)
        self.assertRaises(ValueError, trans.translate, 'ope')
        self.assertIs(trans.translate('open'), CollidingEnum.OPEN)
        self.assertIs(trans.translate('openi'), CollidingEnum.OPENING)
        self.assertRaises(ValueError, trans.translate, 'clos')
        self.assertIs(trans.translate('close'), CollidingEnum.CLOSE)
        self.assertIs(trans.translate('closed'), CollidingEnum.CLOSED)
