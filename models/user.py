import re

from models.person import Person
from models.project import Project


class User(Person):
    users = []
    id_counter = 1

    def __init__(self, name, email=None, projects=None, user_id=None):
        super().__init__(name, email)

        self.id = user_id if user_id is not None else User.id_counter
        User.id_counter = max(User.id_counter, self.id + 1)

        self.projects = projects if projects else []

        User.users.append(self)

    def add_project(self, project):
     self.projects.append(project)
     return project
    
    def introduce(self):
     return f"Hi, I am {self.name}"

    # REQUIRED BY TESTS
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