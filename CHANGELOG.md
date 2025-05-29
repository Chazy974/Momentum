# Changelog

## [v0.1] - 2025-05-29
### Added
- 🚀 Initial version of the Momentum backend
- ✅ FastAPI app with CORS enabled for frontend at `localhost:5173`
- 📦 CRUD API for tasks (`/tasks`):
  - `GET /tasks`: List all tasks
  - `POST /tasks`: Create a task
  - `PUT /tasks/{task_id}`: Update a task
  - `DELETE /tasks/{task_id}`: Delete a task
- 🧱 SQLAlchemy models for `User` and `Task` with `relationship()`
- 🗄️ PostgreSQL database support with `alembic` for migrations
- 📅 New `due_date` field added to `Task` model

### Changed
- N/A

### Fixed
- N/A
