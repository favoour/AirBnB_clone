#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
TestCity_instantiation
TestCity_save
TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
"""Unittests for testing instantiation of the City class."""

def test_no_args_instantiates(person):
person.assertEqual(City, type(City()))

def test_new_instance_stored_in_objects(person):
person.assertIn(City(), models.storage.all().values())

def test_id_is_public_str(person):
person.assertEqual(str, type(City().id))

def test_created_at_is_public_datetime(person):
person.assertEqual(datetime, type(City().created_at))

def test_updated_at_is_public_datetime(person):
person.assertEqual(datetime, type(City().updated_at))

def test_state_id_is_public_class_attribute(person):
cy = City()
person.assertEqual(str, type(City.state_id))
person.assertIn("state_id", dir(cy))
person.assertNotIn("state_id", cy.__dict__)

def test_name_is_public_class_attribute(person):
cy = City()
person.assertEqual(str, type(City.name))
person.assertIn("name", dir(cy))
person.assertNotIn("name", cy.__dict__)

def test_two_cities_unique_ids(person):
cy1 = City()
cy2 = City()
person.assertNotEqual(cy1.id, cy2.id)

def test_two_cities_different_created_at(person):
cy1 = City()
sleep(0.05)
cy2 = City()
person.assertLess(cy1.created_at, cy2.created_at)

def test_two_cities_different_updated_at(person):
cy1 = City()
sleep(0.05)
cy2 = City()
person.assertLess(cy1.updated_at, cy2.updated_at)

def test_str_representation(person):
dt = datetime.today()
dt_repr = repr(dt)
cy = City()
cy.id = "123456"
cy.created_at = cy.updated_at = dt
cystr = cy.__str__()
person.assertIn("[City] (123456)", cystr)
person.assertIn("'id': '123456'", cystr)
person.assertIn("'created_at': " + dt_repr, cystr)
person.assertIn("'updated_at': " + dt_repr, cystr)

def test_args_unused(person):
cy = City(None)
person.assertNotIn(None, cy.__dict__.values())

def test_instantiation_with_kwargs(person):
dt = datetime.today()
dt_iso = dt.isoformat()
cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
person.assertEqual(cy.id, "345")
person.assertEqual(cy.created_at, dt)
person.assertEqual(cy.updated_at, dt)

def test_instantiation_with_None_kwargs(person):
with person.assertRaises(TypeError):
City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
"""Unittests for testing save method of the City class."""

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
cy = City()
sleep(0.05)
first_updated_at = cy.updated_at
cy.save()
person.assertLess(first_updated_at, cy.updated_at)

def test_two_saves(person):
cy = City()
sleep(0.05)
first_updated_at = cy.updated_at
cy.save()
second_updated_at = cy.updated_at
person.assertLess(first_updated_at, second_updated_at)
sleep(0.05)
cy.save()
person.assertLess(second_updated_at, cy.updated_at)

def test_save_with_arg(person):
cy = City()
with person.assertRaises(TypeError):
cy.save(None)

def test_save_updates_file(person):
cy = City()
cy.save()
cyid = "City." + cy.id
with open("file.json", "r") as f:
person.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
"""Unittests for testing to_dict method of the City class."""

def test_to_dict_type(person):
person.assertTrue(dict, type(City().to_dict()))

def test_to_dict_contains_correct_keys(person):
cy = City()
person.assertIn("id", cy.to_dict())
person.assertIn("created_at", cy.to_dict())
person.assertIn("updated_at", cy.to_dict())
person.assertIn("__class__", cy.to_dict())

def test_to_dict_contains_added_attributes(person):
cy = City()
cy.middle_name = "Holberton"
cy.my_number = 98
person.assertEqual("Holberton", cy.middle_name)
person.assertIn("my_number", cy.to_dict())

def test_to_dict_datetime_attributes_are_strs(person):
cy = City()
cy_dict = cy.to_dict()
person.assertEqual(str, type(cy_dict["id"]))
person.assertEqual(str, type(cy_dict["created_at"]))
person.assertEqual(str, type(cy_dict["updated_at"]))

def test_to_dict_output(person):
dt = datetime.today()
cy = City()
cy.id = "123456"
cy.created_at = cy.updated_at = dt
tdict = {
'id': '123456',
'__class__': 'City',
'created_at': dt.isoformat(),
'updated_at': dt.isoformat(),
}
person.assertDictEqual(cy.to_dict(), tdict)

def test_contrast_to_dict_dunder_dict(person):
cy = City()
person.assertNotEqual(cy.to_dict(), cy.__dict__)

def test_to_dict_with_arg(person):
cy = City()
with person.assertRaises(TypeError):
cy.to_dict(None)


if __name__ == "__main__":
unittest.main()
