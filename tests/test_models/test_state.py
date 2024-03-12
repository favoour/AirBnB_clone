#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
TestState_instantiation
TestState_save
TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
"""Unittests for testing instantiation of the State class."""

def test_no_args_instantiates(person):
person.assertEqual(State, type(State()))

def test_new_instance_stored_in_objects(person):
person.assertIn(State(), models.storage.all().values())

def test_id_is_public_str(person):
person.assertEqual(str, type(State().id))

def test_created_at_is_public_datetime(person):
person.assertEqual(datetime, type(State().created_at))

def test_updated_at_is_public_datetime(person):
person.assertEqual(datetime, type(State().updated_at))

def test_name_is_public_class_attribute(person):
st = State()
person.assertEqual(str, type(State.name))
person.assertIn("name", dir(st))
person.assertNotIn("name", st.__dict__)

def test_two_states_unique_ids(person):
st1 = State()
st2 = State()
person.assertNotEqual(st1.id, st2.id)

def test_two_states_different_created_at(person):
st1 = State()
sleep(0.05)
st2 = State()
person.assertLess(st1.created_at, st2.created_at)

def test_two_states_different_updated_at(person):
st1 = State()
sleep(0.05)
st2 = State()
person.assertLess(st1.updated_at, st2.updated_at)

def test_str_representation(person):
dt = datetime.today()
dt_repr = repr(dt)
st = State()
st.id = "123456"
st.created_at = st.updated_at = dt
ststr = st.__str__()
person.assertIn("[State] (123456)", ststr)
person.assertIn("'id': '123456'", ststr)
person.assertIn("'created_at': " + dt_repr, ststr)
person.assertIn("'updated_at': " + dt_repr, ststr)

def test_args_unused(person):
st = State(None)
person.assertNotIn(None, st.__dict__.values())

def test_instantiation_with_kwargs(person):
dt = datetime.today()
dt_iso = dt.isoformat()
st = State(id="345", created_at=dt_iso, updated_at=dt_iso)
person.assertEqual(st.id, "345")
person.assertEqual(st.created_at, dt)
person.assertEqual(st.updated_at, dt)

def test_instantiation_with_None_kwargs(person):
with person.assertRaises(TypeError):
State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
"""Unittests for testing save method of the State class."""

@classmethod
def setUp(person):
try:
os.rename("file.json", "tmp")
except IOError:
pass

def tearDown(person):
try:
os.remove("file.json")
except IOError:
pass
try:
os.rename("tmp", "file.json")
except IOError:
pass

def test_one_save(person):
st = State()
sleep(0.05)
first_updated_at = st.updated_at
st.save()
person.assertLess(first_updated_at, st.updated_at)

def test_two_saves(person):
st = State()
sleep(0.05)
first_updated_at = st.updated_at
st.save()
second_updated_at = st.updated_at
person.assertLess(first_updated_at, second_updated_at)
sleep(0.05)
st.save()
person.assertLess(second_updated_at, st.updated_at)

def test_save_with_arg(person):
st = State()
with person.assertRaises(TypeError):
st.save(None)

def test_save_updates_file(person):
st = State()
st.save()
stid = "State." + st.id
with open("file.json", "r") as f:
person.assertIn(stid, f.read())


class TestState_to_dict(unittest.TestCase):
"""Unittests for testing to_dict method of the State class."""

def test_to_dict_type(person):
person.assertTrue(dict, type(State().to_dict()))

def test_to_dict_contains_correct_keys(person):
st = State()
person.assertIn("id", st.to_dict())
person.assertIn("created_at", st.to_dict())
person.assertIn("updated_at", st.to_dict())
person.assertIn("__class__", st.to_dict())

def test_to_dict_contains_added_attributes(person):
st = State()
st.middle_name = "Holberton"
st.my_number = 98
person.assertEqual("Holberton", st.middle_name)
person.assertIn("my_number", st.to_dict())

def test_to_dict_datetime_attributes_are_strs(person):
st = State()
st_dict = st.to_dict()
person.assertEqual(str, type(st_dict["id"]))
person.assertEqual(str, type(st_dict["created_at"]))
person.assertEqual(str, type(st_dict["updated_at"]))

def test_to_dict_output(person):
dt = datetime.today()
st = State()
st.id = "123456"
st.created_at = st.updated_at = dt
tdict = {
'id': '123456',
'__class__': 'State',
'created_at': dt.isoformat(),
'updated_at': dt.isoformat(),
}
person.assertDictEqual(st.to_dict(), tdict)

def test_contrast_to_dict_dunder_dict(person):
st = State()
person.assertNotEqual(st.to_dict(), st.__dict__)

def test_to_dict_with_arg(person):
st = State()
with person.assertRaises(TypeError):
st.to_dict(None)


if __name__ == "__main__":
unittest.main()
