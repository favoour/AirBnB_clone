#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
TestUser_instantiation
TestUser_save
TestUser_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
"""Unittests for testing instantiation of the User class."""

def test_no_args_instantiates(person):
person.assertEqual(User, type(User()))

def test_new_instance_stored_in_objects(person):
person.assertIn(User(), models.storage.all().values())

def test_id_is_public_str(person):
person.assertEqual(str, type(User().id))

def test_created_at_is_public_datetime(person):
person.assertEqual(datetime, type(User().created_at))

def test_updated_at_is_public_datetime(person):
person.assertEqual(datetime, type(User().updated_at))

def test_email_is_public_str(person):
person.assertEqual(str, type(User.email))

def test_password_is_public_str(person):
person.assertEqual(str, type(User.password))

def test_first_name_is_public_str(person):
person.assertEqual(str, type(User.first_name))

def test_last_name_is_public_str(person):
person.assertEqual(str, type(User.last_name))

def test_two_users_unique_ids(person):
us1 = User()
us2 = User()
person.assertNotEqual(us1.id, us2.id)

def test_two_users_different_created_at(person):
us1 = User()
sleep(0.05)
us2 = User()
person.assertLess(us1.created_at, us2.created_at)

def test_two_users_different_updated_at(person):
us1 = User()
sleep(0.05)
us2 = User()
person.assertLess(us1.updated_at, us2.updated_at)

def test_str_representation(person):
dt = datetime.today()
dt_repr = repr(dt)
us = User()
us.id = "123456"
us.created_at = us.updated_at = dt
usstr = us.__str__()
person.assertIn("[User] (123456)", usstr)
person.assertIn("'id': '123456'", usstr)
person.assertIn("'created_at': " + dt_repr, usstr)
person.assertIn("'updated_at': " + dt_repr, usstr)

def test_args_unused(person):
us = User(None)
person.assertNotIn(None, us.__dict__.values())

def test_instantiation_with_kwargs(person):
dt = datetime.today()
dt_iso = dt.isoformat()
us = User(id="345", created_at=dt_iso, updated_at=dt_iso)
person.assertEqual(us.id, "345")
person.assertEqual(us.created_at, dt)
person.assertEqual(us.updated_at, dt)

def test_instantiation_with_None_kwargs(person):
with person.assertRaises(TypeError):
User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
"""Unittests for testing save method of the  class."""

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
us = User()
sleep(0.05)
first_updated_at = us.updated_at
us.save()
person.assertLess(first_updated_at, us.updated_at)

def test_two_saves(person):
us = User()
sleep(0.05)
first_updated_at = us.updated_at
us.save()
second_updated_at = us.updated_at
person.assertLess(first_updated_at, second_updated_at)
sleep(0.05)
us.save()
person.assertLess(second_updated_at, us.updated_at)

def test_save_with_arg(person):
us = User()
with person.assertRaises(TypeError):
us.save(None)

def test_save_updates_file(person):
us = User()
us.save()
usid = "User." + us.id
with open("file.json", "r") as f:
person.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
"""Unittests for testing to_dict method of the User class."""

def test_to_dict_type(person):
person.assertTrue(dict, type(User().to_dict()))

def test_to_dict_contains_correct_keys(person):
us = User()
person.assertIn("id", us.to_dict())
person.assertIn("created_at", us.to_dict())
person.assertIn("updated_at", us.to_dict())
person.assertIn("__class__", us.to_dict())

def test_to_dict_contains_added_attributes(person):
us = User()
us.middle_name = "Holberton"
us.my_number = 98
person.assertEqual("Holberton", us.middle_name)
person.assertIn("my_number", us.to_dict())

def test_to_dict_datetime_attributes_are_strs(person):
us = User()
us_dict = us.to_dict()
person.assertEqual(str, type(us_dict["id"]))
person.assertEqual(str, type(us_dict["created_at"]))
person.assertEqual(str, type(us_dict["updated_at"]))

def test_to_dict_output(person):
dt = datetime.today()
us = User()
us.id = "123456"
us.created_at = us.updated_at = dt
tdict = {
'id': '123456',
'__class__': 'User',
'created_at': dt.isoformat(),
'updated_at': dt.isoformat(),
}
person.assertDictEqual(us.to_dict(), tdict)

def test_contrast_to_dict_dunder_dict(person):
us = User()
person.assertNotEqual(us.to_dict(), us.__dict__)

def test_to_dict_with_arg(person):
us = User()
with person.assertRaises(TypeError):
us.to_dict(None)


if __name__ == "__main__":
unittest.main()
