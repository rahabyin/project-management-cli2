# 🚀 Project Management CLI Tool

A Python-based Command-Line Interface (CLI) application that helps teams manage **users**, **projects**, and **tasks** directly from the terminal.

This project was developed as part of a Python Software Engineering lab to demonstrate practical use of:

* Object-Oriented Programming (OOP)
* Command-Line Interfaces (CLI)
* JSON Data Persistence
* File I/O Operations
* Modular Project Design
* External Python Packages
* Automated Testing with Pytest
* Git & GitHub Workflow

---

# 📌 Overview

Managing projects often requires tracking:

* Team members
* Project assignments
* Task progress
* Completion status

This CLI application provides a lightweight project management system where administrators can create users, assign projects, create tasks, and track project progress using simple terminal commands.

All project data is automatically saved locally using JSON, allowing information to persist between sessions.

---

# ✨ Features

### 👤 User Management

* Create new users
* View all users
* Store user information persistently

### 📁 Project Management

* Create projects
* Assign projects to users
* View all projects
* View projects belonging to a specific user
* Search projects by keyword

### ✅ Task Management

* Add tasks to projects
* Assign tasks to users
* Mark tasks as complete
* View project tasks

### 💾 Data Persistence

* Save data automatically to JSON
* Reload existing data when the application starts

### 🎨 Improved Terminal Experience

* Uses the Rich package for cleaner terminal output
* Clear success and error messages
* User-friendly CLI help menus

---

# 🛠 Technologies Used

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python 3.10+ | Core programming language |
| argparse     | CLI command handling      |
| json         | Data storage              |
| os           | File operations           |
| Rich         | Enhanced terminal output  |
| Pytest       | Unit testing              |

---

# 📂 Project Structure

```text
project-management-cli/
│
├── data/
│   └── tracker_data.json
│
├── models/
│   ├── person.py
│   ├── user.py
│   ├── project.py
│   └── task.py
│
├── utils/
│   └── storage.py
│
├── tests/
│   ├── test_models.py
│   └── test_storage.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/project-management-cli.git
```

```bash
cd project-management-cli
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 CLI Commands

## Display Help

```bash
python main.py --help
```

---

## Add a User

```bash
python main.py add-user --name "Alex" --email "alex@example.com"
```

---

## List All Users

```bash
python main.py list-users
```

---

## Add a Project

```bash
python main.py add-project \
--user "Alex" \
--title "CLI Tool" \
--description "Build a project tracker" \
--due-date "2026-07-01"
```

---

## List All Projects

```bash
python main.py list-projects
```

---

## List Projects for a User

```bash
python main.py list-projects --user "Alex"
```

---

## Add a Task

```bash
python main.py add-task \
--project "CLI Tool" \
--title "Implement add-task" \
--assigned-to "Alex"
```

---

## View Tasks

```bash
python main.py list-tasks --project "CLI Tool"
```

---

## Complete a Task

```bash
python main.py complete-task \
--project "CLI Tool" \
--task-id 1
```

---

## Search Projects

```bash
python main.py search-projects --keyword "CLI"
```

---

# 🧪 Running Tests

Run the complete test suite:

```bash
python3 -m pytest
```

or

```bash
python3 -m pytest
```

Example output:

```text
====== 6 passed in 0.02s ======
```

---

# 💾 Data Storage

All application data is stored locally in:

```text
data/tracker_data.json
```

The application automatically creates and updates this file whenever changes are made.

---

# 🏗 Object Relationships

This project demonstrates common OOP relationships:

### One-to-Many

```text
User
 ├── Project 1
 ├── Project 2
 └── Project 3
```

A single user can own multiple projects.

### One-to-Many

```text
Project
 ├── Task 1
 ├── Task 2
 └── Task 3
```

A project can contain multiple tasks.

---

# 🐞 Testing & Debugging

The project was tested using Pytest to verify:

* User creation
* Project creation
* Task creation
* JSON persistence
* Data loading and saving

The application also includes input validation and user-friendly error handling.

---

# 🔄 Git Workflow

This project follows a Git-based development workflow:

1. Create project structure
2. Commit changes regularly
3. Push updates to GitHub
4. Use feature branches for enhancements
5. Merge completed work into the main branch

Example:

```bash
git checkout -b feature/add-task-search
git add .
git commit -m "Add project search feature"
git push origin feature/add-task-search
```

---

# 📈 Future Improvements

Potential future enhancements include:

* User authentication
* Project deadlines and reminders
* Task priorities
* Contributor management
* CSV export support
* Database integration (SQLite/PostgreSQL)
* Interactive Rich dashboards

---

# 👨‍💻 Author

**Rahab Wanja**

---

# 📄 License

This project was created for educational purposes as part of a Python Software Engineering coursework project.