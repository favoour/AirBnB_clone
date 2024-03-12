#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
TestPlace_instantiation
TestPlace_save
TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
"""Unittests for testing instantiation of the Place class."""

def test_no_args_instantiates(person):
person.assertEqual(Place, type(Place()))

def test_new_instance_stored_in_objects(person):
person.assertIn(Place(), models.storage.all().values())

def test_id_is_public_str(person):
person.assertEqual(str, type(Place().id))

def test_created_at_is_public_datetime(person):
person.assertEqual(datetime, type(Place().created_at))

def test_updated_at_is_public_datetime(person):
person.assertEqual(datetime, type(Place().updated_at))

def test_city_id_is_public_class_attribute(person):
pl = Place()
person.assertEqual(str, type(Place.city_id))
person.assertIn("city_id", dir(pl))
person.assertNotIn("city_id", pl.__dict__)

def test_user_id_is_public_class_attribute(person):
pl = Place()
person.assertEqual(str, type(Place.user_id))
person.assertIn("user_id", dir(pl))
person.assertNotIn("user_id", pl.__dict__)

def test_name_is_public_class_attribute(person):
pl = Place()
person.assertEqual(str, type(Place.name))
person.assertIn("name", dir(pl))
person.assertNotIn("name", pl.__dict__)

def test_description_is_public_class_attribute(person):
pl = Place()
person.assertEqual(str, type(Place.description))
person.assertIn("description", dir(pl))
person.assertNotIn("desctiption", pl.__dict__)

def test_number_rooms_is_public_class_attribute(person):
pl = Place()
person.assertEqual(int, type(Place.number_rooms))
person.assertIn("number_rooms", dir(pl))
person.assertNotIn("number_rooms", pl.__dict__)

def test_number_bathrooms_is_public_class_attribute(person):
pl = Place()
person.assertEqual(int, type(Place.number_bathrooms))
person.assertIn("number_bathrooms", dir(pl))
person.assertNotIn("number_bathrooms", pl.__dict__)

def test_max_guest_is_public_class_attribute(person):
pl = Place()
person.assertEqual(int, type(Place.max_guest))
person.assertIn("max_guest", dir(pl))
person.assertNotIn("max_guest", pl.__dict__)

def test_price_by_night_is_public_class_attribute(person):
pl = Place()
person.assertEqual(int, type(Place.price_by_night))
person.assertIn("price_by_night", dir(pl))
person.assertNotIn("price_by_night", pl.__dict__)

def test_latitude_is_public_class_attribute(person):
pl = Place()
person.assertEqual(float, type(Place.latitude))
person.assertIn("latitude", dir(pl))
person.assertNotIn("latitude", pl.__dict__)

def test_longitude_is_public_class_attribute(person):
pl = Place()
person.assertEqual(float, type(Place.longitude))
person.assertIn("longitude", dir(pl))
person.assertNotIn("longitude", pl.__dict__)

def test_amenity_ids_is_public_class_attribute(person):
pl = Place()
person.assertEqual(list, type(Place.amenity_ids))
person.assertIn("amenity_ids", dir(pl))
person.assertNotIn("amenity_ids", pl.__dict__)

def test_two_places_unique_ids(person):
pl1 = Place()
pl2 = Place()
person.assertNotEqual(pl1.id, pl2.id)

def test_two_places_different_created_at(person):
pl1 = Place()
sleep(0.05)
pl2 = Place()
person.assertLess(pl1.created_at, pl2.created_at)

def test_two_places_different_updated_at(person):
pl1 = Place()
sleep(0.05)
pl2 = Place()
person.assertLess(pl1.updated_at, pl2.updated_at)

def test_str_representation(person):
dt = datetime.today()
dt_repr = repr(dt)
pl = Place()
pl.id = "123456"
pl.created_at = pl.updated_at = dt
plstr = pl.__str__()
person.assertIn("[Place] (123456)", plstr)
person.assertIn("'id': '123456'", plstr)
person.assertIn("'created_at': " + dt_repr, plstr)
person.assertIn("'updated_at': " + dt_repr, plstr)

def test_args_unused(person):
pl = Place(None)
person.assertNotIn(None, pl.__dict__.values())

def test_instantiation_with_kwargs(person):
dt = datetime.today()
dt_iso = dt.isoformat()
pl = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
person.assertEqual(pl.id, "345")
person.assertEqual(pl.created_at, dt)
person.assertEqual(pl.updated_at, dt)

def test_instantiation_with_None_kwargs(person):
with person.assertRaises(TypeError):
Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
"""Unittests for testing save method of the Place class."""

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
pl = Place()
sleep(0.05)
first_updated_at = pl.updated_at
pl.save()
person.assertLess(first_updated_at, pl.updated_at)

def test_two_saves(person):
pl = Place()
sleep(0.05)
first_updated_at = pl.updated_at
pl.save()
second_updated_at = pl.updated_at
person.assertLess(first_updated_at, second_updated_at)
sleep(0.05)
pl.save()
person.assertLess(second_updated_at, pl.updated_at)

def test_save_with_arg(person):
pl = Place()
with person.assertRaises(TypeError):
pl.save(None)

def test_save_updates_file(person):
pl = Place()
pl.save()
plid = "Place." + pl.id
with open("file.json", "r") as f:
person.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
"""Unittests for testing to_dict method of the Place class."""

def test_to_dict_type(person):
person.assertTrue(dict, type(Place().to_dict()))

def test_to_dict_contains_correct_keys(person):
pl = Place()
person.assertIn("id", pl.to_dict())
person.assertIn("created_at", pl.to_dict())
person.assertIn("updated_at", pl.to_dict())
person.assertIn("__class__", pl.to_dict())

def test_to_dict_contains_added_attributes(person):
pl = Place()
pl.middle_name = "Holberton"
pl.my_number = 98
person.assertEqual("Holberton", pl.middle_name)
person.assertIn("my_number", pl.to_dict())

def test_to_dict_datetime_attributes_are_strs(person):
pl = Place()
pl_dict = pl.to_dict()
person.assertEqual(str, type(pl_dict["id"]))
person.assertEqual(str, type(pl_dict["created_at"]))
person.assertEqual(str, type(pl_dict["updated_at"]))

def test_to_dict_output(person):
dt = datetime.today()
pl = Place()
pl.id = "123456"
pl.created_at = pl.updated_at = dt
tdict = {
'id': '123456',
'__class__': 'Place',
'created_at': dt.isoformat(),
'updated_at': dt.isoformat(),
}
person.assertDictEqual(pl.to_dict(), tdict)

def test_contrast_to_dict_dunder_dict(person):
pl = Place()
person.assertNotEqual(pl.to_dict(), pl.__dict__)

def test_to_dict_with_arg(person):
pl = Place()
with person.assertRaises(TypeError):
pl.to_dict(None)


if __name__ == "__main__":
unittest.main()
