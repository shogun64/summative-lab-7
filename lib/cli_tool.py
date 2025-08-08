import argparse
import json
import os
from models import Project, Task, User
from rich import print

def load_data(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            contents = f.read().strip()
            return json.loads(contents) if contents else []
    except json.JSONDecodeError:
        return []
    
def save_data(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
def set_users(users):
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

def get_users(data):
    users = []
    for u in data:
        user = User(u["name"], u["email"])
        user.id = u["id"]
        users.append(user)
    return users

def set_projects(projects):
    return [{"id": p.id, "user_id": p.user_id, "title": p.title, "description": p.description,
             "due_date": p.due_date} for p in projects]

def get_projects(data):
    projects = []
    for p in data:
        project = Project(p["user_id"], p["title"], p["description"], p["due_date"])
        project.id = p["id"]
        projects.append(project)
    return projects

def set_tasks(tasks):
    return [{"id": t.id, "project_id": t.project_id, "title": t.title, "status": t.status,
             "assigned_to": t.assigned_to} for t in tasks]

def get_tasks(data):
    tasks = []
    for t in data:
        task = Task(t["project_id"], t["title"], t["status"], t["assigned_to"])
        task.id = t["id"]
        tasks.append(task)
    return tasks

USER_FILE = "users.json"
PROJECT_FILE = "projects.json"
TASK_FILE = "tasks.json"

users = get_users(load_data(USER_FILE))
projects = get_projects(load_data(PROJECT_FILE))
tasks = get_tasks(load_data(TASK_FILE))

def add_user(args):
    user = User(args.name, args.email)
    users.append(user)
    save_data(USER_FILE, set_users(users))
    print(f"[blue]User has been added:[/blue] {user}")

def list_users(args):
    if not users:
        print("[yellow]No users found.[/yellow]")
    for u in users:
        print(u)

def add_project(args):
    user = next((u for u in users if u.name == args.user), None)
    if not user:
        print(f"[red]User '{args.user}' could not be found.[/red]")
        return
    project = Project(user.id, args.title, args.description, args.due_date)
    projects.append(project)
    save_data(PROJECT_FILE, set_projects(projects))
    print(f"[purple]Project has been added:[/purple] {project}")

def list_projects(args):
    if args.user:
        user = next((u for u in users if u.name == args.user), None)
        if not user:
            print(f"[red]User '{args.user}' could not be found.[/red]")
            return
        user_projects = [p for p in projects if p.user_id == user.id]
        for p in user_projects:
            print(p)
    else:
        for p in projects:
            print(p)

def add_task(args):
    project = next((p for p in projects if p.id == int(args.project_id)), None)
    if not project:
        print(f"[red]Project ID '{args.project_id}' could not be found.[/red]")
        return
    task = Task(project.id, args.title, "Incomplete", args.assigned_to)
    project.tasks.append(task)
    tasks.append(task)
    save_data(TASK_FILE, set_tasks(tasks))
    print(f"[green]Task added:[/green] {task}")

def list_tasks(args):
    for t in tasks:
        print(t)

def complete_task(args):
    task = next((t for t in tasks if t.id == args.task_id), None)
    if not task:
        print(f"[red]Task ID {args.task_id} could not be found.[/red]")
        return
    task.mark_complete()
    save_data(TASK_FILE, set_tasks(tasks))
    print(f"[green]Task has been marked complete:[/green] {task}")

def setup_parser():
    parser = argparse.ArgumentParser(description="Project Manager CLI")
    subparsers = parser.add_subparsers()

    user_parser = subparsers.add_parser("add-user")
    user_parser.add_argument("--name", required=True)
    user_parser.add_argument("--email", required=True)
    user_parser.set_defaults(func=add_user)

    list_users_parser = subparsers.add_parser("list-users")
    list_users_parser.set_defaults(func=list_users)

    project_parser = subparsers.add_parser("add-project")
    project_parser.add_argument("--user", required=True)
    project_parser.add_argument("--title", required=True)
    project_parser.add_argument("--description", required=True)
    project_parser.add_argument("--due-date", required=True)
    project_parser.set_defaults(func=add_project)

    list_project_parser = subparsers.add_parser("list-projects")
    list_project_parser.add_argument("--user")
    list_project_parser.set_defaults(func=list_projects)

    task_parser = subparsers.add_parser("add-task")
    task_parser.add_argument("--project-id", required=True)
    task_parser.add_argument("--title", required=True)
    task_parser.add_argument("--assigned-to", required=True)
    task_parser.set_defaults(func=add_task)

    list_task_parser = subparsers.add_parser("list-tasks")
    list_task_parser.set_defaults(func=list_tasks)

    complete_task_parser = subparsers.add_parser("complete-task")
    complete_task_parser.add_argument("--task-id", required=True, type=int)
    complete_task_parser.set_defaults(func=complete_task)

    return parser

if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()