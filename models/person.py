from utils.validators import validate_not_empty

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

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data.get("email")
        )
    
print("Utils and Person written.")