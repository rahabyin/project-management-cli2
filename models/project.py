from models.task import Task


class Project:
    projects = []
    id_counter = 1

    def __init__(self, title, description="", due_date=""):
        self.id = Project.id_counter
        Project.id_counter += 1

        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []

        Project.projects.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty")
        self._title = value.strip()

    def add_task(self, task):
    # if already a Task object → use it directly
     if isinstance(task, Task):
        self.tasks.append(task)
        return task
    # if it's a string → convert to Task
     task = Task(title=task)
     self.tasks.append(task)
     return task

    def complete_task(self, task_id):
        """Mark a task complete by ID."""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_complete()
                return task
        return None
    
    def get_completed_tasks(self):
     return [task for task in self.tasks if task.status == "completed"]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data):
        tasks = [Task.from_dict(task) for task in data.get("tasks", [])]
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            tasks=tasks,
            project_id=data.get("id")
        )

    def __str__(self):
        return f"{self.title} ({len(self.tasks)} tasks)"
    
    @classmethod
    def clear_projects(cls):
     cls.projects = []
     cls.id_counter = 1

    @classmethod
    def find_by_title(cls, title):
     for project in cls.projects:
        if project.title.lower() == title.lower():
            return project
     return None