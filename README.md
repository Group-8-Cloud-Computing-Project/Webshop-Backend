# 🌐 Backend Development Branch

## 📝 Overview
This repository contains the backend development code for the **Three-Tier Webshop Demo Application** as part of the Cloud Computing project for WiSe2024. The project demonstrates a scalable and high-availability architecture using modern cloud services and technologies.

The demo focuses on:
- A dynamic **Web Frontend** for the shop.
- A robust **Middleware** with REST API capabilities.
- A reliable **Storage Backend** for structured (relational/NoSQL) and unstructured (BLOB) data.

## 🏗️ Architecture
The application follows a **Three-Tier Architecture**:
1. **Presentation Tier (Frontend)**:  
   A dynamic user interface implemented using a modern JavaScript framework (e.g., React). It interacts with the backend via REST APIs to display products, manage shopping carts, and handle checkouts.

2. **Application Tier (Middleware)**:  
   The business logic layer implemented in **Python 3** using Django or Flask. It provides REST API endpoints for managing products, orders, inventory, and notifications.

3. **Data Tier (Storage Backend)**:  
   - A relational or NoSQL database for storing structured data such as products, orders, and inventory.
   - A BLOB storage service for unstructured data like product images.


## ✨ Features
### Frontend:
- Product catalog with images, descriptions, and prices.
- Search and filter functionality.
- Shopping cart and checkout process with responsive design.

### Middleware:
- CRUD operations for products and orders.
- Inventory management and email notifications (mocked).
- RESTful APIs for seamless frontend-backend communication.

### Database:
- Tables for product, order, and inventory management.
- BLOB storage for handling large unstructured data.


## ☁️ Cloud Service Provider (CSP)
The chosen CSP is determined by group-specific guidelines. Services include:
- **Compute Instances**: Hosting frontend and backend components.
- **Database Solutions**: Relational or NoSQL databases.
- **Storage Solutions**: For BLOBs and backups.
- **Load Balancers**: Ensuring high availability and scalability.

## 🗂️ Project Structure
The following is an overview of the project's structure:

```plaintext
Backend/
├── api/            # The actual Python package for the project.
│   ├── __init__.py     # Marks the directory as a Python package.
│   ├── asgi.py         # Entry point for the ASGI-compatible web servers to serve your project.
│   ├── settings.py     # Project settings/configuration file.
│   ├── urls.py         # URL routing for the project.
│   └── wsgi.py         # Entry point for WSGI-compatible web servers to serve your project.
├── webshop/     # Django app directory for the Webshop functionality.
│   ├── migrations/     # Database migrations for the app.
│   ├── __init__.py     # Marks the directory as a Python package.
│   ├── admin.py        # Configuration for the Django admin interface.
│   ├── apps.py         # App-specific configuration file.
│   ├── models.py       # Defines the data models (database structure) for the app.
│   ├── serializers.py  # Serialization of data
│   ├── tests.py        # Test cases for the app.
│   └── views.py        # Handles requests and responses for the app.
├── .gitignore          # Files that are excluded from Git tracking.
├── README.md           # This documentation.
└── manage.py           # Main Django management script (used for running commands like runserver, migrate, etc.).
```

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Group-8-Cloud-Computing-Project/Webshop-Backend.git

cd repository
```
### 2. Dependencies

1. **Python 3.8+**: Django requires Python 3.8 or later.
Check with:
```bash
python --version
```
2. **Pip**: Python’s package manager (comes pre-installed with Python).
Check with:
```bash
pip --version
```
3. **Virtualenv** (recommended): Creates isolated environments to avoid dependency conflicts.
Install (if not already installed):
```bash
pip install virtualenv
```

4. **The core packages for Django and REST API development:**
```bash
pip install django djangorestframework
```

### 3. Start the Development Server
```bash
python manage.py runserver
```
The server will be available at http://127.0.0.1:8000.

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
- Apply Database Migrations
```bash
python manage.py migrate
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
