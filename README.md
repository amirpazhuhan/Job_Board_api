# Job Board API

A REST API for job seekers and company owners. Users can create accounts, manage company profiles, publish and save jobs, and submit or review applications.

## Features

- JWT authentication with access and refresh tokens
- User profiles and password changes
- One company profile per owner
- Job creation, search, filtering, ordering, updates, and deletion
- Saved jobs
- Applications with resumes and company-side status updates
- OpenAPI schema and Swagger UI

## Tech stack

- Python and Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- drf-spectacular

## Setup

1. Create and activate a virtual environment.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root.

   ```env
   SECRET_KEY=replace-with-a-long-random-secret
   DEBUG=True
   DB_NAME=job_board
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Apply migrations and start the development server.

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

The API is served at `http://127.0.0.1:8000/`.

## Documentation

- Swagger UI: `/api/docs/`
- OpenAPI schema: `/api/schema/`

## Authentication

Register a user, then request a token pair:

```http
POST /api/auth/register/
POST /api/auth/token/
```

Use the access token on protected endpoints:

```http
Authorization: Bearer <access_token>
```

Refresh an expired access token with:

```http
POST /api/auth/token/refresh/
```

## API endpoints

| Area | Method | Endpoint | Purpose |
| --- | --- | --- | --- |
| Auth | POST | `/api/auth/register/` | Register a user |
| Auth | POST | `/api/auth/token/` | Obtain access and refresh tokens |
| Auth | POST | `/api/auth/token/refresh/` | Refresh an access token |
| Auth | GET, PUT, PATCH | `/api/auth/profile/` | View or update the current profile |
| Auth | PUT, PATCH | `/api/auth/change_password/` | Change the current password |
| Companies | GET, POST | `/api/companies/` | List companies or create a company |
| Companies | GET, PUT, PATCH, DELETE | `/api/companies/me/` | Manage the current user's company |
| Jobs | GET | `/api/jobs/` | List, search, filter, and order jobs |
| Jobs | POST | `/api/jobs/create/` | Create a job for the current company |
| Jobs | GET, PUT, PATCH, DELETE | `/api/jobs/{id}/` | View or manage a job |
| Saved jobs | POST, DELETE | `/api/jobs/{id}/save/` | Save or remove a saved job |
| Saved jobs | GET | `/api/jobs/saved/` | List saved jobs |
| Applications | GET | `/api/applications/` | List personal or company applications |
| Applications | POST | `/api/applications/{job_id}/apply/` | Apply to a job |
| Applications | GET, PUT, PATCH | `/api/applications/{id}/` | Company-side application review |
| Applications | GET, PUT, PATCH | `/api/applications/my/{id}/` | Manage a personal application |

## Job query parameters

`GET /api/jobs/` supports the following query parameters:

| Parameter | Example | Purpose |
| --- | --- | --- |
| `search` | `?search=python` | Search job title, description, and company name |
| `location` | `?location=Tehran` | Filter by location |
| `employment_type` | `?employment_type=full-time` | Filter by employment type |
| `min_salary_min` | `?min_salary_min=50000` | Minimum value for `salary_min` |
| `max_salary_min` | `?max_salary_min=100000` | Maximum value for `salary_min` |
| `min_salary_max` | `?min_salary_max=80000` | Minimum value for `salary_max` |
| `max_salary_max` | `?max_salary_max=150000` | Maximum value for `salary_max` |
| `ordering` | `?ordering=-salary_min` | Order by `salary_min` or `salary_max` |

## Tests

Run the test suite with:

```bash
python manage.py test
```

## Media uploads

Company logos and application resumes are saved under `media/` during development. Django serves them only while `DEBUG=True`; use object storage or a web server for media in production.

## Production notes

- Set a strong `SECRET_KEY` through environment variables.
- Set `DEBUG=False`.
- Configure `ALLOWED_HOSTS` for your deployment domain.
- Use a production email backend and media storage service.
