import enum
import unittest

import six

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


class TestFieldMachine(unittest.TestCase):

    def test_model(self):

        class Model(_Model):

            field1 = _Field('field1')
            field2 = _Field('field2')
            field3 = _Field('field3')

        model = Model()
        self.assertEqual(3, len(model.fields))
        for name, field in model.fields.items():
            self.assertIs(True, isinstance(field, _Field))
            self.assertEqual(name, field.name)

    def test_field_machine(self):

        class Model(extras.FieldMachine.wrap(_Model)):

            field1 = _Field('field1')
            field2 = _Field('field2')
            field3 = extras.FieldMachine(_Field('field3'), Lock)

        model = Model()
        self.assertEqual(3, len(model.fields))
        for name, field in model.fields.items():
            self.assertIs(True, isinstance(field, _Field))
            self.assertEqual(name, field.name)

        self.assertEqual(model.field3, 'open')
        model.field3.lock()
        self.assertEqual(model.field3, 'locked')
        model.field3.open()
        self.assertEqual(model.field3, 'open')


class _Field(object):

    def __init__(self, name):
        self.name = name


class _ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        fields = {}
        to_delete = []
        for name, attr in attrs.items():
            if isinstance(attr, _Field):
                fields[name] = attr
                to_delete.append(attrs[name])

        attrs = {
            key: value for key, value in attrs.items() if key not in to_delete}

        attrs['fields'] = fields

        return super(cls, cls).__new__(cls, name, bases, attrs)


class _Model(six.with_metaclass(_ModelMetaclass)):

    pass
