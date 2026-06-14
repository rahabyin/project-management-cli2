class Task:
    tasks = []
    ALLOWED_STATUSES = {"pending", "completed"}

    def __init__(self, title, assigned_to=None, status="pending"):
        self.title = title
        self.assigned_to = assigned_to
        self.status = status
        Task.tasks.append(self)
        

    # TITLE 
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
        raise ValueError("Invalid status")
     self._status = value

    # STATUS 
    def mark_complete(self):
        self.status = "completed"

    def mark_pending(self):
        self.status = "pending"

    def is_completed(self):
        return self.status == "completed"

    @classmethod
    def clear_tasks(cls):
     cls.tasks.clear()
     cls.id_counter = 1 