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

    def test_can_be_property_of_non_hashable_objects(self):

        class Door(object):

            lock1 = extras.PropertyMachine(Lock)
            lock2 = extras.PropertyMachine(Lock)

            def __hash__(self):
                raise RuntimeError('You shall not pass!')

        door = Door()
        self.assertEqual(door.lock1, 'open')
        self.assertEqual(door.lock2, 'open')
        door.lock1.lock()


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

    def test_inheritance(self):

        class Computer(object):

            def what_is_the_ultimate_question(self):
                return 'dunno'

        class Model(extras.FieldMachine.wrap(_Model), Computer):

            field1 = _Field('field1')
            field2 = _Field('field2')
            field3 = extras.FieldMachine(_Field('field3'), Lock)

        model = Model()
        self.assertIs(True, isinstance(model, Model))
        self.assertIs(True, isinstance(model, _Model))
        self.assertIs(True, isinstance(model, Computer))
        self.assertEqual(42, model.what_is_the_ultimate_answer())
        self.assertEqual('dunno', model.what_is_the_ultimate_question())

    def test_wrap_allows_to_add_additional_attributes(self):

        class Computer(object):

            def chuck(self):
                return 'testa'

        def one(self):
            return 'one'

        def two(self):
            return 'two'

        new_attributes = {
            'chuck': one,
            'two': two,
        }

        wrapped_type = extras.FieldMachine.wrap(_Model, new_attributes)

        wrapped_type_instance = wrapped_type()

        self.assertEqual('one', wrapped_type_instance.chuck())
        self.assertEqual('two', wrapped_type_instance.two())

        class Model(wrapped_type, Computer):

            field1 = _Field('field1')
            field2 = _Field('field2')
            field3 = extras.FieldMachine(_Field('field3'), Lock)

        model = Model()
        self.assertEqual('one', model.chuck())
        self.assertEqual('two', model.two())


class _Field(object):

    def __init__(self, name):
        self.name = name


class _ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        fields = {}
        to_delete = []
        for attr_name, attr in attrs.items():
            if isinstance(attr, _Field):
                fields[attr_name] = attr
                to_delete.append(attrs[attr_name])

        attrs = {
            key: value for key, value in attrs.items() if key not in to_delete}

        attrs['fields'] = fields

        return super(_ModelMetaclass, cls).__new__(cls, name, bases, attrs)


class _Model(six.with_metaclass(_ModelMetaclass)):

    def what_is_the_ultimate_answer(self):
        return 42
