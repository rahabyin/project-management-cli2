'''import pytest
from unittest.mock import patch
from io import StringIO

from main import build_parser, cmd_add_user, cmd_add_project, cmd_add_task
from models.user import User
from models.project import Project
from models.task import Task


class TestCLI:
    def setup_method(self):
        User.clear_users()
        Project.clear_projects()
        Task.clear_tasks()

    @patch("main.persist_data")
    def test_add_user_command(self, mock_persist):
        mock_persist.return_value = True
        parser = build_parser()
        args = parser.parse_args(["user", "add", "Alice", "--email", "alice@example.com"])
        args.func(args)
        assert len(User.users) == 1
        assert User.users[0].name == "Alice"

    @patch("main.persist_data")
    def test_add_project_command(self, mock_persist):
        mock_persist.return_value = True
        User(name="Alice")
        parser = build_parser()
        args = parser.parse_args([
            "project", "add", "Website",
            "--user", "Alice",
            "--description", "Company site",
            "--due-date", "2025-12-01"
        ])
        args.func(args)
        assert len(Project.projects) == 1
        assert Project.projects[0].title == "Website"

    @patch("main.persist_data")
    def test_add_task_command(self, mock_persist):
        mock_persist.return_value = True
        user = User(name="Alice")
        proj = Project(title="Website")
        user.add_project(proj)
        parser = build_parser()
        args = parser.parse_args([
            "task", "add", "Design",
            "--project", "Website",
            "--assigned-to", "Alice"
        ])
        args.func(args)
        assert len(proj.tasks) == 1
        assert proj.tasks[0].title == "Design"

    def test_parser_help(self):
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_cli_error_on_missing_user(self):
        parser = build_parser()
        args = parser.parse_args(["project", "add", "Website", "--user", "Nobody"])
        with pytest.raises(SystemExit):
            args.func(args)
'''
