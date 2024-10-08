# Post Machines Admin (post_machines_admin)

**Post Machines Admin** is a Django-based application for managing parcels and lockers in a post machine system. This system is designed to allow administrators to handle parcel deliveries, track statuses, and manage lockers. The project features an HTML-based frontend and supports both local SQLite and PostgreSQL databases (via Docker).

## Features

- Manage lockers and parcels.
- Track parcel statuses (delivered, pending, etc.).
- Admin interface for managing users and parcels.
- HTML frontend interface.
- Uses SQLite for local development.
- Uses PostgreSQL for production (Docker setup).

## Technologies Used

- **Django**: Python-based web framework.
- **HTML/CSS**: Frontend for the application.
- **SQLite**: Local database for development.
- **PostgreSQL**: Production database in Docker.
- **Docker**: Containerization of the app and PostgreSQL database.

## Running the Application with Docker Compose

The project includes a `docker-compose.yml` file for running the application and PostgreSQL database.

**Build and Start Containers:**
   ```bash
   docker-compose up --build
