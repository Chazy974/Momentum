## ✅ Release v0.1 – Task system functional

- Added SQLAlchemy models: `User`, `Task` with `due_date`
- Alembic migrations set up and working
- FastAPI endpoints: `GET /tasks`, `POST`, `PUT`, `DELETE`
- Frontend connected to API (CORS enabled)
- Tasks can be added and deleted from the UI

## 🔧 TODO

- [ ] Auth system (register/login)
- [ ] Link tasks to a logged-in user (`user_id`)
- [ ] Add due date field in frontend form
- [ ] Add task editing (PUT)
- [ ] Improve API validation & error responses
- [ ] Add unit tests (pytest)
- [ ] Deploy dev version (Render / Railway)
- [ ] UI: show due date and status (completed)
- [ ] Handle HTTP errors visually on frontend
