"""Unit tests for Project Management CLI Tool"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import User, Project, Task
from utils import validate_not_empty, validate_email


class TestUser(unittest.TestCase):
    def setUp(self):
        User.clear_users()

    def tearDown(self):
        User.clear_users()

    def test_user_creation(self):
        user = User("Alex", "alex@example.com")
        self.assertEqual(user.name, "Alex")
        self.assertEqual(user.email, "alex@example.com")

    def test_user_name_setter(self):
        user = User("Alex")
        user.name = "Alexander"
        self.assertEqual(user.name, "Alexander")

    def test_user_name_validation(self):
        user = User("Alex")
        with self.assertRaises(ValueError):
            user.name = ""

    def test_user_email_validation(self):
        user = User("Alex")
        with self.assertRaises(ValueError):
            user.email = "invalid-email"

    def test_user_projects(self):
        user = User("Alex")
        project = Project("Website", "Build a website")
        user.add_project(project)
        self.assertEqual(len(user.projects), 1)
        self.assertEqual(user.projects[0].title, "Website")

    def test_find_by_name(self):
        User("Alex")
        found = User.find_by_name("Alex")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Alex")

    def test_find_by_name_not_found(self):
        result = User.find_by_name("NonExistent")
        self.assertIsNone(result)

    def test_population_counter(self):
        initial = User.get_population()
        User("User1")
        User("User2")
        self.assertEqual(User.get_population(), initial + 2)


class TestProject(unittest.TestCase):
    def setUp(self):
        Project.clear_projects()
        Task.clear_tasks()

    def tearDown(self):
        Project.clear_projects()
        Task.clear_tasks()

    def test_project_creation(self):
        project = Project("Website", "Build a website", "2026-12-31")
        self.assertEqual(project.title, "Website")
        self.assertEqual(project.due_date, "2026-12-31")

    def test_project_id_counter(self):
        p1 = Project("Project1")
        p2 = Project("Project2")
        self.assertEqual(p2.id, p1.id + 1)

    def test_add_task(self):
        project = Project("Website")
        task = Task("Design homepage")
        project.add_task(task)
        self.assertEqual(len(project.tasks), 1)
        self.assertEqual(project.tasks[0].title, "Design homepage")

    def test_task_status(self):
        task = Task("Test task")
        self.assertEqual(task.status, "pending")
        task.mark_complete()
        self.assertEqual(task.status, "completed")
        self.assertTrue(task.is_completed())

    def test_completed_tasks(self):
        project = Project("Website")
        task1 = Task("Task1")
        task2 = Task("Task2")
        project.add_task(task1)
        project.add_task(task2)
        task1.mark_complete()
        completed = project.get_completed_tasks()
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].title, "Task1")

    def test_find_by_title(self):
        Project("Website")
        found = Project.find_by_title("Website")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Website")


class TestTask(unittest.TestCase):
    def setUp(self):
        Task.clear_tasks()

    def tearDown(self):
        Task.clear_tasks()

    def test_task_creation(self):
        task = Task("Implement feature", "Alex", "pending")
        self.assertEqual(task.title, "Implement feature")
        self.assertEqual(task.assigned_to, "Alex")
        self.assertEqual(task.status, "pending")

    def test_mark_complete(self):
        task = Task("Test")
        task.mark_complete()
        self.assertEqual(task.status, "completed")

    def test_mark_pending(self):
        task = Task("Test")
        task.mark_complete()
        task.mark_pending()
        self.assertEqual(task.status, "pending")


class TestValidators(unittest.TestCase):
    def test_validate_not_empty(self):
        self.assertTrue(validate_not_empty("hello", "name"))

    def test_validate_not_empty_raises(self):
        with self.assertRaises(ValueError):
            validate_not_empty("", "name")

    def test_validate_email(self):
        self.assertTrue(validate_email("test@example.com"))

    def test_validate_email_invalid(self):
        with self.assertRaises(ValueError):
            validate_email("invalid-email")


class TestFileIO(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join(os.path.dirname(__file__), "test_data.json")
        self.test_data = [
            {"name": "Alex", "email": "alex@example.com"},
            {"name": "Sam", "email": "sam@example.com"}
        ]

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load(self):
        from utils.file_io import save_to_json, load_from_json
        result = save_to_json(self.test_data, self.test_file)
        self.assertTrue(result)
        loaded = load_from_json(self.test_file)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["name"], "Alex")

    def test_load_nonexistent_file(self):
        from utils.file_io import load_from_json
        result = load_from_json("nonexistent.json")
        self.assertEqual(result, [])


class TestInheritance(unittest.TestCase):
    def setUp(self):
        User.clear_users()

    def tearDown(self):
        User.clear_users()

    def test_user_is_person(self):
        from models.person import Person
        user = User("Alex")
        self.assertIsInstance(user, Person)

    def test_user_has_introduce(self):
        user = User("Alex")
        self.assertEqual(user.introduce(), "Hi, I am Alex")


class TestCLICommands(unittest.TestCase):
    def setUp(self):
        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()

    def tearDown(self):
        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()

    def test_add_user_command(self):
        from main import cmd_add_user

        class MockArgs:
            name = "TestUser"
            email = "test@example.com"

        cmd_add_user(MockArgs())
        user = User.find_by_name("TestUser")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    def test_add_project_command(self):
        from main import cmd_add_project

        User("TestUser")

        class MockArgs:
            user = "TestUser"
            title = "TestProject"
            description = "A test project"
            due_date = "2026-12-31"

        cmd_add_project(MockArgs())
        project = Project.find_by_title("TestProject")
        self.assertIsNotNone(project)
        self.assertEqual(project.description, "A test project")

    def test_add_task_command(self):
        from main import cmd_add_task

        User("TestUser")
        project = Project("TestProject")
        User.find_by_name("TestUser").add_project(project)

        class MockArgs:
            project = "TestProject"
            title = "TestTask"
            assigned_to = "TestUser"

        cmd_add_task(MockArgs())
        self.assertEqual(len(project.tasks), 1)
        self.assertEqual(project.tasks[0].title, "TestTask")

    def test_complete_task_command(self):
        from main import cmd_complete_task

        User("TestUser")
        project = Project("TestProject")
        User.find_by_name("TestUser").add_project(project)
        task = Task("TestTask")
        project.add_task(task)

        class MockArgs:
            project = "TestProject"
            task = "TestTask"

        cmd_complete_task(MockArgs())
        self.assertEqual(task.status, "completed")

    def test_list_users_command(self):
        from main import cmd_list_users

        User("User1")
        User("User2")

        class MockArgs:
            pass

        cmd_list_users(MockArgs())

    def test_user_details_command(self):
        from main import cmd_user_details

        User("TestUser", "test@example.com")

        class MockArgs:
            name = "TestUser"

        cmd_user_details(MockArgs())


if __name__ == "__main__":
    unittest.main(verbosity=2)