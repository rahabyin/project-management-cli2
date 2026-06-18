'''#!/usr/bin/env python3
"""
Project Management CLI Tool

A command-line interface for managing users, projects, and tasks
with full JSON persistence and rich terminal output.
"""

import argparse
import sys
import logging

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from models.user import User
from models.project import Project
from models.task import Task
from storage import load_all, save_all, find_user, find_project, find_task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

console = Console()


def load_data():
    """Load data from disk into model class variables."""
    users = load_all()
    # load_all already populates User.users, Project.projects, Task.tasks
    return users


def persist_data():
    """Save current in-memory state to disk."""
    return save_all(User.users)


# ─────────────────────────────────────────────
# COMMAND HANDLERS
# ─────────────────────────────────────────────

def cmd_add_user(args):
    try:
        user = User(name=args.name, email=args.email)
        if persist_data():
            console.print(f"[green]✓ User '{args.name}' added successfully.[/green]")
        else:
            console.print("[yellow]⚠ User created but failed to save to disk.[/yellow]")
    except ValueError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


def cmd_add_project(args):
    user = find_user(User.users, args.user)
    if user is None:
        console.print(f"[red]✗ User '{args.user}' not found.[/red]")
        sys.exit(1)

    try:
        project = Project(
            title=args.title,
            description=args.description or "",
            due_date=args.due_date or ""
        )
        user.add_project(project)
        if persist_data():
            console.print(f"[green]✓ Project '{args.title}' added to user '{user.name}'.[/green]")
        else:
            console.print("[yellow]⚠ Project created but failed to save.[/yellow]")
    except ValueError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


def cmd_add_task(args):
    project = find_project(User.users, args.project)
    if project is None:
        console.print(f"[red]✗ Project '{args.project}' not found.[/red]")
        sys.exit(1)

    try:
        task = Task(title=args.title, assigned_to=args.assigned_to)
        project.add_task(task)
        if persist_data():
            console.print(f"[green]✓ Task '{args.title}' added to project '{project.title}'.[/green]")
        else:
            console.print("[yellow]⚠ Task created but failed to save.[/yellow]")
    except ValueError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


def cmd_complete_task(args):
    task, project, user = find_task(User.users, args.task)
    if task is None:
        console.print(f"[red]✗ Task '{args.task}' not found.[/red]")
        sys.exit(1)

    task.mark_complete()
    if persist_data():
        console.print(f"[green]✓ Task '{task.title}' marked as completed.[/green]")
    else:
        console.print("[yellow]⚠ Task updated but failed to save.[/yellow]")


def cmd_list_users(args):
    if not User.users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Users", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Projects", justify="right")

    for user in User.users:
        table.add_row(
            str(user.id),
            user.name,
            user.email or "—",
            str(len(user.projects))
        )
    console.print(table)


def cmd_user_details(args):
    user = find_user(User.users, args.name)
    if user is None:
        console.print(f"[red]✗ User '{args.name}' not found.[/red]")
        sys.exit(1)

    # Build project sub-table
    proj_table = Table(box=box.SIMPLE)
    proj_table.add_column("Project", style="cyan")
    proj_table.add_column("Tasks", justify="right")
    proj_table.add_column("Completed", justify="right")
    proj_table.add_column("Due Date", style="dim")

    for proj in user.projects:
        proj_table.add_row(
            proj.title,
            str(len(proj.tasks)),
            str(len(proj.get_completed_tasks())),
            proj.due_date or "—"
        )

    panel = Panel(
        f"[bold]Name:[/bold] {user.name}\\n"
        f"[bold]Email:[/bold] {user.email or 'Not set'}\\n"
        f"[bold]Projects:[/bold] {len(user.projects)}\\n\\n"
        f"[bold underline]Project Breakdown[/bold underline]\\n",
        title=f"User #{user.id}",
        border_style="blue"
    )
    console.print(panel)
    console.print(proj_table)


def cmd_list_projects(args):
    if not Project.projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title="All Projects", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Tasks", justify="right")
    table.add_column("Completed", justify="right")
    table.add_column("Due Date", style="dim")

    for proj in Project.projects:
        table.add_row(
            str(proj.id),
            proj.title,
            str(len(proj.tasks)),
            str(len(proj.get_completed_tasks())),
            proj.due_date or "—"
        )
    console.print(table)


def cmd_project_details(args):
    project = find_project(User.users, args.title)
    if project is None:
        console.print(f"[red]✗ Project '{args.title}' not found.[/red]")
        sys.exit(1)

    task_table = Table(box=box.SIMPLE)
    task_table.add_column("ID", style="cyan", no_wrap=True)
    task_table.add_column("Task", style="magenta")
    task_table.add_column("Assigned To", style="green")
    task_table.add_column("Status")

    for task in project.tasks:
        status_style = "green" if task.is_completed() else "yellow"
        status_text = "[green]✓ Done[/green]" if task.is_completed() else "[yellow]○ Pending[/yellow]"
        task_table.add_row(
            str(task.id),
            task.title,
            task.assigned_to or "—",
            status_text
        )

    panel = Panel(
        f"[bold]Title:[/bold] {project.title}\\n"
        f"[bold]Description:[/bold] {project.description or 'None'}\\n"
        f"[bold]Due Date:[/bold] {project.due_date or 'Not set'}\\n"
        f"[bold]Tasks:[/bold] {len(project.tasks)} total, {len(project.get_completed_tasks())} completed\\n\\n"
        f"[bold underline]Tasks[/bold underline]",
        title=f"Project #{project.id}",
        border_style="purple"
    )
    console.print(panel)
    console.print(task_table)


def cmd_delete_user(args):
    user = find_user(User.users, args.name)
    if user is None:
        console.print(f"[red]✗ User '{args.name}' not found.[/red]")
        sys.exit(1)

    User.users.remove(user)
    if persist_data():
        console.print(f"[green]✓ User '{args.name}' deleted.[/green]")
    else:
        console.print("[yellow]⚠ User removed but failed to save.[/yellow]")


def cmd_delete_project(args):
    project = find_project(User.users, args.title)
    if project is None:
        console.print(f"[red]✗ Project '{args.title}' not found.[/red]")
        sys.exit(1)

    # Remove from owner's project list
    for user in User.users:
        if project in user.projects:
            user.projects.remove(project)
            break

    # Remove from global projects list
    if project in Project.projects:
        Project.projects.remove(project)

    if persist_data():
        console.print(f"[green]✓ Project '{args.title}' deleted.[/green]")
    else:
        console.print("[yellow]⚠ Project removed but failed to save.[/yellow]")


# ─────────────────────────────────────────────
# CLI SETUP
# ─────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="pmcli",
        description="Project Management CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s user add "Alice" --email alice@example.com
  %(prog)s project add "Website" --user Alice --due-date 2025-12-01
  %(prog)s task add "Design homepage" --project Website --assigned-to Alice
  %(prog)s task complete "Design homepage"
  %(prog)s list users
  %(prog)s show user Alice
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── user ──
    user_parser = subparsers.add_parser("user", help="User management commands")
    user_sub = user_parser.add_subparsers(dest="user_cmd")

    user_add = user_sub.add_parser("add", help="Add a new user")
    user_add.add_argument("name", help="User name")
    user_add.add_argument("--email", help="User email")
    user_add.set_defaults(func=cmd_add_user)

    user_del = user_sub.add_parser("delete", help="Delete a user")
    user_del.add_argument("name", help="User name")
    user_del.set_defaults(func=cmd_delete_user)

    # ── project ──
    proj_parser = subparsers.add_parser("project", help="Project management commands")
    proj_sub = proj_parser.add_subparsers(dest="proj_cmd")

    proj_add = proj_sub.add_parser("add", help="Add a new project")
    proj_add.add_argument("title", help="Project title")
    proj_add.add_argument("--user", required=True, help="Owner user name")
    proj_add.add_argument("--description", help="Project description")
    proj_add.add_argument("--due-date", help="Due date (YYYY-MM-DD)")
    proj_add.set_defaults(func=cmd_add_project)

    proj_del = proj_sub.add_parser("delete", help="Delete a project")
    proj_del.add_argument("title", help="Project title")
    proj_del.set_defaults(func=cmd_delete_project)

    # ── task ──
    task_parser = subparsers.add_parser("task", help="Task management commands")
    task_sub = task_parser.add_subparsers(dest="task_cmd")

    task_add = task_sub.add_parser("add", help="Add a task to a project")
    task_add.add_argument("title", help="Task title")
    task_add.add_argument("--project", required=True, help="Project title")
    task_add.add_argument("--assigned-to", help="Person assigned to the task")
    task_add.set_defaults(func=cmd_add_task)

    task_comp = task_sub.add_parser("complete", help="Mark a task as completed")
    task_comp.add_argument("task", help="Task title")
    task_comp.set_defaults(func=cmd_complete_task)

    # ── list ──
    list_parser = subparsers.add_parser("list", help="List entities")
    list_sub = list_parser.add_subparsers(dest="list_cmd")

    list_users = list_sub.add_parser("users", help="List all users")
    list_users.set_defaults(func=cmd_list_users)

    list_projects = list_sub.add_parser("projects", help="List all projects")
    list_projects.set_defaults(func=cmd_list_projects)

    # ── show ──
    show_parser = subparsers.add_parser("show", help="Show detailed information")
    show_sub = show_parser.add_subparsers(dest="show_cmd")

    show_user = show_sub.add_parser("user", help="Show user details")
    show_user.add_argument("name", help="User name")
    show_user.set_defaults(func=cmd_user_details)

    show_project = show_sub.add_parser("project", help="Show project details")
    show_project.add_argument("title", help="Project title")
    show_project.set_defaults(func=cmd_project_details)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Load data from disk before executing any command
    load_data()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
'''


