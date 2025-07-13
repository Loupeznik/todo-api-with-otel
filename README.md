# TODO API with OTEL

This repository contains a FastAPI application that integrates OpenTelemetry for distributed tracing and logging. The application provides endpoints for user login/registration and task management, with instrumentation to capture performance metrics and logs.

## Running the Application

To run the application, you can use Docker. The Dockerfile is set up to build the application image with all necessary dependencies. The app can be run with docker compose:

```bash
cp .env.example .env
docker compose up --build
```

## Database

Database is setup automatically and migrations are done via Alembic. The migrations are applied on app startup.

You can create migrations manually and apply them by running the following commands when the application is running with Docker Compose:

```bash
docker-compose exec web alembic revision --autogenerate -m "<MIGRATION_NAME>"
docker-compose exec web alembic upgrade head
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
