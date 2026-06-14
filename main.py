import argparse

from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task

console = Console()

def add_user(args):
    users = load_users()

    if find_user(users, args.name):
        console.print(f"[red]User '{args.name}' already exists.[/red]")
        return

    user = User(name=args.name, email=args.email)
    users.append(user)
    save_users(users)

    console.print(f"[green]User added successfully:[/green] {user}")


def list_users(args):
    users = load_users()

    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Users")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Projects")

    for user in users:
        table.add_row(str(user.id), user.name, user.email, str(len(user.projects)))

    console.print(table)


def add_project(args):
    users = load_users()
    user = find_user(users, args.user)

    if not user:
        console.print(f"[red]User '{args.user}' not found.[/red]")
        return

    if user.get_project(args.title):
        console.print(f"[red]Project '{args.title}' already exists for {args.user}.[/red]")
        return

    project = user.add_project(
        title=args.title,
        description=args.description,
        due_date=args.due_date
    )

    save_users(users)
    console.print(f"[green]Project added:[/green] {project.title} assigned to {user.name}")


def list_projects(args):
    users = load_users()

    if args.user:
        user = find_user(users, args.user)

        if not user:
            console.print(f"[red]User '{args.user}' not found.[/red]")
            return

        projects = user.projects
        title = f"Projects for {user.name}"
    else:
        projects = []
        for user in users:
            projects.extend(user.projects)
        title = "All Projects"

    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title=title)
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Due Date")
    table.add_column("Tasks")

    for project in projects:
        table.add_row(
            str(project.id),
            project.title,
            project.description,
            project.due_date,
            str(len(project.tasks))
        )

    console.print(table)


def add_task(args):
    users = load_users()
    project = find_project(users, args.project)

    if not project:
        console.print(f"[red]Project '{args.project}' not found.[/red]")
        return

    task = project.add_task(title=args.title, assigned_to=args.assigned_to)
    save_users(users)

    console.print(f"[green]Task added:[/green] {task.title} to project '{project.title}'")


def list_tasks(args):
    users = load_users()
    project = find_project(users, args.project)

    if not project:
        console.print(f"[red]Project '{args.project}' not found.[/red]")
        return

    if not project.tasks:
        console.print("[yellow]No tasks found for this project.[/yellow]")
        return

    table = Table(title=f"Tasks for {project.title}")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Assigned To")
    table.add_column("Status")

    for task in project.tasks:
        table.add_row(
            str(task.id),
            task.title,
            task.assigned_to or "Unassigned",
            task.status
        )

    console.print(table)


def complete_task(args):
    users = load_users()
    project = find_project(users, args.project)

    if not project:
        console.print(f"[red]Project '{args.project}' not found.[/red]")
        return

    task = project.complete_task(args.task_id)

    if not task:
        console.print(f"[red]Task with ID {args.task_id} not found.[/red]")
        return

    save_users(users)
    console.print(f"[green]Task completed:[/green] {task.title}")


def search_projects(args):
    users = load_users()
    results = []

    for user in users:
        for project in user.projects:
            if args.keyword.lower() in project.title.lower():
                results.append((user, project))

    if not results:
        console.print("[yellow]No matching projects found.[/yellow]")
        return

    table = Table(title=f"Search Results for '{args.keyword}'")
    table.add_column("User")
    table.add_column("Project")
    table.add_column("Due Date")

    for user, project in results:
        table.add_row(user.name, project.title, project.due_date)

    console.print(table)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool",
        epilog="Example: python main.py add-user --name Alex --email alex@example.com"
    )

    subparsers = parser.add_subparsers(dest="command")

    add_user_parser = subparsers.add_parser("add-user", help="Create a new user")
    add_user_parser.add_argument("--name", required=True)
    add_user_parser.add_argument("--email", required=True)
    add_user_parser.set_defaults(func=add_user)

    list_users_parser = subparsers.add_parser("list-users", help="List all users")
    list_users_parser.set_defaults(func=list_users)

    add_project_parser = subparsers.add_parser("add-project", help="Add project to a user")
    add_project_parser.add_argument("--user", required=True)
    add_project_parser.add_argument("--title", required=True)
    add_project_parser.add_argument("--description", default="")
    add_project_parser.add_argument("--due-date", default="")
    add_project_parser.set_defaults(func=add_project)

    list_projects_parser = subparsers.add_parser("list-projects", help="List projects")
    list_projects_parser.add_argument("--user", required=False)
    list_projects_parser.set_defaults(func=list_projects)

    add_task_parser = subparsers.add_parser("add-task", help="Add task to a project")
    add_task_parser.add_argument("--project", required=True)
    add_task_parser.add_argument("--title", required=True)
    add_task_parser.add_argument("--assigned-to", default=None)
    add_task_parser.set_defaults(func=add_task)

    list_tasks_parser = subparsers.add_parser("list-tasks", help="List tasks for a project")
    list_tasks_parser.add_argument("--project", required=True)
    list_tasks_parser.set_defaults(func=list_tasks)

    complete_task_parser = subparsers.add_parser("complete-task", help="Mark task as complete")
    complete_task_parser.add_argument("--project", required=True)
    complete_task_parser.add_argument("--task-id", required=True, type=int)
    complete_task_parser.set_defaults(func=complete_task)

    search_parser = subparsers.add_parser("search-projects", help="Search projects by keyword")
    search_parser.add_argument("--keyword", required=True)
    search_parser.set_defaults(func=search_projects)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


