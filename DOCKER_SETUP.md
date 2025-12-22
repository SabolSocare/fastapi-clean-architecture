# 🐳 Docker PostgreSQL Setup

This guide shows you how to run PostgreSQL locally with Docker for your FastAPI backend.

---

## 📋 Prerequisites

### Check if Docker is installed
```bash
docker --version
docker-compose --version
```

### If Docker is not installed:
- **macOS:** Download from https://www.docker.com/products/docker-desktop
- **Linux:** `sudo apt-get install docker docker-compose` or `brew install docker docker-compose`
- **Windows:** Download from https://www.docker.com/products/docker-desktop

---

## 🚀 Quick Start

### 1. Start PostgreSQL with Docker
```bash
cd /Users/socaresabol/POC/vue_project/backend
docker-compose up -d
```

This will:
- Download PostgreSQL image (first time only)
- Start PostgreSQL on port 5432
- Start pgAdmin (web UI) on port 5050
- Create persistent volumes for data

### 2. Check if Database is Running
```bash
docker-compose ps
```

You should see:
```
NAME                IMAGE                  STATUS
fastapi_postgres    postgres:15-alpine    Up
fastapi_pgadmin     dpage/pgadmin4        Up
```

### 3. Test Database Connection
```bash
source venv/bin/activate
python test/test_db_connection.py
```

### 4. Start Your FastAPI App
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access Your Services
- **API Docs:** http://localhost:8000/docs
- **pgAdmin:** http://localhost:5050 (admin@admin.com / admin)
- **Database:** localhost:5432

---

## 🔧 Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose stop
```

### Stop and Remove Containers
```bash
docker-compose down
```

### Stop and Remove Everything (including data)
```bash
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs

# PostgreSQL only
docker-compose logs postgres

# Follow logs (real-time)
docker-compose logs -f postgres
```

### Restart Services
```bash
docker-compose restart
```

---

## 📊 Database Connection Details

| Setting | Value |
|---------|-------|
| Host | `localhost` |
| Port | `5432` |
| Database | `fastapi_db` |
| Username | `postgres` |
| Password | `postgres123` |

**Connection String:**
```
postgresql+psycopg://postgres:postgres123@localhost:5432/fastapi_db
```

---

## 🔍 Using pgAdmin (Optional)

pgAdmin is a web-based database management tool.

### 1. Access pgAdmin
Open: http://localhost:5050

### 2. Login
- **Email:** admin@admin.com
- **Password:** admin

### 3. Add Server Connection
1. Click "Add New Server"
2. **General Tab:**
   - Name: FastAPI Local DB
3. **Connection Tab:**
   - Host: postgres (or host.docker.internal on Mac/Windows)
   - Port: 5432
   - Database: fastapi_db
   - Username: postgres
   - Password: postgres123
4. Click "Save"

### 4. Browse Your Database
You can now see tables, run queries, and manage your database visually.

---

## 🗄️ Direct Database Access

### Using psql (if installed)
```bash
# Connect to database
psql -h localhost -U postgres -d fastapi_db

# Enter password: postgres123
```

### Using Docker exec
```bash
# Access PostgreSQL container
docker exec -it fastapi_postgres psql -U postgres -d fastapi_db
```

### Common SQL Commands
```sql
-- List all tables
\dt

-- Describe a table
\d users

-- Query users
SELECT * FROM users;

-- Create a test user
INSERT INTO users (email, username, hashed_password, is_active) 
VALUES ('test@example.com', 'testuser', 'hashed_password_here', true);

-- Exit
\q
```

---

## 🔄 Migrate from Supabase to Local

Your app is now configured for local PostgreSQL. The changes:

### Old (.env):
```env
DATABASE_URL=postgresql+psycopg://postgres:password@db.xxx.supabase.co:5432/postgres
```

### New (.env):
```env
DATABASE_URL=postgresql+psycopg://postgres:postgres123@localhost:5432/fastapi_db
```

---

## 📦 What's Included

### PostgreSQL Container
- **Image:** postgres:15-alpine (lightweight)
- **Port:** 5432
- **Data:** Persisted in Docker volume
- **Health Check:** Automatic readiness checks

### pgAdmin Container (Optional)
- **Image:** dpage/pgadmin4
- **Port:** 5050
- **Access:** http://localhost:5050

---

## 🧪 Test Everything

### 1. Test Docker is Running
```bash
docker-compose ps
```

### 2. Test Database Connection
```bash
python test/test_db_connection.py
```

### 3. Test DNS (should work with localhost)
```bash
python test/test_dns.py
```

### 4. Run Diagnostics
```bash
python test/diagnose_issue.py
```

### 5. Start the App
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔒 Change Database Password (Optional)

### 1. Update docker-compose.yml
Change `POSTGRES_PASSWORD: postgres123` to your desired password

### 2. Update .env
Update the DATABASE_URL with new password

### 3. Recreate Container
```bash
docker-compose down -v
docker-compose up -d
```

---

## 🐛 Troubleshooting

### Port 5432 Already in Use
```
Error: port is already allocated
```

**Solution:** Stop other PostgreSQL instances
```bash
# macOS/Linux
sudo lsof -i :5432
sudo kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "5433:5432"  # Use 5433 on host instead
```
Then update DATABASE_URL: `...@localhost:5433/...`

### Container Won't Start
```bash
# Check logs
docker-compose logs postgres

# Remove and recreate
docker-compose down -v
docker-compose up -d
```

### Cannot Connect to Database
1. Check container is running: `docker-compose ps`
2. Check logs: `docker-compose logs postgres`
3. Wait 10 seconds after starting
4. Run: `python test/test_db_connection.py`

---

## 💾 Backup and Restore

### Backup Database
```bash
docker exec fastapi_postgres pg_dump -U postgres fastapi_db > backup.sql
```

### Restore Database
```bash
docker exec -i fastapi_postgres psql -U postgres fastapi_db < backup.sql
```

---

## 🎯 Production Notes

**⚠️ This setup is for development only!**

For production:
1. Use strong passwords
2. Don't expose PostgreSQL port publicly
3. Use managed database services (Supabase, AWS RDS, etc.)
4. Set up regular backups
5. Use SSL connections
6. Configure proper user permissions

---

## ✨ You're All Set!

Your local PostgreSQL database is ready to use with your FastAPI backend!

**Next Steps:**
1. Start Docker: `docker-compose up -d`
2. Start FastAPI: `uvicorn app.main:app --reload`
3. Open API Docs: http://localhost:8000/docs
4. Start coding! 🚀

