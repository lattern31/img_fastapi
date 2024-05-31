## Image Processing API

This API built with FastAPI provides a robust solution for handling and manipulating images, utilizing asynchronous operations and onion architecture for optimal performance.

### Key Features

- **Secure Authentication:** Implement authentication using JWT (JSON Web Tokens) through FastAPI-Users, ensuring secure access to user-specific image resources.
- **Asynchronous Database Interaction:** Leverage the power of asynchronous SQLAlchemy to interact with the PostgreSQL database efficiently. Concurrent handling of image uploads, edits, and retrievals.
- **Background Task Processing:** Utilize Celery with Redis as a message broker to offload time-consuming tasks like image processing and email sending to background workers, keeping the API responsive.
- **Efficient Containerization:** Easily deploy and scale the application using Docker and Docker Compose, simplifying environment setup and ensuring consistency across different deployments.

### Tech Stack

- **Framework:** FastAPI
- **Authentication:** FastAPI-Users
- **ORM:** Async SQLAlchemy
- **Database:** PostgreSQL
- **Background Tasks:** Celery, Redis, Flower
- **Containerization:** Docker, Docker Compose
- **Image Processing:** Pillow (PIL)
- **Email Sending:** smtplib

### Roadmap

- [x] Tests on pytest
- [ ] Caching on redis
- [ ] Migrations via alembic
- [ ] Searching, filtering, pagination of images
- [ ] Thumbnails via celery

### Getting Started

1. Set up environment variables:
    * Create a `.env` file based on the provided `.env.example`.
    * Fill in the required values for database credentials, API secrets, and other configurations.
2. Start the application:
    * `make`
3. View logs:
    * `make logs`
4. Stop and remove containers:
    * `make down`

You can then access the API documentation at `/api/docs` (e.g., http://localhost:8001/api/docs).
