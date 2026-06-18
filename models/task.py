class Task:
    tasks = []
    id_counter = 1
    ALLOWED_STATUSES = {"pending", "completed"}

    def __init__(self, title, assigned_to=None, status="pending", task_id=None):
        self.id = task_id if task_id is not None else Task.id_counter
        Task.id_counter = max(Task.id_counter, self.id + 1)

        self.title = title
        self.assigned_to = assigned_to
        self.status = status
        Task.tasks.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string")
        self._title = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {value}. Must be one of {self.ALLOWED_STATUSES}")
        self._status = value

    def mark_complete(self):
        self.status = "completed"

    def mark_pending(self):
        self.status = "pending"

    def is_completed(self):
        return self.status == "completed"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            assigned_to=data.get("assigned_to"),
            status=data.get("status", "pending"),
            task_id=data.get("id")
        )

    @classmethod
    def clear_tasks(cls):
        cls.tasks.clear()
        cls.id_counter = 1

    @classmethod
    def find_by_title(cls, title):
        for task in cls.tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    def __str__(self):
        status_icon = "✓" if self.is_completed() else "○"
        return f"[{status_icon}] {self.title} (Assigned to: {self.assigned_to or 'Unassigned'})"