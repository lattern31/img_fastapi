## Image Processing API

This API built with FastAPI provides a robust solution for handling and manipulating images, utilizing asynchronous operations and a microservice architecture for optimal performance.

### Key Features

- **Secure Authentication:** Implement robust authentication using JWT (JSON Web Tokens) through FastAPI-Users, ensuring secure access to user-specific image resources.
- **Asynchronous Database Interaction:** Leverage the power of asynchronous SQLAlchemy to interact with the PostgreSQL database efficiently, enabling concurrent handling of image uploads, edits, and retrievals.
- **Background Task Processing:** Utilize Celery with Redis as a message broker to offload time-consuming tasks like image processing, thumbnail generation, and email sending to background workers, keeping the API responsive.
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

- [ ] Caching on redis
- [ ] Migrations via alembic
- [ ] Searching, filtering, pagination of images
- [ ] Tambnails via celery
- [ ] Tests on pytest

### Getting Started

1. **Clone the repository:** `git clone https://github.com/lattern31/img_fastapi`
2. Set up environment variables:
    * Create a `.env` file based on the provided `.env.example`.
    * Fill in the required values for database credentials, API secrets, and other configurations.
3. Start the application:
    * `make`
4. View logs:
    * `make logs`
5. Stop and remove containers:
    * `make down`
This will start the API, Celery worker, and Flower (for monitoring Celery tasks). You can then access the API documentation at `/api/docs` (e.g., http://localhost:8000/api/docs).

### Contributing
Contributions are welcome! Please feel free to open issues for bug reports, feature requests, or any questions you may have. For code contributions, fork the repository and submit a pull request.