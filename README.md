# Webshop-Backend

A brief description of the project: What does it do? What is its purpose? (e.g., "A web application for task management.")

---

## 🚀 Features

- **Feature 1:** ...

---

## 🛠️ Prerequisites

Before starting the project, ensure you have the following software installed:

- [Python 3.13+](https://www.python.org/downloads/)
- [Django 4.x](https://www.djangoproject.com/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- Optional: [Virtualenv](https://virtualenv.pypa.io/)
- Optional: [PyCharm IDE](https://www.jetbrains.com/de-de/pycharm/download/?section=windows)

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Group-8-Cloud-Computing-Project/Webshop-Backend.git

cd repository
```
### 2. Start the Development Server
```bash
python manage.py runserver
```
The server will be available at http://127.0.0.1:8000.

## 🗂️ Project Structure
The following is an overview of the project's structure:

```plaintext
Backend/
├── .venv/              # Virtual environment directory (stores dependencies isolated for the project).
├── Backend/            # The actual Python package for the project.
│   ├── __init__.py     # Marks the directory as a Python package.
│   ├── asgi.py         # Entry point for the ASGI-compatible web servers to serve your project.
│   ├── settings.py     # Project settings/configuration file.
│   ├── urls.py         # URL routing for the project.
│   └── wsgi.py         # Entry point for WSGI-compatible web servers to serve your project.
├── templates/          # Directory for HTML templates used in rendering views.
├── WebshopBackend/     # Django app directory for the Webshop functionality.
│   ├── migrations/     # Database migrations for the app.
│   ├── __init__.py     # Marks the directory as a Python package.
│   ├── admin.py        # Configuration for the Django admin interface.
│   ├── apps.py         # App-specific configuration file.
│   ├── models.py       # Defines the data models (database structure) for the app.
│   ├── tests.py        # Test cases for the app.
│   └── views.py        # Handles requests and responses for the app.
├── db.sqlite3          # SQLite database file (default database for Django projects).
└── manage.py           # Main Django management script (used for running commands like runserver, migrate, etc.).
```

## 🧪 Running Tests
```bash
python manage.py test
```

## 📝 Useful Commands
- Create a Superuser (Admin):
```bash
python manage.py createsuperuser
```
- Generate a Database Migration File:
```bash
python manage.py makemigrations
```
- Collect Static Files (for deployment):
```bash
python manage.py collectstatic
```
- Create and Activate a Virtual Environment
    1. Linux/macOS:
    ```bash
    python3 -m venv venv 
    source venv/bin/activate
    ```
    2. Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
- Apply Database Migrations
```bash
python manage.py migrate
```
