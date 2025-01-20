# Backend Development Branch

## Overview
This repository contains the backend development code for the **Three-Tier Webshop Demo Application** as part of the Cloud Computing project for WiSe2024. The project demonstrates a scalable and high-availability architecture using modern cloud services and technologies.

The demo focuses on:
- A dynamic **Web Frontend** for the shop.
- A robust **Middleware** with REST API capabilities.
- A reliable **Storage Backend** for structured (relational/NoSQL) and unstructured (BLOB) data.

## Architecture
The application follows a **Three-Tier Architecture**:
1. **Presentation Tier (Frontend)**:  
   A dynamic user interface implemented using a modern JavaScript framework (e.g., React). It interacts with the backend via REST APIs to display products, manage shopping carts, and handle checkouts.

2. **Application Tier (Middleware)**:  
   The business logic layer implemented in **Python 3** using Django or Flask. It provides REST API endpoints for managing products, orders, inventory, and notifications.

3. **Data Tier (Storage Backend)**:  
   - A relational or NoSQL database for storing structured data such as products, orders, and inventory.
   - A BLOB storage service for unstructured data like product images.


## Features
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


## Cloud Service Provider (CSP)
The chosen CSP is determined by group-specific guidelines. Services include:
- **Compute Instances**: Hosting frontend and backend components.
- **Database Solutions**: Relational or NoSQL databases.
- **Storage Solutions**: For BLOBs and backups.
- **Load Balancers**: Ensuring high availability and scalability.


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
