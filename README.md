# Job Board Platform

A scalable **Job Board Platform** designed for managing job postings, applications, and role-based access control. Built with **Django** and **PostgreSQL**, this backend provides secure APIs and efficient job search capabilities, with room for frontend integration in the future.

[![API Documentation](https://img.shields.io/badge/API-Documentation-blue)](/api/docs)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Role-Based Access Control](#role-based-access-control)
- [Performance & Optimization](#performance--optimization)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Job Posting Management**
  - Create, update, delete, and retrieve job postings.
  - Categorize jobs by industry, location, and type.

- **User & Admin Roles**
  - Admins can manage jobs and categories.
  - Users can browse jobs and manage applications.

- **Optimized Job Search**
  - Advanced filtering: location, category, type.
  - Indexed queries for large datasets.

- **API Documentation**
  - Interactive Swagger documentation hosted at `/api/docs`.

---

## Tech Stack

| Technology            | Purpose                                |
| --------------------- | -------------------------------------- |
| Django                | High-level Python framework            |
| Django REST Framework | API development & serialization        |
| PostgreSQL            | Relational database for jobs and users |
| JWT                   | Secure role-based authentication       |
| Swagger               | API documentation                      |

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip / virtualenv

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/solomonferede/job-board-platform.git
   cd job-board-platform/backend
   ```
2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Update database credentials, JWT secret, etc.

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Run the server**

   ```bash
   python manage.py runserver
   ```

7. **Access API docs**
   ```
   http://127.0.0.1:8000/api/docs/
   ```

---

## API Endpoints

### Jobs

- **GET** `/jobs/` – List jobs with filters
- **POST** `/jobs/` – Create a job (admin only)
- **GET** `/jobs/{id}/` – Retrieve job details
- **PUT** `/jobs/{id}/` – Update job (admin only)
- **DELETE** `/jobs/{id}/` – Delete job (admin only)

### Categories

- **GET** `/categories/` – List categories
- **POST** `/categories/` – Create category (admin only)

### Applications

- **GET** `/applications/` – List user's applications
- **POST** `/applications/` – Apply for a job
- **PUT** `/applications/{id}/` – Update application status (admin only)

---

## Database Schema

### Main Entities

- **User**
  - id, username, email, role (USER / ADMIN), etc.

- **Job**
  - id, title, description, location, category_id, created_by, created_at, etc.

- **Category**
  - id, name, description

- **Application**
  - id, job_id, user_id, status, applied_at

### Relationships:

- User (1) → Application (many)
- Job (1) → Application (many)
- Category (1) → Job (many)

---

## Role-Based Access Control

| Role  | Permissions                                         |
| ----- | --------------------------------------------------- |
| Admin | Manage jobs & categories, update application status |
| User  | Browse jobs, create/manage own applications         |

JWT authentication ensures secure role verification across endpoints.

---

## Performance & Optimization

### Database Indexing

- Indexed fields: location, category_id, job_type, created_at

### Optimized Queries

- `select_related` / `prefetch_related` for joined tables
- Pagination for large result sets

### Search

- Filter by location, category, and job type efficiently

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "feat: add feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request
