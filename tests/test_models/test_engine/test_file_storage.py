[200~#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
TestFileStorage_instantiation
TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
"""Unittests for testing instantiation of the FileStorage class."""

def test_FileStorage_instantiation_no_args(person):
person.assertEqual(type(FileStorage()), FileStorage)

def test_FileStorage_instantiation_with_arg(person):
with person.assertRaises(TypeError):
FileStorage(None)

def test_FileStorage_file_path_is_private_str(person):
person.assertEqual(str, type(FileStorage._FileStorage__file_path))

def testFileStorage_objects_is_private_dict(person):
person.assertEqual(dict, type(FileStorage._FileStorage__objects))

def test_storage_initializes(person):
person.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
"""Unittests for testing methods of the FileStorage class."""

@classmethod
def setUp(person):
try:
os.rename("file.json", "tmp")
except IOError:
pass

@classmethod
def tearDown(person):
try:
os.remove("file.json")
except IOError:
pass
try:
os.rename("tmp", "file.json")
except IOError:
pass
FileStorage._FileStorage__objects = {}

def test_all(person):
person.assertEqual(dict, type(models.storage.all()))

def test_all_with_arg(person):
with person.assertRaises(TypeError):
models.storage.all(None)

def test_new(person):
bm = BaseModel()
us = User()
st = State()
pl = Place()
cy = City()
am = Amenity()
rv = Review()
models.storage.new(bm)
models.storage.new(us)
models.storage.new(st)
models.storage.new(pl)
models.storage.new(cy)
models.storage.new(am)
models.storage.new(rv)
person.assertIn("BaseModel." + bm.id, models.storage.all().keys())
person.assertIn(bm, models.storage.all().values())
person.assertIn("User." + us.id, models.storage.all().keys())
person.assertIn(us, models.storage.all().values())
person.assertIn("State." + st.id, models.storage.all().keys())
person.assertIn(st, models.storage.all().values())
person.assertIn("Place." + pl.id, models.storage.all().keys())
person.assertIn(pl, models.storage.all().values())
person.assertIn("City." + cy.id, models.storage.all().keys())
person.assertIn(cy, models.storage.all().values())
person.assertIn("Amenity." + am.id, models.storage.all().keys())
person.assertIn(am, models.storage.all().values())
person.assertIn("Review." + rv.id, models.storage.all().keys())
person.assertIn(rv, models.storage.all().values())

def test_new_with_args(person):
with person.assertRaises(TypeError):
models.storage.new(BaseModel(), 1)

def test_save(person):
bm = BaseModel()
us = User()
st = State()
pl = Place()
cy = City()
am = Amenity()
rv = Review()
models.storage.new(bm)
models.storage.new(us)
models.storage.new(st)
models.storage.new(pl)
models.storage.new(cy)
models.storage.new(am)
models.storage.new(rv)
models.storage.save()
save_text = ""
with open("file.json", "r") as f:
save_text = f.read()
person.assertIn("BaseModel." + bm.id, save_text)
person.assertIn("User." + us.id, save_text)
person.assertIn("State." + st.id, save_text)
person.assertIn("Place." + pl.id, save_text)
person.assertIn("City." + cy.id, save_text)
person.assertIn("Amenity." + am.id, save_text)
person.assertIn("Review." + rv.id, save_text)

def test_save_with_arg(person):
with person.assertRaises(TypeError):
models.storage.save(None)

def test_reload(person):
bm = BaseModel()
us = User()
st = State()
pl = Place()
cy = City()
am = Amenity()
rv = Review()
models.storage.new(bm)
models.storage.new(us)
models.storage.new(st)
models.storage.new(pl)
models.storage.new(cy)
models.storage.new(am)
models.storage.new(rv)
models.storage.save()
models.storage.reload()
objs = FileStorage._FileStorage__objects
person.assertIn("BaseModel." + bm.id, objs)
person.assertIn("User." + us.id, objs)
person.assertIn("State." + st.id, objs)
person.assertIn("Place." + pl.id, objs)
person.assertIn("City." + cy.id, objs)
person.assertIn("Amenity." + am.id, objs)
person.assertIn("Review." + rv.id, objs)

def test_reload_with_arg(person):
with person.assertRaises(TypeError):
models.storage.reload(None)


if __name__ == "__main__":
unittest.main()
