from datetime import datetime
from typing import List

class Person:
    def __init__(self, name: str, email: str):
        self.name = name.strip()
        self.email = email

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        v = value.strip()
        if "@" not in v:
            raise ValueError("Invalid email address")
        self._email = v

class User(Person):
    _ID_COUNTER = 0
    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        type(self)._ID_COUNTER += 1
        self.id = type(self)._ID_COUNTER
        self.projects = []

    @property
    def projects(self) -> List["Project"]:
        return [p for p in Project.all() if p.user_id == self.id]
    
    def create_project(self, title: str, description: str, due_date: str) -> "Project":
        return Project.create(user_id=self.id, title=title, description=description, due_date=due_date)

    def add_project(self, project):
        self.projects.append(project)

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name} Email: {self.email}"

class Project:
    _ID_COUNTER = 0
    _PROJECTS: dict[int, "Project"] = {}
    def __init__(self, user_id: int, title: str, description: str, due_date: str):
        self.user_id = int(user_id)
        self.title = title.strip()
        self.description = description.strip()
        self.due_date = due_date
        type(self)._ID_COUNTER += 1
        self.id = type(self)._ID_COUNTER
        type(self)._PROJECTS[self.id] = self
        self.tasks = []

    @property
    def due_date(self) -> str:
        return self._due_date
    
    @due_date.setter
    def due_date(self, value: str):
        dt = datetime.strptime(value.strip(), "%Y-%m-%d")
        self._due_date = dt.date().isoformat()

    @property
    def tasks(self) -> List["Task"]:
        return [t for t in Task.all() if t.project_id == self.id]
    
    def create_task(self, title: str, status: str, assigned_to: int) -> "Task":
        return Task.create(project_id=self.id, title=title, status=status, assigned_to=assigned_to)

    def add_task(self, task):
        self.tasks.append(task)

    @classmethod
    def create(cls, user_id: int, title: str, description: str, due_date: str) -> "Project":
        return cls(user_id, title, description, due_date)

    @classmethod
    def get(cls, id: int) -> "Project":
        return cls._PROJECTS.get(id)
    
    @classmethod
    def all(cls) -> List["Project"]:
        return list(cls._PROJECTS.values())
    
    def __str__(self):
        return f"ID: {self.id}, Title: {self.title} Due: {self.due_date}"

class Task:
    _TASKS: dict[int, "Task"] = {}
    def __init__(self, project_id: int, title: str, status: str, assigned_to: int):
        self.project_id = int(project_id)
        self.title = title.strip()
        self.status = status
        self.assigned_to = assigned_to
        type(self)._TASKS[self.id] = self

    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, value: str):
        v = value.strip()
        if v is not "Incomplete" and v is not "Complete":
            raise ValueError("Invalid status")
        self._status = v

    @classmethod
    def create(cls, project_id: int, title: str, status: str, assigned_to: int):
        if not Project.get(project_id):
            raise ValueError("Project does not exist")
        return cls(project_id=project_id, title=title, status=status, assigned_to=assigned_to)
    
    @classmethod
    def all(cls) -> List["Task"]:
        return list(cls._TASKS.values())

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title} ({self.status}), Assigned to: {self.assigned_to}"
    