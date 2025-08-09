# Summative Lab 7

This lab revolves around a command line tool, allowing you to manage users, projects, and tasks stored in JSON files.

# Commands

```bash
python3 lib/cli_tool.py add-user --name "Tester" --email "tester@example.com"
[Adds a user to the users.json file]

python3 lib/cli_tool.py list-users
[Lists all users in the users.json file]

python3 lib/cli_tool.py add-project --user "Tester" --title "Test Project" --description "Project for testing" --due-date "2025-08-09"
[Creates a project for the user listed above, and adds it to the projects.json file]

python3 lib/cli_tool.py list-projects
[Lists all projects in the project.json file]

python3 lib/cli_tool.py list-projects --user "Tester"
[Lists all projects for the user with the name listed above]

python3 lib/cli_tool.py add-task --project-id "1" --title "Testing" --assigned-to "1"
[Creates a task for the project with the id listed above, assigned to the user with the id listed, and adds it to the tasks.json file]

python3 lib/cli_tool.py list-tasks
[Lists all tasks in the tasks.json file]

python3 lib/cli_tool.py complete-task --task-id 1
[Marks the task with the id listed above as complete]
```
