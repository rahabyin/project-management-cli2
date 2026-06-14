import json
import os

from models.user import User


DATA_FILE = "data/tracker_data.json"


def ensure_data_folder():
    """Create the data folder if it does not exist."""
    os.makedirs("data", exist_ok=True)


def load_users(filename=DATA_FILE):
    """Load users, projects, and tasks from JSON."""
    ensure_data_folder()

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return [User.from_dict(user) for user in data.get("users", [])]
    except json.JSONDecodeError:
        print("Warning: Data file is damaged. Starting with empty data.")
        return []


def save_users(users, filename=DATA_FILE):
    """Save all users, projects, and tasks to JSON."""
    ensure_data_folder()

    data = {
        "users": [user.to_dict() for user in users]
    }

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def find_user(users, name):
    """Find a user by name."""
    for user in users:
        if user.name.lower() == name.lower():
            return user
    return None


def find_project(users, title):
    """Find a project across all users."""
    for user in users:
        project = user.get_project(title)
        if project:
            return project
    return None