# 🐳 PostgreSQL Database Setup

This folder contains the Docker configuration for PostgreSQL database and pgAdmin web interface.

---

## 🚀 Quick Start

### Start Database
```bash
./start.sh
```

### Stop Database
```bash
./stop.sh
```

### Restart Database
```bash
./restart.sh
```

### Check Status
```bash
./status.sh
```

---

## 📊 Access Your Database

### Option 1: pgAdmin Web UI (Recommended for Chrome)

1. **Start the database:**
   ```bash
   ./start.sh
   ```

2. **Open in Chrome:**
   ```
   http://localhost:5050
   ```

3. **Login:**
   - Email: `admin@admin.com`
   - Password: `admin`

4. **Add Server Connection:**
   - Right-click "Servers" → "Register" → "Server"
   - **General Tab:**
     - Name: `FastAPI Local DB`
   - **Connection Tab:**
     - Host name/address: `postgres` (or `host.docker.internal` on Mac/Windows)
     - Port: `5432`
     - Maintenance database: `fastapi_db`
     - Username: `postgres`
     - Password: `postgres123`
   - Click "Save"

5. **Browse Tables:**
   - Expand "FastAPI Local DB" → "Databases" → "fastapi_db" → "Schemas" → "public" → "Tables"
   - Right-click on `users` table → "View/Edit Data" → "All Rows"

### Option 2: Command Line (psql)

```bash
# Access database via Docker
docker exec -it fastapi_postgres psql -U postgres -d fastapi_db

# Then run SQL commands
\dt                    # List tables
\d users              # Describe users table
SELECT * FROM users;   # Query users
\q                    # Quit
```

---

## 🔧 Database Connection Details

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

## 📁 Files

- `docker-compose.yml` - Docker configuration
- `start.sh` - Start database script
- `stop.sh` - Stop database script
- `restart.sh` - Restart database script
- `status.sh` - Check status script
- `README.md` - This file

---

## 🛠️ Docker Commands (Alternative)

If you prefer using Docker commands directly:

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart
docker-compose restart
```

---

## 🌐 View Tables in Chrome

### Using pgAdmin (Easiest)

1. Start database: `./start.sh`
2. Open Chrome: http://localhost:5050
3. Login and connect to database
4. Browse tables visually

### Using Direct SQL Query

1. In pgAdmin, open Query Tool
2. Run: `SELECT * FROM users;`
3. View results in table format

---

## 🐛 Troubleshooting

### Port 5432 Already in Use
```bash
# Check what's using the port
lsof -i :5432

# Stop local PostgreSQL if running
brew services stop postgresql@14
```

### Can't Access pgAdmin
- Make sure containers are running: `./status.sh`
- Check if port 5050 is available: `lsof -i :5050`
- Try: http://127.0.0.1:5050 instead

### Database Connection Failed
- Wait 10 seconds after starting
- Check logs: `docker-compose logs postgres`
- Verify containers are healthy: `docker-compose ps`

---

## 💾 Data Persistence

Your database data is stored in Docker volumes and persists even after stopping containers.

To completely remove data:
```bash
docker-compose down -v
```

---

## 🔐 Security Note

⚠️ **This setup is for DEVELOPMENT only!**

- Default passwords are used
- Database is exposed on localhost
- No SSL/TLS encryption

For production, use:
- Strong passwords
- Managed database services
- Proper security configurations

---

## 📚 Related Documentation

- Main project: `../README.md`
- FastAPI setup: `../QUICKSTART_DOCKER.md`
- Docker details: `../DOCKER_SETUP.md`

---

## ✨ Quick Reference

```bash
# Start everything
./start.sh

# Open in Chrome
open http://localhost:5050

# Stop everything
./stop.sh
```

Happy coding! 🚀

