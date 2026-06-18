import pytest
from models.user import User
from models.project import Project
from models.task import Task


class TestUser:
    def setup_method(self):
        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()

    def test_user_creation(self):
        user = User(name="Alice", email="alice@example.com")
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.id == 1

    def test_user_email_validation(self):
        with pytest.raises(ValueError):
            User(name="Bob", email="not-an-email")

    def test_user_add_project(self):
        user = User(name="Alice")
        proj = Project(title="Website")
        user.add_project(proj)
        assert len(user.projects) == 1
        assert user.projects[0].title == "Website"

    def test_user_find_by_name(self):
        User(name="Alice")
        User(name="Bob")
        found = User.find_by_name("alice")
        assert found is not None
        assert found.name == "Alice"

    def test_user_to_dict(self):
        user = User(name="Alice", email="alice@example.com")
        d = user.to_dict()
        assert d["name"] == "Alice"
        assert d["email"] == "alice@example.com"
        assert "id" in d
        assert "projects" in d

    def test_user_from_dict(self):
        data = {
            "id": 5,
            "name": "Alice",
            "email": "alice@example.com",
            "projects": []
        }
        user = User.from_dict(data)
        assert user.id == 5
        assert user.name == "Alice"

    def test_user_name_cannot_be_empty(self):
        with pytest.raises(ValueError):
            User(name="")

    def test_user_introduce(self):
        user = User(name="Alice", email="alice@example.com")
        intro = user.introduce()
        assert "Alice" in intro
        assert "alice@example.com" in intro


class TestProject:
    def setup_method(self):
        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()

    def test_project_creation(self):
        proj = Project(title="Website", description="Company site", due_date="2025-12-01")
        assert proj.title == "Website"
        assert proj.description == "Company site"
        assert proj.due_date == "2025-12-01"
        assert proj.id == 1

    def test_project_add_task(self):
        proj = Project(title="Website")
        task = proj.add_task("Design homepage")
        assert len(proj.tasks) == 1
        assert isinstance(task, Task)
        assert task.title == "Design homepage"

    def test_project_add_task_object(self):
        proj = Project(title="Website")
        task = Task(title="Code backend")
        returned = proj.add_task(task)
        assert returned == task
        assert task in proj.tasks

    def test_project_complete_task(self):
        proj = Project(title="Website")
        task = Task(title="Design", task_id=10)
        proj.add_task(task)
        result = proj.complete_task(10)
        assert result is not None
        assert result.is_completed()

    def test_project_title_cannot_be_empty(self):
        with pytest.raises(ValueError):
            Project(title="")

    def test_project_to_dict(self):
        proj = Project(title="Website")
        proj.add_task("Task 1")
        d = proj.to_dict()
        assert d["title"] == "Website"
        assert len(d["tasks"]) == 1

    def test_project_from_dict(self):
        data = {
            "id": 3,
            "title": "Website",
            "description": "Desc",
            "due_date": "2025-01-01",
            "tasks": [
                {"id": 1, "title": "T1", "assigned_to": None, "status": "pending"}
            ]
        }
        proj = Project.from_dict(data)
        assert proj.id == 3
        assert proj.title == "Website"
        assert len(proj.tasks) == 1

    def test_project_find_by_title(self):
        Project(title="Website")
        Project(title="App")
        found = Project.find_by_title("app")
        assert found is not None
        assert found.title == "App"


class TestTask:
    def setup_method(self):
        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()

    def test_task_creation(self):
        task = Task(title="Design", assigned_to="Alice")
        assert task.title == "Design"
        assert task.assigned_to == "Alice"
        assert task.status == "pending"

    def test_task_mark_complete(self):
        task = Task(title="Design")
        task.mark_complete()
        assert task.is_completed()
        assert task.status == "completed"

    def test_task_mark_pending(self):
        task = Task(title="Design")
        task.mark_complete()
        task.mark_pending()
        assert not task.is_completed()

    def test_task_invalid_status(self):
        task = Task(title="Design")
        with pytest.raises(ValueError):
            task.status = "invalid"

    def test_task_title_cannot_be_empty(self):
        with pytest.raises(ValueError):
            Task(title="")

    def test_task_to_dict(self):
        task = Task(title="Design", assigned_to="Alice", status="completed", task_id=7)
        d = task.to_dict()
        assert d["title"] == "Design"
        assert d["assigned_to"] == "Alice"
        assert d["status"] == "completed"
        assert d["id"] == 7

    def test_task_from_dict(self):
        data = {"id": 2, "title": "Code", "assigned_to": "Bob", "status": "pending"}
        task = Task.from_dict(data)
        assert task.id == 2
        assert task.title == "Code"
        assert task.assigned_to == "Bob"

