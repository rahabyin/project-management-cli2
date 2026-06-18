'''import os
import json
import pytest

from models.user import User
from models.project import Project
from models.task import Task
from storage import (
    load_all,
    save_all,
    find_user,
    find_project,
    find_task,
    ensure_data_folder,
    DATA_FILE
)


class TestStorage:
    def setup_method(self):
        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()
        # Clean test data file
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def teardown_method(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_save_and_load_users(self):
        user = User(name="Alice", email="alice@example.com")
        proj = Project(title="Website")
        user.add_project(proj)
        task = Task(title="Design")
        proj.add_task(task)

        assert save_all(User.users) is True
        # Clear and reload
        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()

        users = load_all()
        assert len(users) == 1
        assert users[0].name == "Alice"
        assert len(users[0].projects) == 1
        assert len(users[0].projects[0].tasks) == 1

    def test_load_missing_file_returns_empty(self):
        users = load_all()
        assert users == []

    def test_load_corrupted_json(self):
        ensure_data_folder()
        with open(DATA_FILE, "w") as f:
            f.write("not valid json{{{")
        users = load_all()
        assert users == []

    def test_find_user(self):
        User(name="Alice")
        User(name="Bob")
        found = find_user(User.users, "alice")
        assert found is not None
        assert found.name == "Alice"
        assert find_user(User.users, "charlie") is None

    def test_find_project(self):
        user = User(name="Alice")
        proj = Project(title="Website")
        user.add_project(proj)
        found = find_project(User.users, "website")
        assert found is not None
        assert found.title == "Website"

    def test_find_task(self):
        user = User(name="Alice")
        proj = Project(title="Website")
        user.add_project(proj)
        task = Task(title="Design")
        proj.add_task(task)

        t, p, u = find_task(User.users, "design")
        assert t is not None
        assert t.title == "Design"
        assert p.title == "Website"
        assert u.name == "Alice"

    def test_persistence_id_consistency(self):
        User(name="Alice")
        save_all(User.users)

        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()

        users = load_all()
        # Adding a new user after reload should get id=2
        new_user = User(name="Bob")
        assert new_user.id == 2
'''
