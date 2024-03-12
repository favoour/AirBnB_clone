#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
TestHBNBCommand_prompting
TestHBNBCommand_help
TestHBNBCommand_exit
TestHBNBCommand_create
TestHBNBCommand_show
TestHBNBCommand_all
TestHBNBCommand_destroy
TestHBNBCommand_update
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompting(unittest.TestCase):
"""Unittests for testing prompting of the HBNB command interpreter."""

def test_prompt_string(person):
person.assertEqual("(hbnb) ", HBNBCommand.prompt)

def test_empty_line(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(""))
person.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
"""Unittests for testing help messages of the HBNB command interpreter."""

def test_help_quit(person):
h = "Quit command to exit the program."
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help quit"))
person.assertEqual(h, output.getvalue().strip())

def test_help_create(person):
h = ("Usage: create <class>\n        "
    "Create a new class instance and print its id.")
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help create"))
person.assertEqual(h, output.getvalue().strip())

def test_help_EOF(person):
h = "EOF signal to exit the program."
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help EOF"))
person.assertEqual(h, output.getvalue().strip())

def test_help_show(person):
h = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
    "Display the string representation of a class instance of"
    " a given id.")
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help show"))
person.assertEqual(h, output.getvalue().strip())

def test_help_destroy(person):
h = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
    "Delete a class instance of a given id.")
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help destroy"))
person.assertEqual(h, output.getvalue().strip())

def test_help_all(person):
h = ("Usage: all or all <class> or <class>.all()\n        "
    "Display string representations of all instances of a given class"
    ".\n        If no class is specified, displays all instantiated "
    "objects.")
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help all"))
person.assertEqual(h, output.getvalue().strip())

def test_help_count(person):
h = ("Usage: count <class> or <class>.count()\n        "
    "Retrieve the number of instances of a given class.")
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help count"))
person.assertEqual(h, output.getvalue().strip())

def test_help_update(person):
h = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
    "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
    ">) or\n       <class>.update(<id>, <dictionary>)\n        "
    "Update a class instance of a given id by adding or updating\n   "
    "     a given attribute key/value pair or dictionary.")
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help update"))
person.assertEqual(h, output.getvalue().strip())

def test_help(person):
h = ("Documented commands (type help <topic>):\n"
    "========================================\n"
    "EOF  all  count  create  destroy  help  quit  show  update")
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("help"))
person.assertEqual(h, output.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
"""Unittests for testing exiting from the HBNB command interpreter."""

def test_quit_exits(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertTrue(HBNBCommand().onecmd("quit"))

def test_EOF_exits(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
"""Unittests for testing create from the HBNB command interpreter."""

@classmethod
def setUp(person):
try:
os.rename("file.json", "tmp")
except IOError:
pass
FileStorage.__objects = {}

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

def test_create_missing_class(person):
correct = "** class name missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create"))
person.assertEqual(correct, output.getvalue().strip())

def test_create_invalid_class(person):
correct = "** class doesn't exist **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create MyModel"))
person.assertEqual(correct, output.getvalue().strip())

def test_create_invalid_syntax(person):
correct = "*** Unknown syntax: MyModel.create()"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
person.assertEqual(correct, output.getvalue().strip())
correct = "*** Unknown syntax: BaseModel.create()"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
person.assertEqual(correct, output.getvalue().strip())

def test_create_object(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
person.assertLess(0, len(output.getvalue().strip()))
testKey = "BaseModel.{}".format(output.getvalue().strip())
person.assertIn(testKey, storage.all().keys())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create User"))
person.assertLess(0, len(output.getvalue().strip()))
testKey = "User.{}".format(output.getvalue().strip())
person.assertIn(testKey, storage.all().keys())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create State"))
person.assertLess(0, len(output.getvalue().strip()))
testKey = "State.{}".format(output.getvalue().strip())
person.assertIn(testKey, storage.all().keys())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create City"))
person.assertLess(0, len(output.getvalue().strip()))
testKey = "City.{}".format(output.getvalue().strip())
person.assertIn(testKey, storage.all().keys())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
person.assertLess(0, len(output.getvalue().strip()))
testKey = "Amenity.{}".format(output.getvalue().strip())
person.assertIn(testKey, storage.all().keys())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Place"))
person.assertLess(0, len(output.getvalue().strip()))
testKey = "Place.{}".format(output.getvalue().strip())
person.assertIn(testKey, storage.all().keys())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Review"))
person.assertLess(0, len(output.getvalue().strip()))
testKey = "Review.{}".format(output.getvalue().strip())
person.assertIn(testKey, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
"""Unittests for testing show from the HBNB command interpreter"""

@classmethod
def setUp(person):
try:
os.rename("file.json", "tmp")
except IOError:
pass
FileStorage.__objects = {}

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

def test_show_missing_class(person):
correct = "** class name missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(".show()"))
person.assertEqual(correct, output.getvalue().strip())

def test_show_invalid_class(person):
correct = "** class doesn't exist **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show MyModel"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
person.assertEqual(correct, output.getvalue().strip())

def test_show_missing_id_space_notation(person):
correct = "** instance id missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show BaseModel"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show User"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show State"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show City"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show Amenity"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show Place"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show Review"))
person.assertEqual(correct, output.getvalue().strip())

def test_show_missing_id_dot_notation(person):
correct = "** instance id missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("User.show()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("State.show()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("City.show()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Place.show()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Review.show()"))
person.assertEqual(correct, output.getvalue().strip())

def test_show_no_instance_found_space_notation(person):
correct = "** no instance found **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show User 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show State 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show City 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show Place 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("show Review 1"))
person.assertEqual(correct, output.getvalue().strip())

def test_show_no_instance_found_dot_notation(person):
correct = "** no instance found **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("User.show(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("State.show(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("City.show(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
person.assertEqual(correct, output.getvalue().strip())

def test_show_objects_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["BaseModel.{}".format(testID)]
command = "show BaseModel {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create User"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["User.{}".format(testID)]
command = "show User {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create State"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["State.{}".format(testID)]
command = "show State {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Place"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Place.{}".format(testID)]
command = "show Place {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create City"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["City.{}".format(testID)]
command = "show City {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Amenity.{}".format(testID)]
command = "show Amenity {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Review"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Review.{}".format(testID)]
command = "show Review {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())

def test_show_objects_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["BaseModel.{}".format(testID)]
command = "BaseModel.show({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create User"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["User.{}".format(testID)]
command = "User.show({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create State"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["State.{}".format(testID)]
command = "State.show({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Place"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Place.{}".format(testID)]
command = "Place.show({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create City"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["City.{}".format(testID)]
command = "City.show({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Amenity.{}".format(testID)]
command = "Amenity.show({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Review"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Review.{}".format(testID)]
command = "Review.show({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
"""Unittests for testing destroy from the HBNB command interpreter."""

@classmethod
def setUp(person):
try:
os.rename("file.json", "tmp")
except IOError:
pass
FileStorage.__objects = {}

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
storage.reload()

def test_destroy_missing_class(person):
correct = "** class name missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(".destroy()"))
person.assertEqual(correct, output.getvalue().strip())

def test_destroy_invalid_class(person):
correct = "** class doesn't exist **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
person.assertEqual(correct, output.getvalue().strip())

def test_destroy_id_missing_space_notation(person):
correct = "** instance id missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy User"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy State"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy City"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy Place"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy Review"))
person.assertEqual(correct, output.getvalue().strip())

def test_destroy_id_missing_dot_notation(person):
correct = "** instance id missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("User.destroy()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("State.destroy()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("City.destroy()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
person.assertEqual(correct, output.getvalue().strip())

def test_destroy_invalid_id_space_notation(person):
correct = "** no instance found **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy User 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy State 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy City 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
person.assertEqual(correct, output.getvalue().strip())

def test_destroy_invalid_id_dot_notation(person):
correct = "** no instance found **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
person.assertEqual(correct, output.getvalue().strip())

def test_destroy_objects_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["BaseModel.{}".format(testID)]
command = "destroy BaseModel {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create User"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["User.{}".format(testID)]
command = "show User {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create State"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["State.{}".format(testID)]
command = "show State {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Place"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Place.{}".format(testID)]
command = "show Place {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create City"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["City.{}".format(testID)]
command = "show City {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Amenity.{}".format(testID)]
command = "show Amenity {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Review"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Review.{}".format(testID)]
command = "show Review {}".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())

def test_destroy_objects_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["BaseModel.{}".format(testID)]
command = "BaseModel.destroy({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create User"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["User.{}".format(testID)]
command = "User.destroy({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create State"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["State.{}".format(testID)]
command = "State.destroy({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Place"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Place.{}".format(testID)]
command = "Place.destroy({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create City"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["City.{}".format(testID)]
command = "City.destroy({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Amenity.{}".format(testID)]
command = "Amenity.destroy({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Review"))
testID = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
obj = storage.all()["Review.{}".format(testID)]
command = "Review.destory({})".format(testID)
person.assertFalse(HBNBCommand().onecmd(command))
person.assertNotIn(obj, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
"""Unittests for testing all of the HBNB command interpreter."""

@classmethod
def setUp(person):
try:
os.rename("file.json", "tmp")
except IOError:
pass
FileStorage.__objects = {}

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

def test_all_invalid_class(person):
correct = "** class doesn't exist **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all MyModel"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
person.assertEqual(correct, output.getvalue().strip())

def test_all_objects_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
person.assertFalse(HBNBCommand().onecmd("create User"))
person.assertFalse(HBNBCommand().onecmd("create State"))
person.assertFalse(HBNBCommand().onecmd("create Place"))
person.assertFalse(HBNBCommand().onecmd("create City"))
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
person.assertFalse(HBNBCommand().onecmd("create Review"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all"))
person.assertIn("BaseModel", output.getvalue().strip())
person.assertIn("User", output.getvalue().strip())
person.assertIn("State", output.getvalue().strip())
person.assertIn("Place", output.getvalue().strip())
person.assertIn("City", output.getvalue().strip())
person.assertIn("Amenity", output.getvalue().strip())
person.assertIn("Review", output.getvalue().strip())

def test_all_objects_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
person.assertFalse(HBNBCommand().onecmd("create User"))
person.assertFalse(HBNBCommand().onecmd("create State"))
person.assertFalse(HBNBCommand().onecmd("create Place"))
person.assertFalse(HBNBCommand().onecmd("create City"))
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
person.assertFalse(HBNBCommand().onecmd("create Review"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(".all()"))
person.assertIn("BaseModel", output.getvalue().strip())
person.assertIn("User", output.getvalue().strip())
person.assertIn("State", output.getvalue().strip())
person.assertIn("Place", output.getvalue().strip())
person.assertIn("City", output.getvalue().strip())
person.assertIn("Amenity", output.getvalue().strip())
person.assertIn("Review", output.getvalue().strip())

def test_all_single_object_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
person.assertFalse(HBNBCommand().onecmd("create User"))
person.assertFalse(HBNBCommand().onecmd("create State"))
person.assertFalse(HBNBCommand().onecmd("create Place"))
person.assertFalse(HBNBCommand().onecmd("create City"))
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
person.assertFalse(HBNBCommand().onecmd("create Review"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all BaseModel"))
person.assertIn("BaseModel", output.getvalue().strip())
person.assertNotIn("User", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all User"))
person.assertIn("User", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all State"))
person.assertIn("State", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all City"))
person.assertIn("City", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all Amenity"))
person.assertIn("Amenity", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all Place"))
person.assertIn("Place", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("all Review"))
person.assertIn("Review", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())

def test_all_single_object_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
person.assertFalse(HBNBCommand().onecmd("create User"))
person.assertFalse(HBNBCommand().onecmd("create State"))
person.assertFalse(HBNBCommand().onecmd("create Place"))
person.assertFalse(HBNBCommand().onecmd("create City"))
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
person.assertFalse(HBNBCommand().onecmd("create Review"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
person.assertIn("BaseModel", output.getvalue().strip())
person.assertNotIn("User", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("User.all()"))
person.assertIn("User", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("State.all()"))
person.assertIn("State", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("City.all()"))
person.assertIn("City", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
person.assertIn("Amenity", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Place.all()"))
person.assertIn("Place", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Review.all()"))
person.assertIn("Review", output.getvalue().strip())
person.assertNotIn("BaseModel", output.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
"""Unittests for testing update from the HBNB command interpreter."""

@classmethod
def setUp(person):
try:
os.rename("file.json", "tmp")
except IOError:
pass
FileStorage.__objects = {}

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

def test_update_missing_class(person):
correct = "** class name missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(".update()"))
person.assertEqual(correct, output.getvalue().strip())

def test_update_invalid_class(person):
correct = "** class doesn't exist **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update MyModel"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
person.assertEqual(correct, output.getvalue().strip())

def test_update_missing_id_space_notation(person):
correct = "** instance id missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update BaseModel"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update User"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update State"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update City"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update Amenity"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update Place"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update Review"))
person.assertEqual(correct, output.getvalue().strip())

def test_update_missing_id_dot_notation(person):
correct = "** instance id missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("User.update()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("State.update()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("City.update()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Place.update()"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Review.update()"))
person.assertEqual(correct, output.getvalue().strip())

def test_update_invalid_id_space_notation(person):
correct = "** no instance found **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update User 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update State 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update City 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update Place 1"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("update Review 1"))
person.assertEqual(correct, output.getvalue().strip())

def test_update_invalid_id_dot_notation(person):
correct = "** no instance found **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("User.update(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("State.update(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("City.update(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
person.assertEqual(correct, output.getvalue().strip())

def test_update_missing_attr_name_space_notation(person):
correct = "** attribute name missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
testId = output.getvalue().strip()
testCmd = "update BaseModel {}".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create User"))
testId = output.getvalue().strip()
testCmd = "update User {}".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create State"))
testId = output.getvalue().strip()
testCmd = "update State {}".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create City"))
testId = output.getvalue().strip()
testCmd = "update City {}".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
testId = output.getvalue().strip()
testCmd = "update Amenity {}".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Place"))
testId = output.getvalue().strip()
testCmd = "update Place {}".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())

def test_update_missing_attr_name_dot_notation(person):
correct = "** attribute name missing **"
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
testId = output.getvalue().strip()
testCmd = "BaseModel.update({})".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create User"))
testId = output.getvalue().strip()
testCmd = "User.update({})".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create State"))
testId = output.getvalue().strip()
testCmd = "State.update({})".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create City"))
testId = output.getvalue().strip()
testCmd = "City.update({})".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
testId = output.getvalue().strip()
testCmd = "Amenity.update({})".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Place"))
testId = output.getvalue().strip()
testCmd = "Place.update({})".format(testId)
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())

def test_update_missing_attr_value_space_notation(person):
correct = "** value missing **"
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create BaseModel")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "update BaseModel {} attr_name".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create User")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "update User {} attr_name".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create State")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "update State {} attr_name".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create City")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "update City {} attr_name".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Amenity")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "update Amenity {} attr_name".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "update Place {} attr_name".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Review")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "update Review {} attr_name".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())

def test_update_missing_attr_value_dot_notation(person):
correct = "** value missing **"
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create BaseModel")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "BaseModel.update({}, attr_name)".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create User")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "User.update({}, attr_name)".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create State")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "State.update({}, attr_name)".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create City")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "City.update({}, attr_name)".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Amenity")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "Amenity.update({}, attr_name)".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "Place.update({}, attr_name)".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Review")
testId = output.getvalue().strip()
with patch("sys.stdout", new=StringIO()) as output:
testCmd = "Review.update({}, attr_name)".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
person.assertEqual(correct, output.getvalue().strip())

def test_update_valid_string_attr_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create BaseModel")
testId = output.getvalue().strip()
testCmd = "update BaseModel {} attr_name 'attr_value'".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create User")
testId = output.getvalue().strip()
testCmd = "update User {} attr_name 'attr_value'".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["User.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create State")
testId = output.getvalue().strip()
testCmd = "update State {} attr_name 'attr_value'".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["State.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create City")
testId = output.getvalue().strip()
testCmd = "update City {} attr_name 'attr_value'".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["City.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "update Place {} attr_name 'attr_value'".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Amenity")
testId = output.getvalue().strip()
testCmd = "update Amenity {} attr_name 'attr_value'".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Review")
testId = output.getvalue().strip()
testCmd = "update Review {} attr_name 'attr_value'".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Review.{}".format(testId)].__dict__
person.assertTrue("attr_value", test_dict["attr_name"])

def test_update_valid_string_attr_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create BaseModel")
tId = output.getvalue().strip()
testCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create User")
tId = output.getvalue().strip()
testCmd = "User.update({}, attr_name, 'attr_value')".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["User.{}".format(tId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create State")
tId = output.getvalue().strip()
testCmd = "State.update({}, attr_name, 'attr_value')".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["State.{}".format(tId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create City")
tId = output.getvalue().strip()
testCmd = "City.update({}, attr_name, 'attr_value')".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["City.{}".format(tId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
tId = output.getvalue().strip()
testCmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Place.{}".format(tId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Amenity")
tId = output.getvalue().strip()
testCmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Review")
tId = output.getvalue().strip()
testCmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Review.{}".format(tId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

def test_update_valid_int_attr_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "update Place {} max_guest 98".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual(98, test_dict["max_guest"])

def test_update_valid_int_attr_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
tId = output.getvalue().strip()
testCmd = "Place.update({}, max_guest, 98)".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Place.{}".format(tId)].__dict__
person.assertEqual(98, test_dict["max_guest"])

def test_update_valid_float_attr_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "update Place {} latitude 7.2".format(testId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual(7.2, test_dict["latitude"])

def test_update_valid_float_attr_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
tId = output.getvalue().strip()
testCmd = "Place.update({}, latitude, 7.2)".format(tId)
person.assertFalse(HBNBCommand().onecmd(testCmd))
test_dict = storage.all()["Place.{}".format(tId)].__dict__
person.assertEqual(7.2, test_dict["latitude"])

def test_update_valid_dictionary_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create BaseModel")
testId = output.getvalue().strip()
testCmd = "update BaseModel {} ".format(testId)
testCmd += "{'attr_name': 'attr_value'}"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create User")
testId = output.getvalue().strip()
testCmd = "update User {} ".format(testId)
testCmd += "{'attr_name': 'attr_value'}"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["User.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create State")
testId = output.getvalue().strip()
testCmd = "update State {} ".format(testId)
testCmd += "{'attr_name': 'attr_value'}"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["State.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create City")
testId = output.getvalue().strip()
testCmd = "update City {} ".format(testId)
testCmd += "{'attr_name': 'attr_value'}"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["City.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "update Place {} ".format(testId)
testCmd += "{'attr_name': 'attr_value'}"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Amenity")
testId = output.getvalue().strip()
testCmd = "update Amenity {} ".format(testId)
testCmd += "{'attr_name': 'attr_value'}"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Review")
testId = output.getvalue().strip()
testCmd = "update Review {} ".format(testId)
testCmd += "{'attr_name': 'attr_value'}"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Review.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

def test_update_valid_dictionary_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create BaseModel")
testId = output.getvalue().strip()
testCmd = "BaseModel.update({}".format(testId)
testCmd += "{'attr_name': 'attr_value'})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create User")
testId = output.getvalue().strip()
testCmd = "User.update({}, ".format(testId)
testCmd += "{'attr_name': 'attr_value'})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["User.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create State")
testId = output.getvalue().strip()
testCmd = "State.update({}, ".format(testId)
testCmd += "{'attr_name': 'attr_value'})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["State.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create City")
testId = output.getvalue().strip()
testCmd = "City.update({}, ".format(testId)
testCmd += "{'attr_name': 'attr_value'})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["City.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "Place.update({}, ".format(testId)
testCmd += "{'attr_name': 'attr_value'})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Amenity")
testId = output.getvalue().strip()
testCmd = "Amenity.update({}, ".format(testId)
testCmd += "{'attr_name': 'attr_value'})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Review")
testId = output.getvalue().strip()
testCmd = "Review.update({}, ".format(testId)
testCmd += "{'attr_name': 'attr_value'})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Review.{}".format(testId)].__dict__
person.assertEqual("attr_value", test_dict["attr_name"])

def test_update_valid_dictionary_with_int_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "update Place {} ".format(testId)
testCmd += "{'max_guest': 98})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual(98, test_dict["max_guest"])

def test_update_valid_dictionary_with_int_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "Place.update({}, ".format(testId)
testCmd += "{'max_guest': 98})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual(98, test_dict["max_guest"])

def test_update_valid_dictionary_with_float_space_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "update Place {} ".format(testId)
testCmd += "{'latitude': 9.8})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual(9.8, test_dict["latitude"])

def test_update_valid_dictionary_with_float_dot_notation(person):
with patch("sys.stdout", new=StringIO()) as output:
HBNBCommand().onecmd("create Place")
testId = output.getvalue().strip()
testCmd = "Place.update({}, ".format(testId)
testCmd += "{'latitude': 9.8})"
HBNBCommand().onecmd(testCmd)
test_dict = storage.all()["Place.{}".format(testId)].__dict__
person.assertEqual(9.8, test_dict["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
"""Unittests for testing count method of HBNB comand interpreter."""

@classmethod
def setUp(person):
try:
os.rename("file.json", "tmp")
except IOError:
pass
FileStorage._FileStorage__objects = {}

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

def test_count_invalid_class(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
person.assertEqual("0", output.getvalue().strip())

def test_count_object(person):
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create BaseModel"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
person.assertEqual("1", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create User"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("User.count()"))
person.assertEqual("1", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create State"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("State.count()"))
person.assertEqual("1", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Place"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Place.count()"))
person.assertEqual("1", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create City"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("City.count()"))
person.assertEqual("1", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Amenity"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
person.assertEqual("1", output.getvalue().strip())
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("create Review"))
with patch("sys.stdout", new=StringIO()) as output:
person.assertFalse(HBNBCommand().onecmd("Review.count()"))
person.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
unittest.main()
