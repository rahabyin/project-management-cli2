from models import User, Project, Task


def cmd_add_user(args):
    User(args.name, args.email)
    print(f"User '{args.name}' added successfully.")


def cmd_add_project(args):
    user = User.find_by_name(args.user)

    if user is None:
        print(f"User '{args.user}' not found.")
        return

    project = Project(args.title, args.description, args.due_date)
    user.add_project(project)
    print(f"Project '{args.title}' added successfully.")


def cmd_add_task(args):
    project = Project.find_by_title(args.project)

    if project is None:
        print(f"Project '{args.project}' not found.")
        return

    task = Task(args.title, args.assigned_to)
    project.add_task(task)
    print(f"Task '{args.title}' added successfully.")


def cmd_complete_task(args):
    project = Project.find_by_title(args.project)

    if project is None:
        print(f"Project '{args.project}' not found.")
        return

    for task in project.tasks:
        if task.title == args.task:
            task.mark_complete()
            print(f"Task '{args.task}' marked as completed.")
            return

    print(f"Task '{args.task}' not found.")


def cmd_list_users(args):
    for user in User.users:
        print(f"{user.name} - {user.email}")


def cmd_user_details(args):
    user = User.find_by_name(args.name)

    if user is None:
        print(f"User '{args.name}' not found.")
        return

    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"Projects: {len(user.projects)}")