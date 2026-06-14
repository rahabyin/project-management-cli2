from models.person import Person
from utils import validate_email


class User(Person):
    users = []
    id_counter = 1

    def __init__(self, name, email=None, projects=None, user_id=None):
        super().__init__(name)

        self.id = user_id if user_id is not None else User.id_counter
        User.id_counter = max(User.id_counter, self.id + 1)

        self.email = email
        self.projects = projects if projects else []

        User.users.append(self)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            self._email = None
            return

        validate_email(value)
        self._email = value

    def add_project(self, project):
        self.projects.append(project)
        return project

    def introduce(self):
        return f"Hi, I am {self.name}"

    @classmethod
    def clear_users(cls):
        cls.users.clear()
        cls.id_counter = 1

    @classmethod
    def get_population(cls):
        return len(cls.users)

    @classmethod
    def find_by_name(cls, name):
        for user in cls.users:
            if user.name.lower() == name.lower():
                return user
        return None