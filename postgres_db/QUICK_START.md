# ⚡ Quick Start Guide

## 🚀 Start Database & Open in Chrome (3 Commands)

```bash
cd postgres_db
./start.sh
./open_chrome.sh
```

That's it! pgAdmin will open in Chrome automatically.

---

## 📋 All Available Scripts

| Script | What It Does |
|--------|--------------|
| `./start.sh` | Start PostgreSQL and pgAdmin |
| `./stop.sh` | Stop PostgreSQL and pgAdmin |
| `./restart.sh` | Restart both services |
| `./status.sh` | Check if services are running |
| `./open_chrome.sh` | Open pgAdmin in Chrome browser |

---

## 🌐 Access pgAdmin

**URL:** http://localhost:5050

**Login:**
- Email: `admin@admin.com`
- Password: `admin`

---

## 🔗 Connect to Database in pgAdmin

1. Right-click **"Servers"** → **"Register"** → **"Server"**
2. **Name:** `FastAPI Local DB`
3. **Connection:**
   - Host: `postgres`
   - Port: `5432`
   - Database: `fastapi_db`
   - Username: `postgres`
   - Password: `postgres123`
4. Click **"Save"**

---

## 📊 View Tables

1. Expand: **FastAPI Local DB** → **Databases** → **fastapi_db** → **Schemas** → **public** → **Tables**
2. Right-click **"users"** → **"View/Edit Data"** → **"All Rows"**

---

## 💡 Daily Workflow

```bash
# Morning: Start database
cd postgres_db && ./start.sh

# View tables in Chrome
./open_chrome.sh

# Evening: Stop database
./stop.sh
```

---

## 🎯 That's It!

You're ready to view and manage your database tables in Chrome! 🚀

