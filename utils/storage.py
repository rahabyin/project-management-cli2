import json
import os
import logging

from models.user import User
from models.project import Project
from models.task import Task

logger = logging.getLogger(__name__)

DATA_FILE = "data/tracker_data.json"


def ensure_data_folder():
    """Create the data folder if it does not exist."""
    try:
        os.makedirs("data", exist_ok=True)
    except PermissionError:
        logger.error("Permission denied creating data folder")
        raise


def load_all(filename=DATA_FILE):
    """
    Load users, projects, and tasks from JSON.
    Returns a list of User objects with fully reconstructed relationships.
    Handles missing files, corrupted JSON, permission errors, and invalid data.
    """
    ensure_data_folder()

    # Clear in-memory state to avoid duplicates on reload
    User.clear_users()
    Project.clear_projects()
    Task.clear_tasks()

    if not os.path.exists(filename):
        logger.info("Data file not found. Starting with empty dataset.")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"Data file is corrupted ({e}). Starting with empty dataset.")
        return []
    except PermissionError:
        logger.error(f"Permission denied reading {filename}. Starting with empty dataset.")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error in {filename} ({e}). Starting with empty dataset.")
        return []

    users_data = data.get("users", [])
    users = []
    for user_data in users_data:
        try:
            user = User.from_dict(user_data)
            users.append(user)
        except (KeyError, ValueError, TypeError) as e:
            logger.warning(f"Skipping corrupted user entry: {e}")

    logger.info(f"Loaded {len(users)} user(s) from {filename}")
    return users


def save_all(users, filename=DATA_FILE):
    """
    Save all users, projects, and tasks to JSON with proper error handling.
    Returns True on success, False on failure.
    """
    ensure_data_folder()

    data = {
        "users": [user.to_dict() for user in users]
    }

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info(f"Saved {len(users)} user(s) to {filename}")
        return True
    except PermissionError:
        logger.error(f"Permission denied writing to {filename}")
        return False
    except TypeError as e:
        logger.error(f"Serialization error: {e}")
        return False
    except OSError as e:
        logger.error(f"OS error saving data: {e}")
        return False


def find_user(users, name):
    """Find a user by name (case-insensitive)."""
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


def find_task(users, task_title):
    """Find a task across all users and projects."""
    for user in users:
        for project in user.projects:
            for task in project.tasks:
                if task.title.lower() == task_title.lower():
                    return task, project, user
    return None, None, None


def backup_data(filename=DATA_FILE, backup_suffix=".backup"):
    """Create a backup of the current data file."""
    if not os.path.exists(filename):
        logger.warning("No data file to backup")
        return False
    backup_name = filename + backup_suffix
    try:
        with open(filename, "r", encoding="utf-8") as src:
            with open(backup_name, "w", encoding="utf-8") as dst:
                dst.write(src.read())
        logger.info(f"Backup created: {backup_name}")
        return True
    except OSError as e:
        logger.error(f"Failed to create backup: {e}")
        return False