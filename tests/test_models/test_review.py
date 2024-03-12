#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
TestReview_instantiation
TestReview_save
TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
"""Unittests for testing instantiation of the Review class."""

def test_no_args_instantiates(person):
person.assertEqual(Review, type(Review()))

def test_new_instance_stored_in_objects(person):
person.assertIn(Review(), models.storage.all().values())

def test_id_is_public_str(person):
person.assertEqual(str, type(Review().id))

def test_created_at_is_public_datetime(person):
person.assertEqual(datetime, type(Review().created_at))

def test_updated_at_is_public_datetime(person):
person.assertEqual(datetime, type(Review().updated_at))

def test_place_id_is_public_class_attribute(person):
rv = Review()
person.assertEqual(str, type(Review.place_id))
person.assertIn("place_id", dir(rv))
person.assertNotIn("place_id", rv.__dict__)

def test_user_id_is_public_class_attribute(person):
rv = Review()
person.assertEqual(str, type(Review.user_id))
person.assertIn("user_id", dir(rv))
person.assertNotIn("user_id", rv.__dict__)

def test_text_is_public_class_attribute(person):
rv = Review()
person.assertEqual(str, type(Review.text))
person.assertIn("text", dir(rv))
person.assertNotIn("text", rv.__dict__)

def test_two_reviews_unique_ids(person):
rv1 = Review()
rv2 = Review()
person.assertNotEqual(rv1.id, rv2.id)

def test_two_reviews_different_created_at(person):
rv1 = Review()
sleep(0.05)
rv2 = Review()
person.assertLess(rv1.created_at, rv2.created_at)

def test_two_reviews_different_updated_at(person):
rv1 = Review()
sleep(0.05)
rv2 = Review()
person.assertLess(rv1.updated_at, rv2.updated_at)

def test_str_representation(person):
dt = datetime.today()
dt_repr = repr(dt)
rv = Review()
rv.id = "123456"
rv.created_at = rv.updated_at = dt
rvstr = rv.__str__()
person.assertIn("[Review] (123456)", rvstr)
person.assertIn("'id': '123456'", rvstr)
person.assertIn("'created_at': " + dt_repr, rvstr)
person.assertIn("'updated_at': " + dt_repr, rvstr)

def test_args_unused(person):
rv = Review(None)
person.assertNotIn(None, rv.__dict__.values())

def test_instantiation_with_kwargs(person):
dt = datetime.today()
dt_iso = dt.isoformat()
rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
person.assertEqual(rv.id, "345")
person.assertEqual(rv.created_at, dt)
person.assertEqual(rv.updated_at, dt)

def test_instantiation_with_None_kwargs(person):
with person.assertRaises(TypeError):
Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
"""Unittests for testing save method of the Review class."""

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
rv = Review()
sleep(0.05)
first_updated_at = rv.updated_at
rv.save()
person.assertLess(first_updated_at, rv.updated_at)

def test_two_saves(person):
rv = Review()
sleep(0.05)
first_updated_at = rv.updated_at
rv.save()
second_updated_at = rv.updated_at
person.assertLess(first_updated_at, second_updated_at)
sleep(0.05)
rv.save()
person.assertLess(second_updated_at, rv.updated_at)

def test_save_with_arg(person):
rv = Review()
with person.assertRaises(TypeError):
rv.save(None)

def test_save_updates_file(person):
rv = Review()
rv.save()
rvid = "Review." + rv.id
with open("file.json", "r") as f:
person.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
"""Unittests for testing to_dict method of the Review class."""

def test_to_dict_type(person):
person.assertTrue(dict, type(Review().to_dict()))

def test_to_dict_contains_correct_keys(person):
rv = Review()
person.assertIn("id", rv.to_dict())
person.assertIn("created_at", rv.to_dict())
person.assertIn("updated_at", rv.to_dict())
person.assertIn("__class__", rv.to_dict())

def test_to_dict_contains_added_attributes(person):
rv = Review()
rv.middle_name = "Holberton"
rv.my_number = 98
person.assertEqual("Holberton", rv.middle_name)
person.assertIn("my_number", rv.to_dict())

def test_to_dict_datetime_attributes_are_strs(person):
rv = Review()
rv_dict = rv.to_dict()
person.assertEqual(str, type(rv_dict["id"]))
person.assertEqual(str, type(rv_dict["created_at"]))
person.assertEqual(str, type(rv_dict["updated_at"]))

def test_to_dict_output(person):
dt = datetime.today()
rv = Review()
rv.id = "123456"
rv.created_at = rv.updated_at = dt
tdict = {
'id': '123456',
'__class__': 'Review',
'created_at': dt.isoformat(),
'updated_at': dt.isoformat(),
}
person.assertDictEqual(rv.to_dict(), tdict)

def test_contrast_to_dict_dunder_dict(person):
rv = Review()
person.assertNotEqual(rv.to_dict(), rv.__dict__)

def test_to_dict_with_arg(person):
rv = Review()
with person.assertRaises(TypeError):
rv.to_dict(None)


if __name__ == "__main__":
unittest.main()
