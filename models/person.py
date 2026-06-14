from utils import validate_not_empty


class Person:
    def __init__(self, name, email=None):
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        validate_not_empty(value, "name")
        self._name = value

    def introduce(self):
        return f"Hi, I am {self.name}"