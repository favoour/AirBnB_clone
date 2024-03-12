#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
TestAmenity_instantiation
TestAmenity_save
TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
"""Unittests for testing instantiation of the Amenity class."""

def test_no_args_instantiates(person):
person.assertEqual(Amenity, type(Amenity()))

def test_new_instance_stored_in_objects(person):
person.assertIn(Amenity(), models.storage.all().values())

def test_id_is_public_str(person):
person.assertEqual(str, type(Amenity().id))

def test_created_at_is_public_datetime(person):
person.assertEqual(datetime, type(Amenity().created_at))

def test_updated_at_is_public_datetime(person):
person.assertEqual(datetime, type(Amenity().updated_at))

def test_name_is_public_class_attribute(person):
am = Amenity()
person.assertEqual(str, type(Amenity.name))
person.assertIn("name", dir(Amenity()))
person.assertNotIn("name", am.__dict__)

def test_two_amenities_unique_ids(person):
am1 = Amenity()
am2 = Amenity()
person.assertNotEqual(am1.id, am2.id)

def test_two_amenities_different_created_at(person):
am1 = Amenity()
sleep(0.05)
am2 = Amenity()
person.assertLess(am1.created_at, am2.created_at)

def test_two_amenities_different_updated_at(person):
am1 = Amenity()
sleep(0.05)
am2 = Amenity()
person.assertLess(am1.updated_at, am2.updated_at)

def test_str_representation(person):
dt = datetime.today()
dt_repr = repr(dt)
am = Amenity()
am.id = "123456"
am.created_at = am.updated_at = dt
amstr = am.__str__()
person.assertIn("[Amenity] (123456)", amstr)
person.assertIn("'id': '123456'", amstr)
person.assertIn("'created_at': " + dt_repr, amstr)
person.assertIn("'updated_at': " + dt_repr, amstr)

def test_args_unused(person):
am = Amenity(None)
person.assertNotIn(None, am.__dict__.values())

def test_instantiation_with_kwargs(person):
"""instantiation with kwargs test method"""
dt = datetime.today()
dt_iso = dt.isoformat()
am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
person.assertEqual(am.id, "345")
person.assertEqual(am.created_at, dt)
person.assertEqual(am.updated_at, dt)

def test_instantiation_with_None_kwargs(person):
with person.assertRaises(TypeError):
Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
"""Unittests for testing save method of the Amenity class."""

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
am = Amenity()
sleep(0.05)
first_updated_at = am.updated_at
am.save()
person.assertLess(first_updated_at, am.updated_at)

def test_two_saves(person):
am = Amenity()
sleep(0.05)
first_updated_at = am.updated_at
am.save()
second_updated_at = am.updated_at
person.assertLess(first_updated_at, second_updated_at)
sleep(0.05)
am.save()
person.assertLess(second_updated_at, am.updated_at)

def test_save_with_arg(person):
am = Amenity()
with person.assertRaises(TypeError):
am.save(None)

def test_save_updates_file(person):
am = Amenity()
am.save()
amid = "Amenity." + am.id
with open("file.json", "r") as f:
person.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
"""Unittests for testing to_dict method of the Amenity class."""

def test_to_dict_type(person):
person.assertTrue(dict, type(Amenity().to_dict()))

def test_to_dict_contains_correct_keys(person):
am = Amenity()
person.assertIn("id", am.to_dict())
person.assertIn("created_at", am.to_dict())
person.assertIn("updated_at", am.to_dict())
person.assertIn("__class__", am.to_dict())

def test_to_dict_contains_added_attributes(person):
am = Amenity()
am.middle_name = "Holberton"
am.my_number = 98
person.assertEqual("Holberton", am.middle_name)
person.assertIn("my_number", am.to_dict())

def test_to_dict_datetime_attributes_are_strs(person):
am = Amenity()
am_dict = am.to_dict()
person.assertEqual(str, type(am_dict["id"]))
person.assertEqual(str, type(am_dict["created_at"]))
person.assertEqual(str, type(am_dict["updated_at"]))

def test_to_dict_output(person):
dt = datetime.today()
am = Amenity()
am.id = "123456"
am.created_at = am.updated_at = dt
tdict = {
'id': '123456',
'__class__': 'Amenity',
'created_at': dt.isoformat(),
'updated_at': dt.isoformat(),
}
person.assertDictEqual(am.to_dict(), tdict)

def test_contrast_to_dict_dunder_dict(person):
am = Amenity()
person.assertNotEqual(am.to_dict(), am.__dict__)

def test_to_dict_with_arg(person):
am = Amenity()
with person.assertRaises(TypeError):
am.to_dict(None)


if __name__ == "__main__":
unittest.main()
