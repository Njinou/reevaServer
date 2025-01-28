Here’s the formatted Markdown for your documentation:

```markdown
# Documentation for Django API Project

## 1. Getting Started

### Prerequisites
Ensure the following are installed:

- **Python 3.x+**
- **Django 4.x+**
- **Django REST Framework (DRF) 3.x+**
- **SQLite** or any database configured in `settings.py`.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install Dependencies**:
   Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Apply Migrations**:
   Set up the database schema:
   ```bash
   python manage.py migrate
   ```

4. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## 2. API Endpoints

### Base URL
The base URL for all API endpoints is:
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

- **POST** `/api/token/`  
  Obtain a JWT access token and refresh token using valid credentials.

- **POST** `/api/token/refresh/`  
  Refresh your JWT access token using the refresh token.

- **POST** `/api/login/`  
  Same as `/api/token/`, this endpoint allows you to log in and get a token.

### Project Management Endpoints

- **GET** `/projects/`  
  List all projects owned by the authenticated user.

- **POST** `/projects/`  
  Create a new project (with the owner automatically assigned).

- **GET** `/projects/{id}/`  
  Get details of a specific project by ID.

- **PUT** `/projects/{id}/`  
  Update project details by ID.

- **DELETE** `/projects/{id}/`  
  Delete a project by ID.

- **GET** `/projects/analytics/`  
  Get project analytics for the authenticated user (e.g., total projects, completed tasks, overdue tasks).

### Task Management Endpoints

- **GET** `/tasks/`  
  List tasks related to projects owned by the authenticated user.

- **POST** `/tasks/`  
  Create a new task for a project.

- **GET** `/tasks/{id}/`  
  Get details of a specific task by ID.

- **PUT** `/tasks/{id}/`  
  Update task details by ID.

- **DELETE** `/tasks/{id}/`  
  Delete a task by ID.

### User Management Endpoints

- **GET** `/users/`  
  List all users.

- **POST** `/users/`  
  Create a new user (password must meet the strength criteria).

---

## 3. URL Configuration

Here’s a breakdown of your project’s URL configuration based on the provided `urls.py` file.

### Admin Dashboard

- **URL**: `/admin/`  
  Access the Django Admin dashboard to manage your projects, tasks, and users.  
  You can log in using the superuser credentials created earlier.

### API Endpoints

- **URL Prefix**: `/api/`  
  All your API endpoints are prefixed with `/api/`.

#### Authentication Endpoints:
- **Login**:
  - **POST** `/api/token/` - Obtain a JWT access token and refresh token.
  - **POST** `/api/token/refresh/` - Refresh the JWT access token using the refresh token.
  - **POST** `/api/login/` - Alias to `/api/token/` for logging in.

#### Core API Endpoints:
- Project and Task Endpoints are included via:
  ```python
  path('api/', include('core.urls'))
  ```

### Django REST Framework Authentication

You are using **JWT authentication** for the API:

- **Obtain Token**: Use the `/api/token/` endpoint by providing valid user credentials (username and password) to receive the access token and refresh token.

**Example request** to obtain a token:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ -d "username=<your-username>&password=<your-password>"
```

**Response**:
```json
{
  "access": "<JWT-access-token>",
  "refresh": "<JWT-refresh-token>"
}
```

---

## 4. Models

### Project Model

Represents a project, which contains multiple tasks and is owned by a user.

- **Fields**:
  - `owner`: ForeignKey to `User`, represents the project owner.
  - `title`: The name of the project.
  - `description`: A brief description of the project.
  - `status`: The status of the project (e.g., `'active'`, `'on_hold'`, `'completed'`).
  - `deadline`: The deadline for the project.
  - `created_at`: Timestamp when the project was created.
  - `updated_at`: Timestamp when the project was last updated.

### Task Model

Represents a task, associated with a project, and assigned to a user.

- **Fields**:
  - `project`: ForeignKey to `Project`, representing which project the task belongs to.
  - `assignee`: ForeignKey to `User`, representing the user assigned to complete the task.
  - `title`: The title of the task.
  - `description`: A brief description of the task.
  - `status`: The status of the task (e.g., `'todo'`, `'in_progress'`, `'done'`).
  - `priority`: Integer representing the task's priority.
  - `due_date`: The task's due date.
  - `created_at`: Timestamp when the task was created.
  - `updated_at`: Timestamp when the task was last updated.

---

## 5. Usage Example

### Creating a New Project

- **POST** `/projects/`

**Request body**:
```json
{
  "title": "Website Redesign",
  "description": "A project to redesign the company website.",
  "status": "active",
  "deadline": "2025-12-31"
}
```

**Response**:
```json
{
  "id": 1,
  "owner": 1,
  "title": "Website Redesign",
  "description": "A project to redesign the company website.",
  "status": "active",
  "deadline": "2025-12-31",
  "created_at": "2025-01-28T10:00:00Z",
  "updated_at": "2025-01-28T10:00:00Z"
}
```

### Creating a New Task

- **POST** `/tasks/`

**Request body**:
```json
{
  "project": 1,
  "assignee": 2,
  "title": "Design Homepage",
  "status": "todo",
  "priority": 2,
  "due_date": "2025-02-01"
}
```

**Response**:
```json
{
  "id": 1,
  "project": 1,
  "assignee": 2,
  "title": "Design Homepage",
  "status": "todo",
  "priority": 2,
  "due_date": "2025-02-01",
  "created_at": "2025-01-28T10:00:00Z",
  "updated_at": "2025-01-28T10:00:00Z"
}
```

---

## 6. Admin Dashboard (Optional)

Access the Django Admin dashboard at:
```
http://127.0.0.1:8000/admin/
```

Log in using the superuser credentials you created.

---
