import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.models import Project, Task, User

def test_user_creation():
    user = User("Ian", "ian@email.com")
    assert user.name == "Ian"
    assert user.email == "ian@email.com"
    assert user.projects == []

def test_project_creation():
    project = Project(1, "Testing CLI", "Testing creation of CLI tool", 
                      "2025-08-09")
    assert project.user_id == 1
    assert project.title == "Testing CLI"
    assert project.description == "Testing creation of CLI tool"
    assert project.due_date == "2025-08-09"
    assert project.tasks == []

def test_task_creation():
    task = Task(1, "Write tests", "Incomplete", 1)
    assert task.project_id == 1
    assert task.title == "Write tests"
    assert task.status == "Incomplete"
    assert task.assigned_to == 1
    task.mark_complete()
    assert task.status == "Complete"