# Student Management System

A robust, scalable Student Management API built with Django and Django REST Framework (DRF). This project provides a secure backend for managing students, courses, authentication, and profile images, with integration for Cloudinary image hosting and JWT-based authentication.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Usage](#api-usage)
- [Authentication](#authentication)
- [Profile Image Uploads](#profile-image-uploads)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **JWT Authentication**: Secure login and registration for students.
- **Student & Course Management**: CRUD operations for students and courses.
- **Profile Image Uploads**: Store and serve profile images via Cloudinary.
- **Password Management**: Change, reset, and forgot password flows.
- **Site Restriction**: API access limited to specific domains.
- **Extensible Models**: Custom user model for students.
- **RESTful API**: Built with Django REST Framework.
- **MySQL/SQLite Support**: Easily switchable database backend.

---

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: MySQL (default), SQLite (for development)
- **Authentication**: JWT (via `djangorestframework-simplejwt`)
- **Image Hosting**: Cloudinary
- **Other**: Docker (optional), Cloudinary Python SDK

---

## Architecture

- **students/**: Core app containing models, serializers, views, and URLs for student and course management.
- **Authentication**: Custom user model (`Student`) with email as username.
- **Profile Images**: Managed via Cloudinary, with URLs stored in the database.
- **API Endpoints**: All major operations exposed via RESTful endpoints.

---

## Installation

```bash
git clone https://github.com/your-username/student_management.git
cd Student_Management-_System
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

---

## Configuration

1. **Database**:  
   Update `settings.py` for MySQL or use SQLite for local development.

2. **Cloudinary**:  
   Add your Cloudinary credentials to `settings.py`:
   ```python
   CLOUDINARY = {
       'cloud_name': 'your_cloud_name',
       'api_key': 'your_api_key',
       'api_secret': 'your_api_secret'
   }
   ```

3. **JWT**:  
   Configure JWT settings in `settings.py` as needed.

4. **Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

---

## API Usage

### Authentication

- **Register**:  
  `POST /api/register/`  
  Fields: `email`, `first_name`, `last_name`, `password`, etc.

- **Login**:  
  `POST /api/login/`  
  Fields: `email`, `password`  
  Returns: JWT tokens

### Students

- **List Students**:  
  `GET /api/students/`

- **Retrieve Student**:  
  `GET /api/students/{id}/`

- **Update Student**:  
  `PUT /api/students/{id}/`

- **Delete Student**:  
  `DELETE /api/students/{id}/`

### Courses

- **List Courses**:  
  `GET /api/courses/`

- **Create Course**:  
  `POST /api/courses/`

### Profile Images

- **Upload/Update Profile Image**:  
  `POST /api/profile-image/`  
  Fields: `student`, `image` (file)  
  Returns: `image_url` (Cloudinary link)

---

## Authentication

All protected endpoints require JWT authentication.  
Include your token in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

---

## Profile Image Uploads

- Upload images via the `/api/profile-image/` endpoint.
- Images are stored in Cloudinary; the API returns a secure URL.
- Only one profile image per student (enforced by the model).

---

## Testing

Run unit tests with:

```bash
python manage.py test
```

---

## Deployment

- Configure allowed hosts and production database in `settings.py`.
- Set up environment variables for secrets.
- Use a production-ready server (e.g., Gunicorn, Nginx).
- Optionally, deploy with Docker.

---

## Troubleshooting

- **Image Not Displaying**: Ensure images are uploaded to Cloudinary and the `image_url` is a valid Cloudinary link.
- **IntegrityError on ProfileImage**: Only one profile image per student; update existing instead of creating new.
- **JWT Issues**: Check token expiration and settings.

---

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/fooBar`).
3. Commit your changes.
4. Push to the branch (`git push origin feature/fooBar`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

**For questions or support, open an issue or contact the maintainer.**

