# 🌐 Website Uptime Monitoring (FastAPI + SQLModel + Alembic)

This project is a **Website Uptime Monitoring System** built using **FastAPI**, **SQLModel**, **Alembic**, and **SQLite**.  
It periodically checks registered websites' availability, measures their response time, and protects against **SSRF attacks**.

---

## 🚀 Features

✅ Add, List, and Update websites  
✅ Manual and automatic (background) uptime checks  
✅ Response time tracking (in milliseconds)  
✅ SSRF (Server-Side Request Forgery) Protection  
✅ URL normalization (auto adds https:// if missing)  
✅ Configurable check intervals per website  
✅ Fully asynchronous (async/await everywhere)  
✅ Database migration support with Alembic  
✅ FastAPI interactive documentation (Swagger UI /PostMAN)

---

## 🧠 Project Structure

```
WebsiteURL_Monitor/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routers/
│   │       │   └── websites.py
│   │       └── schemas/
│   │           └── website.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── website.py
│   └── utils/
│       ├── normalization.py
│       ├── scheduler.py
│       └── ssrf_guard.py
│
├── migrations/
│   └── versions/
│
├── main.py
├── alembic.ini
└── README.md
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone <your_repo_url>
cd WebsiteURL_Monitor
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate   # On Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> Example dependencies:
>
> - fastapi
> - sqlmodel
> - httpx
> - alembic
> - aiosqlite
> - pydantic-settings
> - uvicorn

---

## 🛠️ Database Setup (Alembic)

1. Initialize Alembic (if not already done)

   ```bash
   alembic init migrations
   ```

2. Edit **alembic.ini** → set:

   ```ini
   sqlalchemy.url = sqlite:///./websites.db
   ```

3. Edit **migrations/env.py** → import your models:

   ```python
   from app.models.website import Website, WebsiteCheck
   from app.core.database import DATABASE_URL
   target_metadata = SQLModel.metadata
   ```

4. Generate Migrations:

   ```bash
   alembic revision --autogenerate -m "initial"
   ```

5. Apply Migrations:
   ```bash
   alembic upgrade head
   ```

---

## 🧩 Environment Variables

Create a `.env` file in project root:

```env
DATABASE_URL=sqlite+aiosqlite:///./websites.db
GLOBAL_CHECK_INTERVAL=30
CHECK_CONCURRENCY=10
```

---

## 🧠 Core Components Explained

### 🔹 main.py

- Starts the FastAPI app
- Runs database initialization and background scheduler
- Cleans up gracefully on shutdown

### 🔹 Background Scheduler (`app/utils/scheduler.py`)

- Periodically checks all active websites
- Skips sites checked recently
- Stores the latest status in `website_checks` table
- Runs every `GLOBAL_CHECK_INTERVAL` seconds

### 🔹 SSRF Protection (`app/utils/ssrf_guard.py`)

- Validates host IPs to ensure they’re public
- Blocks requests to private, loopback, or reserved IPs

### 🔹 URL Normalization (`app/utils/normalization.py`)

- Ensures URLs are properly formatted
- Adds `https://` if missing
- Removes trailing slashes

### 🔹 CRUD Operations (`app/api/v1/routers/websites.py`)

- `POST /api/v1/websites/` → Add website
- `GET /api/v1/websites/` → List websites
- `GET /api/v1/websites/{id}` → Get single website
- `PATCH /api/v1/websites/{id}` → Update website
- `POST /api/v1/websites/{id}/check` → Run manual check

---

## 🧪 Testing Using Postman

| Method | Endpoint                      | Description                 |
| ------ | ----------------------------- | --------------------------- |
| POST   | `/api/v1/websites/`           | Add a website               |
| GET    | `/api/v1/websites/`           | List all websites           |
| GET    | `/api/v1/websites/{id}`       | Get details of one website  |
| PATCH  | `/api/v1/websites/{id}`       | Update a website            |
| POST   | `/api/v1/websites/{id}/check` | Perform manual uptime check |

**Sample Request:**

```json
POST /api/v1/websites/
{
  "url": "https://example.com",
  "name": "Example",
  "check_interval_sec": 60
}
```

**Sample Response:**

```json
{
  "id": 1,
  "url": "https://example.com",
  "name": "Example",
  "is_active": true,
  "check_interval_sec": 60,
  "created_at": "2025-10-22T08:00:00Z",
  "updated_at": "2025-10-22T08:00:00Z"
}
```

---

## 🧰 Run the Server

```bash
uvicorn main:app --reload
```

Visit:

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧹 Optional Cleanup

To reset your database:

```bash
rm websites.db
alembic downgrade base
alembic upgrade head
```

---

## 🧩 Tech Stack

| Layer             | Technology     |
| ----------------- | -------------- |
| Backend Framework | FastAPI        |
| ORM               | SQLModel       |
| DB                | SQLite (async) |
| HTTP Client       | httpx          |
| Scheduler         | asyncio loop   |
| Migrations        | Alembic        |
| Validation        | Pydantic       |

---

## 👨‍💻 Author

**Developed by:** Shahzada Rizwan Ali
**Organization:** Synares Systems  
**Date:** Week 6 Task  
**Purpose:** Website Uptime Monitoring Tool with SSRF Protection

---

## 🧾 License

This project is licensed under the **MIT License** — feel free to modify and use it.

---

### ✅ Next Steps

- [ ] Add pytest tests for all endpoints
- [ ] Add Docker support
- [ ] Add frontend dashboard for visualization
