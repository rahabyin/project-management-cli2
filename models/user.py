from models.person import Person
from models.project import Project
from utils.validators import validate_email

class User(Person):
    users = []
    id_counter = 1

    def __init__(self, name, email=None, projects=None, user_id=None):
        super().__init__(name)

        self.id = user_id if user_id is not None else User.id_counter
        User.id_counter = max(User.id_counter, self.id + 1)

        self.email = email
        self.projects = projects if projects is not None else []

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
        if isinstance(project, Project):
            self.projects.append(project)
            return project
        # If dict, reconstruct
        if isinstance(project, dict):
            proj = Project.from_dict(project)
            self.projects.append(proj)
            return proj
        raise TypeError("project must be a Project instance or dict")

    def get_project(self, title):
        """Find a project by title."""
        for project in self.projects:
            if project.title.lower() == title.lower():
                return project
        return None

    def introduce(self):
        base = super().introduce()
        if self.email:
            return f"{base} | Contact: {self.email}"
        return base

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects]
        }

    @classmethod
    def from_dict(cls, data):
        projects = [Project.from_dict(proj) for proj in data.get("projects", [])]
        return cls(
            name=data["name"],
            email=data.get("email"),
            projects=projects,
            user_id=data.get("id")
        )

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

    @classmethod
    def find_by_id(cls, user_id):
        for user in cls.users:
            if user.id == user_id:
                return user
        return None
    
